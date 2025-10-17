
"""
Voice-controlled ESP32 lab automation.

Listens for voice commands via microphone and sends HTTP requests to
an ESP32 web server to control connected devices (lights, fans, etc).

Usage:
    python voice_controller.py --ip 192.168.0.172 --verbose
"""

from __future__ import annotations

import argparse
import logging
import re
import signal
import sys
import time
from typing import Dict, Iterable, Optional

import requests
import speech_recognition as sr
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


DEFAULT_ESP32_IP = "192.168.0.172"
DEFAULT_AMBIENT_DURATION = 2.0
DEFAULT_TIMEOUT = 5.0
DEFAULT_PAUSE = 0.1


def build_session(
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = 3
) -> requests.Session:
    """
    Create an HTTP session with automatic retries.
    
    Helps recover from transient network issues without manual intervention.
    """
    s = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 503, 504)
    )
    s.mount("http://", HTTPAdapter(max_retries=retry_strategy))
    s.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    s.request_timeout = timeout  # type: ignore[attr-defined]
    return s


class VoiceController:
    """Handles voice recognition and device control."""

    def __init__(
        self,
        esp32_ip: str,
        recognizer: Optional[sr.Recognizer] = None,
        mic: Optional[sr.Microphone] = None
    ):
        self.esp32_ip = esp32_ip
        self.recognizer = recognizer or sr.Recognizer()
        self.mic = mic or sr.Microphone()
        self.session = build_session()
        self.running = True

        # Map voice commands to ESP32 endpoints (relay wiring)
        # Relay Channel 1 (GPIO 32): Light
        # Relay Channel 2 (GPIO 33): Fan
        # Order matters - more specific phrases should come first
        self.command_map: Dict[Iterable[str], str] = {
            ("turn everything on", "turn all on", "all on"): "all/on",
            ("turn everything off", "turn all off", "all off"): "all/off",
            ("led on", "turn on led", "turn led on"): "led/on",
            ("led off", "turn off led", "turn led off"): "led/off",
            ("light on", "turn on light", "turn light on"): "light/on",
            ("light off", "turn off light", "turn light off"): "light/off",
            ("fan on", "turn on fan"): "fan/on",
            ("fan off", "turn off fan"): "fan/off",
        }

    def _match_command(self, text: str) -> Optional[str]:
        """
        Try to match user's speech to a known command.
        Returns the endpoint path if found, None otherwise.
        """
        text = text.lower()
        
        # Check direct substring matches first (handles extra words gracefully)
        for phrases, endpoint in self.command_map.items():
            for p in phrases:
                if p in text:
                    return endpoint
        
        # Fallback: regex patterns for natural variations
        if re.search(r"\b(turn|switch) .* all .* on\b", text):
            return "all/on"
        if re.search(r"\b(turn|switch) .* all .* off\b", text):
            return "all/off"
        
        return None

    def send_command(self, path: str) -> bool:
        """Send HTTP request to ESP32. Returns True if successful."""
        url = f"http://{self.esp32_ip}/{path}"
        try:
            logging.debug("Sending request to %s", url)
            resp = self.session.get(url, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            logging.info("Command sent: %s (status=%s)", path, resp.status_code)
            return True
        except requests.RequestException as exc:
            logging.warning("Failed to send command %s: %s", path, exc)
            return False

    def adjust_ambient(self, duration: float = DEFAULT_AMBIENT_DURATION) -> None:
        """Calibrate microphone for background noise."""
        logging.info("Calibrating microphone (%.1fs)...", duration)
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=duration)

    def listen_once(self) -> Optional[str]:
        """
        Listen for one utterance and return the recognized text.
        Returns None if speech wasn't understood or request failed.
        """
        with self.mic as source:
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio)
            logging.info("Heard: %s", text)
            return text.lower()
        except sr.UnknownValueError:
            logging.debug("Couldn't understand that")
            return None
        except sr.RequestError as exc:
            logging.error("Speech recognition service error: %s", exc)
            return None

    def run(
        self,
        ambient_duration: float = DEFAULT_AMBIENT_DURATION,
        pause: float = DEFAULT_PAUSE
    ) -> None:
        """Main loop - listen for commands and execute them."""
        logging.info("Starting voice controller (ESP32=%s)", self.esp32_ip)
        self.adjust_ambient(ambient_duration)
        logging.info("Ready - speak a command (Ctrl-C to exit)")

        while self.running:
            text = self.listen_once()
            if not text:
                time.sleep(pause)
                continue

            endpoint = self._match_command(text)
            if not endpoint:
                continue
            
            # Handle bulk commands by sending multiple requests
            if endpoint == "all/on":
                logging.info("Activating all devices")
                for e in ("led/on", "light/on", "projector/on", "fan/on"):
                    self.send_command(e)
                    time.sleep(0.1)
            elif endpoint == "all/off":
                logging.info("Deactivating all devices")
                for e in ("led/off", "light/off", "projector/off", "fan/off"):
                    self.send_command(e)
                    time.sleep(0.1)
            else:
                self.send_command(endpoint)

    def stop(self) -> None:
        """Stop the main loop gracefully."""
        logging.info("Shutting down")
        self.running = False


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Voice-controlled ESP32 lab automation"
    )
    p.add_argument(
        "--ip",
        default=DEFAULT_ESP32_IP,
        help="ESP32 IP address or hostname"
    )
    p.add_argument(
        "--ambient",
        type=float,
        default=DEFAULT_AMBIENT_DURATION,
        help="Seconds to calibrate for ambient noise"
    )
    p.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show debug output"
    )
    return p.parse_args(list(argv) if argv else None)


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(message)s"
    )


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    setup_logging(args.verbose)

    controller = VoiceController(args.ip)

    def handle_interrupt(sig, frame):
        controller.stop()

    signal.signal(signal.SIGINT, handle_interrupt)

    try:
        controller.run(ambient_duration=args.ambient)
    except Exception:
        logging.exception("Unexpected error")
        return 2
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
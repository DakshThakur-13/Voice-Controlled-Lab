#  Voice Controlled Lab

[![CI](https://github.com/YOUR_USERNAME/Voice_Controlled_Lab/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/Voice_Controlled_Lab/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A voice-controlled automation system for laboratory equipment using Python speech recognition and ESP32 microcontroller.

##  Features

-  **Voice Control**: Natural language commands for device control
-  **ESP32 Integration**: Web-based device control via HTTP
-  **Bulk Operations**: Control all devices with a single command
-  **Logging & Monitoring**: Comprehensive logging and health checks
-  **Tested**: Unit tests with pytest
-  **Configurable**: CLI arguments and environment variables

##  Quick Start

### Prerequisites

- Python 3.9 or higher
- ESP32 development board
- Arduino IDE or PlatformIO
- Microphone (for voice recognition)

### Python Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Voice_Controlled_Lab.git
cd Voice_Controlled_Lab
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the voice controller:
```bash
python voice_controller.py --ip YOUR_ESP32_IP
```

### ESP32 Setup

1. Open `lab_controller_esp32/lab_controller_esp32.ino` in Arduino IDE
2. Create `lab_controller_esp32/secrets.h` with your Wi-Fi credentials:
```cpp
const char* ssid = "Your_SSID";
const char* password = "Your_Password";
```
3. Upload to your ESP32
4. Note the IP address from Serial Monitor

##  Usage

### Voice Commands

| Command | Action |
|---------|--------|
| "LED on/off" | Control LED |
| "Light on/off" | Control light |
| "Projector on/off" | Control projector |
| "Fan on/off" | Control fan |
| "Turn everything on/off" | Control all devices |

### Command Line Options

```bash
python voice_controller.py --help
```

Options:
- `--ip`: ESP32 IP address (default: 192.168.0.172)
- `--ambient`: Ambient noise adjustment duration in seconds
- `--verbose`: Enable debug logging

##  Development

### Running Tests

```bash
pytest -v
```

### Code Style

```bash
flake8 voice_controller.py
```

##  Hardware Wiring

| Device | GPIO Pin |
|--------|----------|
| LED | 25 |
| Projector | 33 |
| Fan | 32 |
| Light | 21 |

##  Security

- Wi-Fi credentials are stored in `secrets.h` (not tracked by git)
- Use HTTPS for production deployments
- Run on trusted networks only

##  Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- Built with [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- ESP32 WebServer library
- Arduino community

##  Support

-  [Report a bug](https://github.com/YOUR_USERNAME/Voice_Controlled_Lab/issues)
-  [Request a feature](https://github.com/YOUR_USERNAME/Voice_Controlled_Lab/issues)
-  [Documentation](https://github.com/YOUR_USERNAME/Voice_Controlled_Lab/wiki)

---

Made with  by the Voice Controlled Lab team

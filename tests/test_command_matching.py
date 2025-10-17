import pytest
from unittest.mock import Mock

from voice_controller import VoiceController


@pytest.fixture
def vc():
    # Mock mic to avoid pyaudio dependency in tests
    mock_mic = Mock()
    return VoiceController("127.0.0.1", mic=mock_mic)


@pytest.mark.parametrize("phrase,expected", [
    ("LED on", "led/on"),
    ("turn led off", "led/off"),
    ("please turn the light on", "light/on"),
    ("projector off now", "projector/off"),
    ("fan on please", "fan/on"),
    ("turn everything on", "all/on"),
    ("can you turn everything off", "all/off"),
])
def test_match_simple(vc, phrase, expected):
    assert vc._match_command(phrase) == expected


def test_no_match(vc):
    assert vc._match_command("play music") is None

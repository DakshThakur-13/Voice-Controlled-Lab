# Changelog

All notable changes to this project will be documented in this file.

## Repository

GitHub: https://github.com/DakshThakur-13/Voice-Controlled-Lab

## [Unreleased]
- Initial public release

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-17

### Added
- Initial release of Voice Controlled Lab
- Python voice controller with speech recognition
- ESP32 web server for device control (LED, light, projector, fan)
- Support for individual device control and all on/off commands
- Logging, CLI arguments, and configurable settings
- HTTP session with automatic retries
- Unit tests for command matching logic
- Comprehensive documentation (README, CONTRIBUTING, CODE_OF_CONDUCT)
- MIT License

### Features
- Voice commands: LED on/off, light on/off, projector on/off, fan on/off
- Bulk commands: turn everything on/off
- ESP32 status endpoint for health checks
- Configurable ambient noise adjustment
- Graceful shutdown handling

### Security
- Wi-Fi credentials template with .gitignore protection
- Recommendation to use secrets management

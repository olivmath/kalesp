# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned
- KALE blockchain integration
- Optimized Keccak-256 implementation for ESP32
- Automatic Stellar transaction orchestration
- Distributed ESP32 network
- Pool mining system for small devices

## [0.1.0] - 2025-01-XX

### Added
- **ESP32 Firmware** in Rust with support for:
  - SHA-256 and Keccak-256 algorithms
  - Robust serial communication
  - Basic mining commands
  - Difficulty configuration (prefixed zeros)
- **Python Interface** with:
  - Modern GUI using Flet
  - Serial communication with ESP32
  - Real-time monitoring
  - Auto-detection of serial ports
- **ESP32 Commands**:
  - `help` - List of available commands
  - `info` - Device information
  - `reset` - System reset
  - `mine` - Start mining
  - `zeros <n>` - Difficulty configuration
  - `entropy <hex>` - Entropy definition
  - `hash <algo>` - Algorithm selection
- **Complete Documentation**:
  - README.md with installation and usage instructions
  - LORE.md with project narrative context
  - ROADMAP.md with KALE integration plans
  - CHANGELOG.md for version control
- **Development Configuration**:
  - Cargo.toml for ESP32 with optimized dependencies
  - requirements.txt for Python interface
  - Comprehensive .gitignore
  - MIT License

### Technical Features
- **Modular architecture** prepared for expansion
- **Optimized serial communication** protocol
- **Structured logging** system
- **Responsive interface** with real-time feedback
- **Cross-platform support** (macOS, Linux, Windows)

### Development Notes
- Project serves as foundation for future KALE integration
- Current implementation focused on proof of concept
- Architecture prepared for distributed mining
- Code optimized for ESP32 performance

---

## Types of Changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities
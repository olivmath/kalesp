# Contributing to KALESP

🎉 Thank you for considering contributing to KALESP! This project is part of the KALE ecosystem and aims to democratize mining through ESP32 devices.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Environment Setup](#environment-setup)
- [Development Process](#development-process)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project adheres to the **Proof-of-Teamwork** principles of the KALE ecosystem. We expect all participants to:

- 🤝 Be respectful and inclusive
- 🌱 Focus on collaboration and mutual growth
- 🔧 Prioritize solid technical solutions
- 🌍 Maintain the vision of decentralization and accessibility

## 🚀 How Can I Contribute?

### 🐛 Reporting Bugs

Before reporting a bug:
1. Check if a similar issue doesn't already exist
2. Test with the latest version
3. Collect system information (OS, Python version, ESP32 model)

**Bug Report Template:**
```markdown
**Bug Description**
Clear and concise description of the problem.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Execute '...'
4. See error

**Expected Behavior**
What should happen.

**Screenshots/Logs**
If applicable, add screenshots or logs.

**Environment:**
- OS: [e.g. macOS 14.0]
- Python: [e.g. 3.11.0]
- ESP32: [e.g. DevKit v1]
- KALESP Version: [e.g. 0.1.0]
```

### 💡 Suggesting Improvements

**Feature Request Template:**
```markdown
**Related Problem**
Describe the problem this feature would solve.

**Proposed Solution**
Describe the solution you would like to see.

**Alternatives Considered**
Describe alternatives you considered.

**Additional Context**
Any other context about the feature.
```

### 🔧 Contributing Code

Areas where contributions are especially welcome:

#### ESP32 Firmware (Rust)
- Hash algorithm optimizations
- Serial communication protocol improvements
- New command implementations
- Performance and memory optimizations

#### Python Interface
- GUI improvements with Flet
- New monitoring features
- External API integrations
- Automated testing

#### KALE Integration
- Stellar protocol implementation
- KALE smart contract integration
- Transaction orchestration system
- Distributed ESP32 network

## 🛠️ Environment Setup

### Prerequisites
```bash
# Rust and ESP32 tools
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install espup
espup install
source $HOME/export-esp.sh
cargo install espflash

# Python and dependencies
python3 -m pip install --upgrade pip
cd interface
pip install -r requirements.txt
```

### Fork and Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/kalesp.git
cd kalesp

# Add the original repository as upstream
git remote add upstream https://github.com/ORIGINAL_OWNER/kalesp.git
```

## 🔄 Development Process

### 1. Create a Branch
```bash
git checkout -b feature/feature-name
# or
git checkout -b fix/bug-name
# or
git checkout -b docs/documentation-improvement
```

### 2. Make Your Changes
- Keep commits small and focused
- Use descriptive commit messages
- Test your changes locally

### 3. Test
```bash
# Test ESP32 firmware
cd esp
cargo check
cargo build --release

# Test Python interface
cd ../interface
python -m pytest  # if tests exist
python esp32_gui.py  # manual test
```

### 4. Commit and Push
```bash
git add .
git commit -m "feat: add new functionality X"
git push origin feature/feature-name
```

### 5. Open a Pull Request
- Use the PR template
- Clearly describe the changes
- Reference related issues
- Wait for review and feedback

## 📝 Code Standards

### Rust (ESP32)
```rust
// Use snake_case for functions and variables
fn calculate_hash_rate() -> u32 {
    // Code here
}

// Use PascalCase for structs and enums
struct MiningConfig {
    difficulty: u8,
    algorithm: HashAlgorithm,
}

// Document public functions
/// Calculates the Keccak-256 hash of the provided data
/// 
/// # Arguments
/// * `data` - The data to hash
/// 
/// # Returns
/// * `[u8; 32]` - The resulting hash
pub fn keccak256(data: &[u8]) -> [u8; 32] {
    // Implementation
}
```

### Python (Interface)
```python
# Use snake_case for functions and variables
def connect_to_esp32(port: str) -> bool:
    """Connects to ESP32 serial port.
    
    Args:
        port: Serial port path (e.g., '/dev/ttyUSB0')
        
    Returns:
        True if connected successfully, False otherwise
    """
    pass

# Use PascalCase for classes
class ESP32Manager:
    """Manages communication with ESP32 devices."""
    
    def __init__(self, port: str, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
```

### Commit Messages
Use the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```
feat: add support for Keccak-256 algorithm
fix: fix bug in serial communication
docs: update README with installation instructions
style: format Rust code with rustfmt
refactor: reorganize module structure
test: add tests for hash function
chore: update Cargo.toml dependencies
```

## 🧪 Testing

### Unit Tests (Rust)
```bash
cd esp
cargo test
```

### Integration Tests (Python)
```bash
cd interface
python -m pytest tests/
```

### Manual Tests
1. Compile and flash firmware to ESP32
2. Run Python interface
3. Test all available commands
4. Check logs and expected behavior

## 📚 Documentation

### Updating Documentation
- Keep README.md updated
- Document new features
- Update CHANGELOG.md
- Add code comments

### Documentation Standards
- Use Markdown for documentation
- Include code examples
- Keep language clear and concise
- Add diagrams when necessary

## 🎯 Priority Areas

### High Priority
- Hash algorithm optimization
- Serial communication stability improvements
- Implementation of new mining algorithms
- Automated testing

### Medium Priority
- More intuitive graphical interface
- Support for more ESP32 types
- Detailed technical documentation
- Usage examples

### Low Priority
- Interface themes
- Experimental features
- Integrations with other tools
- Minor performance optimizations

## 🤔 Questions?

If you have questions about how to contribute:

1. 📖 Read existing documentation
2. 🔍 Search for similar issues
3. 💬 Open an issue for discussion
4. 📧 Contact the maintainers

---

**Remember**: Every contribution, no matter how small, is valuable! From typo fixes to complex feature implementations, everything helps strengthen the **Proof-of-Teamwork** spirit of KALESP.

🚀 **Let's build the future of decentralized mining together!**
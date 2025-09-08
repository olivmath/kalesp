# KALE ESP32 Miner Integration Plan (kalesp)

## 🎯 Objective
Integrate ESP32 as a KALE miner by reusing logic from existing repositories:
- **ESP32**: Executes Keccak-256 mining to find nonces
- **Python Host**: Orchestrates Stellar transactions (plant, work, harvest) using stellar_sdk + Launchtube

## 📋 KALE Repositories Analysis

### 🥬 KALE-sc (Smart Contract)
**Location**: `/Users/olivmath/dev/esp/KALE-sc/`

**Mining Flow**:
1. **`plant(farmer, amount)`**: Initial stake, requires farmer auth
2. **`work(farmer, hash, nonce)`**: Submits proof-of-work, no auth (can be called by third parties)
3. **`harvest(farmer, index)`**: Collects block rewards

**Critical Parameters**:
- **Block Index**: Current block index
- **Entropy**: Previous block hash (32 bytes)
- **Farmer Address**: Miner's Stellar address (32 bytes)
- **Nonce**: Value to be tested (8 bytes)
- **Hash**: Keccak-256 result (32 bytes)

**Input Data Structure** (76 bytes total):
```
[0-3]   Block Index (4 bytes, big-endian)
[4-11]  Nonce (8 bytes, big-endian)
[12-43] Entropy (32 bytes)
[44-75] Farmer Address (32 bytes)
```

**Hash Validation**:
- Support for SHA256 and Keccak-256 of the 76 input bytes
- Prefixed zeros counting (nibbles)
- More zeros = greater contribution to reward
- Algorithm configurable via `hash` command

### 🦀 kale-farmer (Rust Reference)
**Location**: `/Users/olivmath/dev/esp/kale-farmer/`

**Main Components**:
- **Rust Miner** (`src/main.rs`): Parallel mining with Keccak-256
- **Bun Scripts**: plant/work/harvest orchestration
- **Stellar SDK**: Stellar blockchain integration

**Orchestration Logic**:
- Monitors new blocks every 5 seconds
- Automatic plant at new block start
- Work with ~4.7 minute delay for maturation
- Harvest from previous block

### ⚡ kale-miner (C++/GPU Reference)
**Location**: `/Users/olivmath/dev/esp/kale-miner/`

**Keccak-256 Implementations**:
- **Optimized CPU**: `utils/keccak_opt.h` (~49 MH/s Intel i9)
- **Portable CPU**: `utils/keccak.h` (~42 MH/s Intel i9)
- **CUDA Kernel**: `utils/keccak.cuh` (~1.9 GH/s RTX 4080)
- **OpenCL Kernel**: `utils/keccak.cl` (~1.3 GH/s RTX 4080)

### 🔧 kalesp (Current Project)
**Location**: `/Users/olivmath/dev/esp/kalesp/`

**Current State**:
- **ESP32 Firmware**: Rust with basic serial communication
- **Python Interface**: GUI with Flet + serial communication
- **Implemented Commands**: help, info, reset, zeros, entropy, hash, mine

## 🏗️ Proposed Architecture

### ESP32 (Rust Firmware)
**Responsibilities**:
- Receive mining parameters via serial
- Execute optimized Keccak-256 loop
- Return best nonce found
- Report progress and statistics

**Input**:
```
START_MINING <block_index> <entropy_hex> <farmer_hex> <difficulty> <batch_size>
```

**Output**:
```
MINE_PROGRESS <nonces_tested> <best_zeros> <hashrate>
MINE_RESULT <nonce> <hash_hex> <zeros_count>
MINE_ERROR <error_message>
```

### Python Host (Orchestrator)
**Responsibilities**:
- Monitor Stellar blockchain for new blocks
- Execute plant → work → harvest sequence
- Manage serial communication with ESP32
- Sign and submit transactions via Launchtube
- Persist state and recover from failures

**Modules**:
- `stellar_client.py`: Stellar SDK + Launchtube integration
- `mining_orchestrator.py`: Mining cycle logic
- `esp32_manager.py`: Serial communication with ESP32
- `state_manager.py`: State persistence

## 📋 Detailed Task List

### 🔴 High Priority

1. **Analyze KALE Functional Requirements**
   - Study plant → work → harvest flow
   - Map input parameters (block index, entropy, farmer, nonce)
   - Understand reward calculation and deadlines
   - Document contract rules

2. **Extract Mining Logic**
   - Keccak-256 algorithm from existing repositories
   - Data preparation (76 bytes: index + nonce + entropy + farmer)
   - Prefixed zeros counting
   - Difficulty criteria

3. **Define Detailed Architecture**
   - ESP32 vs Python responsibilities
   - Data formats and protocols
   - Integration points
   - Data flow

4. **Specify Serial Protocol**
   - Messages (start/stop mining, job parameters, progress)
   - Binary vs text format
   - Sizes, checksums, timeouts
   - Error handling

5. **Port Keccak-256 to ESP32**
   - Implement in Rust no_std or optimized C
   - Evaluate performance and memory usage
   - Ensure equivalence with references
   - Test endianness and data layout

6. **Implement Stellar Python Client**
   - Module for plant/work/harvest transactions
   - Integration with stellar_sdk
   - Launchtube support
   - Retry logic and backoff

7. **Develop Mining Orchestration**
   - Plant and maturation timing
   - Work submission strategy
   - Harvest timing
   - Windows and rate limits

8. **Ensure Security**
   - Keys only on host (never on ESP)
   - Protection of .env variables
   - Launchtube token protection
   - Logs without sensitive information

### 🟡 Medium Priority

9. **Create Test Vectors**
   - Generate test cases from existing miners
   - Validate hash equivalence
   - Verify zeros counting
   - Regression tests

10. **Implement State Persistence**
    - File/DB for per-account state
    - Last block, best nonce/hash
    - Stakes and recent errors
    - Failure recovery

### 🟢 Low Priority

11. **Improve Telemetry/GUI**
    - Real-time hashrate
    - Transaction status
    - Connection indicators
    - Performance metrics

12. **Build/Flash Pipeline**
    - Makefile for ESP32 firmware
    - Python environment setup
    - Prerequisites documentation

13. **Performance Metrics**
    - ESP32 hashrate target
    - Host→tx latency
    - 24h stability
    - Transaction failure rate

14. **Automated Testing**
    - Unit tests (Keccak/zeros)
    - Integration tests (serial)
    - Complete flow tests

15. **Error Handling**
    - Plant/harvest retry
    - Difficulty adjustment
    - ESP disconnection fallback
    - Work buffers

16. **Multi-account Compatibility**
    - Job queue for multiple farmers
    - ESP concurrency limits
    - State isolation

17. **Observability**
    - Structured logs
    - Log rotation
    - Hashrate and success counters
    - Optional export (file/HTTP)

18. **Support Repo Integration**
    - Equivalence bridge with kale-miner
    - Timing strategies from kale-farmer
    - Maintain compatibility without full copy

## ✅ Minimum Acceptance Criteria

### Functional

- [x] ESP32 executes Keccak-256 mining equivalent to existing miners
- [x] Python Interact and Control ESP32 Mineration
- [x] GUI for control ESP32
- [ ] Python orchestrates plant → work → harvest
- [ ] Integrate Python to Transactions submitted via Launchtube successfully

### Performance
- [ ] ESP32: >100 KH/s (conservative target)
- [ ] Plant→work latency: <30s
- [ ] Uptime: >95% in 24h
- [ ] Transaction success rate: >90%

### Security
- [ ] Private keys never on ESP32
- [ ] Logs without secret exposure
- [ ] Robust input validation
- [ ] Account isolation

## ⚠️ Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Limited ESP32 performance | High | Optimize Keccak in C/Rust, adjust difficulty |
| Hash divergence | High | Early validation with test vectors |
| Network/tx failures | Medium | Retries, backoff, visual alerts |
| Endianness/layout | Medium | Equivalence tests with references |
| Serial overhead | Low | Optimized binary protocol |

## 📅 Estimated Timeline

### Week 1-2: Analysis and Design
- Complete study of KALE repositories
- Detailed architecture definition
- Protocol specification
- Development environment setup

### Week 3-4: Core Development
- Port Keccak-256 to ESP32
- Serial communication implementation
- Basic Stellar Python client
- Fundamental unit tests

### Week 5-6: Integration
- Complete mining orchestration
- ESP32↔Python integration tests
- Stellar testnet validation
- Performance refinement

### Week 7-8: Polish
- Robust error handling
- Complete documentation
- Stability tests
- Production preparation

## 🚀 Next Steps

1. **Phase 1 - Analysis**: Consolidate data mapping and input preparation
2. **Phase 2 - Prototyping**: Implement basic Keccak on ESP32
3. **Phase 3 - Integration**: Develop serial protocol and Python client
4. **Phase 4 - Testing**: Validate equivalence and execute flow tests
5. **Phase 5 - Production**: Deploy on testnet/mainnet with monitoring

---

**Goal**: Transform ESP32 into a functional KALE miner, reusing maximum logic from existing repositories, with focus on simplicity, performance and reliability.

**Status**: 📋 Complete Planning - Ready for Implementation
**Last Update**: January 2025
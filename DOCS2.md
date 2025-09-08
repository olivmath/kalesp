# KALE Integration Plan for ESP (kalesp)

## Objective
- Reuse KALE repositories' mining logic to enable ESP to search for nonces (hashing/Keccak) while Python host (stellar_sdk + Launchtube) handles on-chain transactions (plant, work, harvest). Current focus: planning and requirement mapping only.

## Target Architecture (high-level)
- ESP32 (Rust firmware in kalesp/esp): Receives block data + parameters, runs Keccak-256 loop on nonce(s), returns best candidate (hash, nonce, zeros, stats) via serial.
- Host (kalesp/interface in Python):
  - Orchestrator: Gets block/contract data, schedules plant, waits for optimal window, sends work with best hash, then sends harvest.
  - Connects to ESP via serial (python_serial.py), displays telemetry (esp32_gui.py), uses stellar_sdk + Launchtube for transaction signing/submission.
- KALE Contract (esp/KALE-sc): Reference for rules and flow (plant → work → harvest).

## Workspace References
- Logic/Strategies: esp/kale-farmer (Rust + Bun scripts), esp/kale-miner (C++/GPU, Keccak routines, zero checking, data preparation)
- Contract & Rules: esp/KALE-sc (README and contract code)
- Target Project: esp/kalesp (firmware in esp/src, Python interface in interface/)

## Task List (Planning Only)
1. Map KALE functional requirements: plant → work → harvest sequence, reward calculations, deadlines (from KALE-sc/README and contract code)
2. Extract mining logic: hash input assembly (header, block/hash base64, miner id, nonce), prefix zero counting, difficulty criteria (kale-farmer and kale-miner)
3. Define detailed architecture: ESP vs Python responsibilities, data formats, integration points, host state persistence
4. Specify ESP↔Python serial protocol: messages (start/stop, job, progress), binary vs text, sizes, checksums, timeouts, error handling, protocol versioning
5. Plan Keccak ESP port: Rust no_std/ESP-IDF vs optimized C; performance/memory evaluation; layout/endianness for reference miner equivalence
6. Define test vectors and equivalence: generate kale-farmer/kale-miner cases, validate ESP produces identical hash/zeros for same inputs
7. Plan Python Stellar client: plant/work/harvest build/sign/send module with stellar_sdk, Launchtube integration (.env token), retries and backoff
8. Cycle orchestration: planting timing, ripening wait, work submission strategy (best-only vs updates), harvest timing - including window and rate limits
9. Host persistence: light file/DB for per-account state (last block, best nonce/hash, stakes, recent errors) and failure recovery
10. Security: host-only keys (never on ESP), .env variables, Launchtube token protection, secret-free logs, dump cleanup
11. Telemetry/GUI: extend esp32_gui.py for hashrate, temperature, uptime, best zeros, tx status, errors; serial and network connection indicators
12. Build/flash pipeline: Makefile/justfile for ESP firmware compilation/flashing and Python venv setup; prerequisites documentation
13. Performance/acceptance metrics: ESP hashrate target, host→tx latency, 24h stability, tx failure rate, power consumption
14. Automated testing: unit tests (Keccak/zeros), integration (serial loopback, ESP mock), complete flow tests on futurenet/testnet
15. Error handling and recovery: plant/harvest retry, difficulty adjustment, ESP disconnect fallback, work buffers
16. Multi-account compatibility: job queue for multiple farmers (sequential per account), ESP concurrency limits
17. Observability: structured host logs, log levels/rotation; hashrate and tx success counters; optional export (file/HTTP)
18. Support repo integration planning: maintain equivalence bridge with kale-miner (data prep/check) and kale-farmer (parameters/timing strategy) without full copy

## Minimum Acceptance Criteria
- ESP correctly finds/returns nonces with reference-identical zero verification
- Host executes plant → work → harvest cycle with host keys and Launchtube, on futurenet/testnet, with retries and logging
- GUI displays hashrate and status without freezing, 24h operation with auto-reconnect

## Risks and Mitigations
- Limited ESP performance: adjust difficulty/batch; optimize Keccak in C/Rust; reduce serial overhead
- Hash divergence (endianness/layout): early validation with test vectors and reference tools
- Network/tx failures: retries, backoff, telemetry and visual alerts

## Next Steps
- Consolidate block data mapping and input preparation (kale-miner/kale-farmer), draft serial protocol and equivalence test criteria

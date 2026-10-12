# Security Policy

## Supported Versions

This project is actively maintained as part of the **BCSE303L - Operating Systems Laboratory** curriculum at Vellore Institute of Technology (VIT). Security patches and concurrency bug fixes are applied to the active branches below:

| Branch / Release | Supported          |
| :--------------- | :----------------- |
| `main`           | :white_check_mark: |
| Feature branches | :x:                |

---

## Scope & Security Posture

This project benchmarks low-level POSIX concurrency primitives, CPU cache coherence protocols, and synchronization mechanisms in C. 

The software operates under the following security and safety boundaries:
1. **Unprivileged Execution:** All testbeds and benchmarks run entirely in non-root user space. No kernel modifications, `sudo` access, or privileged capabilities (`CAP_SYS_ADMIN`) are required.
2. **Memory Safety & Race Conditions:** Intentional data races exist exclusively inside `src/module1_concurrency_race_conditions/race_condition.c` for educational demonstration. Synchronized implementations (`mutex_sync.c`, `semaphore_sync.c`, `spinlock_atomic_sync.c`) must remain completely race-free and pass continuous integration checks under GCC/Clang ThreadSanitizer (`-fsanitize=thread`).
3. **Denial of Service / Spinlock Starvation:** Benchmarks under high core contention (16+ threads) consume heavy CPU cycles by design. They should not be deployed in production or resource-constrained shared environments without thread limits.

---

## Reporting a Vulnerability

If you discover a security flaw, unauthorized privilege escalation, memory corruption issue, or unexpected kernel deadlock behavior:

1. **Do not create a public GitHub issue.**
2. Send an email to the project maintainers:
   * **Sagnik Datta:** [sagnik.datta111@gmail.com](mailto:sagnik.datta111@gmail.com)
   * **Project Team:** [armoredglock@github.com](https://github.com/armoredglock)
3. Please include:
   * System architecture (CPU architecture, OS version, kernel release via `uname -r`).
   * Steps to reproduce the issue or minimal proof-of-concept code.
   * AddressSanitizer (ASan) or ThreadSanitizer (TSan) diagnostics trace, if applicable.

---

## Response Timeline

* **Acknowledgment:** Within 48 hours of report receipt.
* **Assessment & Reproduction:** Within 5 business days.
* **Fix & Advisory Release:** Verified patch merged to `main` with appropriate attribution.

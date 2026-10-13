# Multicore OS Concurrency and Synchronization Benchmarks

[![Multicore Concurrency CI/CD](https://github.com/armoredglock/multicore-os-concurrency/actions/workflows/ci.yml/badge.svg)](https://github.com/armoredglock/multicore-os-concurrency/actions/workflows/ci.yml)

Course project for **BCSE303L - Operating Systems Laboratory**, Vellore Institute of Technology (VIT).

This repository contains an empirical evaluation of race conditions, hardware cache coherence overheads (MESI protocol), and synchronization primitives (POSIX Mutexes, POSIX Counting Semaphores, hardware atomics, and cache-line alignment) across multicore architectures.

---

## Authors

* **Sagnik Datta** (Reg No: 24BCT0102) - Race condition testbed, POSIX mutex implementation, disassembly analysis, and ThreadSanitizer diagnostics.
* **Swati Saumya** (Reg No: 24BCI0253) - POSIX semaphore implementation, hardware atomics, false-sharing analysis (`alignas(64)`), and benchmark plotting.

---

## Project Structure

```
.
├── Makefile
├── .gitignore
├── README.md
├── .github/
│   └── workflows/
│       └── ci.yml                                  # GitHub Actions CI/CD automation workflow
├── bin/                                            # Compiled executable binaries (git-ignored)
├── docs/
│   ├── Review1_Summary.md                          # Review 1 concepts, architecture & viva Q&As
│   └── Review2_Official_Task_Allocation.md         # Review 2 milestone split between team members
├── src/
│   ├── module1_concurrency_race_conditions/
│   │   ├── race_condition.c                        # Unsynchronized counter with race condition
│   │   └── mutex_sync.c                            # POSIX Mutex implementation
│   └── module2_deadlock_and_bankers/
│       ├── semaphore_sync.c                        # POSIX Counting Semaphore implementation
│       └── spinlock_atomic_sync.c                  # Hardware atomics & cache false sharing
└── benchmarks/
    ├── benchmark_runner.py                         # Sweeps 1, 2, 4, 8, 16 threads & generates plots
    └── results/
        └── execution_time_comparison.png           # Generated timing & scalability chart
```

---

## Technical Overview

Modern multicore CPUs execute threads in true hardware simultaneity. Without synchronization, non-deterministic interleaving corrupts shared memory state. 

### 1. Assembly-Level Race Condition Disassembly
A simple C statement like `shared_counter++` is not atomic. On x86-64, GCC decomposes it into three distinct machine instructions:

```assembly
movq  shared_counter(%rip), %rax   # 1. Load counter from memory into register
addq  $1, %rax                     # 2. Increment in CPU ALU
movq  %rax, shared_counter(%rip)   # 3. Store register back to memory
```

When two cores execute this concurrently, both cores load the same initial value before either core stores its increment, silently dropping writes.

### 2. Synchronization Mechanisms Evaluated
* **Unsynchronized:** Baseline demonstrating silent counter corruption.
* **POSIX Mutex (`pthread_mutex_t`):** Fast user-space check via atomic instructions, falling back to kernel sleep (`sys_futex`) under contention.
* **POSIX Semaphore (`sem_t`):** Counting semaphore enforcing binary exclusion via `sem_wait` and `sem_post`.
* **Hardware Atomics:** Hardware bus-locking via `__sync_fetch_and_add`.
* **Cache Alignment (`alignas(64)`):** Eliminating false sharing where independent variables occupy the same 64-byte CPU cache line.

---

## Building the Project

### Prerequisites
* GCC (supporting C11 and POSIX threads)
* Make
* Python 3.8+ with Matplotlib (for benchmark graphing)

### Compilation
To compile all binaries into the `bin/` directory:

```bash
make
```

To compile individual targets:
```bash
make race        # Compiles bin/race_condition
make mutex       # Compiles bin/mutex_sync
make semaphore   # Compiles bin/semaphore_sync
make atomic      # Compiles bin/spinlock_atomic_sync
```

To clean generated binaries:
```bash
make clean
```

---

## Running the Benchmarks

All executables accept two optional arguments: `[num_threads]` and `[iterations_per_thread]`.

### 1. Race Condition Demonstration
```bash
./bin/race_condition 4 1000000
```
**Example Output:**
```
==================================================
   Unsynchronized Race Condition Benchmark       
==================================================
Threads Spawned      : 4
Increments / Thread  : 1000000
Expected Counter     : 4000000
Actual Final Counter : 1471944
Lost Updates         : 2528056 (63.20% corrupted)
Elapsed Time         : 3.305 ms
==================================================
```

### 2. POSIX Mutex
```bash
./bin/mutex_sync 4 1000000
```
**Example Output:**
```
==================================================
        POSIX Mutex Synchronization Benchmark     
==================================================
Threads Spawned      : 4
Increments / Thread  : 1000000
Expected Counter     : 4000000
Actual Final Counter : 4000000
Correctness Status   : VERIFIED (100% Consistent)
Elapsed Time         : 47.76 ms
Throughput           : 83.75 M ops/sec
==================================================
```

### 3. False Sharing vs. Cache Line Alignment
```bash
./bin/spinlock_atomic_sync 4 5000000
```
**Example Output:**
```
==============================================================
  Hardware Atomics & Cache Line False-Sharing Profiling      
==============================================================
Threads: 4 | Iterations per Thread: 5000000
--------------------------------------------------------------
1. Hardware Atomic (Bus Lock) :   140.49 ms (Count: 20000000)
2. False Sharing (Same 64B)   :     0.33 ms (Cache Bouncing)
3. Cache Aligned (alignas 64) :     0.23 ms (Isolated Line)
--------------------------------------------------------------
False Sharing Speedup Gain    : 1.45x faster with alignment
==============================================================
```

### 4. Automated Thread Scalability Sweep (1 to 16 Threads)
To run the automated sweep and generate the comparison graph:

```bash
python benchmarks/benchmark_runner.py
```

The resulting chart is saved to `benchmarks/results/execution_time_comparison.png`.

---

## ThreadSanitizer Diagnostics

To catch runtime memory races using Clang/GCC ThreadSanitizer:

```bash
gcc -O2 -fsanitize=thread -pthread src/module1_concurrency_race_conditions/race_condition.c -o bin/race_tsan
./bin/race_tsan
```

ThreadSanitizer intercepts uncoordinated memory accesses at runtime and outputs the call stacks for the conflicting writes.

---

## Continuous Integration (CI/CD)

The repository features an automated GitHub Actions workflow (`.github/workflows/ci.yml`) that triggers on every push and pull request to `main`. It automatically:
1. Compiles all C testbeds with `-Wall -Wextra` to ensure zero compilation warnings.
2. Runs the synchronization testbeds and verifies mathematical consistency.
3. Tests data-race interception via ThreadSanitizer.
4. Executes the Python benchmark suite and archives timing plots as build artifacts.

---

## References & Review Documentation

* **Review 1 Report & Viva Defense Guide:** [`docs/Review1_Summary.md`](docs/Review1_Summary.md)
* **Review 2 Milestone & Task Breakdown:** [`docs/Review2_Official_Task_Allocation.md`](docs/Review2_Official_Task_Allocation.md)
* **GitHub Issues for Review 2:** View open tasks directly in the [Issues tab](https://github.com/armoredglock/multicore-os-concurrency/issues).

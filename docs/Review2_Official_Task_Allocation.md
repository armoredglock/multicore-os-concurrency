# Official Task Allocation for OS Project Review 2

Based on **Section 7 (Methodology & Work Plan for Subsequent Reviews)** of the Course Project Review-1 Report:

> **Review 2 Deliverables:**  
> Development of C/POSIX testbed; demonstration of race conditions; implementation of mutexes/semaphores; hardware benchmarking of lock contention across 1–16 threads with timing graphs.
>
> *(Note: Dining Philosophers, Hierarchical Lock Ordering, and Banker's Algorithm are scheduled as **Review 3 Deliverables**).*

---

## 👥 Student Task Breakdown for Review 2

```
                              REVIEW 2 DELIVERABLES
               (C/POSIX Testbed, Race Conditions, Mutex/Semaphores,
                   and 1–16 Thread Contention Benchmarking)
                                      |
         +----------------------------+----------------------------+
         |                                                         |
  [SAGNIK DATTA (24BCT0102)]                                [SWATI SAUMYA (24BCI0253)]
  Race Testbed, Mutex & Diagnostics                         Semaphores, Spinlocks & Graphing
  • Race condition testbed (C/POSIX)                        • POSIX Semaphore implementation
  • Assembly disassembly (load-add-store)                   • Spinlock & atomic baseline
  • POSIX Mutex (`pthread_mutex_t`)                         • False sharing & cache alignment
  • ThreadSanitizer (`-fsanitize=thread`)                   • Semaphore & spinlock benchmarks (1-16)
  • Mutex latency & contention (1-16 threads)               • Unified Timing & Contention Graphs
```

---

### 1. Sagnik Datta (24BCT0102)
**Assigned Deliverable Modules:** Race Condition Demonstration, POSIX Mutex Implementation, Assembly Analysis & ThreadSanitizer Diagnostics

#### Detailed Responsibilities:
1. **Multi-Threaded Race Condition Testbed (`race_condition.c`):**
   * Write C program using POSIX threads where $N$ concurrent threads perform unsynchronized increments on a shared counter (`global_counter++`).
   * Demonstrate severe data divergence (e.g., expected 8,000,000 vs actual 3,124,500).
2. **Assembly Disassembly Analysis:**
   * Generate assembly listing (`objdump -d` or `gcc -S`) showing the 3 distinct x86-64 machine instructions:
     ```assembly
     movq  global_counter(%rip), %rax   # 1. Load from memory to register
     addq  $1, %rax                     # 2. Increment in ALU
     movq  %rax, global_counter(%rip)   # 3. Store register back to memory
     ```
   * Explain in viva how core interleaving between steps 1 and 3 leads to lost updates.
3. **POSIX Mutex Implementation (`mutex_sync.c`):**
   * Protect critical sections using `pthread_mutex_init`, `pthread_mutex_lock`, and `pthread_mutex_unlock`.
   * Verify mathematical correctness (final count matches expected count exactly).
4. **ThreadSanitizer Diagnostics:**
   * Compile testbed using `gcc -O2 -fsanitize=thread -lpthread race_condition.c -o race_tsan`.
   * Capture and document runtime data-race warnings and conflicting memory access stacks for the review report.
5. **Mutex Contention Profiling:**
   * Benchmark execution time and average acquisition latency of POSIX Mutex across 1, 2, 4, 8, and 16 threads.

---

### 2. Swati Saumya (24BCI0253)
**Assigned Deliverable Modules:** POSIX Semaphore Implementation, Spinlock / Cache Analysis & Comparative Benchmarking Graph Suite

#### Detailed Responsibilities:
1. **POSIX Counting Semaphore Implementation (`semaphore_sync.c`):**
   * Implement mutual exclusion using POSIX counting semaphores (`sem_init`, `sem_wait`, `sem_post`).
   * Verify correctness against the shared counter benchmark.
2. **Spinlock & Atomic Baseline (`spinlock_sync.c`):**
   * Implement spinlock synchronization (`pthread_spin_lock`, `pthread_spin_unlock`) and atomic instructions (`__sync_fetch_and_add` or C11 `stdatomic.h`).
   * Highlight the fundamental trade-off: busy-waiting (100% CPU usage, cache-bus storm) vs. kernel sleeping.
3. **False Sharing & Cache Alignment Experiment:**
   * Demonstrate the impact of false sharing when multiple threads modify adjacent variables within the same 64-byte cache line.
   * Apply `alignas(64)` padding and measure the performance speedup.
4. **Semaphore & Spinlock Contention Profiling:**
   * Benchmark execution time and throughput for Semaphores and Spinlocks across 1, 2, 4, 8, and 16 threads.
5. **Unified Timing & Contention Graph Suite:**
   * Collect all timing data across all 4 modes (Unsynchronized, Mutex, Semaphore, Spinlock/Cache-aligned).
   * Generate official publication-quality review plots using Python (Matplotlib):
     * **Graph 1:** Wall-Clock Execution Time vs Thread Count (1, 2, 4, 8, 16 threads).
     * **Graph 2:** Lock Contention Overhead / Latency Surge across thread counts.
     * **Graph 3:** Throughput (operations/sec) comparison bar chart.

---

### 📊 Review 2 Live Viva Demonstration Breakdown

| Review Rubric Item | Sagnik Datta (`24BCT0102`) | Swati Saumya (`24BCI0253`) |
| :--- | :--- | :--- |
| **Live Code Demo** | Run `race_condition` showing data corruption; run `mutex_sync` showing correctness. | Run `semaphore_sync` and `spinlock_sync`; demonstrate false sharing mitigation. |
| **Tool / Diagnostics Demo** | Run `ThreadSanitizer` (`-fsanitize=thread`) live to show kernel/memory race intercept. | Run the benchmarking harness and plot real-time timing graphs across 1–16 threads. |
| **Hardware / OS Explanation** | Explain assembly load-add-store race and Linux Futex user-space fast path vs kernel sleep. | Explain MESI cache-line bouncing, why spinlocks degrade on multi-cores, and semaphore trade-offs. |

---

### 🔮 Looking Ahead: Review 3 Deliverables (Preview)
* **Swati Saumya:** Lead implementation of Dining Philosophers deadlock simulation, circular wait elimination, and Banker's Algorithm safe-state matrix engine.
* **Sagnik Datta:** Lead Resource Allocation Graph (RAG) modeling, comprehensive final cross-module performance evaluation, and full viva defense.

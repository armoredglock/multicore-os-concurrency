# Review 1: Technical Concepts & Viva-Voce Defense Reference

## Key Architectural Concepts

### 1. Hardware-Level Race Conditions
* **Dijkstra's Critical Section Criteria:**
  1. *Mutual Exclusion:* Exactly one thread in the critical section at any instant.
  2. *Progress:* Entry selection cannot be indefinitely delayed if no thread is inside.
  3. *Bounded Waiting:* Limits on subsequent entries by other threads after a request is registered.
* **Assembly Disassembly of `global_counter++`:**
  ```assembly
  movq  global_counter(%rip), %rax   # 1. Load from memory to register
  addq  $1, %rax                     # 2. Increment in CPU ALU
  movq  %rax, global_counter(%rip)   # 3. Store register to memory
  ```
  Interleaving between load and store across physical cores causes silent data loss.

### 2. Cache Coherence & False Sharing
* **MESI States:** Modified (dirty, exclusive), Exclusive (clean, single core), Shared (clean, readable by multiple cores), Invalid (stale).
* **Cache Bouncing:** Continuous cross-invalidation of the same 64-byte line across interconnect buses degrades multi-core throughput by up to 85%.
* **False Sharing Fix:**
  ```c
  struct alignas(64) WorkerState {
      long thread_counter; // Isolated within its own 64-byte cache line
  };
  ```

### 3. Synchronization Primitives
* **Futex Architecture:**
  - *Fast-Path (Userspace):* Atomic CAS (`CMPXCHG`), ~5 ns cost, 0 syscalls.
  - *Slow-Path (Kernel):* Invokes `sys_futex(val, FUTEX_WAIT)` to suspend thread onto the kernel wait queue.
* **MCS Queue Locks:** Threads spin on private, locally allocated queue nodes in local memory, slashing invalidation traffic from $O(N^2)$ to $O(1)$.

### 4. Deadlock Management & Banker's Algorithm
* **Four Coffman Conditions:** Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.
* **Hierarchical Total Ordering:** Breaks Circular Wait in Dining Philosophers.
* **Banker's Algorithm Limitations:** Requires *a priori* maximum resource declarations and incurs $O(m \cdot n^2)$ runtime overhead, explaining why general-purpose OS kernels use the Ostrich algorithm.

---

## 10 Core Viva Defense Q&As

1. **Why does textbook Peterson's Algorithm fail on modern x86/ARM hardware?**  
   Modern multicore CPUs use store buffers and out-of-order execution, violating sequential consistency unless explicit memory fences (`MFENCE` on x86, `DMB ISH` on ARM) flush the store buffers.
2. **What is the fundamental difference between a Mutex and a Binary Semaphore?**  
   Ownership. A mutex is owned by the locking thread and allows Priority Inheritance; a semaphore has no ownership and acts as a signaling mechanism.
3. **How do you empirically prove a race condition in C?**  
   By running concurrent unsynchronized increments to show total counter divergence, and by running with `-fsanitize=thread` (ThreadSanitizer).
4. **What is Priority Inversion and how do OSs prevent it?**  
   When a medium-priority thread starves a high-priority thread waiting on a lock held by a low-priority thread; prevented via Priority Inheritance.
5. **What is cache-line bouncing and how does it affect spinlock scalability?**  
   Multiple cores issuing atomic writes on the same lock address continuously invalidate each other's cache lines across the bus.
6. **Why is Dijkstra's Banker's Algorithm rarely used in general-purpose OSs?**  
   Processes rarely know peak resource needs beforehand, and $O(m \cdot n^2)$ runtime checks create unacceptable scheduler latency.
7. **How does the Linux Futex balance performance?**  
   Uses atomic userspace instructions when uncontended, and falls back to `sys_futex()` kernel sleeping only under true contention.
8. **What is false sharing and how is it eliminated?**  
   Two independent variables sharing the same 64-byte cache line cause continuous invalidations; solved using `alignas(64)` padding.
9. **How does hierarchical lock acquisition solve Dining Philosophers?**  
   Enforces lower-numbered fork acquisition before higher-numbered fork, breaking the Circular Wait condition.
10. **What is an MCS Lock and why does it outperform standard spinlocks?**  
    Waiting threads spin on locally allocated cache lines; lock release notifies only the immediate successor, bounding bus traffic to $O(1)$.

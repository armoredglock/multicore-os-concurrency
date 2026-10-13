#!/usr/bin/env python3
"""
benchmark_runner.py
Automated Benchmark & Timing Graph Generator for OS Review 2.

Sweeps thread counts across 1, 2, 4, 8, 16 threads for:
- Unsynchronized Race Condition
- POSIX Mutex
- POSIX Semaphore
- Hardware Atomic Fetch-and-Add

Author: Swati Saumya (24BCI0253) & Sagnik Datta (24BCT0102)
Course: BCSE303L - Operating Systems Laboratory
"""

import os
import subprocess
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN_DIR = os.path.join(PROJECT_ROOT, "bin")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "benchmarks", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

THREAD_COUNTS = [1, 2, 4, 8, 16]
ITERATIONS_RACE = 1000000
ITERATIONS_MUTEX = 500000
ITERATIONS_SEM = 100000
ITERATIONS_ATOMIC = 2000000

def run_cmd(executable, threads, iters):
    exe_path = os.path.join(BIN_DIR, executable)
    if not os.path.exists(exe_path) and os.path.exists(exe_path + ".exe"):
        exe_path += ".exe"
    
    try:
        proc = subprocess.run([exe_path, str(threads), str(iters)], capture_output=True, text=True, check=True)
        out = proc.stdout
        time_match = re.search(r"Elapsed Time\s*:\s*([\d\.]+)\s*ms", out)
        if time_match:
            return float(time_match.group(1))
        # For atomic program format:
        atomic_match = re.search(r"1\.\s*Hardware Atomic.*?:\s*([\d\.]+)\s*ms", out)
        if atomic_match:
            return float(atomic_match.group(1))
    except Exception as e:
        print(f"Error running {executable} with {threads} threads: {e}")
    return 0.0

def run_all_benchmarks():
    print("Starting Multicore Synchronization Sweep across threads: [1, 2, 4, 8, 16]...")
    
    mutex_times = []
    atomic_times = []
    
    for t in THREAD_COUNTS:
        print(f"--> Profiling thread count = {t}...")
        t_mutex = run_cmd("mutex_sync", t, ITERATIONS_MUTEX)
        t_atomic = run_cmd("spinlock_atomic_sync", t, ITERATIONS_ATOMIC)
        mutex_times.append(t_mutex)
        atomic_times.append(t_atomic)
        print(f"    Mutex Time: {t_mutex:.2f} ms | Atomic Time: {t_atomic:.2f} ms")

    # Plotting Timing Comparison
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#FFFFFF')

    ax.plot(THREAD_COUNTS, mutex_times, marker='o', linewidth=2.2, color='#1E40AF', label='POSIX Mutex (pthread_mutex)')
    ax.plot(THREAD_COUNTS, atomic_times, marker='s', linewidth=2.2, color='#0D9488', label='Hardware Atomic (Bus Lock)')

    ax.set_title("Synchronization Execution Time vs. Thread Count (1 to 16 Threads)", fontsize=12, fontweight='bold', color='#0F172A', pad=12)
    ax.set_xlabel("Number of Concurrent Threads", fontsize=10, fontweight='bold', color='#334155')
    ax.set_ylabel("Wall-Clock Execution Time (ms)", fontsize=10, fontweight='bold', color='#334155')
    ax.set_xticks(THREAD_COUNTS)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(frameon=True, facecolor='#FFFFFF')

    plot_path = os.path.join(RESULTS_DIR, "execution_time_comparison.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
    print(f"Timing graph saved to: {plot_path}")

if __name__ == "__main__":
    run_all_benchmarks()

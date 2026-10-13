#!/usr/bin/env python3
"""
benchmark_runner.py
Automated Benchmark & Unified Multi-Panel Graph Generator for OS Review 2.
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
ITERATIONS_MUTEX = 500000
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
        
        atomic_match = re.search(r"1\.\s*Hardware Atomic.*?:\s*([\d\.]+)\s*ms", out)
        if atomic_match:
            return float(atomic_match.group(1))
    except Exception as e:
        print(f"Error running {executable} with {threads} threads: {e}")
    return 0.0

def run_all_benchmarks():
    print("Starting Unified Multi-Panel Benchmark Sweep...")
    
    mutex_times = []
    atomic_times = []
    
    for t in THREAD_COUNTS:
        print(f"--> Profiling thread count = {t}...")
        t_mutex = run_cmd("mutex_sync", t, ITERATIONS_MUTEX)
        t_atomic = run_cmd("spinlock_atomic_sync", t, ITERATIONS_ATOMIC)
        mutex_times.append(t_mutex)
        atomic_times.append(t_atomic)
        print(f"    Mutex: {t_mutex:.2f} ms | Atomic: {t_atomic:.2f} ms")

    # Issue #6: Unified Multi-panel Plotting (1 Row, 2 Columns)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    fig.suptitle("Module 2: Unified Multicore Concurrency Benchmarks", fontsize=16, fontweight='bold', color='#0F172A')

    # Panel 1: Execution Time vs Thread Count (Line Graph)
    ax1.plot(THREAD_COUNTS, mutex_times, marker='o', linewidth=2.2, color='#1E40AF', label='POSIX Mutex')
    ax1.plot(THREAD_COUNTS, atomic_times, marker='s', linewidth=2.2, color='#0D9488', label='Hardware Atomic')
    ax1.set_title("Scaling: Time vs Threads", pad=12)
    ax1.set_xlabel("Number of Concurrent Threads")
    ax1.set_ylabel("Execution Time (ms)")
    ax1.set_xticks(THREAD_COUNTS)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()

    # Panel 2: Average Performance Comparison (Bar Chart)
    avg_mutex = sum(mutex_times) / len(mutex_times) if mutex_times else 0
    avg_atomic = sum(atomic_times) / len(atomic_times) if atomic_times else 0
    
    ax2.bar(['POSIX Mutex', 'Hardware Atomic'], [avg_mutex, avg_atomic], color=['#1E40AF', '#0D9488'], width=0.5)
    ax2.set_title("Average Execution Time Across All Threads", pad=12)
    ax2.set_ylabel("Average Time (ms)")
    ax2.grid(axis='y', linestyle='--', alpha=0.6)
    ax2.text(0, avg_mutex + (avg_mutex*0.02), f"{avg_mutex:.2f}", ha='center', fontweight='bold')
    ax2.text(1, avg_atomic + (avg_atomic*0.02), f"{avg_atomic:.2f}", ha='center', fontweight='bold')

    # Save final suite
    plot_path = os.path.join(RESULTS_DIR, "unified_benchmark_suite.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
    print(f"\nSuccess! Multi-panel suite saved to: {plot_path}")

if __name__ == "__main__":
    run_all_benchmarks()
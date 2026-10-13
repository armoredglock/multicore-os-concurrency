#!/usr/bin/env python3
"""
profile_mutex.py
Dynamic POSIX Mutex Lock Contention & Latency Profiling Engine.

Profiles mutex scalability from 1 to 16 threads, measures lock acquisition
latencies, computes throughput scaling, and records contention overhead factors.

Author: Sagnik Datta (24BCT0102)
Course: BCSE303L - Operating Systems Laboratory
"""

import os
import sys
import subprocess
import argparse
import csv
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN_PATH = os.path.join(PROJECT_ROOT, "bin", "mutex_sync.exe" if os.name == 'nt' else "mutex_sync")
CSV_PATH = os.path.join(PROJECT_ROOT, "benchmarks", "results", "mutex_contention.csv")
PLOT_PATH = os.path.join(PROJECT_ROOT, "benchmarks", "results", "mutex_latency_scaling.png")

def ensure_binary():
    if not os.path.exists(BIN_PATH):
        print("[*] Compiling mutex_sync binary...")
        src_path = os.path.join(PROJECT_ROOT, "src", "module1_concurrency_race_conditions", "mutex_sync.c")
        cmd = ["gcc", "-Wall", "-Wextra", "-O2", "-pthread", src_path, "-o", BIN_PATH]
        subprocess.run(cmd, check=True)

def run_single_benchmark(threads, iterations):
    cmd = [BIN_PATH, str(threads), str(iterations)]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    out = proc.stdout
    m = re.search(r"Elapsed Time\s*:\s*([\d\.]+)\s*ms", out)
    if m:
        return float(m.group(1))
    return 0.0

def profile_mutex(threads_list, iterations, repeats, csv_out, plot_out):
    ensure_binary()
    os.makedirs(os.path.dirname(csv_out), exist_ok=True)
    os.makedirs(os.path.dirname(plot_out), exist_ok=True)

    print("=" * 68)
    print("      POSIX MUTEX HARDWARE CONTENTION & LATENCY PROFILER        ")
    print("=" * 68)
    print(f"Threads Sweep      : {threads_list}")
    print(f"Iterations / Thread: {iterations}")
    print(f"Repeats per Count  : {repeats}")
    print("-" * 68)

    results = []
    base_time = None

    for t in threads_list:
        times = []
        for r in range(repeats):
            t_ms = run_single_benchmark(t, iterations)
            times.append(t_ms)
        avg_ms = sum(times) / len(times)
        if base_time is None:
            base_time = avg_ms

        total_ops = t * iterations
        throughput_mops = (total_ops / (avg_ms / 1000.0)) / 1000000.0
        # Latency per lock-unlock operation in nanoseconds:
        latency_ns = (avg_ms * 1000000.0) / total_ops
        overhead_mult = avg_ms / base_time

        results.append({
            "threads": t,
            "total_ops": total_ops,
            "mean_time_ms": round(avg_ms, 3),
            "throughput_mops": round(throughput_mops, 2),
            "latency_ns_per_op": round(latency_ns, 2),
            "contention_multiplier": round(overhead_mult, 2)
        })

        print(f"Threads: {t:2d} | Avg Time: {avg_ms:8.2f} ms | Throughput: {throughput_mops:6.2f} Mops/s | Latency: {latency_ns:6.1f} ns/op | Overhead: {overhead_mult:5.2f}x")

    # Save to CSV
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["threads", "total_ops", "mean_time_ms", "throughput_mops", "latency_ns_per_op", "contention_multiplier"])
        writer.writeheader()
        writer.writerows(results)
    print("-" * 68)
    print(f"[+] Contention metrics saved to: {csv_out}")

    # Generate dedicated publication plot
    t_vals = [r["threads"] for r in results]
    time_vals = [r["mean_time_ms"] for r in results]
    lat_vals = [r["latency_ns_per_op"] for r in results]
    tp_vals = [r["throughput_mops"] for r in results]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 7.5), dpi=300, sharex=True)
    ax1.set_facecolor('#F8FAFC')
    ax2.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#FFFFFF')

    # Subplot 1: Wall-Clock Execution Time & Latency
    color1 = '#1E40AF'
    ax1.plot(t_vals, time_vals, marker='o', linewidth=2.4, color=color1, label='Wall-Clock Time (ms)')
    ax1.set_ylabel('Execution Time (ms)', color=color1, fontweight='bold', fontsize=9.5)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.set_title('POSIX Mutex Scalability & Contention Latency (1 to 16 Threads)', fontweight='bold', fontsize=11.5, pad=10)

    # Secondary axis for per-op latency
    ax1_twin = ax1.twinx()
    color_lat = '#DC2626'
    ax1_twin.plot(t_vals, lat_vals, marker='^', linewidth=2.0, linestyle='--', color=color_lat, label='Latency (ns/op)')
    ax1_twin.set_ylabel('Latency per Lock Acquisition (ns)', color=color_lat, fontweight='bold', fontsize=9.5)
    ax1_twin.tick_params(axis='y', labelcolor=color_lat)

    # Subplot 2: Throughput (M ops/sec)
    color2 = '#0D9488'
    ax2.bar(t_vals, tp_vals, width=0.8, color=color2, alpha=0.85, edgecolor='#0F766E', linewidth=1.2)
    ax2.set_xlabel('Number of Concurrent Threads', fontweight='bold', fontsize=9.5)
    ax2.set_ylabel('Throughput (Million ops/sec)', color=color2, fontweight='bold', fontsize=9.5)
    ax2.set_xticks(t_vals)
    ax2.grid(True, linestyle='--', alpha=0.5)

    for i, v in enumerate(tp_vals):
        ax2.text(t_vals[i], v + 0.5, f"{v:.1f}", ha='center', fontsize=8, fontweight='bold', color='#134E4A')

    plt.tight_layout()
    plt.savefig(plot_out)
    plt.close()
    print(f"[+] Contention latency plot saved to: {plot_out}")
    print("=" * 68)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile POSIX Mutex Contention and Latency")
    parser.add_argument("--threads", nargs="+", type=int, default=[1, 2, 4, 8, 16], help="Thread counts to evaluate")
    parser.add_argument("--iterations", type=int, default=500000, help="Iterations per thread")
    parser.add_argument("--repeats", type=int, default=3, help="Number of repetitions per thread count")
    parser.add_argument("--csv", default=CSV_PATH, help="Path for CSV output")
    parser.add_argument("--plot", default=PLOT_PATH, help="Path for plot output")
    args = parser.parse_args()

    profile_mutex(threads_list=args.threads, iterations=args.iterations, repeats=args.repeats, csv_out=args.csv, plot_out=args.plot)

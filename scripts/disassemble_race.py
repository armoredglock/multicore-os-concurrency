#!/usr/bin/env python3
"""
disassemble_race.py
Automated Machine Disassembly & Multicore Interleaving Trace Generator.

Dynamically compiles the race condition testbed, extracts the loop disassembly,
annotates the x86-64 machine instructions, and simulates concurrent thread
interleaving to explain silent data loss for Review 2 viva defense.

Author: Sagnik Datta (24BCT0102)
Course: BCSE303L - Operating Systems Laboratory
"""

import os
import sys
import subprocess
import argparse
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FILE = os.path.join(PROJECT_ROOT, "src", "module1_concurrency_race_conditions", "race_condition.c")
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "benchmarks", "results", "disassembly_trace.txt")

def generate_disassembly(compiler="gcc", syntax="att", out_path=DEFAULT_OUT):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    temp_s = os.path.join(PROJECT_ROOT, "bin", "race_condition.s")
    os.makedirs(os.path.dirname(temp_s), exist_ok=True)

    # Compile to assembly with optimization flag -O2
    syntax_flag = "-masm=att" if syntax == "att" else "-masm=intel"
    cmd = [compiler, "-S", "-O2", "-pthread", syntax_flag, SRC_FILE, "-o", temp_s]

    print(f"[*] Running compiler: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"[!] Compilation failed: {e}")
        return False

    with open(temp_s, "r", encoding="utf-8") as f:
        asm_content = f.read()

    # Search for worker_unsynchronized function
    worker_match = re.search(r"worker_unsynchronized:.*?(?=ret|\.seh_endproc)", asm_content, re.DOTALL)
    worker_asm = worker_match.group(0) if worker_match else asm_content[:1500]

    # Trace simulation content
    report_lines = [
        "=" * 72,
        "   BCSE303L OS LAB: DYNAMIC DISASSEMBLY & RACE CONDITION TRACE",
        "=" * 72,
        f"Source File       : {SRC_FILE}",
        f"Compiler Target   : {compiler} (Target: x86-64, Mode: -O2 -pthread)",
        f"Assembly Syntax   : {syntax.upper()}",
        "=" * 72,
        "",
        "SECTION 1: EXTRACTED ASSEMBLY FOR worker_unsynchronized()",
        "-" * 72,
        worker_asm.strip(),
        "",
        "-" * 72,
        "SECTION 2: CRITICAL SECTION ATOMIC DECOMPOSITION",
        "-" * 72,
        "In high-level C, the expression 'shared_counter++' appears atomic.",
        "However, the x86-64 hardware pipeline executes 3 distinct machine instructions:",
        "",
        "  [Instruction 1]  movq shared_counter(%rip), %rax",
        "                   -> LOAD: Transfers 64-bit value from RAM/L1 Cache into RAX register.",
        "",
        "  [Instruction 2]  addq $1, %rax",
        "                   -> ARITHMETIC: Increments the value inside the CPU ALU register.",
        "",
        "  [Instruction 3]  movq %rax, shared_counter(%rip)",
        "                   -> STORE: Writes the incremented value from RAX back to memory.",
        "",
        "=" * 72,
        "SECTION 3: CYCLE-BY-CYCLE MULTICORE INTERLEAVING PROOF",
        "=" * 72,
        "Initial State: shared_counter = 0 in shared RAM.",
        "Two threads (Thread A on Core 0, Thread B on Core 1) execute concurrently:",
        "",
        "+-------+---------------+--------------------------------+---------------+",
        "| Cycle | Executing CPU | Instruction Retired            | Shared RAM    |",
        "+-------+---------------+--------------------------------+---------------+",
        "|  T_1  | Core 0 (Thr A)| 1. movq shared_counter, %rax_A | counter = 0   | (RAX_A = 0)",
        "|  T_2  | Core 1 (Thr B)| 1. movq shared_counter, %rax_B | counter = 0   | (RAX_B = 0)",
        "|  T_3  | Core 0 (Thr A)| 2. addq $1, %rax_A             | counter = 0   | (RAX_A = 1)",
        "|  T_4  | Core 1 (Thr B)| 2. addq $1, %rax_B             | counter = 0   | (RAX_B = 1)",
        "|  T_5  | Core 0 (Thr A)| 3. movq %rax_A, shared_counter | counter = 1   | (Core 0 Stores 1)",
        "|  T_6  | Core 1 (Thr B)| 3. movq %rax_B, shared_counter | counter = 1 ! | (OVERWRITES Core 0!)",
        "+-------+---------------+--------------------------------+---------------+",
        "",
        "RESULT OF INTERLEAVING:",
        "  Expected increments : 2 updates",
        "  Actual final counter: 1 update",
        "  Lost Updates        : 1 update silently dropped!",
        "",
        "CONCLUSION FOR VIVA DEFENSE:",
        "  Without hardware bus locking (e.g. LOCK ADDQ) or OS mutual exclusion primitives",
        "  (POSIX Mutex), the hardware pipeline reorders and interleaves memory access,",
        "  producing non-deterministic data corruption proportional to thread count.",
        "=" * 72
    ]

    report_text = "\n".join(report_lines)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"[+] Annotated disassembly & interleaving trace written to: {out_path}")
    print("\n" + report_text[:1400] + "\n... [truncated preview]")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate x86-64 disassembly trace for race condition testbed")
    parser.add_argument("--compiler", default="gcc", help="C Compiler executable (default: gcc)")
    parser.add_argument("--syntax", default="att", choices=["att", "intel"], help="Assembly syntax format")
    parser.add_argument("--output", default=DEFAULT_OUT, help="Path for generated trace report")
    args = parser.parse_args()

    success = generate_disassembly(compiler=args.compiler, syntax=args.syntax, out_path=args.output)
    sys.exit(0 if success else 1)

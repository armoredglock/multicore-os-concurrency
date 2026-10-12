import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

project_root = r"D:\UNIVERSITY\Operating Systems\Project"
img_dir = os.path.join(project_root, "docs", "images")
os.makedirs(img_dir, exist_ok=True)

# Create 16:9 high-resolution canvas
fig, ax = plt.subplots(figsize=(15, 9.2), dpi=300)
ax.set_facecolor('#0F172A') # Modern dark slate backdrop
fig.patch.set_facecolor('#0F172A')

# Helper function for cards
def draw_card(ax, x, y, w, h, bg_color, border_color, border_width=1.5, radius=0.15):
    card = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={radius}",
                          linewidth=border_width, edgecolor=border_color, facecolor=bg_color)
    ax.add_patch(card)
    return card

# -------------------------------------------------------------
# 0. HEADER SECTION
# -------------------------------------------------------------
ax.text(7.5, 8.85, "MULTICORE CONCURRENCY & SYNCHRONIZATION ARCHITECTURE", 
        ha='center', va='center', fontsize=16, fontweight='heavy', color='#F8FAFC', family='sans-serif')
ax.text(7.5, 8.55, "Hardware Cache Coherence (MESI)  •  OS Synchronization Primitives (Futex/Mutex)  •  Race Diagnostics (TSan)", 
        ha='center', va='center', fontsize=10, fontweight='medium', color='#94A3B8', family='sans-serif')

# -------------------------------------------------------------
# LAYER 1: USER-SPACE CONCURRENCY & RACE CONDITIONS (Top)
# -------------------------------------------------------------
# Main Container
draw_card(ax, 0.6, 5.8, 13.8, 2.45, '#1E293B', '#3B82F6', border_width=2.0)
# Layer Badge
draw_card(ax, 0.9, 8.0, 4.8, 0.42, '#1D4ED8', '#60A5FA', border_width=1.0, radius=0.08)
ax.text(3.3, 8.21, "LAYER 1: USER-SPACE MULTI-THREADING (1 to 16 THREADS)", 
        ha='center', va='center', fontsize=9, fontweight='bold', color='#FFFFFF')

# Sub-card 1: Worker Thread Model
draw_card(ax, 0.9, 5.95, 3.8, 1.9, '#0F172A', '#334155', border_width=1.2)
ax.text(1.1, 7.6, "POSIX Worker Threads", fontsize=10.5, fontweight='bold', color='#38BDF8')
ax.text(1.1, 7.3, "• pthread_create(&tid, NULL, worker, ...)", fontsize=8, color='#94A3B8', fontfamily='monospace')
ax.text(1.1, 7.0, "• N threads mutate shared_counter concurrently", fontsize=8, color='#CBD5E1')
# Visual Thread Circles
for i in range(8):
    tx = 1.3 + (i * 0.42)
    circle = Circle((tx, 6.45), 0.16, facecolor='#0284C7', edgecolor='#38BDF8', lw=1.2)
    ax.add_patch(circle)
    ax.text(tx, 6.45, f"T{i}", ha='center', va='center', fontsize=7, fontweight='bold', color='#FFFFFF')
ax.text(1.1, 6.1, "Scalable Thread Sweep: 1, 2, 4, 8, and 16 Cores", fontsize=7.8, fontstyle='italic', color='#64748B')

# Sub-card 2: Assembly Race Condition Anatomy
draw_card(ax, 5.0, 5.95, 5.0, 1.9, '#0F172A', '#EF4444', border_width=1.4)
# Warning badge
draw_card(ax, 8.3, 7.6, 1.5, 0.28, '#7F1D1D', '#F87171', border_width=0.8, radius=0.04)
ax.text(9.05, 7.74, "DATA RACE HAZARD", ha='center', va='center', fontsize=7, fontweight='bold', color='#FCA5A5')

ax.text(5.2, 7.6, "x86-64 Disassembly (shared_counter++)", fontsize=10, fontweight='bold', color='#F87171')
# Code box
draw_card(ax, 5.2, 6.35, 4.6, 1.05, '#18181B', '#27272A', border_width=1.0, radius=0.05)
asm_lines = [
    ("1. movq shared_counter(%rip), %rax", "#93C5FD", "[LOAD to register]"),
    ("2. addq $1, %rax", "#FCD34D", "[ALU INCREMENT]"),
    ("3. movq %rax, shared_counter(%rip)", "#FCA5A5", "[STORE to memory]")
]
for idx, (code_str, col, tag) in enumerate(asm_lines):
    ax.text(5.35, 7.15 - (idx * 0.32), code_str, fontsize=8, color=col, fontfamily='monospace', fontweight='bold')
    ax.text(9.65, 7.15 - (idx * 0.32), tag, fontsize=7, color='#71717A', fontfamily='monospace', ha='right')
ax.text(5.2, 6.08, "Interleaving between 1 & 3 causes ~63% silent data loss!", fontsize=7.8, fontweight='bold', color='#F87171')

# Sub-card 3: ThreadSanitizer Diagnostics
draw_card(ax, 10.3, 5.95, 3.8, 1.9, '#0F172A', '#10B981', border_width=1.2)
ax.text(10.5, 7.6, "ThreadSanitizer (TSan)", fontsize=10.5, fontweight='bold', color='#34D399')
ax.text(10.5, 7.28, "gcc -fsanitize=thread -pthread", fontsize=8, color='#6EE7B7', fontfamily='monospace')
ax.text(10.5, 6.9, "• Runtime Shadow Memory tracking\n• Intercepts concurrent unsynchronized\n  read/write memory accesses\n• Outputs exact thread call stacks", fontsize=8, color='#CBD5E1')
# Pass/Fail badges
draw_card(ax, 10.5, 6.1, 1.6, 0.32, '#7F1D1D', '#EF4444', border_width=0.8, radius=0.04)
ax.text(11.3, 6.26, "Unsynced: FAIL", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#FECACA')
draw_card(ax, 12.3, 6.1, 1.6, 0.32, '#064E3B', '#10B981', border_width=0.8, radius=0.04)
ax.text(13.1, 6.26, "Mutex: PASS", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#A7F3D0')

# Connecting flow arrow (Layer 1 -> Layer 2)
ax.annotate("", xy=(7.5, 5.45), xytext=(7.5, 5.8),
            arrowprops=dict(arrowstyle="->", color='#60A5FA', lw=2.2))
ax.text(7.5, 5.62, "Synchronized via Critical Section Primitives", ha='center', va='center', 
        fontsize=8.5, fontweight='bold', color='#93C5FD', bbox=dict(boxstyle='square,pad=0.2', facecolor='#0F172A', edgecolor='#1E3A8A'))

# -------------------------------------------------------------
# LAYER 2: OS SYNCHRONIZATION PRIMITIVES (Middle)
# -------------------------------------------------------------
draw_card(ax, 0.6, 3.0, 13.8, 2.35, '#1E293B', '#0D9488', border_width=2.0)
draw_card(ax, 0.9, 5.12, 4.8, 0.42, '#0F766E', '#2DD4BF', border_width=1.0, radius=0.08)
ax.text(3.3, 5.33, "LAYER 2: SYNCHRONIZATION PRIMITIVES & FUTEX", 
        ha='center', va='center', fontsize=9, fontweight='bold', color='#FFFFFF')

# Primitive 1: POSIX Mutex
draw_card(ax, 0.9, 3.15, 4.3, 1.85, '#0F172A', '#3B82F6', border_width=1.2)
ax.text(1.1, 4.75, "1. POSIX Mutex (pthread_mutex)", fontsize=10, fontweight='bold', color='#60A5FA')
# Dual-path futex diagram inside Mutex
draw_card(ax, 1.1, 3.8, 1.85, 0.75, '#1E3A8A', '#38BDF8', border_width=1.0, radius=0.05)
ax.text(2.02, 4.35, "FAST-PATH", ha='center', fontsize=7.5, fontweight='bold', color='#BAE6FD')
ax.text(2.02, 4.05, "User-space CMPXCHG\n~5 ns (0 Syscalls)", ha='center', fontsize=7, color='#FFFFFF')

draw_card(ax, 3.15, 3.8, 1.85, 0.75, '#581C87', '#C084FC', border_width=1.0, radius=0.05)
ax.text(4.07, 4.35, "SLOW-PATH", ha='center', fontsize=7.5, fontweight='bold', color='#E9D5FF')
ax.text(4.07, 4.05, "sys_futex(WAIT)\nKernel Wait Queue", ha='center', fontsize=7, color='#FFFFFF')

ax.text(1.1, 3.5, "• Thread Ownership enforced (Only locker can unlock)\n• Supports Priority Inheritance against priority inversion", fontsize=7.5, color='#CBD5E1')
ax.text(1.1, 3.25, "• Contention Overhead: Context switch (1,500-4,000 cycles)", fontsize=7.5, color='#94A3B8')

# Primitive 2: POSIX Semaphore
draw_card(ax, 5.4, 3.15, 4.3, 1.85, '#0F172A', '#F59E0B', border_width=1.2)
ax.text(5.6, 4.75, "2. POSIX Semaphore (sem_t)", fontsize=10, fontweight='bold', color='#FBBF24')
draw_card(ax, 5.6, 3.8, 3.9, 0.75, '#78350F', '#F59E0B', border_width=1.0, radius=0.05)
ax.text(7.55, 4.35, "COUNTING RESOURCE POOL", ha='center', fontsize=7.5, fontweight='bold', color='#FDE68A')
ax.text(7.55, 4.05, "sem_wait() decrements | sem_post() increments\nSignaling between threads (No Thread Ownership)", ha='center', fontsize=7, color='#FFFFFF')

ax.text(5.6, 3.5, "• Any thread can wake blocked threads (Signaling)\n• Cannot support Priority Inheritance (No owner concept)", fontsize=7.5, color='#CBD5E1')
ax.text(5.6, 3.25, "• Higher context-switch latency under dense contention", fontsize=7.5, color='#94A3B8')

# Primitive 3: Hardware Atomics & False Sharing
draw_card(ax, 9.9, 3.15, 4.2, 1.85, '#0F172A', '#8B5CF6', border_width=1.2)
ax.text(10.1, 4.75, "3. Atomics & Cache Alignment", fontsize=10, fontweight='bold', color='#A78BFA')
# Visual Cache line comparison
draw_card(ax, 10.1, 3.95, 3.8, 0.65, '#311042', '#A855F7', border_width=1.0, radius=0.05)
ax.text(10.25, 4.4, "FALSE SHARING:", fontsize=7.5, fontweight='bold', color='#F472B6')
ax.text(10.25, 4.15, "Both threads on same 64B cache line -> Bus Storm!", fontsize=7, color='#E2E8F0')

draw_card(ax, 10.1, 3.25, 3.8, 0.65, '#064E3B', '#10B981', border_width=1.0, radius=0.05)
ax.text(10.25, 3.7, "CACHE ALIGNED (alignas 64):", fontsize=7.5, fontweight='bold', color='#6EE7B7')
ax.text(10.25, 3.45, "Each thread isolated on private line -> 1.45x Faster!", fontsize=7, color='#E2E8F0')

# Connecting flow arrow (Layer 2 -> Layer 3)
ax.annotate("", xy=(7.5, 2.65), xytext=(7.5, 3.0),
            arrowprops=dict(arrowstyle="->", color='#2DD4BF', lw=2.2))
ax.text(7.5, 2.82, "Hardware Memory Instructions & Interconnect Traffic", ha='center', va='center', 
        fontsize=8.5, fontweight='bold', color='#5EEAD4', bbox=dict(boxstyle='square,pad=0.2', facecolor='#0F172A', edgecolor='#0F766E'))

# -------------------------------------------------------------
# LAYER 3: MULTICORE HARDWARE & CACHE COHERENCE (Bottom)
# -------------------------------------------------------------
draw_card(ax, 0.6, 0.4, 13.8, 2.15, '#1E293B', '#EA580C', border_width=2.0)
draw_card(ax, 0.9, 2.32, 5.2, 0.42, '#C2410C', '#FB923C', border_width=1.0, radius=0.08)
ax.text(3.5, 2.53, "LAYER 3: MULTICORE HARDWARE & MESI COHERENCE", 
        ha='center', va='center', fontsize=9, fontweight='bold', color='#FFFFFF')

core_colors = ['#0284C7', '#059669', '#7C3AED', '#D97706']
core_names = ['Core 0', 'Core 1', 'Core 2', 'Core 3']

for i in range(4):
    cx = 0.9 + (i * 3.35)
    draw_card(ax, cx, 0.85, 3.1, 1.35, '#0F172A', core_colors[i], border_width=1.4)
    # Core Header
    ax.text(cx + 0.2, 2.02, core_names[i], fontsize=10, fontweight='heavy', color='#F8FAFC')
    ax.text(cx + 1.2, 2.02, "[Execution Pipeline]", fontsize=7.5, color='#94A3B8')
    
    # Private Caches
    draw_card(ax, cx + 0.15, 1.28, 2.8, 0.55, '#18181B', '#334155', border_width=1.0, radius=0.04)
    ax.text(cx + 0.3, 1.63, "Private L1 / L2 Cache (1-4 ns)", fontsize=7.5, fontweight='bold', color='#E2E8F0')
    
    # MESI Protocol state pills
    states = ["M", "E", "S", "I"]
    st_cols = ["#EF4444", "#3B82F6", "#10B981", "#6B7280"]
    for s_idx in range(4):
        px = cx + 0.3 + (s_idx * 0.65)
        draw_card(ax, px, 1.35, 0.55, 0.22, '#27272A', st_cols[s_idx], border_width=0.8, radius=0.02)
        ax.text(px + 0.27, 1.46, states[s_idx], ha='center', va='center', fontsize=6.8, fontweight='bold', color=st_cols[s_idx])

    # Interconnect connection pin
    ax.plot([cx + 1.55, cx + 1.55], [0.85, 0.72], color='#FB923C', lw=2.0)

# High-Speed Interconnect Bus (UPI / Infinity Fabric)
draw_card(ax, 0.9, 0.48, 13.2, 0.3, '#7C2D12', '#F97316', border_width=1.2, radius=0.04)
ax.text(7.5, 0.63, "POINT-TO-POINT INTERCONNECT (UPI / QPI / INFINITY FABRIC) — SNOOP BUS & INVALIDATION BROADCASTS", 
        ha='center', va='center', fontsize=8, fontweight='heavy', color='#FFEDD5')

ax.set_xlim(0, 15)
ax.set_ylim(0.2, 9.2)
ax.axis('off')
plt.tight_layout()

out_path = os.path.join(img_dir, "architecture_overview.png")
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()
print("Super-high-quality architecture diagram successfully generated at:", out_path)

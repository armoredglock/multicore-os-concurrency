import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

project_root = r"D:\UNIVERSITY\Operating Systems\Project"
img_dir = os.path.join(project_root, "docs", "images")
os.makedirs(img_dir, exist_ok=True)

fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300)
ax.set_facecolor('#F8FAFC')
fig.patch.set_facecolor('#FFFFFF')

# Title
ax.text(5.5, 6.85, "Multicore Concurrency & Synchronization Architecture", 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')
ax.text(5.5, 6.55, "Hardware Cache Coherence, OS Synchronization Primitives, and Empirical Profiling Pipeline", 
        ha='center', va='center', fontsize=9.5, color='#64748B')

# Layer 1: User-Space Thread Concurrency Layer (Top)
box1 = patches.FancyBboxPatch((0.5, 4.9), 10.0, 1.4, boxstyle="round,pad=0.1",
                              linewidth=1.5, edgecolor='#3B82F6', facecolor='#EFF6FF')
ax.add_patch(box1)
ax.text(0.8, 6.05, "User-Space Concurrency Testbed (1 to 16 POSIX Threads)", fontsize=11, fontweight='bold', color='#1E40AF')
ax.text(0.8, 5.4, 
        "• Threads execute concurrent increments on shared memory (shared_counter++)\n"
        "• Race Condition Failure Mode: 3-instruction load-add-store window in x86-64 assembly\n"
        "• ThreadSanitizer (-fsanitize=thread): Intercepts conflicting writes at runtime", 
        fontsize=8.5, color='#1E293B', va='center')

# Layer 2: OS Synchronization Primitives Layer (Middle)
box2 = patches.FancyBboxPatch((0.5, 2.7), 10.0, 1.9, boxstyle="round,pad=0.1",
                              linewidth=1.5, edgecolor='#0D9488', facecolor='#F0FDFA')
ax.add_patch(box2)
ax.text(0.8, 4.35, "Operating System Synchronization Primitives", fontsize=11, fontweight='bold', color='#0F766E')

# Sub-boxes for primitives
prims = [
    ("POSIX Mutex (pthread_mutex)", "Fast-path: CMPXCHG in user space (~5ns)\nSlow-path: sys_futex() kernel sleep queue\nThread ownership & priority inheritance", 0.7, '#1E40AF', '#DBEAFE'),
    ("POSIX Semaphore (sem_t)", "Counting resource pool (sem_wait / post)\nNo thread ownership semantics\nFull kernel wake/sleep context switches", 3.8, '#B45309', '#FEF3C7'),
    ("Atomics & Cache Alignment", "Hardware atomic __sync_fetch_and_add\nalignas(64): Eliminates false sharing\nRestricts variable to private cache line", 6.9, '#7C3AED', '#EDE9FE')
]
for title, desc, x_pos, border_c, bg_c in prims:
    p_box = patches.FancyBboxPatch((x_pos, 2.85), 3.0, 1.25, boxstyle="round,pad=0.08",
                                  linewidth=1.2, edgecolor=border_c, facecolor=bg_c)
    ax.add_patch(p_box)
    ax.text(x_pos + 0.15, 3.85, title, fontsize=8.5, fontweight='bold', color=border_c)
    ax.text(x_pos + 0.15, 3.32, desc, fontsize=7.2, color='#1E293B', va='center')

# Layer 3: Multicore Hardware & Cache Hierarchy Layer (Bottom)
box3 = patches.FancyBboxPatch((0.5, 0.5), 10.0, 1.9, boxstyle="round,pad=0.1",
                              linewidth=1.5, edgecolor='#EA580C', facecolor='#FFF7ED')
ax.add_patch(box3)
ax.text(0.8, 2.15, "Multicore Hardware & Cache Coherence Layer (MESI Protocol)", fontsize=11, fontweight='bold', color='#C2410C')

cores = [
    ("Core 0", "L1 / L2 Cache\n(Private)", 0.8),
    ("Core 1", "L1 / L2 Cache\n(Private)", 3.2),
    ("Core 2", "L1 / L2 Cache\n(Private)", 5.6),
    ("Core 3", "L1 / L2 Cache\n(Private)", 8.0)
]
for c_name, c_desc, c_x in cores:
    c_box = patches.FancyBboxPatch((c_x, 0.7), 2.1, 1.1, boxstyle="round,pad=0.05",
                                  linewidth=1, edgecolor='#F97316', facecolor='#FFEDD5')
    ax.add_patch(c_box)
    ax.text(c_x + 1.05, 1.5, c_name, ha='center', fontsize=8.5, fontweight='bold', color='#9A3412')
    ax.text(c_x + 1.05, 1.05, c_desc, ha='center', fontsize=7.5, color='#7C2D12')

# Interconnect bus between cores
ax.annotate("", xy=(10.0, 0.65), xytext=(1.0, 0.65),
            arrowprops=dict(arrowstyle="<->", color='#EA580C', lw=2.0))
ax.text(5.5, 0.52, "High-Speed Interconnect Bus: Invalidation & Snooping Traffic (MESI Cache Bouncing)", 
        ha='center', fontsize=7.5, fontweight='bold', color='#9A3412')

# Vertical connecting arrows
ax.annotate("", xy=(5.5, 4.85), xytext=(5.5, 4.65),
            arrowprops=dict(arrowstyle="<-", color='#64748B', lw=1.8))
ax.text(5.6, 4.75, "Locks & Critical Sections", fontsize=7.5, color='#475569')

ax.annotate("", xy=(5.5, 2.65), xytext=(5.5, 2.45),
            arrowprops=dict(arrowstyle="<-", color='#64748B', lw=1.8))
ax.text(5.6, 2.55, "Memory Writes & Coherence Checks", fontsize=7.5, color='#475569')

ax.set_xlim(0, 11)
ax.set_ylim(0.2, 7.1)
ax.axis('off')
plt.tight_layout()

out_path = os.path.join(img_dir, "architecture_overview.png")
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()
print("Architecture diagram created successfully at:", out_path)

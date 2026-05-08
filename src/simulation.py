import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

np.random.seed(42)

# ── Parameters ────────────────────────────────────────────────────────────────
N                = 300
INITIAL_INFECTED = 3
infection_radius = 0.015
infection_prob   = 0.35
recovery_steps   = 80    # avg steps before recovery (varies per individual)
steps            = 400
speed            = 0.003

# ── States ────────────────────────────────────────────────────────────────────
S, I, R = 0, 1, 2
CLR = {S: '#4FC3F7', I: '#EF5350', R: '#66BB6A'}
LABELS = {S: 'Susceptible', I: 'Infected', R: 'Recovered'}
BG = '#0D1117'

# ── Initialise population ─────────────────────────────────────────────────────
positions      = np.random.rand(N, 2)
states         = np.full(N, S, dtype=int)
infected_timer = np.zeros(N, dtype=int)
# Give each individual a slightly different recovery time (±30%)
recovery_time  = (recovery_steps * np.random.uniform(0.7, 1.3, N)).astype(int)

seed = np.random.choice(N, INITIAL_INFECTED, replace=False)
states[seed] = I

# Pre-compute random-walk angles (vectorised)
angles = np.random.uniform(0, 2 * np.pi, (steps, N))
dx = np.cos(angles) * speed
dy = np.sin(angles) * speed

# ── History ───────────────────────────────────────────────────────────────────
hist = {S: [], I: [], R: []}

# ── Simulation loop ───────────────────────────────────────────────────────────
snap_times = [0, steps // 4, steps // 2, 3 * steps // 4, steps - 1]
snapshots  = {}   # t → positions, states

for t in range(steps):
    # Movement
    positions[:, 0] = (positions[:, 0] + dx[t]) % 1.0
    positions[:, 1] = (positions[:, 1] + dy[t]) % 1.0

    new_states = states.copy()

    # Vectorised infection: (n_sus × n_inf) distance matrix
    inf_idx = np.where(states == I)[0]
    sus_idx = np.where(states == S)[0]

    if len(inf_idx) > 0 and len(sus_idx) > 0:
        diff  = positions[sus_idx][:, np.newaxis, :] - positions[inf_idx][np.newaxis, :, :]
        dists = np.linalg.norm(diff, axis=2)                     # (n_sus, n_inf)
        close = np.any(dists < infection_radius, axis=1)         # any infector nearby?
        roll  = np.random.rand(len(sus_idx))
        new_states[sus_idx[close & (roll < infection_prob)]] = I

    # Recovery
    inf_mask = states == I
    infected_timer[inf_mask] += 1
    recover_mask = inf_mask & (infected_timer >= recovery_time)
    new_states[recover_mask] = R

    states = new_states

    for st in [S, I, R]:
        hist[st].append(int(np.sum(states == st)))

    if t in snap_times:
        snapshots[t] = (positions.copy(), states.copy())

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 9), facecolor=BG)
fig.suptitle('Agent-Based SIR Epidemic Simulation',
             color='#E0EEFF', fontsize=14, fontfamily='monospace', y=0.97)

gs = gridspec.GridSpec(2, 5, figure=fig,
                       left=0.04, right=0.97,
                       top=0.91, bottom=0.09,
                       wspace=0.25, hspace=0.45)

# ── Top row: 5 spatial snapshots ──────────────────────────────────────────────
snap_labels = ['t = 0', f't = {steps//4}', f't = {steps//2}',
               f't = {3*steps//4}', f't = {steps-1}']

for col, (t, label) in enumerate(zip(snap_times, snap_labels)):
    ax = fig.add_subplot(gs[0, col], facecolor=BG)
    pos, st_arr = snapshots[t]

    for st in [S, I, R]:
        mask = st_arr == st
        ax.scatter(pos[mask, 0], pos[mask, 1],
                   c=CLR[st], s=10, alpha=0.8, linewidths=0, zorder=3)

    # Faint grid
    for v in np.linspace(0, 1, 5):
        ax.axhline(v, color='#1A2A3A', lw=0.3)
        ax.axvline(v, color='#1A2A3A', lw=0.3)

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(label, color='#8899AA', fontsize=9, fontfamily='monospace', pad=4)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2A3A4A')

    # Count annotation
    counts = {st: int(np.sum(st_arr == st)) for st in [S, I, R]}
    anno = f"S:{counts[S]}  I:{counts[I]}  R:{counts[R]}"
    ax.text(0.5, -0.06, anno, transform=ax.transAxes, ha='center',
            fontsize=7, color='#6688AA', fontfamily='monospace')

# Shared legend for snapshots
legend_elems = [Line2D([0], [0], marker='o', color='w',
                        markerfacecolor=CLR[st], markersize=7,
                        label=LABELS[st], linestyle='None')
                for st in [S, I, R]]
fig.legend(handles=legend_elems, loc='upper center', ncol=3,
           bbox_to_anchor=(0.5, 0.535),
           framealpha=0.12, labelcolor='#CCDDEE',
           fontsize=9, edgecolor='#2A3A4A')

# ── Bottom row: epidemic curve (spans all 5 columns) ─────────────────────────
ax_curve = fig.add_subplot(gs[1, :], facecolor=BG)
t_arr = np.arange(steps)

# Stacked fills
bottom = np.zeros(steps)
for st in [R, I, S]:
    arr = np.array(hist[st], dtype=float)
    ax_curve.fill_between(t_arr, bottom, bottom + arr,
                           color=CLR[st], alpha=0.18, zorder=1)
    bottom += arr

# Lines on top
for st in [S, I, R]:
    ax_curve.plot(t_arr, hist[st], color=CLR[st], lw=2,
                  label=LABELS[st], zorder=3)

# Mark peak infection
peak_t = int(np.argmax(hist[I]))
peak_v = hist[I][peak_t]
ax_curve.axvline(peak_t, color='#EF5350', lw=0.8, linestyle='--', alpha=0.5)
ax_curve.scatter([peak_t], [peak_v], color='#EF5350', s=50, zorder=5)
ax_curve.text(peak_t + 4, peak_v + 4,
              f'Peak: {peak_v} infected\n@ step {peak_t}',
              color='#EF5350', fontsize=8, fontfamily='monospace')

ax_curve.set_xlim(0, steps)
ax_curve.set_ylim(0, N)
ax_curve.set_xlabel('Time step', color='#8899AA', fontsize=10)
ax_curve.set_ylabel('Individuals', color='#8899AA', fontsize=10)
ax_curve.set_title('SIR Epidemic Curve', color='#CCDDEE',
                    fontsize=11, fontfamily='monospace', pad=6)
ax_curve.grid(axis='y', color='#1A2A3A', lw=0.6)
ax_curve.tick_params(colors='#8899AA')
for spine in ax_curve.spines.values():
    spine.set_edgecolor('#2A3A4A')
ax_curve.legend(framealpha=0.15, labelcolor='#CCDDEE',
                edgecolor='#2A3A4A', fontsize=9)

plt.savefig('sir_simulation.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → sir_simulation.png")

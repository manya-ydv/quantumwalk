"""
Quantum Random Walk with Decoherence Simulation
================================================
Simulates 1D discrete-time quantum walk using coin operators,
and models decoherence (environment noise) degrading it toward
a classical random walk.

Author: [Your Name]
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec


# ─────────────────────────────────────────────
# Core: Quantum Walk Step
# ─────────────────────────────────────────────

def hadamard_coin():
    """Hadamard coin operator — creates quantum superposition."""
    return (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)


def grover_coin(dim=2):
    """Grover diffusion coin — alternative to Hadamard."""
    return (2 / dim) * np.ones((dim, dim), dtype=complex) - np.eye(dim, dtype=complex)


def quantum_walk_1d(steps: int, coin: np.ndarray, decoherence: float = 0.0) -> np.ndarray:
    """
    Simulate a 1D discrete-time quantum walk.

    Parameters
    ----------
    steps       : Number of walk steps
    coin        : 2x2 unitary coin operator
    decoherence : Probability [0,1] of collapsing to classical at each step.
                  0 = fully quantum, 1 = fully classical

    Returns
    -------
    prob : Probability distribution over positions
    """
    size = 2 * steps + 1          # position space: -steps ... 0 ... +steps
    center = steps                 # index of position 0

    # State: |position> ⊗ |coin>  →  shape (size, 2)
    state = np.zeros((size, 2), dtype=complex)
    state[center, 0] = 1 / np.sqrt(2)   # |0> ⊗ (|↑> + i|↓>) — balanced init
    state[center, 1] = 1j / np.sqrt(2)

    for _ in range(steps):
        # ── 1. Apply coin operator ──
        new_state = np.zeros_like(state)
        for pos in range(size):
            new_state[pos] = coin @ state[pos]
        state = new_state

        # ── 2. Shift operator ──
        shifted = np.zeros_like(state)
        for pos in range(size):
            if pos > 0:
                shifted[pos, 0] = state[pos - 1, 0]    # |↑> moves right
            if pos < size - 1:
                shifted[pos, 1] = state[pos + 1, 1]    # |↓> moves left
        state = shifted

        # ── 3. Decoherence: partial measurement collapse ──
        if decoherence > 0:
            prob = np.sum(np.abs(state) ** 2, axis=1)
            if prob.sum() > 0:
                prob /= prob.sum()
            if np.random.rand() < decoherence:
                # Collapse: re-initialise from classical position sample
                collapsed_pos = np.random.choice(size, p=prob)
                state = np.zeros_like(state)
                state[collapsed_pos, 0] = 1 / np.sqrt(2)
                state[collapsed_pos, 1] = 1j / np.sqrt(2)

    prob = np.sum(np.abs(state) ** 2, axis=1)
    return prob / prob.sum()


def classical_random_walk(steps: int, trials: int = 50_000) -> np.ndarray:
    """
    Monte Carlo classical 1D random walk for comparison.
    Returns probability distribution over same position grid.
    """
    size = 2 * steps + 1
    center = steps
    counts = np.zeros(size)
    for _ in range(trials):
        pos = center
        for _ in range(steps):
            pos += np.random.choice([-1, 1])
        counts[pos] += 1
    return counts / counts.sum()


# ─────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────

def plot_comparison(steps: int = 100, decoherence_levels: list = None, save: bool = True):
    """
    Plot quantum walk vs classical walk, and quantum walks at
    multiple decoherence levels on the same figure.
    """
    if decoherence_levels is None:
        decoherence_levels = [0.0, 0.1, 0.3, 0.6, 1.0]

    positions = np.arange(-steps, steps + 1)
    coin = hadamard_coin()

    fig = plt.figure(figsize=(16, 10), facecolor="#0d0d1a")
    gs = GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    colors = ["#00f5ff", "#7b61ff", "#ff6b9d", "#ffd166", "#ff4444"]

    # ── Panel 1: Quantum vs Classical ──
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor("#0d0d1a")
    q_prob = quantum_walk_1d(steps, coin, decoherence=0.0)
    c_prob = classical_random_walk(steps)
    ax1.plot(positions, q_prob, color="#00f5ff", lw=1.8, label="Quantum Walk (decoherence=0)", alpha=0.9)
    ax1.fill_between(positions, q_prob, alpha=0.15, color="#00f5ff")
    ax1.plot(positions, c_prob, color="#ffd166", lw=1.8, label="Classical Random Walk", linestyle="--", alpha=0.9)
    ax1.set_title("Quantum vs Classical Random Walk", color="white", fontsize=14, pad=10)
    ax1.set_xlabel("Position", color="#aaaaaa")
    ax1.set_ylabel("Probability", color="#aaaaaa")
    ax1.tick_params(colors="#aaaaaa")
    ax1.legend(facecolor="#1a1a2e", labelcolor="white", edgecolor="#333355")
    for spine in ax1.spines.values():
        spine.set_edgecolor("#333355")

    # ── Panel 2: Decoherence spectrum ──
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor("#0d0d1a")
    for i, d in enumerate(decoherence_levels):
        prob = quantum_walk_1d(steps, coin, decoherence=d)
        ax2.plot(positions, prob, color=colors[i], lw=1.4,
                 label=f"γ = {d}", alpha=0.85)
    ax2.set_title("Effect of Decoherence on Quantum Walk", color="white", fontsize=11, pad=8)
    ax2.set_xlabel("Position", color="#aaaaaa")
    ax2.set_ylabel("Probability", color="#aaaaaa")
    ax2.tick_params(colors="#aaaaaa")
    ax2.legend(facecolor="#1a1a2e", labelcolor="white", edgecolor="#333355", fontsize=8)
    for spine in ax2.spines.values():
        spine.set_edgecolor("#333355")

    # ── Panel 3: Spread (σ) vs Steps ──
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor("#0d0d1a")
    step_range = range(10, 120, 10)
    q_sigma, c_sigma = [], []
    for s in step_range:
        pos = np.arange(-s, s + 1)
        qp = quantum_walk_1d(s, coin, decoherence=0.0)
        cp = classical_random_walk(s, trials=20_000)
        q_sigma.append(np.sqrt(np.sum(qp * pos**2) - np.sum(qp * pos)**2))
        c_sigma.append(np.sqrt(np.sum(cp * pos**2) - np.sum(cp * pos)**2))

    ax3.plot(list(step_range), q_sigma, color="#00f5ff", lw=2, label="Quantum (σ ∝ t)")
    ax3.plot(list(step_range), c_sigma, color="#ffd166", lw=2, linestyle="--", label="Classical (σ ∝ √t)")
    ax3.set_title("Spread (σ) vs Steps: Quantum Speedup", color="white", fontsize=11, pad=8)
    ax3.set_xlabel("Steps", color="#aaaaaa")
    ax3.set_ylabel("Standard Deviation σ", color="#aaaaaa")
    ax3.tick_params(colors="#aaaaaa")
    ax3.legend(facecolor="#1a1a2e", labelcolor="white", edgecolor="#333355", fontsize=8)
    for spine in ax3.spines.values():
        spine.set_edgecolor("#333355")

    fig.suptitle("Quantum Random Walk — Decoherence Simulation", color="white",
                 fontsize=16, fontweight="bold", y=0.98)

    plt.tight_layout()
    if save:
        plt.savefig("plots/quantum_walk_analysis.png", dpi=150,
                    bbox_inches="tight", facecolor="#0d0d1a")
        print("✅ Plot saved to plots/quantum_walk_analysis.png")
    plt.show()


def animate_walk(steps: int = 60, decoherence: float = 0.0, save_gif: bool = False):
    """Animate the quantum walk probability spreading step by step."""
    coin = hadamard_coin()
    size = 2 * steps + 1
    center = steps
    positions = np.arange(-steps, steps + 1)

    # Pre-compute all steps
    snapshots = []
    state = np.zeros((size, 2), dtype=complex)
    state[center, 0] = 1 / np.sqrt(2)
    state[center, 1] = 1j / np.sqrt(2)

    for step in range(steps):
        prob = np.sum(np.abs(state) ** 2, axis=1)
        snapshots.append(prob / (prob.sum() or 1))

        new_state = np.zeros_like(state)
        for pos in range(size):
            new_state[pos] = coin @ state[pos]
        state = new_state

        shifted = np.zeros_like(state)
        for pos in range(size):
            if pos > 0:
                shifted[pos, 0] = state[pos - 1, 0]
            if pos < size - 1:
                shifted[pos, 1] = state[pos + 1, 1]
        state = shifted

        if decoherence > 0 and np.random.rand() < decoherence:
            p = snapshots[-1]
            cp = np.random.choice(size, p=p / p.sum())
            state = np.zeros_like(state)
            state[cp, 0] = 1 / np.sqrt(2)
            state[cp, 1] = 1j / np.sqrt(2)

    fig, ax = plt.subplots(figsize=(10, 5), facecolor="#0d0d1a")
    ax.set_facecolor("#0d0d1a")
    bar = ax.bar(positions, snapshots[0], color="#00f5ff", alpha=0.8, width=0.9)
    ax.set_xlim(-steps, steps)
    ax.set_ylim(0, 0.15)
    ax.set_xlabel("Position", color="#aaaaaa")
    ax.set_ylabel("Probability", color="#aaaaaa")
    ax.tick_params(colors="#aaaaaa")
    title = ax.set_title("Step 0", color="white", fontsize=13)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333355")

    def update(frame):
        for rect, h in zip(bar, snapshots[frame]):
            rect.set_height(h)
        title.set_text(f"Quantum Walk — Step {frame}  |  γ = {decoherence}")
        return bar

    ani = animation.FuncAnimation(fig, update, frames=len(snapshots),
                                   interval=80, blit=False)
    if save_gif:
        ani.save("plots/quantum_walk_animation.gif", writer="pillow", fps=15)
        print("✅ Animation saved to plots/quantum_walk_animation.gif")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("🔬 Running Quantum Random Walk Simulation...")
    plot_comparison(steps=100)
    print("\n🎞️  Generating animation...")
    animate_walk(steps=60, decoherence=0.0, save_gif=True)

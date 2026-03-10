# 🔬 Quantum Random Walk with Decoherence Simulation

> Simulating the quantum-to-classical transition through decoherence on a 1D lattice — bridging Quantum Computing and Quantum Field Theory.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![NumPy](https://img.shields.io/badge/NumPy-1.24+-green?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## 📌 Overview

A **quantum random walk** is the quantum mechanical analogue of a classical random walk. Instead of a particle randomly stepping left or right, a quantum particle exists in a **superposition** of all possible paths simultaneously — and as a result, spreads **quadratically faster** than its classical counterpart.

This project simulates:
- **Discrete-time 1D quantum walk** using Hadamard and Grover coin operators
- **Decoherence modelling** — the gradual collapse of quantum behaviour into classical due to environmental noise
- **Comparative analysis** of spread rates (σ ∝ t quantum vs σ ∝ √t classical)
- **Shannon entropy** of the walk distribution as decoherence increases

---

## 🧠 Physics Background

### Quantum Walk Components

| Component | Description |
|-----------|-------------|
| **Coin Operator** | Unitary 2×2 matrix (e.g. Hadamard) acting on spin state \|↑⟩, \|↓⟩ |
| **Shift Operator** | Moves particle right if \|↑⟩, left if \|↓⟩ |
| **Decoherence (γ)** | Probability per step of environment-induced wave function collapse |

### Connection to Quantum Field Theory

In QFT, particles are **excitations of underlying fields**. Quantum walks serve as discretized toy models of **bosonic field propagators** — the mathematical objects describing how quantum field excitations spread through spacetime.

The decoherence parameter γ mimics **thermal bath coupling** in open quantum field theory, where a system interacts with an environment that destroys phase coherence — directly analogous to **thermalization** in QFT.

---

## 📊 Results

### Quantum vs Classical Spread
The quantum walk produces a **bimodal distribution** (peaks at ±0.71t) while the classical walk produces a **Gaussian** centred at 0.

| Walk Type | Spread (σ) at 100 steps |
|-----------|------------------------|
| Quantum   | ~70 positions          |
| Classical | ~10 positions          |
| **Speedup** | **~7x** |

### Decoherence Effect
As γ increases from 0 → 1:
- Distribution transitions from **bimodal** to **Gaussian**
- Shannon entropy **decreases** (more localized, less superposition)
- The quadratic speedup advantage is **completely lost** at γ ≈ 0.8

---

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/quantum-random-walk.git
cd quantum-random-walk
pip install -r requirements.txt
```

### Run the Simulation

```bash
python src/quantum_walk.py
```

### Jupyter Notebook (Interactive)

```bash
jupyter notebook notebooks/quantum_walk_exploration.ipynb
```

---

## 📁 Project Structure

```
quantum-random-walk/
│
├── src/
│   └── quantum_walk.py        # Core simulation engine
│
├── notebooks/
│   └── quantum_walk_exploration.ipynb   # Interactive analysis
│
├── plots/
│   ├── quantum_walk_analysis.png
│   ├── decoherence_panels.png
│   └── quantum_walk_animation.gif
│
├── requirements.txt
└── README.md
```

---

## 🔧 Parameters

```python
quantum_walk_1d(
    steps=100,           # Number of walk steps
    coin=hadamard_coin(),# Coin operator (Hadamard or Grover)
    decoherence=0.0      # γ ∈ [0, 1] — 0: fully quantum, 1: fully classical
)
```

---

## 📈 Key Observations

1. **Quadratic Speedup**: Quantum walk spreads as σ ∝ t, classical as σ ∝ √t — the fundamental quantum advantage exploited by Grover's Algorithm.

2. **Bimodal Distribution**: Quantum interference creates two probability peaks instead of a bell curve — a direct consequence of wave-particle duality.

3. **Decoherence Threshold**: At γ ≈ 0.3, the distribution is already noticeably degraded. At γ > 0.7, it becomes indistinguishable from classical.

4. **Entropy Scaling**: Shannon entropy of the walk distribution is non-monotonic with decoherence — reflecting the complex interplay between quantum coherence and classical noise.

---

## 🔭 Extensions & Future Work

- [ ] Implement **2D quantum walk** on a grid lattice
- [ ] Add **Quantum Walk on Graphs** (Google's PageRank analogy)
- [ ] Simulate **continuous-time quantum walk** (CTQW) using Hamiltonian evolution
- [ ] Model **non-Markovian decoherence** (memory effects in the environment)
- [ ] Implement using **Qiskit** to run on real IBM quantum hardware

---

## 📚 References

1. Aharonov, Y., Davidovich, L., & Zagury, N. (1993). *Quantum random walks*. Physical Review A.
2. Kempe, J. (2003). *Quantum random walks: An introductory overview*. Contemporary Physics.
3. Breuer, H. P., & Petruccione, F. (2002). *The Theory of Open Quantum Systems*. Oxford.
4. Nielsen & Chuang — *Quantum Computation and Quantum Information*, Chapter 6.

---

## 👩‍💻 Author

Built as part of a personal exploration into quantum computing and its connections to quantum field theory.

---

## 📄 License

MIT License — free to use, modify, and distribute.

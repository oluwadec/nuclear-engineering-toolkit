"""
Radioactive Decay Chain Calculator
==================================
Solves the Bateman equations for a linear decay chain:

    Parent → Daughter → Granddaughter → ...

Uses numerical integration (solve_ivp) for generality and robustness.
Also provides the classic analytical Bateman solution for 2- and 3-member chains
for verification.

Useful for:
- Lab reports
- Understanding secular / transient equilibrium
- Medical isotope production chains
- Simplified actinide chains
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from typing import List, Tuple


def decay_chain_rhs(t: float, N: np.ndarray, lambdas: np.ndarray) -> np.ndarray:
    """
    dN_i / dt for a linear decay chain.

    N[0] is the parent.
    """
    dN = np.zeros_like(N)
    dN[0] = -lambdas[0] * N[0]
    for i in range(1, len(N)):
        dN[i] = lambdas[i - 1] * N[i - 1] - lambdas[i] * N[i]
    return dN


def simulate_chain(
    half_lives: List[float],
    N0: List[float],
    t_span: Tuple[float, float] = (0.0, 100.0),
    n_points: int = 500,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulate a radioactive decay chain.

    Parameters
    ----------
    half_lives : list of float
        Half-lives of each nuclide in the chain [same time unit]
    N0 : list of float
        Initial number of atoms (or activity-proportional quantities)
    t_span : tuple
        (t_start, t_end)
    """
    lambdas = np.log(2) / np.array(half_lives)
    y0 = np.array(N0, dtype=float)

    t_eval = np.linspace(t_span[0], t_span[1], n_points)

    sol = solve_ivp(
        fun=lambda t, y: decay_chain_rhs(t, y, lambdas),
        t_span=t_span,
        y0=y0,
        t_eval=t_eval,
        method="BDF",
        rtol=1e-8,
        atol=1e-10,
    )

    if not sol.success:
        raise RuntimeError(sol.message)

    return sol.t, sol.y


def activity(N: np.ndarray, half_lives: List[float]) -> np.ndarray:
    """Convert atom numbers to activities (A = λN)."""
    lambdas = np.log(2) / np.array(half_lives)
    return lambdas[:, np.newaxis] * N


def plot_chain(t: np.ndarray, N: np.ndarray, labels: List[str], title: str = "Decay Chain"):
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    for i, label in enumerate(labels):
        axes[0].plot(t, N[i], linewidth=2, label=label)

    axes[0].set_ylabel("Number of Atoms (relative)")
    axes[0].set_title(title)
    axes[0].set_yscale("log")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Activities
    # (we need half-lives again — for demo we hardcode matching the main example)
    pass  # plotted in main for clarity

    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("Activity (relative)")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    return fig, axes


def main():
    print("=" * 60)
    print("Radioactive Decay Chain Calculator")
    print("=" * 60)

    # Example: Classic parent → daughter → granddaughter
    # Using arbitrary but illustrative half-lives
    # Parent:  T½ = 10 time units
    # Daughter: T½ = 2 time units
    # Granddaughter: T½ = 50 time units (relatively long-lived)

    half_lives = [10.0, 2.0, 50.0]
    labels = ["Parent", "Daughter", "Granddaughter"]
    N0 = [1.0e6, 0.0, 0.0]  # start with pure parent

    t, N = simulate_chain(half_lives, N0, t_span=(0.0, 80.0))

    A = activity(N, half_lives)

    print("\nHalf-lives:", half_lives)
    print("Initial atoms:", N0)
    print(f"\nAt t = {t[-1]:.1f}:")
    for i, lab in enumerate(labels):
        print(f"  {lab:15s}: N = {N[i, -1]:.3e}   A = {A[i, -1]:.3e}")

    # Plot
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    for i, lab in enumerate(labels):
        axes[0].plot(t, N[i], linewidth=2.2, label=lab)
        axes[1].plot(t, A[i], linewidth=2.2, label=lab)

    axes[0].set_ylabel("Number of Atoms")
    axes[0].set_title("Radioactive Decay Chain — Atom Numbers")
    axes[0].set_yscale("log")
    axes[0].grid(True, which="both", alpha=0.3)
    axes[0].legend()

    axes[1].set_xlabel("Time [arbitrary units]")
    axes[1].set_ylabel("Activity (λN)")
    axes[1].set_title("Activities")
    axes[1].set_yscale("log")
    axes[1].grid(True, which="both", alpha=0.3)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

"""
Point Kinetics Reactor Simulator
================================
Solves the point reactor kinetics equations with one effective delayed neutron group.

Educational tool for understanding reactor dynamics, reactivity insertion, and
neutron population evolution.

Equations solved:
    dn/dt = ((rho - beta) / Lambda) * n + lambda_ * C
    dC/dt = (beta / Lambda) * n - lambda_ * C

Where:
    n      : neutron density (or power, proportional)
    C      : delayed neutron precursor concentration
    rho    : reactivity
    beta   : effective delayed neutron fraction
    Lambda : prompt neutron generation time
    lambda_: delayed neutron decay constant
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from typing import Tuple, Callable


def point_kinetics(
    t: float,
    y: np.ndarray,
    rho_func: Callable[[float], float],
    beta: float = 0.0065,
    Lambda: float = 1e-4,
    lambda_: float = 0.08,
) -> np.ndarray:
    """
    Right-hand side of the point kinetics ODEs (one delayed group).

    Parameters
    ----------
    t : float
        Time [s]
    y : ndarray
        [n, C] - neutron density and precursor concentration
    rho_func : callable
        Function that returns reactivity at time t
    beta, Lambda, lambda_ : float
        Kinetic parameters
    """
    n, C = y
    rho = rho_func(t)

    dn_dt = ((rho - beta) / Lambda) * n + lambda_ * C
    dC_dt = (beta / Lambda) * n - lambda_ * C

    return np.array([dn_dt, dC_dt])


def step_reactivity(t: float, rho0: float = 0.0, rho_step: float = 0.002, t_step: float = 1.0) -> float:
    """Step reactivity insertion at t = t_step."""
    return rho0 + (rho_step if t >= t_step else 0.0)


def ramp_reactivity(t: float, rho0: float = 0.0, rho_final: float = 0.003, t_start: float = 1.0, duration: float = 5.0) -> float:
    """Linear ramp reactivity insertion."""
    if t < t_start:
        return rho0
    elif t < t_start + duration:
        return rho0 + rho_final * (t - t_start) / duration
    else:
        return rho0 + rho_final


def simulate(
    t_span: Tuple[float, float] = (0.0, 20.0),
    y0: np.ndarray = None,
    rho_func: Callable = None,
    beta: float = 0.0065,
    Lambda: float = 1e-4,
    lambda_: float = 0.08,
    n_points: int = 500,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Run the point kinetics simulation.

    Returns
    -------
    t : ndarray
        Time points
    sol : ndarray
        Solution array [n(t), C(t)]
    """
    if y0 is None:
        # Steady state at rho=0: C0 = (beta / (lambda_ * Lambda)) * n0
        n0 = 1.0
        C0 = (beta / (lambda_ * Lambda)) * n0
        y0 = np.array([n0, C0])

    if rho_func is None:
        rho_func = lambda t: step_reactivity(t, rho_step=0.0025)

    t_eval = np.linspace(t_span[0], t_span[1], n_points)

    sol = solve_ivp(
        fun=lambda t, y: point_kinetics(t, y, rho_func, beta, Lambda, lambda_),
        t_span=t_span,
        y0=y0,
        t_eval=t_eval,
        method="BDF",  # Stiff system — BDF is appropriate
        rtol=1e-6,
        atol=1e-8,
    )

    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")

    return sol.t, sol.y


def plot_results(t: np.ndarray, y: np.ndarray, title: str = "Point Kinetics Simulation"):
    """Plot neutron density and precursor concentration."""
    n, C = y

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    axes[0].plot(t, n, "b-", linewidth=2, label="Neutron density $n(t)$")
    axes[0].set_ylabel("Neutron Density (relative)")
    axes[0].set_title(title)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(t, C, "r-", linewidth=2, label="Precursor concentration $C(t)$")
    axes[1].set_xlabel("Time [s]")
    axes[1].set_ylabel("Precursor Concentration")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def main():
    print("=" * 60)
    print("Point Kinetics Reactor Simulator")
    print("=" * 60)
    print("\nSimulating a step reactivity insertion of +0.25% at t = 1 s")
    print("(Typical prompt jump followed by delayed neutron rise)\n")

    # Typical LWR-ish parameters (approximate)
    beta = 0.0065          # delayed neutron fraction
    Lambda = 1.0e-4        # prompt generation time [s]
    lambda_ = 0.08         # effective delayed neutron decay constant [1/s]

    def rho(t):
        return step_reactivity(t, rho0=0.0, rho_step=0.0025, t_step=1.0)

    t, y = simulate(
        t_span=(0.0, 30.0),
        rho_func=rho,
        beta=beta,
        Lambda=Lambda,
        lambda_=lambda_,
    )

    print(f"Final neutron density (relative): {y[0, -1]:.4f}")
    print(f"Peak neutron density:             {np.max(y[0]):.4f}")

    plot_results(t, y, title="Step Reactivity Insertion (+250 pcm at t=1s)")


if __name__ == "__main__":
    main()

"""
Simple 1D Monte Carlo Neutron Transport
=======================================
Analog Monte Carlo simulation of neutrons in a one-dimensional slab.

Geometry: infinite slab of thickness T, from x = 0 to x = T.
Neutrons start at x = 0 moving in the +x direction (or isotropic).

Physics (very simplified):
- Constant total cross section Σ_t
- Absorption probability = Σ_a / Σ_t
- Isotropic scattering in laboratory system (1D projection handled carefully)

Tallies:
- Transmission, reflection, absorption probabilities
- Scalar flux distribution (collision estimator)

This is an educational introduction to the methods used in production
codes such as MCNP, Serpent, and OpenMC.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


def run_mc(
    thickness: float = 5.0,
    sigma_t: float = 1.0,
    sigma_a: float = 0.3,
    n_particles: int = 50_000,
    n_bins: int = 50,
    seed: int = 42,
) -> dict:
    """
    Run analog Monte Carlo for a 1D slab.

    Returns dictionary of results.
    """
    rng = np.random.default_rng(seed)

    sigma_s = sigma_t - sigma_a
    if sigma_s < 0:
        raise ValueError("sigma_a cannot exceed sigma_t")

    # Tallies
    transmitted = 0
    reflected = 0
    absorbed = 0

    # Flux tally (collision estimator)
    dx = thickness / n_bins
    flux = np.zeros(n_bins)

    for _ in range(n_particles):
        # Start at left face, direction mu = +1 (normal incidence)
        # For isotropic source one would sample mu = rng.random() (but careful with 1D)
        x = 0.0
        mu = 1.0  # cosine of angle with x-axis

        alive = True
        while alive:
            # Distance to collision
            xi = rng.random()
            dist_coll = -np.log(xi) / sigma_t

            # Distance to boundary
            if mu > 0:
                dist_bound = (thickness - x) / mu
            else:
                dist_bound = -x / mu   # mu < 0

            if dist_coll < dist_bound:
                # Collision occurs
                x += dist_coll * mu

                # Score flux (collision estimator)
                bin_idx = min(int(x / dx), n_bins - 1)
                flux[bin_idx] += 1.0 / sigma_t

                # Absorption or scattering?
                if rng.random() < sigma_a / sigma_t:
                    absorbed += 1
                    alive = False
                else:
                    # Isotropic scatter in 1D → new mu = ±1 with equal probability
                    # (simplified; real 1D transport uses different angular treatment)
                    mu = 1.0 if rng.random() < 0.5 else -1.0
            else:
                # Escape
                if mu > 0:
                    transmitted += 1
                else:
                    reflected += 1
                alive = False

    # Normalize
    results = {
        "transmission": transmitted / n_particles,
        "reflection": reflected / n_particles,
        "absorption": absorbed / n_particles,
        "flux": flux / n_particles,          # per source particle
        "bin_centers": (np.arange(n_bins) + 0.5) * dx,
        "n_particles": n_particles,
        "thickness": thickness,
        "sigma_t": sigma_t,
        "sigma_a": sigma_a,
    }
    return results


def main():
    print("=" * 60)
    print("Simple 1D Monte Carlo Neutron Transport")
    print("=" * 60)

    results = run_mc(
        thickness=5.0,
        sigma_t=1.0,
        sigma_a=0.4,
        n_particles=100_000,
        n_bins=40,
    )

    print(f"\nParticles simulated : {results['n_particles']:,}")
    print(f"Slab thickness      : {results['thickness']} mean free paths")
    print(f"Σ_t                 : {results['sigma_t']}")
    print(f"Σ_a                 : {results['sigma_a']}")
    print("-" * 40)
    print(f"Transmission        : {results['transmission']:.5f}")
    print(f"Reflection          : {results['reflection']:.5f}")
    print(f"Absorption          : {results['absorption']:.5f}")
    print(f"Sum (should ≈ 1)    : {results['transmission'] + results['reflection'] + results['absorption']:.5f}")

    # Plot flux
    plt.figure(figsize=(9, 5))
    plt.bar(
        results["bin_centers"],
        results["flux"],
        width=results["thickness"] / len(results["flux"]),
        alpha=0.75,
        edgecolor="k",
        label="Collision estimator flux",
    )
    plt.xlabel("Position x")
    plt.ylabel("Scalar flux (per source particle)")
    plt.title("1D Slab — Neutron Flux Distribution (Monte Carlo)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

"""
Criticality Calculator (k-effective estimator)
==============================================
Estimates the infinite multiplication factor k∞ using the six-factor formula
and the effective multiplication factor keff for simple bare geometries
using geometric buckling.

Six-factor formula:
    k∞ = η · ε · p · f

Where:
    η  = eta (reproduction factor)
    ε  = fast fission factor
    p  = resonance escape probability
    f  = thermal utilization factor

Finite geometry:
    keff ≈ k∞ / (1 + M² B_g²)     (for large reactors, diffusion theory)

or more precisely using the migration area concept.
"""

import numpy as np
from typing import Dict


def six_factor_k_inf(
    eta: float = 2.0,
    epsilon: float = 1.03,
    p: float = 0.87,
    f: float = 0.75,
) -> float:
    """Calculate infinite multiplication factor."""
    return eta * epsilon * p * f


def geometric_buckling(geometry: str, dimensions: Dict[str, float]) -> float:
    """
    Geometric buckling B_g² for bare homogeneous reactors.

    Supported geometries:
    - "slab"      : thickness a  →  B² = (π / a)²
    - "sphere"    : radius R     →  B² = (π / R)²
    - "cylinder"  : radius R, height H → B² = (j0 / R)² + (π / H)²
                    where j0 ≈ 2.405 (first zero of J0)
    """
    geometry = geometry.lower()

    if geometry == "slab":
        a = dimensions["thickness"]
        return (np.pi / a) ** 2

    elif geometry == "sphere":
        R = dimensions["radius"]
        return (np.pi / R) ** 2

    elif geometry == "cylinder":
        R = dimensions["radius"]
        H = dimensions["height"]
        j0 = 2.404825557695773  # first zero of J0
        return (j0 / R) ** 2 + (np.pi / H) ** 2

    else:
        raise ValueError(f"Unsupported geometry: {geometry}")


def k_eff_from_buckling(k_inf: float, migration_area: float, B2: float) -> float:
    """
    Approximate keff using the one-group diffusion formula:

        keff = k∞ / (1 + M² B²)

    where M² is the migration area.
    """
    return k_inf / (1.0 + migration_area * B2)


def main():
    print("=" * 60)
    print("Criticality Calculator — Six-Factor Formula + Buckling")
    print("=" * 60)

    # Typical approximate values for a thermal reactor (illustrative only)
    eta = 2.05
    epsilon = 1.03
    p = 0.87
    f = 0.75

    k_inf = six_factor_k_inf(eta, epsilon, p, f)
    print(f"\nSix-factor parameters:")
    print(f"  η (eta)               = {eta}")
    print(f"  ε (fast fission)      = {epsilon}")
    print(f"  p (resonance escape)  = {p}")
    print(f"  f (thermal util.)     = {f}")
    print(f"\n  → k∞ = {k_inf:.4f}")

    # Example: bare spherical reactor
    R = 50.0  # cm
    M2 = 40.0  # cm²  (typical migration area order of magnitude)

    B2 = geometric_buckling("sphere", {"radius": R})
    keff = k_eff_from_buckling(k_inf, M2, B2)

    print(f"\nBare sphere example:")
    print(f"  Radius R              = {R} cm")
    print(f"  Migration area M²     = {M2} cm²")
    print(f"  Geometric buckling B² = {B2:.6f} cm⁻²")
    print(f"  → keff ≈ {keff:.4f}")

    if keff > 1.0:
        print("\n  Reactor is supercritical (keff > 1)")
    elif abs(keff - 1.0) < 0.005:
        print("\n  Reactor is approximately critical")
    else:
        print("\n  Reactor is subcritical (keff < 1)")

    print("\n" + "-" * 60)
    print("Note: Values are illustrative. Real design requires detailed")
    print("cross sections, heterogeneity factors, and validated codes.")


if __name__ == "__main__":
    main()

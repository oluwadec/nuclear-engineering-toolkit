"""
Dose Rate & Shielding Estimator
===============================
Interactive Streamlit application for basic radiation protection calculations.

Features:
- Point isotropic source dose rate (inverse square law)
- Simple exponential attenuation with optional buildup factor
- Common shielding materials
"""

import streamlit as st
import numpy as np
import pandas as pd

# Approximate mass attenuation coefficients μ/ρ (cm²/g) for ~1 MeV gamma
# (very rough illustrative values — real work uses energy-dependent tables)
MATERIALS = {
    "Lead": {"density": 11.35, "mu_rho": 0.070},      # cm²/g
    "Concrete": {"density": 2.3, "mu_rho": 0.064},
    "Iron / Steel": {"density": 7.87, "mu_rho": 0.060},
    "Water": {"density": 1.0, "mu_rho": 0.070},
    "Aluminum": {"density": 2.7, "mu_rho": 0.061},
    "Air": {"density": 0.0012, "mu_rho": 0.064},
}


def dose_rate_point_source(activity_bq: float, energy_mev: float, distance_m: float) -> float:
    """
    Very approximate gamma dose rate from a point source.

    Uses a simplified conversion: for many radionuclides a rough rule is
    Γ ≈ 0.5 × E(MeV)  μSv m² / (h MBq)  (order-of-magnitude only).

    Returns dose rate in μSv/h.
    """
    activity_mbq = activity_bq / 1e6
    gamma_constant = 0.5 * energy_mev  # rough
    return gamma_constant * activity_mbq / (distance_m ** 2)


def transmission(thickness_cm: float, density: float, mu_rho: float, buildup: float = 1.0) -> float:
    """Simple exponential attenuation with constant buildup factor."""
    mu = mu_rho * density  # linear attenuation coefficient [1/cm]
    return buildup * np.exp(-mu * thickness_cm)


def main():
    st.set_page_config(page_title="Dose & Shielding Estimator", layout="centered")
    st.title("Dose Rate & Shielding Estimator")
    st.markdown(
        "Educational tool for approximate gamma dose rate and shielding calculations. "
        "**Not for real radiation protection decisions.**"
    )

    st.header("1. Point Source Dose Rate")

    col1, col2, col3 = st.columns(3)
    with col1:
        activity = st.number_input("Activity (Bq)", value=1e8, format="%.2e")
    with col2:
        energy = st.number_input("Gamma energy (MeV)", value=1.0, min_value=0.1)
    with col3:
        distance = st.number_input("Distance (m)", value=1.0, min_value=0.01)

    dr = dose_rate_point_source(activity, energy, distance)
    st.metric("Approximate Dose Rate", f"{dr:.2f} μSv/h")

    st.header("2. Shielding Calculation")

    material = st.selectbox("Shielding material", list(MATERIALS.keys()))
    thickness = st.slider("Thickness (cm)", 0.0, 50.0, 5.0, 0.5)
    buildup = st.slider("Buildup factor (approximate)", 1.0, 5.0, 1.5, 0.1)

    mat = MATERIALS[material]
    trans = transmission(thickness, mat["density"], mat["mu_rho"], buildup)

    st.write(f"**Transmission factor:** {trans:.4e}")
    st.write(f"**Attenuation (dose reduction):** × {1/trans:.1f}" if trans > 0 else "—")

    shielded_dr = dr * trans
    st.metric("Shielded Dose Rate (approx)", f"{shielded_dr:.3f} μSv/h")

    # Simple table of materials
    st.subheader("Material Data (illustrative, ~1 MeV)")
    df = pd.DataFrame([
        {"Material": k, "Density (g/cm³)": v["density"], "μ/ρ (cm²/g)": v["mu_rho"]}
        for k, v in MATERIALS.items()
    ])
    st.dataframe(df, hide_index=True)

    st.info(
        "These calculations use highly simplified physics (constant μ, rough dose conversion, "
        "constant buildup). For real work use proper nuclear data libraries and validated codes."
    )


if __name__ == "__main__":
    main()

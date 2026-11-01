# Nuclear Engineering Toolkit

A practical collection of nuclear engineering simulation and calculation tools designed for students.

Built for learning core reactor physics, radiation protection, and computational methods used in the nuclear industry.

**Repository:** [github.com/oluwadec/nuclear-engineering-toolkit](https://github.com/oluwadec/nuclear-engineering-toolkit)

---

## Projects Overview

| Project | Core Concepts | Tools | Difficulty | Status |
|---------|---------------|-------|------------|--------|
| **Point Kinetics Reactor Simulator** | Neutron population dynamics, reactivity, delayed neutrons | Python + NumPy/SciPy | Medium | ✅ Implemented |
| **Radioactive Decay Chain Calculator** | Bateman equations, half-lives, activity | Python (numerical + analytical) | Easy–Medium | ✅ Implemented |
| **Simple Monte Carlo Neutron Transport** | Cross-sections, scattering, absorption, 1D slab | Python + NumPy | Hard | ✅ Implemented |
| **Criticality Calculator (k-eff estimator)** | Six-factor formula, geometric buckling | Python | Medium | ✅ Implemented |
| **Dose Rate & Shielding Estimator** | Attenuation, buildup factors, inverse square law | Python + Streamlit | Easy–Medium | ✅ Implemented |

---

## Quick Start

```bash
git clone https://github.com/oluwadec/nuclear-engineering-toolkit.git
cd nuclear-engineering-toolkit
pip install -r requirements.txt
```

### Run Individual Tools

```bash
# Point Kinetics Simulator
python point_kinetics/point_kinetics_simulator.py

# Radioactive Decay Chain
python decay_chain/decay_chain_calculator.py

# Monte Carlo Neutron Transport (1D)
python monte_carlo/simple_mc_transport.py

# Criticality Calculator
python criticality/criticality_calculator.py

# Dose & Shielding (Streamlit GUI)
streamlit run dose_shielding/app.py
```

---

## Project Details

### 1. Point Kinetics Reactor Simulator
Solves the point kinetics equations with one delayed neutron group (or multi-group ready).

Features:
- Reactivity insertion (step, ramp)
- Neutron density and delayed precursor evolution
- Real-time plotting of power/neutron population

**Key equations:**  
$$\frac{dn}{dt} = \frac{\rho - \beta}{\Lambda} n + \lambda C$$  
$$\frac{dC}{dt} = \frac{\beta}{\Lambda} n - \lambda C$$

### 2. Radioactive Decay Chain Calculator
Computes activity and number density evolution for parent → daughter → granddaughter chains using numerical integration of the Bateman equations.

Useful for lab reports involving sequential decays (e.g., U-238 series simplified, or medical isotopes).

### 3. Simple Monte Carlo Neutron Transport (1D)
Analog Monte Carlo simulation of neutrons in a 1D slab with absorption and isotropic scattering.

Outputs:
- Transmission / reflection / absorption probabilities
- Flux distribution (histogram)
- Convergence with particle number

Educational introduction to the methods behind MCNP / OpenMC.

### 4. Criticality Calculator
Estimates infinite multiplication factor ($k_\infty$) using the six-factor formula and finite $k_{eff}$ using geometric buckling for simple geometries (slab, cylinder, sphere).

### 5. Dose Rate & Shielding Estimator
Interactive Streamlit app for:
- Point source dose rate calculation
- Shielding calculations with exponential attenuation + simple buildup
- Material selection (lead, concrete, water, iron, etc.)

---

## Requirements

- Python 3.9+
- NumPy, SciPy, Matplotlib
- Streamlit (for the GUI tool)

See `requirements.txt`.

---

## Educational Goals

These tools are intentionally transparent and well-commented so students can:
1. Understand the underlying physics equations
2. Modify parameters and observe effects
3. Extend the codes (e.g., multi-group kinetics, 2D Monte Carlo, better buildup factors)

---

## Future Improvements

- Multi-group point kinetics
- 2D/3D Monte Carlo with better geometry
- Integration with OpenMC for advanced users
- More realistic delayed neutron groups (6-group)
- Temperature feedback in kinetics
- GUI versions for all tools

---

## License

MIT License – free for educational and personal use.

---

**Author:** Nuclear Engineering student @ FUT Minna  
Built for learning. Contributions and improvements welcome.

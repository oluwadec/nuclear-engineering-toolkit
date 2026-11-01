# Simple 1D Monte Carlo Neutron Transport

Educational analog Monte Carlo code for neutron transport in a one-dimensional slab.

## What you learn

- How particle histories are sampled
- Collision vs. surface crossing logic
- Basic tallies (current and flux)
- Statistical nature of Monte Carlo (run with different particle numbers)

## Limitations (intentional)

- 1D only
- Highly simplified scattering (μ = ±1)
- No energy dependence
- No fission / multiplication

These simplifications keep the code short and readable while teaching the core algorithm.

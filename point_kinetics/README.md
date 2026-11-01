# Point Kinetics Reactor Simulator

Solves the classic point reactor kinetics equations with one effective delayed neutron group.

## Physics

The point kinetics model assumes the neutron flux shape is fixed in space and only the amplitude changes with time. This is an excellent approximation for many transients.

**Equations:**

$$
\frac{dn}{dt} = \frac{\rho - \beta}{\Lambda} n + \lambda C
$$

$$
\frac{dC}{dt} = \frac{\beta}{\Lambda} n - \lambda C
$$

## Usage

```bash
python point_kinetics_simulator.py
```

Modify the reactivity function (`step_reactivity`, `ramp_reactivity`, or write your own) to explore different insertion scenarios.

## Suggested Experiments

1. Prompt critical insertion ($\rho > \beta$)
2. Very slow ramp
3. Effect of changing $\Lambda$ (prompt generation time)
4. Compare one-group vs. thinking about six-group delayed neutrons

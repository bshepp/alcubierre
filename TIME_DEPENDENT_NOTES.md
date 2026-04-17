# Slice 3: Time-Dependent Acceleration Profile — Notes

**Source:** [`time_dependent.ipynb`](time_dependent.ipynb).
**Written:** 2026-04-17 (Session 9).

---

## TL;DR

**Package 3's steady-state-plus-Lorentz-boost analysis is qualitatively correct.** The genuine $\dot v$ correction to the wall stress-energy during a $\tanh$-ramp acceleration is small (~0.3% of the static $\rho_p$ peak at $\tau = R/c$, scaling as $1/\tau$) and **antisymmetric in the axis-of-motion coordinate $x$**. The antisymmetry means there's no net momentum injection from this correction at the quadrupole order — it just shifts proper energy density forward of the wall by an equal amount it removes from behind.

**Implication for Package 3.** The three-mechanism conclusion transfers to the genuinely time-dependent setting. The "steady-state" assumption was *not* load-bearing in Package 3's negative result.

**The audit interleave (TRUST_AUDIT #5) is wired for Colab**: the `sxs` waveform pull cell runs cleanly when `sxs` is installed (Colab) and falls back to Package 3's heuristic value (5000 km/s) when not available (local Windows). Locally executed: fallback. To upgrade, open in Colab and re-run the cell.

---

## What was actually computed

Time-dependent Alcubierre metric in the bubble-comoving frame:

$$ds^2 = -dt^2 + (dx - v(t) f(r) dt)^2 + dy^2 + dz^2,\qquad r = \sqrt{x^2 + y^2 + z^2}.$$

Built the full 4D Einstein tensor $G_{\mu\nu}$ symbolically with $v$ as an abstract function and $f$ as an abstract function of $r$, then substituted concrete forms (tanh ramp for $v(t)$; Alcubierre tanh-bump for $f(r)$) using `expr.replace(f_call, f_concrete).replace(v_call, v_concrete).doit()` (the chain rule then handles all derivatives correctly).

### Cell 5: 9 of 10 components have $\dot v$ contributions

Only $G_{yz}$ has identically zero dynamic correction. The other nine components (including $G_{tt}, G_{tx}$, etc.) have non-zero terms proportional to $\dot v$ or $\ddot v$.

### Cells 11, 13: the $\dot v$ correction to $G_{tt}$ is antisymmetric in $x$

Cell 11 sampled along a line at fixed $y = R, z = 0$ with $x$ varying. The dynamic-vs-static comparison (at fixed $v = \beta/2$, only $\dot v$ varying) shows:

- $\Delta\rho_p$ peaks at $\sim \pm 9.5 \times 10^{-7}$ on the forward/trailing sides at $\tau = R/c$, $\beta = 0.1$.
- The static $\rho_p$ peak is $2.8 \times 10^{-4}$, so the ratio $|\Delta\rho_p|^{\rm peak} / |\rho^{\rm static}|^{\rm peak} = 0.003$.
- **Antisymmetric in $x$**: positive for $x > 0$ (forward of bubble centre), negative for $x < 0$.

Cell 13: empirical $\tau$-scaling slope is exactly **−1.000** (linear in $\dot v$, not quadratic). At fast ramps ($\tau = 0.01 R/c$): ratio ≈ 0.33. At slow ramps ($\tau = 100 R/c$): ratio ≈ $3 \times 10^{-5}$.

### Cell 15: GW radiated power during the ramp

Computed the bulk quadrupole moment $Q_{xx}(t)$ on the WEC-respecting region of $\rho_p$, finite-differenced for $\dddot Q$, and used the Landau-Lifshitz quadrupole formula $P_{\rm GW} = \tfrac{3}{10} \dddot Q_{xx}^2$ for axisymmetric drives. Sample numbers:

- $\dddot Q_{xx}$ peaks during the ramp at $|t| \sim \tau$.
- Total radiated GW energy is finite and scales as $\beta^2/\tau^3$.
- **For axisymmetric drive, the quadrupole-order *momentum* recoil is zero** by symmetry. Real momentum recoil requires a quadrupole-octupole beat — which we cannot easily isolate in the comoving frame. Package 3's binary-analog ceiling on Mechanism C therefore stands.

---

## Audit interleave: TRUST_AUDIT #5

Cell 17 implements the `sxs` waveform pull as a Colab-runnable upgrade:

```python
try:
    import sxs
    sim = sxs.load('SXS:BBH:1937')
    final_v_kick = float(np.linalg.norm(sim.metadata.remnant_velocity))
    # Compare to Package 3's heuristic input (5000 km/s)
    ...
except ImportError:
    print('sxs not installed; falling back to Package 3 heuristic value 5000 km/s.')
```

**Status**: cell present and tested for the fallback path. To upgrade to A-grade, open `time_dependent.ipynb` in Colab, run the setup cell (auto-installs `requirements.txt` + we'd need to add `sxs` separately), and re-run cell 17. The expected outcome is that the SXS:BBH:1937 remnant velocity matches Varma et al. 2022's reported 5000 km/s to within a factor of 1.5 (within the precision of the heuristic-vs-real comparison).

---

## Implication for the project

Slice 3 confirms that the *steady-state* assumption was not load-bearing in Package 3's negative result. The narrowing continues:

| Sub-assumption | Status (after Slices 1, 2, 3) |
|---|---|
| Single-mode axisymmetric shift | Slice 1: not load-bearing within tested family. |
| Krasnikov wall is bare-vacuum (no matter) | Slice 2: not load-bearing for single-bump matter perturbations. |
| Steady-state metric + Lorentz boost | **Slice 3: not load-bearing.** Time-dependent corrections at physical timescales are sub-1%. |
| Asymptotically flat vacuum exterior | **Open** (Slice 5). |
| 4D Einstein gravity | **Open** (Slice 6). |
| Quantum-inequality bounds tight | **Open** (Slice 4). |

**The remaining load-bearing assumptions are the *background* (vacuum + asymptotic flatness + Einstein gravity) and the *quantum/classical interpretation* (whether QI bounds are as tight as Pfenning-Ford suggested).** Slices 4-6 test these.

---

## Citations

- Schuster, Santiago & Visser 2023 (arXiv:2310.10871) — steady-state ADM 4-momentum theorem, the formal target of Slice 3.
- Varma et al. 2022 (arXiv:2208.02805) — record BBH-merger kick, used as Package 3's heuristic input and Slice 3's audit-cell target.
- Maggiore *Gravitational Waves* Vol. 1 (2007) — quadrupole formula used in Cell 15.
- Package 3: [`acceleration.ipynb`](acceleration.ipynb).

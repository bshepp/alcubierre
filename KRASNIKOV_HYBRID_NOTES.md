# Krasnikov Hybrid Quantum/Classical Wall — Notes

**Companion to:** [krasnikov_hybrid.ipynb](krasnikov_hybrid.ipynb)
**Slice:** Phase 2C / Slice 4b (Task 2A.13b, Session 23)
**Status:** Closed — negative.
**Trust grade:** A (derived in our notebook from B-grade Everett-Roman 1997 + Krasnikov 2003 inputs).
**Slice scope:** Krasnikov-tube radial wall (cylindrical, $x$-translation invariant), static observer, $\eta\in[10^{-2},1)$, $\epsilon\in[10^{-2},1]\,\mathrm{m}$, $n=\rho_{\max}/\epsilon\in[2,100]$, tube length $D\ge 1\,\mathrm{m}$. Out of scope: ANEC-only criteria, designs that classically satisfy DEC, Planck-sub-$\mathrm{m}$ tubes.

## Headline

> Within the slice, the quantum negative-energy supplement required to repair pointwise DEC failures of a classical Krasnikov-tube wall **exceeds the Krasnikov 2003 §3.3 milligram budget by no fewer than 31 orders of magnitude**. The mg-scale "tail" identified as the non-classical residue in [KRASNIKOV2003_EVALUATION.md](KRASNIKOV2003_EVALUATION.md) cannot serve as a quantum patch.

Numerical anchor (Cell 9 of [krasnikov_tube.ipynb](krasnikov_tube.ipynb), $\eta=0.5,\,\epsilon=1\,\mathrm{m},\,\rho_{\max}=10\,\mathrm{m}$):

| Quantity | Value |
|---|---|
| $\rho_p^{\min}$ (geo, length$^{-2}$) | $-6.72\times10^{-2}$ |
| $\Delta_{\rm DEC}^{\max}$ (geo) | $+1.33\times10^{-1}$ |
| $\mathcal{I}=2\pi\!\int\!\Delta_{\rm DEC}\rho\,d\rho$ (geo, m$^{-1}$) | $+2.67$ |
| $\mathcal{I}\cdot c^2/G$ | $3.60\times10^{30}\,\mathrm{g/m}$ |
| Headline ratio $r$ at $D=1\,\mathrm{m}$ | $3.60\times10^{33}$ |

Sweep result over the full $(\eta,\epsilon,n)$ grid (360 points): $r_{\min}(D=1\,\mathrm{m})=1.10\times10^{31}$.

## Method (5 steps)

1. **Pointwise DEC deficit.** From the Krasnikov-tube classical stress-energy in the static-observer orthonormal frame (`hf_jobs/sweeps/krasnikov_tube.py::_T_orthonormal`), define $\rho_p=-T_{\hat t\hat t}$, $p_{\max}=\max(|T_{xx}|,|T_{rr}|,|T_{\phi\phi}|)$, $|T_{\hat t\hat x}|$, and the pointwise dominant-energy deficit
$$\Delta_{\rm DEC}(\rho_{\rm cyl})=\max\!\left(0,\ \max(p_{\max},|T_{\hat t\hat x}|)-\rho_p\right).$$
2. **Cylindrical integral per unit length.** With $x$-translation invariance,
$$|E_Q^-|_{\rm req}(\eta,\epsilon,\rho_{\max},D)\;=\;D\cdot 2\pi\!\int_0^\infty\!\Delta_{\rm DEC}\,\rho_{\rm cyl}\,d\rho_{\rm cyl}\;\equiv\;D\cdot\mathcal{I}(\eta,\epsilon,\rho_{\max}).$$
3. **Geometrized $\to$ grams.** $c^2/G\approx 1.347\times10^{30}\,\mathrm{g/m}$.
4. **Headline ratio.** $r(D)=|E_Q^-|_{\rm req}(D)/10^{-3}\,\mathrm{g}$.
5. **Sweep.** $\eta\in\{12\text{ pts on }[10^{-2},0.99]\}$, $\epsilon\in\{0.01,0.0316,0.1,0.316,1\}\,\mathrm{m}$, $n\in\{2,5,12,32,80,100\}$ ⇒ 360 points; report $r$ at $D\in\{1\,\mathrm{m},\,1\,\mathrm{km},\,4\times10^{16}\,\mathrm{m}\}$.

## Verification gates (all PASS)

- **(i) Inner-edge anchor**: $\rho_p^{\min}=-0.067$ straddles Everett-Roman saturation $-1/(8\pi\epsilon^2)=-0.040$ and the linearised $-\eta/(8\pi\epsilon^2)=-0.020$. ✓
- **(ii) Universal $\epsilon^2$ collapse**: $\mathcal{I}\cdot\epsilon^2$ and $\Delta_{\rm DEC}^{\max}\cdot\epsilon^2$ are $\epsilon$-independent at fixed $(\eta,n)$ — verified at $\epsilon\in\{0.1,1,10\}$, $(\eta,n)=(0.5,10)$: $\mathcal{I}\epsilon^2=2.6698\times10^{-2,0,2}$, $\Delta_{\rm DEC}^{\max}\epsilon^2=0.1330$ in all three rows. Confirms Phase 2A.13 result that Krasnikov stress-energy is governed by $\rho_p\propto\eta/\epsilon^2$ ([KRASNIKOV_TUBE_NOTES.md](KRASNIKOV_TUBE_NOTES.md) §9). ✓
- **(iii) Everett-Roman $\alpha$-band**: $\alpha=|E_{\rm class}^{\rm per~length}|\cdot\epsilon/\rho_{\max}=0.133$ at the anchor, inside Everett-Roman §3 expected $\mathcal{O}(0.01\!\!-\!\!1)$. ✓

## Why the deficit is huge

Two compounding factors:

1. **Geometrized $\to$ SI mass conversion**: the deficit is $\mathcal{O}(1)$ in geometrized length$^{-2}$ but $c^2/G\sim 10^{30}\,\mathrm{g/m}$ converts even modest $\mathcal{I}$ (in m$^{-1}$) into $\sim 10^{30}\,\mathrm{g/m}$.
2. **Linear $D$ scaling with no compensation**: the wall integrand is $x$-independent, so reducing $D$ proportionally reduces the deficit, but to bring $r$ below 1 one needs $D\lesssim 10^{-31}\,\mathrm{m}$ — far below the Planck length.

The Krasnikov 2003 §3.3 budget is fixed at $\sim 10^{-3}\,\mathrm{g}$ regardless of $D$ (it tracks the *total* non-classical tail, not a per-length density). It is therefore impossible for any classical Krasnikov tube of macroscopic length to receive a sufficient quantum patch from this budget.

## Caveats and what this does NOT close

- Pointwise DEC, not ANEC. Models satisfying ANEC averaging (Fewster-Roman 2003) but failing pointwise DEC are not addressed.
- Locked to the Krasnikov-tube ansatz of [krasnikov_tube.ipynb](krasnikov_tube.ipynb); designs that classically satisfy DEC and only need a parametrically small supplement are a different slice.
- Static observer only; rotating / boosted frames may give different $\rho_p$ minima but the integrated geometric scale will not change by 30 OoM.
- The $1/\rho_{\rm cyl}$ Christoffel terms in `_T_orthonormal` require a strictly positive lower edge for the radial grid; Cell 4 clamps `rho_lo = max(rho_max-margin*eps, 1e-3*eps)`. The wall is exponentially localised at $\rho_{\max}\gg\epsilon$ so this clamp loses no physics (verified: $\Delta_{\rm DEC}$ vanishes outside the wall band in all 360 sweep points).

## Cross-links

- Stress-energy expressions: [krasnikov_tube.ipynb](krasnikov_tube.ipynb) Cell 5 (symbolic) + [KRASNIKOV_TUBE_NOTES.md](KRASNIKOV_TUBE_NOTES.md) §9.
- Origin of the mg budget: [KRASNIKOV2003_EVALUATION.md](KRASNIKOV2003_EVALUATION.md) "Direct implications" §3.3.
- Everett-Roman saturation estimate: [KRASNIKOV_TUBE_NOTES.md](KRASNIKOV_TUBE_NOTES.md) §3 + their Eq. 14.
- Quantum/classical bridge framing: [QUANTUM_CLASSICAL_BRIDGE.md](QUANTUM_CLASSICAL_BRIDGE.md).
- Landscape position: [LANDSCAPE_SYNTHESIS.md](LANDSCAPE_SYNTHESIS.md), [NAVIGATOR.md](NAVIGATOR.md) load-bearing-assumptions table (row: "small quantum supplement could repair classical wall" → falsified within slice).

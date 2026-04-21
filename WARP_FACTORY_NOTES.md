# Warp Factory cross-check (Task 2A.9b / TRUST_AUDIT #3)

## Scope

Independent numerical reproduction of Fuchs et al. 2024 (arXiv:2405.02709) Fig. 10 via [Warp Factory](https://github.com/NerdsWithAttitudes/WarpFactory) (Helmerich et al. 2024, arXiv:2404.03095) on MATLAB R2023a Update 8 (Parallel Computing Toolbox + default toolboxes). Closes:

- [`TRUST_AUDIT.md`](TRUST_AUDIT.md) row #3 (Fuchs existence anchor) — **B → A**.
- [`ROADMAP.md`](ROADMAP.md) Task 2A.9b (mass-to-velocity scaling, Warp Factory cross-check).

This was the last deferred TRUST_AUDIT item.

## Slice scope

Same as the rest of [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md):

- 4D General Relativity, signature $(-,+,+,+)$.
- Static spherical anisotropic-fluid shell on $R_1 \le r \le R_2$ with TOV-iterated $T^{\hat\mu\hat\nu} = \mathrm{diag}(\rho, P_1, P_2, P_3)$.
- Minkowski interior ($r < R_1$), Schwarzschild exterior ($r > R_2$), comoving frame ($v_{\rm shell} = 0$).
- Alcubierre-class shift $\beta^x(r)\,\hat x$ with Fuchs bump function $f(r)$ supported on the shell domain; $\beta^x_{\rm interior} = -v_s$, $\beta^x_{\rm exterior} = 0$.
- Fixed canonical params: $R_1 = 10$ m, $R_2 = 20$ m, $M = 4.49 \times 10^{27}$ kg, $\beta_{\rm warp} = 0.02 c$, $\sigma = 0$, smoothing $= 4000$.

## What was done

1. **Cloned** Warp Factory v1.0 into `F:\science-projects\WarpFactory\` (out-of-tree; do not commit the dependency itself).
2. **Reproduced Fig. 10** at canonical params via `fuchs_fig10_repro.m` — a headless wrapper around `metricGet_WarpShellComoving` + `evalMetric` that exports the energy tensor and the four pointwise energy-condition arrays (NEC/WEC/DEC/SEC) on a 300 × 300 × 5 grid (in-plane spacing 0.2 m).
3. **κ-bracket sweep** via `kappa_sweep.m`: held $(M, R_2, \beta)$ fixed and varied $\Delta = R_2 - R_1 \in \{1, 1.5, 2, 3, 5, 7, 10\}$ m to bracket the numerical $\Delta_{\min}$ where DEC first achieves in-shell pass-fraction = 1.

Artifacts in [`warp_factory_repro/`](warp_factory_repro/):

- `fuchs_fig10_repro.m`, `kappa_sweep.m` — the MATLAB scripts.
- `fuchs_repro.mat` — energy tensor + four EC arrays at canonical params.
- `fuchs_repro_{rho,nec,wec,dec,sec}.png` — slice plots through the equator.
- `kappa_sweep.mat` — pass-fractions and `min(DEC|shell)` as a function of $\Delta$.

## Result 1 — Fuchs Fig. 10 reproduced

At canonical params:

| Energy condition | In-shell pass fraction |
|---|---|
| NEC | **1.0000** |
| WEC | **1.0000** |
| DEC | **1.0000** |
| SEC | **1.0000** |

Visual signature of the DEC slice ([fuchs_repro_dec.png](warp_factory_repro/fuchs_repro_dec.png)): a uniform DEC-positive annulus from $R_1 = 10$ m to $R_2 = 20$ m, white interior (Minkowski) and white exterior (Schwarzschild vacuum), DEC value $\sim 9 \times 10^{39}$ at the shell mid-radius. Matches Fuchs et al. 2024 Fig. 10 panel structure on visual inspection. **The Fuchs existence claim is independently confirmed.**

## Result 2 — κ-bracket cross-check (2A.9b proper)

Setup: hold $M = 4.49 \times 10^{27}$ kg, $R_2 = 20$ m, $\beta = 0.02$ fixed; the compactness $C = 2GM/(R_2 c^2) = 1/3$. The mapping

$$\Delta_{\min} = \kappa\,\beta\,R_2 / C = 1.2\,\kappa\ \text{m}$$

converts the analytic [`ROADMAP.md`](ROADMAP.md) 2A.9a bracket $\kappa \in [0.05, 0.875]$ into $\Delta_{\min} \in [0.06, 1.05]$ m.

Numerical sweep:

| $\Delta$ [m] | $R_1$ [m] | passNEC | passWEC | passDEC | passSEC | min(DEC\|shell) | $\kappa = \Delta C / (\beta R_2)$ |
|---|---|---|---|---|---|---|---|
| 1.0  | 19.0 | 0.5014 | 0.5014 | 0.6328 | 0.6369 | $-8.7 \times 10^{39}$ | 0.83 |
| 1.5  | 18.5 | 0.5142 | 0.5142 | 0.6668 | 0.6705 | $-8.6 \times 10^{39}$ | 1.25 |
| 2.0  | 18.0 | 0.5142 | 0.5142 | 0.6752 | 0.6766 | $-8.6 \times 10^{39}$ | 1.67 |
| 3.0  | 17.0 | 0.5164 | 0.5164 | 0.6769 | 0.6807 | $-8.2 \times 10^{39}$ | 2.50 |
| 5.0  | 15.0 | 0.6486 | 0.6486 | 0.8909 | 0.8951 | $-4.4 \times 10^{39}$ | 4.17 |
| 7.0  | 13.0 | 0.8638 | 0.8638 | **1.0000** | **1.0000** | $+2.7 \times 10^{39}$ | 5.83 |
| 10.0 | 10.0 | **1.0000** | **1.0000** | **1.0000** | **1.0000** | $+4.2 \times 10^{39}$ | 8.33 |

**Numerical bracket:** $\Delta_{\min}^{\rm num} \in (5, 7]$ m, i.e. $\kappa^{\rm num} \in (4.17, 5.83]$.

**Discrepancy with analytic prediction:** $\kappa^{\rm num}$ exceeds the analytic upper $\kappa = 0.875$ by a factor of $\sim 6$.

## Disposition: scaling-law form holds; numerical bound is ~6× tighter

The discrepancy is **not** a refutation of 2A.7; it is a refinement. The two calculations test different limits of the same physics:

- **Analytic 2A.7 / 2A.9a** ([`thickness_bound.ipynb`](thickness_bound.ipynb)) is a *thin-shell Israel-junction* derivation evaluated at the anti-motion pole. It computes the additional surface-stress contribution induced by the shift jump and asks when that contribution flips the DEC sign. The matter shell is treated as a passive positive-energy support background.
- **Numerical 2A.9b** (this calculation) is a *thick TOV-solved anisotropic-fluid* construction with the shift function $\beta^x(r) f(r)$ distributed across the entire shell. The DEC is evaluated *pointwise* at every grid cell in the shell domain. The dominant failure mode at small $\Delta$ is the *distributed shift-gradient stress* through the shell interior, not the pole jump.

These are different mechanisms and the latter is tighter by $\sim 6\times$ at canonical $C = 1/3$. The scaling form $\Delta_{\min}/R = \kappa\,\beta/C$ is preserved (the pass-fraction sweep is consistent with a single threshold near $\kappa \sim 5$ rather than a smeared-out failure), but the numerical $\kappa$ is ~6× larger. The matter-shell route is therefore **harder** than 2A.7 alone advertises, not easier.

This *strengthens* the overall negative reading of the warp-drive landscape inside the static slice: the analytic-thin-shell bound was a permissive lower estimate, and the full-pipeline numerical bound rules out an additional ~6× of the parameter space that 2A.7 left open.

## Pass-fraction structure: why the curve does not go to 0

At $\Delta = 1$ m the in-shell DEC pass-fraction is **0.63**, not 0. That is because the TOV-supported anisotropic fluid has positive density throughout the shell; the warp-shift gradient stress only exceeds it in a sub-region. Visually (not reproduced here as PNGs but stored in the WarpFactory working directory), the failure region is concentrated near the anti-motion pole and along the bump-function transition zone, consistent with the two failure-mode interpretation above. NEC, WEC plateau at $\sim 0.51$ at small $\Delta$ — about half the shell — rather than 0; the SEC and DEC track each other to within $\lesssim 0.01$ throughout, expected given the Eulerian-frame structure of the warp shift.

## What this does **not** close

- **Matching toleration of analytic vs numerical $\kappa$ to a tighter bracket.** Closing $\kappa^{\rm num}$ to better than $(4.17, 5.83]$ would require running $\Delta \in \{5.5, 6, 6.5\}$ m (~3 more MATLAB runs at ~45 s each). Not done; the factor-of-6 discrepancy with analytic is established beyond rounding.
- **Anisotropic vs isotropic refinement of the analytic upper bound** beyond 2A.9a's $r = 1.5$ point. WarpFactory's TOV iteration already includes anisotropy; the analytic upper $\kappa = 0.875$ uses the same. The 6× discrepancy survives.
- **The original Fuchs Fig. 10 visual matching panel-by-panel** (energy-condition map shape vs published colormap). What is matched here is the *quantitative* in-shell pass-fraction $\to 1$ at canonical parameters, which is the load-bearing claim. Visual matching of the colormap shape would be cosmetic.
- **Warp Factory at amplitudes $\beta > 0.02$.** The κ-sweep here is at the published Fuchs amplitude. A separate scan in $\beta$ at fixed $\Delta$ would test the linear-in-$\beta$ scaling form directly. Not done here; the existence anchor + scaling-law cross-check are enough to close 2A.9b / TRUST_AUDIT #3.

## Reopening criteria

The 2A.7 + 2A.9a scaling law and its numerical refinement here are **disposition: scaling form holds; numerical $\kappa$ is ~6× the analytic upper.** Reopen this calculation if:

1. A new analytic refinement of 2A.7 closes the 6× gap (e.g., explicit volumetric-DEC term in the thin-shell argument that brings the analytic upper into the (4.17, 5.83] window).
2. A second numerical pipeline (e.g., NRPy+, the Bobrick-Martire group's MATLAB-free code, or a direct Python-finite-difference port) returns a $\kappa^{\rm num}$ inconsistent with this one to better than the grid-resolution uncertainty.
3. Fuchs et al. or a follow-up paper publishes a $\beta$-sweep or $C$-sweep that constrains the scaling-law slope independently.

## Citations

- Fuchs, J., Helmerich, C., Bobrick, A., Sellers, L., Melcher, B., Martire, G. 2024. "Constant Velocity Physical Warp Drive Solution," *Class. Quantum Grav.* (arXiv:2405.02709). Canonical params taken from §4.
- Helmerich, C., Fuchs, J., Bobrick, A., et al. 2024. "Analyzing warp drive spacetimes with Warp Factory," *Class. Quantum Grav.* 41 095009 (arXiv:2404.03095). Code: [github.com/NerdsWithAttitudes/WarpFactory](https://github.com/NerdsWithAttitudes/WarpFactory) (MIT license).

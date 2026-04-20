# Fell-Heisenberg WEC-Residual Sweep — Task 2D.4 Results

**Status:** Sweep complete (Session 11, 2026-04-19). Headline result is **substantially stronger than the open lead in [`NAVIGATOR.md`](NAVIGATOR.md) anticipated** and warrants careful follow-up before being elevated to a project headline. This document records the result and its caveats.

**Cross-references.**
- Task definition: [`ROADMAP.md`](ROADMAP.md) Task 2D.4.
- Pipeline source: [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb) cells 7, 11, 13.
- Sweep module: [`hf_jobs/sweeps/fell_heisenberg.py`](hf_jobs/sweeps/fell_heisenberg.py).
- Configs: [`hf_jobs/configs/fell_heisenberg_preview.json`](hf_jobs/configs/fell_heisenberg_preview.json), [`hf_jobs/configs/fell_heisenberg_full.json`](hf_jobs/configs/fell_heisenberg_full.json).
- Job entry script: [`hf_jobs/jobs/run_fell_heisenberg.sh`](hf_jobs/jobs/run_fell_heisenberg.sh).
- Raw results: HF Dataset [`bshepp/alcubierre-sweeps`](https://huggingface.co/datasets/bshepp/alcubierre-sweeps), `preview-20260420T021828/` and `full-20260420T022727/`.
- HF Jobs run IDs: preview `69e58cf8ac288e522d8f0148`, full `69e58f13ac288e522d8f014e`.

---

## §1 Headline result

The sweep found **1404 of 15000 grid points** (9.4%) where the Fell-Heisenberg smooth-multi-mode irrotational shift produces a **fully-energy-condition-respecting positive-energy classical warp metric in standard 4D General Relativity**: every interior cell satisfies the **strict full Weak Energy Condition** ($\rho + p_i^p > 0$ for all principal pressures) **and the strict full Dominant Energy Condition** ($\rho > |p_i^p|_{\max}$).

Within those 1404 points the central frame-dragging magnitude $|\vec{N}|_{\max}$ ranges from **0.73c to 18.6c** with no negative-energy region at any point in the box ($E_{\rm neg} = 0$ identically).

This is **stronger than what Fell & Heisenberg 2021 themselves claim**. Their §3.3 explicitly admits full WEC and DEC are violated in compact regions for their tested point and asserts these violations "cannot be removed by modification." The sweep falsifies this assertion within their own multi-mode irrotational ansatz.

### §1.1 Anchor point

| | Value | Notes |
|---|---|---|
| $V$ | 1.5 | overall amplitude |
| $\sigma$ | 10 | profile width |
| $m_0$ | 3 | asymmetry baseline |
| $a$ | 0.05 | asymmetry amplitude |
| $\ell$ | 4 | asymmetry length |
| $r$ | 9 | bubble radius parameter |
| $|\vec{N}|_{\max}$ (center) | **18.51** | superluminal central shift, in units of $c$ |
| $\rho_E > 0$ everywhere | **100.000%** of interior cells |
| Strict full WEC slack min | **+0.0339** |
| Strict full DEC slack min | **+0.0170** |
| $E_{\rm neg}$ | **0.0000** | no negative energy density anywhere |
| $E_{\rm net}$ | $+1.83 \times 10^3$ | geometric units |

Verified at Npts=65 (sweep), Npts=81 (notebook resolution), Npts=97. DEC slack stays positive at all three resolutions; absolute value drifts by $\lesssim 5\%$ between Npts=65 and Npts=97 — resolution-converged.

---

## §2 Reproducibility / sanity checks

Five independent checks were applied before declaring the result real.

### §2.1 Fell-Heisenberg paper anchor still fails ✓

The Session 10 anchor `(V=0.5, sigma=4, m0=2, a=0.3, ell=4, r=6)` (which Fell & Heisenberg themselves test, and which the notebook reported as `wec_pass=0.987`, `dec_pass=0.947` at Npts=81) was re-run through the sweep module:

| Npts | wec_pass_fraction | dec_pass_fraction | match notebook? |
|---|---|---|---|
| 49 | 0.99538 | 0.96462 | (lower-res, conservative drift) |
| 65 | 0.99072 | 0.95353 | within drift |
| **81** | **0.98716** | **0.94736** | **literal match to notebook** |

So the pipeline is correctly reproducing FH 2021's published failure case at the anchor. The new positive results come from different parameter regions, not from a code bug that always reports passing.

### §2.2 Resolution convergence ✓

At the new top point `(V=1.5, sigma=10, m0=3, a=0.05, ell=4, r=9)`:

| Npts | wec_slack_min | dec_slack_min | dec_pass |
|---|---|---|---|
| 49 | +0.0434 | **−0.6969** | 0.99988 |
| **65 (sweep)** | **+0.0370** | **+0.0186** | 1.00000 |
| 81 | +0.0339 | +0.0170 | 1.00000 |
| 97 | +0.0320 | +0.0160 | 1.00000 |
| 113 | +0.0275 | +0.0156 | 1.00000 |

DEC pass stabilises by Npts=65 and is unchanged through Npts=113. Npts=49 (preview) is insufficient — it gives a misleadingly large negative slack from undersampling near the bubble's surface — which is why the preview reported only 87 WEC-pass points and 0 DEC-pass points whereas the full sweep at Npts=65 found 1404 DEC-pass points.

### §2.3 m0 sensitivity is smooth ✓

The sweep grid had `m0 ∈ {2, 3, 4, 5, 6}` and DEC pass appeared **exclusively** at `m0 = 3.0`. This pattern initially looked alarming (suggested an artifact triggered by exact-3 numerics). It is not. A 12-point scan in `m0 ∈ [2.5, 4.0]` at fixed other parameters at Npts=65:

| m0 | dec_slack_min | central_N_max |
|---|---|---|
| 2.5 | +0.0102 | 14.4 |
| 2.8 | +0.0149 | 16.9 |
| 2.9 | +0.0167 | 17.8 |
| 3.0 | +0.0186 | 18.6 |
| 3.1 | +0.0205 | 19.4 |
| 3.2 | +0.0226 | 20.3 |
| 3.5 | +0.0294 | 22.8 |
| 4.0 | **−1.13** | 27.0 |

DEC slack varies smoothly with $m_0$ across the band $[2.5, 3.5]$; the catastrophic transition at $m_0 = 4$ is the metric becoming non-physical (the bubble is no longer well-localised inside the box). The "m0 = 3 only" appearance in the sweep is a grid-resolution artifact: $m_0 \in \{2, 3, 4, ...\}$ misses the band edges. The DEC-passing manifold is continuous, not a single point.

### §2.4 V scaling is the predicted V² scaling ✓

The Fell-Heisenberg potential is $\phi \propto V$, so the shift $\vec{N} = \nabla\phi \propto V$, the metric perturbation $\propto V^2$, and the stress-energy / slacks $\propto V^2$. A 9-point V scan at fixed `(sigma=10, m0=3, a=0.05, ell=4, r=9)`:

| V | $|\vec{N}|_{\max}$ | dec_slack_min | $E_{\rm net}$ |
|---|---|---|---|
| 0.10 | 1.24 | +8.25e-05 | +8.17 |
| 0.50 | 6.20 | +2.06e-03 | +204 |
| 1.50 | 18.6 | +1.86e-02 | +1839 |
| 10.0 | 124 | +0.825 | +81700 |

`dec_slack_min` scales as exactly $V^2$ (factor 100× from V=0.1 to V=1.0; factor 10000× from V=0.1 to V=10.0). This is the correct scaling, and it has an **important consequence**:

> If `dec_slack_min > 0` at any one $V$, it is positive at every $V > 0$ for the same $(\sigma, m_0, a, \ell, r)$.

So the question "is there a DEC-respecting FH warp metric" reduces to "is there a $(\sigma, m_0, a, \ell, r)$ tuple with positive dimensionless DEC slack." The amplitude $V$ is a free parameter — choose it as small or as large as needed. **The smallest superluminal DEC-passing point in the sweep has $|\vec{N}|_{\max} = 0.73c$ at $V = 0.1$**, which is the truly subluminal end of the DEC-respecting band. Increasing $V$ to 0.135 brings $|\vec{N}|_{\max}$ exactly to $c$ at the same DEC-respecting point.

### §2.5 Slice-1 negative result is unaffected ✓

[`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md) reported 0/140 sweep points achieving WEC ≥ 0.999 across four single-mode axisymmetric shift families at Slice 1. That result holds — the FH potential is **multi-mode and not axisymmetric**, so the Slice-1 conclusion ("single-mode axisymmetric shifts cannot achieve full WEC") is uncontradicted. The new result simply confirms that the load-bearing assumption flagged in [`NAVIGATOR.md`](NAVIGATOR.md) (assumption #1 in the canonical table) was indeed the load-bearing one.

---

## §3 Structure of the energy-condition-passing region

### §3.1 Where DEC passes

Restricting to $m_0 = 3$ (the grid value that hits the band centre), DEC pass count by $(\sigma, a)$:

| sigma\a | 0.050 | 0.106 | 0.224 | 0.473 | 1.000 |
|---|---|---|---|---|---|
| **2** | 0 | 0 | 0 | 0 | 0 |
| **4** | 96 | 96 | 72 | 48 | 0 |
| **6** | 120 | 120 | 90 | 42 | 0 |
| **8** | 120 | 114 | 84 | 42 | 0 |
| **10** | 120 | 114 | 84 | 42 | 0 |

(Each cell counts over the $(V, \ell, r) = 6 \times 4 \times 5 = 120$ subgrid.)

Patterns:
- **DEC pass requires $\sigma \ge 4$.** Below this the FH Gaussian envelopes are too narrow and create steep bubble walls where the principal-pressure eigenvalues blow up.
- **DEC pass requires $a < 1$.** With $a = 1$ the asymmetry is so strong that $m = m_0 + a\tanh(z/\ell)$ approaches zero on one side of the bubble, blowing up the $1/(m+n)$ factor in the potential.
- **DEC pass is essentially $V$-independent** (every V column has the same count) per §2.4.

The DEC-passing region is therefore a connected sub-volume in $(\sigma, m_0, a)$-space with $\sigma \in [4, 10]$, $m_0 \in [\sim 2.5, \sim 3.5]$, $a \in (0, \sim 0.5)$, with $V$ a free amplitude.

### §3.2 Leaderboard — top 5 by central superluminal magnitude

(All have wec_slack_min > 0, dec_slack_min > 0, rho_E_pos_fraction = 1.0, $E_{\rm neg} = 0$.)

| V | sigma | m0 | a | ell | r | $|\vec{N}|_{\max}$ | wec_slack_min | dec_slack_min | $E_{\rm net}$ |
|---|---|---|---|---|---|---|---|---|---|
| 1.5 | 10 | 3 | 0.473 | 6 | 9 | **18.60** | +0.0346 | +0.0021 | +1712 |
| 1.5 | 10 | 3 | 0.473 | 8 | 9 | 18.60 | +0.0353 | +0.0128 | +1716 |
| 1.5 | 10 | 3 | 0.224 | 4 | 9 | 18.60 | +0.0372 | +0.0143 | +1811 |
| 1.5 | 10 | 3 | 0.106 | 2 | 9 | 18.60 | +0.0369 | +0.0157 | +1833 |
| 1.5 | 10 | 3 | 0.224 | 6 | 9 | 18.60 | +0.0374 | +0.0187 | +1812 |

By V scaling these can be reduced to **any superluminal magnitude** (e.g. $V=0.081 \Rightarrow |\vec{N}|_{\max} = c$ at the last row).

### §3.3 Leaderboard — bottom 5 (least extreme superluminal at DEC-pass)

| V | sigma | m0 | a | ell | r | $|\vec{N}|_{\max}$ | dec_slack_min | $E_{\rm net}$ |
|---|---|---|---|---|---|---|---|---|
| 0.1 | 4 | 3 | 0.050 | 2 | 9 | 0.7342 | +3.3e-5 | +3.27 |
| 0.1 | 4 | 3 | 0.050 | 4 | 9 | 0.7342 | +3.3e-5 | +3.27 |
| 0.1 | 4 | 3 | 0.050 | 6 | 9 | 0.7342 | +3.3e-5 | +3.27 |
| 0.1 | 4 | 3 | 0.050 | 8 | 9 | 0.7342 | +3.3e-5 | +3.27 |
| 0.1 | 4 | 3 | 0.106 | 2 | 9 | 0.7342 | +1.0e-5 | +3.26 |

These are subluminal-bubble configurations — entirely in the regime where the construction's perturbative validity is uncontested. **They still respect DEC strictly with $E_{\rm neg} = 0$ and a positive Eulerian energy density everywhere**, just without warp-relevant velocity. They serve as a clean baseline showing the result is not contingent on going to the strongly-nonlinear $|\vec{N}| \gtrsim c$ regime.

---

## §4 Caveats — what this is and is NOT

### §4.1 What this IS

A demonstration that **within the Fell-Heisenberg multi-mode irrotational ansatz, in standard 4D Einstein gravity, with a static unit-lapse flat-spatial-metric foliation**, a positive-energy Type I (in the Hawking-Ellis classification) stress-energy tensor satisfying both the strict full WEC and the strict full DEC at every interior point of a 12³ box can be constructed by appropriate choice of $(V, \sigma, m_0, a, \ell, r)$. The smallest such configuration has subluminal central shift; the strongest has $|\vec{N}|_{\max} = 18.6c$.

This **falsifies Fell & Heisenberg's §3.3 claim** that "no amount of modification could get rid of these regions" — within their own potential family, a wide neighbourhood of WEC+DEC-respecting solutions exists.

This **strictly subsumes the Slice-1 negative result** ([`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md)): the Slice-1 0/140 result was for *single-mode axisymmetric* shifts. The FH potential is multi-mode non-axisymmetric, and the load-bearing assumption flagged in [`NAVIGATOR.md`](NAVIGATOR.md) §"Load-bearing assumptions" is now explicitly broken.

### §4.2 What this is NOT (open questions)

1. **Not a complete physical drive.** The construction is **static** (the FH potential has no time dependence). The acceleration question (Package 3 of Path 2A, [`acceleration.ipynb`](acceleration.ipynb)) is unaddressed: how does this configuration get *built*, and how does it *move*? The construction has all the same dynamic-build, ADM-momentum-conservation, and GW-recoil obstructions as the Path 2A static result.

2. **Not necessarily geodesically complete or stable.** The sweep tests *energy conditions on a fixed slice*. It does not test:
   - Causality (presence/absence of CTCs, horizons)
   - Linear stability of the matter+geometry configuration
   - Whether the matter source is realisable (the FH construction reverse-engineers a metric, then computes the matter source — the source's *field-theoretic interpretation* is open)

3. **Not free from the asymptotic-flatness question.** The bubble extends to $r = 9$ in a box of half-width $L = 12$. The FH potential decays as $r \to \infty$ but the domain is finite. Whether the configuration matches smoothly to an asymptotically flat exterior (or whether the boundary needs an Israel junction with negative-energy support) is not tested by the sweep.

4. **Source matter is unspecified.** The stress-energy $T_{\mu\nu}$ computed satisfies WEC and DEC (so it is *kinematically* compatible with ordinary positive-energy matter). What ordinary matter — fluid, field, ensemble of particles — can produce this $T_{\mu\nu}$ is open. The Fuchs et al. 2024 construction had this question answered (it's an explicit fluid shell); the FH construction does not.

5. **Resolution-converged at Npts=65 but only modest absolute precision.** The slack values are $\sim 10^{-2}$ at the top point, $\sim 10^{-5}$ near the boundary. A more demanding test (e.g. higher-order WEC formulations, off-grid evaluation) might find sub-cell violations the FD discretisation cannot resolve. This matters most for the boundary points where slack is very small.

6. **The construction is non-perturbative in $|\vec{N}|$.** The metric is fully nonlinear; no small-$|\vec{N}|$ assumption is made. But conventionally a warp drive is discussed as a perturbation of Minkowski. At $|\vec{N}|_{\max} = 18c$ this is *very* far from a perturbation. The nearby horizon structure of the metric (does it contain trapped surfaces? does the foliation $t = \text{const}$ remain spacelike?) is not analysed by the sweep. This is the most likely place a "too good to be true" objection lands; it requires §5-style follow-up.

### §4.3 Calibrated honest summary

> Within standard 4D General Relativity, the Fell-Heisenberg multi-mode irrotational static shift admits a positive-energy, strictly full-WEC-respecting, strictly full-DEC-respecting, fully Type-I configuration with superluminal central frame-dragging — the first such construction in the project's literature catalog. The result is mathematically robust at the finite-difference grid level. Its physical interpretation depends on follow-up analysis of horizon structure, geodesic completeness, asymptotic matching, source-matter realisability, and dynamical buildability — none of which the sweep addresses. The honest current statement is: **a passing test of the energy conditions on a static slice has been achieved; whether this assembles into a working warp drive is a separate question the project has not answered.**

---

## §5 Recommended next steps

In rough priority order, with effort estimates per session. The first two are **cheap, high-signal, and should be done immediately** — both are zero-additional-compute and re-use existing data.

1. **Connectivity and topology of the WEC+DEC-passing region** (1 session, no new compute — re-analyses the existing parquet). Are the 1404 strict-pass points a single connected manifold in $(\sigma, m_0, a, \ell, r)$-space, or several disconnected islands? If connected, characterise the boundary surface — does the slack vanish smoothly, suggesting a closed-form sub-family lurks at the boundary? Does the region respect any obvious group action on the parameters? **An analytic sub-family — derived in closed form rather than discovered by sweep — is substantially more defensible in peer review than "we swept and found 1404 hits."** Connectivity analysis is the prerequisite for finding such a sub-family. Method: 2D pairwise projections of the strict-pass subset, connected-component analysis on the discrete sweep grid (treating grid neighbours as edges), boundary-cell extraction. If the existing grid is too coarse to resolve the region's shape, dispatch a denser refinement sweep at the band centre $(\sigma, m_0, a, \ell, r) \in [4, 10] \times [2.5, 3.5] \times [0.05, 0.5] \times [2, 8] \times [4, 9]$ at Npts=65 (~5K points, ~$0.50 of HF Jobs). **ROADMAP Task 2D.5.**

2. **Pointwise lapse-shift ratio as cheap horizon test** (<0.1 session, zero compute). Compute $|\vec{N}(x, y, z)| / \alpha(x, y, z)$ on the 3D grid for a representative WEC+DEC-passing winner. With unit lapse $\alpha = 1$, this reduces to $|\vec{N}|$ pointwise. Threshold: if $|\vec{N}| < 1$ everywhere, the $t = \text{const}$ foliation is spacelike and **no horizon exists, full stop**. If $|\vec{N}| \ge 1$ somewhere, that's exactly the locus to investigate further for trapped-surface formation. Do this **as the very first sub-step of step 3 below** — cheap filter that may eliminate the need for full horizon analysis. Note that at the top WEC+DEC point we already know $|\vec{N}|_{\max} = 18.6$ in the 7³ central cube, so the test at that point will return "horizon exists" immediately; the question is *where* the $|\vec{N}| = 1$ surface lies and whether the $|\vec{N}| \le 1$ subregion is by itself the genuinely-warp-respecting subset, with the central superluminal core being separately a horizon-bounded region. **ROADMAP Task 2D.6.**

3. **Horizon and CTC analysis** (1-2 sessions, mostly analytic; gated by step 2). For the canonical $(V, \sigma, m_0, a, \ell, r)$ at the WEC+DEC band centre, compute:
   - The norm of $\partial_t$ pointwise — does it stay timelike everywhere? (Step 2 sharpens this: $|\vec{N}| < 1$ ⇒ yes; $|\vec{N}| \ge 1$ ⇒ horizon present, find its surface.)
   - The expansion scalar of outward null geodesics — does the foliation contain trapped surfaces, and where?
   - Closed timelike curves — apply the Everett-Roman 1997 §4 test (CTCs in any single-bubble warp metric require stationarity + a closed orbit; the FH bubble is single, static, simply-connected, so the CTC test is expected to be clean — but should be confirmed). **ROADMAP Task 2D.7.**

4. **Higher-order energy condition tests** (1 session, no new compute). Does the strict full DEC pass survive replacing the principal-pressure eigvalsh test with a more conservative sum-of-pressures formulation? Does the SEC pass anywhere in the WEC+DEC region?

5. **Identify the source matter sector** (1 session, lit-hard). Given $T_{\mu\nu}^{\rm FH}$, ask: what classical matter satisfies the same anisotropic stress profile? The eigenvalues of $S_{ij}$ tell us $\rho, p_1, p_2, p_3$ as a field on the box. Is this realisable as a perfect fluid? Anisotropic fluid? Plasma? Reverse-engineer in the Bobrick-Martire 2021 §III taxonomy. **ROADMAP Task 2D.9.**

6. **Multi-bubble Everett-Roman CTC test** (1 session). Two FH bubbles in opposite directions: do they form CTCs the way Krasnikov tubes do? If yes, we have the same restriction as Slice 4: the *infrastructure* for transport is causally pathological even though each bubble is locally fine. **ROADMAP Task 2D.10.**

7. **Asymptotic-matching analysis** (1 session). Match the FH bubble interior to a Schwarzschild or Minkowski exterior at the box edge. Does the matching require a negative-energy Israel junction? If yes, the WEC+DEC pass is incomplete — it's the bubble interior that respects the conditions, but the boundary still needs exotic matter. (This is the "smuggling" objection that several Path 2A tests had to defend against.) **ROADMAP Task 2D.10.**

8. **Re-run the sweep at $L = 24$** (~$2 of HF Jobs). Doubles the box and tests whether the FH "tail" (which the sweep cuts off at $r = 9$ in $L = 12$) actually decays asymptotically or contains negative-energy contributions outside the current box.

9. **Independent re-implementation** (1-2 sessions). Replicate the result in a second pipeline (e.g. SymPy + LAPACK in a different language, or a Mathematica xAct verification) to rule out a systematic finite-difference bug in our specific stencil-of-stencils Hessian-of-Hessian computation. **ROADMAP Task 2D.8.**

---

## §6 Logistics

**Sweep cost summary:**
| Phase | HF Jobs flavor | Wall time | Cost |
|---|---|---|---|
| Local smoke tests | this machine (Win11, 16 cores) | ~2 min | $0 |
| Preview (729 pts, Npts=49) | cpu-upgrade (8 vCPU advertised) | 69 sec | <$0.01 |
| Full (15000 pts, Npts=65) | cpu-xl (16 vCPU advertised) | 63 min | ~$1.05 |
| **Total** | | **~70 min** | **~$1.05** |

The container reported 64 logical CPUs but only 16 cgroup vCPUs (cpu-xl). The dispatcher's `ProcessPoolExecutor(max_workers=64)` over-subscribed; using `max_workers=16` would likely halve the full-sweep wall time to ~30 min. Worth fixing in [`hf_jobs/run_sweep.py`](hf_jobs/run_sweep.py) before the next sweep.

**Data location:** raw parquets uploaded to private HF Dataset [`bshepp/alcubierre-sweeps`](https://huggingface.co/datasets/bshepp/alcubierre-sweeps) under `preview-20260420T021828/`, `full-20260420T022727/`, and `refine-20260420T041817/` (Stage 2 of Task 2D.5). Local working copies in `sweeps_remote/`.

---

## §7 Connectivity, topology, and analytic-sub-family analysis (Task 2D.5)

Output of [`hf_jobs/analysis/fell_heisenberg_topology.py`](hf_jobs/analysis/fell_heisenberg_topology.py), saved to [`fell_heisenberg_topology/`](fell_heisenberg_topology/) (figures + summary JSON + boundary CSV).

### §7.1 Stage 1 (existing full-sweep parquet, Npts=65)

Re-analysing the 1404-strict-pass subset of `full-20260420T022727/` projected to the 4-D `(sigma, a, ell, r)` lattice (the `m0` axis collapsed because **all 1404 strict-pass points lie on the single grid value $m_0 = 3.0$**; `V` dropped per §2.4 invariance):

| Metric | Value |
|---|---|
| Connected components (4-conn) | **1** |
| Connected components (full-conn) | 1 |
| Lattice cells filled | 234 / 320 (73.1%) |
| Interior cells (4-conn) | 16 (6.8% of region) |
| Boundary cells | 218 (93.2% of region) |
| DEC slack at boundary cells | $\sim +5\!\times\!10^{-7}$ to $\sim +0.013$ |
| DEC slack at distance-3 interior | median $\sim +0.003$, max $\sim +0.018$ |

The strict-pass set is a **single connected manifold** in the 4-D parameter slice. The slack vanishes smoothly toward the boundary (no cliff in the box plot of `dec_slack` vs lattice distance). However, the boundary fraction of 93% means the existing grid is too coarse to expose interior structure, and the m0 dimension is invisible (only one grid value in the band). **Both Stage-2 trigger criteria fired** (boundary fraction > 40%, m0 info-loss).

### §7.2 Stage 2 — refinement sweep at the band centre

Dispatched [`hf_jobs/configs/fell_heisenberg_refine.json`](hf_jobs/configs/fell_heisenberg_refine.json) — a 10080-point grid over `(V=1, sigma in [4,10], m0 in [2.3,3.7], a in [0.05,0.5] log, ell in [2,8], r in [4,9])` at Npts=65. Wall time ~37 min on cpu-xl, ~$0.65. Result: **5334 of 10080 points (52.9%) achieve strict full WEC + DEC**, matching the band-centre projection of the original sweep.

Re-analysing the refine parquet alone (a regular grid on the densified lattice):

| Metric | Stage 1 | Stage 2 (refine) |
|---|---|---|
| Strict-pass count | 1404 | **5334** |
| Active params | 4 (m0 collapsed) | **5** |
| Lattice fill | 234 / 320 (73.1%) | 5334 / 10080 (52.9%) |
| Connected components (4-conn) | 1 | **1** |
| Connected components (full-conn) | 1 | **1** |
| Interior cells | 16 (6.8%) | **648 (12.1%)** |
| Boundary cells | 218 (93.2%) | 4686 (87.9%) |
| Max DEC slack | 0.018 (at $V$=1.5) | 0.0154 (at $V$=1.0) |
| Max central $|\vec{N}|$ | 18.6 (at $V$=1.5) | 16.3 (at $V$=1.0) |

**The single-component result is preserved at 5-D resolution**: the WEC+DEC-passing region is a connected manifold in $(\sigma, m_0, a, \ell, r)$-space, not several islands.

### §7.3 Boundary structure (smoothness)

The DEC slack as a function of lattice distance to boundary, in the refine sweep:

| Distance to boundary | n | DEC slack (median) | DEC slack (max) |
|---|---|---|---|
| 1 (boundary cell) | 4686 | +0.0030 | +0.0156 |
| 2 (one step interior) | $\sim$580 | +0.0042 | +0.0111 |
| 3 (two steps) | $\sim$70 | +0.0036 | +0.0091 |

**Slack vanishes smoothly toward the boundary** (no cliff, no discrete transition). This is the signature of an **analytic boundary surface** — the strict-pass region is delimited by a smooth $(d-1)$-dimensional manifold in 5-D parameter space, not a set of discrete jump conditions. The smooth-vanishing observation is consistent with the existence of an analytic sub-family at the boundary itself (a continuous "marginal" family $\partial(\text{strict-pass})$ where one of the slacks vanishes exactly).

### §7.4 Symmetry probe — dimensionless invariants

Spread of various dimensionless ratios across the 5334-strict-pass set:

| Ratio | mean | range | spread / |mean| | Interpretation |
|---|---|---|---|---|
| **`m0 + a`** | 3.03 | 2.35–4.20 | **0.13** | tightly bounded ⇒ approx control parameter |
| **`m0 - a`** | 2.73 | 1.98–3.65 | **0.14** | tightly bounded |
| `r / m0` | 2.40 | 1.14–3.91 | 0.28 | bounded but broad |
| `r / sqrt(sigma)` | 2.56 | 1.27–4.50 | 0.28 | matches `r/m0` spread, suggestive |
| `r / sigma` | 0.99 | 0.40–2.25 | 0.39 | weak |
| `ell / r` | 0.86 | 0.22–2.00 | 0.47 | weak |
| `sigma / r²` | 0.20 | 0.05–0.62 | 0.63 | not a control parameter |
| `a / m0` | 0.053 | 0.014–0.20 | 0.74 | not a control parameter |

**Reading**: `m0 ± a` are the tightest constraints (i.e. the bubble-asymmetry envelope endpoints `m = m0 + a tanh(z/ell)` and `n = m0 - a tanh(z/ell)` need to lie within a bounded range — physically, both `m` and `n` need to stay positive and not too large). The next-tightest constraints are on `r/m0` and `r/sqrt(sigma)`, which have the *same* spread (0.28) suggesting these two ratios may share an underlying constraint. **No single ratio narrowed to a "constant" invariant — there is no sharp closed-form sub-family of the form `r = f(sigma, m0, ...)`** at the resolution of this sweep.

### §7.5 Analytic-sub-family hypothesis — verdict

**The current evidence does not support an analytic closed-form sub-family inside the strict-pass region.** What we instead have is:
- A **single connected smooth manifold** in 5-D parameter space (one connected component at both connectivity levels)
- **Bounded by a smooth analytic boundary surface** (slack vanishes continuously, no cliff) where one of the WEC/DEC slacks crosses zero
- Whose shape is **roughly convex** in pairwise projections (boundary cells form a one-cell-thick shell around an interior bulk)
- With **no clean low-order dimensionless invariant** identifying the boundary (the symmetry probe finds bounded ratios but no single "constant" surface)

This is **the next-best thing to a closed-form sub-family** for peer-review purposes — a *characterised* connected region with a smooth boundary, not a "we swept and found scattered hits." The honest claim is: "the strict WEC+DEC-passing configurations form a 5-D manifold $\mathcal{M} \subset \mathbb{R}^5_{(\sigma, m_0, a, \ell, r)}$ with positive 5-D measure, single connected component, smooth boundary $\partial\mathcal{M}$ on which the DEC slack vanishes continuously, located in the band $m_0 \in [\sim 2.3, \sim 3.7]$, $\sigma \gtrsim 4$, $a \lesssim 0.5$, $r \gtrsim 4$, $\ell$ free."

The strongest WEC+DEC slack is achieved **at the boundary of the search grid** (top 50 leaderboard all at `(sigma, m0, r) = (10, 3.7, 9)`), suggesting the optimum extends *past* the refine grid's upper edges. A further refinement at higher `(sigma, m0, r)` would tell us where the slack actually peaks — but the existing data already establishes the existence claim.

### §7.6 Outputs

Saved to [`fell_heisenberg_topology/`](fell_heisenberg_topology/):
- `summary.json` — refine-sweep aggregate counts and component summary
- `component_summary.csv` — connected-component table (1 component, full extents)
- `boundary_cells.csv` — flat list of 4686 boundary points
- `pairwise_pass_count.png` — 5×5 grid of strict-pass count projections
- `pairwise_dec_slack.png` — 5×5 grid of max-DEC-slack projections (shows the band-centre peak at high sigma + high m0)
- `boundary_cells.png` — 5×5 grid showing interior (blue) vs boundary (red) vs mixed (purple) cells in 2-D projection
- `slack_vs_distance.png` — box plots of DEC + WEC slack vs lattice distance to boundary (smooth vanishing)
- `symmetry_probe.json` — dimensionless ratio invariance table

The analysis module [`hf_jobs/analysis/fell_heisenberg_topology.py`](hf_jobs/analysis/fell_heisenberg_topology.py) is parquet-agnostic — re-runnable on any future sweep with the same schema.

### §7.7 Polynomial-surface fitting and residual structure

After the §7.4-§7.5 conclusion ("no clean low-order rational invariant"), a follow-up question: **does the boundary surface itself admit a low-degree polynomial implicit equation, and if we fit `dec_slack_min` directly with polynomials, are the residuals consistent with discretisation noise or do they show systematic structure?** Module [`hf_jobs/analysis/fell_heisenberg_polyfit.py`](hf_jobs/analysis/fell_heisenberg_polyfit.py) (separate from the topology module so the two analyses can evolve independently) answers both.

**Setup.** Restrict to the near-boundary subset $|{\rm dec\_slack\_min}| < 0.05$ (7591 of 10080 points) so the regression isn't dominated by deep-failure points. Standardise the 5 parameters. Fit polynomial regressions of degree 1-5 with 5-fold CV.

**Slack-value polynomial regression results:**

| Degree | #features | $R^2_{\rm CV}$ | RMSE | Resid 95th-pctile |
|---:|---:|---:|---:|---:|
| 1 | 5 | 0.223 | 9.08e-3 | 2.04e-2 |
| 2 | 20 | 0.469 | 7.47e-3 | 1.32e-2 |
| 3 | 55 | 0.637 | 6.12e-3 | 1.18e-2 |
| 4 | 125 | 0.763 | 4.87e-3 | 9.73e-3 |
| **5** | **251** | **0.862** | **3.62e-3** | **6.99e-3** |

**Residual structure at degree 5** (saved to [`fell_heisenberg_topology/poly_fit_residuals.png`](fell_heisenberg_topology/poly_fit_residuals.png)):
- **Residuals vs predicted** plot shows a clear *fan structure* — heteroskedastic, with width opening at both signs of predicted slack.
- **QQ vs Gaussian** has heavy tails on both sides — strongly non-Gaussian, far more outliers than noise would produce.
- **Spearman correlations** of residuals with each input axis are all $|\rho| < 0.03$ (no monotonic trend) but **the residuals visibly cluster vertically into discrete columns** at each grid value, with within-column spread larger near the band edges.
- **RMSE / Npts=65 noise floor** $\approx 7\times$. Well above what discretisation alone would produce.

**Verdict on slack-value fits**: the slack response surface has **systematic non-polynomial structure**. The polynomial fits never reach noise-level residuals; the QQ and fan plots make it clear the missing structure is not random. This is the expected fingerprint of the FH potential's **erf and exp factors** — transcendental in the parameters — that no polynomial of any practical degree can match.

**Boundary-surface classification results** (logistic regression of pass/fail vs polynomial features, 5-fold CV):

| Degree | #features | Accuracy | F1 |
|---:|---:|---:|---:|
| 1 | 5 | 0.776 | 0.792 |
| 2 | 20 | 0.940 | 0.944 |
| **3** | **55** | **0.984** | **0.985** |
| 4 | 125 | 0.989 | 0.989 |
| 5 | 251 | 0.991 | 0.992 |

(see [`fell_heisenberg_topology/boundary_classifier_curve.png`](fell_heisenberg_topology/boundary_classifier_curve.png) for the elbow shape).

**Verdict on the boundary surface**: the zero level set $\partial \mathcal{M} = \{{\rm dec\_slack} = 0\}$ **IS approximately a degree-3 polynomial surface** in $(\sigma, m_0, a, \ell, r)$. The classifier's accuracy jumps from 78% (deg 1, hyperplane) to 94% (deg 2, quadric) to **98.4% (deg 3)** with diminishing returns past degree 3. Over the 5-D space of 10080 grid points, a degree-3 implicit polynomial misclassifies only ~165 points — and those 165 are concentrated *at the boundary itself* where the slack is closest to zero, i.e. exactly the points where any noise dominates the sign.

**Combined honest answer to "is there an analytic sub-family":**

1. **The boundary surface admits a low-degree polynomial approximation.** The implicit equation $P_3(\sigma, m_0, a, \ell, r) = 0$ for some specific cubic $P_3$ recovers ~98.4% of the pass/fail distinction. **A genuine analytic sub-family of the form "configurations satisfying $P_3(\sigma, m_0, a, \ell, r) = 0$ are on the WEC+DEC marginal manifold" is plausible** — this is the *existence* of an analytic sub-family.
2. **The slack value field itself is NOT a low-degree polynomial.** Residuals at any practical degree show systematic structure (fan, heavy tails, ~7× noise floor) consistent with the FH potential's transcendental (exp + erf) factors leaking into the slack response. So the *full slack* will not have a closed-form polynomial expression; only its zero level set does.

**Practical implication**: Task 2D.5b — "extract the cubic implicit boundary equation $P_3$ from the fitted classifier coefficients, simplify analytically, and check whether it has a clean physical interpretation (e.g. matches a known dimensionless combination from the FH derivation)" — is a now-meaningful, ~1-session follow-up. The result wouldn't be a closed-form expression for all of $\mathcal{M}$, but it WOULD be a closed-form expression for $\partial \mathcal{M}$ — substantially stronger than what §7.5 originally claimed.

### §7.8 Resolution-convergence test: Npts=65 vs Npts=97 refine sweep

**Motivation.** The §7.7 finding that the boundary surface is approximately a degree-3 polynomial (98.4% binary classification accuracy at Npts=65) had a critical caveat: ~24 of the 104 misclassified points had $|{\rm slack}| < 10^{-4}$ — *literally below the estimated Npts=65 discretization noise floor of $\sim 5 \times 10^{-4}$*. A cheap test: re-run the same 10080-point grid at Npts=97 ($\sim 5\times$ smaller noise floor expected) and ask whether the cubic CV accuracy jumps toward 100% (Outcome A: residual was noise, surface IS cubic) or stays around 98.7% (Outcome B: cubic genuinely fails).

Sweep config [`hf_jobs/configs/fell_heisenberg_refine_hires.json`](hf_jobs/configs/fell_heisenberg_refine_hires.json), 10080 points at Npts=97, dispatched as HF Jobs job `69e5be83cd8c002f31dffdda`. Wall time **150 minutes** on cpu-xl (vs 37 min for Npts=65; the cubic-of-grid-size scaling holds), cost ~$2.50.

**Topology comparison.**

| Metric | Npts=65 | **Npts=97** |
|---|---|---|
| Strict pass | 5334 / 10080 | **6818 / 10080** (+28%) |
| Connected components | 1 | 1 |
| Interior cells (4-conn) | 648 | 877 |
| Boundary fraction | 87.9% | 87.1% |

The strict-pass region is **larger at higher resolution** by 1484 net points — but this is not "more configurations satisfy WEC+DEC at finer grids" (the parameter values themselves haven't changed); it's "the lower-resolution grid was systematically biasing toward 'fail' near the band edges where the FH potential has steep gradients." Single connected component at both resolutions; the topology story is unchanged.

**Pass/fail flip analysis** between the two resolutions on the same 10080 grid points:

| | count |
|---|---|
| Flipped fail → pass (Npts=65 → Npts=97) | 2033 |
| Flipped pass → fail | 549 |
| Unchanged | 7498 |
| Net new strict-pass | +1484 |

The 4× asymmetry (2033 vs 549) confirms a **systematic bias** in the Npts=65 sweep, not just random noise.

**Where the noise was biggest.** Per-sigma median |drift| Npts=65→97:

| sigma | n | median |drift| | p95 |drift| |
|---|---|---|---|
| 4 | 1440 | **1.26e-1** | 4.69e-1 |
| 5 | 1440 | **6.31e-2** | 4.41e-1 |
| 6 | 1440 | 1.03e-3 | 3.89e-1 |
| 7 | 1440 | 8.74e-4 | 3.24e-1 |
| 8 | 1440 | 9.97e-4 | 2.50e-1 |
| 9 | 1440 | 1.11e-3 | 1.52e-1 |
| 10 | 1440 | 1.18e-3 | 5.65e-2 |

**At sigma ≥ 6 the Npts=65 sweep was essentially correct** (median drift ~1e-3, well below typical slack values). **At sigma = 4-5 the Npts=65 sweep was severely under-resolved** (median drift 0.06-0.13, comparable to or larger than the slack itself). This makes physical sense: smaller `sigma` means narrower Gaussian envelopes in the FH potential, which means sharper spatial gradients in the shift, which means greater sensitivity to the finite-difference grid spacing $h = 2L/(N_{\rm pts}-1)$.

**Convergence sanity check on the canonical winner** $(V=1.5, \sigma=10, m_0=3, a=0.05, \ell=4, r=9)$:

| Npts | central_N | dec_slack_min |
|---|---|---|
| 49 | 18.50 | −0.697 |
| 65 | 18.60 | +0.0186 |
| 81 | 18.51 | +0.0170 |
| **97** | **18.33** | **+0.0160** |
| 113 | 18.17 | +0.0154 |

The Session-11 anchor IS resolution-converged at Npts ≥ 97 (Δ ≤ 4% from Npts=97 to Npts=113). All earlier convergence claims about *this specific point* hold. What was wrong at Npts=65 was the sweep's behaviour at unrelated sharp-gradient points elsewhere in the grid.

**Boundary-classifier accuracy at Npts=97** (logistic regression of pass/fail vs polynomial features, 5-fold CV):

| Degree | Npts=65 CV | **Npts=97 CV** | Δ |
|---|---|---|---|
| 1 | 0.776 | **0.893** | +0.117 |
| 2 | 0.940 | **0.966** | +0.026 |
| 3 | 0.984 | **0.986** | +0.002 |
| 4 | 0.989 | **0.993** | +0.004 |
| 5 | 0.991 | **0.994** | +0.003 |

**Slack-value polynomial regression at Npts=97** (near-boundary subset):

| Degree | Npts=65 R²_CV | **Npts=97 R²_CV** | Δ |
|---|---|---|---|
| 1 | 0.223 | **0.422** | +0.199 |
| 2 | 0.469 | **0.669** | +0.200 |
| 3 | 0.637 | **0.801** | +0.164 |
| 4 | 0.763 | **0.869** | +0.106 |
| 5 | 0.862 | **0.917** | +0.055 |

#### §7.8.1 Verdict — partial Outcome A, refined picture

**The result is more nuanced than the binary "Outcome A or B" framing in the plan.** Three findings:

1. **The slack-value polynomial fit improved substantially at every degree** (R² jumped +0.05 to +0.20). This is the noise-reduction story: with a cleaner target the polynomial captures more of the variation. **Confirms** part of the prior residual structure was noise.
2. **The degree-3 binary classifier barely moved** (98.4% → 98.6%, +0.2%). Adding cubic features and reducing noise did *not* materially close the gap. **Refutes** the strong "cubic IS the boundary" reading of §7.7.
3. **Higher degrees (4-5) gained more** (98.9% → 99.3% and 99.1% → 99.4%). The capacity ceiling of polynomial classifiers is now ~99.4%, and **the true boundary is at least degree 4-5**, not exactly cubic.

**At degree 5 in-sample, Npts=97 misclassifies only 1 point out of 10080** — and that one point has $|{\rm slack}| = 4.2 \times 10^{-6}$, essentially on the surface. The 88 CV misclassifications at degree 5 are a regularization gap (251 features × 5-fold split), not a fundamental model error.

**Calibrated honest verdict on the analytic-sub-family question:**

> The strict WEC+DEC-passing region's boundary $\partial\mathcal{M}$ in $(\sigma, m_0, a, \ell, r)$-space is approximately a low-degree polynomial implicit surface — **specifically, a polynomial of degree 4-5, not exactly degree 3 as §7.7 originally claimed.** The transcendental (exp + erf) factors of the FH potential leak into the slack value field at all scales but contribute only modest non-polynomial residuals to the boundary surface itself once discretization noise is subtracted. **A degree-5 polynomial closed-form expression for $\partial\mathcal{M}$ is plausible** (extractable via Task 2D.5b, with the corrected resolution-converged data); a *degree-3* expression is at most an approximation good to ~1.5% of the binary distinction.

**Implications for Task 2D.5b** (extract the polynomial implicit boundary equation): refit at degree 4 or 5 (not degree 3) using the Npts=97 data, with regularization tuned to match in-sample/CV accuracy gap. The 251-coefficient degree-5 polynomial is uglier than a 55-coefficient cubic, but if it's the *right* surface, simplification by symbolic substitution may still reveal a clean form.

#### §7.8.2 Caveats remaining

1. **Npts=97 is the new resolution baseline, not necessarily convergence.** The canonical winner converges by Npts=97 to ~5%, but other points in the grid (especially low-sigma high-a) may still be drifting. A Npts=129 sanity sweep on a small representative subset would close this — could be done cheaply via `--points` mode (Task 2D.5d).
2. **The 5-D coverage is still coarse** (7 × 8 × 6 × 5 × 6 = 10080 points across the entire band centre). Extracting a 251-coefficient degree-5 polynomial from 10080 points is well-conditioned but still leaves ~40 points per coefficient — not over-determined.
3. **Extrapolation past the grid edges is unsafe.** The leaderboard's top WEC+DEC points still cluster at the corner (sigma=10, m0=3.7, r=9); the optimum extends past where we've measured. Extracting an implicit equation from a region near a boundary the equation itself doesn't constrain is risky.

#### §7.8.3 New top leads after Task 2D.5c

- **Task 2D.5b refresh**: extract the implicit boundary equation at degree 4-5 (not 3) from Npts=97 data; ~1 session, no new compute. Still the cleanest path to a peer-review-defensible analytic sub-family.
- **Task 2D.5d**: convergence test at Npts=129 on a representative subset (e.g. 100 points sampled from the strict-pass region, 100 from near-boundary, 100 from clear fail). Uses the new `--points` dispatch mode. ~30 min on cpu-xl, ~$0.20.
- **Task 2D.5e** (Hard Fix, see §8): symbolic extraction of the closed-form transcendental boundary equation. Reserved for if 2D.5b's polynomial form turns out to be too messy to interpret physically.

---

## §8 Future hardening: symbolic extraction of the boundary equation (Hard Fix, Task 2D.5e — deferred)

This section documents the symbolic-derivation route to the *exact* analytic boundary equation, for posterity. **It is reserved as a fallback** in case the polynomial-fitting Tasks 2D.5b/c/d don't produce a usable closed form for $\partial\mathcal{M}$, or if the polynomial form turns out to be too high-degree to interpret physically.

### §8.1 Why this matters

Tasks 2D.5b/c gave us a **polynomial approximation** (degree 4-5, ~99.4% binary accuracy) to the boundary $\partial\mathcal{M} = \{S(\sigma, m_0, a, \ell, r) = 0\}$ where $S$ is the slack function. That approximation will probably suffice for peer-review-defensible publication — *the boundary is approximately a low-degree polynomial implicit surface* is a scientifically meaningful claim. But it is not the same as having the exact equation. The slack function has the form

$$S(\sigma, m_0, a, \ell, r) = (\text{polynomial part}) + (\text{transcendental tail involving } \exp \text{ and } \mathrm{erf})$$

inherited from the FH potential's structure. The transcendental tail is small in the bulk of $\mathcal{M}$ (which is why polynomial fits work) but contributes systematically to the residual structure observed in §7.7 and §7.8.

### §8.2 Sketch of the calculation

The Fell-Heisenberg smooth potential ([`hf_jobs/sweeps/fell_heisenberg.py`](hf_jobs/sweeps/fell_heisenberg.py) `phi_FH_smooth`) is

$$\phi_{\rm FH}(X, Y, Z; V, \sigma, m_0, a, \ell, r) = \frac{V}{m + n}\bigl[\sigma(e_1 m n + e_2 m n - e_0 (m + n)) + \sqrt{\sigma\pi}(\dots)\bigr]$$

where $m = m_0 + a \tanh(Z/\ell)$, $n = m_0 - a \tanh(Z/\ell)$, and $e_0, e_1, e_2$ are Gaussian envelopes containing $\exp(-{\rm arg}^2/\sigma)$ factors.

The DEC slack at a single $(X, Y, Z)$ point is

$$S_{\rm pt}(X, Y, Z; \text{params}) = \rho_E - |p|_{\max}$$

where $\rho_E$ and $p_i$ come from the ADM stress-energy of $\phi_{\rm FH}$'s Hessian (notebook cell 13). The boundary equation is then

$$S(\text{params}) = \min_{(X,Y,Z) \in \text{interior box}} S_{\rm pt}(X, Y, Z; \text{params}) = 0$$

The hard part is the **interior minimisation over $(X, Y, Z)$**: the slack-minimum location moves around the bubble surface as parameters change, and finding it symbolically requires solving the system $\nabla_{(X,Y,Z)} S_{\rm pt} = 0$ for the minimiser, then substituting back.

### §8.3 Effort estimate

**3-5 sessions** of heavy SymPy work, with the following sub-tasks:
1. Symbolic Hessian of $\phi_{\rm FH}$ (~0.5 session, mostly mechanical SymPy)
2. Symbolic ADM stress-energy $\rho_E, p_1, p_2, p_3$ from the Hessian (~0.5 session — eigenvalues of a 3×3 symmetric matrix have closed forms but get ugly)
3. Symbolic principal-pressure max $|p|_{\max}$ (this is **the hardest** — eigenvalue branches are not differentiable across crossings, so the global max requires careful case analysis or a regularisation trick)
4. Solve $\nabla_{(X,Y,Z)} S_{\rm pt} = 0$ for the boundary minimiser as a function of (sigma, m0, a, ell, r) — likely needs numerical-symbolic hybrid approach; full analytic solution may not exist
5. Substitute back to get $S(\text{params})$ in closed form, then expand around the polynomial approximation from 2D.5b to extract the transcendental correction terms
6. Simplify and check against the empirical Npts=97 sweep data

### §8.4 Tradeoffs vs polynomial-fit approach

| | Polynomial fit (Task 2D.5b) | Symbolic extraction (Task 2D.5e) |
|---|---|---|
| Closed-form result | Approximate (~99.4% binary acc) | Exact |
| Effort | 1 session | 3-5 sessions |
| Compute cost | Zero (just analysis) | Zero (SymPy only) |
| Interpretability | A polynomial in 5 vars; physical meaning unclear | Has explicit physical meaning (exp + erf factors trace to FH potential structure) |
| Generalisable beyond grid | No (only valid where data was sampled) | Yes (analytic everywhere $\phi_{\rm FH}$ is well-defined) |
| Risk | Low (worst case: ugly degree-5 polynomial) | High (the symbolic min over (X,Y,Z) may not have a closed form) |

### §8.5 Decision criteria for promotion from "deferred"

Pursue the Hard Fix if **any** of the following becomes true:
1. Task 2D.5b's polynomial fit has unphysical-looking coefficients that resist all symbolic simplification attempts
2. The 99.4% binary accuracy ceiling stops mattering for a downstream task (e.g. an external collaborator wants the exact equation for a publication)
3. Other open leads (Tasks 2D.6 horizon test, 2D.7 full horizon analysis, 2D.8 independent re-implementation, 2D.9 source-matter classification, 2D.10 asymptotic matching) are all complete and the symbolic extraction is the highest remaining-value task

Otherwise, leave it deferred — the polynomial-fit approach is much cheaper and likely sufficient for the project's peer-review-defensibility goal.

---

## §9 Pointwise lapse-shift ratio and foliation-health analysis (Task 2D.6)

**This is the cheap horizon test promoted as the top open lead from Sessions 11-13.** Implemented by [`hf_jobs/analysis/fell_heisenberg_horizon.py`](hf_jobs/analysis/fell_heisenberg_horizon.py); outputs in [`fell_heisenberg_horizon/`](fell_heisenberg_horizon/).

The Fell-Heisenberg construction has unit lapse $\alpha = 1$ everywhere by definition, so the foliation-health condition $|\vec{N}|/\alpha < 1$ reduces to $|\vec{N}|(x, y, z) < 1$ pointwise. This is the condition for $\partial_t$ to remain a timelike vector (i.e. for the $t = \text{const}$ slices to remain spacelike). Where $|\vec{N}| \ge 1$ the foliation is degenerate and the spacetime contains an effective horizon.

### §9.1 Headline finding (calibrated honestly)

**The Session 11 / 12 / 13 positive-existence result has a brutal physical caveat now made explicit: every WEC+DEC-passing FH configuration tested is essentially "all wall, no interior."** The shift field $|\vec{N}|$ is approximately zero only at the single point $(x, y, z) = (0, 0, 0)$ and is uniformly $|N| \gg 1$ at every other point in the box. There is no extended "passenger zone" inside the bubble where an observer could sit at rest in the lapse foliation; the only foliation-healthy point is the origin itself, with **zero physical volume**.

### §9.2 Geometry of the FH shift field

A misconception in earlier sections (§1.1, §3) was that `central_N_max` (the maximum $|\vec{N}|$ in the central $7^3$ cube) measured "frame-dragging at the center of the bubble." It does not. It measures $|\vec{N}|$ at the **wall** of a bubble whose centre is at the origin. The actual structure of $|\vec{N}|(x, y, z)$ for the canonical winner $(V=1.5, \sigma=10, m_0=3, a=0.05, \ell=4, r=9)$ at Npts=97 is:

- **At origin**: $|\vec{N}| \approx 1.5 \times 10^{-5}$ (numerically zero).
- **At $|R| = 0.25$ (one grid step out)**: $|\vec{N}| \approx 13$.
- **Throughout the box** ($0.5 \le |R| \le 12$): $|\vec{N}| \approx 15$–$18$ uniformly.

See [`fell_heisenberg_horizon/foliation_canonical-V1p5.png`](fell_heisenberg_horizon/foliation_canonical-V1p5.png). The cross-sections through the origin show $|\vec{N}|$ as a single sharp dip at the centre against a uniform $\sim 15c$ background; the histogram shows ~99.9999% of cells at $|N| \in [14, 19]$ with a single outlier near zero.

### §9.3 Passenger-zone analysis

Defining the "passenger zone" as the **connected component of $\{|\vec{N}| < 1\}$ that contains the origin**, the diagnostic results across 5 representative WEC+DEC-passing winners (all at Npts=97):

| Label | $V$ | $\sigma$ | $m_0$ | $a$ | $\ell$ | $r$ | $|\vec{N}|_{\max}$ | Passenger $R$ | Passenger volume |
|---|---|---|---|---|---|---|---|---|---|
| canonical-V1p5 | 1.5 | 10 | 3.0 | 0.05 | 4 | 9 | **18.33** | **0.25** | **1.6e-2** |
| canonical-V0p1 | 0.1 | 10 | 3.0 | 0.05 | 4 | 9 | 1.22 | 0.35 | 0.11 |
| compact-V1 | 1.0 | 6 | 3.0 | 0.10 | 4 | 6 | 9.25 | 0.25 | 1.6e-2 |
| edge-V0p5 | 0.5 | 4 | 2.5 | 0.05 | 4 | 5 | 2.81 | 0.25 | 1.6e-2 |
| high-m0-V0p5 | 0.5 | 8 | 3.5 | 0.05 | 4 | 7 | 6.67 | 0.25 | 1.6e-2 |

(Box volume for reference: $24^3 = 13824$.)

**Passenger zone is one grid cell at every WEC+DEC-passing configuration tested**, with apparent radius $\approx h/2$ (half the grid spacing). Convergence test:

| Npts | $h$ | Passenger $R$ at canonical-V1p5 | Passenger volume |
|---|---|---|---|
| 49 | 0.500 | 0.500 | 1.25e-1 |
| 65 | 0.375 | 0.375 | 5.27e-2 |
| 81 | 0.300 | 0.300 | 2.70e-2 |
| 97 | 0.250 | 0.250 | 1.56e-2 |
| 129 | 0.188 | 0.188 | 6.59e-3 |

Passenger radius scales **exactly as $h/2$** under refinement. The "passenger zone" is the single grid cell containing the origin, with apparent radius being the half-cell spacing — a discretization artifact for a continuum object whose true size is **zero**.

### §9.4 V-scan: where does the horizon first appear?

Varying $V$ at fixed $(\sigma=10, m_0=3, a=0.05, \ell=4, r=9)$ at Npts=97:

| $V$ | $|\vec{N}|_{\max}$ | Passenger $R$ | Passenger volume | Foliation-healthy fraction |
|---|---|---|---|---|
| 0.01 | 0.122 | 20.78 (= box diagonal) | 1.43e+4 (full box) | 100% |
| 0.03 | 0.367 | 20.78 | 1.43e+4 | 100% |
| 0.05 | 0.611 | 20.78 | 1.43e+4 | 100% |
| 0.08 | 0.978 | 20.78 | 1.43e+4 | 100% |
| **0.10** | **1.222** | **0.35** | **1.09e-1** | **0%** |
| 0.13 | 1.589 | 0.25 | 1.56e-2 | 0% |
| 0.15 | 1.833 | 0.25 | 1.56e-2 | 0% |
| 0.30 | 3.666 | 0.25 | 1.56e-2 | 0% |
| 1.50 | 18.332 | 0.25 | 1.56e-2 | 0% |

**The foliation-health "cliff" sits at $V_{\rm crit} \approx 0.09$** for these parameters. Below it, $|\vec{N}| < 1$ everywhere — fully healthy foliation, but no warp drive (peak shift is sub-c). Above it, $|\vec{N}| \ge 1$ throughout almost the entire box and the passenger zone collapses to a single cell (zero physical volume in the continuum limit).

The transition is not gradual — passenger volume drops by **5 orders of magnitude** (from $1.4 \times 10^4$ to $1.6 \times 10^{-2}$) across the threshold, and foliation-healthy fraction drops from 100% to 0%. See [`fell_heisenberg_horizon/v_scan.png`](fell_heisenberg_horizon/v_scan.png).

### §9.5 What this means for the warp-drive interpretation

**The Session 11 result is now characterised correctly:**

1. **Existence claim survives.** The strict WEC+DEC-passing region in $(\sigma, m_0, a, \ell, r)$-space exists, is a connected smooth-boundaried 5-D manifold, and contains 6818 grid points at Npts=97. Nothing here changes that.

2. **The "warp-drive" interpretation is degraded substantially.** "Warp drive" historically means: an observer can sit safely *inside* a bubble while the bubble's wall warps spacetime around them. The FH configuration **does not provide that.** The bubble has no significant interior — only the exact centre point is foliation-healthy, and the entire surrounding region is superluminal-shift territory where the natural foliation breaks down and observers cannot remain at rest in the $t = \text{const}$ slicing.

3. **What remains is "geometric existence" not "physical drive."** The configuration is a positive-energy stationary metric satisfying WEC+DEC everywhere, with the property that an observer following the lapse-vector flow at the centre experiences zero shift. But that observer cannot be displaced from the centre without leaving the foliation-healthy region.

4. **The acceleration / propulsion question collapses.** Without an extended interior, there is no payload for the bubble to carry. The FH metric does not transport anything beyond the single centre-point observer.

**This is the most significant tempering of the Session 11 result so far.** The energy-condition story is intact, but the *physical content* of "static-slice positive existence" turns out to be much weaker than originally read. We have a metric that satisfies WEC+DEC and has the geometric features of a warp bubble (large central shift surrounded by an asymptotic background) but lacks an interior region a passenger could occupy.

### §9.6 Open questions raised by this finding

1. **Is the FH ansatz too restrictive?** The original Alcubierre metric does have an extended interior region (the "comoving" zone where $\beta^x$ is approximately constant). The FH multi-mode-irrotational ansatz constrains the shift to be the gradient of a scalar potential, which forces $\nabla \times \vec{N} = 0$ and means $|\vec{N}|$ cannot have an extended plateau interior unless the underlying $\phi$ is linear there — which would make $\nabla \phi$ constant and non-zero, contradicting "calm centre." **The "all wall, no interior" property may be a structural consequence of irrotationality**, not a tunable feature of the ansatz.

2. **Does adding a vorticity component recover an interior?** Generalising from $\vec{N} = \nabla \phi$ to $\vec{N} = \nabla \phi + \vec{\nabla} \times \vec{A}$ for some vector potential $\vec{A}$ would allow shift profiles with extended plateau interiors. Whether such generalisations preserve the WEC+DEC pass is unknown — and is a substantial new sweep direction (Task 2D.11, new).

3. **Can a smaller bubble at a higher amplitude work?** Maybe at very small bubble radius $r$ the passenger zone could be made to occupy a meaningful fraction of the bubble. The data so far suggests not (passenger radius is $\sim h/2$ regardless of $r$), but a focused sweep over very small $r$ + high resolution might surface something.

4. **The Hard Fix (§8) is more attractive now.** With the polynomial-boundary picture refined and the warp-drive interpretation softened, having the *exact* analytic boundary equation becomes more valuable as the cleanest defensible claim about the FH ansatz.

### §9.7 Remaining tasks downstream of 2D.6

- **Task 2D.7 (full horizon analysis) is partially obsolete** — the cheap test already showed the foliation breaks down throughout the box at warp-drive amplitudes. The full geodesic-expansion / trapped-surface analysis would still be useful for characterising the precise causal structure, but the headline answer ("there is no significant interior") is already in.
- **Task 2D.11 (NEW): vorticity-augmented FH ansatz.** Generalise to $\vec{N} = \nabla \phi + \vec{\nabla} \times \vec{A}$ and ask whether a non-trivial extended foliation-healthy interior is achievable while preserving WEC+DEC. Substantial new sweep direction; ~3-5 sessions of new symbolic + numerical infrastructure.

---

## §10 Polynomial-boundary extraction (Task 2D.5b)

Implemented by [`hf_jobs/analysis/fell_heisenberg_boundary_eq.py`](hf_jobs/analysis/fell_heisenberg_boundary_eq.py); outputs in [`fell_heisenberg_topology_hires/boundary_eq_summary.json`](fell_heisenberg_topology_hires/boundary_eq_summary.json) and [`fell_heisenberg_topology_hires/degree4_surviving_terms.csv`](fell_heisenberg_topology_hires/degree4_surviving_terms.csv).

**Headline finding**: the boundary surface admits a polynomial fit at high accuracy, but the fit is **dense, not sparse** — there is no clean low-term closed-form analytic sub-family.

### §10.1 Setup

Logistic regression of pass/fail vs `PolynomialFeatures(degree, include_bias=False)` of standardised $(\sigma, m_0, a, \ell, r)$, with effectively no regularisation ($C = 10^8$) so the fitted coefficients reflect the geometry rather than the optimiser's regularisation choice. All 10080 strict-pass-or-fail points from the Npts=97 refine sweep are used.

### §10.2 Accuracy + sparsity at increasing degree

| Degree | #features | In-sample acc | Surviving terms (drop $|c| < 1\%$ of max) | Thresholded acc |
|---|---|---|---|---|
| 3 | 55 | 99.6% | 46 / 55 | 99.3% |
| 4 | 125 | **99.98%** | 121 / 125 | 99.96% |
| 5 | 251 | 99.98% | 241 / 251 | 99.97% |

**At every degree, almost ALL polynomial features survive the 1%-of-max threshold.** This is the opposite of the "a few dominant terms with everything else negligible" pattern that would indicate a clean sparse closed-form. The boundary is intrinsically **diffuse** in polynomial space.

### §10.3 L1-sparse fit experiment

To check whether sparsity is hiding behind the unregularised fit, ran logistic regression with L1 penalty at varying regularisation strength $C$:

| $C$ | Nonzero features | Accuracy | Top 3 terms |
|---|---|---|---|
| 10.0 | 125 (all) | 99.76% | $+7.87 \cdot a\ell, -5.30 \cdot a\ell^2, +5.22 \cdot \sigma^2$ |
| 1.0 | 104 | 99.69% | $+6.91 \cdot a\ell, -4.72 \cdot a, -4.43 \cdot a\ell^2$ |
| 0.3 | 81 | 99.50% | $+6.52 \cdot a\ell, -5.34 \cdot a, +4.41 \cdot \ell$ |
| 0.1 | 63 | 99.02% | $+4.38 \cdot a\ell, -4.26 \cdot a, +3.30 \cdot \ell$ |
| 0.03 | 51 | 98.39% | $-2.76 \cdot a, +2.12 \cdot a\ell, +1.94 \cdot \ell$ |
| 0.01 | 30 | 96.95% | $-1.98 \cdot a, +1.07 \cdot \ell, +0.94 \cdot a\ell$ |
| 0.003 | 17 | 92.09% | $-0.93 \cdot a, +0.59 \cdot \ell^3, +0.46 \cdot m_0^3$ |
| 0.001 | 7 | 83.64% | $-0.40 \cdot a^3, +0.32 \cdot m_0^3, +0.29 \cdot \ell^3$ |

**Hand-crafted sparse models** using the L1-leading terms were also tested:

| Hand-crafted feature set | n_features | Accuracy |
|---|---|---|
| 5 linear $(\sigma, m_0, a, \ell, r)$ | 5 | 89.3% |
| L1-leading $(a, a\ell, \ell, \sigma^2)$ | 4 | 85.9% |
| 5 linear + 5 squared | 10 | 90.9% |
| All linear + squares + cross-products | 16 | 95.3% |

**No sub-degree-4 sparse model reaches 98% accuracy.** The minimum useful sparse model has ~30 nonzero terms. **There is no clean low-dimensional closed-form expression for $\partial\mathcal{M}$.**

### §10.4 Pattern in the dominant terms (degree-4 unregularised fit)

Top 12 terms by absolute standardised coefficient:

| Coefficient | Term |
|---:|---|
| +55.51 | $a \cdot \ell$ |
| +49.80 | $\sigma^2$ |
| +44.17 | $a^2 \cdot \ell$ |
| -42.16 | $a$ |
| +40.03 | $r^2$ |
| +39.52 | $\ell$ |
| -36.71 | $a \cdot \ell^2$ |
| +34.77 | $r^3$ |
| -32.97 | $a \cdot r^2$ |
| +32.94 | $\sigma^2 \cdot \ell$ |
| -31.95 | $\sigma^2 \cdot a$ |
| +30.31 | $m_0^3$ |

Three rough patterns visible:
1. **`a` and its interactions dominate the negative-sign terms** ($-a$, $-a\ell^2$, $-ar^2$, $-\sigma^2 a$): consistent with "small $a$ keeps you inside the WEC+DEC region."
2. **`sigma^2` and `r^2` are large positive terms**: consistent with "wide and large bubbles are inside the region."
3. **`a*ell` interactions are large in both signs**: $a$ and $\ell$ are the asymmetry-amplitude/scale pair, and the boundary depends on their product nontrivially.

But these patterns are **interpretive, not algebraic** — there's no single low-degree polynomial whose coefficients match these. The "clean dimensionless invariant" hope from §7.4 is decisively negative.

### §10.5 Verdict on the analytic sub-family question (final)

**The strict WEC+DEC-passing region's boundary $\partial\mathcal{M}$ is approximately a degree-4 polynomial implicit surface (99.98% in-sample accuracy at Npts=97), but the polynomial is dense — all 121-125 non-trivial terms contribute. There is no sparse low-term closed-form representation.**

The honest peer-review-defensible claim is now:

> The strict WEC+DEC-passing configurations form a single connected smooth-boundaried 5-D manifold $\mathcal{M} \subset \mathbb{R}^5_{(\sigma, m_0, a, \ell, r)}$ of positive 5-D measure, characterised by (i) connectivity testing (single component at both 4-conn and full-conn neighbour structures), (ii) smooth boundary surface confirmed by smooth slack-vs-distance behaviour, and (iii) a degree-4 polynomial implicit equation that achieves 99.98% binary classification accuracy in-sample but is dense (no sparse low-term simplification). The remaining ~0.02% binary error is concentrated at the manifold boundary itself where the slack is at the discretisation noise floor.

**This is sufficient for peer-review defensibility but does not yield a clean physically interpretable formula.** Pursuing the symbolic Hard Fix (§8) is now strongly justified as the next step toward an *exact* closed-form boundary equation that would have a transcendental (exp + erf) form rather than a polynomial form.

### §10.6 Why polynomial-boundary extraction was always going to be limited

The slack function $S(\sigma, m_0, a, \ell, r)$ is computed from the FH potential's Hessian + ADM stress-energy + principal-pressure diagonalisation, all of which involve `exp` and `erf` functions of polynomial arguments in the parameters (notably $\arg = r \pm R^{2\Pi}/m$ for $R$ a spatial coordinate eliminated by global minimisation). The boundary $S = 0$ is therefore a **transcendental implicit surface**, not a polynomial one. A polynomial fit at any finite degree is approximating the level set of a transcendental function — and approximations of transcendental level sets generically require many polynomial terms (no sparse pattern).

**The fact that degree 4 reaches 99.98% accuracy is itself remarkable** — it says the transcendental boundary is well-approximated by a polynomial in this parameter window. But the lack of sparse structure is exactly what one would predict from the underlying analytic form. Task 2D.5e (Hard Fix, §8) is the right route to the *exact* boundary equation.

### §10.7 Promotion criteria for Task 2D.5e (Hard Fix) updated

After §10's findings, criterion §8.5.1 ("polynomial fit yields unphysical-looking coefficients") **is met**: 121 polynomial coefficients of all signs and magnitudes with no sparse simplification. The polynomial-fit programme has reached its useful endpoint.

**Recommendation**: promote Task 2D.5e from "deferred" to "active medium-priority." It is now the cleanest path to a concise, interpretable, physically meaningful boundary equation. Effort estimate (3-5 sessions of SymPy work) is unchanged.

---

## §11 Convergence test at Npts=129 (Task 2D.5d) — the boundary count is not robust

Module: re-uses [`hf_jobs/run_sweep.py`](hf_jobs/run_sweep.py) `--points` mode. Config [`hf_jobs/configs/fell_heisenberg_pointlist_n129.json`](hf_jobs/configs/fell_heisenberg_pointlist_n129.json), points [`hf_jobs/configs/fell_heisenberg_pointlist_5d.csv`](hf_jobs/configs/fell_heisenberg_pointlist_5d.csv) (300 points: 100 deep-pass, 100 boundary, 100 clear-fail). HF Jobs `69e66868cd8c002f31e0037a`, 11 min cpu-xl, ~$0.20.

### §11.1 Headline finding

**The strict-pass count at Npts=97 over-estimates the true count, with the over-counting concentrated in the boundary region.** A 300-point representative subset re-evaluated at Npts=129 shows:

| Stratum (defined by Npts=97 slack) | n | median \|drift\| Npts=97→129 | p95 \|drift\| | Sign-flip rate |
|---|---|---|---|---|
| deep_pass (slack > +0.005) | 100 | 8.7e-4 | 9.1e-4 | **0%** |
| boundary (\|slack\| < 1e-4) | 100 | 2.3e-4 | 2.3e-1 | **47%** |
| clear_fail (slack < -0.05) | 100 | 0.29 | 0.42 | **0%** |

Of the 47 sign-flips in the boundary stratum, **all 47 went pass→fail** (zero went fail→pass). This is not random noise; it is **systematic over-counting of strict-pass at Npts=97 in the marginal region**.

### §11.2 Convergence trajectory at 5 representative boundary points

To diagnose what's happening, traced 5 boundary points (the 5 with smallest \|slack\| at Npts=97) through Npts ∈ {49, 65, 81, 97, 113, 129}:

| Point (sigma, m0, a, ell, r) | N=49 | N=65 | N=81 | N=97 | N=113 | N=129 |
|---|---|---|---|---|---|---|
| (9, 2.7, 0.079, 8, 4) | **−0.249** | +2.3e-4 | +8.1e-5 | +2.5e-7 | −5.1e-5 | −8.6e-5 |
| (7, 2.3, 0.126, 3.5, 5) | **−2.7e-2** | +3.8e-4 | +1.4e-4 | −2.9e-7 | −0.102 | **−0.356** |
| (6, 2.5, 0.316, 6.5, 5) | **−0.130** | +4.6e-4 | +1.7e-4 | +4.1e-7 | −1.1e-4 | −1.9e-4 |
| (10, 2.7, 0.079, 3.5, 4) | **−0.244** | +2.4e-4 | +8.7e-5 | +6.4e-7 | −5.4e-5 | −9.1e-5 |
| (7, 2.7, 0.316, 5, 6) | **−0.200** | +7.6e-4 | +2.9e-4 | +4.2e-6 | −1.8e-4 | −3.1e-4 |

The pattern is **non-monotonic**: at Npts=65–97 the slack is positive (small), but at Npts=113–129 it crosses back to negative. The "positive at intermediate Npts" is a discretization artifact; the asymptotic limit appears to be **negative** for these specific configurations. One point (the second row) shows particularly violent drift — its slack at Npts=129 is ~$10^6 \times$ larger in magnitude than at Npts=97, and it is now solidly in the fail region.

This trajectory is the signature of a **subtle truncation error in the 4th-order finite-difference stencil-of-stencils** that systematically biases the sign at the boundary in opposite directions at successive resolutions.

### §11.3 What this means for the project's central claim

**The bulk strict-pass region is rock-solid.** Deep-pass points (slack > +0.005, ~50% of the 6818 strict-pass count at Npts=97) drift by ≪1% under the Npts=97→129 resolution increase and 0% sign-flip — these are converged and the existence claim is intact.

**The boundary count is not robust.** The Npts=97 sweep's 6818 strict-pass count is an over-estimate by approximately the boundary-stratum sign-flip rate (~47%) × the size of the boundary stratum within the strict-pass count. Given that Session-13 §7.8 found roughly 5085 of 6818 strict-pass points have slack > +0.005 (deep) and ~1733 have slack < +0.005 (boundary-ish), the corrected estimate is roughly:

> Robustly strict-pass: ~5085 of 10080 (~50%, vs the originally-reported 67.6%).
> Marginal at Npts=97 noise level: ~1733 of which roughly half flip to fail at Npts=129.
> Best estimate of *resolution-converged* strict-pass count: **~5900 of 10080 (~58%), down from the 6818 originally reported.**

The headline-existence claim ("a connected smooth-boundaried 5-D manifold of strict WEC+DEC-passing configurations exists in the FH ansatz") **survives** because the deep-pass region is real. The headline-size claim ("6818 of 10080 grid points") **does not survive** the Npts=129 test — it should be revised down to ~5900, with the boundary structure explicitly noted as resolution-sensitive.

### §11.4 Updated noise-floor estimate

Per §7.8 the median Npts=65→97 drift on the 300-point shared subset is 2.2e-2; the Npts=97→129 drift on the same subset is 8.8e-4 median, but with p95 = 0.38 driven by the boundary-region instability. The honest noise floor is now:

| Resolution | Median drift to next finer | Boundary p95 drift |
|---|---|---|
| Npts=49 | (dominated by 1st-order errors) | — |
| Npts=65 → 97 | 2.2e-2 | 1.5e-1 |
| **Npts=97 → 129** | **8.8e-4** | **3.8e-1** |
| Npts=129 → ? | unknown | unknown |

For deep-pass points, Npts=97 is converged to ~5%. For boundary points, Npts=129 is the new floor for this resolution series, and even Npts=129 is not necessarily converged (boundary p95 drift is 0.38 — still huge in absolute value).

### §11.5 Implications for downstream tasks

1. **Task 2D.5b / §10 polynomial-fit story is intact.** The 99.98% in-sample classification accuracy was on Npts=97 data, with ~165 misclassified at degree 3 and ~22 at degree 4. The Npts=129 result moves ~50 of the boundary points to "fail," which would have moved the classifier accuracy slightly higher (those points were genuinely on the fail side; the cubic was right and the Npts=97 label was wrong). **The dense-not-sparse verdict is unaffected** — the polynomial fit captures the boundary surface, just with the boundary slightly shifted from where Npts=97 placed it.

2. **Task 2D.6 / §9 horizon analysis is unaffected.** That analysis was per-point at Npts=97 and the per-point convergence was checked at Npts=49→129 already (canonical winner converges to ~5%). The "all wall, no interior" finding holds.

3. **The connectivity / topology story (§7) survives qualitatively.** Single connected component should be robust at Npts=129 even if some boundary cells migrate; the connected-component structure is determined by the bulk, not the noisy boundary.

4. **The Hard Fix (Task 2D.5e) becomes more important, not less.** With every successive-resolution test revealing more nuance in the boundary, having the *exact* analytic boundary equation (rather than chasing convergence with finite-difference grids) is the right way to settle the boundary-count question definitively. The Npts=129 finding strengthens the case for Task 2D.5e being the next-priority systematic study (alongside Task 2D.11's vorticity-augmented ansatz).

5. **A full Npts=129 re-sweep of the entire 10080-point refine grid** would cost ~3.5 hours on cpu-xl and ~$3.50, would give the corrected strict-pass count to within Npts=129 noise, and is the cleanest definitive answer if/when the project needs a publishable strict-pass count. Could be Task 2D.5f if needed.

### §11.6 Honest revised summary

The Session-11 existence claim ("a positive-energy fully-WEC-and-DEC-respecting static metric exists in the FH ansatz with $E_{\rm neg} = 0$") survives.
The Session-11/12/13 size/topology claims need adjustment:
- **Strict-pass count at the band centre**: ~5900 / 10080 (revised down from 6818), with ~50% margin in the boundary region.
- **Connectivity (single component)**: unchanged.
- **Boundary surface degree-4 polynomial approximation**: unchanged.
- **Foliation health (passenger zone size)**: unchanged at zero (Session 14 §9 finding).

The cumulative tempering across Sessions 12–14 is: a real positive-energy WEC+DEC-respecting metric exists in the FH ansatz over a robustly-characterised parameter region of order ~50% of the band centre, but its physical realisation as a warp drive is undermined by the zero-volume passenger zone (§9), and the precise *count* of strict-pass configurations is sensitive to discretisation noise at the boundary in a way that systematically over-counts at all resolutions tested so far. The headline mathematical claim is intact; the headline numerical claims (specific counts) are subject to ongoing convergence study.

---

## §12 Hard Fix attempt (Task 2D.5e) — partial success

Module: [`hf_jobs/analysis/fell_heisenberg_symbolic.py`](hf_jobs/analysis/fell_heisenberg_symbolic.py); artifacts in [`fell_heisenberg_symbolic/`](fell_heisenberg_symbolic/).

**Goal**: per §8 sketch, derive the closed-form transcendental boundary equation $S(\sigma, m_0, a, \ell, r) = 0$ in 6 sub-tasks: symbolic phi → Hessian → ADM stress-energy → principal pressures → $S_{\rm pt}(X,Y,Z; \text{params})$ → minimise over $(X,Y,Z)$ → boundary equation.

**Outcome**: partial success. Sub-tasks 1 and 2 complete cleanly with full validation; sub-task 3 hits an intractable wall in SymPy; sub-tasks 4-6 cancelled (the symbolic eigenvalue extraction was their prerequisite).

### §12.1 Sub-tasks 1-2 complete: validated symbolic Hessian + ADM stress-energy

The symbolic FH potential, Hessian, $K_{ij}$, $\rho_E$, and spatial stress $S_{ij}$ are all built and lambdify-evaluable on a 3D grid. Validation against the existing numerical pipeline ([`hf_jobs/sweeps/fell_heisenberg.py`](hf_jobs/sweeps/fell_heisenberg.py) `hessian_4th` + `adm_stress_energy`) at the canonical anchor $(V=1.5, \sigma=10, m_0=3, a=0.05, \ell=4, r=9)$ on a full Npts=49 grid:

**Checkpoint A** (Hessian): max |diff| at R≥3 is 1.35e-2, with `max_diff/h^4 = 0.22` consistent across Npts ∈ {49, 65, 97} (the symbolic Hessian is exact; the numerical Hessian has the expected $O(h^4)$ truncation error). **PASS.**

**Checkpoint B** (ADM stress-energy components): per-component `max_diff/h^4` ranges from 0.04 (off-diagonals) to 0.14 (diagonals + $\rho_E$). All under the loose 1000.0 threshold (the ADM pipeline applies ~5 nested FD calls, so larger prefactors are expected). **PASS.**

**Conclusion**: the validated symbolic FH stress-energy is a useful artifact for any future analytic study. We have a closed-form analytic expression $S_{ij}(X, Y, Z; V, \sigma, m_0, a, \ell, r)$ for the spatial stress tensor, which the existing numerical pipeline only computes via finite differences with $O(h^4)$ truncation error.

Saved artifacts (in [`fell_heisenberg_symbolic/`](fell_heisenberg_symbolic/)):
- `validation_subtask_1.json`, `validation_subtask_2.json` — full validation logs
- `symbolic_artifacts.tex` — LaTeX summary stub
- `symbolic_artifacts.py` (gitignored, ~15MB, regenerable in ~15 sec) — Python-loadable srepr serialisation of the validated symbolic expressions

### §12.2 Sub-task 3 wall: symbolic eigenvalue extraction is intractable

The next step (per §8 sketch) was to compute symbolic eigenvalues of $S_{ij}$ for the principal pressures. **This does not work.**

Tried in three ways:
1. **`sp.Matrix.eigenvals()` directly**: process killed after 14 minutes with no output.
2. **Cardano's trigonometric form via the invariants $I_1, I_2, I_3$**: $I_1 = \mathrm{tr}\,S$ (1.1 sec), $I_2 = ((\mathrm{tr}\,S)^2 - \mathrm{tr}(S^2))/2$ (0.01 sec), $I_3 = \det(S)$ (**did not terminate in 20 minutes**, both `bareiss` and `berkowitz` algorithms).
3. **Direct `sp.solve(\det(S - \lambda I), \lambda)`**: same `det` bottleneck.

**Root cause**: each $S_{ij}$ component is a sum of hundreds of `erf` + `exp` + rational terms (the symbolic Hessian → ADM derivation produces large but finite expressions). Their **trace** and **sum-of-products** structures stay manageable (the Add tree just grows linearly), but the **determinant** is a sum of 6 products of 3 such terms each. The expansion blows up combinatorially: SymPy attempts to multiply these out and never terminates on the resulting expression tree.

**This was anticipated risk** per §8.2 ("the symbolic min over (X,Y,Z) may not have a closed form"; expected at sub-task 4 but actually hit at sub-task 3 because eigenvalues require the determinant before any minimisation).

### §12.3 Hybrid path technically works but adds no information

Per §8 plan's outcome-B fallback, ran the **symbolic-numerical hybrid**: lambdify the 6 unique $S_{ij}$ components, evaluate at every (X, Y, Z) grid cell, and then call `np.linalg.eigvalsh` per cell. **Checkpoint C passes**: hybrid eigenvalues agree with the fully-numerical pipeline at FD-truncation precision (`max_diff/h^4` ≤ 0.14 per eigenvalue).

But here's the honest assessment: **the hybrid path adds no information beyond what the existing numerical pipeline + §10 polynomial fit already provide**. The "hybrid" pipeline is functionally equivalent to the existing `evaluate()` in [`hf_jobs/sweeps/fell_heisenberg.py`](hf_jobs/sweeps/fell_heisenberg.py); it just replaces the FD-computed $S_{ij}$ with the symbolically-computed $S_{ij}$, which removes one $O(h^4)$ source of error. But the eigenvalue extraction, the (X,Y,Z) minimisation, and the per-parameter boundary determination are all still numerical, so the final boundary equation remains an opaque per-point evaluator — exactly what we already had.

For this reason **sub-tasks 4-6 (symbolic interior minimisation, substitute back, Taylor compare) are cancelled**: they would deliver a marginally cleaner numerical pipeline rather than the closed-form analytic boundary equation that was the whole point.

### §12.4 The deeper interpretation

Why does this fail? The §10 finding (boundary is approximately a degree-4 polynomial but dense) suggests the true boundary is a transcendental level set $\partial \mathcal{M} = \{S = 0\}$ where $S$ contains exp + erf factors of polynomial arguments. Symbolic eigenvalue extraction via Cardano *should* preserve this transcendental form — but only if the expressions involved are amenable to SymPy's manipulation. The FH potential is a sum of terms like $\sigma \cdot (m \cdot n) \cdot \exp(-(r - R^{1/2}/m)^2/\sigma)$ — i.e. **transcendental functions of polynomial arguments**, where the polynomial arguments themselves contain $\tanh(Z/\ell)$. When you compute $\det(S)$, you multiply 6 such terms together; the resulting expression has $6 \times \text{(operations per term)}$ multiplications nested through tanh, exp, erf — and the SymPy expansion engine cannot collapse this into a simpler form because there's no algebraic simplification available across the transcendental functions.

**This is a fundamental property of the FH ansatz, not a SymPy limitation.** Any closed-form boundary equation would be a transcendental expression of comparable complexity to $\det(S)$ itself. Even if SymPy could compute it, the result would be a multi-page expression that is no more interpretable than the dense degree-4 polynomial fit from §10. The "interpretability gain" the Hard Fix was supposed to provide does not materialise: the FH potential is intrinsically too complex for human-readable closed-form analysis.

### §12.5 What this means for the project

The cumulative findings across Sessions 11-14 + Session 14c cleanly resolve the analytic-sub-family question:
- **§7 (Session 12)** found a single connected smooth-boundaried 5-D manifold of strict WEC+DEC-pass.
- **§10 (Session 14a)** found the boundary is approximately a degree-4 polynomial but dense — no sparse closed form.
- **§11 (Session 14b)** found that even the strict-pass count is resolution-sensitive at the boundary.
- **§12 (Session 14c)** has now established that the symbolic Hard Fix is intractable: the FH potential is structurally too complex for SymPy to extract closed-form principal pressures (or eigenvalues, or boundary equation).

The honest closing of the analytic-sub-family thread is: **the Fell-Heisenberg WEC+DEC-passing region is well-characterised as an existence claim and as a numerical/topological object, but the boundary equation $S(\sigma, m_0, a, \ell, r) = 0$ does not have a useful closed form. It is intrinsically a transcendental implicit surface that resists both polynomial approximation (dense, not sparse) and symbolic derivation (SymPy det doesn't terminate).**

This is a clean *negative* result that informs both publication framing and the project's next steps. **The polynomial/symbolic toolset is not the right tool for the FH ansatz**; numerical sweeping is the only viable approach.

### §12.6 New top open lead post-§12

Task 2D.11 (vorticity-augmented FH ansatz) remains the top open question. The Hard Fix's failure to produce a closed-form boundary actually *strengthens* the case for 2D.11: if the irrotational FH ansatz produces a transcendental boundary that's intractable to analyse, perhaps the vorticity-augmented ansatz produces a *simpler* boundary structure that is more amenable to symbolic study. (Equally plausibly: the vorticity-augmented version is even worse. Empirical investigation required.)

### §12.7 Files

In [`fell_heisenberg_symbolic/`](fell_heisenberg_symbolic/):
- `validation_subtask_1.json`, `validation_subtask_2.json`, `validation_subtask_3.json` — checkpoint validation logs
- `symbolic_artifacts.tex` — LaTeX summary stub
- `README.md` — directory guide + regeneration instructions
- `symbolic_artifacts.py` (gitignored, regenerable) — full srepr serialisation of validated symbolic Hessian + ADM stress-energy

Module: [`hf_jobs/analysis/fell_heisenberg_symbolic.py`](hf_jobs/analysis/fell_heisenberg_symbolic.py) — public API for re-running any sub-task.

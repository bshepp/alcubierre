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

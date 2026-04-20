# Navigator — Where Everything Is

**Last updated:** 2026-04-20 (Session 14 — Tasks 2D.6 lapse-shift horizon test (§9) and 2D.5b polynomial boundary extraction (§10) complete. **The Session 11 result is significantly tempered**: every WEC+DEC-passing FH configuration is "all wall, no interior" — the passenger zone shrinks to a single grid cell with zero physical volume in the continuum limit. The boundary surface is approximately degree-4 polynomial but dense (no sparse closed-form). See [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) §9 and §10.).

This is the **front-door map** for the Alcubierre boundary-mode reformulation project. If you're returning to the project after a break, start here. If you want the long-form story, see [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md). For sequential history, see [`SESSION_LOG.md`](SESSION_LOG.md).

---

## What this project is

A personal landscape exploration of the Alcubierre warp drive in general relativity, asking whether the standard "exotic-matter requirement" can be reformulated as a *boundary effect* rather than a substance to be manufactured. **Project mode is "surfing", not "paper-writing"** — there are no concrete deliverables; the goal is to understand the structure of the obstructions to a working classical warp drive.

After 9 sessions, the project has produced (i) a *static-slice* classical no-go for useful warp drives, (ii) a six-slice exploration of which assumptions in the no-go are load-bearing, and (iii) a documented set of published candidate constructions outside the slice that face interpretation-dependent caveats.

---

## Where to start

| If you want… | Go here |
|---|---|
| **The headline result in one paragraph** | This document, §"Headline" below |
| **The honest narrative across all sessions** | [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md) |
| **Which assumptions hold up the no-go** | This document, §"Load-bearing assumptions table" below |
| **Sequential session-by-session history** | [`SESSION_LOG.md`](SESSION_LOG.md) |
| **A specific result** (e.g. "what's the minimum shell thickness?") | The relevant notebook in §"Notebook index" below |
| **What we trust vs. what we accepted on the literature's authority** | [`TRUST_AUDIT.md`](TRUST_AUDIT.md) |
| **Project plan and outstanding tasks** | [`ROADMAP.md`](ROADMAP.md) |
| **Literature catalog with abstracts and our take on each paper** | [`LITERATURE.md`](LITERATURE.md) |
| **To extend a slice** | The slice's notebook + its `_NOTES.md` companion |
| **Critical evaluations of specific external papers** | The `*_EVALUATION.md` files (Rodal 2025, Krasnikov 2003, Fell-Heisenberg 2021 when present) |

---

## Headline

**Within the slice of parameter space** defined by:
- Alcubierre $\beta^x \hat x$ shift (or other single-mode axisymmetric shifts);
- Spherical Fuchs-class matter shell or static cylindrical Krasnikov tube;
- Asymptotically flat vacuum exterior;
- Steady-state metric or its Lorentz boost;
- 4D Einstein gravity;

…**no useful classical positive-matter warp drive exists** that is simultaneously DEC-compatible, accelerable to warp-relevant velocities, and transport-relevant.

**Outside that slice**, several published candidate constructions exist:
- **Lentz 2020** (plasma-supported, multi-mode soliton — outside Slice 1);
- **Fell & Heisenberg 2021** (multi-mode "hidden geometric structures" in standard GR — outside Slice 1). **Sessions 11-14 in [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md)**: a connected smooth-boundaried 5-D manifold of strict WEC+DEC-passing configurations exists, with $E_{\rm neg} = 0$ (no negative energy density anywhere). The Npts=97 sweep confirmed 6818/10080 points strictly pass; the boundary surface is approximately a degree-4 polynomial implicit surface (99.98% in-sample classifier accuracy). **Critical caveat from Session 14 §9**: every passing configuration is "all wall, no interior" — the connected $|\vec{N}| < 1$ region containing the origin (the would-be passenger zone) is a single grid cell with apparent radius $h/2$ that scales to **zero physical volume in the continuum limit**. The bubble geometry is "calm point at origin surrounded immediately by uniform $\sim 15c$ shift throughout the box." This degrades the warp-drive interpretation substantially: the existence claim holds mathematically, but no observer can occupy an extended interior. The acceleration / source-matter / asymptotic-matching questions are partially moot at this finding — there's nothing to propel. See [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) and [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md);
- **Lobo & Oliveira 2009** (f(R) wormholes — Jordan-frame loophole, interpretation-dependent);
- **Garattini & Zatrimaylov 2025** (de Sitter bubble at Hubble velocity — averaged WEC/NEC only);
- **Rodal 2025** (irrotational Natário-class, 38× peak-deficit reduction in standard GR but still violates NEC/WEC/DEC/SEC).

The honest project summary, post-Session-14: **"the no-go is robust for full WEC within its single-mode-axisymmetric slice; the multi-mode Fell-Heisenberg case admits a positive-energy fully-WEC-and-DEC-respecting static metric at all amplitudes — the energy-condition bottleneck is mathematically solved within this static slice. But the foliation-health analysis (Task 2D.6 / §9) shows the geometry is 'all wall, no interior': a passenger zone of zero continuum volume. So we have a positive-energy stationary solution that satisfies the WEC and DEC pointwise, but does not provide the extended interior region a conventional warp drive needs. The 'energy-condition bottleneck' was an under-determined formulation of the warp-drive problem; the new bottleneck is 'extended foliation-healthy interior region', which the irrotational FH ansatz appears structurally unable to provide. Whether vorticity-augmented ansätze (Task 2D.11) recover an interior is the new top open question."**

---

## Load-bearing assumptions table (canonical post-Phase-2C)

This is the authoritative version. Slice notes documents that have their own tables now defer to this one.

| # | Sub-assumption | Status | Tested where | Notes |
|---|---|---|---|---|
| 1 | Shift profile is single-mode axisymmetric | **Load-bearing AND broken (Sessions 11-12). But the multi-mode case has a hidden new bottleneck (Session 14).** | Slice 1: [`shift_families.ipynb`](shift_families.ipynb), [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md). Multi-mode: [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb), [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md). Sweep + topology + horizon test: [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md). | Single-mode axisymmetric: 0/140 sweep points achieve full WEC. **Multi-mode irrotational (Fell-Heisenberg 2021)**: Session 11 sweep found ~6800 / 10080 strict-pass at Npts=97 with $E_{\rm neg} = 0$. Session 12 connectivity: single connected smooth-boundaried 5-D manifold. **Session 14 §9 horizon test**: every passing configuration has zero-volume passenger zone (single-grid-cell continuum-zero). Energy-condition bottleneck is solved; foliation-extent bottleneck is not. New top open question: do vorticity-augmented ansätze (Task 2D.11) recover an interior? |
| 2 | Krasnikov-tube wall is bare-vacuum (no matter shell) | **Not load-bearing for single-bump matter perturbations** | Slice 2: [`hybrid_wall.ipynb`](hybrid_wall.ipynb) | 0/480 sweep points achieve WEC. Adding matter shifts the WEC-violating region but does not eliminate it. Multi-bump and off-wall configurations not tested. |
| 3 | Steady-state metric + Lorentz boost is sufficient | **Not load-bearing** | Slice 3: [`time_dependent.ipynb`](time_dependent.ipynb), [`TIME_DEPENDENT_NOTES.md`](TIME_DEPENDENT_NOTES.md) | $\dot v$ correction to $\rho_p$ is antisymmetric in axis-of-motion coordinate $x$, scales as $1/\tau$ (linear in $\dot v$), peaks at 0.3% of static value at $\tau = R/c$. Net momentum injection at quadrupole order is zero by symmetry. |
| 4 | Pfenning-Ford-style tight QI bounds on negative energy | **Substantively weakened by Krasnikov 2003** (but our classical no-go is QI-independent) | Slice 4: [`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md) | Krasnikov gives three loopholes (Weyl/Ricci ratio, $E_{\rm tot}^-$ meaningless, dihedral-portal construction with $10^{-3}$ g exotic matter). Our Task 2A.13 classical no-go is independent of QI. |
| 5a | Asymptotic flatness — momentum exchange | **Not load-bearing** | Slice 5: [`cosmological_exterior.ipynb`](cosmological_exterior.ipynb), [`COSMOLOGICAL_EXTERIOR_NOTES.md`](COSMOLOGICAL_EXTERIOR_NOTES.md) | Cosmological-exterior reaction-mass channel: $\Delta v \le 5.7 \times 10^{-36}$ m/s at $R_{\rm BY} = 100\,R_{\rm shell}$, scaling as $R_{\rm BY}^3$. 42+ orders of magnitude below the GW-recoil channel. |
| 5b | Asymptotic flatness — energy-condition obligations | **Modified for special case $v = v_{\rm Hubble}$** in de Sitter | Slice 5 + Garattini-Zatrimaylov 2025 ([`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md) §"Construction 3") | Bubble at Hubble velocity in de Sitter satisfies *averaged* (not local) WEC/NEC. A real qualifier on Slice 5; only applies under the radial-Hubble-velocity matching condition. |
| 6 | 4D Einstein gravity (Jordan-frame interpretation) | **Real loophole; interpretation-dependent** | Slice 6: [`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md) | Lobo & Oliveira 2009 demonstrate $f(R)$ wormholes where matter satisfies WEC and curvature absorbs the violation in Jordan frame. Einstein-frame transformation moves the violation to a scalar field. Whether this counts as "DEC-respecting matter" depends on which frame you take as physical. Phase 6b (computational $f(R)$ analysis) deferred. |

---

## Document index

### Entry-point and synthesis

| File | Role |
|---|---|
| [`README.md`](README.md) | Project overview, current status, key results, document index |
| [`NAVIGATOR.md`](NAVIGATOR.md) | (this file) — compact front-door map, load-bearing-assumptions table, open leads |
| [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md) | Narrative synthesis structured by physics question |
| [`ROADMAP.md`](ROADMAP.md) | Phase structure, completed and open tasks, decision points, risk register |
| [`SESSION_LOG.md`](SESSION_LOG.md) | Chronological record of work sessions and findings |
| [`TRUST_AUDIT.md`](TRUST_AUDIT.md) | What we derived ourselves vs. accepted on the literature's authority |
| [`LITERATURE.md`](LITERATURE.md) | Full literature catalog with abstracts and relevance notes |

### Path 2A (classical matter-shell route)

| File | Role |
|---|---|
| [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md) | Primary path doc — Fuchs et al. 2024 mapping, Israel junctions, scaling laws, acceleration analysis. Includes Appendix A (three-mechanism exhaustiveness proof) |
| [`matter_shell.ipynb`](matter_shell.ipynb) | Initial Path 2A notebook — bump function, Israel-warm-up, EC scaling |
| [`israel_junction.ipynb`](israel_junction.ipynb) | Package 1 (Task 2A.6) — full Israel junction, Part A static + Part B boosted, $\lambda_*$ acceleration obstruction. Includes Cell 4b Schwarzschild $K_{ab}$ regression (TRUST_AUDIT #4) |
| [`thickness_bound.ipynb`](thickness_bound.ipynb) | Package 2 (Task 2A.7) — minimum shell thickness scaling law $\Delta_{\min}/R = \kappa\,\beta/C$ |
| [`acceleration.ipynb`](acceleration.ipynb) | Package 3 (Task 2A.10) — ADM 4-momentum obstruction, three-mechanism catalog, GW-recoil ceiling |
| [`krasnikov_tube.ipynb`](krasnikov_tube.ipynb) | Task 2A.13 — Krasnikov 4D metric with Fuchs-class thick wall; 0/300 WEC pass |
| [`KRASNIKOV_TUBE_NOTES.md`](KRASNIKOV_TUBE_NOTES.md) | Quantitative synthesis of Krasnikov 1995 / Everett-Roman 1997 / Krasnikov 2003 prior art |

### Phase 2C (adjacent-slices exploration)

| File | Slice | Role |
|---|---|---|
| [`shift_families.ipynb`](shift_families.ipynb) + [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md) | 1 | Alternate axisymmetric shift families |
| [`hybrid_wall.ipynb`](hybrid_wall.ipynb) | 2 | Krasnikov + matter-shell hybrid wall |
| [`time_dependent.ipynb`](time_dependent.ipynb) + [`TIME_DEPENDENT_NOTES.md`](TIME_DEPENDENT_NOTES.md) | 3 | Time-dependent $v(t)$ acceleration |
| [`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md) | 4 | Critical evaluation of Krasnikov 2003 QI loopholes |
| [`cosmological_exterior.ipynb`](cosmological_exterior.ipynb) + [`COSMOLOGICAL_EXTERIOR_NOTES.md`](COSMOLOGICAL_EXTERIOR_NOTES.md) | 5 | McVittie + $\Lambda$ exterior |
| [`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md) | 6 | Modified-gravity warp drive literature pull |

### Path 2B and external evaluations

| File | Role |
|---|---|
| [`QUANTUM_CLASSICAL_BRIDGE.md`](QUANTUM_CLASSICAL_BRIDGE.md) | Path 2B (Casimir / boundary-mode) — three-tiered claim structure, outcome matrix, search-target sharpening (anisotropic Casimir) |
| [`RODAL2025_EVALUATION.md`](RODAL2025_EVALUATION.md) | Critical evaluation of Rodal 2025 (irrotational Natário-class warp drive) |
| [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) | Critical evaluation of Fell & Heisenberg 2021. Session 10. **Pipeline regression A-grade**, qualitative claim verified, full-WEC violations smaller than the paper's text suggests. |
| [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb) | Reproduction notebook for Fell & Heisenberg 2021. Session 10. |
| [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) | **Sessions 11-13 sweep + topology**: §1-§6 the strict-WEC+DEC sweep (1404/15000 strict-pass at Npts=65, falsifies FH §3.3 irreducibility claim), §7 the connectivity/topology analysis (single connected smooth-boundaried 5-D manifold; §7.7 polynomial-fit at Npts=65 found degree-3 ~98% accurate boundary; §7.8 Npts=97 resolution-convergence test found the boundary is degree 4-5, not 3, and Npts=65 was systematically biased at low sigma), §8 deferred Hard Fix path (symbolic boundary extraction). |
| [`fell_heisenberg_topology/`](fell_heisenberg_topology/) | Session 12 outputs from Npts=65 refine sweep: 4 figures, summary JSON, boundary CSV. Generated by [`hf_jobs/analysis/fell_heisenberg_topology.py`](hf_jobs/analysis/fell_heisenberg_topology.py). |
| [`fell_heisenberg_topology_hires/`](fell_heisenberg_topology_hires/) | Session 13 outputs from Npts=97 resolution-convergence sweep + Session 14 polynomial-boundary extraction (boundary_eq_summary.json, degree4_surviving_terms.csv, thresholding_effect.png). |
| [`fell_heisenberg_horizon/`](fell_heisenberg_horizon/) | Session 14 Task 2D.6 outputs: 5 foliation-health plots, V-scan, summary JSON, leaderboard CSV. Generated by [`hf_jobs/analysis/fell_heisenberg_horizon.py`](hf_jobs/analysis/fell_heisenberg_horizon.py). |

### Verification / linearization

| File | Role |
|---|---|
| [`verification.ipynb`](verification.ipynb) | Sympy/numpy verification of all symbolic results from `LINEARIZATION_CALCULATION.md` |

### Historical (pre-pivot)

These are preserved as record of the project's earlier hypotheses; their *symbolic* content remains valid where reused, but their *strategic recommendations* have been superseded.

| File | Role |
|---|---|
| [`ALCUBIERRE_IMAGE_METHOD.md`](ALCUBIERRE_IMAGE_METHOD.md) | Phase 0 seed: image-method hypothesis (subsequently abandoned) |
| [`ALCUBIERRE_MARCH30_INTEGRATION.md`](ALCUBIERRE_MARCH30_INTEGRATION.md) | Addendum to seed doc with March 30 literature integration |
| [`LINEARIZATION_CALCULATION.md`](LINEARIZATION_CALCULATION.md) | Phase 1 derivation: linearised Einstein equations, ADM stress-energy, dipole structure, image-method falsification |

### Speculation

| File | Role |
|---|---|
| [`speculation/RING_NETWORK_CONCEPT.md`](speculation/RING_NETWORK_CONCEPT.md) | Third-party "ring network" speculation document, settled by Task 2A.13 |

### Compute infrastructure

| Path | Role |
|---|---|
| [`hf_jobs/run_sweep.py`](hf_jobs/run_sweep.py) | HF Jobs / Colab / local sweep dispatcher |
| `hf_jobs/sweeps/*.py` | Sweep modules (Israel-junction Part A, thickness bound, GW recoil, Krasnikov tube, shift families, hybrid wall, **fell_heisenberg**) |
| `hf_jobs/configs/*.json` | Sweep configurations (per-sweep `_preview` and `_full` configs) |
| [`hf_jobs/jobs/run_fell_heisenberg.sh`](hf_jobs/jobs/run_fell_heisenberg.sh) | HF Jobs entry script for the Fell-Heisenberg sweep (clones repo, installs deps, runs sweep, uploads to dataset) |
| `requirements.txt`, `requirements-gw.txt` | Pinned dependencies for local / Colab / HF Jobs |
| HF Dataset [`bshepp/alcubierre-sweeps`](https://huggingface.co/datasets/bshepp/alcubierre-sweeps) | Private dataset for sweep result parquets |

---

## Open leads (ranked by signal-per-effort, post-Session-14)

**Note:** Sessions 11-14 progress on FH 2021 ([`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md)): the existence of a positive-energy fully-WEC-and-DEC-respecting static metric is established and characterised topologically (single connected 5-D manifold with smooth boundary). However, the §9 horizon test shows **every passing configuration has zero-volume passenger zone** — the bubble is "all wall, no interior." This degrades the warp-drive interpretation substantially and shifts the open-question priorities. The energy-condition bottleneck is solved but the foliation-extent bottleneck is not.

1. **(NEW, top priority post-Session-14.) Vorticity-augmented FH ansatz (Task 2D.11).** The §9 finding that the irrotational FH ansatz produces "all wall, no interior" suggests this is structurally tied to $\nabla \times \vec{N} = 0$. Generalise to $\vec{N} = \nabla \phi + \vec{\nabla} \times \vec{A}$ (mixed irrotational + vortical) and ask whether (i) such configurations can satisfy WEC+DEC at all, (ii) if yes, do they produce extended foliation-healthy interiors. **The new fundamental open question** for the FH-style positive-energy warp-drive programme. Effort: 3-5 sessions of new symbolic + numerical infrastructure (extend the symbolic Einstein pipeline to non-irrotational shifts; sweep the augmented parameter space).

2. **(PROMOTED from deferred, post-Session-14.) Hard Fix: symbolic extraction of the closed-form boundary equation (Task 2D.5e).** Session 14 §10 found the polynomial fit is dense (no sparse low-term simplification) — Task 2D.5e's promotion criterion §8.5.1 is now met. Symbolic Hessian + ADM stress-energy + interior $(X,Y,Z)$ minimisation gives the exact transcendental boundary equation in closed form (containing exp + erf factors from the FH potential). Yields a concise interpretable boundary equation that the polynomial fit cannot. Effort: **3-5 sessions** of heavy SymPy. Promoted to active medium-priority.

3. **(NEW, Session 13.) Convergence test at Npts=129 on a representative subset (Task 2D.5d).** Npts=97 is *better* than Npts=65 but not necessarily resolution-converged. A targeted ~300-point Npts=129 sweep using the new `--points` mode would close the convergence question definitively. Cheap and adds confidence to all subsequent claims. Effort: ~30 min cpu-xl, ~$0.20.

4. **(Session-11-defined, partially obsolete after §9.) Fell-Heisenberg full horizon and CTC analysis (Task 2D.7).** §9 already established the foliation breaks down throughout the box at warp-drive amplitudes. Full geodesic-expansion + trapped-surface analysis would still characterise the precise causal structure, but the headline answer ("no significant interior") is in. Effort: ~1 session if pursued.

5. **(Session-11-defined.) Independent re-implementation of the FH ADM stress-energy pipeline (Task 2D.8).** Replicate the result in a second pipeline (e.g. SymPy + LAPACK in a different stencil, or Mathematica xAct verification) to rule out a systematic finite-difference bug. **The highest-value cheap check before any external claim is made** — and now extra-important given the surprising §9 finding. Effort: 1-2 sessions.

6. **(Session-11-defined.) Identify the FH source matter sector (Task 2D.9).** Given the WEC+DEC-passing $T_{\mu\nu}$, compute the principal-pressure profile $(\rho, p_1, p_2, p_3)$ as a field on the box and place it in the Bobrick-Martire 2021 §III taxonomy. Effort: 1 session.

7. **(Session-11-defined, partially obsolete after §9.) FH asymptotic-matching + double-bubble CTC test (Task 2D.10).** Box-edge matching to Schwarzschild/Minkowski exterior — does it require negative-energy Israel junction? Do two FH bubbles in opposite directions form CTCs? Less urgent now that the inside-the-bubble interpretation has been undermined. Combined effort: 1-2 sessions.

8. **Garattini-Zatrimaylov 2025 reproduction.** They claim a bubble at Hubble velocity in de Sitter satisfies averaged WEC/NEC. Our Slice 5 McVittie pipeline is already set up; adding a bubble on top and computing the averaged conditions is a focused extension. **Effort: 1-2 sessions.**

9. **Path 2B (Casimir / boundary-mode QFT) — start the programme.** Less urgent given Session 11 result (the energy-condition bottleneck doesn't require a quantum supplement after all, in the static slice), but Path 2B remains the right route for the *acceleration* and *dynamic-buildability* questions which Session 11's static result does not address. Now also relevant if Task 2D.11 vorticity-augmentation also fails — the all-wall-no-interior pathology may be a deep structural feature of classical irrotational shifts that needs a quantum supplement. Tasks 2B.1–2B.5 in [`ROADMAP.md`](ROADMAP.md) are the natural starting points. **Effort: large (multiple sessions); largest scope.**

10. **Slice 4b (Krasnikov 2003 hybrid quantum/classical wall).** Reproduce Krasnikov's $10^{-3}$ g dihedral-portal + Van Den Broeck pocket and ask whether adding a Fuchs-class classical shell can eliminate the residual mg of QI-bounded negative energy. Focused, mostly computational. **Effort: 1 session.**

11. **TRUST_AUDIT #3 (Warp Factory + Fuchs Fig. 10 reproduction).** Last deferred audit item. Requires MATLAB on Windows. **Effort: 1 session of MATLAB wrestling.**

12. **Slice 6b (computational $f(R)$).** Build a 4th-order PDE solver. Significant new infrastructure. **Effort: large.**

### Completed in Session 14:

- ~~Task 2D.6 (lapse-shift horizon test)~~ — done; output is "all wall, no interior" verdict; see §9.
- ~~Task 2D.5b (polynomial boundary extraction)~~ — done; output is "boundary IS approximately degree-4 polynomial but dense"; see §10.

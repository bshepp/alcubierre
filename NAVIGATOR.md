# Navigator — Where Everything Is

**Last updated:** 2026-04-19 (Session 11 — Fell-Heisenberg WEC+DEC residual sweep complete; positive existence result; see [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md)).

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
- **Fell & Heisenberg 2021** (multi-mode "hidden geometric structures" in standard GR — outside Slice 1). **Session 11 sweep in [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md)** found **1404 of 15000 grid points** in the FH potential family $(V, \sigma, m_0, a, \ell, r)$ that achieve **strict full WEC AND strict full DEC at every interior cell** with $E_{\rm neg} = 0$ (no negative energy density anywhere) and central superluminal frame-dragging from $0.73c$ to $18.6c$. Resolution-converged at Npts=65 through Npts=113. **Falsifies the FH §3.3 claim** that residual energy-condition violations "cannot be removed by modification." Sub-volume in $(\sigma, m_0, a)$-space; $V$ is a free amplitude (slacks scale as $V^2$). The construction is **static** — the acceleration / horizon / source-matter / asymptotic-matching questions remain open. See [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) and [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md);
- **Lobo & Oliveira 2009** (f(R) wormholes — Jordan-frame loophole, interpretation-dependent);
- **Garattini & Zatrimaylov 2025** (de Sitter bubble at Hubble velocity — averaged WEC/NEC only);
- **Rodal 2025** (irrotational Natário-class, 38× peak-deficit reduction in standard GR but still violates NEC/WEC/DEC/SEC).

The honest project summary, post-Session-11: **"the no-go is robust for full WEC within its single-mode-axisymmetric slice; the multi-mode Fell-Heisenberg case admits a positive-energy fully-WEC-and-DEC-respecting static configuration at all amplitudes — the kinematic bottleneck of the warp-drive problem in standard GR is genuinely solved within this static slice. The remaining barriers are dynamical (acceleration, source matter, asymptotic matching, horizon structure), not energy-conditional."**

---

## Load-bearing assumptions table (canonical post-Phase-2C)

This is the authoritative version. Slice notes documents that have their own tables now defer to this one.

| # | Sub-assumption | Status | Tested where | Notes |
|---|---|---|---|---|
| 1 | Shift profile is single-mode axisymmetric | **Load-bearing AND broken (Session 11 result).** | Slice 1: [`shift_families.ipynb`](shift_families.ipynb), [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md). Multi-mode follow-up: [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb), [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md). Sweep: [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md). | Single-mode axisymmetric: 0/140 sweep points achieve full WEC. **Multi-mode irrotational (Fell-Heisenberg 2021)**: Session 11 sweep over $(V, \sigma, m_0, a, \ell, r)$ found **1404 / 15000 grid points** (9.4%) achieving **strict full WEC AND strict full DEC** at every interior cell, with $E_{\rm neg} = 0$ and central superluminal frame-dragging $|\vec{N}|_{\max}$ from $0.73c$ to $18.6c$. Resolution-converged. The kinematic energy-condition bottleneck of the warp-drive problem is solved within this static slice; remaining barriers are dynamical. |
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
| [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) | **Session 11 sweep result**: 1404/15000 grid points achieve strict full WEC + DEC at every interior cell with $E_{\rm neg} = 0$ and superluminal central frame-dragging. Falsifies FH §3.3 irreducibility claim. |

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

## Open leads (ranked by signal-per-effort, post-Session-11)

**Note:** the Session-10-era #1 lead (Fell-Heisenberg $(V, \sigma, m_0, a, \ell, r)$ residual-WEC search) has been **completed in Session 11** and produced a positive existence result — see [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md). The new top leads are the §5 follow-ups from that result, which test whether the static-slice positive existence assembles into a complete physical drive.

1. **(NEW, top priority — cheap and high signal.) Connectivity and topology of the WEC+DEC-passing region (Task 2D.5).** Re-analyse the existing 1404-pass parquet (and optionally a denser refinement sweep at the band centre) to determine: (i) Is the passing region a single connected manifold in $(\sigma, m_0, a, \ell, r)$-space, or several disconnected islands? (ii) If connected, does the boundary surface have clean structure suggesting a closed-form sub-family hiding in there that can be derived analytically? (iii) Does the region respect any obvious group action on the parameters? **An analytic sub-family is substantially more defensible in peer review than "we swept and found 1404 hits."** Effort: 1 session, no new compute. Zero additional cost.

2. **(NEW, top priority — cheap and high signal.) Pointwise lapse-shift ratio $|\vec{N}|/\alpha$ as cheap horizon test (Task 2D.6).** Before the full horizon analysis, compute $|\vec{N}|/\alpha$ on the 3D grid for a representative WEC+DEC-passing winner. With unit lapse the threshold for the $t = \text{const}$ foliation to remain spacelike is $|\vec{N}| < 1$ pointwise. **If everywhere below 1, no horizon — done; the foliation is healthy and Task 2D.7 reduces to a CTC test only.** **If $\ge 1$ somewhere, that's exactly the locus to investigate.** A single line of NumPy at $\sim$0.1 sec per winner. Effort: <0.1 session.

3. **(NEW, Session 11.) Fell-Heisenberg full horizon and CTC analysis (Task 2D.7).** *Gated by Task 2D.6.* For the canonical WEC+DEC-passing point, compute (i) the norm of $\partial_t$ pointwise (foliation health, sharpened by 2D.6), (ii) outward null geodesic expansion at locations where 2D.6 flagged $|\vec{N}|/\alpha \to 1$, (iii) closed-timelike-curve test via Everett-Roman 1997 §4. The most likely place a "too good to be true" objection lands. Effort: 1-2 sessions if 2D.6 finds problem regions; 0.5 session if not.

4. **(NEW, Session 11.) Independent re-implementation of the FH ADM stress-energy pipeline (Task 2D.8).** Replicate the result in a second pipeline (e.g. SymPy + LAPACK in a different stencil, or Mathematica xAct verification) to rule out a systematic finite-difference bug. **The highest-value cheap check before any external claim is made.** Effort: 1-2 sessions.

5. **(NEW, Session 11.) Identify the FH source matter sector (Task 2D.9).** Given the WEC+DEC-passing $T_{\mu\nu}$, compute the principal-pressure profile $(\rho, p_1, p_2, p_3)$ as a field on the box and place it in the Bobrick-Martire 2021 §III taxonomy. Effort: 1 session.

6. **(NEW, Session 11.) FH asymptotic-matching + double-bubble CTC test (Task 2D.10).** Box-edge matching to Schwarzschild/Minkowski exterior — does it require negative-energy Israel junction? Do two FH bubbles in opposite directions form CTCs? Combined effort: 1-2 sessions.

7. **Garattini-Zatrimaylov 2025 reproduction.** They claim a bubble at Hubble velocity in de Sitter satisfies averaged WEC/NEC. Our Slice 5 McVittie pipeline is already set up; adding a bubble on top and computing the averaged conditions is a focused extension. **Effort: 1-2 sessions.**

8. **Path 2B (Casimir / boundary-mode QFT) — start the programme.** Less urgent given Session 11 result (the energy-condition bottleneck doesn't require a quantum supplement after all, in the static slice), but Path 2B remains the right route for the *acceleration* and *dynamic-buildability* questions which Session 11's static result does not address. Tasks 2B.1–2B.5 in [`ROADMAP.md`](ROADMAP.md) are the natural starting points. **Effort: large (multiple sessions); largest scope.**

9. **Slice 4b (Krasnikov 2003 hybrid quantum/classical wall).** Reproduce Krasnikov's $10^{-3}$ g dihedral-portal + Van Den Broeck pocket and ask whether adding a Fuchs-class classical shell can eliminate the residual mg of QI-bounded negative energy. Focused, mostly computational. **Effort: 1 session.**

10. **TRUST_AUDIT #3 (Warp Factory + Fuchs Fig. 10 reproduction).** Last deferred audit item. Requires MATLAB on Windows. **Effort: 1 session of MATLAB wrestling.**

11. **Slice 6b (computational $f(R)$).** Build a 4th-order PDE solver. Significant new infrastructure. **Effort: large.**

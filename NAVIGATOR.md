# Navigator — Where Everything Is

**Last updated:** 2026-04-17 (Session 10 — Fell-Heisenberg evaluation complete).

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
- **Fell & Heisenberg 2021** (multi-mode "hidden geometric structures" in standard GR — outside Slice 1). **Session 10 reproduction in [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb)** confirms their qualitative claim (positive Eulerian $\rho_E$ in 99.8% of interior cells, superluminal central $|\vec{N}|$). Full WEC and DEC are violated as the authors themselves admit, but at only **1.3% / 5.3% of interior cells** — much smaller and more compact than their text "no amount of modification could get rid of these regions" suggests. **Most interesting open lead**: can residual full-WEC violations be eliminated by careful $(m, n)$ choice? If so, fully WEC-respecting classical warp drive in standard GR. See [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md);
- **Lobo & Oliveira 2009** (f(R) wormholes — Jordan-frame loophole, interpretation-dependent);
- **Garattini & Zatrimaylov 2025** (de Sitter bubble at Hubble velocity — averaged WEC/NEC only);
- **Rodal 2025** (irrotational Natário-class, 38× peak-deficit reduction in standard GR but still violates NEC/WEC/DEC/SEC).

Each candidate has documented caveats. The honest project summary is **"the no-go is robust for full WEC within its single-mode-axisymmetric slice; the multi-mode case (Fell-Heisenberg) achieves Eulerian-WEC and 99% full-WEC, with a residual 1% violation whose minimisability is the project's most interesting open question."**

---

## Load-bearing assumptions table (canonical post-Phase-2C)

This is the authoritative version. Slice notes documents that have their own tables now defer to this one.

| # | Sub-assumption | Status | Tested where | Notes |
|---|---|---|---|---|
| 1 | Shift profile is single-mode axisymmetric | **Load-bearing in a useful way (Session 10 update).** | Slice 1: [`shift_families.ipynb`](shift_families.ipynb), [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md). Multi-mode follow-up: [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb), [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md). | Single-mode axisymmetric: 0/140 sweep points achieve full WEC. **Multi-mode irrotational (Fell-Heisenberg 2021)**: positive Eulerian $\rho_E$ in 99.8% of interior cells; full WEC pass in 98.7%; full DEC pass in 94.7%. **Residual 1.3%-of-cells full-WEC violation is the project's most interesting open lead** (lead #1 in §"Open leads" below). |
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
| `hf_jobs/sweeps/*.py` | Sweep modules (Israel-junction Part A, thickness bound, GW recoil, Krasnikov tube, shift families, hybrid wall) |
| `hf_jobs/configs/*.json` | Sweep configurations (per-sweep `_preview` and `_full` configs) |
| `requirements.txt`, `requirements-gw.txt` | Pinned dependencies for local / Colab / HF Jobs |

---

## Open leads (ranked by signal-per-effort, post-Session-10)

1. **(NEWLY ELEVATED, Session 10.) Fell-Heisenberg $(m, n)$ residual-WEC search.** Our Session 10 reproduction of Fell-Heisenberg 2021 ([`fell_heisenberg.ipynb`](fell_heisenberg.ipynb)) shows full WEC violated in only ~1.3% of interior cells with a moderate axisymmetric-breaking $(m, n)$ choice. Their text says these regions "cannot be removed by modification"; their actual numerical evidence does not establish that strongly. **Targeted parameter sweep over $(V, \sigma, m_0, a, \ell, r)$ looking for a configuration with 0% full-WEC violation.** If found, this is the **first standing fully-WEC-respecting classical warp drive in standard GR** — substantially more than Fell-Heisenberg themselves claim. Effort: 1-2 sessions on top of the existing pipeline. See [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) §"Most surprising finding."

2. **Garattini-Zatrimaylov 2025 reproduction.** They claim a bubble at Hubble velocity in de Sitter satisfies averaged WEC/NEC. Our Slice 5 McVittie pipeline is already set up; adding a bubble on top and computing the averaged conditions is a focused extension. Either validates or refutes their result. **Effort: 1-2 sessions.**

3. **Path 2B (Casimir / boundary-mode QFT) — start the programme.** Entirely new front. Rodal 2025 and Fell-Heisenberg 2021 both sharpen the QFT-search target to anisotropic transverse vacuum stresses with positive normal energy density. Tasks 2B.1–2B.5 in [`ROADMAP.md`](ROADMAP.md) are the natural starting points. **Effort: large (multiple sessions); largest scope.**

4. **Slice 4b (Krasnikov 2003 hybrid quantum/classical wall).** Reproduce Krasnikov's $10^{-3}$ g dihedral-portal + Van Den Broeck pocket and ask whether adding a Fuchs-class classical shell can eliminate the residual mg of QI-bounded negative energy. Focused, mostly computational. **Effort: 1 session.**

5. **TRUST_AUDIT #3 (Warp Factory + Fuchs Fig. 10 reproduction).** Last deferred audit item. Independent verification of the Fuchs 2024 anchor. Requires MATLAB on Windows (the only friction). **Effort: 1 session of MATLAB wrestling.**

6. **Slice 6b (computational $f(R)$).** Build a 4th-order PDE solver for $f(R) = R + \alpha R^2$, compute the Einstein/Jordan-frame split for the Alcubierre metric, ask whether matter-side stress-energy can be DEC-respecting. **Effort: large; significant new infrastructure.**

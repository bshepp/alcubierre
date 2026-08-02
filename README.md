# Alcubierre Warp Drive — Boundary-Mode Reformulation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19689587.svg)](https://doi.org/10.5281/zenodo.19689587)

**Citable archive:** every tagged release is archived on Zenodo. Cite the concept DOI [10.5281/zenodo.19689587](https://doi.org/10.5281/zenodo.19689587) (resolves to the latest version), or a version DOI for a frozen snapshot ([v0.2.0](https://doi.org/10.5281/zenodo.21333096) · [v0.1.0](https://doi.org/10.5281/zenodo.19689588)). Citation metadata: [`CITATION.cff`](CITATION.cff).

## Project Overview

This project investigates whether the exotic matter required by the Alcubierre warp drive metric can be reinterpreted as a **boundary effect** rather than an independent material source. The original hypothesis proposed a "method of images" reformulation in linearized gravity; the mathematics has since refined this into a **boundary-mode decomposition** approach grounded in the Casimir analog.

## Core Claim

The negative energy density in the Alcubierre bubble wall is not a substance to be manufactured. It is the second-order energy stored in a gravitomagnetic field configuration constrained by boundary conditions — structurally analogous to how the Casimir effect produces negative energy density between conducting plates. Whether this analogy is merely structural, reflects a shared physical mechanism, or can be replaced by a purely classical matter-shell construction is pursued along two parallel tracks (see below).

## Current Status

**(2026-08-02, post-Session 57.)** Phases 0–4 are closed or fully dispositioned: 0–1 (foundation + linearization), 2A (matter-shell, slice-scoped), 2B (Casimir route — closed negative as a physical mechanism, Session 34), 2C (six adjacent slices, all null), 2D (Fell–Heisenberg — strict-pass re-scoped as an evaluation-box artifact, Session 42), 2E (deferred relaxations — fully dispositioned, Sessions 49–52), 3 (numerical verification through the certified minimal-mass maps and the external adjudications: Lentz closed negative at class level S43–45, Garattini–Zatrimaylov reproduced exactly S46, Natário 2002 reproduced exactly S56), and 4 (no-go confrontation — executed Session 57: SSV 2021, Pfenning–Ford 1997, Everett 1996, and Hiscock 1997 instrument-verified against our results, 12/12 battery, no contradictions; see [`NOGO_CONFRONTATION.md`](NOGO_CONFRONTATION.md)). What remains open is externally gated (2E.3 quantum sources, 2E.5 higher-D Krasnikov — awaiting publications) or deferred with explicit criteria (2E.1 deep-dynamical legs; 5.3 wall stability). **[`NAVIGATOR.md`](NAVIGATOR.md) is the live front door** — current-state paragraph, load-bearing-assumptions table, document index.

The founding analysis below is retained for orientation. Path 2A's static-slice analysis (Sessions 5–8) produced four results within the slice **Alcubierre $\beta^x \hat x$ shift × spherical Fuchs-class shell or static cylindrical Krasnikov tube × asymptotically flat vacuum exterior × steady-state metric or its Lorentz boost × 4D General Relativity**:

(i) DEC-compatible static spherical Fuchs shells exist with $\Delta_{\min}/R = \kappa\beta/C$;
(ii) within the catalogued mechanisms, no classical mechanism accelerates such shells in vacuum to warp-relevant $\Delta v$;
(iii) static-infrastructure Krasnikov tubes have no classical-matter wall for any $\eta > 0$ in the bare-vacuum case;
(iv) Krasnikov-tube networks generate CTCs (Everett–Roman 1997).

The **slice composite** is "no useful classical warp drive within these assumptions." This is informative but is not the closure of the classical question — six adjacent slices were explored in Phase 2C (Sessions 9–10, all closed within their scopes), and the deliberately-deferred Phase 2E relaxations have since been fully dispositioned (Sessions 49–52: time-dependence positive-within-slice; topology and modified gravity closed negative, the latter with a designer-f(R) LP theorem; quantum sources and higher-D variants externally gated).

- **Path 2A (primary, static slice mapped):** Anchored on Fuchs et al. 2024's *Constant Velocity Physical Warp Drive Solution* (arXiv:2405.02709). See [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md) §0.5 for the explicit slice scope and which assumptions Phase 2C relaxed.
- **Path 2B (CLOSED as a physical mechanism, Session 34):** the Casimir / boundary-mode programme was closed by the Task 2B.8 spin-2 obstruction assessment — no material gravitational conductor exists in known physics, the one claimed loophole (superconductor Heisenberg–Coulomb mirrors) is speculative and unobserved, and even a *perfect* graviton mirror falls 63.5–69.6 orders of magnitude short of the project's certified density targets. See [`QUANTUM_CLASSICAL_BRIDGE.md`](QUANTUM_CLASSICAL_BRIDGE.md) §8 (with reopening triggers); the 2B.1–2B.6 mode-decomposition mathematics survives as a classification tool.
- **Phase 2C (closed, Sessions 9–10):** Each of the six slices relaxed one assumption from the static-slice scope: (1) alternate shift families, (2) Fuchs+Krasnikov hybrid wall, (3) time-dependent acceleration, (4) Krasnikov-2003 QI loosening, (5) cosmological exterior, (6) modified gravity. See `ROADMAP.md` Phase 2C, [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md) §0.5, and [`TRUST_AUDIT.md`](TRUST_AUDIT.md) for verification interleaves.

See `MATTER_SHELL_PATH.md` §6 for outcome scenarios and §9 for the static-slice analysis.

**Project mode:** This is a personal landscape exploration, not a paper-driven programme. There are no concrete deliverables. Conclusions are reported with explicit slice-of-parameter-space scope so the limits of each result are visible. See [`TRUST_AUDIT.md`](TRUST_AUDIT.md) for the honest accounting of what we derived vs. what we accepted on the literature's authority.

**How this was produced.** The work is a sustained collaboration between Brian Sheppard (project owner — direction, scoping, gating decisions, compute budget, domain reading) and a series of frontier AI coding agents (Anthropic Claude — including Sonnet, Opus, and Opus 4.7 — accessed via GitHub Copilot, 2026-03 onward). The agents executed essentially all of the symbolic derivations, notebook code, sweep modules, prose drafting, and HF-Jobs orchestration; the human direction set the questions, the slice scopes, the trust grading, and the stop conditions. The project started as a capability probe — "what can a current coding agent do with a speculative GR construction?" — and evolved into a genuine landscape map as the human side gained working familiarity with the literature. Wins and losses are shared. Per [`speculation/epistemological_style_guide.md`](speculation/epistemological_style_guide.md), this collaboration is part of the methodology, not a footnote. The conversation logs are not committed but are archived locally for reproducibility.

For the meta-framing of this project alongside the rest of the portfolio (capability probe + research finding + methodology study), see [`speculation/epistemological_style_guide.md`](speculation/epistemological_style_guide.md).

## Documents

| File | Contents |
|------|----------|
| **[NAVIGATOR.md](NAVIGATOR.md)** | **Front-door map of the project: where to start, canonical load-bearing-assumptions table, document index, ranked open leads. The first thing to read if you're returning after a break.** |
| **[LANDSCAPE_SYNTHESIS.md](LANDSCAPE_SYNTHESIS.md)** | **Long-form narrative synthesis structured by physics question rather than chronology. The "what we learned" doc.** |
| [ALCUBIERRE_IMAGE_METHOD.md](ALCUBIERRE_IMAGE_METHOD.md) | Original seed document — image-method hypothesis, GEM framework, proposed calculation sequence (historical / pre-pivot) |
| [ALCUBIERRE_MARCH30_INTEGRATION.md](ALCUBIERRE_MARCH30_INTEGRATION.md) | Integration addendum — literature review, Casimir connection, research context |
| [LINEARIZATION_CALCULATION.md](LINEARIZATION_CALCULATION.md) | Complete linearization derivation, ADM stress-energy, Poisson structure, image method analysis, and boundary-mode pivot |
| **[MATTER_SHELL_PATH.md](MATTER_SHELL_PATH.md)** | **Path 2A (primary) — classical matter-shell realization, Fuchs et al. mapping, Israel junction conditions** |
| [QUANTUM_CLASSICAL_BRIDGE.md](QUANTUM_CLASSICAL_BRIDGE.md) | Path 2B (parallel) — quantum vs. classical gap, three-tiered claim structure, Casimir route |
| [LITERATURE.md](LITERATURE.md) | Full literature catalog with abstracts, arXiv links, and relevance notes |
| [ROADMAP.md](ROADMAP.md) | Research phases, decision points, and open questions |
| [SESSION_LOG.md](SESSION_LOG.md) | Chronological record of work sessions and findings |
| [verification.ipynb](verification.ipynb) | SymPy/numpy notebook verifying all key expressions from the linearization calculation |
| **[matter_shell.ipynb](matter_shell.ipynb)** | **Path 2A notebook — Fuchs bump function, Israel junction, angular decomposition, EC scaling** |
| **[israel_junction.ipynb](israel_junction.ipynb)** | **Path 2A Package 1 (Task 2A.6) — full Israel junction Part A (static) + Part B (boosted), angular decomposition of $[K_{ab}]$, DEC boundary, critical $\lambda_*$** |
| **[thickness_bound.ipynb](thickness_bound.ipynb)** | **Path 2A Package 2 (Task 2A.7) — minimum shell thickness scaling law $\Delta_{\min}/R = \kappa\beta/C$, numerical sweep, Fuchs comparison** |
| **[acceleration.ipynb](acceleration.ipynb)** | **Path 2A Package 3 (Task 2A.10) — ADM 4-momentum obstruction, three-mechanism catalog, GW-recoil quantitative ceiling via HF Jobs + Varma 2022 rescaling** |
| **[krasnikov_tube.ipynb](krasnikov_tube.ipynb)** | **Path 2A Task 2A.13 — Krasnikov 4D metric + Fuchs-class thick wall; reproduces Everett–Roman Eq. 14 symbolically; universal scaling law $\rho_p^{\min} \propto -\eta/\epsilon^2$; HF Jobs sweep returns WEC pass rate 0.0000. Closes the speculation document.** |
| [RODAL2025_EVALUATION.md](RODAL2025_EVALUATION.md) | Critical evaluation of arXiv:2512.18008 (Rodal, Gen. Rel. Grav. 58:1, 2026): irrotational warp drive with 38× peak-deficit reduction; updated Path 2B search target |
| [FELL_HEISENBERG2021_EVALUATION.md](FELL_HEISENBERG2021_EVALUATION.md) | Critical evaluation of the Fell–Heisenberg 2021 positive-energy candidate; the Phase 2D arc dismantled its strict-pass set (evaluation-box artifact, Session 42) |
| [BOBRICK_MARTIRE2021_EVALUATION.md](BOBRICK_MARTIRE2021_EVALUATION.md) | Critical evaluation of Bobrick–Martire 2021 (warp-drive taxonomy); source-matter classification used in Task 2D.9 |
| [LENTZ2020_EVALUATION.md](LENTZ2020_EVALUATION.md) | Critical evaluation of Lentz 2020 (positive-energy soliton); closed negative at class level (Sessions 43–45): full WEC/DEC strictly violated on every compact member's wavefront |
| [GARATTINI_ZATRIMAYLOV2025_EVALUATION.md](GARATTINI_ZATRIMAYLOV2025_EVALUATION.md) | Critical evaluation of Garattini–Zatrimaylov 2025 (de Sitter warp); reproduced exactly (Session 46) — comoving vacuum void, ANEC violated, zero transport content |
| [NATARIO2002_EVALUATION.md](NATARIO2002_EVALUATION.md) | Critical evaluation of Natário 2002 (zero-expansion warp class); reproduced exactly and sharpened (Session 56) — its verified content is itself a no-go |
| [NOGO_CONFRONTATION.md](NOGO_CONFRONTATION.md) | Phase 4 (Session 57): the four canonical no-go works (SSV 2021, Pfenning–Ford 1997, Everett 1996, Hiscock 1997) premise-mapped and instrument-verified against our results — no contradictions; the certified shell corridor sits in SSV's declared open flank |
| [KRASNIKOV_TUBE_NOTES.md](KRASNIKOV_TUBE_NOTES.md) | Quantitative synthesis of Krasnikov 1995 / Everett–Roman 1997 / Krasnikov 2003 prior art; comparison to Path 2A; Task 2A.13 update note |
| [TRUST_AUDIT.md](TRUST_AUDIT.md) | Honest accounting: which results are derived ourselves vs. accepted on the literature's authority. A-graded: Tasks 2A.13, 2A.6/4b. Closed by Session 9 audit interleaves: #4, #6, #7, #8. |
| **[shift_families.ipynb](shift_families.ipynb)** + [SHIFT_FAMILIES_NOTES.md](SHIFT_FAMILIES_NOTES.md) | **Phase 2C Slice 1 — alternate axisymmetric shift families (Alcubierre, Natário, irrotational, free-form Bessel). Closed analytically (Session 36): no family member satisfies WEC everywhere, for any parameters or radial profile; corrected sweeps (0/140 preview, 0/2496 full) concur. Session-9 numbers superseded by the Session-36 frame-projection correction — see the NOTES.** |
| **[hybrid_wall.ipynb](hybrid_wall.ipynb)** | **Phase 2C Slice 2 — Krasnikov wall + Fuchs-style matter-shell perturbation. 0/480 sweep points achieve WEC. Single-bump matter cancellation hand-wave is upheld.** |
| **[time_dependent.ipynb](time_dependent.ipynb)** + [TIME_DEPENDENT_NOTES.md](TIME_DEPENDENT_NOTES.md) | **Phase 2C Slice 3 — explicit $v(t)$ ramp. $\dot v$ correction is antisymmetric in $x$; net momentum injection is zero at quadrupole order. Package 3 conclusions transfer.** |
| [KRASNIKOV2003_EVALUATION.md](KRASNIKOV2003_EVALUATION.md) | Phase 2C Slice 4 — critical evaluation of Krasnikov 2003's three QI-loosening loopholes. Our classical no-go is QI-independent and unaffected. |
| **[cosmological_exterior.ipynb](cosmological_exterior.ipynb)** + [COSMOLOGICAL_EXTERIOR_NOTES.md](COSMOLOGICAL_EXTERIOR_NOTES.md) | **Phase 2C Slice 5 — McVittie exterior. Cosmological-exterior momentum-exchange ceiling: $\Delta v \le 10^{-36}$ m/s. Asymptotic-flatness assumption not load-bearing for momentum exchange (but Garattini-Zatrimaylov 2025 modifies energy-condition obligations under a velocity-matching condition).** |
| [MODIFIED_GRAVITY_LIT.md](MODIFIED_GRAVITY_LIT.md) | Phase 2C Slice 6 — literature pull on $f(R)$ wormholes, hidden-geometric positive-energy solitons, and de Sitter warps. Modified gravity is a real loophole in Jordan frame; interpretation-dependent. |

## Key Results So Far

1. The Alcubierre spatial geometry is **exactly flat** — all warp content lives in the shift vector $\beta^x = -v_s f(r_s)$
2. The warp drive is **gravitomagnetic at leading order** — frame-dragging, not Newtonian potential
3. The shift vector satisfies a **Poisson equation** with source localized at the bubble wall
4. Point-image decomposition **does not work** (constant interior field incompatible with point sources)
5. The **Casimir/boundary-mode interpretation is strengthened** — this is the correct mathematical framework
6. The project pivoted from "method of images" to **"boundary-mode decomposition"**
7. **Fuchs et al. 2024 is a direct realization of the boundary-mode framework** with a classical matter shell — no quantum effects required. This is the anchor for Path 2A.
8. On a sphere centered on the bubble, the Alcubierre shift is a **pure $l = 1$ dipole** in the radial projection (verified in `matter_shell.ipynb` §4)
9. Order-of-magnitude scaling for the matter-shell route: $\beta_\text{warp} \lesssim GM\Delta^2/(R^3 c^2)$ — agrees with Fuchs's empirical bound $\beta \le 0.02$ to within an order of magnitude
10. The thin-shell (Israel) junction for a static Schwarzschild + Minkowski match reproduces the standard weak-field shell mass $\mu \approx M + GM^2/(2R)$ — notebook framework validated against textbook result
11. **Path 2A minimum shell thickness scaling law** (Task 2A.7, `thickness_bound.ipynb`): $\Delta_{\min}/R = \kappa\,\beta/C$ with $C = 2GM/(Rc^2)$ and analytic $\kappa \in [0.05, 0.875]$ (upper bound per Task 2A.9a; the full thick-shell numerical coefficient is $\kappa \approx 4.2$–$5.8$, Tasks 2A.9b/3.10). Trades the Alcubierre exotic-energy requirement ($\sim 10^{30}$ kg of negative energy) for a positive-energy compactness requirement ($\sim 10^{19}$–$10^{20}$ kg of ordinary matter at $R = 100$ m, $\beta = 0.5$)
12. **Part B critical $\lambda_*$ acceleration obstruction** (Task 2A.6, `israel_junction.ipynb` Part B): for thin-wall parameters, DEC fails during accelerating transients at $\lambda = v_{\rm ext}/v_{\rm int} < \lambda_* \approx 0.55$. Isolates acceleration as the remaining open problem (Task 2A.10)
13. **Path 2A dynamical closure** (Task 2A.10, `acceleration.ipynb`): ADM 4-momentum conservation rules out self-acceleration in vacuum; three-mechanism catalog leaves only ordinary mass ejection as viable. GW-recoil ceiling $\lesssim 0.25\%$ of $v_{\rm warp}$ under most favourable Fuchs-compatible parameters (HF Jobs sweep + SXS rescaling of Varma et al. 2022). Strictly strengthens Schuster–Santiago–Visser 2023 Theorem 3 *within the static-shell + Alcubierre-shift + asymptotically flat vacuum + 4D Einstein gravity slice*. Path 2B (Casimir), then the remaining candidate for a dynamical drive, was later closed by Task 2B.8 (Session 34); the six Phase 2C adjacent slices explored other ways the no-go could be broken and closed within their scopes — see [`NAVIGATOR.md`](NAVIGATOR.md) and [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md)
14. **Path 2A static-infrastructure closure** (Task 2A.13, `krasnikov_tube.ipynb`): symbolic Einstein-tensor pipeline reproduces Everett–Roman 1997 Eq. 14 exactly; universal scaling law $\rho_p^{\min}(\eta, \epsilon) = -\kappa_K(\eta)/\epsilon^2$ with $\kappa_K(\eta) \approx 0.122\,\eta$ at small $\eta$, verified to 14-decimal $\epsilon$-independence; HF Jobs preview sweep returns **WEC pass rate 0.0000** across 300 $(\eta, \epsilon, n)$ points. Establishes the unobservability tradeoff: $|\rho_p^{\min}|$ and the observable lightcone opening both scale as $\eta$, so their ratio is fixed and a Krasnikov tube cannot be made simultaneously useful and energy-condition-friendly. Closes the `speculation/RING_NETWORK_CONCEPT.md` static-infrastructure-network branch
15. **Certified minimal-mass floors** (Tasks 3.10/3.10+, Sessions 32 + 47–48): the exact-symbolic radial evaluator (`warp_factory_py/solvers/axisymmetric_ec.py`, ground-truth adjudicated in Session 30) locates the canonical constant-density floor $M_{\min} = 2.568 \times 10^{27}$ kg (the canonical Fuchs mass is over-provisioned 1.75×), re-based −13.3% to $2.226 \times 10^{27}$ kg by the two-body pressure ansatz — with the graded-wall continuum closed negative (0/80)
16. **Four published external constructions adjudicated in-pipeline** (Sessions 42–56): Fell–Heisenberg 2021 (strict-pass is a box artifact), Lentz 2020 (closed negative at class level), Garattini–Zatrimaylov 2025 (reproduced exactly; comoving vacuum void, zero transport content), Natário 2002 (reproduced exactly; its verified content is itself a no-go, sharpened: WEC violated at 100% of wall points, Hawking–Ellis Type IV dominant, off-axis ergo-band from $v^* \approx 0.18$)
17. **Phase 4 no-go confrontation executed** (Session 57): SSV 2021, Pfenning–Ford 1997, Everett 1996, and Hiscock 1997 premise-mapped and instrument-verified (12/12 battery) — no certified result contradicts any of them; the Alcubierre–Lobo NEC identity $G_{zz} = 3G_{nn}$ certified as an exact class identity; the EC-clean shell corridor sits exactly in the flank SSV's Appendix B declares open (lapse ≠ 1 / curved slices). See [`NOGO_CONFRONTATION.md`](NOGO_CONFRONTATION.md)

## Running the notebooks

All notebooks run locally on any Python 3.12+ environment with the pinned scientific stack from [`requirements.txt`](requirements.txt). For heavier parameter sweeps and the GW-recoil numerics in [`acceleration.ipynb`](acceleration.ipynb), two external compute paths are wired up:

| Notebook | Local default | Recommended for heavy cells |
|---|---|---|
| [verification.ipynb](verification.ipynb) | Yes | — (pure symbolic) |
| [matter_shell.ipynb](matter_shell.ipynb) | Yes | — (moderate numerics) |
| [israel_junction.ipynb](israel_junction.ipynb) | Yes for cells 1–7, 10–15 | Cell 8 sweep: HF Jobs `cpu-upgrade` or Colab CPU |
| [thickness_bound.ipynb](thickness_bound.ipynb) | Yes for analytical cells | Cell 6 sweep: HF Jobs `cpu-upgrade` |
| [acceleration.ipynb](acceleration.ipynb) | Yes for cells 1–8 | Cells 9–12 (NR / GW recoil): HF Jobs `cpu-upgrade` with `requirements-gw.txt` |
| [krasnikov_tube.ipynb](krasnikov_tube.ipynb) | Yes for all cells | Cell 19 sweep: HF Jobs `cpu-upgrade` recommended for full $\sim 30{,}000$-point grid; preview ($\sim 300$ points) runs in ~3 s locally |

### Google Colab

Click the "Open In Colab" badge at the top of any notebook. The first code cell auto-installs [`requirements.txt`](requirements.txt) when `google.colab` is detected, so no manual setup is needed. Free T4 GPUs work for any GPU-accelerated cell but none of the current notebooks require GPU.

### Hugging Face Jobs

Heavy parameter sweeps are factored out of the notebooks into sweep modules under [`hf_jobs/sweeps/`](hf_jobs/sweeps/) and dispatched via [`hf_jobs/run_sweep.py`](hf_jobs/run_sweep.py). Typical invocation from a notebook cell:

```bash
hf jobs run --flavor cpu-upgrade \
    -e HF_JOB=1 -v $PWD:/work python:3.12 \
    bash -c "cd /work && pip install -q -r requirements.txt && \
             python -m hf_jobs.run_sweep <sweep_name> \
                 --config hf_jobs/configs/<sweep_name>_full.json"
```

Outputs land in `sweeps/<sweep_name>_<timestamp>.parquet`. Each sweep ships with a `*_preview.json` config (small grid, runs locally in seconds) and a `*_full.json` config (full grid, runs on HF Jobs in minutes). Always validate the preview locally before dispatching the full grid — HF Jobs is billed per second and the preview is the safety net.

Large sweep outputs and the Package 3 NR data optionally mirror to a Hugging Face dataset repo; see `MATTER_SHELL_PATH.md` §3.4 and §7 for the specific dataset slugs once created.

## References (Core)

- Alcubierre 1994 (gr-qc/0009013) — The metric
- Lobo & Visser 2004a (gr-qc/0406083) — Fundamental limitations on warp drives; linearized analysis (must read)
- Lobo & Visser 2004b (gr-qc/0412065) — Linearized warp drive and energy conditions (companion paper)
- Fuchs, Helmerich, Bobrick et al. 2024 (2405.02709) — Physical warp drive with all energy conditions satisfied
- Santiago, Schuster & Visser 2021 (2105.03079) — No-go theorems for positive-energy superluminal drives
- Helmerich et al. 2024 (2404.03095) — Warp Factory numerical toolkit
- Quach 2015 (1502.07429) — Gravitational Casimir effect (key for quantum/classical bridge)
- Ford & Pfenning 1998 (gr-qc/9805037) — Quantum inequalities in curved spacetime
- Full literature table in [LITERATURE.md](LITERATURE.md)

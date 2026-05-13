# Navigator — Where Everything Is

**Last updated:** 2026-05-13 (Session 25 — **Phase 3.3 sub-items 1–3 closed via Python port.** Fuchs Fig. 10 reproduced byte-for-byte (rho diff 2.6e-11, ECs to ≤3e-3 sampling noise) by an independent NumPy pipeline (no MATLAB); in-shell pass-fractions = 1.0000 for NEC/WEC/DEC/SEC in both byte-faithful (`wf_compat=True`) and bug-corrected (`wf_compat=False`) modes — Fuchs's central claim survives both. Three WarpFactory bugs identified and isolated: (i) `ricciT.m` Christoffel-permutation typo, (ii) `getEulerianTransformationMatrix.m` time-column sign flip, (iii) `getEnergyConditions.m` curved-coord re-lowering of tetrad-frame T in NEC/WEC branches. New port modules: [`warp_factory_py/metrics/warp_shell.py`](warp_factory_py/metrics/warp_shell.py) + the existing solvers in [`warp_factory_py/solvers/`](warp_factory_py/solvers/). Continued from Session 23 below.

**Session 23 (2026-05-12):** Slice 4b reframed as the *minimum* quantum supplement required to repair pointwise DEC failures of a classical Krasnikov-tube wall (rather than the original "add a Fuchs shell" framing, which is incompatible with the cylindrical $x$-translation invariance of the tube). Result ([`krasnikov_hybrid.ipynb`](krasnikov_hybrid.ipynb), [`KRASNIKOV_HYBRID_NOTES.md`](KRASNIKOV_HYBRID_NOTES.md)): within the Krasnikov-tube slice ($\eta\in[10^{-2},1)$, $\epsilon\in[10^{-2},1]\,\mathrm{m}$, $n=\rho_{\max}/\epsilon\in[2,100]$, $D\ge 1\,\mathrm{m}$), the required supplement exceeds the Krasnikov 2003 §3.3 milligram budget by $\ge 31$ orders of magnitude across all 360 sweep points (minimum $r=|E_Q^-|_{\rm req}/10^{-3}\,\mathrm{g}=1.10\times 10^{31}$ at $D=1\,\mathrm{m}$). Three verification gates pass: (i) inner-edge $\rho_p$ matches Everett-Roman saturation, (ii) universal $\epsilon^2$ collapse confirms the $\rho_p\propto\eta/\epsilon^2$ Phase 2A.13 scaling, (iii) Everett-Roman $\alpha$-band recovered at $\alpha=0.13$. Phase 3.3 (nested + non-spherical Fuchs shells) deferred — MATLAB toolchain is unavailable in the current environment; will reactivate if MATLAB access is acquired or a Python port of Warp Factory's TOV+EC pipeline is undertaken.

(Session 22 — Task 2D.5f closed via chunked HF Jobs dispatch (4 × 2520-point cpu-xl sub-jobs, ~$9 total). Direct $N_{\rm pts}=129$ re-sweep of the full 10080-point refine grid: **6240 / 10080 strict WEC ∧ DEC pass (61.90%)**, $E_{\rm neg} = 0$ for every strict-pass row; strict WEC alone passes 7941 / 10080 (78.78%), so DEC is the binding constraint. Direct count is **+5.8% above the §11.6 extrapolation (~5900)**; the Session-14 "strict-pass set is real but boundary-sensitive" reading is now confirmed at the canonical resolution. The 2D.16 reopening criterion (≳5% of strict-pass classifications flipped) was **not triggered**, so the Session-17 Phase E xAct cross-check (9/9 anchors A-grade) remains the operative cross-pipeline anchor and no 20-anchor re-cross-check is needed. Cumulative reading is unchanged: every structural test applied (single-cell passenger, CTC sea, 76× mass overhead, no asymptotic decay envelope, box inside its own would-be Schwarzschild horizon) **degrades** the warp-drive interpretation; none restores it; the now-direct strict-pass count does not change this. Phase 2D headline (existence + tempering) is closed; 2D.5e and 2D.11 remain `[~]` partial.)

**Recent-session changelog** (all in [`SESSION_LOG.md`](SESSION_LOG.md)):
- **Session 25 (2026-05-13):** Phase 3.3 items 1–3 closed via Python port. Fuchs Fig. 10 reproduced byte-for-byte; pass-fractions=1.0000 in-shell in both `wf_compat` modes; three WarpFactory source bugs isolated. New: [`warp_factory_py/metrics/warp_shell.py`](warp_factory_py/metrics/warp_shell.py).
- **Session 24 (2026-05-13):** WarpFactory Alcubierre anchor (A.6) reproduced via Python port; bugs #1 (Ricci typo) and #2 (Eulerian sign) identified.
- **Session 23 (2026-05-12):** Slice 4b (Task 2A.13b, Krasnikov hybrid quantum/classical wall) closed NEGATIVE — required supplement is $\ge 10^{31}\times$ the Krasnikov 2003 mg budget across the full ($\eta,\epsilon,n$) grid. Phase 3.3 deferred (MATLAB unavailable).
- **Session 22 (2026-04-27):** 2D.5f closed (chunked Npts=129 full re-sweep, 6240/10080 strict-pass).
- **Session 21 (2026-04-26):** Npts=129 cpu-upgrade/cpu-xl single-shot retries failed (OOMKilled / 3 h timeout); will-not-retry post-mortem motivated the chunked dispatch path used in Session 22.
- **Session 20 (2026-04-25):** Tier A figures programme delivered ([`figures/plot_figures.py`](figures/plot_figures.py); seven subcommands; PNGs mirrored to `webpage/assets/figures/`).
- **Session 19 (2026-04-21):** Phase 3.1 + 3.2 closed via Warp Factory (standard Alcubierre at $v=c$ recovers Pfenning-Ford expectations; Fuchs $\beta_{\max}$ surface confirms scaling-law form with $\kappa$ varying 18%); Phase 3.3 (nested + non-spherical shells) is the next sub-task.
- **Session 18 (2026-04-21):** Warp Factory + Fuchs Fig. 10 reproduced (TRUST_AUDIT #3 closed B → A); 2A.9b κ-bracket cross-check returned $\kappa^{\rm num} \in (4.17, 5.83]$ vs analytic $[0.05, 0.875]$ — refines 2A.7 downward by 6×.
- **Session 17 (2026-04-21):** Phase 2D triad closed — VIQ (2D.12, 76× mass overhead, $E_{\rm neg}=0$ universal), B-M classification (2D.9, Class III geometric + non-isotropic + static), CTC analysis (2D.7, 98.3% of strict-pass host CTC sea), xAct cross-pipeline check (2D.8, 9/9 anchors A-grade), asymptotic-matching residual (2D.10 second half, no decay envelope + box inside would-be horizon).
- **Session 16 (2026-04-21):** Slab-patch (2A.15) third k-data-point for the codimension-counting law ([`slab_patch.ipynb`](slab_patch.ipynb), [`SLAB_PATCH_NOTES.md`](SLAB_PATCH_NOTES.md), [`speculation/CODIMENSION_SCALING.md`](speculation/CODIMENSION_SCALING.md); per-data-point grade A, induction grade C).
- **Session 15 (2026-04-20):** Phase 1 reading-list closeout (Tasks 1.8 Lobo-Visser 2004, 1.10 gauge analysis, 1.11 spin-2 vs spin-1 — all closed); 2A.8 / 2A.9a / 2A.11 / 2A.12 closed via the same closeout sweep; Task 2D.11 vortical FH (Phases 1+2) NEGATIVE.

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
- **Fell & Heisenberg 2021** (multi-mode "hidden geometric structures" in standard GR — outside Slice 1). **Sessions 11-14 in [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md)**: a connected smooth-boundaried 5-D manifold of strict WEC+DEC-passing configurations exists, with $E_{\rm neg} = 0$ (no negative energy density anywhere). The Npts=97 sweep originally reported 6818/10080 strict-pass; **Session 14b §11 Npts=129 convergence test revises this down to ~5900/10080** because boundary points (47% of which flip pass→fail at higher resolution) were over-counted at Npts=97. The boundary surface is approximately a degree-4 polynomial implicit surface (99.98% in-sample classifier accuracy) but dense (no sparse closed-form per Session 14 §10). **Critical caveat from Session 14a §9**: every passing configuration is "all wall, no interior" — the connected $|\vec{N}| < 1$ region containing the origin (the would-be passenger zone) is a single grid cell with apparent radius $h/2$ that scales to **zero physical volume in the continuum limit**. The bubble geometry is "calm point at origin surrounded immediately by uniform $\sim 15c$ shift throughout the box." This degrades the warp-drive interpretation substantially: the existence claim holds mathematically, but no observer can occupy an extended interior. The acceleration / source-matter / asymptotic-matching questions are partially moot at this finding — there's nothing to propel. See [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) and [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md);
- **Lobo & Oliveira 2009** (f(R) wormholes — Jordan-frame loophole, interpretation-dependent);
- **Garattini & Zatrimaylov 2025** (de Sitter bubble at Hubble velocity — averaged WEC/NEC only);
- **Rodal 2025** (irrotational Natário-class, 38× peak-deficit reduction in standard GR but still violates NEC/WEC/DEC/SEC).

The honest project summary, post-Session-22: **"the no-go is robust for full WEC within its single-mode-axisymmetric slice; the multi-mode Fell-Heisenberg case admits a positive-energy fully-WEC-and-DEC-respecting static metric at all amplitudes — the energy-condition bottleneck is mathematically solved within this static slice. But the foliation-health analysis (Task 2D.6 / §9) shows the geometry is 'all wall, no interior': a passenger zone of zero continuum volume. The Session 17 triad (VIQ + B-M + CTC) anchors the claim against three independent external no-go literatures: (i) the L-V VIQ is trivially satisfied by construction but the passenger volume is outweighed by a 76× positive-energy mass cost (§13); (ii) every strict-pass point is B-M geometric Class III + non-isotropic + static, outside every B-M positive-result pathway (§14, [`BOBRICK_MARTIRE2021_EVALUATION.md`](BOBRICK_MARTIRE2021_EVALUATION.md)); (iii) 98.3% of strict-pass rows host an everywhere-outside-passenger CTC region, with the CTC-free tail confined to a low-$V$ weak-warp corner (§15). So we have a positive-energy stationary solution that satisfies WEC+DEC pointwise, does not violate the VIQ, but provides only a single-voxel passenger zone surrounded by a CTC sea. Both questions that drove Session 17 — whether an independent pipeline (Task 2D.8) confirms the strict-pass existence, and whether vorticity-augmented ansätze (Task 2D.11) recover an interior — have now been answered: 2D.8 confirmed the Python pipeline is not artefactual at A-grade across 9 anchors; 2D.11 Phases 1+2 (axisymmetric and Cartesian-constant-amplitude $\vec A$) returned negative; only 2D.11 Phase 3 (multi-mode FH-style $\vec A$) and 2D.5e Z-axis-symmetry plan-B remain genuinely open inside the FH story. Session 22 also closed Task 2D.5f at the canonical resolution: the count is real (6240/10080 strict-pass at $N_{\rm pts}=129$), is +5.8% above the §11.6 extrapolation, and does not trigger the 2D.16 reopening criterion."**

---

## Load-bearing assumptions table (canonical post-Phase-2C)

This is the authoritative version. Slice notes documents that have their own tables now defer to this one.

| # | Sub-assumption | Status | Tested where | Notes |
|---|---|---|---|---|
| 1 | Shift profile is single-mode axisymmetric | **Load-bearing AND broken (Sessions 11-12). But the multi-mode case has a hidden new bottleneck (Session 14). Vorticity does not lift it (Session 15). Triple-anchored against three external no-go literatures + cross-pipeline-verified + asymptotic-matching residual closed (Session 17).** | Slice 1: [`shift_families.ipynb`](shift_families.ipynb), [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md). Multi-mode: [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb), [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md). Sweep + topology + horizon test + xAct cross-check + asymptotic-matching: [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) §16-§17, [`XACT_PIPELINE_NOTES.md`](XACT_PIPELINE_NOTES.md). Vorticity slice: [`FELL_HEISENBERG_VORTICAL_NOTES.md`](FELL_HEISENBERG_VORTICAL_NOTES.md). Session 17 triad: VIQ (§13) + B-M taxonomy (§14, [`BOBRICK_MARTIRE2021_EVALUATION.md`](BOBRICK_MARTIRE2021_EVALUATION.md)) + CTC (§15). | Single-mode axisymmetric: 0/140 sweep points achieve full WEC. **Multi-mode irrotational (Fell-Heisenberg 2021)**: Session 11 sweep found ~6800 / 10080 strict-pass at Npts=97 with $E_{\rm neg} = 0$. Session 12 connectivity: single connected smooth-boundaried 5-D manifold. **Session 14 §9 horizon test**: every passing configuration has zero-volume passenger zone (single-grid-cell continuum-zero). **Session 15 vorticity-augmented (Task 2D.11) Phases 1+2 NEGATIVE**: at the canonical FH anchor, neither axisymmetric $A_\phi(R, Z)$ (216 preview points) nor Cartesian constant-amplitude $\vec A$ (27 preview points) recovers the passenger zone or improves the dec slack — vorticity strictly degrades or doesn't help. **Session 17 triad** (across 6738 strict-pass rows): (A) L-V VIQ is trivially satisfied ($E_{\rm neg}=0$ universally) but $M_{\rm passenger}/V_{\rm passenger}$ ratio is 44-98× (median 76×); (B) every strict-pass point is B-M geometric Class III + non-isotropic + static, outside every B-M positive-result pathway; (C) 6624/6738 = 98.3% host an everywhere-outside-passenger CTC region; the CTC-free 1.7% tail is all at $V=0.10$ with weak warp effect ($\|\vec N\|_{\max}\lesssim 1.2$); naive double-bubble destroys both passenger zones due to missing asymptotic decay envelope. **Session 17 Phase E** (xAct/Mathematica cross-pipeline check, 9 anchors / 9 A-grade, median rel-diff $\sim 2 \times 10^{-6}$): Python pipeline's strict-pass classification + derived statistics are not artefacts of FD truncation or 3+1 decomposition. **Session 17 Phase F** (FH↔Schwarzschild box-edge L-sensitivity, $L \in \{12, 16, 20, 24\}$): $\langle |\vec N| \rangle$ on the box-edge sphere is constant at $\sim 15.5$ (decay slope $+0.04$ — no decay), and the canonical $M_{\rm box}=1850$ puts the would-be Schwarzschild horizon at $r_h=3700 \gg$ all sampled box radii — the FH ansatz has no asymptotic decay envelope and the configuration sits inside its own would-be horizon. Cumulative reading: energy-condition bottleneck solved within static slice; foliation-extent bottleneck persists; warp-drive interpretation degrades to single passenger voxel surrounded by CTC sea inside its own would-be horizon. |
| 2 | Krasnikov-tube wall is bare-vacuum (no matter shell) | **Not load-bearing for single-bump matter perturbations** | Slice 2: [`hybrid_wall.ipynb`](hybrid_wall.ipynb) | 0/480 sweep points achieve WEC. Adding matter shifts the WEC-violating region but does not eliminate it. Multi-bump and off-wall configurations not tested. |
| 3 | Steady-state metric + Lorentz boost is sufficient | **Not load-bearing** | Slice 3: [`time_dependent.ipynb`](time_dependent.ipynb), [`TIME_DEPENDENT_NOTES.md`](TIME_DEPENDENT_NOTES.md) | $\dot v$ correction to $\rho_p$ is antisymmetric in axis-of-motion coordinate $x$, scales as $1/\tau$ (linear in $\dot v$), peaks at 0.3% of static value at $\tau = R/c$. Net momentum injection at quadrupole order is zero by symmetry. |
| 4 | Pfenning-Ford-style tight QI bounds on negative energy | **Substantively weakened by Krasnikov 2003** (but our classical no-go is QI-independent; the mg-scale Krasnikov budget is too small to repair the classical Krasnikov-tube wall by ≥31 OoM, Session 23) | Slice 4: [`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md). Slice 4b: [`krasnikov_hybrid.ipynb`](krasnikov_hybrid.ipynb), [`KRASNIKOV_HYBRID_NOTES.md`](KRASNIKOV_HYBRID_NOTES.md). | Krasnikov gives three loopholes (Weyl/Ricci ratio, $E_{\rm tot}^-$ meaningless, dihedral-portal construction with $10^{-3}$ g exotic matter). Our Task 2A.13 classical no-go is independent of QI. **Slice 4b (Session 23)** asked whether the mg-scale Krasnikov budget could serve as a quantum supplement to repair pointwise DEC failures of the classical Krasnikov-tube wall: across the full ($\eta\in[10^{-2},1)$, $\epsilon\in[10^{-2},1]\,\mathrm{m}$, $n=\rho_{\max}/\epsilon\in[2,100]$) grid the required supplement exceeds the budget by $\ge 10^{31}$ at $D=1\,\mathrm{m}$. Three gates pass: Everett-Roman saturation match, universal $\epsilon^2$ collapse confirming Phase 2A.13 scaling, Everett-Roman $\alpha$-band recovery. The mg budget cannot serve as a quantum patch in this slice. |
| 5a | Asymptotic flatness — momentum exchange | **Not load-bearing** | Slice 5: [`cosmological_exterior.ipynb`](cosmological_exterior.ipynb), [`COSMOLOGICAL_EXTERIOR_NOTES.md`](COSMOLOGICAL_EXTERIOR_NOTES.md) | Cosmological-exterior reaction-mass channel: $\Delta v \le 5.7 \times 10^{-36}$ m/s at $R_{\rm BY} = 100\,R_{\rm shell}$, scaling as $R_{\rm BY}^3$. 42+ orders of magnitude below the GW-recoil channel. |
| 5b | Asymptotic flatness — energy-condition obligations | **Modified for special case $v = v_{\rm Hubble}$** in de Sitter | Slice 5 + Garattini-Zatrimaylov 2025 ([`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md) §"Construction 3") | Bubble at Hubble velocity in de Sitter satisfies *averaged* (not local) WEC/NEC. A real qualifier on Slice 5; only applies under the radial-Hubble-velocity matching condition. |
| 6 | 4D Einstein gravity (Jordan-frame interpretation) | **Real loophole; interpretation-dependent** | Slice 6: [`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md) | Lobo & Oliveira 2009 demonstrate $f(R)$ wormholes where matter satisfies WEC and curvature absorbs the violation in Jordan frame. Einstein-frame transformation moves the violation to a scalar field. Whether this counts as "DEC-respecting matter" depends on which frame you take as physical. Phase 6b (computational $f(R)$ analysis) deferred. |
| 7 | Shell topology is $S^2$ (spherical) | **Not load-bearing — toroidal $T^2$ topology is strictly worse, not a loophole** | Task 2A.14 (cylindrical-reduction limit, scope a): [`toroidal_fuchs.ipynb`](toroidal_fuchs.ipynb), [`TOROIDAL_FUCHS_NOTES.md`](TOROIDAL_FUCHS_NOTES.md). Causal half: [`KRASNIKOV_TUBE_NOTES.md`](KRASNIKOV_TUBE_NOTES.md) §7.1. | Linearized Levi-Civita exterior + Israel junction on a cylindrical surface gives $\Delta_{\min}^\text{cyl} = (3/8)\beta L/M$, *independent of the shell radius* $R$ (one trapped angular dimension instead of two). Torus penalty $\Delta_\text{cyl}/\Delta_\text{sph} = L/R_\text{min} = 2\pi R_\text{maj}/R_\text{min} \geq 2\pi$ for any non-self-intersecting torus. Combined with the Krasnikov-tube no-causal-advantage result, the toroidal-Fuchs path in [`speculation/RING_NETWORK_CONCEPT.md`](speculation/RING_NETWORK_CONCEPT.md) §4 is closed twice over. Scope (b) fat-torus refinement deferred (would only strengthen the dismissal). |

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
| [`toroidal_fuchs.ipynb`](toroidal_fuchs.ipynb) | Task 2A.14 (scope a) — cylindrical-reduction limit of toroidal Fuchs shell; $\Delta_{\min}^\text{cyl} = (3/8)\beta L/M$, torus penalty $\geq 2\pi$ |
| [`TOROIDAL_FUCHS_NOTES.md`](TOROIDAL_FUCHS_NOTES.md) | Companion to `toroidal_fuchs.ipynb`; scope (b) fat-torus deferred follow-up; §6 records the codimension-counting line of inquiry |
| [`slab_patch.ipynb`](slab_patch.ipynb) | Session 16 — k=0 datum for the codimension-counting law; $\Delta_{\min}^\text{slab} = \beta^2 L^2 / (8M)$ (linear-$\beta$ obstruction vanishes; quadratic takes over) |
| [`SLAB_PATCH_NOTES.md`](SLAB_PATCH_NOTES.md) | Companion to `slab_patch.ipynb`; consolidated three-data-point table for the codimension-counting law |

### Phase 2C (adjacent-slices exploration)

| File | Slice | Role |
|---|---|---|
| [`shift_families.ipynb`](shift_families.ipynb) + [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md) | 1 | Alternate axisymmetric shift families |
| [`hybrid_wall.ipynb`](hybrid_wall.ipynb) | 2 | Krasnikov + matter-shell hybrid wall |
| [`time_dependent.ipynb`](time_dependent.ipynb) + [`TIME_DEPENDENT_NOTES.md`](TIME_DEPENDENT_NOTES.md) | 3 | Time-dependent $v(t)$ acceleration |
| [`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md) | 4 | Critical evaluation of Krasnikov 2003 QI loopholes |
| [`krasnikov_hybrid.ipynb`](krasnikov_hybrid.ipynb) + [`KRASNIKOV_HYBRID_NOTES.md`](KRASNIKOV_HYBRID_NOTES.md) | 4b | Task 2A.13b — Krasnikov-2003 mg budget vs pointwise DEC deficit of the classical Krasnikov tube; closed Session 23 NEGATIVE ($r\ge 10^{31}$) |
| [`cosmological_exterior.ipynb`](cosmological_exterior.ipynb) + [`COSMOLOGICAL_EXTERIOR_NOTES.md`](COSMOLOGICAL_EXTERIOR_NOTES.md) | 5 | McVittie + $\Lambda$ exterior |
| [`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md) | 6 | Modified-gravity warp drive literature pull |

### Path 2B and external evaluations

| File | Role |
|---|---|
| [`QUANTUM_CLASSICAL_BRIDGE.md`](QUANTUM_CLASSICAL_BRIDGE.md) | Path 2B (Casimir / boundary-mode) — three-tiered claim structure, outcome matrix, search-target sharpening (anisotropic Casimir) |
| [`RODAL2025_EVALUATION.md`](RODAL2025_EVALUATION.md) | Critical evaluation of Rodal 2025 (irrotational Natário-class warp drive) |
| [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) | Critical evaluation of Fell & Heisenberg 2021. Session 10. **Pipeline regression A-grade**, qualitative claim verified, full-WEC violations smaller than the paper's text suggests. |
| [`LENTZ2020_EVALUATION.md`](LENTZ2020_EVALUATION.md) | Critical evaluation of Lentz 2020 (hyperbolic-shift Einstein-Maxwell-plasma soliton) + Bobrick-Martire 2021 critique. Session 15c. Closes the citation hole in `FELL_HEISENBERG2021_EVALUATION.md`: Lentz checks Eulerian energy density only, not full WEC; explicitly admits DEC failure for the superluminal case; the "plasma source" is a target, not a construction. Logically a special case of Slice 5 (Fell-Heisenberg irrotational shifts). |
| [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb) | Reproduction notebook for Fell & Heisenberg 2021. Session 10. |
| [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) | **Sessions 11-13 sweep + topology**: §1-§6 the strict-WEC+DEC sweep (1404/15000 strict-pass at Npts=65, falsifies FH §3.3 irreducibility claim), §7 the connectivity/topology analysis (single connected smooth-boundaried 5-D manifold; §7.7 polynomial-fit at Npts=65 found degree-3 ~98% accurate boundary; §7.8 Npts=97 resolution-convergence test found the boundary is degree 4-5, not 3, and Npts=65 was systematically biased at low sigma), §8 deferred Hard Fix path (symbolic boundary extraction). |
| [`fell_heisenberg_topology/`](fell_heisenberg_topology/) | Session 12 outputs from Npts=65 refine sweep: 4 figures, summary JSON, boundary CSV. Generated by [`hf_jobs/analysis/fell_heisenberg_topology.py`](hf_jobs/analysis/fell_heisenberg_topology.py). |
| [`fell_heisenberg_topology_hires/`](fell_heisenberg_topology_hires/) | Session 13 outputs from Npts=97 resolution-convergence sweep + Session 14 polynomial-boundary extraction (boundary_eq_summary.json, degree4_surviving_terms.csv, thresholding_effect.png). |
| [`fell_heisenberg_horizon/`](fell_heisenberg_horizon/) | Session 14 Task 2D.6 outputs: 5 foliation-health plots, V-scan, summary JSON, leaderboard CSV. Generated by [`hf_jobs/analysis/fell_heisenberg_horizon.py`](hf_jobs/analysis/fell_heisenberg_horizon.py). |
| [`fell_heisenberg_symbolic/`](fell_heisenberg_symbolic/) | Session 14c Task 2D.5e outputs: 3 validation JSONs (Checkpoints A/B/C), LaTeX summary stub, README explaining the partial-success-and-wall outcome. Generated by [`hf_jobs/analysis/fell_heisenberg_symbolic.py`](hf_jobs/analysis/fell_heisenberg_symbolic.py). |
| [`FELL_HEISENBERG_VORTICAL_NOTES.md`](FELL_HEISENBERG_VORTICAL_NOTES.md) | **Session 15 Task 2D.11 vorticity-augmented FH**: §1 Phase 1 axisymmetric $A_\phi(R, Z)$ NEGATIVE (vorticity does not improve dec slack at the FH anchor; passenger zone unchanged); §2 Phase 2 Cartesian constant-amplitude $\vec A$ NEGATIVE (same headline in a structurally distinct family); §3 Phase 3 FH-style multi-mode $\vec A$ TBD. Cumulative finding: foliation-extent bottleneck persists across irrotational + two perturbative-vortical families. Sweep modules: [`hf_jobs/sweeps/fell_heisenberg_vortical.py`](hf_jobs/sweeps/fell_heisenberg_vortical.py), [`hf_jobs/sweeps/fell_heisenberg_vortical_cartesian.py`](hf_jobs/sweeps/fell_heisenberg_vortical_cartesian.py). |
| [`BOBRICK_MARTIRE2021_EVALUATION.md`](BOBRICK_MARTIRE2021_EVALUATION.md) | **Session 17 Phase B.** Critical evaluation of Bobrick-Martire 2021 four-class warp-drive taxonomy (§2.1) + spherically-symmetric isotropic-fluid construction (§3). Places FH strict-pass in the taxonomy: Class III geometric signature but static ($v_s=0$) ⇒ kinematic Class III does not apply; non-isotropic ⇒ B-M §3 positive-energy pathway does not apply. A/B/C honest-accounting table. |
| [`fell_heisenberg_viq/`](fell_heisenberg_viq/) | **Session 17 Phase A (Task 2D.12)** outputs: full_viq.parquet (6738 strict-pass rows × VIQ columns), summary.json. Three universal findings: $E_{\rm neg}=0$ everywhere (L-V VIQ trivially satisfied), passenger volume = $h^3$ everywhere, $M_{\rm passenger}/V_{\rm passenger}$ = 44-98× (median 76×). Module: [`hf_jobs/analysis/fell_heisenberg_viq.py`](hf_jobs/analysis/fell_heisenberg_viq.py). |
| [`fell_heisenberg_matter/`](fell_heisenberg_matter/) | **Session 17 Phase B (Task 2D.9)** outputs: 8 representative strict-pass points at $N_{\rm pts}=65$, per-point eigenvalues.npz + slice_plots.png, summary.json, leaderboard.csv. All 8 tag as B-M Class III geometric + non-isotropic + static. Module: [`hf_jobs/analysis/fell_heisenberg_matter.py`](hf_jobs/analysis/fell_heisenberg_matter.py). |
| [`fell_heisenberg_ctc/`](fell_heisenberg_ctc/) | **Session 17 Phase C (Task 2D.7)** outputs: single_bubble.csv (6738 strict-pass rows × CTC columns), summary.json. 6624/6738 = 98.3% host an everywhere-outside-passenger CTC region; all 114 CTC-free rows are at $V=0.10$ with $\|\vec N\|_{\max}<1$. Module: [`hf_jobs/analysis/fell_heisenberg_ctc.py`](hf_jobs/analysis/fell_heisenberg_ctc.py). |
| [`XACT_PIPELINE_NOTES.md`](XACT_PIPELINE_NOTES.md) | **Session 17 Phase E (Task 2D.8).** Independent symbolic Mathematica pipeline (Wolfram 14.3 + xAct 1.3.0 + xCoba 0.8.6) cross-checks `adm_stress_energy` (4th-order FD) against `D[]` symbolic differentiation of the closed-form $\phi_{\rm FH}^{\rm smooth}$. **A-grade** at the canonical anchor (124/125 points, median rel-diff $2 \times 10^{-6}$) and across a 9-anchor sweep over $(V, \sigma, r)$. Single outlier at $\vec x = (0,0,0)$ traced to the $\Pi=1/4$ fractional-power non-smooth point of the FH ansatz, consistent with Session 14 §9. Sessions 11-17 results not pipeline-artefacts. Wolfram scripts: [`agent-tools/fh_rho_at_points.wls`](agent-tools/fh_rho_at_points.wls), [`agent-tools/fh_rho_at_points_multi.wls`](agent-tools/fh_rho_at_points_multi.wls); Python harnesses: [`agent-tools/cross_check_xact.py`](agent-tools/cross_check_xact.py), [`agent-tools/cross_check_xact_sweep.py`](agent-tools/cross_check_xact_sweep.py). |

### Verification / linearization

| File | Role |
|---|---|
| [`verification.ipynb`](verification.ipynb) | Sympy/numpy verification of all symbolic results from `LINEARIZATION_CALCULATION.md` |

### Generated figures

| Path | Role |
|---|---|
| [`figures/`](figures/) | Standalone PNG renders of the quantitatively-strongest results (one subdirectory per topic). All produced by [`figures/plot_figures.py`](figures/plot_figures.py); each subcommand reads a parquet/csv from `sweeps/`, `sweeps_remote/`, or `warp_factory_repro/` and emits PNGs into the matching `figures/<topic>/` folder, mirroring into `webpage/assets/figures/<topic>/` for website deploys. Subcommands: `fh-corner`, `kappa-surface-3d`, `thickness-heatmap`, `krasnikov-collapse`, `gw-recoil-cliff`, `hybrid-wall-heatmap`, `shift-families-bars`, plus `all`. Slice scopes are recorded in each PNG's suptitle and on the website galleries (`webpage/{warp-factory,fell-heisenberg,six-slices}.html`). |
| [`figures/plot_figures.py`](figures/plot_figures.py) | Permanent figure-generation script (lives under `figures/` rather than `agent-tools/` because the latter is gitignored throwaway). Argparse dispatch via `SUBCOMMANDS` dict; `_save()` mirrors each PNG to `webpage/assets/figures/`. |

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
| [`speculation/CODIMENSION_SCALING.md`](speculation/CODIMENSION_SCALING.md) | Session 16 — consolidated codimension-counting law statement, three confirmed data points (k=0,1,2), heuristic derivation, hoop-conjecture connection, slice-scope qualifiers, "donit bad" title note |

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

## Open leads (ranked by signal-per-effort, post-Session-22)

**Note:** the Phase 2D Fell-Heisenberg arc is now closed at the headline level. Existence of a positive-energy fully-WEC-and-DEC-respecting static metric is established (Sessions 11-14), characterised topologically (single connected 5-D manifold with smooth boundary, dense not sparse polynomial boundary), independently cross-pipeline-verified at A-grade (Session 17 Phase E, xAct/xCoba 9/9 anchors), counted directly at the canonical resolution (Session 22, 6240/10080 strict-pass at $N_{\rm pts}=129$, +5.8% above the §11.6 extrapolation), and triple-anchored against external no-go literatures (Session 17 triad: VIQ 76× mass overhead, B-M Class III non-isotropic static, 98.3% CTC sea + no asymptotic decay envelope). **The energy-condition bottleneck is mathematically solved within the static slice; the foliation-extent + asymptotic + causal-structure bottlenecks persist; every structural test applied has degraded the warp-drive interpretation, none has restored it.** The remaining open work splits into (a) one residual FH-internal question (multi-mode vortical $\vec A$, Phase 3 of Task 2D.11), (b) the next active phase (Phase 3.3 numerical verification of nested + non-spherical shell geometries), and (c) several long-deferred external-loophole probes whose priorities have not changed since Phase 2C.

1. **Phase 3.3 — nested + non-spherical Fuchs shells.** Stated as the next sub-task in [`ROADMAP.md`](ROADMAP.md) Phase 3 after Sessions 18-19 closed 3.1 and 3.2. Fuchs et al. 2024 §5.2 already sketches that nested concentric shells should reduce required mass; we now have the Warp Factory pipeline + a confirmed scaling-law surface and 18%-spread $\kappa$ ([`WARP_FACTORY_NOTES.md`](WARP_FACTORY_NOTES.md) §3) as the baseline to push against. Non-spherical shapes test Slice 1's "axisymmetric" assumption inside the *positive*-result Fuchs corner (rather than the negative-result FH corner). **Deferred Session 23: MATLAB toolchain unavailable in current environment.** Will reactivate if MATLAB access is acquired or a Python port of Warp Factory's TOV+EC pipeline is undertaken. Effort: 1-2 sessions of MATLAB sweeping on top of existing infrastructure.

2. **Task 2D.11 Phase 3 (multi-mode FH-style $\vec A$).** Phases 1+2 (axisymmetric $A_\phi(R, Z)$, Cartesian constant-amplitude $\vec A$) returned negative across 162 + 81 preview points at the canonical FH anchor ([`FELL_HEISENBERG_VORTICAL_NOTES.md`](FELL_HEISENBERG_VORTICAL_NOTES.md)). Phase 3 — letting each Cartesian component carry its own FH-style $\Pi$-modulated structure rather than a shared Gaussian envelope — was scaffolded but never started; it is the *only* genuinely-untouched relaxation of the irrotational $\vec N = \nabla \phi$ assumption that drives the §9 "all wall, no interior" pathology. Low expected positive yield (the two existing negatives are structurally distinct), but the only one of the FH-internal questions that has not been hit in some form. Effort: ~1 session new sweep module + ~1 session HF Jobs cpu-xl preview.

3. **Task 2D.5e Z-axis-symmetry plan-B.** §12.8 of [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) describes the un-attempted fallback: assume the global slack minimum sits on the Z axis (where off-diagonal $S_{ij}$ vanish by FH symmetry) and reduce to symbolic 1-D minimisation, sidestepping the SymPy `det()` wall. Pre-flight verification needed: `fell_heisenberg_horizon/leaderboard.csv` reports `N_max_pos = (-0.5, 0, 0)` (off-axis) — yellow flag, not a blocker. Would deliver a closed-form expression for the boundary along one-dimensional cuts even if not in full 5-D. Effort: ~1 session symbolic + verification.

4. **Garattini-Zatrimaylov 2025 reproduction.** Bubble at Hubble velocity in de Sitter satisfies *averaged* WEC/NEC; our Slice 5 McVittie pipeline is already set up; adding a bubble on top and computing the averaged conditions is a focused extension. Listed as a Risk Register entry rather than a roadmap task; would relax assumption 5b of the load-bearing table. **Effort: 1-2 sessions.**

5. **Path 2B (Casimir / boundary-mode QFT).** Less urgent than at Session 11 — the FH static-slice strict-pass result removed the original Path-2B motivation ("need a quantum source for the negative sliver"), and Session 17 anchored the result against three external no-go literatures without invoking a quantum supplement. Still the right route for the *acceleration* and *dynamic-buildability* questions, and for the all-wall-no-interior pathology if it is a deep classical structural feature. Tasks 2B.1–2B.5 in [`ROADMAP.md`](ROADMAP.md); gated on the spin-2 obstruction assessment (Task 2B.8, never started). **Effort: large; largest scope.**

6. **Slice 4b (Krasnikov 2003 hybrid quantum/classical wall).** ~~Reproduce Krasnikov's $10^{-3}$ g dihedral-portal + Van Den Broeck pocket and ask whether adding a Fuchs-class classical shell can eliminate the residual mg of QI-bounded negative energy.~~ **Closed Session 23 (NEGATIVE)** — see Session 23 entry above and [`KRASNIKOV_HYBRID_NOTES.md`](KRASNIKOV_HYBRID_NOTES.md). Required supplement $\ge 10^{31}\times$ the Krasnikov 2003 budget across the full ($\eta,\epsilon,n$) grid; the mg-scale tail cannot serve as a quantum patch for the classical Krasnikov-tube wall.

7. **Slice 6b (computational $f(R)$).** Build a 4th-order PDE solver. Significant new infrastructure. **Effort: large.**

8. **Phase 2E landscape items 2E.1-2E.5.** Each is a deliberately-deferred relaxation with explicit reopening criteria recorded in [`ROADMAP.md`](ROADMAP.md) Phase 2E (genuinely time-dependent inflate-then-coast; modified-gravity computational follow-through; quantum/semiclassical sources beyond AECs; multi-mode vortical $\vec A$ joint with anisotropic $\Pi$ and non-trivial topology; higher-dimensional / active-matter Krasnikov variants). Not a workplan; a checkable landscape map.

### Closed since Session 14c (do not re-open absent the listed reopening criteria):

- **Slice 4b / Task 2A.13b (Krasnikov hybrid quantum/classical wall)** — closed Session 23; **required supplement $\ge 10^{31}\times$ Krasnikov 2003 mg budget** across all 360 ($\eta,\epsilon,n$) sweep points; three verification gates pass; reopening trigger would be a model in which the Krasnikov-tube wall is replaced by a different classical wall whose pointwise DEC deficit drops by $\ge 30$ OoM. See [`KRASNIKOV_HYBRID_NOTES.md`](KRASNIKOV_HYBRID_NOTES.md).
- **Task 2D.5f (full $N_{\rm pts}=129$ re-sweep)** — closed Session 22; **6240/10080 strict-pass**; +5.8% above §11.6 extrapolation; no 2D.16 reopening trigger.
- **Task 2D.7 (FH single-bubble + double-bubble CTC analysis)** — closed Session 17 Phase C; **98.3% of strict-pass host CTC region**; double-bubble destroys both passenger zones via missing decay envelope.
- **Task 2D.8 (independent FH pipeline cross-check)** — closed Session 17 Phase E; **9/9 anchors A-grade** via Wolfram 14.3 + xAct 1.3.0 + xCoba 0.8.6; median rel-diff $\sim 2 \times 10^{-6}$.
- **Task 2D.9 (B-M source-matter classification)** — closed Session 17 Phase B; **Class III geometric + non-isotropic + static** across 8 strict-pass anchors; outside every B-M positive-result pathway.
- **Task 2D.10 (asymptotic-matching residual)** — closed Session 17 Phase F (asymptotic half) + Session 17 Phase C (double-bubble half); **no asymptotic decay envelope ($\langle |\vec N| \rangle \sim 15.5$ on box-edge sphere across $L \in \{12, 16, 20, 24\}$); canonical $M_{\rm box} = 1850$ puts $r_h = 3700 \gg$ all box radii**.
- **Task 2D.12 (VIQ post-processing)** — closed Session 17 Phase A; **$E_{\rm neg}=0$ universally; passenger volume $= h^3$ universally; $M_{\rm passenger}/V_{\rm passenger} = 44$–$98\times$ (median 76×)**.
- **TRUST_AUDIT #3 (Warp Factory + Fuchs Fig. 10)** — closed Session 18; in-shell NEC=WEC=DEC=SEC=1.0000; concurrent 2A.9b κ-bracket $(4.17, 5.83]$.
- **Phase 3.1, 3.2** — closed Session 19; standard Alcubierre at $v=c$ matches Pfenning-Ford expectations; 27-cell Fuchs $\beta_{\max}$ surface confirms scaling-law form with 18%-spread $\kappa$.
- **Tier A figures programme** — closed Session 20; [`figures/plot_figures.py`](figures/plot_figures.py) seven subcommands; PNGs mirrored into [`webpage/assets/figures/`](webpage/assets/figures/).

### Outstanding admin (rolled forward Sessions 20/21/22):

- Publish GitHub Release at <https://github.com/bshepp/alcubierre/releases/new> for tag `v0.1.0` (commit `cba795f`) to trigger the Zenodo webhook and mint a DOI for [`CITATION.cff`](CITATION.cff). Manual step; requires the project owner.

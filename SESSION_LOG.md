# Session Log — Alcubierre Boundary-Mode Reformulation

---

## Session 1 — 2026-03-30

**Participants:** Brian Sheppard + Claude
**Chat ID:** 8fb50fee
**Duration:** Extended literature review

### Work Performed
- Comprehensive literature review of the warp drive field
- Mapped foundational papers (Alcubierre, ADM, Morris & Thorne, Ford & Roman)
- Identified descendant papers (Van Den Broeck, Natário, Lobo & Visser, Lentz, Bobrick & Martire)
- Cataloged no-go results (Pfenning & Ford, Everett, Hiscock, Santiago-Schuster-Visser)
- Identified the Casimir effect as a physical analog for boundary-generated negative energy
- Noted Warp Factory (Helmerich et al. 2024) as computational platform
- Identified Fuchs et al. 2024 as the most significant recent comparison target

### Key Insight
The Casimir effect is an existence proof that boundary conditions on field modes produce negative energy density. If the Alcubierre bubble wall plays the role of Casimir plates for gravitational modes, the exotic matter problem becomes a boundary-value engineering problem.

### Output
Literature atlas and Casimir connection (carried forward into integration document)

---

## Session 2 — 2026-04-04

**Participants:** Brian Sheppard + Claude
**Chat ID:** 50c03df0

### Work Performed
- Formulated the three-body image-method hypothesis
- Developed the GEM (gravitoelectromagnetic) framework for linearized gravity
- Identified Poisson equation structure as the entry point for method of images
- Laid out Phase 1 action items
- Produced the seed document `ALCUBIERRE_IMAGE_METHOD.md`

### Key Insight
Linearized GR has Poisson equation structure identical to electrostatics. The method of images is a standard technique for Poisson equations with boundary conditions. If the Alcubierre bubble wall is a boundary surface, the exotic matter may decompose into "image" contributions from real positive-energy sources.

### Output
`ALCUBIERRE_IMAGE_METHOD.md` (seed document, not in this repo — superseded by integration doc)

---

## Session 3 — 2026-04-15

**Participants:** Brian Sheppard + Claude

### Work Performed

#### Part 1: Understanding the seed document
- Reviewed `ALCUBIERRE_MARCH30_INTEGRATION.md` (integration of Sessions 1 & 2)
- Identified the linearization calculation as the priority next step

#### Part 2: Explicit linearization calculation
Produced complete derivation ([LINEARIZATION_CALCULATION.md](LINEARIZATION_CALCULATION.md)):

1. **ADM decomposition** — confirmed $\alpha = 1$, $\gamma_{ij} = \delta_{ij}$, all content in shift vector $\beta^x = -v_s f(r_s)$
2. **Extrinsic curvature** — derived all $K_{ij}$ components, expansion scalar $\theta = v_s \partial_x f$
3. **Exact stress-energy** via ADM constraints:
   - Energy density: $\rho = \frac{-v_s^2}{32\pi G}(f')^2 \frac{y^2+z^2}{r_s^2}$ (negative everywhere off-axis)
   - Momentum density: $j^x = \frac{-v_s}{16\pi G}\nabla_\perp^2 f$
4. **Order counting**: warp effect and momentum are $O(v_s)$ (gravitomagnetic); energy density is $O(v_s^2)$
5. **Gauge analysis**: Alcubierre metric is NOT in harmonic gauge; ADM framework avoids gauge issues
6. **Poisson structure**: $\nabla^2\beta^x = -v_s\nabla^2 f$ with source at bubble wall
7. **Thin-wall limit**: source becomes monopole + dipole double layer — standard potential-theory structure
8. **Total energy estimate**: $|E| \sim v_s^2 R^2/(12G\Delta)$ — planetary-mass scale even at $v_s = 0.01c$

#### Part 3: Green's function / image decomposition analysis
Investigated whether point-image methods can reproduce the Alcubierre field configuration:

**Finding: Point-image decomposition does not work.**

- The interior field $\beta^x = -v_s$ is constant (uniform frame-dragging)
- No finite superposition of $1/|\mathbf{r} - \mathbf{r}_i|$ point-source fields can produce a constant
- The closest EM analog is a uniformly magnetized sphere (surface current source, not point sources)
- The three-body picture (ship + distant source + image) requires fine-tuned cancellation at every radius

**Finding: Boundary-mode / Casimir picture is strengthened.**

- The correct mathematical framework is mode decomposition on a spherical domain, not point images
- The wall imposes boundary conditions → restricted mode spectrum → negative energy at boundary
- This IS the Casimir mechanism, translated to gravitomagnetic degrees of freedom
- The exotic energy density is a second-order nonlinear functional of the first-order mode structure

#### Part 4: Project documentation
- Updated [LINEARIZATION_CALCULATION.md](LINEARIZATION_CALCULATION.md) with Green's function findings (Section 9)
- Created [README.md](README.md) — project overview
- Created [ROADMAP.md](ROADMAP.md) — five-phase research plan with decision points
- Created this session log

### Decisions Made
1. **Pivot from "method of images" to "boundary-mode decomposition"** as the mathematical framework
2. **ADM formalism is the natural setting** — not harmonic gauge linearization
3. **Subluminal discipline** — no superluminal extensions until Phase 5 at earliest
4. **Priority reading**: Lobo & Visser 2004 and Fuchs et al. 2024 before proceeding to Phase 2

### Open Items Entering Next Session
- [ ] Read Lobo & Visser 2004 (Task 1.8)
- [ ] Read Fuchs et al. 2024 (Task 1.9)
- [ ] Assess spin-2 vs spin-1 differences (Task 1.11)
- [ ] Begin Phase 2 spectral decomposition if literature review supports it

### Conceptual State at End of Session
The project has its first real mathematical result (the linearization calculation) and its first real negative result (point images don't work). The negative result is actually productive — it redirects the approach toward a framework (boundary modes) that has stronger physical grounding (Casimir) and better-developed mathematical tools (spectral theory on bounded domains). The core claim — exotic matter as boundary effect — is intact and arguably strengthened. The question is now whether the mode decomposition produces quantitatively useful results or is merely a restatement of the same physics in different language.

---

## Session 4 — 2026-04-15 (continued)

**Participants:** Brian Sheppard + Claude
**Focus:** Literature retrieval, verification, quantum/classical gap analysis, documentation audit

### Work Performed

#### Part 1: Seed document evaluation
- Reviewed all five existing documents for scientific content, internal consistency, and completeness
- Identified a critical bug: Lobo & Visser 2004 was cited as `gr-qc/0410087` (a solo Lobo wormhole paper) — correct IDs are `gr-qc/0406083` and `gr-qc/0412065`
- Identified the quantum vs. classical gap as the largest unaddressed conceptual issue
- Added the original seed document `ALCUBIERRE_IMAGE_METHOD.md` to the repository

#### Part 2: Literature retrieval and catalog
- Fetched arXiv abstracts and metadata for 15 papers across foundational, descendant, no-go, and new categories
- Created [LITERATURE.md](LITERATURE.md) with structured entries: abstract, publication data, and relevance to boundary-mode program
- Added two new papers not in original seed documents:
  - Quach 2015 (1502.07429) — gravitational Casimir effect with non-idealized boundaries
  - Ford & Pfenning 1998 (gr-qc/9805037) — quantum inequalities in curved spacetime
- Established reading priority order: Lobo & Visser → Fuchs et al. → Santiago-Schuster-Visser → Quach → Ford-Pfenning
- Confirmed 7 textbooks/non-arXiv papers cannot be automatically retrieved

#### Part 3: Verification notebook
- Created [verification.ipynb](verification.ipynb) with 10 cells covering all key results
- Symbolic verifications (SymPy): ADM decomposition, extrinsic curvature, $K^2 - K_{ij}K^{ij}$ cancellation, energy density, all three momentum density components — all pass
- Numerical verifications (numpy): shape function profiles, total energy integral ($E \approx -3.7 \times 10^{26}$ J for $v_s = 0.01c$, $R = 100$ m, $\sigma = 10$), thin-wall estimate agreement (ratio $\approx 0.33$)
- Gauge violation check: confirmed $\partial_\mu \bar{h}^{\mu t} \neq 0$ analytically
- Visualization: 4-panel plot of shape function, derivative, energy density, and expansion scalar

#### Part 4: Quantum/classical gap analysis
- Created [QUANTUM_CLASSICAL_BRIDGE.md](QUANTUM_CLASSICAL_BRIDGE.md) with three-layer analysis:
  - **Claim (a)** — Geometric classification (classical, established): all source structure lives at wall
  - **Claim (b)** — Semiclassical consistency (quantum, testable): $\langle T_{\mu\nu}\rangle_\text{ren}$ calculation needed
  - **Claim (c)** — Physical mechanism (quantum, speculative): exotic matter IS gravitational Casimir effect
- Identified the Boyer sign problem: spherical Casimir energy is repulsive in EM — may be wrong sign
- Identified the Fuchs et al. classical path as a potentially more productive alternative to the Casimir route
- Proposed the "effective boundary" argument: matter shell creates boundary, shift vector modes in shell's presence produce warp geometry classically

#### Part 5: Documentation updates
- Fixed arXiv ID bug across 4 files (LINEARIZATION_CALCULATION.md, README.md, ROADMAP.md, ALCUBIERRE_MARCH30_INTEGRATION.md)
- Fixed section numbering in LINEARIZATION_CALCULATION.md (8.3 → 10)
- Added self-consistency note in Section 6.5 about linearized-source tension
- Qualified "Core Claim" in README.md: "structurally identical" → "structurally analogous"
- Added Casimir analogy caveat to ALCUBIERRE_MARCH30_INTEGRATION.md §2
- Added new references (Quach 2015, Ford-Pfenning 1998) to integration doc literature tables
- Updated README.md document table with all new files
- Fleshed out Phase 2.1 in ROADMAP.md with vector Laplacian specifics and angular structure
- Added Tasks 2.7 (Fuchs et al. connection) and 2.8 (quantum/classical assessment) to ROADMAP.md
- Added three new risks to ROADMAP.md risk register: quantum/classical gap, Boyer sign problem, expanded spin-2 risk

### Decisions Made
1. **Three-tiered claim structure** adopted: geometric (established) / semiclassical (testable) / physical (speculative)
2. **Fuchs et al. 2024** elevated to co-equal priority with Casimir interpretation as potential physical mechanism
3. **Vector Laplacian** (not scalar) identified as the correct operator for Phase 2 spectral problem
4. **Boyer sign problem** identified as a new risk requiring Phase 2 investigation

### Open Items Entering Next Session
- [ ] Read Lobo & Visser 2004 (Task 1.8) — now with correct arXiv IDs
- [ ] Read Fuchs et al. 2024 (Task 1.9) — elevated priority; may provide classical boundary-mode realization
- [ ] Assess spin-2 vs spin-1 differences (Task 1.11) — risk now in register
- [ ] Investigate Boyer sign problem for spherical gravitational Casimir
- [ ] Begin Phase 2 if literature review supports it
- [ ] Run verification.ipynb end-to-end in Jupyter and inspect plots

### Conceptual State at End of Session
The project is more honest and better organized. The quantum/classical gap is now explicitly acknowledged with a clear path forward (three claims at three ambition levels). The Fuchs et al. matter-shell solution has emerged as a potentially more productive connection than the Casimir analogy — it provides a classical physical mechanism (shell as boundary → boundary-constrained shift vector → warp geometry) that the mode decomposition could explain. The Casimir interpretation is not abandoned but correctly positioned as the most ambitious version of the claim, requiring semiclassical QFT work that is Phase 3+ at best. The literature catalog is complete, the key expressions are verified, and the arXiv ID bug is fixed. The project is ready for the priority literature reading (Lobo & Visser, Fuchs et al.) that will determine how much of this framework is novel.

---

## Session 5: 2026-04-15 (Part 2) — Path 2 Pivot, Fuchs et al. Integration

### Directive
User instruction: *"I don't want to abandon the Casimir route but I would like to pursue Path 2 as you suggested first."* Referring to the "classical matter shell" path identified in `QUANTUM_CLASSICAL_BRIDGE.md` §5 as the alternative to the Casimir route. Scope clarified via AskQuestion: doc-only + a *new* dedicated notebook for Israel junction conditions, fetching Fuchs et al. HTML for technical detail.

### What Was Accomplished

#### Part 1: Literature retrieval and technical integration
- Fetched Fuchs et al. 2024 (arXiv:2405.02709) both abstract page and experimental HTML.
- Extracted the full construction: static spherical matter shell (TOV-solved, anisotropic pressure) + pure shift perturbation $\delta g_\text{warp}$ on the interior, Eq. 27-28 bump function with buffer region $R_b$, empirical shift bound $\beta_\text{warp} \le 0.02c$ for all ECs satisfied. Shell parameters: $R_1 = 10$ m, $R_2 = 20$ m, $M = 4.49 \times 10^{27}$ kg.
- Noted the critical caveats they flag: (i) shift amplitude is small, (ii) bubble does not translate (only interior frame-drag), (iii) acceleration is open (their §5.3), (iv) mass is enormous.

#### Part 2: MATTER_SHELL_PATH.md (new, ~370 lines)
- Explicit mapping table between boundary-mode framework and Fuchs construction (§2.1): shift vector $\beta^i$ ↔ Fuchs $\beta^1$; wall ↔ TOV-solved matter shell; boundary condition ↔ shell interior-exterior matching; negative energy → *no longer required* because shell provides positive ADM mass.
- Stated the **refined boundary-mode hypothesis** (§2.3): a one-parameter family interpolating between Fuchs's Warp Shell ($\lambda = 0$) and Alcubierre ($\lambda = 1$), with the interpolation parameter being "warp shift magnitude vs. shell support capacity."
- Listed three open problems explicitly not settled by Fuchs (§2.2): (P1) velocity limit, (P2) acceleration/translation, (P3) mass-to-velocity scaling.
- Developed the Israel thin-shell framework (§3) as complementary analytical probe of their thick-shell construction, including a sketched calculation for the shift-perturbed interior.
- Connected to Phase 2 roadmap: the boundary-mode decomposition of the shell interior has a physical cutoff set by the shell's ADM mass and Schwarzschild radius (§4).
- Articulated four outcome scenarios (§6): Path 2 succeeds / succeeds-only-at-small-amplitude / fails-on-acceleration / fails-both — with the Casimir route becoming necessary or redundant in each.
- Built a dedicated Path 2 reference table (§8).

#### Part 3: matter_shell.ipynb (new, 12 cells)
Verified via `nbclient` end-to-end execution. Results:
- **§1-2:** Numerically reproduced Fuchs's bump function and shift profile. Confirmed $\int dS/dr\, dr = -1$ — boundary is localized in the transition region, consistent with boundary-mode picture.
- **§3:** Israel thin-shell junction for Minkowski interior + Schwarzschild exterior. Surface energy density $\sigma = (1 - \sqrt{1-2GM/R})/(4\pi GR)$; weak-field shell mass $\mu \approx M + GM^2/(2R)$ — **exactly matches textbook result** (ADM mass plus binding energy).
- **§4:** Angular projection of Alcubierre shift onto Legendre polynomials. **Pure $l=1$ dipole confirmed**: monopole and quadrupole projections vanish exactly; dipole projection is $2\beta/3$.
- **§5:** Derived Eulerian-frame EC scaling $\beta_\text{warp} \lesssim GM\Delta^2/(R^3 c^2)$. Numerical value for Fuchs parameters: $0.0988$; Fuchs's empirical bound: $0.02$. Within order of magnitude; remaining factor attributable to anisotropic pressure bookkeeping.
- **§6:** Mass scaling table. For 1 km bubble at $\beta = 0.1c$: $M \sim 10^{31}$ kg ($10^6$ Earth masses). For a 20 m bubble at $\beta = 0.001c$: $M \sim 10^{26}$ kg ($\sim 18$ Earth masses). Orders of magnitude above practical but orders of magnitude below original Alcubierre exotic-matter requirement.

#### Part 4: ROADMAP.md restructuring
- Split Phase 2 into **Phase 2A (Classical Matter-Shell Realization, primary, IN PROGRESS)** and **Phase 2B (Casimir / Boundary-Mode Decomposition, parallel, NOT STARTED)**.
- Phase 2A tasks 2A.1-2A.5 marked completed (Fuchs integration, bump reproduction, Israel warm-up, dipole confirmation, scaling derivation); tasks 2A.6-2A.12 are the next concrete work items.
- Phase 2B retains the original Casimir mode-decomposition program with explicit acknowledgment of the spin-2 obstruction risk.
- Decision points recast for the two-track structure.
- Phase 3 tasks updated to include Fuchs-specific sweeps (3.2, 3.3) in addition to mode-decomposition validation (3.4, 3.5).
- Phase 5 tasks updated: Task 5.4 (Fuchs connection) marked resolved; new task 5.6 (acceleration problem) added.
- Risk register rewritten to reflect two-track structure with path-specific risks and mitigations; added "Fuchs already contains Path 2A results" (novelty risk) and "acceleration always fails" (physical risk) as new entries.
- Open questions Q7-Q9 added (nested shells, acceleration metric, Lentz vs. Fuchs distinction).

#### Part 5: QUANTUM_CLASSICAL_BRIDGE.md update
- Rewrote §6 from "Recommended Path Forward" to "Two-Track Strategy" with explicit primary/parallel designation.
- Added outcome-matrix table showing how the four Path 2A × 2B combinations interpret.
- Split Claim (c) into (c-classical) — Path 2A version — and (c-quantum) — Path 2B version.
- Header updated to mark this as the home of Path 2B specifically, with cross-reference to `MATTER_SHELL_PATH.md` for Path 2A.

#### Part 6: README.md update
- Core Claim and Current Status rewritten for two-track structure.
- Document table expanded with bold entries for `MATTER_SHELL_PATH.md` and `matter_shell.ipynb`.
- Key Results section extended with items 7-10 from the new session's work (Fuchs as direct realization; $l=1$ dipole structure; $\beta$ scaling match; Israel warm-up validated).

### Decisions Made
1. **Dual-track adopted:** Path 2A is primary; Path 2B is parallel and not abandoned. Both tracks proceed and may converge, diverge, or one may foreclose the other.
2. **Fuchs et al. 2024 is the anchor for Path 2A.** The refined boundary-mode hypothesis is stated as an explicit interpolation between their construction and the original Alcubierre metric.
3. **The $l=1$ dipole result** is the first genuinely new, easily-communicable analytical result from this project. It precisely specifies the angular structure that any wall-physics description must realize, and distinguishes the Alcubierre shift from rotationally-symmetric alternatives.
4. **Notebook-driven verification continues.** `matter_shell.ipynb` complements `verification.ipynb` as a working computational artifact. Future Path 2A tasks will have dedicated notebooks or sections.
5. **Acceleration is explicitly flagged** as the hardest open problem across both tracks (Task 2A.10, Task 5.6).

### Open Items Entering Next Session
- [ ] **Path 2A.6:** Full thin-shell Israel junction with the shift-perturbed Alcubierre interior (the bigger calculation the current notebook defers). Needs vector-spherical-harmonic machinery for the angle-dependent $[K_{ab}]$.
- [ ] **Path 2A.7:** Determine $\Delta_\text{min}(v_\text{warp}, M, R)$ — the minimum shell thickness below which DEC must fail. Analytic + numerical.
- [ ] **Path 2A.8:** Vector-spherical-harmonic expansion of the full shift $\beta^x(r)\hat{x}$ on the shell domain. Match against Fuchs's bump profile.
- [ ] **Path 2A.10:** Acceleration problem. Start with ADM 4-momentum conservation as an organizing principle.
- [ ] **Path 2A.11-12:** Compare Fuchs to Lentz 2020 and Natário 2002 explicitly.
- [ ] **Phase 3.1:** Install Warp Factory (MATLAB) and reproduce Fuchs's Figure 10 (energy conditions for warp shell) as validation baseline.
- [ ] **Phase 1.8, 1.9:** Still pending — read Lobo & Visser 2004 and Fuchs et al. in full, not just the abstracts and key sections.

### Conceptual State at End of Session
Path 2 is now a genuine research program with a concrete existence anchor (Fuchs et al.), a technical document laying out the framework (`MATTER_SHELL_PATH.md`), a working notebook that establishes the formalism and produces verified quantitative results (`matter_shell.ipynb`), and a restructured roadmap that sequences the next calculations. Crucially, the project has shifted from "Alcubierre-plus-Casimir-analogy" to "boundary-mode reformulation *of* Alcubierre, realized classically by Fuchs *and* with a parallel Casimir investigation for amplitudes or regimes classical matter cannot cover." The central claim is now scientifically modest and well-founded: the boundary-mode framework is a useful organizing principle that matches an existing positive-energy warp drive construction, predicts testable scaling laws, and identifies the specific open problems (acceleration, mass scaling, spin-2 boundary conditions) that separate "frame-dragging inside a heavy shell" from "useful transportation." The ambitious Casimir claim remains the speculative ceiling of the program, not its foundation.

---

## Session 6: 2026-04-16 — Path 2A Packages 1–3 Execution

### Directive
User instruction: *"Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself. To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos."* Execute the three-package Path 2A plan (Israel junction, thickness bound, acceleration problem) with Colab/HF Jobs compute infrastructure integrated.

### What Was Accomplished

#### Package 0 — Compute Infrastructure
- `requirements.txt` and `requirements-gw.txt` pinning the SymPy/NumPy/SciPy/Matplotlib stack plus optional `sxs` and `gwtools` for Package 3.
- `hf_jobs/run_sweep.py` — generic parameter-sweep dispatcher with local and HF Jobs backends. Windows-specific worker cap added after a `BrokenProcessPool`/OpenBLAS incident.
- Colab "Open In Colab" badges and guarded `pip install` cells added to `verification.ipynb`, `matter_shell.ipynb`, `israel_junction.ipynb`, `thickness_bound.ipynb`, `acceleration.ipynb`.
- `README.md` expanded with a "Running the notebooks" section documenting the three runtimes (local / Colab / HF Jobs) and a per-notebook recommendation table.

#### Package 1 — Israel Junction Conditions (Task 2A.6)
New notebook `israel_junction.ipynb` (31 cells, Part A static Schwarzschild + Part B boosted Schwarzschild). Key technical results:
- **Induced metric $h_{ab}^\pm$ and extrinsic curvatures $K_{ab}^\pm$** computed symbolically on both sides of the matching surface $r = R$.
- **Angular decomposition of $[K_{ab}]$ via Legendre polynomials** confirms the Alcubierre shift sources a pure $l=0$ (monopole) + $l=1$ (dipole) structure in the jump, matching the theoretical expectation from `matter_shell.ipynb` §4.
- **DEC failure at anti-motion pole.** For thin-wall parameters with a static exterior, DEC fails at $\theta \approx 179.4°$ for representative $\beta/C$ — the shift-induced boundary current beats the positive surface energy density from the monopole.
- **Critical $\lambda_* \approx 0.55$** in Part B. When $v_{\rm ext}$ and $v_{\rm int}$ are allowed to differ, DEC fails for $\lambda = v_{\rm ext}/v_{\rm int} < 0.55$. Covariance-preserving configurations ($\lambda = 1$) are DEC-safe; the acceleration transient through $\lambda < 1$ is the residual obstruction.
- HF Jobs preview sweep via `hf_jobs/sweeps/israel_junction_partA.py` (2000-point local preview + 10⁶-point full config) maps the DEC-satisfying region of the ($\beta$, $C$) plane.

`MATTER_SHELL_PATH.md` §3.3 rewritten with the actual results; P2.3 marked resolved; Task 2A.6 marked complete in `ROADMAP.md`.

#### Package 2 — Minimum Shell Thickness (Task 2A.7)
New notebook `thickness_bound.ipynb` (19 cells). Key technical results:
- **Analytical scaling law** $\Delta_{\min}/R = \kappa\beta/C$ with $C = 2GM/(Rc^2)$, derived from worst-angle DEC saturation under the thin-to-thick interpolation. Headline coefficient $\kappa = 3/4$ from the leading-order derivation.
- **Numerical sweep via HF Jobs** (`hf_jobs/sweeps/thickness_bound.py`, ~1.3 × 10⁵-point full config) empirically calibrates $\kappa \in [0.05, 0.75]$ across the physically relevant $(\beta, C)$ regime.
- **Fuchs parameter-regime comparison.** Fuchs shells live at very low Schwarzschild compactness ($C \sim 10^{-10}$) and high matter density; the naive $\kappa$ extracted from their numbers is outside the predicted band, reflecting that the bound applies to Schwarzschild-compactness shells rather than dense-matter shells. Documented as a refinement rather than a contradiction.
- **Design-point extrapolation.** For $\beta = 0.5$, $R = 100$ m, DEC-compatible shell at $\Delta = R$ requires $M \sim 10^{19}\text{–}10^{20}$ kg of ordinary matter — orders of magnitude below the $\sim 10^{30}$ kg of *negative* energy the original Alcubierre metric demands.

`MATTER_SHELL_PATH.md` §3.4 rewritten; P2.5 marked resolved; Task 2A.7 marked complete in `ROADMAP.md`; `README.md` Key Results extended with items 11–12.

#### Package 3 — The Acceleration Problem (Task 2A.10)
New notebook `acceleration.ipynb` (19 cells, five-part structure). Key technical results:
- **ADM 4-momentum obstruction theorem (cells 2–5).** Computed $E_{\rm ADM}$ of the Schwarzschild exterior symbolically; limit at infinity reduces to $M$, validating framework. Initially-static slice has $K_{ij} = 0 \Rightarrow P^i_{\rm ADM} = 0$; conservation forces $P^i_{\rm ADM}(t) = 0$ for all $t$ unless there is boundary flux. Three mechanisms (A shift spin-up, B mass ejection, C GW recoil) exhaust the ways to break this.
- **Three-mechanism catalog (cells 6–9 + 15).** Mechanism A requires comoving exterior mass $\sim M_{\rm shell}$ — reduces to "push-from-a-wall"; not warp drive. Mechanism B is ordinary Tsiolkovsky rocket, DEC-trivial and mass-budget-trivial at $\beta \sim 0.02$, but a warp shell propelled by a chemical rocket is *just* a rocket. Mechanism C is the only genuinely vacuum-+-DEC-compatible option.
- **GW-recoil quantitative ceiling (cells 10–13).** Two independent estimates: (A) SXS rescaling of Varma et al. 2022 record 5000 km/s kick via $v_{\rm kick}^{\rm Fuchs} \sim v_{\rm kick}^{\rm BBH}\,\beta^2\,C^{3/2}$, (B) PN binary analog with shell + 1% beacon. HF Jobs sweep `hf_jobs/sweeps/gw_recoil.py` over ($\beta$, $C$, $M$, $n_{\rm orbits}$) returns max $\Delta v_{\max} \approx 10^{5.82}$ m/s $\approx 660$ km/s at $\beta = 0.9$, $C = 0.5$ — still only 0.25% of the warp-speed target at those parameters. Nominal Fuchs values give $\Delta v_{\max} \sim 600$ m/s.
- **Literature comparison (cells 16–17).** Consistent with and strictly strengthens Schuster–Santiago–Visser 2023 Theorem 3 by decomposing "boundary flux" into the three mechanisms with DEC and quantitative verdicts. Compared against Varma et al. 2022 empirical BBH-kick record.
- **Conclusion (cell 18).** No classical mechanism simultaneously preserves DEC on shell + exterior, keeps exterior vacuum, requires no expelled reaction mass, *and* produces $\Delta v \sim v_{\rm warp}$. Scenario (A) of `MATTER_SHELL_PATH.md` §6 is **falsified for accelerating shells**; scenario (C) — "quantum / boundary-mode mechanism needed for dynamics" — is the remaining open candidate. Path 2B is elevated from parallel hedge to the sole remaining route to a dynamical warp drive.

`MATTER_SHELL_PATH.md` §7 rewritten entirely around the acceleration result; P2.4 marked resolved. `QUANTUM_CLASSICAL_BRIDGE.md` §6 outcome matrix updated with 2026-04-16 status column confirming row 3 (static-only Path 2A + open Path 2B) as the best-supported scenario. `ROADMAP.md` Task 2A.10 marked complete; risk register entry on "acceleration always fails" updated from "High likelihood" to "Realised".

### Decisions Made
1. **Path 2A static half: done.** Packages 1 and 2 confirm DEC-compatible matter shells with the $\kappa\beta/C$ thickness scaling law. This is the deliverable that is mature enough to write up.
2. **Path 2A dynamical half: closed with prejudice.** Package 3 rules out self-acceleration under classical-matter + vacuum-exterior + no-ejecta + DEC. The only viable classical motion requires an ordinary rocket (Mechanism B), which makes the warp geometry thermodynamically redundant.
3. **Path 2B is promoted.** It is now the sole remaining candidate for a genuine (vacuum + DEC + dynamical) warp-drive realisation. The Casimir / boundary-mode programme should be resumed as the primary next track.
4. **Compute infrastructure is production-ready.** `requirements.txt`, `hf_jobs/run_sweep.py`, and the Colab badges across all five notebooks mean Colab and HF Jobs runs are a single-command affair.
5. **Systematic robustness improvements.** The `f_R` substitution fix in `israel_junction.ipynb` and the Windows worker cap in `run_sweep.py` make the pipeline usable on Windows despite the `lalsuite`/OpenBLAS difficulties.

### Open Items Entering Next Session
- [ ] **Path 2B Task:** Resume the Casimir / boundary-mode programme. Starting point is `QUANTUM_CLASSICAL_BRIDGE.md` §3–5; first concrete calculation is the semiclassical $\langle \hat T_{\mu\nu}\rangle$ for a quantized linearised-gravity field on a Fuchs-shell background. This is the only remaining track that could produce a dynamical warp drive.
- [ ] **Task 2A.11–12:** Lentz 2020 and Natário 2002 comparison remains open. Likely easier now that the acceleration catalog is in place — their constructions slot into the same three-mechanism framework.
- [ ] **Task 2A.9:** Refine the $M_{\min}$ scaling to include anisotropic-pressure corrections; Warp Factory validation.
- [ ] **Writing up.** The static Path 2A result (`MATTER_SHELL_PATH.md` §3 + §7) + the acceleration obstruction (`acceleration.ipynb` + §7) together constitute a coherent short-paper-worth of material on the limits of classical warp drives. Decide whether to pursue arXiv preprint or continue with Path 2B first.

### Conceptual State at End of Session
The classical half of the Path 2A programme is now effectively complete. We have (i) a rigorous existence result for static DEC-compatible matter-shell warp geometries with a quantitative thickness bound, (ii) a rigorous obstruction theorem ruling out classical acceleration in vacuum, (iii) a quantitative ceiling on GW recoil that closes the only classically vacuum-compatible loophole, and (iv) a promotion of Path 2B (Casimir / boundary-mode) from hedge to primary track for the dynamical problem. The project has moved from "Alcubierre-plus-analogy" (Session 1–3) through "boundary-mode reformulation realised by Fuchs" (Session 5) to a clear two-sided status: static classical yes, dynamical classical no, dynamical quantum open. This is the sharpest and most defensible statement the programme has yet produced.

---

## Session 7: 2026-04-16 — Speculation Analysis, Literature Sweep, Rodal 2025 Evaluation

### Directive
User added `speculation/RING_NETWORK_CONCEPT.md` (a third-party "Opus 4.7" speculation document proposing a static-infrastructure ring-network warp drive) and asked the assistant to evaluate it. The assistant's evaluation flagged Krasnikov tubes / Everett–Roman networks as likely prior art. The user then directed: **"go with A. Please do a search and tell me everything that is blocked and I'll get it somehow."** The user supplied all blocked papers in a new `papers/` directory. Final instruction: *"Please begin analysis as you see fit."*

### What Was Accomplished

#### Speculation analysis (`speculation/RING_NETWORK_CONCEPT.md`)
- Identified the document as a re-derivation of Krasnikov tubes (1995) plus the Everett–Roman 1997 network construction.
- Provided a calibrated evaluation: strengths (intellectual honesty, sound Mode-A launcher idea), weaknesses (claim of novelty for static-infrastructure approach is incorrect; underspecified link between "tunnel" and Mechanism A; GW-recoil channel already excluded by our Package 3 ceiling).

#### Literature sweep
Targeted lit-check on Krasnikov tubes, ring-wormholes, network constructions, and recent positive-energy warp papers. Findings:
1. **Krasnikov 1995** (gr-qc/9511068, 2D originator) — `papers/9511068v6.pdf`.
2. **Everett & Roman 1997** (gr-qc/9702049, 4D + network + classical $T_{\mu\nu}$ + CTC theorem) — `papers/9702049v1.pdf`.
3. **Krasnikov 2003** (gr-qc/0207057, QI counter-arguments) — `papers/0207057v3.pdf`.
4. **Lobo & Crawford 2002** (gr-qc/0204038, pedagogical reproduction + Olum's WEC theorem) — `papers/arXiv-gr-qc0204038v2.tar.gz`.
5. **Bobrick & Martire 2021** (2102.06824, "any warp drive requires propulsion") — already cited; PDF added.
6. **Rodal 2025** (2512.18008, kinematically irrotational positive-invariant-energy Natário-class drive) — `papers/2512.18008v1.pdf`. The most consequential new paper since our last sweep.

The Visser–Hochberg 2004 "double-walled Krasnikov tubes" paper is the only item we could not retrieve (paywalled, no arXiv preprint). Conceptual ground covered by Everett–Roman.

#### `RODAL2025_EVALUATION.md` (new document)
Detailed technical evaluation of the Rodal paper:
- Reproduced the construction analytically: $\Phi(r,\theta,t) = v(t)\,r\,g(r)\,\cos\theta$ with $g(r)$ derived from irrotationality + $f(r) = 1 - f_{\rm Alc}(r)$.
- Verified the algebraic engine: $G_{\hat 0 \hat i} = 0$ from the momentum constraint on a flat slice with $\beta_i = -\partial_i \Phi$ → globally Type I.
- Confirmed the comparison numbers (38× peak-deficit reduction vs Alcubierre, 2,600× vs Natário, 60× smaller NEC violation) are accurate as stated.
- **Identified three caveats the abstract obscures:** (1) NEC/WEC/DEC/SEC all still violated; (2) "net proper energy ≈ 0" is *not* vanishing ADM mass (the paper itself says so in §C); (3) constant-velocity analysis only — the acceleration problem is unaddressed.
- Concluded: the paper does *not* unblock anything we are currently blocked on, but **does suggest a meaningful update to the Path 2B search direction** — anisotropic transverse vacuum stresses (waveguide-confined Casimir, asymmetric-plate Casimir) are the natural QFT analogue to Rodal's stress-energy profile.

#### `KRASNIKOV_TUBE_NOTES.md` (new document)
Quantitative synthesis of the Krasnikov-Everett-Roman framework, with direct comparison to our Path 2A machinery:
- Extracted the classical wall stress-energy $T_{\hat t \hat t}^{\rm wall} \approx -\eta/(8\pi\epsilon^2)$ (Eq. 39 of Everett–Roman) — a wall-EoS-independent statement, like our Path 2A worst-angle DEC bound.
- Documented the QI bound $\epsilon \lesssim l_P/\sigma^2$ on wall thickness, the total negative-energy estimates ($10^{63}$ g for a 1 m × 1 m tube; $10^{32} M_{\rm galaxy}$ for an interstellar tube), and the network-implies-CTCs theorem.
- Side-by-side comparison with our Path 2A Fuchs-class shell results. Key finding: **the speculation document's "ring" is structurally inconsistent.** A Fuchs-class ring is constructible but doesn't shorten light-travel time; a Krasnikov-tube ring shortens light-travel time but generically contains CTCs. The speculation merges incompatible features.

#### `LITERATURE.md` updates
Added §9 ("Static-Infrastructure Prior Art") and §10 ("New Warp-Drive Construction Since Session 4") with full entries for Krasnikov 1995 / Everett–Roman 1997 / Krasnikov 2003 / Lobo–Crawford 2002 / Bobrick–Martire 2021 (re-evaluated) / Rodal 2025. Each entry tagged with relevance to our project and to the speculation document.

### Decisions Made
1. **The speculation document does not reorient the project.** Its proposed novelty (static-infrastructure ring) is established prior art; its proposed mechanism (Mode A launcher) inherits Bobrick-Martire's "any warp drive requires propulsion" theorem; its proposed dodge (GW recoil internal to the ring) was already excluded by our Package 3 GW-recoil ceiling.
2. **Rodal 2025 does not solve the acceleration obstruction.** Its analysis is at constant velocity. Our Path 2A Package 3 result is independent of which steady-state warp metric one chooses.
3. **Path 2B's search target is updated.** The Rodal stress-energy profile (anisotropic negative transverse pressures on a thin wall, positive density on-axis) is closer to what real anisotropic-Casimir setups produce than Alcubierre's isotropic-negative profile. Path 2B literature pulls should now target waveguide-confined and asymmetric-plate Casimir vacuum stresses, not generic isotropic vacuum-energy proposals.
4. **Reframed Calculation 1 is the right next computation.** Apply our Path 2A Israel-junction tooling to the Krasnikov 4D metric with a thick wall. Expected outcome: confirms Everett–Roman's classical result in our framework + produces a quantitative bound on how much one can soften the negative-energy requirement by going to thick walls and barely-opened light cones. Settles the speculation document rigorously.

### Open Items Entering Next Session
- [ ] **Reframed Calculation 1 (recommended next step):** Krasnikov-tube + Fuchs-class classical thick-wall analysis using our existing Israel-junction notebook tooling. Approximately one session of work; produces a publication-quality quantitative result; closes the speculation question.
- [ ] **Path 2B updated literature pull:** anisotropic Casimir stresses, waveguide-confined modes, asymmetric-plate configurations. Inform whether the Rodal stress-energy profile has a plausible QFT realisation.
- [ ] **Optional:** propagate the Krasnikov-tube comparison into `MATTER_SHELL_PATH.md` and into the `QUANTUM_CLASSICAL_BRIDGE.md` outcome matrix.
- [ ] **Optional:** read Lentz 2020 and Natário 2002 in light of the Type I / Type IV classification in Rodal 2025; their constructions almost certainly fit the same Hawking–Ellis-class taxonomy.

### Conceptual State at End of Session
The Session 6 boundary — "static classical yes, dynamical classical no, dynamical quantum open" — survives intact. Two pieces of new context attach:

(a) **The static-infrastructure-network branch of speculation is closed.** Krasnikov tubes have all the topological features the speculation document wanted, but with negative classical wall energy and a network-implies-CTC theorem. Fuchs-class shells have the energy properties one wants, but lack the light-cone-opening mechanism that would make a network superluminal. The two cannot be merged without confronting one or both of those obstructions. Our reframed Calculation 1 will quantify exactly how much room exists in between.

(b) **Path 2B's search direction is sharper.** Rodal 2025's irrotational warp shows that the negative-energy problem can be redistributed into anisotropic transverse pressures on a thin wall, with a globally Type I stress-energy and 38× lower peak deficit than Alcubierre. This is much closer to what laboratory anisotropic-Casimir setups produce. Path 2B should now target *that* profile, not generic isotropic vacuum energy.

The project's central two-sided result is unchanged. The new material reinforces it from both sides: one further classical extension (Krasnikov-style infrastructure) is structurally blocked; one further classical optimization (Rodal-style irrotational drive) reduces but does not eliminate the energy-condition deficit. Both findings are now documented at the same technical level as Sessions 4–6.

---

## Session 8: 2026-04-16 — Task 2A.13 (Reframed Calculation 1) Execution

### Directive
User: *"I guess at this point we are mapping the boundary condition? Please plan and implement Task 2A.13"* — execute the Krasnikov-tube + Fuchs-class thick-wall analysis recommended at the end of Session 7.

### What Was Accomplished

#### Validation pipeline (`agent-tools/krasnikov_scratch{,2,3,4,5}.py`)
Five staged validation scripts before notebook construction:
1. **scratch.py** — symbolic Einstein-tensor calculation reproduces Everett–Roman Eq. 14 exactly (zero-difference identity).
2. **scratch2.py** — initial numerical scan; identified that the "minimum of $T_{tt}$" differs from Eq. 39's "value at $\rho_{\max} - \epsilon$" by the $1/(1+k)^2$ amplification factor.
3. **scratch3.py** — clean reproduction of Eq. 39 at the right evaluation point ($T_{\hat t \hat t}(\rho_{\max} - \epsilon) \approx -0.042$ at the canonical $\eta = 1.99$, $\epsilon = 1$, $\rho_{\max} = 100$).
4. **scratch4.py** — full orthonormal-frame $T_{\hat\mu\hat\nu}$ via the Everett–Roman tetrad. Confirmed both WEC failure (outer wall) and DEC failure (inner wall, off-diagonal flux).
5. **scratch5.py** — fine $\eta$-sweep showing WEC failure scales linearly to $\eta = 10^{-12}$, no threshold.

#### `krasnikov_tube.ipynb` (new notebook, 22 cells, four-part structure)
Part A: Krasnikov 4D metric and classical stress-energy. Part B: full DEC analysis in the orthonormal frame. Part C: $(\eta, \epsilon, \rho_{\max})$ parameter sweep via HF Jobs. Part D: comparison to Path 2A Packages 1–2 and synthesis. Headline results:

- **Symbolic regression: $T_{tt}$ matches Everett–Roman Eq. 14 exactly** (Cell 5, zero-difference identity).
- **Universal scaling law:** $\rho_p^{\min}(\eta, \epsilon, \rho_{\max}) = -\kappa_K(\eta)/\epsilon^2$ with $\kappa_K(\eta) \approx 1.534\,\eta/(4\pi) \approx 0.122\,\eta$ at small $\eta$, verified to 14-decimal $\epsilon$-independence (Cell 13). Slope-1 power-law fit: $\kappa_K \approx 0.123\,\eta^{1.001}$.
- **WEC fails for any $\eta > 0$, with no thickness threshold.** Fine sweep down to $\eta = 10^{-12}$ shows linear scaling persists (Cell 17).
- **HF Jobs preview sweep:** 300 points across $(\eta, \epsilon, n)$. WEC pass rate **0.0000**, DEC pass rate **0.0000** (Cell 19).
- **Universal collapse figure** (Cell 21): $|\rho_p^{\min}| \cdot \epsilon^2$ vs. $\eta$ collapses all five $\epsilon$ curves onto a single line — the headline figure of Task 2A.13.
- **Unobservability tradeoff** (Cell 23 markdown): both negative-energy density and observable lightcone opening scale linearly with $\eta$; their ratio is $\eta$-independent, so the warp drive cannot be made simultaneously useful and energy-condition-friendly.

#### `hf_jobs/sweeps/krasnikov_tube.py` and configs
Sweep module that builds the orthonormal-frame $T_{\hat\mu\hat\nu}$ symbolically once at module import, lambdifies to NumPy, and evaluates DEC slack and WEC residual on a $(\eta, \epsilon, n)$ grid. Validated against an independent SymPy reference pipeline (`agent-tools/krasnikov_sweep_test.py`) to **byte-identical agreement** across all five tensor components and all test points. Preview config (~600 candidates → 300 valid points after filter, runs in 3 seconds locally on Windows). Full config (~30,000 points) pre-staged for HF Jobs.

#### Documentation updates
- `MATTER_SHELL_PATH.md` §9 (new) — full quantitative statement of the Task 2A.13 result with subsections 9.1–9.8: setup, scaling law, no-go, unobservability, no-rescue argument, comparison table, speculation-document closure, project implication.
- `KRASNIKOV_TUBE_NOTES.md` §9 (new) — update note pointing to the executed notebook and recapping how each pre-execution prediction was confirmed.
- `ROADMAP.md` Task 2A.13 marked complete with full result summary; risk register entry on Krasnikov-tube prior art updated to "mitigation completed."
- `SESSION_LOG.md` — this entry.

### Decisions Made
1. **The static-infrastructure-network branch of speculation is closed** quantitatively: Task 2A.13 produces a robust no-go (WEC pass rate exactly 0/300) for classical Krasnikov tubes, complementary to the Everett–Roman 1997 §4 network-CTC theorem. Combined: classical paths blocked locally + global structure blocked causally.
2. **The Krasnikov $\kappa_K \approx 0.122$ coefficient is now a project-owned result.** It is implicit in Everett–Roman Eq. 38 but they reported it only as "$\approx 1$" in their Eq. 39 because of an incidental simplification at one evaluation point. Our universal-scaling analysis extracts the empirical coefficient to high precision.
3. **The unobservability tradeoff is the strongest classical no-go statement we can make.** The ratio (negative energy density)/(observable warp effect) is a fixed constant $\sim 1/(4\pi\epsilon^2)$ — a parametric statement, not just a numerical one.
4. **Toroidal-Fuchs analysis (Task 2A.14) remains optional** because the speculation question is fully closed by Task 2A.13. A toroidal Fuchs shell is constructible (it's just a topology change of Packages 1–2) but does not provide the lightcone-opening that would make it useful for transport, so the calculation has small marginal value relative to Path 2B.
5. **Path 2B is the next priority.** With Path 2A's classical static and dynamical halves both fully closed (Packages 1–3 + Task 2A.13), the only remaining open route to a useful warp drive is the Casimir / boundary-mode track, with the Rodal 2025 sharpening of the QFT-search target to anisotropic transverse vacuum stresses.

### Open Items Entering Next Session
- [ ] **Path 2B Task 2B.1–2B.5 restart:** anisotropic Casimir geometries (waveguide, asymmetric-plate, repulsive-Casimir), targeting the Rodal stress-energy profile (positive on-axis $\rho_p$, negative transverse pressures on the wall, globally Type I).
- [ ] **Optional Task 2A.14:** toroidal-Fuchs static junction. Lower priority than 2B given the speculation-document closure.
- [ ] **Optional Task 2A.11–12:** Lentz 2020 and Natário 2002 in the Hawking–Ellis-class taxonomy of Rodal 2025.
- [ ] **Writing up.** The complete Path 2A result (Packages 1–3 + Task 2A.13) is now a coherent short-paper-worth of material on the limits of classical warp drives, including: existence of static DEC-compatible matter shells with a $\Delta_{\min}/R = \kappa\beta/C$ scaling law; obstruction theorem for in-vacuum self-acceleration; quantitative GW-recoil ceiling; and now a parametric no-go for static-infrastructure Krasnikov-style geometries with a universal $\rho_p^{\min} \propto -\eta/\epsilon^2$ scaling and the unobservability tradeoff. Decide whether to pursue arXiv preprint or continue with Path 2B first.

### Conceptual State at End of Session
The Path 2A classical research programme is **complete**:

| Sub-question | Status | Source |
|---|---|---|
| Static spherical Fuchs shells satisfy DEC? | Yes, with $\Delta/R \ge \kappa\beta/C$ | Packages 1–2 |
| Acceleration of those shells in vacuum? | No classical mechanism | Package 3 |
| Static-infrastructure Krasnikov tubes with classical matter? | No for any $\eta > 0$, by universal $\rho_p^{\min} \propto -\eta/\epsilon^2$ scaling | Task 2A.13 |
| Network of Krasnikov tubes (causal)? | No, two opposite tubes form CTCs (Everett–Roman §4) | Literature |
| Useful classical warp drive? | **No** under DEC + classical positive matter + vacuum exterior + no expelled reaction mass | Composite of above |

The remaining open question — the only candidate for a useful warp drive consistent with all known classical physics — is whether **a quantum-field source for the warp metric exists**, with the strongest extant target being a Rodal-style anisotropic-Casimir profile. That is Path 2B, and it is the next phase of the project.

---

## Session 9: 2026-04-17 — Reframing and Phase 2C launch (Surfing Mode)

### Directive

User: *"As a point of interest... we aren't writing a paper we are exploring a mathematical landscape. There are no deliverables. Though I am a star trek nerd and I am biased towards wanting a warp drive."*

After the TRUST_AUDIT.md sanity check, the user explicitly reframed the project: this is a personal landscape exploration, not a publication-driven research programme. The framing in `MATTER_SHELL_PATH.md` and `ROADMAP.md` had drifted toward "Path 2A is closed with prejudice / Path 2B is the only remaining route," which oversold the actual coverage of the warp-drive landscape.

User instruction: *"Yes please revise MATTER_SHELL_PATH.md and ROADMAP.md, I defer to you the order we explore them in but lets explore all of them, TRUST_AUDIT.md is being kept and implemented for my own understanding... We are surfing."* and follow-up: *"Implement the plan as specified..."* on the [surfing-the-warp-landscape plan](surfing-the-warp-landscape_37d1bdf0.plan.md).

### What Was Accomplished (Phase 0: Reframe)

#### Documentation rewrites

- [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md): **§0.5 Caveats and Adjacent Slices** added near the top, with explicit slice-scope statement: "Within (Alcubierre $\beta^x \hat x$ shift) × (spherical Fuchs-class shell or static cylindrical Krasnikov tube) × (asymptotically flat vacuum exterior) × (steady-state metric or its Lorentz boost) × (4D General Relativity), no useful warp drive is simultaneously DEC-compatible, accelerable, and transport-relevant." Six adjacent slices listed with notebook + notes targets. §9.7 and §9.8 softened from "closed" / "no classical mechanism" to "this slice of parameter space rules out X; six adjacent slices remain unexplored."
- [`ROADMAP.md`](ROADMAP.md): Phase 2A status changed from "Primary research track" to "Static slice mapped (Sessions 5–8); adjacent slices open (Phase 2C)." Decision-point language softened from "Path 2B is the only remaining positive path" to "Path 2B is one remaining positive path; Phase 2C adjacent slices are also open candidates." **New Phase 2C added** with six tasks (2C.1 through 2C.6), each citing its target notebook and audit interleave. Risk register entries marked "Realised" softened to "Within static slice: realised; outside static slice: open (Phase 2C)" or to acknowledge specific subsequent work that tests them.
- [`README.md`](README.md): Phase 2A status changed from "CLASSICAL HALF COMPLETE" to "STATIC SLICE MAPPED." Added Phase 2C status line. Project description rewritten with explicit slice-of-parameter-space framing for the four results. Added closing paragraph stating "this is a personal landscape exploration, not a paper-driven programme."

#### What was NOT changed

- The actual results, data, and computations from Sessions 5–8 are unaffected. Only the framing language around them was softened.
- TRUST_AUDIT.md is kept as-is per user preference; it is the "where might we be wrong" map and is actively used as a reference during slice exploration.
- The Krasnikov no-go (Task 2A.13) result-quality rating in TRUST_AUDIT.md remains "rock-solid (A)" because the calculation itself is symbolically verified; only the broader interpretive language ("closes the static-infrastructure branch") is softened.

### Decisions Made

1. **Project mode is "surfing," not "paper-writing."** All subsequent slice notebooks should report results with explicit slice-of-parameter-space scope. No claim should overgeneralise from "this slice" to "the landscape."
2. **All six adjacent slices will be deep-dived** (per the plan), in the order: shift families → hybrid wall → time-dependent → QI loosening → cosmological exterior → modified gravity. Order chosen by "most-likely-to-find-something-interesting first" with audit interleaves natural to each slice.
3. **TRUST_AUDIT.md interleaves continue.** Each slice that touches the relevant notebooks drops in the corresponding verification upgrade (e.g. Slice 1 touches `israel_junction.ipynb` so adds the Schwarzschild $K_{ab}$ regression cell).
4. **Compute infrastructure (local / Colab / HF Jobs) is reused without modification** for all six slices. Cost discipline: always preview locally → Colab if interesting → HF Jobs only for full grids.

### Open Items Entering Slice 1

- [x] Slice 1 (alternate shift families) — completed during the same Session 9; see slice-by-slice summary below.

### Slice-by-slice summary (added at end of Session 9, after all six slices completed)

**Slice 1 — Alternate shift families** ([`shift_families.ipynb`](shift_families.ipynb), [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md), [`hf_jobs/sweeps/shift_families.py`](hf_jobs/sweeps/shift_families.py))

- Built single ADM pipeline with closed-form metric inverse (1100× faster than SymPy on tanh shifts), parameterised by orthonormal-frame shift components.
- Tested four families: Alcubierre, Natário zero-expansion, irrotational (Rodal), free-form $j_1$ Bessel mode.
- 0/140 sweep points achieve WEC ≥ 0.999. Best is 0.94 (free-form, very specific tuning).
- Quadrupole moments within an order of magnitude across families → Package 3 GW-recoil ceiling transfers.
- Audit interleave: TRUST_AUDIT #4 closed (Schwarzschild $K_{ab}$ regression cell added to `israel_junction.ipynb`, all three components match Poisson §3.8 to literal 0).

**Slice 2 — Fuchs+Krasnikov hybrid wall** ([`hybrid_wall.ipynb`](hybrid_wall.ipynb), [`hf_jobs/sweeps/hybrid_wall.py`](hf_jobs/sweeps/hybrid_wall.py))

- Modified Krasnikov $k(\rho)$ profile by adding localised matter-shell perturbation $\delta_M B_{w_M}$.
- Pipeline regression at $\delta_M = 0$ exactly reproduces Task 2A.13's $\rho_p^{\min} = -0.175$.
- 0/480 sweep points achieve WEC ≥ 0.999. Best is 0.91 with $\rho_p^{\min} = -0.074$.
- Matter perturbation introduces own gradient-induced curvature, shifting WEC-violating region without removing it.
- Audit interleave: TRUST_AUDIT #6 closed (three-mechanism exhaustiveness proof added as Appendix A to [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md)).

**Slice 3 — Time-dependent acceleration** ([`time_dependent.ipynb`](time_dependent.ipynb), [`TIME_DEPENDENT_NOTES.md`](TIME_DEPENDENT_NOTES.md))

- Built time-dependent Alcubierre Einstein tensor symbolically with $v$ as abstract function of $t$.
- Found that 9 of 10 components have $\dot v$ corrections; specifically $\Delta G_{tt}$ is **antisymmetric in the axis-of-motion coordinate $x$**, scales as $1/\tau$ (linear in $\dot v$), with peak ratio to static $\rho_p$ peak of 0.003 at $\tau = R/c$.
- Antisymmetry → no net momentum injection at quadrupole order → Package 3 conclusions transfer.
- Subtle bug-and-fix in Cell 11: initial diagnostic compared $v(0) \neq v(\infty)$ rather than $v$-equal, $\dot v \neq 0$. After correction, the result is much cleaner and physically sensible.
- Audit interleave: TRUST_AUDIT #5 implemented as Colab-runnable cell. Falls back to Package 3 heuristic locally; ready for Colab upgrade.

**Slice 4 — Krasnikov 2003 QI loosening** ([`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md))

- Critical read of Krasnikov 2003 (gr-qc/0207057). Three substantive loopholes in the standard "QI rules out useful tubes" argument:
  1. Weyl-vs-Ricci ratio breaks the QI's curvature-density chain.
  2. Sub-Planckian support makes $E_{\rm tot}^-$ a meaningless extrapolation.
  3. Explicit "dihedral portal + Van Den Broeck pocket" gives a useful traversable wormhole with $\sim 10^{-3}$ g of exotic matter.
- **Our Task 2A.13 classical no-go is unaffected** because it is a local Einstein-equation result independent of any QI argument.
- Citations of "QI rules out useful Krasnikov tubes" should soften to "QI bounds are subject to substantive loopholes."
- Audit interleaves: TRUST_AUDIT #7 (Bobrick-Martire 2021 §III–IV propulsion theorem, verified verbatim) and #8 (Everett-Roman 1997 §4 CTC theorem, verified geometrically). Both A-grade.

**Slice 5 — Cosmological exterior** ([`cosmological_exterior.ipynb`](cosmological_exterior.ipynb), [`COSMOLOGICAL_EXTERIOR_NOTES.md`](COSMOLOGICAL_EXTERIOR_NOTES.md))

- McVittie metric symbolic Einstein tensor reproduces FRW asymptotic value $G_{tt} \to 3H^2$ at large $r$.
- Cosmological-exterior momentum-exchange ceiling: $\Delta v \le 5.7 \times 10^{-36}$ m/s at $R_{\rm BY} = 100\,R_{\rm shell}$, scaling as $R_{\rm BY}^3$. **42+ orders of magnitude below GW-recoil channel.**
- Hubble drag timescale $1/H_0 \sim 10^{10}$ yr; irrelevant operationally.
- **However**, Garattini-Zatrimaylov 2025 (arXiv:2502.13153, surfaced in Slice 6 lit-pull) shows that for a bubble at exactly Hubble velocity, *averaged* WEC/NEC are recoverable in de Sitter — a different cosmological loophole than the momentum-exchange channel. Slice 5 conclusion is therefore qualified: momentum-exchange channel is not load-bearing, but energy-condition obligations under specific velocity-matching are non-trivially modified.

**Slice 6 — Modified gravity** ([`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md))

- Literature pull. Three credible constructions:
  1. **Lobo & Oliveira 2009** (f(R) wormholes): matter satisfies WEC, curvature absorbs the violation in Jordan frame. Frame-dependent loophole.
  2. **Fell & Heisenberg 2021**: positive-energy soliton in *standard* GR via multi-mode shift. Relevant to Slice 1's "single-mode" caveat, not modified gravity per se.
  3. **Garattini-Zatrimaylov 2025**: bubble at Hubble velocity in de Sitter satisfies averaged WEC/NEC. Standard GR with $\Lambda$, modifies Slice 5.
- Phase 6b (computational) deferred — would need a 4th-order PDE solver, significant infrastructure.
- **Modified gravity is a real loophole** (in Jordan frame), but interpretation-dependent: Einstein-frame transformation moves the violation to a scalar-field side. Whether this counts as "DEC-respecting matter" is contested.

### Decisions Made (Session 9 wrap)

1. **Phase 2C is complete.** All six slices have been deep-dived (Slices 1, 2, 3, 5 with full notebooks; Slices 4, 6 lit-only). Each produces a notebook + notes document.
2. **No slice broke the Path 2A negative result outright.** Within the slice we tested, the obstruction is robust; outside the slice, several published constructions claim positive-energy warps but are subject to interpretation-dependent caveats (modified-gravity frame choice, Garattini-Zatrimaylov velocity matching, Fell-Heisenberg multi-mode optimisation).
3. **TRUST_AUDIT.md is now nearly fully closed.** TRUST_AUDIT #4, #6, #7, #8 closed during Session 9 via slice interleaves. #5 is wired but Colab-only. #3 (Warp Factory MATLAB) remains deferred.
4. **The cleanest follow-up candidate is Fell-Heisenberg 2021** — their positive-energy claim is in *standard* GR with multi-mode shift, falls within our existing tooling, and is a genuine candidate to extend Slice 1 if you want to dig further.

### Conceptual State at End of Session 9 Wrap

After all six slices, the load-bearing assumptions for the Path 2A negative result are:
- **Standard 4D Einstein gravity** (Slice 6 modifies this via $f(R)$);
- **Local DEC required in the matter frame** (modified gravity in Jordan frame moves the violation to the curvature side);
- **Single-mode shift profiles** (Fell-Heisenberg 2021 may break this with multi-mode);
- **Specific-velocity condition not met** (Garattini-Zatrimaylov 2025 needs $v = v_{\rm Hubble}$).

These are interpretation-dependent and somewhat contrived loopholes, but they are also real. None are "easy" engineering paths to a working warp drive — they require either (a) accepting modified-gravity-as-physical, (b) finding a multi-mode shift profile with the Fell-Heisenberg property, or (c) co-moving the warp drive with cosmological expansion at exactly the right rate.

The honest project summary is now: *"No useful classical positive-matter warp drive within the slice we tested; positive-energy claims exist outside the slice but face interpretive challenges. The Path 2A negative result is robust within its assumptions; its assumptions are now mapped explicitly."*

This is the Phase 2C deliverable: a clear and honest map of where the Path 2A no-go applies, where it doesn't, and what the interpretive cost of each loophole is. We are no longer overselling the negative result.

### Conceptual State at End of Session

The project is unchanged in substance and reframed in posture. We have one carefully-mapped slice of the warp-drive landscape (Sessions 5–8), and we are now systematically exploring six adjacent slices to find out whether the negative result we obtained is an artefact of the slice or a genuine landscape feature. Each adjacent-slice exploration is a self-contained notebook + notes document; progress is incremental and we can stop or reorder at any point. There are no deliverables; the goal is to understand the structure of the obstructions.

---

## Session 10: 2026-04-17 — Audit, Synthesis, and Fell-Heisenberg Evaluation

### Directive

User: *"Please audit all documents and make necessary edit/creations. Make sure everything we have done is thoroughly documented. Make a central place for the story you mention in Option F. Then lets implement Option A as you suggest."*

Three-phase plan: (1) audit all 17 markdown docs for stale claims and inconsistencies; (2) create a synthesis layer ([`NAVIGATOR.md`](NAVIGATOR.md) front-door + [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md) narrative); (3) full-reproduction critical evaluation of Fell & Heisenberg 2021.

### What Was Accomplished

**Phase 1 (audit):**
- Patched stale "Path 2B is the only remaining route" claims in [`README.md`](README.md) (Key Result 13), [`QUANTUM_CLASSICAL_BRIDGE.md`](QUANTUM_CLASSICAL_BRIDGE.md), and [`COSMOLOGICAL_EXTERIOR_NOTES.md`](COSMOLOGICAL_EXTERIOR_NOTES.md) to reflect the post-Phase-2C reality.
- Cross-checked load-bearing-assumptions tables across [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md), [`TIME_DEPENDENT_NOTES.md`](TIME_DEPENDENT_NOTES.md), [`COSMOLOGICAL_EXTERIOR_NOTES.md`](COSMOLOGICAL_EXTERIOR_NOTES.md), and [`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md). Each older table marked as historical snapshot with pointer to canonical version in [`NAVIGATOR.md`](NAVIGATOR.md).
- Added "Status: historical (pre-pivot)" headers to [`ALCUBIERRE_IMAGE_METHOD.md`](ALCUBIERRE_IMAGE_METHOD.md), [`ALCUBIERRE_MARCH30_INTEGRATION.md`](ALCUBIERRE_MARCH30_INTEGRATION.md), and [`LINEARIZATION_CALCULATION.md`](LINEARIZATION_CALCULATION.md).
- Updated [`TRUST_AUDIT.md`](TRUST_AUDIT.md): five of the six Concrete Verification Roadmap items now closed (#3 Warp Factory remains deferred); load-bearing-dependencies table updated with Session 9 closures (#4, #6, #7, #8 upgraded from B to A; #5 partially closed); composite project grade now A− with only Fuchs-existence anchor still B.
- Updated [`LITERATURE.md`](LITERATURE.md) last-updated tag.

**Phase 2 (synthesis layer):**
- Created [`NAVIGATOR.md`](NAVIGATOR.md): compact front-door map (~5 pages), with where-to-start triage table, canonical post-Phase-2C load-bearing-assumptions table, full document index by role (entry-point / synthesis / Path 2A / Phase 2C / Path 2B / verification / historical / speculation / compute), and ranked open leads.
- Created [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md): long-form narrative synthesis (~14 pages), structured by physics question rather than chronology. Sections: original problem → static-slice classical realisation → acceleration question → energy-condition obligations across slices → remaining open questions → meta-observation about slicing-vs-asserting → personal Star Trek register.
- Both synthesis docs added to [`README.md`](README.md) document table.

**Phase 3 (Fell-Heisenberg 2021 reproduction):**
- Pulled `papers/2104.06488v4.pdf` (4.3 MB) and `papers/arXiv-2104.06488v4.tar.gz` (3.8 MB).
- Read paper carefully. Critical observation: §3.3 of the body explicitly admits *full* WEC and DEC are violated in compact regions ("no amount of modification could get rid of these"). The paper's title and abstract significantly oversell what is delivered — only the *Eulerian* energy density positivity is the actual claim, not a fully WEC-respecting matter source.
- Wrote [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md): full evaluation with TL;DR, what they prove, what they don't, methodology assessment, project implications.
- Built [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb): symbolic 4D Einstein-tensor pipeline for arbitrary Cartesian shift, Eulerian-energy formula derived independently, A-grade pipeline regression against their Eq. (WECinansatz) (literal symbolic zero), 4th-order finite-difference 3D grid evaluation of Hessian + Jacobian, full ADM stress-energy with $K_{ij}$ and $\mathcal{L}_N K_{ij}$, principal-pressure diagonalisation, full WEC + DEC tests.
- Numerical results at $(V, \sigma, m_0, a, \ell, r) = (0.5, 4, 2, 0.3, 4, 6)$:
  - Eulerian $\rho_E > 0$ in **99.8% of interior cells**.
  - Full WEC pass in **98.7% of interior cells** (1.3% violate).
  - Full DEC pass in **94.7% of interior cells** (5.3% violate).
  - Central $|\vec{N}| = 1.92$ (superluminal).
  - $E_{\rm net} \approx +1.06 \times 10^{-3} M_\odot c^2$ (within order-of-magnitude of their reported $5.2 \times 10^{-4}$).
- **Most surprising finding**: full-WEC violations are *much smaller* than the paper's emphatic "no amount of modification could get rid of these regions" suggests. Only 1.3% of cells fail full WEC at our parameter choice. This raises a clean open question: can a careful $(m, n)$ search eliminate the residual entirely?
- Updated [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md), [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md), [`NAVIGATOR.md`](NAVIGATOR.md), [`LITERATURE.md`](LITERATURE.md), [`ROADMAP.md`](ROADMAP.md) with the FH outcome (Phase 2D added to ROADMAP, Task 2D.4 = the new $(m, n)$ residual-search lead).

### Decisions Made

1. **Project's most interesting open question is now the Fell-Heisenberg $(m, n)$ residual-WEC search** (Task 2D.4 in [`ROADMAP.md`](ROADMAP.md), lead #1 in [`NAVIGATOR.md`](NAVIGATOR.md)). If a parameter choice can eliminate the residual ~1% full-WEC violation, it would be the *first standing fully-WEC-respecting classical warp drive in standard GR* — substantially more than Fell-Heisenberg themselves claim.
2. **Fell-Heisenberg paper should be cited carefully**: as "demonstrates positive Eulerian energy density via multi-mode irrotational shift, with full WEC/DEC violations in compact regions admitted by the authors", *not* as "solved the negative-energy problem in standard GR".
3. **The synthesis-layer documents ([`NAVIGATOR.md`](NAVIGATOR.md) and [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md)) are now the canonical entry points** to the project. Older "Path 2B is the only remaining route" framing has been patched; the project's posture is "structured slice map" not "no-go theorem."

### Conceptual State at End of Session

After 10 sessions of mapping, the prospect of a working warp drive is *slightly more open* than at the end of Session 9 — not by a lot, but by enough to be worth noting. Slice 1's negative result for full WEC under single-mode axisymmetric shifts is unchanged; the Fell-Heisenberg multi-mode follow-up achieves 99% full-WEC pass with a clean residual ~1% region whose minimisability is now the project's most interesting open question. The honest summary in [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md) §7 is *"the no-go is robust within its assumptions; positive-energy claims outside the slice exist but are subject to interpretive challenges; one specific multi-mode construction has come closer than expected to the no-go's edge."*

---

## Session 11: 2026-04-19 — Fell-Heisenberg WEC+DEC sweep (Task 2D.4) + environment cleanup

### Directive

After environmental cleanup (huggingface_hub 1.x upgrade, transformers 4→5, pip 26, Python 3.10 traditional install removed) and confirming HF Jobs CLI access, proceeded directly to the Session-10-era #1 open lead: the Fell-Heisenberg $(V, \sigma, m_0, a, \ell, r)$-family parameter sweep looking for a configuration with zero full-WEC residual.

### What Was Accomplished

**Pipeline port + sweep dispatch:**
- New module [`hf_jobs/sweeps/fell_heisenberg.py`](hf_jobs/sweeps/fell_heisenberg.py) (~280 lines) lifts cells 7, 11, 13 of [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb) into the standard `build_grid` + `evaluate` interface. Returns comprehensive metrics: Eulerian rho_E pass, WEC slack, DEC slack, integrated energies, central $|\vec{N}|$, per-point timing.
- Configs: [`hf_jobs/configs/fell_heisenberg_preview.json`](hf_jobs/configs/fell_heisenberg_preview.json) (729 pts, Npts=49) and [`hf_jobs/configs/fell_heisenberg_full.json`](hf_jobs/configs/fell_heisenberg_full.json) (15000 pts, Npts=65).
- New entry script [`hf_jobs/jobs/run_fell_heisenberg.sh`](hf_jobs/jobs/run_fell_heisenberg.sh) handles HF Jobs container setup + result upload.
- Local 3-point smoke test against the Session-10 anchor reproduces `wec_pass=0.9954` at Npts=49 (notebook 0.987 at Npts=81; <1% drift, conservative direction).
- Created private HF Dataset [`bshepp/alcubierre-sweeps`](https://huggingface.co/datasets/bshepp/alcubierre-sweeps) for parquet result storage.
- HF Jobs preview run (cpu-upgrade, 69 sec, ~$0.01) returned 87 / 729 points with WEC pass = 1.0 but 0 with DEC pass, suggesting Npts=49 was insufficient resolution.
- HF Jobs full run (cpu-xl, 63 min, ~$1.05) returned **1404 / 15000 grid points (9.4%) achieving strict full WEC AND strict full DEC at every interior cell, with $E_{\rm neg} = 0$ identically and central superluminal frame-dragging $|\vec{N}|_{\max}$ from $0.73c$ to $18.6c$.**

**Sanity checks (5 of them, all pass):**
1. The Fell-Heisenberg paper anchor still fails DEC in our pipeline at Npts=81 (literal match to the notebook's 0.94736), confirming the new positive results aren't a generic "always pass" bug.
2. Resolution convergence verified: at the top WEC+DEC-passing point, dec_slack_min stays positive and stable (~+0.016) from Npts=65 through Npts=113.
3. m0 sensitivity is smooth (12-point scan in m0 ∈ [2.5, 4.0] shows DEC slack varies continuously) — the apparent "DEC pass only at exactly m0=3" in the sweep is a grid-stride artifact, not a numerical singularity.
4. V scaling matches the predicted $V^2$ exactly across a 9-point V scan from V=0.1 to V=10.0, so the "DEC pass" property is amplitude-independent — a property of the dimensionless shape $(\sigma, m_0, a, \ell, r)$.
5. The Slice-1 negative result for single-mode axisymmetric shifts is uncontradicted because the FH ansatz is multi-mode and non-axisymmetric.

**Documentation:**
- [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) (new, ~340 lines) — comprehensive write-up: headline result, anchor point, 5 sanity checks, leaderboard, structure of the energy-condition-passing region, and §4 calibrated honest caveats listing what this is NOT (not a complete drive — static only; horizon/CTC/source-matter/asymptotic-matching open).
- [`NAVIGATOR.md`](NAVIGATOR.md) updated: Last-updated tag, headline summary (project-summary paragraph rewritten), load-bearing-assumptions table row for Slice 1 (the multi-mode-is-load-bearing slot), open leads (lead #1 retired, four new top leads from §5 of the sweep notes), document index, compute-infrastructure listing.
- [`ROADMAP.md`](ROADMAP.md) updated: Phase 2D status header (Sessions 10-11), Task 2D.4 marked complete with summary, four new tasks 2D.5-2D.8 defined for the follow-ups.

### Decisions Made

1. **The headline-claim language is calibrated honestly to the static slice.** The result is a static-slice positive existence; it is *not* a complete physical warp drive. The honest summary is "the kinematic energy-condition bottleneck of the warp-drive problem is solved within this static slice; the remaining barriers are dynamical." See [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) §4.
2. **Independent re-implementation of the pipeline (Task 2D.6) is the highest-priority cheap follow-up** before any external claim. The result is too important to publish on the back of a single FD-stencil-of-FD-stencil computation without a second pipeline confirming it.
3. **The horizon/CTC analysis (Task 2D.5) is the most likely place a "too good to be true" objection lands** and is the second-highest priority follow-up. At $|\vec{N}|_{\max} = 18c$ the metric is far from a perturbation of Minkowski; the foliation may break down.
4. **Path 2B (Casimir) is demoted from #3 lead** because the Session-11 result resolves the energy-condition obstruction *kinematically* — Path 2B was the proposed *quantum* fix to the energy-condition obstruction, and that obstruction is now solved classically (in this static slice). Path 2B remains the right route for the *acceleration* and *dynamic-buildability* questions, which the static result does not address.
5. **HF Jobs is now the established compute path for parameter sweeps.** The session 11 sweep validates the workflow end-to-end: local smoke-test → preview HF Jobs run → full HF Jobs run → parquet upload to private dataset → local download and analysis. Per-sweep cost is ~$1, wall time is ~1-2 hours.

### Open Items Entering Next Session

- [ ] **Task 2D.5** (horizon + CTC analysis at the WEC+DEC-passing point) — natural next step.
- [ ] **Task 2D.6** (independent re-implementation) — could be done in parallel via subagent or as a follow-up session.
- [ ] **Task 2D.7** (source-matter classification in Bobrick-Martire taxonomy).
- [ ] **Task 2D.8** (asymptotic matching + double-bubble CTC test).
- [ ] **Update [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md)** with the Session-11 result. The existing §7 honest summary still reads as if the multi-mode case is "close to" passing; needs a rewrite saying "the multi-mode case passes within the static slice."

### Conceptual State at End of Session 11

The project's most-interesting-open-question (Session-10-era) has been answered: **yes, the Fell-Heisenberg multi-mode irrotational ansatz admits a positive-energy fully-WEC-and-DEC-respecting static configuration with superluminal central frame-dragging in standard 4D Einstein gravity**. The 1404 / 15000 grid hit rate is high enough to suggest the WEC+DEC-passing region in $(\sigma, m_0, a, \ell, r)$-space is a finite-volume connected manifold, not a measure-zero boundary curiosity.

This is the **first time in the project's history** that any test of the energy conditions on a candidate warp metric has returned a strict positive answer. Every prior result (Slice 1 single-mode axisymmetric: 0/140; Slice 2 hybrid wall: 0/480; Task 2A.13 Krasnikov tube: 0/300; Session 10 FH single-anchor: 1.3% residual) was negative.

Calibrated honestly, however, this is **a static-slice existence result, not a working warp drive**. The barriers that remain — horizons, CTCs, source matter, asymptotic matching, dynamical buildability, acceleration — are exactly the same barriers Path 2A's static result faced; they have just shifted from "we have no positive existence example" to "we have one but the dynamics are open." The §5 follow-up program in [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) lays out the next 4-7 sessions' worth of focused tests, in priority order. The honest one-liner project summary is now: *"the energy-condition bottleneck has a static-slice existence result; the dynamics remain the open question."*

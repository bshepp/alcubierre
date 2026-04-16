# Research Roadmap — Alcubierre Boundary-Mode Reformulation

## Phase Structure

```
Phase 0:  Foundation (seed documents, literature review)     ✓ COMPLETE
Phase 1:  Linearization & Feasibility                        ◐ IN PROGRESS
Phase 2A: Classical Matter-Shell Realization (primary)       ◐ IN PROGRESS
Phase 2B: Casimir / Boundary-Mode Decomposition (parallel)   ○ NOT STARTED
Phase 3:  Numerical Verification                             ○ NOT STARTED
Phase 4:  No-Go Theorem Confrontation                        ○ NOT STARTED
Phase 5:  Physical Mechanism & Realizability                 ○ NOT STARTED
```

**Phase 2 dual-track policy (2026-04-15):** Following the completion of the quantum vs. classical gap analysis (see `QUANTUM_CLASSICAL_BRIDGE.md`), Phase 2 is split into two parallel research tracks:

- **Phase 2A (primary):** Anchor the boundary-mode framework to Fuchs et al. 2024's *Constant Velocity Physical Warp Drive Solution* (arXiv:2405.02709). This is a classical General Relativity route requiring only ordinary matter. It has a confirmed existence result and a concrete numerical toolkit (Warp Factory). Detailed plan in `MATTER_SHELL_PATH.md`.
- **Phase 2B (parallel):** Continue the Casimir / quantum-field-theoretic route. Remains scientifically interesting independent of Path 2A's outcome, and becomes necessary if Path 2A cannot reach useful velocities with classical matter alone.

The two paths are not mutually exclusive — see `MATTER_SHELL_PATH.md` §6 for the four possible outcome scenarios.

---

## Phase 0 — Foundation ✓

**Goal:** Assemble the theoretical context and formulate the hypothesis.

- [x] Literature review and atlas of surrounding field (March 30 conversation)
- [x] Image-method hypothesis formulation (April 4 seed document)
- [x] Integration of both into working document ([ALCUBIERRE_MARCH30_INTEGRATION.md](ALCUBIERRE_MARCH30_INTEGRATION.md))

---

## Phase 1 — Linearization & Feasibility ◐

**Goal:** Extract the mathematical structure of the Alcubierre metric in the subluminal regime. Determine whether boundary-value methods apply and what form they take.

### Completed

- [x] **1.1** Extract metric perturbation $h_{\mu\nu}$ and verify subluminal linearization regime
- [x] **1.2** Compute exact ADM stress-energy ($\rho$, $j^i$) — exploit flat spatial geometry
- [x] **1.3** Identify order structure: gravitomagnetic ($O(v_s)$) vs energy ($O(v_s^2)$)
- [x] **1.4** Derive Poisson equation for shift vector: $\nabla^2\beta^x = -v_s\nabla^2 f$
- [x] **1.5** Analyze thin-wall limit: monopole + dipole surface layers at $r_s = R$
- [x] **1.6** Test point-image decomposition → **RESULT: Does not work** (constant interior field)
- [x] **1.7** Identify correct framework: boundary-mode decomposition, not point images

### Remaining

- [ ] **1.8** Read Lobo & Visser 2004 (gr-qc/0406083 and gr-qc/0412065) — they did linearized analysis of Alcubierre. Determine overlap with our results and what's new. *(Note: previously cited incorrectly as gr-qc/0410087, which is a solo Lobo wormhole paper.)*
- [ ] **1.9** Read Fuchs et al. 2024 (2405.02709) — constant-velocity physical warp drive satisfying all energy conditions. This is the closest existing result to what the boundary-mode approach predicts.
- [ ] **1.10** Gauge analysis: confirm ADM framework avoids gauge artifacts. Check whether harmonic gauge is recoverable via explicit transformation.
- [ ] **1.11** Document spin-2 vs spin-1 differences that affect gravitomagnetic image intuitions (Costa & Natário 2014).

### Decision Point (Phase 1 → 2)

> **Does the boundary-mode decomposition yield a well-posed mathematical problem with known solution techniques?**
>
> If YES → proceed to Phase 2 (spectral decomposition)
> If NO → reassess whether the approach has content beyond the Casimir analogy

---

## Phase 2A — Classical Matter-Shell Realization ◐

**Status:** Primary research track as of 2026-04-15. Detailed plan in [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md).

**Goal:** Establish that the Alcubierre shift-vector configuration can be embedded inside a physical matter shell (per Fuchs et al. 2024) without violating any energy condition, and determine the maximum shift amplitude and minimum shell mass as a function of bubble parameters.

**Working hypothesis (refined from original Phase 2):** The Alcubierre shift-vector configuration is the *interior* of a physical matter-shell warp drive. There exists a one-parameter family of solutions interpolating between Fuchs's Warp Shell (ordinary matter, all ECs satisfied, small shift) and the original Alcubierre metric (exotic matter, ECs violated, full-amplitude shift). The interpolation parameter corresponds to "warp shift amplitude vs. shell support capacity."

### Completed

- [x] **2A.0** Create dedicated path document ([`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md)) and verification notebook ([`matter_shell.ipynb`](matter_shell.ipynb))
- [x] **2A.1** Fetch and integrate the technical content of Fuchs et al. 2024 (shift-shell construction, bump function Eq. 28, energy-condition bounds, Warp Factory numerical results)
- [x] **2A.2** Reproduce Fuchs bump function $f(r)$ and shift amplitude profile $S_\text{warp}(r)$ numerically; verify support is concentrated in the transition region (boundary localization)
- [x] **2A.3** Static-shell Israel junction: match Minkowski interior to Schwarzschild exterior, derive surface energy density $\sigma = \frac{1}{4\pi GR}(1-\sqrt{1-2GM/R})$ and shell rest mass $\mu \approx M + GM^2/(2R)$. Confirms formalism.
- [x] **2A.4** Show Alcubierre shift has pure $l=1$ dipole structure on a sphere centered on the bubble ($\int \beta^r P_1 \sin\theta\, d\theta = 2\beta/3$, other modes vanish)
- [x] **2A.5** Derive order-of-magnitude shift bound $\beta_\text{warp} \lesssim GM\Delta^2/(R^3 c^2)$ from Eulerian-frame EC inequalities. Matches Fuchs's empirical 0.02 to within one order of magnitude for their parameters.

### Remaining

- [x] **2A.6** Full thin-shell Israel junction with the *shift-perturbed* Alcubierre interior. Completed in [`israel_junction.ipynb`](israel_junction.ipynb) Part A + Part B. Key findings: (i) $[K_{ab}]$ admits only $l=0 + l=1$ angular structure at linear order in $v_s$; (ii) DEC fails at the anti-motion pole for thin walls, with the empirical DEC-satisfying boundary at $v_s \sigma_w R \lesssim GM/R$; (iii) translating shells ($v_{\rm ext} = v_{\rm int}$) are DEC-safe by covariance; (iv) accelerating transients through $\lambda = v_{\rm ext}/v_{\rm int} < 1$ are DEC-unsafe, with a measured $\lambda_* \approx 0.55$ for representative thin-wall parameters. See also `MATTER_SHELL_PATH.md` §3.3.
- [x] **2A.7** Determine the **minimum shell thickness** $\Delta_\text{min}(v_\text{warp}, M, R)$ below which the DEC must fail. Completed in [`thickness_bound.ipynb`](thickness_bound.ipynb). Scaling law: $\Delta_{\min}/R = \kappa\,\beta/C$ with $C = 2GM/(Rc^2)$ and $\kappa \in [0.05, 0.75]$ (numerical lower to analytical pole-dominant upper). See `MATTER_SHELL_PATH.md` §3.4.
- [ ] **2A.8** Vector spherical harmonic decomposition of the full shift vector $\beta^x(r) \hat{x}$ on the shell domain. Match Fuchs's bump function to dominant modes; identify whether the Alcubierre profile is near a fundamental eigenmode.
- [ ] **2A.9** Mass-to-velocity scaling: refine the schematic $M_\text{min} \sim \beta R^3 c^2/(G\Delta^2)$ to include anisotropic pressure bookkeeping. Numerical confirmation against Warp Factory.
- [x] **2A.10** Address the acceleration problem (Fuchs §5.3 open) — **COMPLETED 2026-04-16** in `acceleration.ipynb`. Result: ADM 4-momentum conservation rules out self-acceleration in vacuum; three-mechanism catalog (shift spin-up, mass ejection, GW recoil) shows only mass ejection (ordinary rocket) is practically viable. GW-recoil ceiling is $\lesssim 0.25\%$ of $v_{\rm warp}$ under the most favourable Fuchs-compatible parameters (from HF Jobs sweep + SXS rescaling of Varma et al. 2022 record 5000 km/s). Strictly strengthens Schuster–Santiago–Visser 2023 Theorem 3. Falsifies scenario (A) of `MATTER_SHELL_PATH.md` §6 for accelerating shells; elevates Path 2B to the remaining open candidate for a vacuum+DEC+dynamical realisation.
- [ ] **2A.11** Compare the Fuchs matter shell to Lentz 2020 (Einstein-Maxwell-plasma soliton) — both classical positive-energy warp solutions but with different matter sectors. Are they the same physical mechanism?
- [ ] **2A.12** Compare to Natário 2002 zero-expansion drive — does the boundary-mode framing recover or dismiss this as a special case?

### Decision Point (Phase 2A → later phases)

> **Can a classical matter shell support a useful shift amplitude ($\beta_\text{warp} \gtrsim 0.01 c$) without violating energy conditions at realistic shell masses?**
>
> - If YES at useful amplitudes → proceed to Phase 3 numerical validation and Phase 5 physical realizability
> - If YES only at tiny amplitudes → Phase 2B (Casimir) becomes necessary for the gap; proceed in parallel
> - If NO (acceleration always fails) → Phase 2B is the only remaining positive path
> - If NO (no configuration avoids EC violation) → no-go result; document and publish

---

## Phase 2B — Casimir / Boundary-Mode Decomposition (Parallel Track) ○

**Status:** Parallel to Phase 2A. Conceptual foundation in [`QUANTUM_CLASSICAL_BRIDGE.md`](QUANTUM_CLASSICAL_BRIDGE.md).

**Goal:** Decompose the Alcubierre shift vector into eigenmodes of the vector Laplacian on a spherical domain; test whether the energy density admits a Casimir-like mode-sum interpretation. If Phase 2A succeeds only at small amplitudes, this track provides the quantum supplement for larger amplitudes via the semiclassical Einstein equation $G_{\mu\nu} = 8\pi G\, \langle \hat{T}_{\mu\nu}\rangle_\text{ren}$.

### Tasks

- [ ] **2B.1** Set up the spectral problem: eigenmodes of the **vector Laplacian** (not scalar $\nabla^2$) acting on the shift vector $\beta^i$ on a spherical domain of radius $R$. The shift vector is a spatial vector field, so the relevant operator is $\nabla^2 \beta^i + \frac{1}{3}\partial^i(\nabla \cdot \beta)$ (for the transverse-traceless decomposition) or the full vector Laplacian $\Delta_V \beta^i = \nabla^2 \beta^i$. Determine boundary conditions from wall physics.
- [ ] **2B.2** Expand $\beta^x = -v_s f(r_s)$ in spherical Bessel functions × vector spherical harmonics. Angular structure is pure $l=1$ dipole in the radial projection (confirmed in `matter_shell.ipynb`).
- [ ] **2B.3** Identify which radial modes dominate — is $f(r_s)$ close to the fundamental mode of the wall domain?
- [ ] **2B.4** Compute the mode-by-mode contribution to the energy density: does the wall mode sum carry the negative-energy signature?
- [ ] **2B.5** Compare to the Casimir effect between concentric spheres (Boyer 1968 — repulsive EM case). Determine whether this sign persists for vector modes under warp-drive boundary conditions.
- [ ] **2B.6** Determine whether the Alcubierre energy density $\rho$ can be written as a **mode sum** analogous to Casimir regularization. If yes, this is the quantum-classical bridge.
- [ ] **2B.7** Semiclassical calculation: compute $\langle \hat{T}_{\mu\nu}\rangle_\text{ren}$ for a scalar field on the Alcubierre background with wall boundary conditions (scalar is the tractable warm-up; gravitational field is the hard case).
- [ ] **2B.8** Spin-2 obstruction assessment (per `QUANTUM_CLASSICAL_BRIDGE.md` §4 and Costa & Natário 2014): is there any physical structure that could serve as a "gravitational conductor"? If not, Path 2B is foreclosed and Path 2A must carry the whole result.

### Key Questions

- Is there a physical "boundary condition" for gravitational modes? (Open — no known analog of a conductor for spin-2 fields)
- Does the mode sum converge, or require regularization?
- Does the thick matter shell of Path 2A impose an effective boundary on a quantum gravitational field?

### Decision Point (Phase 2B)

> **Does the mode-sum / semiclassical approach produce a finite, physically interpretable expression that either (a) matches the exotic energy density of Alcubierre or (b) produces a correction to Path 2A's classical result?**
>
> - If (a) → Casimir mechanism is real; full quantum gravitational warp drive
> - If (b) → Hybrid picture; Path 2A primary + Path 2B correction
> - If mode sum diverges irregularly → the regularization scheme *is* the physics; study it
> - If spin-2 obstruction is insurmountable → document the no-go and close Path 2B

---

## Phase 3 — Numerical Verification ○

**Goal:** Validate analytical results against existing numerical tools (Warp Factory) and compute quantities not accessible analytically.

### Tasks

- [ ] **3.1** Set up Warp Factory (MATLAB, arXiv:2404.03095) — reproduce standard Alcubierre energy conditions and Fuchs et al. 2024 Warp Shell as sanity checks
- [ ] **3.2** **(Path 2A)** Numerically sweep the Fuchs construction: vary $M$, $R_1$, $R_2$, $\beta_\text{warp}$; map the boundary of the EC-satisfying region. Test the predicted scaling $\beta_\text{max} \propto GM\Delta^2/(R^3c^2)$.
- [ ] **3.3** **(Path 2A)** Evaluate nested-shell and non-spherical shell geometries — can the Fuchs construction be optimized (Section 5.2 of their paper) to reduce required shell mass by orders of magnitude?
- [ ] **3.4** **(Path 2B)** Implement vector-spherical-harmonic decomposition numerically (Python/numpy): compute mode coefficients for specific shape functions
- [ ] **3.5** **(Path 2B)** Compare mode-sum energy density to exact ADM energy density (Section 4.1 of linearization doc) — verify convergence
- [ ] **3.6** Vary wall thickness $\Delta$ and bubble radius $R$: does the mode structure change qualitatively, or just quantitatively?
- [ ] **3.7** Test against Lentz 2020 positive-energy soliton — does the mode decomposition (or matter-shell framework) naturally produce it?
- [ ] **3.8** Test against Natário 2002 zero-expansion solution — second test case

---

## Phase 4 — No-Go Theorem Confrontation ○

**Goal:** Explicitly check the boundary-mode reformulation against known no-go results.

### Tasks

- [ ] **4.1** Santiago-Schuster-Visser 2021 (2105.03079): identify which assumption the boundary-mode approach challenges (if any). Enumerate all assumptions; check each.
- [ ] **4.2** Pfenning-Ford 1997 quantum inequality constraints: does the mode picture change the wall-thickness/energy trade-off?
- [ ] **4.3** Everett 1996 causality: does the subluminal restriction avoid causality violations?
- [ ] **4.4** Hiscock 1997 horizon formation: does the boundary-mode picture change horizon structure?

### Decision Point (Phase 4 → 5)

> **Does the reformulation survive all no-go theorems, or does it identify a specific failing assumption?**
>
> If SURVIVES → the reformulation may have physical content; proceed to Phase 5
> If IDENTIFIES FAILING ASSUMPTION → that's a publishable result regardless of whether the drive works
> If FAILS → document exactly how and where it fails; close project or pivot

---

## Phase 5 — Physical Mechanism & Realizability ○

**Goal:** If the mathematics survives, determine whether the boundary-mode configuration can be physically realized.

### Tasks

- [ ] **5.1** What physical structure plays the role of the "wall"? Phase 2A evidence: **a physical matter shell** (Fuchs et al. 2024). Open: are there other admissible structures (horizons, membranes, rotating shells)?
- [ ] **5.2** What is the minimum mass/energy of the wall structure? Preliminary scaling from Phase 2A: $M_\text{min} \sim \beta_\text{target} R^3 c^2 / (G\Delta^2)$. Tighten with numerical optimization.
- [ ] **5.3** Is the configuration stable? (Perturbation analysis of the shell + shift; modal stability of the boundary-mode decomposition)
- [ ] **5.4** **(Resolved in Phase 2A.)** Fuchs et al. 2024 is an instance of the boundary-mode framework with a physical matter shell acting as the boundary. See `MATTER_SHELL_PATH.md` §2 for the explicit mapping.
- [ ] **5.5** Energy scaling: does the boundary-mode picture change the $v_s^2 R^2/\Delta$ scaling? Does the matter-shell route change it further (to $M\Delta^2/R^3$ instead of $v^2 R^2/\Delta$)?
- [ ] **5.6** Acceleration problem (Fuchs §5.3): can the bubble be accelerated without reintroducing negative energy? This is the hardest outstanding question for both paths.

---

## Open Questions (Cross-Phase)

These questions don't belong to a single phase; they may resolve at any point.

| # | Question | Relevant to |
|---|----------|-------------|
| Q1 | What gauge makes the boundary-mode decomposition cleanest? | Phases 1–2 |
| Q2 | Which spin-2 vs spin-1 differences break EM image intuitions? | Phases 1–2B |
| Q3 | Does the ship's own $T_{\mu\nu}$ contribute at leading order or is it negligible? | Phases 2A, 2B |
| Q4 | Can Warp Factory accept arbitrary metric inputs for energy-condition analysis? | Phase 3 |
| Q5 | Is there a Krasnikov-tube analog under different boundary conditions? | Phase 5 |
| Q6 | Does the mode picture connect to the dimensional-coherence / emergent-spacetime framework? | Speculative |
| Q7 | Can nested or rotating shells amplify the frame-dragging of a single Fuchs shell? | Phase 2A, 5 |
| Q8 | What is the acceleration-phase metric, and does it require negative energy? | Phase 2A, 5 |
| Q9 | Does Lentz 2020 represent the same mechanism as Fuchs et al., or a genuinely distinct positive-energy route? | Phase 2A |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Lobo & Visser 2004 already contains the key results | Medium | High — reduces novelty | Read it early (Task 1.8). Even if they linearized, the mode decomposition / matter-shell framing may be new. Correct arXiv: gr-qc/0406083, gr-qc/0412065. |
| Fuchs et al. 2024 already contains the key Path 2A results | High | Medium — reduces novelty but not value | They have the existence result; our framing identifies the boundary-mode structure, scaling laws, and the interpolation to Alcubierre. Novelty is in the systematic mapping and the mode-spectrum interpretation, not in the construction itself. |
| Path 2A: Fuchs construction cannot be pushed past tiny shift amplitudes | Medium-High | Medium — still useful if 2B works | If $\beta_\text{max}$ from classical matter remains $\ll 1$, Path 2B becomes necessary to supply the gap. Frame this as "classical provides bulk positive energy; quantum (Casimir) supplies the negative sliver" — much smaller quantum requirement than pure exotic matter. |
| Path 2A: Acceleration always fails (Schwarzschild Drive pathology) | **Realised, 2026-04-16** | High — reduces Path 2A to a static-only result | Confirmed by Task 2A.10 (`acceleration.ipynb`). Static frame-dragging works (Packages 1–2); acceleration under vacuum+DEC+no-ejecta does not. Path 2B now the sole remaining route to a dynamical drive. Mitigation: (i) document the result rigorously (done, MATTER_SHELL_PATH.md §7), (ii) elevate Path 2B priority (see updated QUANTUM_CLASSICAL_BRIDGE.md §6 outcome matrix). |
| Path 2B: Mode decomposition doesn't converge | Low | High — invalidates Phase 2B | Check numerically (Phase 3) in parallel with analytics |
| Path 2B: Spin-2 effects kill the analogy | Low-Medium | High | Costa & Natário 2014 gives the catalog. Key issue: spin-2 boundary conditions are qualitatively different from spin-1 — no known "gravitational conductor" analog. See QUANTUM_CLASSICAL_BRIDGE.md §4. If this kills 2B, Path 2A must carry the whole result. |
| Path 2B: Quantum vs. classical gap invalidates Casimir mechanism | Medium | Medium — Path 2A still viable | The Casimir effect is quantum ($\hbar$-dependent); the boundary-mode picture can be classical (Path 2A) or quantum (Path 2B). If Path 2A succeeds, this risk is moot. Otherwise, a semiclassical $\langle T_{\mu\nu}\rangle$ calculation (Task 2B.7) is needed. See QUANTUM_CLASSICAL_BRIDGE.md. |
| Path 2B: Boyer sign problem — spherical Casimir energy may be repulsive | Medium | High — wrong sign for the application | Boyer (1968) found repulsive Casimir energy for a conducting sphere in EM. Must check whether this carries over to gravitational vector modes under warp-drive boundary conditions. |
| Both paths fail at useful velocities | Low-Medium | Fatal for physical claims | The mathematical framework (mode decomposition, shell matching) is still valid as a classification tool, and a no-go result is publishable. |
| No-go theorems apply without loophole | Medium | Fatal for physical claims | The mathematical framework is still valid even if the physical mechanism isn't; pivot to "classification tool" |
| Project scope creep into superluminal regime | High | Medium — wastes time | Strict subluminal discipline through Phase 3; superluminal is Phase 5+ at earliest |

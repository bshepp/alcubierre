# The Quantum–Classical Gap in the Boundary-Mode Approach

## Status: Working Analysis Document — updated to reflect two-track split
## Author: Brian Sheppard + Claude
## Date: 2026-04-15 (v1), 2026-04-15 (v2 — two-track strategy added)
## Purpose: Rigorously address whether and how the Casimir analogy connects
##          classical boundary-mode decomposition to quantum negative energy.
##          This is the conceptual home of **Path 2B** (Casimir / quantum);
##          Path 2A (classical matter shell) is in [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md).

---

## 1. The Problem

The project's central analogy maps the Alcubierre bubble wall to Casimir plates:

| Feature | Casimir Effect | Boundary-Mode Proposal |
|---------|---------------|----------------------|
| Field | Electromagnetic (spin-1) | Gravitomagnetic (spin-2) |
| Boundary | Conducting plates | Bubble wall ($r_s = R$) |
| Mechanism | Quantum vacuum fluctuations | Classical boundary conditions |
| Negative energy | $\langle T_{00} \rangle_\text{ren} < 0$ between plates | $\rho < 0$ at bubble wall |
| Scale setting | $\hbar$ (Planck's constant) | None ($\hbar$-independent) |
| Experimental status | Measured (Lamoreaux 1997) | Not observed |

The structural parallel is real: both involve boundary conditions restricting a field's mode spectrum, producing negative energy density at the boundary. But the mechanisms are fundamentally different. The Casimir effect is a quantum phenomenon with magnitude set by $\hbar$; the Alcubierre energy density is a classical result with no $\hbar$ dependence.

**The project documents have been asserting "structurally identical" when the honest statement is "structurally analogous."** This document clarifies the distinction and identifies the path from analogy to physical connection.

---

## 2. Three Levels of Claim

The boundary-mode program can make claims at three levels of increasing ambition. They should be clearly distinguished in all project documents.

### Claim (a): Geometric Classification [Classical, Established]

**Statement:** The Alcubierre stress-energy tensor has the mathematical structure of a boundary effect. All source terms ($\nabla^2 f$) are localized at the bubble wall. The interior field ($\beta^x = -v_s$, constant) and the exterior field ($\beta^x \to 0$) are both source-free. The exotic energy density is a quadratic functional of the wall-localized field configuration.

**Status:** This is a theorem about the Alcubierre metric. It is established by the linearization calculation (Sections 4, 6, and 9 of `LINEARIZATION_CALCULATION.md`). No quantum mechanics is needed or invoked.

**What it gives:** A new way to classify warp-drive geometries — by their boundary-mode structure rather than by their volumetric stress-energy. This may be useful even if the Casimir connection fails.

### Claim (b): Semiclassical Consistency [Quantum, Testable]

**Statement:** If one places quantum fields on the Alcubierre background and treats the bubble wall as a boundary (with appropriate boundary conditions on the quantum field modes), the renormalized expectation value $\langle \hat{T}_{\mu\nu} \rangle_\text{ren}$ has the correct sign (negative) and the correct spatial structure (localized at the wall, torus-like angular dependence) to match the classical $T_{\mu\nu}$ required by the Einstein equations.

**Status:** Not yet computed. This requires a QFT-in-curved-spacetime calculation on the Alcubierre background.

**What it would give:** If true, it shows the classical and quantum pictures are consistent — the boundary-mode decomposition identifies the same structure that a semiclassical calculation finds. The negative energy would then have a physical interpretation as vacuum energy of modes restricted by the wall geometry.

**How to test:** Compute $\langle \hat{T}_{\mu\nu} \rangle_\text{ren}$ for a massless scalar field on the Alcubierre background with the bubble wall imposing Dirichlet or Neumann boundary conditions. Use spectral zeta-function regularization or the Hadamard point-splitting method. Compare the angular and radial profile to the classical $\rho = -v_s^2/(32\pi G) \cdot (f')^2 (y^2+z^2)/r_s^2$.

### Claim (c): Physical Mechanism [Quantum, Speculative]

**Statement:** The exotic matter required by the Alcubierre metric IS a gravitational Casimir effect. Arranging ordinary matter into the appropriate boundary geometry will spontaneously produce the required negative energy density through quantum vacuum effects, without needing an independent exotic matter source.

**Status:** Highly speculative. Requires Claim (b) plus magnitude estimates showing the effect is large enough.

**What it would give:** A resolution of the exotic-matter problem for subluminal warp drives. The question "how do we manufacture exotic matter?" becomes "what boundary geometry makes the vacuum produce the required stress-energy?"

**Obstacles:** The gravitational Casimir effect is extraordinarily weak (Quach 2015). For ordinary matter boundaries, it is suppressed by $(E_\text{Planck}/E_\text{boundary})^2$ relative to the electromagnetic Casimir effect. Producing planetary-mass-scale negative energy from vacuum effects seems to require either Planck-scale boundary separations (Pfenning-Ford constraint) or an unknown amplification mechanism.

---

## 3. The Semiclassical Bridge

The gap between claims (a) and (b) is bridged by **semiclassical gravity** — the standard framework in which the Einstein equations couple classical geometry to quantum field expectations:

$$G_{\mu\nu} = 8\pi G \, \langle \hat{T}_{\mu\nu} \rangle_\text{ren}$$

This is not speculative physics. It is the accepted framework for:
- Hawking radiation from black holes
- Casimir energy calculations in curved spacetime
- Cosmological particle creation
- The backreaction problem in inflationary cosmology

In this framework, the Alcubierre metric defines a classical background. Quantum fields living on this background have a $\langle \hat{T}_{\mu\nu} \rangle$ that depends on the geometry and on boundary conditions. The boundary-mode decomposition identifies the wall as a boundary; the question is what $\langle \hat{T}_{\mu\nu} \rangle_\text{ren}$ this boundary produces.

### 3.1 What the Semiclassical Calculation Would Involve

**Setup:** Consider a massless scalar field $\phi$ (simplest case) on the Alcubierre background, with the bubble wall at $r_s = R$ imposing a boundary condition (Dirichlet: $\phi = 0$ on the wall, or Robin: mixed).

**Mode decomposition:** Expand $\phi$ in the eigenmodes of the spatial operator on the domain. Inside the bubble ($r_s < R$), these are spherical Bessel functions $j_l(k_{nl} r_s)$ with eigenvalues determined by the boundary condition at $r_s = R$. Outside ($r_s > R$), modes are unconstrained.

**Vacuum energy:** The renormalized vacuum energy inside the bubble is:

$$E_\text{vac} = \frac{\hbar}{2} \sum_n \omega_n - (\text{free-space reference})$$

This difference can be positive or negative depending on the boundary condition and geometry. For a spherical boundary with Dirichlet conditions, the Casimir energy is repulsive (Boyer 1968), unlike the attractive parallel-plate case.

**Critical question:** Does the spherical bubble geometry produce *attractive* (negative-energy) or *repulsive* (positive-energy) Casimir effects? Boyer (1968) showed that a perfectly conducting spherical shell has a repulsive Casimir energy for the electromagnetic field. This would be the *wrong sign* for the Alcubierre application if it carries over to the gravitational case.

However:
- Boyer's result applies to a perfectly conducting sphere for EM; the gravitational boundary conditions may differ
- The bubble wall is not a sphere in flat space — it is embedded in the Alcubierre geometry, which has nontrivial shift-vector structure
- The gravitomagnetic field is a vector (component of a tensor), not a scalar; its mode structure on a sphere differs from the scalar case
- The relevant quantity is the full $\langle T_{\mu\nu} \rangle$, not just the total energy — the angular distribution matters

### 3.2 Existing Results on the Gravitational Casimir Effect

**Quach 2015** ([arXiv:1502.07429](https://arxiv.org/abs/1502.07429)) computed the gravitonic Casimir effect with non-idealized boundary conditions. Key findings:

- Graviton modes between boundaries DO produce a Casimir-like effect
- For ordinary matter, the gravitational Casimir force is suppressed by a factor of $(G M / r c^2)^2$ relative to the electromagnetic Casimir force — making it negligible for laboratory-scale systems
- Enhanced effects might occur in superconductors via the speculated Heisenberg-Coulomb effect, but this is unconfirmed

**Implication for the project:** The gravitational Casimir effect exists in principle but is meager for ordinary boundaries. The bubble wall would need to be an extraordinarily efficient "gravitational conductor" to produce macroscopic negative energy. What determines the wall's "gravitational reflectivity" is an open question that the mode decomposition (Phase 2) should address.

### 3.3 Quantum Inequalities as Constraints

**Ford & Roman 1995** ([gr-qc/9410043](https://arxiv.org/abs/gr-qc/9410043)) and **Ford & Pfenning 1998** ([gr-qc/9805037](https://arxiv.org/abs/gr-qc/9805037)) established quantum inequalities (QIs) that constrain negative energy densities:

$$\int \rho(t) \, g(t) \, dt \geq -\frac{C}{\tau^4}$$

where $g(t)$ is a sampling function of width $\tau$ and $C$ is a dimensionless constant. These imply:
- Negative energy cannot be arbitrarily large for arbitrarily long
- For the Alcubierre metric, the bubble wall thickness must be $\Delta \lesssim$ a few hundred Planck lengths
- The total negative energy exceeds $\sim 10^{11} M_\text{universe}$ under these constraints

**But there is a subtlety.** Ford & Roman derived *difference inequalities* — bounds on $\langle T_{\mu\nu} \rangle_\psi - \langle T_{\mu\nu} \rangle_\text{Casimir}$ — that are less restrictive than absolute QIs. If the boundary-mode program identifies the Alcubierre vacuum state as a Casimir-type state, then the relevant constraint is the difference QI, not the absolute QI. The Casimir vacuum itself can have $\langle \rho \rangle < 0$ of any magnitude; only *further* deviations from it are constrained.

This does not solve the energy problem — the Casimir vacuum energy itself must still match the required $\rho$ — but it shows that QIs do not automatically forbid the boundary-mode interpretation.

---

## 4. The Spin-2 Question

The deepest conceptual issue is not quantum vs. classical but **spin-2 vs. spin-1**.

The Casimir effect is well-understood for:
- Scalar fields (spin-0): simplest case, well-studied
- Electromagnetic fields (spin-1): the standard Casimir effect, experimentally confirmed
- Graviton fields (spin-2): computed by Quach 2015, extremely weak

The boundary-mode proposal requires the Casimir mechanism to work for the **gravitomagnetic sector of the metric perturbation** — effectively a vector field constrained by tensor (spin-2) gauge symmetries.

Key differences from EM (per Costa & Natário 2014):

| Property | EM (spin-1) | Gravity (spin-2) |
|----------|------------|-----------------|
| Coupling constant | $e$ (charge) | $\sqrt{G} m$ (mass) |
| Sign of like-charge interaction | Repulsive | Attractive |
| Gravitomagnetic correction factor | — | Factor of 4 relative to gravitoelectric |
| Gauge symmetry | $U(1)$ | Diffeomorphism invariance |
| Boundary conditions | Well-defined (conductor, dielectric) | Unclear — what is a "gravitational conductor"? |

The last row is the crux. In EM, a conductor imposes Dirichlet boundary conditions on the tangential electric field. What imposes analogous boundary conditions on the gravitomagnetic field? Options include:

1. **A material boundary with extreme stiffness** (the bubble wall as a rigid mass shell)
2. **A horizon or trapped surface** (but subluminal bubbles don't have horizons)
3. **A topological boundary** (the wall as a domain wall in a field theory)
4. **Nothing** — the bubble wall may not impose boundary conditions on graviton modes at all, in which case the Casimir analogy breaks down

This is an open question that Phase 2 must address before the project can claim physical content beyond the geometric classification (Claim a). **RESOLVED (Session 34, 2026-07-02): see §8 — options 1–3 are foreclosed and option 4 ("nothing") is the answer; even granting a perfect boundary, the magnitude falls ~64–70 OoM short. Path 2B closed as a physical mechanism.**

---

## 5. A Possible Resolution: The "Effective Boundary" Argument

There is one path that might resolve the quantum/classical gap without requiring a full QFT calculation:

**The stress-energy tensor is a classical object.** The Einstein equations relate geometry to stress-energy, period. If a particular matter configuration (a mass shell, a plasma, an EM field) produces a stress-energy tensor with the structure

$$T_{\mu\nu} = T_{\mu\nu}^\text{shell}(\text{positive, at wall}) + T_{\mu\nu}^\text{field}(\text{negative, at wall})$$

where the negative piece arises from classical field energy stored in a boundary-constrained configuration, then no quantum mechanics is needed. The negative energy is classical field energy, not vacuum energy.

This is exactly what **Fuchs et al. 2024** found: a matter shell plus a shift-vector distribution satisfying all energy conditions. Their construction does not invoke quantum effects. It uses a positive-energy shell that creates the boundary, and the shift-vector (gravitomagnetic field) in the shell's presence produces the warp geometry.

**The boundary-mode decomposition may connect to Fuchs et al. rather than to Casimir.** The mode structure of the gravitomagnetic field constrained by the shell boundary may explain *why* the Fuchs et al. construction works — the shell imposes boundary conditions that select the mode configuration producing warp-type shift vectors. The "negative energy" in the classical Alcubierre analysis may be an artifact of computing stress-energy without the shell, i.e., asking what sources the field configuration without including the boundary that actually constrains it.

If this interpretation is correct:
- Claim (a) is established (geometric classification)
- Claim (b) becomes a question about classical field theory, not QFT
- Claim (c) shifts from "Casimir effect produces exotic matter" to "the right boundary geometry makes ordinary matter produce warp fields"

This reframing is less dramatic than the Casimir story but more plausible and more directly testable against existing results.

---

## 6. Recommended Path Forward — Two-Track Strategy (updated 2026-04-15)

After the April 15 session, the project adopted a **dual-track strategy** on this core issue. Path 2A (classical matter shell, anchored to Fuchs et al. 2024) is the **primary** research track. Path 2B (Casimir / semiclassical) continues in **parallel**. Full details in `MATTER_SHELL_PATH.md` and Phase 2 of `ROADMAP.md`.

### Path 2A — Classical Matter Shell (primary)

**Premise:** The negative energy in the Alcubierre analysis is an artifact of computing stress-energy without the physical shell that creates the boundary. Replace the idealized Alcubierre geometry with a physical shell + interior shift (Fuchs et al. 2024 construction). All energy conditions are satisfied.

**Status:** Existence result established by Fuchs et al. at $\beta_\text{warp} = 0.02c$, $M = 4.5 \times 10^{27}$ kg, $R = 10$–$20$ m. Boundary-mode framework maps cleanly onto their construction (see `MATTER_SHELL_PATH.md` §2).

**Open problems:**
- Scaling of maximum shift amplitude with shell parameters (partially derived in `matter_shell.ipynb` §5)
- Full thin-shell Israel junction with shift-perturbed interior (pending — `ROADMAP.md` Task 2A.6)
- Acceleration without negative energy (hard open; `ROADMAP.md` Task 2A.10)

### Path 2B — Casimir / Semiclassical (parallel)

**Premise:** The Casimir analogy is physical, not merely structural. The Alcubierre exotic-matter requirement is the classical limit (or semiclassical projection) of a Casimir-like mode structure for gravitational fields constrained by a boundary.

**Status:** Not yet pursued beyond the analysis in this document. Specific targets listed in `ROADMAP.md` Phase 2B.

**Open problems:**
- Spin-2 boundary conditions (the "gravitational conductor" question, §4 above)
- Boyer sign problem — repulsive EM Casimir on spheres may indicate wrong sign for gravity
- Renormalization of $\langle \hat{T}_{\mu\nu}\rangle$ on a non-trivial background

### Relationship Between the Two Tracks

The paths are **complementary, not mutually exclusive**. Four possible outcome combinations (see `MATTER_SHELL_PATH.md` §6):

| Path 2A | Path 2B | Interpretation | Status (2026-04-16) |
|---------|---------|----------------|---------------------|
| Succeeds at useful amplitudes | — | Classical matter is sufficient; Casimir analogy becomes a reinterpretation | **Falsified for acceleration** by `acceleration.ipynb` Task 2A.10 |
| Succeeds only at small amplitudes | Succeeds for the gap | Hybrid: classical bulk + quantum sliver | Open for *static* configurations (supported by Packages 1 and 2) |
| Fails at translation; only static frame-drag | Succeeds | Casimir mechanism required for acceleration | **Current best-supported scenario.** Packages 1–2 confirm static viability; Package 3 confirms dynamical failure under classical-matter-only assumptions |
| Fails generically | Fails generically | Rigorous no-go result | Ruled out for static problem by Packages 1–2 |

**Path 2A status summary (2026-04-16).** Packages 1 and 2 of the Path 2A plan (`ROADMAP.md` Phase 2A) have confirmed the **static** classical realisation: DEC-compatible matter shells exist with $\Delta_{\min}/R = \kappa\beta/C$, $\kappa \in [0.05, 0.75]$. Package 3 (`acceleration.ipynb`, Task 2A.10) has falsified the simplest **dynamical** realisations: no classical mechanism simultaneously preserves DEC, keeps the exterior vacuum, requires no expelled reaction mass, and produces $\Delta v \sim v_{\rm warp}$. The obstruction catalog (Mechanisms A/B/C in `MATTER_SHELL_PATH.md` §7.2) is the reason we are now in row 3 of the table above: static classical shells yes, classical acceleration to warp speeds no, quantum / boundary-mode acceleration still open.

The refined Claim (c) from §2 of this document can therefore take two forms:

- **(c-classical)** "The right boundary geometry makes ordinary matter produce warp fields." — Path 2A version. **Confirmed for static, falsified for dynamical under DEC+vacuum+no-ejecta.**
- **(c-quantum)** "The Casimir effect on an appropriate gravitational boundary produces the exotic matter required for warp drives." — Path 2B version. ~~Open, and elevated in importance: it is now the sole remaining candidate for a vacuum+DEC+dynamical realisation.~~ **CLOSED (Session 34, Task 2B.8 — see §8): no gravitational conductor exists in known physics, and even a perfect one falls ~64–70 OoM short of the certified density targets. Within 4D semiclassical GR there is no known candidate for a vacuum+DEC+dynamical realisation; what remains are the Phase 2E relaxations (modified gravity, exotic field content).**

Path 2A (c-classical) is the more conservative; its static half is done within the tested slice and its dynamical half is closed within the same slice. Path 2B (c-quantum) is *one* remaining candidate for a genuine warp drive. Phase 2C (added Session 9; see [`ROADMAP.md`](ROADMAP.md) and [`NAVIGATOR.md`](NAVIGATOR.md)) explored six adjacent slices that test whether the static-slice negative result is an artefact of a specific assumption: alternate shift families, hybrid Krasnikov+matter walls, time-dependent acceleration, Krasnikov 2003 QI loosening, cosmological exterior, and modified gravity. **Path 2B and Phase 2C are parallel candidates, not a single "only remaining route."** The honest summary is that within the static slice we tested, no useful classical positive-matter warp drive exists; outside the slice, several published constructions (Lentz 2020, Fell-Heisenberg 2021, Lobo-Oliveira f(R) wormholes, Garattini-Zatrimaylov de Sitter) face interpretation-dependent caveats and are open candidates. See [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md) for the synthesis.

### Session-7 update (2026-04-16): Rodal 2025 sharpens the Path 2B target

The literature sweep that followed `speculation/RING_NETWORK_CONCEPT.md` surfaced **Rodal 2025** (arXiv:2512.18008, Gen. Rel. Grav. **58**, 1 (2026)), the first explicit kinematically irrotational Natário-class warp drive. Detailed evaluation in `RODAL2025_EVALUATION.md`. The findings change Path 2B's search direction in a useful way:

- Rodal's irrotational drive has stress-energy that is **globally Hawking–Ellis Type I** with a well-defined timelike eigenvalue everywhere — no Type IV pockets like Alcubierre or Natário.
- Peak proper-energy *deficit* is reduced by **≈38× vs. Alcubierre and ≈2,600× vs. Natário** at identical $(\rho, \sigma, v/c)$.
- **However, NEC, WEC, DEC, SEC are still all violated.** The deficit is now driven by **anisotropic transverse principal pressures** $p_2 = \lambda_{G(2)}/\kappa$ and $p_3 = \lambda_{G(3)}/\kappa$ becoming negative on the wall, while the proper energy density $\rho_p$ is positive on-axis. Quoting Rodal (Sec. 6.2.1): *"these large transverse negative pressures are responsible for $\rho_p + p_k < 0$, thus violating the NEC, even though $\rho_p$ is positive at $\theta = 0$."*

This is a *qualitatively different* stress-energy profile from Alcubierre's isotropic negative density, and it is **much closer to what real anisotropic-Casimir setups produce**:

- **Asymmetric-plate Casimir** (one perfect conductor, one dielectric or magnetic) produces anisotropic stress with a different sign for transverse vs. normal directions.
- **Waveguide-confined modes** (e.g., between coaxial cylinders or in a torus) produce direction-dependent vacuum stresses with both signs accessible.
- **Repulsive Casimir geometries** (Boyer 1968 spherical conductor; recent metamaterial proposals) demonstrate that sign-engineering of $\langle T_{\mu\nu}\rangle$ is possible in vacuum.

**Updated Path 2B priority targets:** The Path 2B literature pull (Tasks 2B.1–2B.5) should now be re-targeted away from generic "isotropic vacuum energy" proposals (which match Alcubierre but not Rodal) and toward **anisotropic vacuum stresses with positive normal energy density and negative transverse pressure**, which match Rodal. This is a meaningful narrowing of the search.

The matrix above is unchanged in row assignments, but the *content* of row 3 (now-confirmed best-supported scenario) is refined: "Casimir mechanism required for acceleration" should be read as "an *anisotropic* Casimir mechanism, matching the Rodal stress-energy profile, is the most plausible quantum supplement," not as "isotropic negative-energy Casimir."

### Cross-cutting tasks

- Read Quach 2015 for gravitational Casimir magnitudes (relevant to 2B)
- Read Costa & Natário 2014 for spin-2 differences (relevant to 2B)
- Read Lentz 2020 and Natário 2002 as alternative classical constructions (relevant to 2A)
- Use Warp Factory (arXiv:2404.03095) to validate both paths numerically (relevant to both)
- **(Session 7, new)** Pull literature on **anisotropic Casimir stresses**: asymmetric plates, waveguide-confined modes, repulsive geometries. Target: identify a QFT setup whose $\langle T_{\mu\nu}\rangle$ has the same algebraic structure as Rodal's wall stress-energy (positive proper energy density on-axis, negative transverse pressures on the wall, globally Type I).

---

## 7. References Added by This Analysis

| Paper | arXiv | Relevance |
|-------|-------|-----------|
| Quach 2015 | [1502.07429](https://arxiv.org/abs/1502.07429) | Gravitational Casimir effect with real boundaries |
| Ford & Pfenning 1998 | [gr-qc/9805037](https://arxiv.org/abs/gr-qc/9805037) | Quantum inequalities in curved spacetime; Alcubierre constraints |
| Ford & Roman 1995 | [gr-qc/9410043](https://arxiv.org/abs/gr-qc/9410043) | Difference inequalities relative to Casimir vacuum |
| Boyer 1968 | doi:10.1103/PhysRev.174.1764 | Casimir energy of a conducting sphere (repulsive — sign issue) |
| Costa & Natário 2014 | (see LITERATURE.md) | Spin-2 vs spin-1 catalog |
| Birrell & Davies 1982 | textbook | QFT in curved spacetime methods |
| Fulling 1989 | textbook | Spectral methods for Casimir energy |
| Fuchs et al. 2024 | [2405.02709](https://arxiv.org/abs/2405.02709) | Matter-shell warp drive — possible classical realization of boundary-mode picture |

---

## 8. Task 2B.8 — Spin-2 Obstruction Assessment (Session 34, 2026-07-02): Path 2B CLOSED as a physical mechanism

This section is the canonical record of the Task 2B.8 assessment — the gate on Tasks 2B.1–2B.7 that §4 posed and the ROADMAP decision point anticipated ("if the spin-2 obstruction is insurmountable → document the no-go and close Path 2B"). Three independent legs; the third is decisive on its own.

### 8.1 Leg 1 — no material "gravitational conductor" exists in known physics *(literature; grade B)*

The reason EM conductors exist is that EM reflectivity can be engineered: the coupling is to charge, and a material's conductivity can be made effectively infinite at the relevant frequency. Gravity has no analogous dial — the graviton couples to stress-energy with the universal strength $G$, so a material's "gravitational conductivity" is bounded by its mechanical response. Quantitatively, two uncontested facts close the door for ordinary matter:

- **Impedance mismatch.** The gravitational characteristic impedance of free space is $Z_G \sim 2.8 \times 10^{-18}$ SI; a material must present impedance *below* this to reflect appreciably, and all classical matter is dozens of orders of magnitude above it. This statement is made most plainly in the pro-mirror school's own papers: "all ordinary classical matter is essentially completely transparent to gravitational waves" (Minter–Wegter-McNelly–Chiao 2010, arXiv:0903.0661).
- **Absorption bound.** Dyson 2013 ("Is a graviton detectable?", the Poincaré lecture): graviton absorption cross-sections in matter are of order $10^{-41}\,\mathrm{cm^2/g}$ (keV scale), the graviton mean free path exceeds astrophysical scales, and any detector dense enough to absorb single gravitons collapses into a black hole first. Matter — and the universe — is transparent to gravitational waves back to the Planck era (concordant with the Weinberg-era absorption estimates).

Of §4's four candidate boundary types this forecloses **1 (stiff material shell)** and **3 (matter-based domain wall)**; **2 (horizons)** was already excluded for subluminal bubbles in §4 (and horizons *absorb* rather than reflect coherently).

### 8.2 Leg 2 — the superconductor loophole is speculative, contested, and unobserved *(literature; grade B)*

The only claimed evasion of Leg 1 is the "Heisenberg–Coulomb (H-C) effect" programme: Minter–Wegter-McNelly–Chiao 2010 (thin superconducting films specularly reflect microwave-frequency GWs via non-geodesic Cooper-pair motion), continued in Inan–Thompson–Chiao 2017 (gravitational Meissner-like DC expulsion), and adopted conditionally by **Quach 2015** (PRL 114, 081104) — whose gravitonic Casimir effect for *ordinary* matter is itself meagre, and whose observable superconductor prediction is explicitly framed as a **test of the H-C hypothesis**, not a consequence of established physics (the 2017 erratum, PRL 118, 139901, corrected a units error only). §3.2 of this document should be read with that conditionality in mind. Status of the H-C claim:

- It originates from and remains confined to essentially one research programme plus adopters; the broader superconductor-gravity literature is openly contradictory (the 2022 review arXiv:2203.09417 catalogs ~18 papers by 20+ authors over 55 years with conflicting results, including the Harris–Kowitt finding that the earlier Li–Torr enhancement claims are not credible).
- There is **no experimental support** for any anomalous superconductor–gravitational-wave interaction.
- Later work within the same programme (Inan et al. 2022, arXiv:2207.08062) models the Cooper-pair density response to a GW as *far smaller* than the ionic lattice's — i.e. even the originating school's refined treatment does not reproduce the original enhancement mechanism as claimed.
- Even taken at face value, the claim concerns reflection of *microwave-frequency radiation* by thin films — it is not a design for a static negative-energy cavity at metre scale.

### 8.3 Leg 3 — the even-if magnitude bound *(decisive; grade A within slice; harness [`verification/test_2b8_casimir_gap.py`](verification/test_2b8_casimir_gap.py))*

Grant Path 2B everything Legs 1–2 deny: a **perfect graviton mirror** (reflectivity 1) and a **favourable sign** (waive Boyer 1968). The renormalised vacuum-energy density available from boundary confinement of a massless field at separation $d$ is bounded by the dimensional Casimir envelope $|\rho_C| \le K\,\hbar c/d^4$ with $K = O(1)$ (EM parallel plates: $K = \pi^2/720 \approx 0.0137$; we take $K = 1$, generous by ~73×). Against this project's own radial-certified EC scales:

| boundary separation $d$ | $|\rho_C| \le \hbar c/d^4$ | vs certified targets |
|---|---|---|
| 10 m (shell inner radius) | $3.2 \times 10^{-30}$ J/m³ | **67.5–69.6 OoM short** |
| 1 m (wall sub-scale) | $3.2 \times 10^{-26}$ J/m³ | **63.5–65.6 OoM short** |

Certified targets: the canonical-shell in-shell EC-margin scale ~$10^{38}$ J/m³ (Sessions 29–32), the S31 sharp-optimum DEC violation $3.7 \times 10^{39}$, and the shell rest-energy density $\rho c^2 \approx 1.4 \times 10^{40}$. Matching even the smallest of these requires boundary separation $d \approx 1.3 \times 10^{-16}$ m — **sub-proton spacing** ($\sim 10^{19}\,\ell_P$) maintained throughout a metre-scale wall, at which point the Pfenning–Ford wall-thickness constraints (§3.3) and the ordinary-matter composition of any physical mirror reassert themselves. For calibration: the project's Slice-4b closure standard was a 31-OoM shortfall; this is ~2× that in log terms, **and it is independent of how the contested mirror question resolves**. The same bound kills the §6 row-3 role (quantum supplement for *acceleration*): any dynamical supplement must act at the same densities. The §3.3 "difference-QI" door — that a Casimir-type vacuum may carry $\langle\rho\rangle < 0$ unconstrained by absolute QIs — is now quantified: at wall-scale separations the Casimir-state magnitude is what this bound says, ~65 OoM short.

### 8.4 What survives, verdict, and reopening triggers

**Survives:** Claim (a) (geometric classification — a classical theorem, untouched); the §5 "effective boundary" reading (that is Path 2A physics, and it already carried the load via Fuchs et al.); the mode-decomposition mathematics of Tasks 2B.1–2B.6 as a *classification tool* (the ROADMAP decision point's fallback branch), available if ever needed. Claim (b) (semiclassical consistency) remains an academically well-posed QFT question — but with no physical payoff at ~65 OoM, Task 2B.7 would quantify an irrelevantly small effect and stays unfunded.

**Verdict (slice-scoped): Path 2B is CLOSED as a physical mechanism for warp-relevant negative energy — both the static "negative sliver" role and the dynamical/acceleration-supplement role — within 4D semiclassical gravity with standard QFT Casimir scaling at macroscopic boundary scales.** The spin-2 obstruction of §4 stands: no gravitational conductor exists in known physics; and even granting a perfect one, boundary-confinement vacuum energy falls ~64–70 orders of magnitude short of every certified target in this project's slices. Exotica beyond this slice (non-standard field content, modified gravity, trans-QI vacuum states) are Phase 2E.2/2E.3 territory, not Path 2B.

**Reopening triggers:** (i) experimental demonstration of anomalous GW reflection or absorption by any material (e.g. a confirmed H-C effect) — reopens Leg 2 only; Leg 3 still stands; (ii) a demonstrated vacuum state with $|\langle T_{00}\rangle| \gg \hbar c/d^4$ at macroscopic $d$ consistent with quantum inequalities — the only trigger that touches Leg 3; (iii) a horizon-class boundary compatible with a subluminal shell (none known).

### 8.5 References added by this assessment

| Paper | Where | Relevance |
|-------|-------|-----------|
| Dyson 2013, "Is a Graviton Detectable?" | Int. J. Mod. Phys. A 28, 1330041 (Poincaré lecture) | Graviton absorption $\sim 10^{-41}$ cm²/g; single-graviton detectors collapse to black holes; matter transparent |
| Minter, Wegter-McNelly, Chiao 2010 | Physica E 42, 234; [arXiv:0903.0661](https://arxiv.org/abs/0903.0661) | The H-C superconductor-mirror claim; also states the ordinary-matter impedance no-go plainly |
| Inan, Thompson, Chiao 2017 | Fortschr. Phys. 65, 1600066 | Same programme: gravitational Meissner-like DC expulsion |
| Inan et al. 2022 | [arXiv:2207.08062](https://arxiv.org/abs/2207.08062) | Refined same-programme treatment; Cooper-pair response ≪ ionic lattice |
| Gallerati, Modanese, Ummarino 2022 | [arXiv:2203.09417](https://arxiv.org/abs/2203.09417) | Review: 55 years of contradictory superconductor-gravity claims; no experimental support |
| Quach 2017 (Erratum) | PRL 118, 139901 | Units fix to Quach 2015; conclusions (incl. H-C conditionality) unchanged |

---

*This document is intended to be honest about what the project has established, what remains open, and where the analogies might break. The Casimir connection is beautiful and may be correct, but it requires substantially more work to elevate from analogy to mechanism.* **(Session-34 note: §8 above completed that work in the negative direction — the analogy fails as a mechanism at the magnitude level, decisively and independently of the contested mirror physics.)**

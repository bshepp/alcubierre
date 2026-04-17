# Literature Catalog — Alcubierre Boundary-Mode Reformulation

## Status and Scope

This catalog covers all papers referenced in the project seed documents, organized by role. Each entry includes the abstract, publication data, and relevance to the boundary-mode program.

**Last updated:** 2026-04-17 (Session 9 — Phase 2C reframing, Slices 1-4 + audit interleaves #4-8)

---

## 1. Foundational — The Metric and Its Framework

### Alcubierre 1994 — "The warp drive: hyper-fast travel within general relativity"

- **arXiv:** [gr-qc/0009013](https://arxiv.org/abs/gr-qc/0009013)
- **Journal:** Class. Quant. Grav. 11, L73–L77 (1994)
- **Authors:** Miguel Alcubierre

> It is shown how, within the framework of general relativity and without the introduction of wormholes, it is possible to modify a spacetime in a way that allows a spaceship to travel with an arbitrarily large speed. By a purely local expansion of spacetime behind the spaceship and an opposite contraction in front of it, motion faster than the speed of light as seen by observers outside the disturbed region is possible. The resulting distortion is reminiscent of the "warp drive" of science fiction. However, just as it happens with wormholes, exotic matter will be needed in order to generate a distortion of spacetime like the one discussed here.

**Relevance:** Defines the metric $ds^2 = -dt^2 + (dx - v_s f(r_s) dt)^2 + dy^2 + dz^2$ that this project analyzes. The shape function $f(r_s)$, bubble radius $R$, and wall thickness parameter $\sigma$ originate here.

---

### ADM Formalism — Arnowitt, Deser & Misner 1962

- **arXiv:** [gr-qc/0405109](https://arxiv.org/abs/gr-qc/0405109) (2004 reprint with commentary)
- **Original:** In *Gravitation: An Introduction to Current Research* (Wiley, 1962)
- **Authors:** R. Arnowitt, S. Deser, C. W. Misner

**Relevance:** The 3+1 decomposition is the natural setting for the project. The Alcubierre metric is already in ADM form ($\alpha = 1$, $\gamma_{ij} = \delta_{ij}$, $\beta^x = -v_s f$), and the flat spatial slices make the constraint equations exact. Boundary-value problems in GR are most naturally posed in ADM.

---

## 2. Linearized Analysis — Direct Predecessors

### Lobo & Visser 2004a — "Fundamental limitations on 'warp drive' spacetimes"

- **arXiv:** [gr-qc/0406083](https://arxiv.org/abs/gr-qc/0406083)
- **Journal:** Class. Quant. Grav. 21, 5871–5892 (2004)
- **Authors:** Francisco S. N. Lobo, Matt Visser

> "Warp drive" spacetimes are useful as "gedanken-experiments" that force us to confront the foundations of general relativity, and among other things, to precisely formulate the notion of "superluminal" communication. We verify the non-perturbative violation of the classical energy conditions of the Alcubierre and Natario warp drive spacetimes and apply linearized gravity to the weak-field warp drive, testing the energy conditions to first and second order of the non-relativistic warp-bubble velocity. We are primarily interested in a secondary feature of the warp drive that has not previously been remarked upon, if it could be built, the warp drive would be an example of a "reaction-less drive". For both the Alcubierre and Natario warp drives we find that the occurrence of significant energy condition violations is not just a high-speed effect, but that the violations persist even at arbitrarily low speeds. An interesting feature of this construction is that it is now meaningful to place a finite mass spaceship at the center of the warp bubble, and compare the warp field energy with the mass-energy of the spaceship. There is no hope of doing this in Alcubierre's original version of the warp-field, since by definition the point in the center of the warp bubble moves on a geodesic and is "massless".

**Relevance:** **CRITICAL — highest priority reading.** They already performed linearized analysis of Alcubierre and Natario drives. Key findings: (1) energy condition violations persist at arbitrarily low speeds; (2) the linearized framework allows treating the ship as finite mass; (3) the net negative warp field energy must be a significant fraction of ship mass. Must determine overlap with our ADM-based results before claiming novelty. The gravitomagnetic framing and boundary-mode decomposition may still be new contributions.

**NOTE:** Previously cited incorrectly as gr-qc/0410087 (which is a solo Lobo wormhole paper). Corrected in this catalog.

---

### Lobo & Visser 2004b — "Linearized warp drive and the energy conditions"

- **arXiv:** [gr-qc/0412065](https://arxiv.org/abs/gr-qc/0412065)
- **Authors:** Francisco S. N. Lobo, Matt Visser

> "Warp drive" spacetimes are useful as "gedanken-experiments" and as a theoretician's probe of the foundations of general relativity. Applying linearized gravity to the weak-field warp drive, i.e., for non-relativistic warp-bubble velocities, we find that the occurrence of energy condition violations in this class of spacetimes is generic to the form of the geometry under consideration and is not simply a side-effect of the "superluminal" properties. Using the linearized construction it is now possible to compare the warp field energy with the mass-energy of the spaceship, and applying the "volume integral quantifier", extremely stringent conditions on the warp drive spacetime are found.

**Relevance:** Companion paper applying the "volume integral quantifier" to bound warp-field energy. Establishes that energy condition violations are generic, not a superluminal artifact — consistent with our finding that $\rho \leq 0$ at all $v_s$.

---

## 3. Descendant Solutions — Comparison Targets

### Van Den Broeck 1999 — "A 'warp drive' with more reasonable total energy requirements"

- **arXiv:** [gr-qc/9905084](https://arxiv.org/abs/gr-qc/9905084)
- **Journal:** Class. Quant. Grav. 16, 3973–3979 (1999)
- **Authors:** Chris Van Den Broeck

> I show how a minor modification of the Alcubierre geometry can dramatically improve the total energy requirements for a 'warp bubble' that can be used to transport macroscopic objects. A spacetime is presented for which the total negative mass needed is of the order of a few solar masses, accompanied by a comparable amount of positive energy. This puts the warp drive in the mass scale of large traversable wormholes. The new geometry satisfies the quantum inequality concerning WEC violations and has the same advantages as the original Alcubierre spacetime.

**Relevance:** Energy reduction via bubble geometry modification. Test case: does the boundary-mode decomposition recover Van Den Broeck's improvement? If the mode structure changes with bubble geometry in a way that predicts this reduction, that validates the framework.

---

### Natário 2002 — "Warp drive with zero expansion"

- **arXiv:** [gr-qc/0110086](https://arxiv.org/abs/gr-qc/0110086)
- **Journal:** Class. Quant. Grav. 19, 1157–1166 (2002)
- **Authors:** José Natário

> It is commonly believed that Alcubierre's warp drive works by contracting space in front of the warp bubble and expanding space behind it. We show that this expansion/contraction is but a marginal consequence of the choice made by Alcubierre, and explicitly construct a similar spacetime where no contraction/expansion occurs. Global and optical properties of warp drive spacetimes are also discussed.

**Relevance:** Alternative shift-vector construction with $\theta = 0$ everywhere. Second test case for boundary-mode analysis: if the framework applies, it should work for the Natário metric with a different mode spectrum. Also challenges the intuition that expansion/contraction is the warp mechanism.

---

### Lentz 2020 — "Breaking the warp barrier: hyper-fast solitons in Einstein-Maxwell-plasma theory"

- **arXiv:** [2006.07125](https://arxiv.org/abs/2006.07125)
- **Authors:** Erik W. Lentz

> This paper overcomes this barrier by constructing a class of soliton solutions that are capable of superluminal motion and sourced by purely positive energy densities. The solitons are also shown to be capable of being sourced from the stress-energy of a conducting plasma and classical electromagnetic fields. This is the first example of hyper-fast solitons resulting from known and familiar sources, reopening the discussion of superluminal mechanisms rooted in conventional physics.

**Relevance:** Positive-energy soliton warp drive. Key question: does boundary-mode decomposition naturally produce soliton-like (self-reinforcing, localized) solutions under certain boundary conditions? If different boundary conditions on the same domain yield Alcubierre-type (negative energy) vs Lentz-type (positive energy) solutions, the framework becomes a unifying classification tool.

---

### Bobrick & Martire 2021 — "Introducing physical warp drives"

- **arXiv:** [2102.06824](https://arxiv.org/abs/2102.06824)
- **Authors:** Alexey Bobrick, Gianni Martire

> We develop a model of a general warp drive spacetime in classical relativity that encloses all existing warp drive definitions and allows for new metrics without the most serious issues present in the Alcubierre solution. We present the first general model for subluminal positive-energy, spherically symmetric warp drives; construct superluminal warp-drive solutions which satisfy quantum inequalities; provide optimizations for the Alcubierre metric that decrease the negative energy requirements by two orders of magnitude. Conceptually, we demonstrate that any warp drive, including the Alcubierre drive, is a shell of regular or exotic material moving inertially with a certain velocity. Therefore, any warp drive requires propulsion.

**Relevance:** Classification framework for warp drives. Their finding that every warp drive is a material shell moving inertially is directly compatible with the boundary-mode picture (the "shell" IS the boundary). Their subluminal positive-energy solutions are priority comparison targets.

---

### Fell & Heisenberg 2021 — "Positive energy warp drive from hidden geometric structures"

- **arXiv:** [2104.06488](https://arxiv.org/abs/2104.06488)
- **Authors:** Shaun D. B. Fell, Lavinia Heisenberg

> A general decomposition of the defining variables and the corresponding decomposition of the Eulerian energy are studied. A geometrical interpretation of the Eulerian energy is found, shedding new light on superluminal solitons generated by realistic energy distributions. With this new interpretation, it becomes a relatively simple matter to generate solitonic configurations, within a certain subclass, that respect the positive energy constraint.

**Relevance:** "Hidden geometric structures" may relate to the boundary-mode decomposition. Their geometric decomposition of Eulerian energy could be connected to the spectral decomposition of modes on the bubble domain.

---

### Fuchs, Helmerich, Bobrick et al. 2024 — "Constant velocity physical warp drive solution"

- **arXiv:** [2405.02709](https://arxiv.org/abs/2405.02709)
- **Journal:** Class. Quantum Grav. 41, 095013 (2024)
- **Authors:** Jared Fuchs, Christopher Helmerich, Alexey Bobrick, Luke Sellers, Brandon Melcher, Gianni Martire

> We present a solution for a constant-velocity subluminal warp drive that satisfies all of the energy conditions. The solution involves combining a stable matter shell with a shift vector distribution that closely matches well-known warp drive solutions such as the Alcubierre metric. We generate the spacetime metric numerically, evaluate the energy conditions, and confirm that the shift vector distribution cannot be reduced to a coordinate transformation.

**Relevance:** **The closest existing result to what the boundary-mode approach predicts.** A matter shell (= boundary) plus a shift vector (= the field whose modes we decompose) produces a physical warp drive. If the boundary-mode framework can recover this solution as a natural eigenmode configuration, that is strong evidence the approach has content. Priority comparison target alongside Lobo & Visser.

---

## 4. Critical / No-Go Results

### Pfenning & Ford 1997 — "The unphysical nature of 'warp drive'"

- **arXiv:** [gr-qc/9702026](https://arxiv.org/abs/gr-qc/9702026)
- **Journal:** Class. Quant. Grav. 14, 1743–1751 (1997)
- **Authors:** Michael J. Pfenning, L. H. Ford

> We will apply the quantum inequality type restrictions to Alcubierre's warp drive metric on a scale in which a local region of spacetime can be considered "flat". It will be shown that the bubble wall thickness is on the order of only a few hundred Planck lengths. Then we will show that the total integrated energy density needed to maintain the warp metric with such thin walls is physically unattainable.

**Relevance:** Constrains bubble wall thickness to Planck scale and energy to universe-scale. The boundary-mode picture reframes this: the $1/\Delta$ divergence in energy is the gravitational analog of the Casimir divergence for infinitesimally close plates. The question is whether the mode picture changes the thickness/energy trade-off, or whether it merely restates the same constraint in new language.

---

### Santiago, Schuster & Visser 2021 — "Generic warp drives violate the null energy condition"

- **arXiv:** [2105.03079](https://arxiv.org/abs/2105.03079)
- **Authors:** Jessica Santiago, Sebastian Schuster, Matt Visser

> A more careful analysis shows that the situation is actually much grimmer than advertised — all physically reasonable warp drives will violate the null energy condition, and so also automatically violate the WEC, and both the strong and dominant energy conditions. Even in modified gravity, physically reasonable warp drives will still violate the purely geometrical null convergence condition and the timelike convergence condition.

**Relevance:** **The paper the boundary-mode approach must survive.** They show NEC violation is generic to warp drives, not just Alcubierre's specific form. The boundary-mode approach must either: (a) respect their no-go (subluminal, NEC-violating but with Casimir-sourced violation), (b) identify which assumption it challenges, or (c) fail. Their argument applies to all timelike observers, not just co-moving Eulerian ones — a stronger constraint than earlier work.

---

### Ford & Roman 1995 — "Averaged energy conditions and quantum inequalities"

- **arXiv:** [gr-qc/9410043](https://arxiv.org/abs/gr-qc/9410043)
- **Journal:** Phys. Rev. D 51, 4277–4286 (1995)
- **Authors:** L. H. Ford, Thomas A. Roman

> Connections are uncovered between the averaged weak (AWEC) and averaged null (ANEC) energy conditions, and quantum inequality restrictions on negative energy for free massless scalar fields. In a two-dimensional compactified Minkowski universe, we derive a covariant quantum inequality-type bound on the difference of the expectation values of the energy density in an arbitrary quantum state and in the Casimir vacuum state.

**Relevance:** Establishes foundational quantum inequalities. Critically, they derive bounds relative to the *Casimir vacuum state*, not the Minkowski vacuum. This means the Casimir effect is already built into the QI framework as a baseline. If the boundary-mode picture maps to a Casimir vacuum, the relevant QI is the difference inequality — potentially less restrictive than the absolute QI.

---

### Ford & Pfenning 1998 — "Quantum inequality restrictions on negative energy densities in curved spacetimes"

- **arXiv:** [gr-qc/9805037](https://arxiv.org/abs/gr-qc/9805037)
- **Authors:** Michael John Pfenning, L. H. Ford

> We derive a general form of the QI on the energy density for both the quantized scalar and electromagnetic fields in static curved spacetimes. The application of the quantum inequalities to the Alcubierre warp drive spacetime leads to strict constraints on the thickness of the negative energy region needed to maintain the warp drive. Under these constraints, we discover that the total negative energy required exceeds the total mass of the visible universe by a hundred billion times.

**Relevance:** **NEW addition to the project (not in original seed documents).** Extends quantum inequalities to curved spacetime and applies directly to Alcubierre. The result ($|E| > 10^{11} M_\text{universe}$) is the most severe constraint on the warp drive. The boundary-mode approach must confront this. Key question: does the QI in the Casimir vacuum state (which is the boundary-mode's natural ground state) differ from the absolute QI applied here?

---

### Everett 1996 — Causality problems

- **Journal:** Phys. Rev. D 53, 7365 (1996)
- **Authors:** Allen E. Everett
- **arXiv:** Not available on arXiv

**Relevance:** Causality violations from warp drives. The subluminal restriction adopted by this project may avoid these issues.

---

### Hiscock 1997 — Horizon problems

- **Journal:** Class. Quant. Grav. 14, L183 (1997)
- **Authors:** William A. Hiscock
- **arXiv:** Not available on arXiv

**Relevance:** Horizon formation in superluminal Alcubierre spacetimes. Again, subluminal restriction may sidestep this.

---

## 5. Quantum / Classical Bridge — New References

### Quach 2015 — "Gravitational Casimir effect"

- **arXiv:** [1502.07429](https://arxiv.org/abs/1502.07429)
- **Journal:** Phys. Rev. Lett. 114, 081104 (2015)
- **Authors:** James Q. Quach

> We derive the gravitonic Casimir effect with non-idealised boundary conditions. This allows the quantification of the gravitonic contribution to the Casimir effect from real bodies. We quantify the meagreness of the gravitonic Casimir effect in ordinary matter. We also quantify the enhanced effect produced by the speculated Heisenberg-Coulomb (H-C) effect in superconductors, thereby providing a test for the validity of the H-C theory, and consequently the existence of gravitons.

**Relevance:** **KEY paper for the quantum/classical gap.** Establishes that graviton modes between boundaries DO produce a Casimir-like effect, but it is extremely weak for ordinary matter. This means: (a) the structural analogy between EM Casimir and gravitational Casimir is physically realized, not just mathematical; (b) the magnitude is meager unless enhanced by exotic boundary conditions. The boundary-mode program must address whether the warp bubble wall provides sufficient "reflectivity" for graviton modes to produce macroscopic effects.

---

## 6. Numerical Tools

### Helmerich et al. 2024 — "Analyzing warp drive spacetimes with Warp Factory"

- **arXiv:** [2404.03095](https://arxiv.org/abs/2404.03095)
- **Authors:** Christopher Helmerich, Jared Fuchs, Alexey Bobrick, Luke Sellers, Brandon Melcher, Gianni Martire
- **Code:** [github.com/NerdsWithAttitudes/WarpFactory](https://github.com/NerdsWithAttitudes/WarpFactory) (MATLAB, MIT license)

> We introduce Warp Factory: a numerical toolkit designed for modeling warp drive spacetimes. By leveraging numerical analysis, Warp Factory enables the examination of general warp drive geometries by evaluating the Einstein field equations and computing energy conditions.

**Relevance:** Computational platform for Phase 3. Can reproduce standard Alcubierre energy conditions as sanity check. Key question: can it accept arbitrary metric inputs for energy-condition analysis? If so, boundary-mode-predicted metrics can be tested directly.

---

## 7. Textbooks and Non-arXiv References

These are not available for automated retrieval but are referenced in the project documents.

| Reference | Role |
|-----------|------|
| Hawking & Ellis, *The Large Scale Structure of Space-Time* (1973) | Definitive treatment of energy conditions |
| Visser, *Lorentzian Wormholes* (1995) | Comprehensive exotic spacetime reference |
| Jackson, *Classical Electrodynamics* (3rd ed.) | Canonical reference for method of images, dielectric sphere |
| Carroll, *Spacetime and Geometry* (2004) | Standard linearized gravity textbook treatment |
| Morris & Thorne 1988, Am. J. Phys. 56, 395 | First systematic exotic-matter calculation (wormholes) |
| Morris, Thorne & Yurtsever 1988, PRL 61, 1446 | Energy condition violations in exotic spacetimes |
| Birrell & Davies, *Quantum Fields in Curved Space* (1982) | Standard reference for semiclassical gravity / QFT in curved spacetime |
| Fulling, *Aspects of Quantum Field Theory in Curved Space-Time* (1989) | Spectral methods for Casimir energy on bounded domains |
| Costa & Natário 2014, *Gravito-electromagnetic analogies* | Catalog of spin-2 vs spin-1 differences in GEM |
| White 2011, NASA TRS 20110015936 | Canonical form, thick-wall energy reduction |
| Gourgoulhon, *3+1 Formalism in General Relativity* (gr-qc/0703035) | Reference for boundary conditions in 3+1 GR |

---

## 8. Reading Priority

For advancing Phase 1 completion:

1. **Lobo & Visser 2004a** (gr-qc/0406083) — Determine overlap with our linearized results
2. **Lobo & Visser 2004b** (gr-qc/0412065) — Volume integral quantifier for energy bounds
3. **Fuchs et al. 2024** (2405.02709) — Matter shell + shift vector comparison target
4. **Santiago, Schuster & Visser 2021** (2105.03079) — No-go theorem to confront
5. **Quach 2015** (1502.07429) — Gravitational Casimir effect for quantum/classical bridge
6. **Ford & Pfenning 1998** (gr-qc/9805037) — QI constraints in curved spacetime

---

## 9. Static-Infrastructure Prior Art (added Session 7)

This section is added in response to the `speculation/RING_NETWORK_CONCEPT.md` analysis. Krasnikov's 1995 construction and the Everett–Roman 1997 generalization establish that the speculation document's "static infrastructure" thesis is not novel; it is a re-derivation of the Krasnikov tube, including the network construction and its CTC consequence.

### Krasnikov 1995 — "Hyperfast Interstellar Travel in General Relativity"

- **arXiv:** [gr-qc/9511068](https://arxiv.org/abs/gr-qc/9511068)
- **Journal:** Phys. Rev. D 57, 4760 (1998)
- **Author:** S. V. Krasnikov
- **Local copy:** `papers/9511068v6.pdf`

**Relevance:** Original 2D construction of the *static* spacetime tunnel ("Krasnikov tube") connecting two endpoints. Built once by an outbound traveller; once built, any later traveller can use it for arbitrarily fast round trips as measured by Earth clocks. **This is the Mode-B "passenger transport along static infrastructure" idea from `RING_NETWORK_CONCEPT.md` §2.2, predating it by 31 years.** The 2D construction does not yet expose the negative-energy issue — that comes in the 4D extension below.

### Everett & Roman 1997 — "A Superluminal Subway: The Krasnikov Tube"

- **arXiv:** [gr-qc/9702049](https://arxiv.org/abs/gr-qc/9702049)
- **Journal:** Phys. Rev. D 56, 2100 (1997)
- **Authors:** Allen E. Everett, Thomas A. Roman
- **Local copy:** `papers/9702049v1.pdf`

**Relevance:** **CRITICAL prior art for the speculation document.** Three results matter for our project:

1. **4D extension of Krasnikov's 2D construction.** Sec. 3 builds a tube of finite radius $\rho_{\max}$ connecting Earth and Deneb with flat interior and a curved wall of thickness $\epsilon$.
2. **Stress-energy calculation (Sec. 5).** Computes $T_{\mu\nu}$ classically from the metric. Finds: "$T_{tt}$ is negative on the inner side of the wall … changes sign and develops appreciable positive values on the outer side." Concludes: "Krasnikov tubes, like warp bubbles and traversable wormholes, also involve unphysically thin layers of negative energy density, as well as large total negative energies, and therefore probably cannot be realized in practice." **This is a classical (non-QI) result — the same kind we did for the Alcubierre case.**
3. **Network construction and CTC theorem (Sec. 4).** "If Krasnikov tubes could be constructed, one could, at least in principle, establish a network of such tubes forming an interstellar transportation system… A necessary corollary of the existence of such a network is the possibility of backward time travel and the consequent existence of CTCs." Two non-overlapping oppositely-directed tubes form a time machine. **This is the speculation document's Mode-B network idea, with a no-go theorem attached.**

The speculation doc's claim that "static infrastructure approach is novel" is incorrect. Any extension of the speculation requires either (a) confronting Everett–Roman's classical negative-energy result with a Fuchs-style classical thick wall, or (b) constraining all tubes in the network to a single global orientation to avoid CTCs.

**Audit status (TRUST_AUDIT #8, closed Session 9):** §4 (network → CTC theorem) re-read independently. The argument is essentially geometric and convincing: in 3D, two non-overlapping oppositely-oriented tubes constructed at separated cylindrical radii allow a round-trip Earth → Deneb → Earth that arrives backward in time by an arbitrary amount. CTCs are avoided only if all tubes share a single global orientation axis, which defeats the network's purpose. **Audit summary in `KRASNIKOV2003_EVALUATION.md` §"TRUST_AUDIT #8".**

### Krasnikov 2003 — "The quantum inequalities do not forbid spacetime shortcuts"

- **arXiv:** [gr-qc/0207057](https://arxiv.org/abs/gr-qc/0207057)
- **Journal:** Phys. Rev. D 67, 104013 (2003)
- **Author:** S. V. Krasnikov
- **Local copy:** `papers/0207057v3.pdf`

**Relevance:** Pushes back on Pfenning–Ford-style quantum-inequality arguments that ostensibly rule out warp bubbles, Krasnikov tubes, and traversable wormholes. Three lines of attack: (i) the relevant QI does not always imply Planck-scale energy densities (the Weyl/Ricci ratio argument); (ii) large local densities need not imply large total negative energy $|E_{\rm tot}^-|$; (iii) explicit "dihedral portal + Van Den Broeck pocket" construction with $|E_{\rm tot}^-| \sim 10^{-3}$ g, many orders of magnitude smaller than the canonical bound.

**Important caveat for our project: this is a QI counter-argument, not a positive-energy / DEC-satisfying classical construction.** The classical Task 2A.13 result (negative energy in the wall from the local Einstein equations, $\rho_p^{\min} = -0.122 \eta/\epsilon^2$) is unaffected by Krasnikov 2003.

**Slice 4 detailed evaluation: [`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md).** Headline conclusion: the QI bound on $E_{\rm tot}^-$ is substantively weaker than canonical citations suggest, but our classical no-go is independent of QI and stands.

### Visser & Hochberg ~2004 — "Simple and double walled Krasnikov tubes"

- **OSTI:** [biblio/20431521](https://www.osti.gov/etdeweb/biblio/20431521)
- **Status:** Paywalled; no public arXiv preprint located.

**Relevance:** Mass-reduction analysis for Krasnikov tubes. Negative-energy walls remain. Not blocking — Everett–Roman covers the conceptual ground.

### Lobo & Crawford 2002 — "Weak energy condition violation and superluminal travel"

- **arXiv:** [gr-qc/0204038](https://arxiv.org/abs/gr-qc/0204038)
- **Authors:** Francisco S. N. Lobo, Paulo Crawford
- **Local copy:** `papers/arXiv-gr-qc0204038v2.tar.gz` (LaTeX source only)

**Relevance:** Comparative study of WEC violation across Alcubierre warps, Krasnikov tubes, and traversable wormholes. **Verdict (Session 7):** read; the paper reproduces Everett–Roman's stress-energy calculation pedagogically and adds Olum's superluminal-implies-WEC-violation theorem. **It does NOT use a thin-shell (Israel-junction) formalism for the Krasnikov tube, and does NOT address thick-wall regimes.** No prior art for our reframed Calculation 1 here. Olum's theorem is worth knowing about but is a global causal-structure result that doesn't directly bear on our finite-thickness shell question.

### Bobrick & Martire 2021 — "Introducing Physical Warp Drives"

- **arXiv:** [2102.06824](https://arxiv.org/abs/2102.06824)
- **Journal:** Class. Quant. Grav. 38, 105009 (2021)
- **Authors:** Alexey Bobrick, Gianni Martire
- **Local copy:** `papers/2102.06824v2.pdf`

**Relevance:** General framework for warp-drive shells. Two results matter for the speculation analysis: (1) "any warp drive… is a shell of regular or exotic material moving inertially" — i.e., identifies the warp-drive problem with the matter-shell problem (this is the antecedent to the Fuchs construction); (2) **"any warp drive requires propulsion"** — a no-free-lunch theorem that applies to any closed shell topology including toroidal, and which the speculation doc's "Mode A launcher" runs straight into.

**Audit status (TRUST_AUDIT #7, closed Session 9):** §III–IV read independently. Two key statements verified from their text: §III.A shows that for spherically symmetric subluminal positive-matter warp drives, the inner-region time can only pass *more slowly* than at infinity (never faster) — this is the rigorous reason the Alcubierre-class drives need negative energy. §V.B states verbatim *"Whatever is the acceleration mechanism, it must obey the conservation of 4-momentum. This is because all warp drive spacetimes are asymptotically-flat. ... no metric which describes an accelerating warp drive solution has so far been presented in the literature."* This is the rigorous "any warp drive requires propulsion" theorem. Audit summary in `KRASNIKOV2003_EVALUATION.md` §"TRUST_AUDIT #7" and `MATTER_SHELL_PATH.md` Appendix A.

### Krasnikov-Everett network ↔ ring-wormhole literature

- **Garattini, Cardoso et al.** (e.g., [arXiv:2305.03887](https://arxiv.org/abs/2305.03887)) develop ring wormholes with toroidal topology. Distinct from warp shells but worth noting as the closest published work on toroidal exotic-matter geometries. Local copy: `papers/arXiv-2305.03887v1.tar.gz`.

---

## 10. New Warp-Drive Construction Since Session 4 (added Session 7)

### Rodal 2025 — "A warp drive with predominantly positive invariant energy density and global Hawking–Ellis Type I"

- **arXiv:** [2512.18008](https://arxiv.org/abs/2512.18008)
- **Journal:** Gen. Rel. Grav. 58, Article 1 (2026), published Dec 17 2025
- **Author:** José Rodal (Rodal Consulting, single author)
- **Local copy:** `papers/2512.18008v1.pdf` and source `papers/arXiv-2512.18008v1.tar.gz`

**Headline claim.** First *fully explicit, continuous, analytically derived* warp-drive spacetime whose shift is kinematically irrotational. Built on the Santiago–Schuster–Visser observation that $\boldsymbol{\omega} = 0$ gives Hawking–Ellis Type I. Compared to Alcubierre and Natário at identical $(\rho, \sigma, v/c)$:

- Peak proper-energy *deficit* reduced by ≈38× vs. Alcubierre, ≈2.6×10³ vs. Natário.
- Peak NEC violation ≈60× smaller than Natário.
- Globally Type I (well-defined timelike eigenvalue everywhere); other drives have Type IV pockets.
- Net proper energy "consistent with zero to four decimals" after $1/R$ tail extrapolation: $|E_{\rm net}|/E_{\rm abs}(\infty) = 0.04\%$ vs 3.34% in the finite window.

**Construction.** Shift potential $\Phi(r,\theta,t) = v(t) r g(r) \cos\theta$ with $f(r) = 1 - f_{\rm Alc}(r)$, and $g(r)$ given by an explicit hyperbolic-function formula (their Eq. (g(r))). This is a Natário-class drive (zero asymptotic motion of distant stars) with kinematic irrotationality replacing zero divergence.

**What it does *not* do** (own admission, §"Limitations"):
- Energy conditions are still violated. NEC, WEC, DEC, SEC all fail (their Eq. (hierarchy)). Peak NEC violation $\lambda_{G(2)} - \lambda_{G(0)} \approx -4 \, \mathrm{m}^{-2}$ on-axis, driven by large *transverse negative pressures*.
- The "net proper energy ≈ 0" is an *integrated proper energy* statement, not an ADM/Komar mass. Quoting the paper directly (§ "Physical remark on near cancellation"): "*This statement concerns the proper energy density defined by the timelike eigenvalue of $T^\mu{}_\nu$; it does not, by itself, establish a vanishing ADM or Komar mass, which require global geometric fluxes/constraints beyond the local energy density.*"
- All quantitative results assume **constant velocity** ($v(t) \to v$), unit lapse, flat static spatial slices. The acceleration problem we analyzed in Path 2A Package 3 is *not* addressed; the paper notes that "letting $\alpha$ or $v$ vary in time… can reintroduce off-diagonal fluxes in mixed components and creating Type IV pockets."
- The tail extrapolation is a two-point $1/R$ fit using $R_1 = 8\rho$, $R_2 = 12\rho$. The baseline $E_-(12\rho) = 1.21\times10^{44}$ J extrapolates to $E_-(\infty) = 1.33\times10^{44}$ J — a ~10% extrapolation. Reasonable but not negligible.
- Single-author, no institutional affiliation listed beyond consulting practice. Peer-reviewed at Springer/GRG.

**Relevance to our project.** See `RODAL2025_EVALUATION.md` for the full assessment. Summary:

1. **Does NOT solve the Path 2A "translation impossibility" finding.** Rodal's analysis is at constant velocity. The acceleration obstruction we proved in `acceleration.ipynb` (no in-vacuum self-acceleration mechanism for a closed shell of classical DEC matter) is independent of the energy budget of the *moving* steady-state metric.
2. **Does NOT establish a positive-energy warp drive.** The headline "net proper energy ≈ 0" does not say negative-energy regions are absent — they're 70% of the volume, and NEC is still violated everywhere on the wall by anisotropic transverse pressures. A classical-matter source would still be incompatible.
3. **Does extend the moving-bubble design space.** If quantum-field sources can be found that mimic the irrotational stress-energy distribution (positive proper energy density on-axis, negative transverse pressures concentrated on the wall), the *integrated* energy budget collapses by ~38× compared to Alcubierre. This could lower the threshold for our Path 2B (Casimir/boundary mode) program if such modes can produce anisotropic-pressure stress-energies.
4. **The Hawking–Ellis Type I block-diagonal structure is the most useful theoretical takeaway for us.** It means the moving Natário-class warp can be analyzed with standard energy-condition tools (positive $\rho_p$, three real principal pressures) rather than the more pathological Type IV sectors. This simplifies any future thin-shell analysis of irrotational warps.

**Action items for our project:**
- Adopt Rodal 2025 as a new comparison target alongside Fuchs 2024 in `MATTER_SHELL_PATH.md` § Comparison.
- Re-evaluate whether our Path 2B (Casimir) program should target *anisotropic transverse pressures* on a thin wall (matching Rodal's profile) rather than isotropic negative energy density (matching Alcubierre's profile). This is a meaningful change of search direction.
- Note in `QUANTUM_CLASSICAL_BRIDGE.md` outcome matrix: the irrotational construction strengthens scenario "C — fails at translation; only static frame-drag" (because translation still costs propulsion per Bobrick–Martire even if the steady-state drive is cheap), but weakens scenario "D — energy conditions impassable" since the *peak* deficit just dropped by orders of magnitude.

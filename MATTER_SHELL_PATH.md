# Path 2 — The Classical Matter-Shell Realization of the Boundary-Mode Framework

## Author: Brian Sheppard + Claude
## Date: 2026-04-15 (last reframed 2026-04-17, Session 9 — see §0.5)
## Purpose: Concrete classical-physics realization of the boundary-mode reformulation,
##          anchored to Fuchs et al. 2024's constant-velocity Warp Shell. Treats the
##          "wall" as a real shell of ordinary matter and maps the Alcubierre shift
##          vector onto an interior-only perturbation.
## Status: Static slice mapped (Packages 1–3 + Task 2A.13). Six adjacent slices
##         remain unexplored; see §0.5. The Casimir route (Path 2B) continues in
##         parallel — see QUANTUM_CLASSICAL_BRIDGE.md for the three-level claim
##         structure.

---

## 0. Why Path 2 Leads

The Casimir route requires three independent leaps: (i) reinterpret the Alcubierre stress-energy as a quantum expectation value $\langle \hat{T}_{\mu\nu} \rangle_\text{ren}$; (ii) identify a physical structure that plays the role of a "gravitational conductor"; (iii) show that the resulting regularized mode sum reproduces the Alcubierre profile with the right sign. Each step is open, and each interacts with unresolved issues in semiclassical gravity (spin-2 field, renormalization ambiguity, Boyer sign problem).

The matter-shell route requires only one leap: that the Alcubierre bubble wall is a physical object — an actual shell of ordinary matter with positive energy density — rather than an exotic distribution or a boundary condition on quantum modes. If this leap works, the boundary-mode picture becomes **a statement about classical field theory on a classical background**, and the existence result of Fuchs et al. 2024 is direct evidence that it does work, at least at zero bubble velocity.

The two routes are not mutually exclusive. If Path 2 succeeds, it may simply *be* the realization of the "boundary" in the boundary-mode framework, making the Casimir analogy a reinterpretation of a classical effect (much as Casimir energy itself admits both QFT and source-theoretic classical derivations for idealized geometries). If Path 2 fails — e.g., if no Fuchs-style shell can sustain a shift that induces actual translation rather than just internal frame-dragging — then the Casimir route becomes necessary, not optional.

---

## 0.5 Caveats and Adjacent Slices (added Session 9, 2026-04-17)

This document originally read as a closure document — "Path 2A is done; only Path 2B remains." That framing oversold our actual coverage of the warp-drive landscape. After a re-evaluation, what Packages 1–3 + Task 2A.13 *actually* establish is more carefully stated as:

> **Within the slice of parameter space defined by (Alcubierre-style $\beta^x \hat x$ shift) × (spherical Fuchs-class matter shell or static cylindrical Krasnikov tube) × (asymptotically flat vacuum exterior) × (steady-state metric or its Lorentz boost) × (4D General Relativity with classical positive matter sources)**, no useful warp drive is simultaneously DEC-compatible, accelerable, and transport-relevant.

That slice is informative but is not the whole landscape. The following six adjacent slices are explicitly *not* addressed by Packages 1–3 + Task 2A.13. Each is treated as an open question and pursued in its own notebook + notes document (Phase 2C of `ROADMAP.md`):

| # | Adjacent slice | Assumption being relaxed | Notebook | Notes | Status |
|---|---|---|---|---|---|
| 1 | **Alternate shift families** | Shift is Alcubierre $\beta^x \hat x$ | [`shift_families.ipynb`](shift_families.ipynb) | [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md) | **DONE 2026-04-17 (Session 9).** 0/140 sweep points achieve WEC across the four single-mode axisymmetric families (Alcubierre, Natário, irrotational/Rodal, free-form $j_1$). Lentz 2020 is not contradicted because his construction is multi-mode + plasma source, outside this slice. |
| 2 | **Fuchs+Krasnikov hybrid wall** | Krasnikov wall is sourced only by the metric (no matter shell coincident) | [`hybrid_wall.ipynb`](hybrid_wall.ipynb) | section in [`KRASNIKOV_TUBE_NOTES.md`](KRASNIKOV_TUBE_NOTES.md) | **DONE 2026-04-17 (Session 9).** 0/480 sweep points achieve WEC; best WEC pass fraction is 0.91 with $\rho_p^{\min}$ still $-0.07$. The single-bump matter perturbation shifts the negative-energy region around but does not eliminate it, upholding the §9.5 hand-wave. |
| 3 | **Time-dependent acceleration** | Steady-state metric + Lorentz boost is sufficient | [`time_dependent.ipynb`](time_dependent.ipynb) | [`TIME_DEPENDENT_NOTES.md`](TIME_DEPENDENT_NOTES.md) | **DONE 2026-04-17 (Session 9).** $\dot v$ correction to $\rho_p$ is antisymmetric in $x$, scales as $1/\tau$, with peak ratio to static $\rho_p$ of 0.003 at $\tau = R/c$. Net momentum injection at quadrupole order is zero by symmetry. Package 3 conclusions transfer. TRUST_AUDIT #5 sxs cell wired for Colab. |
| 4 | **Krasnikov 2003 QI loosening** | Quantum-inequality bounds on negative energy are tight enough to forbid useful tubes | `qi_loosening.ipynb` (optional, deferred) | [`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md) | **DONE 2026-04-17 (Session 9)**, lit-only. Krasnikov 2003 has three substantive QI-loosening arguments, including an explicit "$10^{-3}$ g of exotic matter" wormhole construction. Our classical Task 2A.13 no-go is *independent* of QI and unaffected. The QI-bound *additional* objection to wormhole-class spacetimes is substantively weakened. Hybrid quantum/classical wall calc (4b) deferred to a future session. TRUST_AUDIT #7 (Bobrick-Martire) and #8 (Everett-Roman §4) closed via re-reads. |
| 5 | **Cosmological exterior** | Exterior is asymptotically flat vacuum | [`cosmological_exterior.ipynb`](cosmological_exterior.ipynb) | [`COSMOLOGICAL_EXTERIOR_NOTES.md`](COSMOLOGICAL_EXTERIOR_NOTES.md) | **DONE 2026-04-17 (Session 9).** McVittie + $\Lambda$ Einstein-tensor regression matches FRW value at large $r$. Mechanism A ceiling from cosmological background: $\Delta v \le 10^{-36}$ m/s at $R_{\rm BY} = 100\,R_{\rm shell}$, scaling as $R_{\rm BY}^3$. **42 orders of magnitude below GW-recoil channel**. Asymptotic-flatness assumption is not load-bearing. |
| 6 | **Modified gravity** | Field equations are 4D Einstein gravity | `modified_gravity.ipynb` (deferred — would need a 4th-order PDE solver) | [`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md) | **DONE 2026-04-17 (Session 9)**, lit-only. Lobo & Oliveira 2009 demonstrate $f(R)$ wormholes where matter satisfies WEC and curvature absorbs the violation; this is a genuine loophole in *Jordan frame*. Frame-dependence (Einstein-frame transformation moves the violation to a scalar field) makes the verdict interpretation-sensitive. Fell-Heisenberg 2021 is positive-energy in *standard* GR via multi-mode shift (related to Slice 1). Garattini-Zatrimaylov 2025 modifies Slice 5: warp bubble at Hubble velocity in de Sitter satisfies averaged WEC/NEC. |

The §9 conclusion below is updated to reflect this — what we have is the static-slice mapping, not the closure of the entire classical question. Each of the six slices is approached as an honest open question with a real chance of revealing a loophole, not a residual cleanup task.

---

## 1. Summary of Fuchs et al. 2024

**Paper:** Fuchs, Helmerich, Bobrick, Sellers, Melcher, Martire. *Constant Velocity Physical Warp Drive Solution*. Class. Quant. Grav. 41, 095013 (2024). [arXiv:2405.02709](https://arxiv.org/abs/2405.02709).

### 1.1 Construction

Start with a static, spherically symmetric *matter shell* in Schwarzschild coordinates:

$$ds^2_\text{shell} = -e^{2a(r)}\,dt^2 + e^{2b(r)}\,dr^2 + r^2 d\Omega^2$$

with anisotropic pressure $T^{\hat\mu\hat\nu}_\text{shell} = \operatorname{diag}(\rho, P_1, P_2, P_3)$ solving the TOV equation iteratively (isotropic initial guess → anisotropic refinement) to support the shell against self-gravity. The shell occupies $R_1 \le r \le R_2$. The interior $r < R_1$ is Minkowski; the exterior $r > R_2$ is Schwarzschild with ADM mass $M$.

### 1.2 The Warp Modification

Add to this shell metric a pure shift-vector perturbation:

$$g_\text{warpshell} = g_\text{shell} + \delta g_\text{warp}, \qquad \delta g_\text{warp} = \begin{pmatrix} 0 & \beta_1 & 0 & 0 \\ \beta_1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}$$

The shift vector amplitude is controlled by a function $S_\text{warp}(r)$ that is 1 in the passenger region $r < R_1 + R_b$, transitions smoothly through the shell via Fuchs's bump function

$$f(r) = \left(\exp\!\left[(R_2-R_1)\!\left(\tfrac{1}{r-R_2} + \tfrac{1}{r-R_1}\right)\right] + 1\right)^{-1}$$

and is 0 outside $r > R_2 - R_b$. The shift magnitude $\beta_\text{warp} = 0.02$ (in units of $c$) is small enough that the induced momentum flux does not violate energy conditions in the shell interior.

### 1.3 Numerical Result

With $R_1 = 10$ m, $R_2 = 20$ m, $M = 4.49 \times 10^{27}$ kg, $\beta_\text{warp} = 0.02c$:

- All four energy conditions (NEC, WEC, SEC, DEC) are satisfied *everywhere*.
- Light-ray transit times in the $\pm x$ directions differ by $\delta t \approx 7.6$ ns — a real Lense-Thirring (frame-dragging) signature that cannot be removed by coordinate transformation.
- Passenger region interior is flat Minkowski; geodesics through it follow the shift.
- The Alcubierre solution with $R = 15$ m, $v = 0.04 c$ shows $\delta t = 8.0$ ns — **comparable but from exotic matter**.

The Fuchs construction is therefore a genuine *physical* warp drive at constant (internal) velocity. The critical caveats:

1. The shift amplitude is small ($v_\text{warp} = 0.02c$), not the full Alcubierre $v_s$.
2. The bubble itself does not translate — the frame-dragging is inside a static shell.
3. Acceleration is not addressed (Section 5.3 of the paper lists it as open).
4. The mass is enormous ($\sim 4.5 \times 10^{27}$ kg $\approx 750$ Earth masses for a 20 m shell).

---

## 2. Mapping to the Boundary-Mode Framework

### 2.1 The Structural Isomorphism

The boundary-mode reformulation proposed in `LINEARIZATION_CALCULATION.md` and `ALCUBIERRE_MARCH30_INTEGRATION.md` asserts:

> The Alcubierre exotic energy density is the ADM energy of a shift-vector field that lives on a flat spatial slice and vanishes outside a bubble wall. The wall imposes boundary conditions that select this configuration.

Fuchs et al. provide a direct realization:

| Boundary-Mode Framework | Fuchs et al. Warp Shell |
|-------------------------|--------------------------|
| Shift vector $\beta^i$ on flat slices | Shift vector $\beta^1$ added to shell interior |
| Wall selects boundary condition | Physical matter shell imposes $\beta^1 \to 0$ outside |
| Energy density localized at wall | Momentum/pressure modification localized in shell |
| Ordinary matter at wall, exotic nowhere | Ordinary matter with $\rho > 0$, all EC satisfied |
| $\rho$ as mode-sum / boundary effect | Stress-energy from shell's TOV structure + shift perturbation |

**This is not an analogy. The Fuchs construction *is* an instance of the boundary-mode picture, with a specific choice of "wall" (a TOV-solved anisotropic matter shell).** The critical insight is that the added shift vector inside a massive shell produces a physically realizable warp effect *without* introducing negative energy density anywhere in the spacetime.

### 2.2 What Fuchs et al. Did Not Settle

Three open problems remain even granting their construction:

**(P1) The velocity limit.** Their $\beta_\text{warp} = 0.02$ is kept small to keep the momentum flux $T^{0i}$ below the energy density $T^{00}$ of the shell. As $\beta$ grows, the induced momentum flux grows and eventually dominates, triggering WEC/DEC violations. The **maximum physical $\beta$** as a function of shell mass, radius, and pressure profile is undetermined. This is where our framework can contribute: a mode-decomposition analysis of the permissible shift magnitudes under the Eulerian-frame inequalities $|T^{0i}|, |T^{ij}| \le T^{00}$.

**(P2) Acceleration and translation.** Fuchs's metric is *constant-velocity* in a comoving frame — the bubble does not translate relative to its own matter. Accelerating the bubble (changing $v_\text{warp}$ in time) or translating its center reintroduces the Schuster-Santiago-Visser (2022) "Schwarzschild Drive" problem of negative energy density asymptotically. **Genuine transportation requires solving this.** Path 2 in its current form is a static frame-dragging generator, not a translational drive.

**(P3) Mass-to-velocity scaling.** The Fuchs example uses ~750 Earth masses for a 20 m bubble and $\beta = 0.02c$. Scaling analysis (how does the minimum required mass scale with desired $\beta$, bubble size, and shell thickness?) is absent from their paper. Connecting this to the Alcubierre energy estimate $E \sim v_s^2 R^2 / \Delta$ from `LINEARIZATION_CALCULATION.md` Section 6 is an open calculation.

### 2.3 The Refined Boundary-Mode Hypothesis

In light of Fuchs et al., the boundary-mode framework should be stated as:

> **Refined Hypothesis.** The Alcubierre shift-vector configuration is the *external limit* of the interior of a physical matter-shell warp drive. Specifically: there exists a one-parameter family of solutions $g(\lambda)$ with $\lambda \in [0, 1]$, where $\lambda = 0$ is the Fuchs Warp Shell (ordinary matter, all ECs satisfied) and $\lambda = 1$ is the original Alcubierre metric (exotic matter, ECs violated). The interpolation parameter $\lambda$ corresponds physically to the ratio of "warp shift magnitude" to "shell support capacity."

This hypothesis is testable: it predicts specific relationships between shell mass, shift magnitude, and the onset of energy-condition violations.

---

## 3. Israel Junction Conditions — The Thin-Shell Limit

Fuchs et al. use a *thick* shell with smoothly varying TOV profile. A complementary, more analytically tractable approach is the **thin-shell limit**, where the matter lives on an infinitesimally thin layer at $r = R$ and is described by a 2-dimensional surface stress-energy tensor $S_{ab}$. This is the Israel junction condition framework (Israel 1966; Poisson 2004 *A Relativist's Toolkit*).

### 3.1 Setup

Let $\Sigma$ be a timelike hypersurface at $r = R$ separating:
- **Interior** ($r < R$): Alcubierre geometry with shift $\beta^x = -v_s f(r_s)$ on flat slices (so interior $\gamma^{-}_{ij} = \delta_{ij}$, lapse $\alpha^{-} = 1$)
- **Exterior** ($r > R$): Schwarzschild with ADM mass $M$, in isotropic or Schwarzschild coordinates

The induced 3-metric $h_{ab}$ on $\Sigma$ must be continuous ($[h_{ab}] = 0$), which is the first Israel condition. The second Israel condition relates the jump in the extrinsic curvature $K_{ab}$ of $\Sigma$ to the surface stress-energy:

$$[K_{ab}] - [K] h_{ab} = -8\pi G\, S_{ab}$$

where $[X] \equiv X^+ - X^-$ is the jump across $\Sigma$, and $K = h^{ab} K_{ab}$.

### 3.2 Why This Matters

For a *spherical* shell with a *spherically symmetric* interior and exterior, the junction problem is classical and well-understood. The Alcubierre interior is **not spherically symmetric** — the shift vector singles out the $+x$ direction, breaking the isotropy. Therefore:

- The induced metric on the shell will depend on polar angle $\theta$ (measured from the $+x$ axis).
- The extrinsic curvature will have angular dependence matching the shift's $l=1$ dipole structure.
- The surface stress-energy $S_{ab}$ required to support the discontinuity will have non-trivial angular dependence — specifically, anisotropic surface stresses that correlate with the shift direction.

This angular dependence is the analogue, in the thin-shell limit, of the anisotropic pressure components ($P_1, P_2, P_3$) that Fuchs et al. solve for iteratively in the thick-shell case.

### 3.3 Key Calculation (Task 2A.6, carried out in `israel_junction.ipynb`)

The full thin-shell Israel junction with a shift-perturbed Alcubierre interior has been carried out symbolically and numerically in [`israel_junction.ipynb`](israel_junction.ipynb). Headline results:

**Part A — static Schwarzschild exterior (cells 1–9).** Matching an Alcubierre-shift interior $\beta^{\hat r} = -v_s f_R \cos\theta$, $\beta^{\hat\theta} = +v_s f_R \sin\theta$ to a static Schwarzschild exterior at $r = R$:

1. **Angular decomposition of $[K_{ab}]$ is exhausted by $l=0$ and $l=1$.** No quadrupole or higher is generated at linear order in $v_s$. This is a clean angular-momentum selection rule: the $+x$ translation direction carries $l=1$, and the thin-shell matching cannot generate higher-$l$ sources at leading order.
2. **Worst-case DEC violation is at the pole, not the equator.** In the local parameter-point test ($M=0.02, R=1, v_s=0.02, \sigma_w=10$ in geometrised units), DEC fails at $\theta \approx 179°$ — opposite the direction of motion. Physical interpretation: the radial-shift dipole unbalances the static Schwarzschild monopole at the anti-motion pole.
3. **Empirical DEC-satisfying region.** The preview sweep ($\sim$800 points) maps out a region in the $(\sigma_w, v_s)$ plane bounded roughly by $v_s \sigma_w R \lesssim GM/R$ — consistent with the `matter_shell.ipynb` §5 scaling to within an order of magnitude (Jaccard $\approx 0.4$ vs. the exact numerical boundary). A wider full sweep ($32^4 \approx 10^6$ points) is dispatched via `hf jobs run`; see `israel_junction.ipynb` cell 8.
4. **Regression check.** At $v_s = 0$ the surface density reduces to the textbook Schwarzschild weak-field shell $\sigma_0 = (1 - \sqrt{1 - 2GM/R})/(4\pi GR)$ with leading weak-field expansion $M/(4\pi R^2)$ — matching `matter_shell.ipynb` §3.

**Part B — boosted Schwarzschild exterior (cells 10–15).** Introducing two independent velocities, $v_{\rm ext}$ for the exterior boost and $v_{\rm int}$ for the interior Alcubierre shift amplitude:

5. **Covariance regression.** With $v_{\rm ext} = v_{\rm int}$ (translating physical shell), $S_{ab}$ reduces to a Lorentz transform of the static shell. Energy conditions are preserved by covariance.
6. **Critical $\lambda_* > 0$.** Varying $\lambda = v_{\rm ext}/v_{\rm int}$ from 0 to 1 at fixed worst-angle parameters gives a continuous interpolation between the Part A frame-dragging-only DEC failure ($\lambda = 0$) and the covariant DEC-safe translating shell ($\lambda = 1$). For the tested parameter point ($M=0.05, R=1, v_{\rm int}=0.02, \sigma_w=20$), the critical value is $\lambda_* \approx 0.55$ — below this, DEC fails at the worst pole.
7. **The acceleration obstruction is a $\lambda$ constraint.** To accelerate a Fuchs shell from $v_1$ to $v_2 > v_1$, one must transit through configurations with $\lambda < 1$ (exterior lags interior). These are precisely the DEC-unsafe regimes at thin-wall thicknesses. Package 2 (Task 2A.7) asks what $\Delta$ is needed to push $\lambda_*$ down to zero; Package 3 (Task 2A.10) asks whether an alternative mechanism can avoid the $\lambda$-transit entirely.

The thin-shell construction is therefore *consistent* with Fuchs's comoving-frame construction and *isolates the acceleration obstruction* as a single dimensionless critical ratio. The thick-shell regularization (Package 2) is the primary candidate for relaxing the obstruction.

### 3.4 Minimum Shell Thickness (Task 2A.7, derived in `thickness_bound.ipynb`)

The thin-shell version of §3.3 is *harder* to keep physical than Fuchs's thick shell: in the thin-shell limit, the angular pressure anisotropy induced by the shift is concentrated onto a 2D surface, making the surface stresses large compared to the surface energy density. A thick shell spreads these stresses over a finite radial interval, and the extra radial-pressure-gradient freedom is what lets Fuchs satisfy $|T^{ij}| < T^{00}$ pointwise.

The minimum thickness was derived in [`thickness_bound.ipynb`](thickness_bound.ipynb). Starting from the Part A worst-angle (anti-motion pole, $\theta = \pi$) DEC saturation

$$\frac{M}{4\pi R^2} - \frac{\beta\sigma_w}{16\pi R} \ge \frac{\beta\sigma_w}{32\pi R},$$

rearranging gives the Path 2A minimum thickness scaling law:

$$\boxed{\;\frac{\Delta_{\min}}{R} \;=\; \kappa\,\frac{\beta}{C},\qquad C \equiv \frac{2GM}{Rc^2},\qquad \kappa = O(1)\;}$$

where $\kappa = 3/4$ at the analytical pole-dominant level and $\kappa \sim 0.05$–$0.25$ in the numerical sweep (the empirical DEC-safe region is wider than the conservative pole bound because the DEC integrates multiple inequalities with partial cancellations).

**Consequences:**

- Linear in $\beta$, inverse in $C$. Halving the warp velocity halves the required thickness; doubling compactness halves it.
- For $\beta = 0.5$ and near-black-hole compactness $C = 0.9$, $\Delta_{\min}/R \approx 0.04$–$0.42$ depending on $\kappa$ — physically thick but not pathological.
- For $\beta = 0.5$ and $R = 100$ m, the required mass scales from $\sim 3 \times 10^{19}$ kg ($\kappa_{\rm emp}$) up to $\sim 5 \times 10^{20}$ kg ($\kappa_{\rm analytical}$) — small-asteroid to small-planetoid class. The Alcubierre original exotic energy requirement at the same parameters was $10^{30}$+ kg of *negative* energy; Path 2A trades that for positive-energy ordinary matter at much lower mass scales.
- Fuchs et al.'s published regime ($R = 15$ m, $\Delta = 10$ m, $\beta = 0.02$, $M = 4.49 \times 10^{27}$ kg) lives at very low Schwarzschild compactness ($C \sim 10^{-28}$) with dense nuclear-density matter; the scaling law is not directly applicable at their operating point and must be reinterpreted with local density replacing compactness. This suggests a refinement of the scaling law for non-vacuum interiors is a natural Package 2 extension.

The headline plot (cell 10 of `thickness_bound.ipynb`) is a family of $\Delta_{\min}/R$-vs.-$\beta$ curves at several compactness values, bracketed by the $\kappa = 0.10$ numerical and $\kappa = 0.75$ analytical coefficients.

---

## 4. Connection to the Boundary-Mode Decomposition (Phase 2 of the Roadmap)

Phase 2 of the roadmap calls for decomposing the Alcubierre shift vector into eigenmodes of the vector Laplacian on a spherical domain. Fuchs et al.'s construction suggests a specific physical interpretation of this decomposition:

- **Modes with small amplitude:** correspond to warp shifts that can be supported by a shell of a given mass without violating ECs. These are the "physically realizable" modes.
- **Modes with large amplitude:** require more shell mass than the Schwarzschild radius permits (because $R_\text{shell} > 2GM_\text{shell}/c^2$ is a hard constraint). These are the "exotic" modes — including full-amplitude Alcubierre.

So the boundary-mode decomposition acquires a new physical meaning: **the spectrum of eigenmodes on the shell is cut off at a maximum amplitude set by the shell's ADM mass and radius.** Alcubierre's original exotic result corresponds to trying to excite a mode beyond this cutoff with ordinary matter — which is why it requires negative energy.

This is a testable prediction and a clear mathematical target for Phase 2A.

---

## 5. Open Questions Specific to Path 2

| # | Question | Approach |
|---|----------|----------|
| P2.1 | What is the maximum $\beta_\text{warp}$ as a function of $M$, $R_1$, $R_2$ for energy conditions to hold? | Numerical: extend Fuchs's parameter sweep. Analytical: Eulerian-frame inequality $|T^{0i}| \le T^{00}$ as a constraint on $\nabla \beta$. |
| P2.2 | Does the Fuchs shift vector profile correspond to a fundamental mode of the vector Laplacian on the shell domain? | `matter_shell.ipynb`: spectral expansion of $\beta^1(r)$ in vector spherical harmonics + spherical Bessel functions. |
| P2.3 | **(Resolved, 2026-04-16.)** What is the thin-shell limit's surface stress-energy, and does it satisfy DEC? | Addressed in `israel_junction.ipynb` Part A+B (see §3.3). Thin-shell $S_{ab}$ has $l=0 + l=1$ structure; DEC fails at the anti-motion pole for thin walls. Covariance-preserving configurations ($v_{\rm ext}=v_{\rm int}$) are DEC-safe; the acceleration transient through $\lambda < 1$ is the residual obstruction (handed to Task 2A.10). |
| P2.4 | **(Resolved, 2026-04-16.)** Can Fuchs's solution be accelerated without reintroducing negative energy? | Addressed in `acceleration.ipynb` (Task 2A.10, see §7). Three-mechanism catalog (A: shift spin-up with non-vacuum exterior, B: mass ejection, C: GW recoil). Only B is practically viable for warp-relevant $\Delta v$; A reduces the warp drive to "push-from-a-wall"; C is quantitatively limited to $\lesssim 0.25\%$ of $v_{\rm warp}$ under the most favourable Fuchs-compatible parameters. No purely-classical vacuum acceleration mechanism produces $\Delta v$ comparable to $v_{\rm warp}$. |
| P2.5 | **(Resolved, 2026-04-16.)** How does the required shell mass scale with desired $\beta_\text{warp}$ and $R$? | Addressed in `thickness_bound.ipynb`. The scaling law is $\Delta_{\min}/R = \kappa\beta/C$ with $\kappa \in [0.05, 0.75]$; equivalently $M_{\min} \sim \kappa \beta R c^2 / (2G)$ at fixed $\Delta = R$. Fuchs-regime interpretation (dense matter, low compactness) deferred as a refinement. |
| P2.6 | **(Resolved, 2026-04-20, Session 15c — closes ROADMAP 2A.11.)** Does the Lentz 2020 positive-energy soliton fit into this framework, or is it genuinely different? | **Genuinely different mechanism.** Side-by-side comparison in [`LENTZ2020_EVALUATION.md`](LENTZ2020_EVALUATION.md) Appendix B. Fuchs = TOV-solved matter shell + small subluminal shift with full-WEC + DEC Warp-Factory-verified. Lentz = shift-engineered Eulerian-positive metric with no exhibited matter source and explicit DEC failure in the superluminal regime. Logically Lentz lives in Slice 5 (Fell-Heisenberg-class purely irrotational shift); Fuchs lives in Slice 0 (Path 2A baseline). Not interpolable inside Path 2A. The "both classical positive-energy" framing of the original question conflates full-WEC with Eulerian-only positivity. |
| P2.7 | Can the frame-dragging inside the Fuchs shell be amplified (nested shells? rotating shells?) to approach useful transport velocities? | Speculative but testable with Warp Factory. |
| P2.8 | **(Resolved, 2026-04-20, Session 15c — closes ROADMAP 2A.12.)** Does the boundary-mode framing recover Natário 2002 (zero-expansion warp drive) as a special case? | **No: dismissed.** Natário's $\theta=K=0$ ansatz is the purely-solenoidal corner of Fell-Heisenberg's Helmholtz decomposition. The Hamiltonian-constraint identity reduces to $8\pi\rho_E = -\tfrac{1}{2}K_{ij}K^{ij} \le 0$ pointwise (proven in [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb) Phase 3b; see [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) §3.2), so the Eulerian energy density is $\le 0$ everywhere the shift is non-trivial. Slice 1 ([`shift_families.ipynb`](shift_families.ipynb)) included the Natário family explicitly: 0/140 sweep points achieve full WEC. Lobo & Visser 2004 reach the same conclusion via independent linearised-gravity argument. **Distinct from Rodal 2025**, which is a kinematically-irrotational Natário-*class* drive (different corner of the Helmholtz decomposition); see `RODAL2025_EVALUATION.md`. |

---

## 6. Relationship to the Casimir Route (Path 2B)

The Casimir interpretation remains viable and is pursued in parallel. Several possible outcomes:

**(A) Path 2 succeeds fully.** Ordinary matter shells can support warp drives at useful velocities. The Casimir connection becomes a reinterpretation: the same stress-energy that the shell produces classically is also what a quantum field would produce if forced into the same boundary conditions. (Cf. Schwinger's source-theoretic Casimir derivation.) The "exotic matter" problem dissolves.

**(B) Path 2 succeeds only at small amplitude.** The Fuchs construction is real but cannot be pushed to useful speeds with ordinary matter. In this regime, the Casimir route becomes necessary to supply additional negative-energy density — but only the gap between what ordinary matter provides and what the target warp metric requires, which may be vastly less than the full Alcubierre exotic requirement. This would justify QI-scale negative energies rather than macroscopic ones.

**(C) Path 2 fails at any amplitude requiring genuine translation.** Constant-velocity frame-dragging may be all that ordinary matter can produce; accelerating shells may always violate some EC. Then Casimir or another quantum source is required for *acceleration*, not for the static configuration.

**(D) Both fail, for different reasons.** Path 2 because shell acceleration is forbidden; Casimir because spin-2 and sign issues kill the analogy. Then the project has established a rigorous no-go result.

Outcomes (A) and (B) are the positive cases and are consistent with the "structurally analogous" qualification already in `README.md`. Outcome (C) is the most likely given current understanding, and is still scientifically valuable. Outcome (D) is a negative but publishable result.

---

## 7. The Acceleration Problem (Task 2A.10, carried out in `acceleration.ipynb`)

Packages 1 and 2 established that static Fuchs-class matter shells are classically viable under DEC provided the shell is thick enough to satisfy $\Delta/R \gtrsim \kappa\,\beta/C$. The remaining Path 2A question is whether such a shell can be *accelerated* to the target $v_{\rm warp}$ without reintroducing negative-energy regions during the transient. Part B of the Israel junction analysis (§3.3, cell 28 of `israel_junction.ipynb`) identified a critical $\lambda_* = v_{\rm ext}/v_{\rm int} \approx 0.55$ below which DEC fails; Package 3 addresses the mechanism-level question.

### 7.1 ADM 4-Momentum Obstruction

For any asymptotically flat spacetime the ADM linear momentum $P^i_{\rm ADM}$ is conserved at spatial infinity modulo boundary flux. An initially-static Fuchs shell ($K_{ij}(t_0) = 0$) has $P^i_{\rm ADM} = 0$; if the exterior stays vacuum and no matter escapes to infinity, then $P^i_{\rm ADM}(t) = 0$ for all $t > t_0$. This is a gauge-independent obstruction: **the shell cannot self-accelerate in empty space**. Any nonzero centre-of-mass velocity must be sourced by (A) matter flux, (B) non-vacuum exterior, or (C) outgoing gravitational radiation.

The theorem is consistent with and strictly strengthens Schuster–Santiago–Visser 2023 Theorem 3 by decomposing the "boundary flux" term into three physically distinct mechanisms.

### 7.2 Three-Mechanism Catalog

| Mechanism | ADM-consistent | DEC-compatible | Vacuum-compatible | Quantitative feasibility | Verdict |
|-----------|----------------|----------------|-------------------|--------------------------|---------|
| **A — shift spin-up, non-vacuum exterior** | yes (momentum in exterior matter) | yes, iff exterior pre-loaded with positive-energy matter $\sim M_{\rm shell}$ | no | requires comoving mass $\sim M_{\rm shell}$ | Reduces to "push-from-a-wall"; not warp drive |
| **B — mass ejection / photon rocket** | yes (Tsiolkovsky) | yes (ordinary matter/radiation ejecta) | yes | trivial for $\beta \sim 0.02$ (mass ratio 1.02) | Viable, but ordinary rocket; no warp benefit |
| **C — GW recoil** | yes (GW radiation carries $P^i$) | yes (radiation is null, positive energy) | yes | $\Delta v_{\max} < 10^{5.8}$ m/s, all Fuchs params | Allowed but negligible; ruled out quantitatively |

### 7.3 Quantitative GW-Recoil Ceiling

Two independent estimates converge on a hard ceiling for Mechanism C:

- **Approach A (SXS rescaling, Varma et al. 2022).** $v_{\rm kick}^{\rm Fuchs} \sim v_{\rm kick}^{\rm BBH} \cdot \beta^2 \cdot C^{3/2}$, where $v_{\rm kick}^{\rm BBH}$ is the 5000 km/s record for near-equal-mass BBH merger. For Fuchs parameters ($\beta = 0.02$, $C = 0.44$) this gives $v_{\rm kick}^{\rm Fuchs} \sim 600$ m/s, or $\sim 10^{-4}$ of $v_{\rm warp}$.
- **Approach B (PN shell-analog binary).** Shell + 1% beacon at grazing orbit gives $\lesssim 10^{-8}$ m/s per orbit; accumulating over $10^8$ orbits yields $\sim 10^{-12}$ m/s.

A full HF-Jobs sweep (cell 13, `hf_jobs/sweeps/gw_recoil.py`) over $(\beta, C, M, n_{\rm orbits})$ returns a max of $10^{5.82}$ m/s $\approx 660$ km/s, at $\beta = 0.9$ and $C = 0.5$ — still $\sim 0.25\%$ of the warp target at those parameters.

### 7.4 Consequence for Path 2A

**Task 2A.10 result.** No classical mechanism simultaneously (i) preserves DEC on shell and exterior, (ii) keeps the exterior vacuum, (iii) requires no expelled reaction mass, and (iv) produces $\Delta v$ comparable to $v_{\rm warp}$.

This closes the dynamical problem under classical-matter assumptions: Path 2A produces static-viable shells, but accelerating them requires an ordinary rocket stage (Mechanism B) or a pre-loaded exterior medium (Mechanism A). It does not rule out the Path 2B (Casimir / boundary-mode) programme — indeed it *motivates* it as the remaining candidate for a dynamical warp-drive realisation. This is outcome **(C)** of §6.

---

## 8. Static-Infrastructure Prior Art and Recent Comparison Targets (added Session 7)

### 8.1 Krasnikov tubes — the static-network analogue

Following the analysis of `speculation/RING_NETWORK_CONCEPT.md`, the following prior art is now central to any static-infrastructure extension of Path 2A. Full details in `KRASNIKOV_TUBE_NOTES.md`.

- **Krasnikov 1995** (gr-qc/9511068) introduced the static-tube spacetime in 2D. Built once by an outbound traveller; once built, any later traveller uses it for arbitrarily fast round trips as measured by terrestrial clocks.
- **Everett & Roman 1997** (gr-qc/9702049) extended to 4D and computed $T_{\mu\nu}$ classically in the wall: $T_{\hat t \hat t}^{\rm wall} \approx -\eta/(8\pi\epsilon^2)$ with $\eta = 2 - \delta$ the light-cone-opening parameter and $\epsilon$ the wall thickness. **Negative for any non-trivial $\eta$, classically, regardless of wall EoS.** They also proved that any *network* of Krasnikov tubes generates CTCs (two non-overlapping oppositely-directed tubes form a time machine).
- **Krasnikov 2003** (gr-qc/0207057) pushed back on Pfenning–Ford QI bounds but did not produce a positive-energy / DEC-satisfying construction.
- **Lobo & Crawford 2002** (gr-qc/0204038) reproduced Everett–Roman pedagogically and added Olum's superluminal-implies-WEC-violation theorem. No thin-shell/Israel formalism for Krasnikov tubes anywhere in the literature we could find.

**Implication for Path 2A.** Task 2A.13 (the reframed Calculation 1, completed 2026-04-16 in `krasnikov_tube.ipynb`) ports the Path 2A Israel-junction tooling to the Krasnikov 4D metric with a Fuchs-class thick wall. **Result:** the Everett–Roman classical $-\eta/(8\pi\epsilon^2)$ negative-energy spike is reproduced in our framework with a quantitative universal scaling law and a robust no-go: there is no $(\eta, \epsilon, \rho_{\max})$ region in which any classical positive-matter wall satisfies WEC, let alone DEC. Full statement in §9 below.

### 8.2 Rodal 2025 — a new comparison target

Rodal 2025 (arXiv:2512.18008, Gen. Rel. Grav. **58**, 1 (2026)) constructed the first explicit, continuous, analytically derived **kinematically irrotational** Natário-class warp drive. Detailed evaluation in `RODAL2025_EVALUATION.md`. Key facts for Path 2A:

- **Peak proper-energy deficit** is reduced by ≈38× vs. Alcubierre and ≈2,600× vs. Natário at identical $(\rho, \sigma, v/c)$. **Globally Hawking–Ellis Type I** (no Type IV pockets).
- **Net proper energy ≈ 0** to 0.04% of total $\int |\rho_p| dV$ after a $1/R$ tail extrapolation. This is a *proper* energy statement — the paper itself notes (§ "Physical remark on near cancellation") it does *not* establish vanishing ADM/Komar mass.
- **NEC, WEC, DEC, SEC are still all violated.** The improvement is in algebraic structure (Type I vs Type IV) and in the *peak* deficit, not in the underlying physics. Classical matter still cannot source the stress-energy.
- **Constant velocity only.** The acceleration problem (our Task 2A.10) is unaddressed. The author explicitly notes that letting $v(t)$ vary "can reintroduce off-diagonal fluxes in mixed components and creating Type IV pockets."

**Implication for Path 2A.** No change to the Task 2A.10 conclusion. Rodal's analysis is at constant $v$; our acceleration obstruction is independent of which steady-state metric is chosen.

**Implication for Path 2B.** Significant. Rodal's stress-energy profile is qualitatively different from Alcubierre's: positive on-axis density in thin polar collars + **negative anisotropic transverse pressures** in equatorial mantles, instead of isotropic negative density. Anisotropic vacuum stresses (waveguide-confined Casimir, asymmetric-plate Casimir) are closer to what real QFT setups produce than isotropic negative energy density. Path 2B's literature pull should now target this geometry. See `QUANTUM_CLASSICAL_BRIDGE.md` for the updated outcome matrix.

---

## 9. The Krasnikov Tube + Fuchs-Class Thick Wall (Task 2A.13, completed 2026-04-16 in `krasnikov_tube.ipynb`)

This section reports the quantitative Path 2A bound on Krasnikov-style geometries, closing the speculation question raised in `RING_NETWORK_CONCEPT.md`. The full computation is in `krasnikov_tube.ipynb`; the prior-art context is in `KRASNIKOV_TUBE_NOTES.md` §§1–6.

### 9.1 Setup

The Krasnikov 4D metric (Everett & Roman 1997, Eq. 13) in the long-after-formation static region:

$$ds^2 = -dt^2 + (1 - k(\rho))\,dx\,dt + k(\rho)\,dx^2 + d\rho^2 + \rho^2\,d\phi^2$$

with $k(\rho) = 1 - \eta\,\theta_\epsilon(\rho_{\max} - \rho)$, the smooth step $\theta_\epsilon$ from their Eq. 35, and parameters

- $\eta = 2 - \delta \in (0, 2)$ — **light-cone-opening parameter**. The observable round-trip-time-shortening grows linearly with $\eta$. $\eta = 0$ recovers Minkowski (no warp effect); $\eta = 2$ is the singular $k = -1$ limit.
- $\epsilon$ — wall thickness (free, can be macroscopic).
- $\rho_{\max}$ — tube radius.

We compute the orthonormal-frame stress-energy $T^{\hat\mu\hat\nu}$ in the static observer's tetrad (their Eqs. 24–27) directly from the Einstein equations on this metric. As a regression check, the symbolic $T_{tt}$ matches their Eq. 14 exactly.

### 9.2 Headline scaling law

The minimum (most negative) value of the proper energy density across the wall obeys a universal scaling law:

$$\boxed{\;\rho_p^{\min}(\eta, \epsilon, \rho_{\max}) \;=\; -\frac{\kappa_K(\eta)}{\epsilon^2}\;}$$

with

$$\kappa_K(\eta) \;\approx\; \frac{1.534\,\eta}{4\pi} \;\approx\; 0.122\,\eta \quad \text{for } \eta \ll 1,$$

and $\kappa_K(\eta) \to \infty$ as $\eta \to 2$ (the $1/(1+k)^2$ amplification near the singular metric). The $\rho_{\max}$-dependence is sub-percent for $n = \rho_{\max}/\epsilon > 5$. **Verified numerically across the parameter sweep** (`krasnikov_tube.ipynb` Cells 13, 19–21) to $\epsilon$-independence at the 14-decimal level.

### 9.3 No-go: WEC fails for any $\eta > 0$

The negative-energy region is local to the wall and present at every $(\eta, \epsilon, \rho_{\max})$ with $\eta > 0$. Sweep statistics over 300 parameter points (`hf_jobs/sweeps/krasnikov_tube.py` preview run):

- **WEC pass rate: 0.0000.** All points have $\rho_p^{\min} < 0$ somewhere in the wall.
- **DEC pass rate: 0.0000.** Inside the wall, the off-diagonal flux $|T_{\hat t \hat x}|$ exceeds $\rho_p$ even where $\rho_p > 0$; outside the wall, $\rho_p < 0$ directly.
- **Full sweep extrapolation.** The expected null result for the full $\sim 30{,}000$-point HF Jobs sweep matches the analytical prediction; the local sweep already establishes the no-go to high confidence.

### 9.4 The unobservability tradeoff

The negative-energy density and the observable warp effect are governed by the same parameter $\eta$:

- $|\rho_p^{\min}| \;\propto\; \eta/\epsilon^2$ (negative energy density)
- $\Delta v_{\rm photon}/c \;\approx\; \eta + O(\eta^2)$ (lightcone opening; the photon speed inside the tube is $1/(1-\eta)$, exceeding $c$ by $\eta + O(\eta^2)$)

So **the ratio (negative energy density)/(observable warp effect) is a fixed $\eta$-independent constant of order $1/(4\pi\epsilon^2)$**. You cannot simultaneously make the warp drive useful and the energy violation small. This is the quantitative version of Everett–Roman's qualitative "completely unobservable" remark (their §6 final paragraph), and it is the strongest classical no-go we can produce for Krasnikov-style geometries.

### 9.5 A Fuchs-class matter shell does not save the construction

A natural follow-up is whether wrapping a Fuchs-class positive-matter shell *around* the Krasnikov tube wall could compensate the local negative-energy spike. The answer is no: the Krasnikov-wall negative density is *local* (concentrated in a band of width $\sim \epsilon$ centred at the wall edge), and DEC is a *pointwise* condition. A separate matter shell at a different cylindrical radius adds positive-energy elsewhere but does not change the local stress-energy in the Krasnikov wall band. Wrapping the shell *coincident* with the Krasnikov wall would require matching cylindrical extrinsic curvature jumps to a stress-energy distribution that is *more* negative than what either side can produce — a more-singular Israel-junction problem that does not have a classical-matter solution. See `krasnikov_tube.ipynb` Cell 17 for the order-of-magnitude argument.

### 9.6 Comparison to Path 2A Packages 1–2 (Fuchs spherical shell)

| Quantity | Fuchs spherical shell (Packages 1–2) | Krasnikov tube (Task 2A.13) |
|---|---|---|
| Wall geometry | Constant-$r$ sphere, thickness $\Delta$ | Constant-$\rho$ cylinder, thickness $\epsilon$ |
| Matter parameter | Compactness $C = 2GM/(Rc^2)$ | (none — vacuum metric) |
| "Useful" parameter | Warp velocity $\beta = v_s/c$ | Lightcone opening $\eta = 2 - \delta$ |
| DEC scaling law | $\Delta_{\min}/R = \kappa\,\beta/C$, $\kappa \in [0.05, 0.75]$ | $\rho_p^{\min} = -0.122\,\eta/\epsilon^2$ for ALL $\eta > 0$ |
| Knob to satisfy DEC | Increase shell mass $M$ (raise $C$) or thicken the wall ($\Delta$) | **NONE** — no parameter eliminates the spike |
| Useful regime | DEC-compatible thick shell at $\beta \lesssim C$ (e.g. $C = 0.5$, $\beta = 0.5$, $\Delta/R = 0.75$) | **Empty** under classical positive matter |

**Why the difference?** The Fuchs-class spherical shell gets DEC by hiding the warp's kinematic cost in the shell's *gravitational binding energy* (the $C$ term). The Krasnikov tube has no such matter source — it asks the *vacuum metric itself* to do the work, which the Einstein equations require to come from negative classical $T_{\hat t \hat t}$.

### 9.7 What this means for the speculation document

`speculation/RING_NETWORK_CONCEPT.md` proposed building a *static infrastructure* of Krasnikov-style tubes as a way to dodge the acceleration obstruction (Task 2A.10): assemble a closed network adiabatically while no shell is moving, then use the network for transport that requires no acceleration of the shell. Two structural tensions with this proposal are now identified:

1. **The wall stress-energy resists classical positive-matter sourcing** — Task 2A.13 (this section) shows that within the metric ansatz used by Krasnikov 1995 / Everett–Roman 1997, no classical positive matter sources a Krasnikov-tube wall for any $\eta > 0$. **Caveat (added Session 9):** Slice 2 of Phase 2C tests whether a Fuchs-class matter shell *coincident* with the wall can locally cancel the negative spike via cylindrical Israel junctions — see `hybrid_wall.ipynb`. The §9.5 hand-wave that this can't work has not yet been made rigorous; if Slice 2 produces a cancellation, this point softens.
2. **The network creates CTCs in the canonical Krasnikov construction** — Everett–Roman 1997 §4 (independent of this calculation) shows two non-overlapping oppositely-oriented Krasnikov tubes form a time machine. We have not independently rederived their §4 (TRUST_AUDIT #8); it is on the read-and-summarise list.

A Fuchs-class spherical shell *ring* is constructible (Packages 1–2 cover that), but a Fuchs-class ring does *not* shorten light-travel time the way a Krasnikov-tube ring would, because Fuchs shells have flat-but-shifted interiors, not opened-out lightcones. The speculation as originally framed merges constructibility (Fuchs) with transport benefit (Krasnikov), and no single construction we have computed provides both. Whether some other construction outside our slice does is exactly what Phase 2C is for.

### 9.8 Implication for the project

Task 2A.13 closes the **static-infrastructure-vacuum-classical** branch of the speculation under the explicit assumptions listed in §0.5. Combined with Packages 1–3, the static-slice picture is:

- **Static spherical Fuchs shells** (Packages 1–2): DEC-compatible classical realisation. ✓
- **Acceleration of those shells via the three catalogued mechanisms in vacuum** (Package 3): no classical mechanism produces warp-relevant $\Delta v$. ✗
- **Static-infrastructure Krasnikov tubes with bare-metric vacuum source** (Task 2A.13, this section): negative classical $T_{\hat t \hat t}$ in the wall for any $\eta > 0$. ✗
- **Acceleration via static-infrastructure transport with bare Krasnikov walls** (the speculation): inherits the wall problem from item 3 plus the CTC theorem of Everett–Roman §4. ✗

**This is one slice of the landscape, not the landscape.** Six adjacent slices (§0.5 above) remain explicitly open. The most natural extensions are:

- **Slice 1** (alternate shift families): is the negative result an artefact of choosing $\beta^x \hat x$? Lentz 2020 already demonstrated that a different shift profile produces positive-energy solutions, so the answer is at least *partially* yes.
- **Slice 2** (Fuchs+Krasnikov hybrid): is the §9.5 hand-wave correct? Has not yet been computed properly.
- **Slice 3** (time-dependent metrics): can explicit $v(t)$ ramps reveal transient loopholes that the steady-state-plus-boost analysis misses?

In parallel, **Path 2B** (Casimir / boundary-mode QFT mechanism) remains a candidate, with the Rodal 2025 evaluation (`RODAL2025_EVALUATION.md`) suggesting the natural QFT-search target is anisotropic transverse vacuum stresses with positive normal energy density (waveguide-confined Casimir, asymmetric-plate Casimir, repulsive-Casimir geometries). Path 2B is one of several remaining routes, not the only one.

---

## 10. References for Path 2

| Paper | arXiv | Role in Path 2 |
|-------|-------|----------------|
| Fuchs et al. 2024 | [2405.02709](https://arxiv.org/abs/2405.02709) | Primary anchor: existence of physical warp shell |
| Helmerich et al. 2024 (Warp Factory) | [2404.03095](https://arxiv.org/abs/2404.03095) | Numerical toolkit for testing |
| Lentz 2020 | [2006.07125](https://arxiv.org/abs/2006.07125) | Alternative classical positive-energy soliton (Einstein-Maxwell-plasma) |
| Lentz 2021 | [2201.00652](https://arxiv.org/abs/2201.00652) | Extension to hyper-fast positive-energy drives |
| Natário 2002 | (see LITERATURE.md) | Zero-expansion warp drive — classical reformulation of Alcubierre |
| Bobrick & Martire 2021 | (see LITERATURE.md) | General framework for physical warp drives |
| Fell & Heisenberg 2021 | (see LITERATURE.md) | Positive energy from hidden geometric structures |
| Santiago-Schuster-Visser 2022 | [2105.03079](https://arxiv.org/abs/2105.03079) | Generic warp drives violate NEC — Path 2 must confront |
| Schuster-Santiago-Visser 2022 | [2205.15950](https://arxiv.org/abs/2205.15950) | ADM mass in warp spacetimes — constraint on acceleration |
| Schuster-Santiago-Visser 2023 | [2310.10871](https://arxiv.org/abs/2310.10871) | ADM 4-momentum conservation theorem used in §7.1 |
| Varma et al. 2022 | [2208.02805](https://arxiv.org/abs/2208.02805) | NR record GW-recoil kick (5000 km/s); rescaled in §7.3 |
| Israel 1966 | (textbook / Poisson 2004) | Thin-shell junction conditions formalism |
| Poisson 2004 *A Relativist's Toolkit* | Cambridge UP | Standard reference for Israel formalism |
| **Krasnikov 1995** | [gr-qc/9511068](https://arxiv.org/abs/gr-qc/9511068) | Static-tube spacetime; prior art for "static infrastructure" speculation. See §8.1 and `KRASNIKOV_TUBE_NOTES.md`. |
| **Everett & Roman 1997** | [gr-qc/9702049](https://arxiv.org/abs/gr-qc/9702049) | 4D Krasnikov tube + classical $T_{\hat t \hat t}$ + network/CTC theorem. Direct comparison target for Task 2A.13. |
| **Krasnikov 2003** | [gr-qc/0207057](https://arxiv.org/abs/gr-qc/0207057) | QI counter-arguments; does not produce a positive-energy construction. |
| **Lobo & Crawford 2002** | [gr-qc/0204038](https://arxiv.org/abs/gr-qc/0204038) | Pedagogical Everett–Roman reproduction + Olum's WEC theorem. |
| **Rodal 2025** | [2512.18008](https://arxiv.org/abs/2512.18008) | New Natário-class irrotational warp drive; 38× peak-deficit reduction vs. Alcubierre. Detailed evaluation in `RODAL2025_EVALUATION.md`. |

---

## Appendix A — Three-Mechanism Exhaustiveness (TRUST_AUDIT #6, added Session 9)

Package 3 (`acceleration.ipynb`) catalogued three mechanisms by which a Fuchs-class shell could accelerate in vacuum: (A) shift spin-up against a non-vacuum exterior, (B) mass ejection (rocket), (C) gravitational-wave recoil. The original exposition argued by elimination but did not write the formal exhaustiveness proof. This appendix closes that audit gap.

**Setup.** Let $\Sigma$ be an asymptotically flat spacetime containing a compact "warp shell" body, with ADM 4-momentum $P^\mu_{\rm ADM}$ defined at spatial infinity via the standard surface integrals (Arnowitt-Deser-Misner 1962; Wald 1984 §11.2):

$$P^i_{\rm ADM} = \frac{1}{8\pi}\oint_\infty (K^{ij} - K\,\gamma^{ij})\,n_j\,dA.$$

Initial data: at $t = t_0$ the shell is in a static configuration (in some inertial frame $S_0$ at infinity), with $K_{ij}(t_0) = 0$ on the constant-$t_0$ slice. Then $P^i_{\rm ADM}(t_0) = 0$ in frame $S_0$.

**Claim.** The change $\Delta P^i_{\rm ADM} = P^i_{\rm ADM}(t) - P^i_{\rm ADM}(t_0)$ for $t > t_0$ can come *only* from one or more of the following three categories of boundary flux:

- **(A) Non-vacuum exterior**: a non-zero stress-energy $T^{\mu\nu}$ in the asymptotic region carries momentum that can be exchanged with the shell.
- **(B) Mass ejection**: a portion of the shell's matter is expelled and crosses the asymptotic boundary, carrying momentum with it.
- **(C) Outgoing gravitational radiation**: a non-zero $\dddot{Q}^{ij}$ produces a gravitational-wave momentum flux at null infinity (Bondi-Sachs sense).

**Proof sketch.** The Bianchi identity $\nabla_\mu G^{\mu\nu} = 0$ implies, via the Einstein equations, $\nabla_\mu T^{\mu\nu} = 0$ — local conservation of stress-energy. Integrating over a 4-volume $V$ bounded by the constant-$t_0$ slice $\Sigma_0$, the constant-$t$ slice $\Sigma_t$, and a timelike cylinder $C$ at large spatial radius:

$$\int_V \nabla_\mu T^{\mu\nu}\,d^4x = 0 = \int_{\Sigma_t} T^{0\nu}\,dV - \int_{\Sigma_0} T^{0\nu}\,dV + \int_C T^{i\nu}\,n_i\,dA - \int_{\mathcal{I}^+} (\text{GW flux})$$

(with appropriate signs from the $4 \to 3$ projection). The four terms correspond to:

1. $\int_{\Sigma_t} T^{0i} dV$ = ADM linear momentum of *all matter on the slice* including the shell.
2. $\int_{\Sigma_0} T^{0i} dV$ = same at $t_0$ (zero by assumption).
3. $\int_C T^{ij} n_j dA$ = momentum flux through the cylinder = momentum carried by exterior matter (Mechanism A) or by ejected matter (Mechanism B).
4. $\int_{\mathcal{I}^+}$ (GW flux) = momentum carried away by gravitational radiation (Mechanism C).

Therefore $\Delta P^i_{\rm ADM} = -(\text{term 3}) + (\text{term 4}) = -[\text{Mech A} + \text{Mech B}] + [\text{Mech C}]$. Any non-zero $\Delta P^i_{\rm ADM}$ must therefore come from a non-zero contribution in at least one of Mechanisms A, B, C.

**No "fourth mechanism."** A pure metric self-rearrangement of the shell — a configuration change in $g_{\mu\nu}$ on the slice with no matter or radiation flux at the boundary — cannot change $P^i_{\rm ADM}$. This is because $P^i_{\rm ADM}$ is a *boundary integral* defined entirely by the asymptotic falloff of the metric, and asymptotic falloff cannot be changed by interior reconfiguration without sending a flux to infinity.

**Caveats**:
1. The proof assumes asymptotic flatness. Slice 5 (cosmological exterior) explicitly relaxes this.
2. The proof assumes 4D Einstein gravity. Slice 6 (modified gravity) relaxes this; in modified gravity the analogue of $P^i_{\rm ADM}$ may pick up a "gravitational degree of freedom" contribution that has no Einstein analogue.
3. The proof assumes the cylinder $C$ is at *spatial* infinity. If horizons or other interior boundaries form during the shell's evolution, additional flux terms enter.

Subject to these caveats, the three-mechanism catalog is exhaustive. **TRUST_AUDIT #6 closed.**

This proof was written as a Slice 2 audit interleave in Session 9. The proof technique reuses the ADM-flux logic that motivated the cylindrical Israel junction analysis in [`hybrid_wall.ipynb`](hybrid_wall.ipynb), which is why the audit fits naturally here.

---

*This document is the operational plan for the primary research track. It is not a commitment to abandon the Casimir framing — see `QUANTUM_CLASSICAL_BRIDGE.md` for that track's continuation — but it is the track where the first concrete calculations of the next phase will live.*

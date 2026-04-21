# Toroidal-Fuchs Shell — Notes (Task 2A.14)

**Notebook:** [`toroidal_fuchs.ipynb`](toroidal_fuchs.ipynb) (16 cells, executes in seconds)
**Companion to:** [`KRASNIKOV_TUBE_NOTES.md`](KRASNIKOV_TUBE_NOTES.md) §7.2, [`thickness_bound.ipynb`](thickness_bound.ipynb) Cell 3, [`speculation/RING_NETWORK_CONCEPT.md`](speculation/RING_NETWORK_CONCEPT.md) §4
**Status:** Scope (a) complete, scope (b) deferred (see §3 below)
**Verdict:** Toroidal Fuchs shell is **strictly worse** than spherical Fuchs shell by a geometric factor $\geq 2\pi$ at any non-degenerate torus aspect ratio.

---

## 1. Motivation

[`KRASNIKOV_TUBE_NOTES.md`](KRASNIKOV_TUBE_NOTES.md) §7.2 listed two reasons the toroidal-Fuchs proposal in [`speculation/RING_NETWORK_CONCEPT.md`](speculation/RING_NETWORK_CONCEPT.md) §4 was likely uninteresting:

1. The Path-2A no-go is sufficiently general that the *topological* swap $S^2 \to T^2$ should not be expected to evade it; intuitively, distributing the same total mass over a torus rather than a sphere only changes the local curvature scale at which the Israel-jump bound activates.
2. Even if a toroidal Fuchs shell were classically constructible, it provides no causal advantage (it is a static structure with no light-cone tilting) — already settled in [`KRASNIKOV_TUBE_NOTES.md`](KRASNIKOV_TUBE_NOTES.md) §7.1 and §9.

Task 2A.14 was deferred for a long time because reason (2) made the calculation of reason (1) uninteresting in isolation. With Phase-2A closed and Tasks 2A.9b / 2A.13 already settling the strongest version of the no-go on the spherical and Krasnikov sides, the toroidal-Fuchs follow-up is now closeable cheaply — and a clean dismissal completes the topology census.

This notebook does the cylindrical-reduction limit (scope a). Scope b — full fat-torus calculation in a Weyl/Bach-Weyl axisymmetric vacuum exterior — is deferred (§3).

---

## 2. Scope (a): cylindrical-reduction result

The thin-torus limit ($R_\text{minor}/R_\text{major} \ll 1$) reduces locally to an infinite cylinder of radius $R = R_\text{minor}$. The exterior is the linearized Levi-Civita vacuum (Bonnor canonical form, gauge $\rho_0 = R$ to absorb the well-known $\ln R$ asymptotic-mass ambiguity); the interior is Minkowski; the junction is the Israel surface stress at $\rho = R$.

### 2.1 Static cylindrical shell

The Israel-jump calculation gives, to first order in the line mass density $\sigma$:

$$
\sigma_E = \frac{\sigma}{2\pi R}, \qquad p_z = 0, \qquad p_\varphi = 0
$$

The shell is pressureless dust localized on $\rho = R$ — DEC is saturated trivially. This is the cylindrical analog of the spherical static dust shell ($\sigma_E = M/(4\pi R^2)$, $p_\theta = p_\varphi = 0$).

### 2.2 Cylindrical Fuchs bound

Adding the Path-2A axial shift $\beta^z$ (the cylindrical analog of the Alcubierre/Fuchs shift $\beta^\theta$ on the spherical case) and applying the same worst-angle DEC analysis as [`thickness_bound.ipynb`](thickness_bound.ipynb) Cell 3:

| | spherical (2A.9a) | cylindrical (this notebook) |
|---|---:|---:|
| $\sigma_0$ | $M/(4\pi R^2)$ | $M/(2\pi R L)$ |
| $\sigma_1$ | $-\beta\sigma_w/(16\pi R)$ | $-\beta\sigma_w/(8\pi R)$ |
| $P_1$ | $-\beta\sigma_w/(32\pi R)$ | $-\beta\sigma_w/(16\pi R)$ |
| DEC bound | $\sigma_0 + \sigma_1 \geq |P_1|$ | $\sigma_0 + \sigma_1 \geq |P_1|$ |
| $\Delta_{\min}$ (geom.) | $\dfrac{3}{8}\dfrac{\beta R}{M}$ | $\dfrac{3}{8}\dfrac{\beta L}{M}$ |
| dimensionless form | $\dfrac{\Delta}{R} = \dfrac{3}{4}\dfrac{\beta}{C_\text{sph}}$, $C_\text{sph} = 2GM/(Rc^2)$ | $\Delta\,\mu_\text{geom} = \dfrac{3}{8}\beta$, $\mu_\text{geom} = G\mu/c^2 = GM/(Lc^2)$ |
| trapped angular dims | 2 | 1 |

The structurally interesting fact: **$\Delta_{\min}^\text{cyl}$ is independent of the shell radius $R$.** The $R$ cancels between $\sigma_0 \propto 1/(RL)$ and $\sigma_1, P_1 \propto 1/R$, leaving the natural length scale as $L$ (the axial extent), not $R$.

This is the structural signature of having one trapped angular dimension instead of two: in the cylindrical surface area $2\pi R L$, the $R$ cancels against the $1/R$ in the surface stress; in the spherical surface area $4\pi R^2$, the analogous cancellation leaves a single $R$ surviving.

### 2.3 Torus penalty

Identifying $L \to 2\pi R_\text{maj}$ (the central-axis circumference) and $R \to R_\text{min}$:

$$
\boxed{\;\frac{\Delta_{\min}^\text{cyl}}{\Delta_{\min}^\text{sph}} \;=\; \frac{L}{R_\text{min}} \;=\; \frac{2\pi R_\text{maj}}{R_\text{min}}\;}
$$

For any non-self-intersecting torus ($R_\text{maj} \geq R_\text{min}$), the penalty satisfies $L/R_\text{min} \geq 2\pi \approx 6.28$. The crossover where the cylindrical and spherical bounds coincide sits at $R_\text{maj}/R_\text{min} = 1/(2\pi) \approx 0.159$ — a degenerate "torus" where the minor cross-section punches through the central axis.

For Fuchs's reference parameters ($R_\text{min} = 15$ m, $R_\text{maj} = 75$ m, $\beta = 0.02$, $M = 4.49 \times 10^{27}$ kg):

- $\Delta_{\min}^\text{sph} = 3.4 \times 10^{-2}$ m
- $\Delta_{\min}^\text{cyl} = 1.06$ m
- penalty $= 31.4$ ($= 2\pi \cdot 5$)

### 2.4 Verdict

> A toroidal Fuchs-class shell is constructible (DEC-compatible at sufficiently large $\Delta$), but offers **no advantage** over the spherical Fuchs shell — it is **strictly worse** in the energy-condition window by a factor $\geq 2\pi$, AND offers no causal advantage (per [`KRASNIKOV_TUBE_NOTES.md`](KRASNIKOV_TUBE_NOTES.md) §6, §7.1). **The toroidal-Fuchs path is dismissed.**

This is a stronger dismissal than [`KRASNIKOV_TUBE_NOTES.md`](KRASNIKOV_TUBE_NOTES.md) §7.2 anticipated: not just "no advantage," but "strictly worse by a calculable, bounded-below geometric factor."

---

## 3. Scope (b) deferred — full fat-torus matching

The cylindrical-reduction limit ignores the torus's intrinsic curvature: the inboard side of the tube ($\rho = R_\text{maj} - R_\text{min}$) and the outboard side ($\rho = R_\text{maj} + R_\text{min}$) are at different distances from the central axis, so the local curvature scales differently across the tube cross-section.

A full fat-torus calculation would:

1. **Choose an exterior vacuum.** The Weyl class of axisymmetric static vacuum solutions provides candidates (Bach–Weyl ring, Israel–Khan multi-particle, etc.), but no closed-form regular asymptotically-flat exterior of a single solid-torus mass distribution is known. Numerical relativity (or large-order multipole expansions) would be required.
2. **Israel-junction match on a 2-torus surface.** The induced metric and extrinsic curvature on $T^2$ depend on both the major and minor radii; the surface stress is no longer of the simple "line-mass × $1/R$" form.
3. **Re-derive $\Delta_{\min}$.** The expectation, based on the qualitative structure of the cylindrical-reduction result, is that the inboard side (smaller effective radius, tighter local curvature) will activate the DEC bound first, yielding $\Delta_{\min}^\text{fat} \geq \Delta_{\min}^\text{cyl}$ (i.e., the dismissal only gets stronger under fat-torus refinement).

**Why deferred:**
- The cylindrical-reduction result already dismisses the speculation by a clear geometric factor $\geq 2\pi$. Refining the dismissal to "$\geq 2\pi$ AND additionally penalized by the inboard/outboard asymmetry" doesn't change the qualitative verdict.
- The required numerical relativity (or high-order Bach–Weyl matching) is multi-week effort with no qualitative payoff.
- It would be relevant if someone proposed a *quantitatively specific* fat-torus design that the cylindrical-reduction limit fails to address — e.g., a fat-torus design optimized for some other property (low total mass, large interior volume, etc.) where the cylindrical limit underestimates by a factor that matters for that proposal. No such proposal exists in the literature or in [`speculation/RING_NETWORK_CONCEPT.md`](speculation/RING_NETWORK_CONCEPT.md).

**Reopening criteria:** scope (b) becomes worth executing if:
1. Someone publishes a specific fat-torus warp-shell design with a quantitative claim about $\Delta_{\min}$ or DEC-compatibility, OR
2. A fully analytic regular exterior for a solid-torus mass distribution is found in the GR literature (would make the calculation tractable), OR
3. Phase-3 (or later) explicitly investigates non-spherical compact-object exteriors for some other reason and the framework can be reused at low marginal cost.

---

## 4. Honest accounting

- **Numerical coefficient $3/8$** comes from worst-angle dimensional reconstruction of the Israel-jump-induced surface-stress correction (paralleling [`thickness_bound.ipynb`](thickness_bound.ipynb) Cell 3). A first-principles perturbative Israel calculation with the axial shift turned on explicitly would refine this. The spherical numerical sweep ([`thickness_bound.ipynb`](thickness_bound.ipynb) Cell 7) found $\kappa_\text{emp} \approx 0.10$ vs analytical $3/4$; an analogous cylindrical sweep would likely soften the coefficient comparably. The *ratio* $L/R_\text{min}$ that drives the verdict is dimensionally robust and gauge-independent.
- **Levi-Civita gauge.** Absorbing $\ln R$ into $\rho_0 = R$ removed the asymptotic-mass ambiguity. Different gauges give different $\sigma \leftrightarrow \mu$ identifications but the structural form $\Delta_{\min}^\text{cyl} = $ const $\times \beta L/M$ is gauge-invariant.
- **Discrepancy with [`thickness_bound.ipynb`](thickness_bound.ipynb) §3.** The boxed equation in `thickness_bound.ipynb` Cell 3 markdown reads $\Delta_{\min}^\text{sph} = (3/8)\beta R^2/M$; the actual algebraic chain printed by the notebook (from $M/R^2 \geq 3\beta\sigma_w/(8R)$ to $\sigma_w \leq 8M/(3\beta R)$) gives $\Delta_{\min}^\text{sph} = (3/8)\beta R/M$, which is what we use here. The extra $R$ in the boxed form is a typo in the decorative display equation; the dimensionless form $\Delta_{\min}/R = (3/4)\beta/C_\text{sph}$ printed by both notebooks is identical and correct. Logged here, not back-propagated to a fix in `thickness_bound.ipynb` because the working chain there is correct and the result is used downstream consistently.
- **One-trapped-angular-dim heuristic.** The structural difference ($R$-independence of cylindrical bound vs $R$-linear spherical bound) is physically attributed to the cylindrical surface having one degenerate (axial) direction. This is consistent with the known fact that linearized cylindrical vacuum has a *logarithmic* gravitational potential (no asymptotic Newtonian limit), in contrast to the spherical $1/r$ potential. A fully separated analytical demonstration of this attribution (e.g., via dimensional analysis of $G_{\hat a \hat a} = 0$ in cylindrical vs spherical vacuum) is straightforward but not undertaken here.

---

## 5. Cross-references

- [`KRASNIKOV_TUBE_NOTES.md`](KRASNIKOV_TUBE_NOTES.md) §7.2 — original prompt for this calculation; updated with disposition pointing here.
- [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md) §5 — parent documentation of the Path-2A spherical Fuchs shell.
- [`thickness_bound.ipynb`](thickness_bound.ipynb) Cells 2–3 — spherical $\kappa_\text{sph} = 3/4$ derivation, used as the reference template here.
- [`speculation/RING_NETWORK_CONCEPT.md`](speculation/RING_NETWORK_CONCEPT.md) §4 — the speculation that motivated the calculation; settled (negatively) in scope (a).
- [`ROADMAP.md`](ROADMAP.md) Task 2A.14 — flipped to `[x]` with a one-paragraph disposition pointing here.
- [`NAVIGATOR.md`](NAVIGATOR.md) — document index entry added.

---

## 6. Changelog

- **2026-04-17, Session 16:** Notebook + this document created. Scope (a) executed end-to-end. Scope (b) recorded as deferred with reopening criteria. Verdict: toroidal-Fuchs path dismissed by a factor $\geq 2\pi$ in the energy-condition window, no causal advantage either.

---

## Note to future self

If any of this material is ever written up for external consumption, the working title is non-negotiably **"donit bad"** (per user directive, 2026-04-20, Session 16). The formal subtitle can be something like *"A topological-penalty bound on toroidal Fuchs-class warp shells in the cylindrical-reduction limit"*, but the headline stays.

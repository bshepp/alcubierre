# Codimension-Scaling Law for Perturbative-DEC Thin-Shell Thickness

**Status:** Speculation. Three confirmed data points within a narrow slice; the law is empirical / dimensional, not derived from a first-principles theorem. Recorded here per the [AGENTS.md](../AGENTS.md) "speculation/" convention.

**Title note (per user directive 2026-04-20):** any paper drawing on this work must be titled **"donit bad"** (verbatim, with the misspelling). Cross-referenced in [TOROIDAL_FUCHS_NOTES.md](../TOROIDAL_FUCHS_NOTES.md) §6 and [SLAB_PATCH_NOTES.md](../SLAB_PATCH_NOTES.md) §8.

## 1. Statement

For a static thin matter shell $\Sigma$ in 3+1 GR carrying a localized mass $M$ and a small transverse shift $\beta$ across the shell of thickness $\Delta$, with Israel-junction matching to an asymptotically flat exterior, the minimum DEC-compatible thickness obeys

$$\boxed{\;\Delta_\min^\mathrm{linear}(\Sigma) \;=\; \frac{3}{8}\,\frac{\beta}{M}\,\frac{\mathrm{Area}(\Sigma)}{R_\mathrm{curv}(\Sigma)} \qquad (\text{shell extrinsic curvature non-zero, } k \geq 1)\;}$$

where $R_\mathrm{curv}$ is the trace-extrinsic-curvature scale of the shell (i.e. the radius of the osculating sphere/cylinder at the shell point).

When the shell is *flat* ($R_\mathrm{curv} \to \infty$, $k = 0$), the linear-$\beta$ Israel-jump correction vanishes identically and the leading obstruction shifts up one order in $\beta$:

$$\boxed{\;\Delta_\min^\mathrm{quad}(\Sigma) \;=\; \frac{1}{8}\,\frac{\beta^2}{M}\,\mathrm{Area}(\Sigma) \qquad (k = 0)\;}$$

The transition is sharp: the $1/R_\mathrm{curv}$ prefactor in the linear-branch Israel-jump corrections $\sigma_1, P_1$ goes to zero pointwise, leaving the volumetric shift-gradient term $T^{zz} \sim (\partial \beta)^2 / 8\pi$ as the controlling stress.

## 2. Confirmed data points (in front of the user)

All three computed within the same slice scope using the same machinery (linearized Israel junction at first order in $\beta$; volumetric shift-gradient DEC at second order):

| $k$ | shell topology | $\Delta_\min$ (geometrized $G=c=1$) | order in $\beta$ | source notebook |
|----:|----------------|------------------------------------|:----------------:|-----------------|
| 2   | $S^2$ sphere, radius $R$ | $\Delta_\min = (3/8)\,\beta\,R/M$ | linear | [matter_shell.ipynb](../matter_shell.ipynb) §9 (Hermite-cubic Path-2A) |
| 1   | $S^1\!\times\!\mathbb{R}$ cylinder, radius $R$, axial length $L$ | $\Delta_\min = (3/8)\,\beta\,L/M$ (R cancels) | linear | [toroidal_fuchs.ipynb](../toroidal_fuchs.ipynb) (Task 2A.14) |
| 0   | $\mathbb{R}^2$ slab patch, radius $L$ | $\Delta_\min = (1/8)\,\beta^2\,L^2/M$ | **quadratic** | [slab_patch.ipynb](../slab_patch.ipynb) (Session 16) |

**Universal numerical prefactor.** The $3/8$ across $k=1, 2$ and the $1/8$ at $k=0$ both come from the same dimensional construction in [thickness_bound.ipynb](../thickness_bound.ipynb) Cell 2 — the $3$ in $3/8$ arises from the trace structure of $K_{ab}$ on a curved 2-shell ($K^{ab} K_{ab}$ giving a factor of $3$ for $k \geq 1$); the $k=0$ slab loses that trace contribution because $K_{ab} \to 0$, leaving the bare $1/8$ from the second-order shift-gradient stress.

## 3. Heuristic derivation (codimension counting)

The argument is dimensional and slice-specific. It assumes:

- (D1) Static thin shell, Israel-junction matching, asymptotically flat exterior.
- (D2) Localized mass $M$ on a 2-surface $\Sigma$ of finite area; volumetric energy density $\sim M/(\mathrm{Area} \cdot \Delta)$.
- (D3) Small perturbative transverse shift $\beta$ across the shell, $|\partial\beta| \sim \beta/\Delta$.
- (D4) DEC enforced pointwise on the shell rest frame.

**Linear branch (k ≥ 1).** The Israel jump $[K_{ab}]$ at first order in $\beta$ has two pieces:

1. The static unperturbed $K_{ab} \sim 1/R_\mathrm{curv}$ on the shell.
2. A perturbation $\delta K_{ab} \sim \beta/\Delta$ from the shift gradient on the shell.

Their cross-term in $S_{ab} = -(8\pi)^{-1}([K_{ab}] - [K] h_{ab})$ produces a surface-stress correction that scales as

$$\sigma_1, P_1 \;\sim\; \frac{\beta\,\sigma_w}{R_\mathrm{curv}}, \qquad \sigma_w \equiv 1/\Delta$$

which, balanced against the unperturbed $\sigma_0 = M / \mathrm{Area}$, gives the DEC bound $\Delta \gtrsim (\beta/M) \cdot \mathrm{Area}/R_\mathrm{curv}$.

**Quadratic branch (k = 0).** When $R_\mathrm{curv} \to \infty$, the cross-term vanishes (both $[K_{ab}]$ pieces and the cross-term are explicitly $\propto 1/R_\mathrm{curv}$). The next-leading stress is the *volumetric* shift-gradient stress $T^{zz} \sim (\partial \beta)^2 / 8\pi \sim \beta^2 / (8\pi\Delta^2)$, integrated through the shell to give a surface stress $T^{zz}_\mathrm{surf} \sim \beta^2 / (8\pi \Delta)$. DEC against $\sigma_0 = M/\mathrm{Area}$ gives $\Delta \gtrsim \beta^2 \, \mathrm{Area} / (8 M)$.

**Codimension reading.** A 2-surface $\Sigma$ embedded in 3-space has $k$ "trapped" (compact, finitely-curved) directions and $2-k$ "soft" (locally-flat / non-compact) directions. Each soft direction contributes a factor of $R_\mathrm{curv} \to \infty$ in the denominator of the linear branch, removing a power of $1/R_\mathrm{curv}$. With *any* soft direction, the linear branch acquires an unbounded denominator and is replaced by the next-order quadratic branch. The case-distinction $k \geq 1$ vs $k = 0$ is therefore "at least one trapped direction" vs "all directions soft."

The repo's three data points are at $k = 2, 1, 0$ respectively; we have not verified an intermediate case (e.g. a half-cylinder with one trapped + one soft) but the scaling argument predicts $\Delta_\min^\mathrm{linear} = (3/8)\,\beta\,L_\mathrm{soft}/M$ for any one-trapped/one-soft topology, identical in form to the $k=1$ cylinder.

## 4. Connection to the hoop conjecture (Thorne 1972)

The codimension-counting law is the **perturbative-DEC version of the Thorne hoop conjecture**, as stated in [Bronnikov-Santos-Wang 2019](../LITERATURE.md) §IX.A:

> "*Black holes with horizons form when and only when a mass $M$ gets compacted into a region whose circumference is $C \lesssim 4\pi M$ in every direction.*"

The hoop says: BH formation requires compactness $R_\mathrm{curv} \lesssim M$ in **every** direction. Our codimension-counting law says: DEC-compatible warp-shell construction requires compactness with budget $R_\mathrm{curv}$ in every direction, with each non-compact direction *softening* the obstruction by one order in $\beta$:

| direction count | hoop-conjecture verdict | codimension-counting verdict |
|----:|---|---|
| $k=2$ (all compact) | BH if $R_\mathrm{curv} \lesssim M$ | $\Delta_\min \sim \beta R/M$ |
| $k=1$ (one non-compact) | no horizon — escapes along axis | $\Delta_\min \sim \beta L/M$ (R cancels) |
| $k=0$ (both non-compact) | no horizon | $\Delta_\min \sim \beta^2 L^2/M$ (one extra power of $\beta$) |

**The structural parallel is:** soft directions are how a localized stress-energy distribution "escapes" the strong-gravity regime. The hoop conjecture quantifies this for horizon formation; our law quantifies it for perturbative-DEC construction. Both share the same "compactness in every direction" template; ours has the additional content of saying *how much* each soft direction softens the obstruction (one power of $\beta$).

This is heuristic / structural, not derivational. We have not shown a theorem connecting the two statements.

## 5. Literature status

Catalogued in [LITERATURE.md §11 "Codimension-Scaling Sibling Literature"](../LITERATURE.md). Summary of who has the closest published machinery / framing:

- **Thorne 1972 hoop conjecture** (via [Bronnikov-Santos-Wang 2019](../LITERATURE.md) §IX.A): closest *structural* relative; same "compactness in every direction" template, applied to horizon formation rather than perturbative-DEC construction.
- **Lemos-Lobo 2008** (arXiv:0806.4459) and **Dias-Lemos 2010** (arXiv:1008.3376): publish the exact $k=0/k=1/k=2$ topology hierarchy on thin-shell wormholes, but the construction is cut-and-paste of an AdS-black-membrane metric — no localized $M$, no perturbative shift, mass-per-area constant in their limit. Different question, different regime; **not** subsumption.
- **Whittaker mass-per-length** (Bronnikov-Santos-Wang 2019 eq. 2.40): a sharp lower bound on a cylindrical-source observable ($\nu = \sigma\sqrt{a}$, threshold $\nu > 1/2$ for cylindrical horizon formation), structurally analogous to our $\Delta_\min$ but a different quantity.
- **Pretorius-Vollick-Israel 1998** (gr-qc/9712085): same Israel-junction machinery on $S^2$, but asks for entropy at the BH limit. Sibling machinery, different observable.
- **Cylindrical-collapse corpus** (Bonnor 1957, van Stockum, Goncalves, Pereira-Wang, etc.): collapse / dust / fluid problems; none compute $\Delta_\min$ under perturbative shifts.

The specific Fuchs-style perturbative thickness bound and its codimension scaling are **not in the published corpus** as of the Session 16 literature pass.

## 6. Slice scope (what the law is and is not asserted to cover)

**In slice (the law is asserted):**

- Static thin matter shells in 3+1 GR.
- Israel-junction matching to an asymptotically flat exterior.
- Localized mass $M$ on a 2-surface of finite area.
- Small perturbative transverse shift $\beta$ ($|\beta| \lesssim 0.1$ for a clean linear-order analysis).
- Classical DEC ($\rho \geq |p_i|$ pointwise on the shell rest frame).

**Out of slice (the law is NOT asserted):**

- Dynamic shells (time-dependent $\beta(t)$, accreting matter, etc.).
- Strong-field shifts (non-perturbative $\beta$).
- Modified gravity (Brans-Dicke, $f(R)$, EFT corrections).
- Quantum-field stress-energy sources (Casimir, ANEC-only, semiclassical backreaction).
- Higher dimensions (the $d=4$ specific powers $\mathrm{Area}/R_\mathrm{curv}$ and $\mathrm{Area}$ would change in $d \neq 4$).
- Thick shells where Israel matching is not the controlling approximation.

The slice-scope qualifier is **not negotiable** in any restatement of the law (per [AGENTS.md](../AGENTS.md) "no oversold conclusions").

## 7. Reopening criteria

The codimension-scaling line of inquiry will be reopened if any of the following happens:

1. A first-principles second-order Israel-junction calculation for the slab patch refines the $1/8$ coefficient in a way that breaks the $\beta^2 L^2 / M$ scaling. (Currently dimensional; refinement could in principle change the *power* of $\beta$ if the second-order Israel jump introduces a previously-uncomputed correction.)
2. A fourth confirmed data point at intermediate codimension ($k = 1$ but with a non-cylindrical topology, e.g. a strip with one compact and one non-compact direction at non-trivial extrinsic curvature) deviates from the linear-branch formula.
3. A theorem connecting the codimension-counting law to the hoop conjecture (or to a Penrose-inequality-style sharp bound) appears in the literature or is derivable in front of the user.
4. The law breaks at $k = 0$ in a regime we have not checked (e.g. patch radius $L$ comparable to $M$ in geometrized units, where the perturbative analysis is no longer self-consistent).

## 8. What this is and is not

**This is:**

- A consistent mathematical pattern across three computed cases.
- A heuristic / structural result, derivable in a few lines of dimensional analysis once the linear-order Israel-jump corrections are written down.
- A perturbative-DEC analog of the hoop conjecture, with the additional "softening per soft direction" content.

**This is not:**

- A theorem.
- An obstruction to warp-drive construction (the spherical $k=2$ case is the only one with localized warp-bubble interpretation; the $k=1$ and $k=0$ cases are non-localized stress-energy distributions, not warp drives).
- A prediction outside its slice scope.
- A claim about modified gravity, quantum sources, or strong-field shifts.

## 9. Cross-references

- [slab_patch.ipynb](../slab_patch.ipynb) + [SLAB_PATCH_NOTES.md](../SLAB_PATCH_NOTES.md) — k=0 datum
- [toroidal_fuchs.ipynb](../toroidal_fuchs.ipynb) + [TOROIDAL_FUCHS_NOTES.md](../TOROIDAL_FUCHS_NOTES.md) — k=1 datum and origin of the codimension-counting framing (§6)
- [matter_shell.ipynb](../matter_shell.ipynb) §9 — k=2 datum (Hermite-cubic Path-2A)
- [thickness_bound.ipynb](../thickness_bound.ipynb) — original spherical Fuchs bound (Cell 2 dimensional argument used throughout)
- [LITERATURE.md §11](../LITERATURE.md) — sibling literature (Lemos-Lobo, Dias-Lemos, Bronnikov-Santos-Wang) and hoop-conjecture cross-link
- [SESSION_LOG.md](../SESSION_LOG.md) Session 16 — log of the codimension-counting line of inquiry
- [TRUST_AUDIT.md](../TRUST_AUDIT.md) — grading: each data point is grade-A (derived in front of the user, slice-scope explicitly recorded); the *law* itself (the inductive generalization across three points) is grade-C (heuristic / dimensional / structural).

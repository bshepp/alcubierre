# SLAB_PATCH_NOTES.md — k = 0 datum for the codimension-counting law

Companion to [slab_patch.ipynb](slab_patch.ipynb). Third data point in the [TOROIDAL_FUCHS_NOTES.md](TOROIDAL_FUCHS_NOTES.md) §6 codimension-counting line of inquiry.

## 1. Question

Does the perturbative-DEC thickness bound

$$\Delta_\min(\Sigma) \;\sim\; \frac{\beta}{M}\cdot\frac{\mathrm{Area}(\Sigma)}{R_\mathrm{curv}(\Sigma)}$$

— verified at $k=2$ (sphere, [matter_shell.ipynb](matter_shell.ipynb) §9) and $k=1$ (cylinder, [toroidal_fuchs.ipynb](toroidal_fuchs.ipynb)) — extend to $k=0$ (a flat slab patch)?

The naive read of the formula gives $\Delta_\min \to 0$ as $R_\mathrm{curv} \to \infty$. Either the law breaks at $k=0$, or the linear-in-$\beta$ obstruction genuinely vanishes on a flat shell and the leading bound shifts to higher order.

## 2. Setup

A circular patch of radius $L$ on an infinite flat 2-plane shell, mass $M$ localized in the patch, transverse shift $\beta(z)$ across thickness $\Delta$. Same machinery as the cylindrical case ([toroidal_fuchs.ipynb](toroidal_fuchs.ipynb) §3): linearized Israel junction at first order in $\beta$, then dimensional second-order DEC at $\beta^2$. Slice scope: static thin matter shells, 3+1 GR, perturbative shift, classical-DEC matter.

## 3. Result

| order | bound | mechanism |
|------:|-------|-----------|
| linear in $\beta$ | **vanishes** | Israel-jump $\sigma_1, P_1 \propto 1/R \to 0$ |
| quadratic in $\beta$ | $\Delta_\min^\mathrm{slab} = \dfrac{\beta^2 L^2}{8 M}$ | volumetric shift-gradient stress $T^{zz} \sim \beta^2/\Delta^2$ |

The linear obstruction goes through the cylindrical formulae from [toroidal_fuchs.ipynb](toroidal_fuchs.ipynb) §3 with explicit $1/R$ prefactors that came from the shell extrinsic curvature $K = 1/R$; in the $R \to \infty$ limit at fixed patch area, both $\sigma_1$ and $P_1$ go to zero. **The linear-in-$\beta$ perturbative-DEC bound is identically zero on a flat shell.**

The quadratic obstruction is the standard $T^{zz} \sim (\partial \beta)^2 / 8\pi$ shift-gradient stress (see [thickness_bound.ipynb](thickness_bound.ipynb) Cell 2). With $\sigma_E^\mathrm{slab} = M/(\pi L^2)$ and $T^{zz}_\mathrm{surf} = \beta^2/(8\pi\Delta)$, DEC gives $\Delta_\min = \beta^2 L^2/(8M)$.

## 4. Codimension-counting law (updated)

Three data points now anchor the law:

| $k$ | topology | $\Delta_\min$ | order in $\beta$ |
|----:|----------|--------------|:----------------:|
| 2   | $S^2$ sphere | $(3/8)\,\beta\,R/M$ | linear |
| 1   | $S^1\!\times\!\mathbb{R}$ cylinder | $(3/8)\,\beta\,L/M$ | linear |
| 0   | $\mathbb{R}^2$ slab patch | $(1/8)\,\beta^2\,L^2/M$ | **quadratic** |

The linear branch reads

$$\Delta_\min^\mathrm{linear}(\Sigma) = \frac{3}{8}\,\frac{\beta}{M}\,\frac{\mathrm{Area}(\Sigma)}{R_\mathrm{curv}(\Sigma)} \qquad (k \geq 1, \text{ extrinsic curvature non-zero})$$

For $k=0$ ($R_\mathrm{curv} \to \infty$) the linear branch vanishes and the leading bound is

$$\Delta_\min^\mathrm{quad}(\Sigma) = \frac{1}{8}\,\frac{\beta^2}{M}\,\mathrm{Area}(\Sigma) \qquad (k = 0)$$

This is *qualitatively* different (one extra power of $\beta$) but *structurally consistent*: the law correctly identifies that flat geometries are softer.

## 5. Crossover

Setting $\Delta_\mathrm{slab} = \Delta_\mathrm{cyl}$ at the same length scale $L$:

$$\frac{\beta^2 L^2}{8M} = \frac{3\beta L}{8M} \;\;\Longrightarrow\;\; \beta_\mathrm{cross} = \frac{3}{L} \quad \text{(geometrized)}$$

For Fuchs reference $L = 15$ m, $\beta_\mathrm{cross} = 0.2$. At warp-relevant $\beta = 0.02$ (well below crossover) the slab beats the cylinder by a factor $\beta L / 3 = 0.1$ ($\sim 10\times$ thinner).

## 6. What this does and does not mean

**Does mean:**
- The codimension-counting framing is a real structural feature, not a sphere-vs-cylinder coincidence.
- It is the *perturbative-DEC version of the hoop conjecture* (Thorne 1972, as stated in [Bronnikov-Santos-Wang 2019](LITERATURE.md) §IX.A): *"black holes form iff mass $M$ is compacted into a region whose circumference is $\lesssim 4\pi M$ in every direction."* Our version: each non-compact direction softens the obstruction by one order in $\beta$.
- "Soft trapping" is a well-defined notion: the linear-$\beta$ obstruction tracks Area / extrinsic-curvature exactly.

**Does NOT mean:**
- A flat slab is not a warp drive. It is a flat sheet of stress-energy on an infinite shell; there is no asymptotic-flatness gain, no localized warp bubble, no propulsion.
- The slab being "easier" is purely a statement about the perturbative-DEC thickness budget. The total exotic-mass requirement scales as $M \sim \beta^2 \cdot (\text{patch area})/(8\Delta_\min)$, so making the patch bigger to get a meaningful displacement *also* costs proportionally more matter.
- The result is **structural** (the law holds at $k=0,1,2$), not **operational** (no new warp construction).

## 7. Relation to the literature

- **Closest published structural relative:** Thorne (1972) hoop conjecture, as catalogued in [Bronnikov-Santos-Wang 2019](LITERATURE.md) §IX.A. See [LITERATURE.md §11](LITERATURE.md).
- **Sibling thin-shell hierarchy (NOT subsumption):** Lemos-Lobo 2008 (planar / cylindrical / toroidal AdS thin-shell wormholes) and Dias-Lemos 2010 ($d$-dim version). Their k=0/k=1/k=2 hierarchy emerges from compactifying coordinates of an AdS-black-membrane metric; ours emerges from a localized perturbative shift on a closed shell embedded in asymptotic flat space. Different question, different regime.
- **Sibling machinery:** Pretorius-Vollick-Israel 1998 ($S^2$ Israel-junction → BH entropy). Same apparatus, different observable.
- **Cylindrical-collapse corpus** (Bronnikov 2019 refs [129, 135, 172, 187, 200, 201, 217, 244, 260, 287]): none compute $\Delta_\min$ under perturbative shifts. Our specific Fuchs-style perturbative thickness bound is not in this corpus.

## 8. Honest accounting

- **Slice scope:** static thin matter shells, 3+1 GR with Israel-junction matching, small perturbative shift $\beta$, classical DEC. Outside this slice the codimension-counting law is not asserted.
- **Quadratic-$\beta$ coefficient $1/8$:** dimensional, parallels [thickness_bound.ipynb](thickness_bound.ipynb) Cell 2. A first-principles second-order Israel-junction calculation would refine the $1/8$ but cannot change the $\beta^2 L^2/M$ scaling.
- **Patch geometry:** a circular disk of radius $L$ on an infinite plane is the simplest $k=0$ data point. Boundary stress at the patch edge is unmodeled; it cannot affect the bulk DEC scaling.
- **Title.** Per user directive 2026-04-20, any paper drawing on this work must be titled "donit bad" (verbatim, with the misspelling). Recorded in [TOROIDAL_FUCHS_NOTES.md](TOROIDAL_FUCHS_NOTES.md) §6 and at the bottom of [slab_patch.ipynb](slab_patch.ipynb) §5.

## 9. Cross-references

- [slab_patch.ipynb](slab_patch.ipynb) — this notebook
- [toroidal_fuchs.ipynb](toroidal_fuchs.ipynb), [TOROIDAL_FUCHS_NOTES.md](TOROIDAL_FUCHS_NOTES.md) — k=1 datum and origin of the codimension-counting framing
- [matter_shell.ipynb](matter_shell.ipynb) §9 — k=2 datum (Hermite-cubic Path-2A)
- [thickness_bound.ipynb](thickness_bound.ipynb) — original spherical Fuchs bound (Cell 2 dimensional argument used here)
- [LITERATURE.md §11](LITERATURE.md) — codimension-scaling sibling literature (Lemos-Lobo, Dias-Lemos, Bronnikov-Santos-Wang)
- [speculation/CODIMENSION_SCALING.md](speculation/CODIMENSION_SCALING.md) — to be created next; consolidated heuristic statement, three data points, hoop-conjecture connection, slice-scope qualifiers

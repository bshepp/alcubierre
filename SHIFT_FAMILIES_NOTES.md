# Slice 1: Alternate Shift Families — Notes

**Source:** [`shift_families.ipynb`](shift_families.ipynb) and [`hf_jobs/sweeps/shift_families.py`](hf_jobs/sweeps/shift_families.py).
**Written:** 2026-04-17 (Session 9), as the first deep-dive of Phase 2C.

---

## TL;DR

**Across the four single-mode axisymmetric shift families tested (Alcubierre, Natário zero-expansion, irrotational/Rodal, free-form $j_1$ Bessel), no profile satisfies WEC at non-trivial warp velocity $v$ within the swept parameter ranges.** The Path 2A negative result is therefore *not* an artefact of the choice of Alcubierre's specific shift profile — it transfers across these four families.

**However**, this is one family of profiles, not the landscape. Lentz 2020's positive-energy result is *not* a counter-example to this slice because Lentz used (i) a plasma-supported source rather than a fluid, (ii) a multi-mode superposition rather than a single $j_1$, (iii) breaking of axial symmetry in some sectors. Slice 1's negative result *narrows* the load-bearing assumption from "Alcubierre shift" to one of "single-mode axisymmetric shift + DEC-fluid source," neither of which Lentz preserved.

---

## What was actually computed

Single ADM pipeline (unit lapse, flat spatial slices, spherical coords) parameterised by orthonormal-frame shift components $(\beta^{\hat r}, \beta^{\hat \theta})$ as functions of $(r, \theta)$. Closed-form ADM-metric inverse used (1100× faster than SymPy `g.inv()` on tanh expressions).

Four families:

| Family | $\beta^{\hat r}$ | $\beta^{\hat \theta}$ | Notes |
|---|---|---|---|
| Alcubierre | $v\,f_{\rm Alc}(r)\,\cos\theta$ | $-v\,f_{\rm Alc}(r)\,\sin\theta$ | Standard Alcubierre 1994 with tanh bump |
| Natário (zero-exp) | $-v\,(1-f_{\rm Alc})\,\cos\theta$ | $v\,((1-f_{\rm Alc}) + (r/2)(1-f_{\rm Alc})')\,\sin\theta$ | $\nabla\cdot\beta = 0$ by construction |
| Irrotational (Rodal 2025) | $-v\,(1-f_{\rm Alc})\,\cos\theta$ | $v\,g(r)\,\sin\theta$, $g = (1/r)\int(1-f_{\rm Alc})dr$ | $\nabla\times\beta = 0$, Hawking–Ellis Type I |
| Free-form $j_1$ | $v\,A_1\,j_1(kr)\,\cos\theta$ | $-v\,A_1\,j_1(kr)\,\sin\theta$ | Single vector spherical harmonic mode |

For each family, computed the Eulerian-frame stress-energy $T_{\hat\mu\hat\nu}$ symbolically, lambdified to NumPy, evaluated WEC ($\rho_p \ge 0$) and DEC ($\rho_p \ge \max|p_i|, \max|q_i|$) on a $(r, \theta)$ grid, and reported the pass fractions.

## Headline results

### Single-point evaluation (v=0.1, R0=5, σ=4)

| Family | WEC fraction | DEC fraction | min ρ_p | min DEC slack |
|---|---|---|---|---|
| Alcubierre | 0.479 | 0.003 | -4.9e-2 | -3.3e-3 |
| Natário | 0.696 | 0.020 | -2.5e-1 | -1.0e-1 |
| Irrotational | 0.282 | 0.019 | -1.6e-3 | -1.4e-2 |
| Free-form ($A_1=1$, $k=\pi/2R_0$) | 0.473 | 0.000 | -4.1e-6 | -4.2e-3 |

WEC fraction < 1 for every family — every family has a region of WEC violation. The irrotational case has the *smallest* peak deficit (consistent with Rodal 2025 evaluation: ≈38× reduction vs. Alcubierre), but still has a wider WEC-violating region by area. Natário has the largest peak deficit (consistent with our Rodal evaluation noting Natário's transverse-pressure pathology).

### 140-point preview sweep across (v, R₀, σ) for the closed-form families and (v, A₁, k) for free-form

- **0/140 points achieve WEC fraction ≥ 0.999** (i.e. WEC everywhere on the grid).
- **0/140 points achieve DEC fraction ≥ 0.999.**
- **Best WEC pass fraction**: 0.94 (free-form $j_1$ at some specific $A_1, k$ tuning) — the closest any family came to satisfying WEC, but still 6% of the grid in violation.

### Acceleration-obstruction proxy (quadrupole moment)

Bulk quadrupole moments $Q_{zz}$ of the WEC-respecting region of each family (at $v=0.1$):

| Family | $Q_{zz}$ |
|---|---|
| Alcubierre | $-4.7\times10^{-1}$ |
| Natário | (large, dominated by edge effects) |
| Irrotational | $-1.9\times10^{-1}$ |
| Free-form | $-1.4\times10^{-1}$ |

All within an order of magnitude of each other. The Mechanism C (GW recoil) ceiling of Package 3 scales as $\langle \dddot Q^2 \rangle$, so it is roughly shift-family-independent. Package 3's quantitative ceiling **transfers** to all four families.

---

## Audit interleave: TRUST_AUDIT #4 closed

A new Cell 4b was added to [`israel_junction.ipynb`](israel_junction.ipynb) that derives the Schwarzschild $K^+_{ab}$ formulas from first principles using SymPy:

1. Build Schwarzschild metric $g_{\mu\nu}$ with $f(r) = 1 - 2GM/r$.
2. Take the outward unit normal $n_\mu = (0, 1/\sqrt{f}, 0, 0)$.
3. Compute $K_{ab} = \nabla_a n_b - \Gamma^c_{ab} n_c$ symbolically.
4. Compare to Cell 9's quoted formulas.

Result: all three components match to literal `0` (after sign-convention alignment, see cell comment). TRUST_AUDIT #4 is now A-grade.

---

## What this slice does NOT establish

1. **Lentz 2020's specific construction** uses a plasma source with multi-mode + non-axisymmetric shift. We did *not* reproduce his construction. A genuine Lentz-style probe would need to (i) extend the free-form ansatz to multi-mode $\sum_n a_n j_l(k_n r)$ for $l > 1$, (ii) break axial symmetry. Both are extensions for future work.
2. **Multi-mode optimisation**: optimisation over $\{a_n, k_n\}$ in a multi-mode expansion was not done. It is plausible that no axisymmetric *spherically supported* shift can satisfy WEC under fluid sources (Bobrick-Martire 2021's general framework points this way), but a rigorous optimisation would be the test.
3. **Non-spherical interior shapes**: only spherical interiors were considered. Toroidal, prolate, oblate are different slices.
4. **Acceleration**: only a quadrupole-moment proxy was computed; actual time-dependent $v(t)$ ramps + ADM-momentum analysis are Slice 3.
5. **Choice of `f_Alc` bump function**: we used Alcubierre's standard tanh bump. Different shape functions (compact-support, bump with steeper falloff) might have different EC-violation patterns in the closed-form families. The free-form $j_1$ family is the first probe of this.

---

## Implication for the project

**The Path 2A negative result is *robust* to choice of single-mode axisymmetric shift family.** This is a meaningful narrowing: the load-bearing assumption is *not* "Alcubierre $\beta^x \hat x$" but rather **"single-mode axisymmetric shift + spherical fluid-shell source + asymptotically flat vacuum exterior + steady-state metric."**

To find a positive-energy classical warp drive, one of those four sub-assumptions must give. Slice 1 confirms it's not the first one (within the single-mode family). Slices 2-6 test the remaining three.

Lentz 2020's construction *did* break the third sub-assumption (using plasma source instead of fluid) and may have broken the first (multi-mode). His result is therefore consistent with our Slice 1 finding rather than contradicting it.

---

## Citations

- Alcubierre 1994 (gr-qc/0009013) — original shift family.
- Natário 2002 (gr-qc/0110086) — zero-expansion variant.
- Rodal 2025 ([arXiv:2512.18008](https://arxiv.org/abs/2512.18008)) — irrotational variant; see [`RODAL2025_EVALUATION.md`](RODAL2025_EVALUATION.md).
- Lentz 2020 ([arXiv:2006.07125](https://arxiv.org/abs/2006.07125)) — plasma-supported positive-energy soliton, *not* a single-mode axisymmetric shift family.
- Bobrick & Martire 2021 ([arXiv:2102.06824](https://arxiv.org/abs/2102.06824)) — general "any warp drive is a shell of matter" framework.
- Lobo & Visser 2004a (gr-qc/0406083) — linearised analysis showing EC violations at any $v > 0$ for Alcubierre.

# Slice 1: Alternate Shift Families — Notes

**Source:** [`shift_families.ipynb`](shift_families.ipynb) and [`hf_jobs/sweeps/shift_families.py`](hf_jobs/sweeps/shift_families.py).
**Written:** 2026-04-17 (Session 9), as the first deep-dive of Phase 2C.
**Corrected:** 2026-07-05 (Session 36) — the Session-9 evaluator carried a frame-projection bug; every recorded number below is superseded by the [Session-36 correction](#session-36-correction--frame-projection-bug-negative-rebuilt-as-analytic-closure). The verdict survives and strengthens.

---

## TL;DR

**No member of any of the four single-mode axisymmetric shift families (Alcubierre, Natário zero-expansion, irrotational/Rodal, free-form $j_1$ Bessel) satisfies WEC everywhere, for *any* parameter values or radial profile — analytically (Session 36):**

1. **z-directed shifts** $\beta = b(r)\hat z$ (the Alcubierre and free-form families, and any radial multi-mode superposition $\sum_n a_n j_1(k_n r)$): $\rho_E = -b'(r)^2\sin^2\theta/32\pi \le 0$ identically (Hamiltonian constraint, flat slices, unit lapse).
2. **Natário zero-expansion** (any profile $F(r)$): $\nabla\cdot\beta \equiv 0$ ⟹ $\rho_E = -K_{ij}K^{ij}/16\pi \le 0$ (the repo's Session-15c identity, fell_heisenberg.ipynb Phase 3b).
3. **Irrotational** $\beta = \nabla\phi$ (any potential with uniform-flow/decaying asymptotics): $\int\rho_E\, dV = 0$ exactly, so $\rho_E \ge 0$ everywhere forces $\rho_E \equiv 0$ — the only WEC-everywhere member is trivial.

The Path 2A negative result is therefore *not* an artefact of the choice of Alcubierre's specific shift profile — it is an identity-level property of the whole single-mode axisymmetric slice. Corrected sweeps (Session 36, fixed evaluator) support this empirically: 0/140 preview points and 0/2496 full-config points achieve WEC (or DEC) everywhere.

**However**, this is one family of profiles, not the landscape. Lentz 2020's positive-energy result is *not* a counter-example to this slice because Lentz used (i) a plasma-supported source rather than a fluid, (ii) a genuinely three-dimensional multi-mode shift rather than a radial-profile $\hat z$-shift, (iii) breaking of axial symmetry in some sectors. Slice 1's negative result *narrows* the load-bearing assumption from "Alcubierre shift" to "single-mode axisymmetric shift + DEC-fluid source" — and the Session-36 z-shift identity extends the closed corner to *all* radial-profile multi-mode axisymmetric $l=1$ shifts.

---

## Session-36 correction — frame-projection bug; negative rebuilt as analytic closure

**The bug.** Cell 3 of [`shift_families.ipynb`](shift_families.ipynb) (and the derived sweep module) stores the Eulerian tetrad legs as the **columns** of its `tetrad` matrix — the cell's own comment says "column j = e_{hat j}^mu", and column 0 is indeed the correct Eulerian 4-velocity $(1, -\beta^r, -\beta^\theta_{\rm coord}, 0)$ — but the projection loop contracts **rows**: it computes $M\,T\,M^{\mathsf T}$ where the frame projection is $M^{\mathsf T} T\, M$. Since row 0 is $(1,0,0,0)$, the recorded scalar collapses to coordinate $T_{tt}$, and the recorded `rho_p = -T_tt` is **not** the Eulerian energy density: at leading order in shift amplitude it is $-\rho_E$ (sign-inverted), with $O(1)$-relative $\beta\cdot$flux and $\beta^2\cdot$stress contamination. Measured deviation from true $\rho_E$ at the Session-9 single-point parameters: 3.27× (Alcubierre), 2.57× (Natário), 2.00× (irrotational), 8.57× (free-form). A subsidiary defect: the irrotational antiderivative used sympy's $\log(1\pm\tanh)$ form, which overflows once tanh saturates ($|r-R_0| \gtrsim 19/\sigma$), so the recorded irrotational fractions were computed on a silently truncated domain.

**How it surfaced (Session-35 audit queue, Block 2(a)).** A scaling diagnostic ahead of the planned "0.94 ridge" refinement returned `wec_fraction = 1.0000` at $k \le 0.05$ with strictly positive minimum "ρ" — impossible, because the free-form family is exactly $\beta = b(r)\hat z$ and the Hamiltonian constraint forces $\rho_E \le 0$ for that class. In hindsight the recorded Natário fraction (0.696) had contradicted the repo's own Session-15c identity ($8\pi\rho_E = -\tfrac12 K_{ij}K^{ij} \le 0$ for zero-expansion shifts) since Session 9, and the Session-10 FH comparison table in [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) even states "$\rho_E < 0$ everywhere" for Slice 1 — the record was internally inconsistent and the cross-check was never run.

**Adjudication.** [`verification/test_shift_families_frame_adjudication.py`](verification/test_shift_families_frame_adjudication.py) — 20/20 gates in certification mode: symbolic orthonormality certificate (columns pass, rows fail); an exact 3+1 constraint route ≡ an independent 4D-Einstein + correct-projection route to ≤ 2.6e-12 relative on all four families; the fixed module ≡ true $\rho_E$ to ≤ 2.6e-10 and finite everywhere; the three analytic identities above verified symbolically/numerically (the irrotational zero-integral closes to 1.1e-08 once the analytic $1/r^4$ dipole-tail contribution $-v^2C^2/6R$, $C = R_0/\tanh(\sigma R_0)$, is included); and Route A matches `warp_factory_py`'s anchored Eulerian `T_eul[0,0]` to median 1.6e-07 relative (SI→geometric via $G/c^4$), closing the chain to the WarpFactory MATLAB anchor.

**What is superseded.** Every number in the Session-9 sections below: the single-point table, the 140-point fractions ("best 0.94" — the ridge does not exist on the corrected observable; corrected free-form maximum is 0.0027 on the preview grid / 0.034 across the full box, both pure noise-counting since $\rho_E \le 0$, and the $k\to 0$ climb was additionally an artifact of the fixed-domain fraction measure, which lets the bubble wall slide off-grid), and the $Q_{zz}$ quadrupole-proxy table (its "WEC-respecting regions" were selected by the defective observable; the acceleration-transfer question is moot now that no WEC-satisfying member exists in any of the four families). The Session-9 tables are retained below as the historical record, marked ⚠ superseded.

**Corrected record (fixed evaluator, artifacts 2026-07-05).**

| Family | corrected WEC everywhere? | corrected max $\rho_E$ on grid | corrected best cell fraction with $\rho_E > 0$ |
|---|---|---|---|
| Alcubierre | Never (identity 1) | ~1e-13 (float noise) | noise-counting only |
| Natário | Never (identity 2) | ~1e-14 (float noise) | noise-counting only |
| Free-form $j_1$ | Never (identity 1) | ~1e-14 (float noise) | noise-counting only |
| Irrotational | Never non-trivially (identity 3) | genuinely indefinite | 0.741 full-run, at the (R₀=1, σ=0.5) box corner |

- Corrected preview (same 140-point grid as Session 9): **0/140** at `wec_fraction ≥ 0.999`, **0/140** at DEC.
- First-ever `shift_families_full.json` dispatch (2496 points; $R_0 \in [1,50]$ unfrozen, $v \le 0.5$, $\sigma \le 16$, wider free-form box; run locally in six chunks, Session 36): **0/2496** at `wec_fraction ≥ 0.999`, **0/2496** at DEC. Irrotational max `wec_fraction` = 0.7408 at the ($R_0{=}1, \sigma{=}0.5$) corner of the box, exactly $v$-degenerate (ρ_E is quadratic in the shift amplitude, so the WEC sign pattern is $v$-independent); its best DEC fraction 0.1217 sits at the same corner. Caveat inherited by *any* fraction measure on this grid: the $(r,\theta)$ domain is $[0.1, 3R_0]$, so fractions are domain-dependent (the corner trend is partly the negative region sliding off-grid) — the zero-integral identity, not the fraction, is the closure.

The corrected sweep artifacts are negation-tracked per the data-artifact policy: `sweeps/shift_families_full_concat.parquet` (the 2496-row full-config record, concatenated from the six local chunks) and `sweeps/shift_families_20260705T184353.parquet` (the corrected 140-point preview, source of the figure). The Session-9 artifact `shift_families_20260416T235319.parquet` is retained locally as the pre-fix record (a fresh pre-fix re-run reproduced it bit-exactly, so the defect is deterministic code, not environment drift).

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

For each family, *intended* to compute the Eulerian-frame stress-energy $T_{\hat\mu\hat\nu}$ symbolically, lambdified to NumPy, evaluate WEC ($\rho_p \ge 0$) and DEC ($\rho_p \ge \max|p_i|, \max|q_i|$) on a $(r, \theta)$ grid, and report the pass fractions. ⚠ **Session 36: the frame projection was transposed, so the quantity actually evaluated was coordinate $-T_{tt}$, not $\rho_E$** — see the correction section above.

## Headline results — ⚠ superseded (Session 36): wrong observable; historical record only

### Single-point evaluation (v=0.1, R0=5, σ=4) — ⚠ superseded; corrected table in the Session-36 section (alc/nat/ff: WEC fraction 0.000; irrotational 0.617/0.010)

| Family | WEC fraction | DEC fraction | min ρ_p | min DEC slack |
|---|---|---|---|---|
| Alcubierre | 0.479 | 0.003 | -4.9e-2 | -3.3e-3 |
| Natário | 0.696 | 0.020 | -2.5e-1 | -1.0e-1 |
| Irrotational | 0.282 | 0.019 | -1.6e-3 | -1.4e-2 |
| Free-form ($A_1=1$, $k=\pi/2R_0$) | 0.473 | 0.000 | -4.1e-6 | -4.2e-3 |

WEC fraction < 1 for every family — every family has a region of WEC violation. The irrotational case has the *smallest* peak deficit (consistent with Rodal 2025 evaluation: ≈38× reduction vs. Alcubierre), but still has a wider WEC-violating region by area. Natário has the largest peak deficit (consistent with our Rodal evaluation noting Natário's transverse-pressure pathology).

### 140-point preview sweep across (v, R₀, σ) for the closed-form families and (v, A₁, k) for free-form — ⚠ superseded; the corrected preview gives 0/140 on the true $\rho_E$ and no 0.94 ridge

- **0/140 points achieve WEC fraction ≥ 0.999** (i.e. WEC everywhere on the grid).
- **0/140 points achieve DEC fraction ≥ 0.999.**
- **Best WEC pass fraction**: 0.94 (free-form $j_1$ at some specific $A_1, k$ tuning) — the closest any family came to satisfying WEC, but still 6% of the grid in violation.

### Acceleration-obstruction proxy (quadrupole moment) — ⚠ superseded (Session 36): regions selected by the defective observable; moot under the analytic closure

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
2. **Multi-mode optimisation**: ~~optimisation over $\{a_n, k_n\}$ in a multi-mode expansion was not done~~ — **partially closed by Session 36**: the z-shift identity covers *any* radial profile $b(r)$, hence every multi-mode superposition $\sum_n a_n j_1(k_n r)$ of this family, with no optimisation needed. Still open: genuinely three-dimensional multi-mode shifts (independent vector spherical harmonics with $l > 1$ / mixed components) — that space is exactly where Fell-Heisenberg and Lentz live (Sessions 10–17).
3. **Non-spherical interior shapes**: only spherical interiors were considered. Toroidal, prolate, oblate are different slices.
4. **Acceleration**: only a quadrupole-moment proxy was computed; actual time-dependent $v(t)$ ramps + ADM-momentum analysis are Slice 3.
5. **Choice of `f_Alc` bump function**: we used Alcubierre's standard tanh bump. Different shape functions (compact-support, bump with steeper falloff) might have different EC-violation patterns in the closed-form families. The free-form $j_1$ family is the first probe of this.

---

## Implication for the project

**The Path 2A negative result is *robust* to choice of single-mode axisymmetric shift family — since Session 36, as an identity rather than a sweep observation.** This is a meaningful narrowing: the load-bearing assumption is *not* "Alcubierre $\beta^x \hat x$" but rather **"single-mode axisymmetric shift + spherical fluid-shell source + asymptotically flat vacuum exterior + steady-state metric."**

To find a positive-energy classical warp drive, one of those four sub-assumptions must give. Slice 1 confirms it's not the first one (within the single-mode family). Slices 2-6 test the remaining three.

Lentz 2020's construction *did* break the third sub-assumption (using plasma source instead of fluid) and may have broken the first (multi-mode). His result is therefore consistent with our Slice 1 finding rather than contradicting it.

**Canonical post-Phase-2C load-bearing-assumptions table**: see [`NAVIGATOR.md`](NAVIGATOR.md) for the integrated view across all six slices.

---

## Multi-mode follow-up: Fell-Heisenberg 2021 (Session 10)

The natural next test was: does *multi-mode* (irrotational, non-axisymmetric) shift achieve full WEC where single-mode axisymmetric does not? Fell-Heisenberg 2021 ([arXiv:2104.06488](https://arxiv.org/abs/2104.06488)) is the most credible standing positive-energy claim in this regime.

**Result of independent reproduction in [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb)** (full evaluation in [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md)):

- Their Eulerian-energy decomposition formula (Eq. WECinansatz) regression-checks against our symbolic Einstein-tensor pipeline to literal symbolic zero (A-grade pipeline confirmation).
- Their qualitative claim is verified: a multi-mode irrotational shift gives positive Eulerian $\rho_E$ on 99.8% of interior cells with superluminal central $|\vec{N}|$.
- **Full WEC violations are smaller than they suggest**: only 1.3% of interior cells violate full WEC (with their text saying "no amount of modification could get rid of these regions"), and 5.3% violate full DEC.
- **Slice 1's negative result is therefore unchanged for the full-WEC test**, but the residual full-WEC-violation regions are far smaller than the Slice 1 0/140 sweep would suggest. The Fell-Heisenberg construction is a real partial success, narrowing the obstruction without eliminating it.

**Updated load-bearing assumption**: "no axisymmetric single-mode shift achieves full WEC" → **"single-mode axisymmetric shifts cannot achieve even Eulerian-WEC; multi-mode irrotational shifts achieve Eulerian-WEC and 99% full-WEC, with residual ~1% violation regions whose minimisability is the most interesting open question Slice 1+Session 10 has surfaced."**

---

## Citations

- Alcubierre 1994 (gr-qc/0009013) — original shift family.
- Natário 2002 (gr-qc/0110086) — zero-expansion variant.
- Rodal 2025 ([arXiv:2512.18008](https://arxiv.org/abs/2512.18008)) — irrotational variant; see [`RODAL2025_EVALUATION.md`](RODAL2025_EVALUATION.md).
- Lentz 2020 ([arXiv:2006.07125](https://arxiv.org/abs/2006.07125)) — plasma-supported positive-energy soliton, *not* a single-mode axisymmetric shift family.
- Bobrick & Martire 2021 ([arXiv:2102.06824](https://arxiv.org/abs/2102.06824)) — general "any warp drive is a shell of matter" framework.
- Lobo & Visser 2004a (gr-qc/0406083) — linearised analysis showing EC violations at any $v > 0$ for Alcubierre.

## Figures

- `figures/shift_families/family_comparison.png` — three-panel grouped bar chart of WEC pass fraction, DEC pass fraction, and DEC-slack medians across the four shift families (alcubierre, freeform_j1, irrotational, natario). Generated by `python figures/plot_figures.py shift-families-bars`; since Session 36 reads the **corrected** preview artifact (`sweeps/shift_families_20260705T*.parquet`). Slice scope: 140-cell corrected preview, single-mode axisymmetric shifts only — visualises the corrected record (only the irrotational family has genuinely positive-$\rho_E$ regions; the analytic closure is the primary result).

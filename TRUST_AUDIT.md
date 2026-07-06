# Trust Audit — What We Derived vs. What We Accepted

**Last updated:** 2026-05-16 (after Session 31; **Phase 3.3+ Step 2 (anisotropic) CLOSED NEGATIVE → Phase 3.3+ fully closed**. Free α–m metric-first optimization plateaued at 3.7% whose full-res min(EC)=−3.72e39 (DEC FAIL); adversarial KILL/KILL. Fuchs §6 "orders of magnitude" unsupported in BOTH isotropic & anisotropic slices; only real radial-certified finding = Fuchs-mass over-provisioning (uniform reduction dominates profile-shaping & anisotropy). 3rd-instance methodological refinement: optimizer mines whatever discretization is in its objective — incl. the under-sampled discrete minimization grid even with an exact-certified curvature engine. Composite Path 2A verdict A unchanged. Prior (Session 30) header below.
**Prior:** 2026-05-15 (after Session 29; Phase 3.3+ Step 1 closed NEGATIVE via the radial-frame redo; a new exact-symbolic EC evaluator is A-grade on smooth inputs but an unresolved ~10-OoM cross-representation conflict on sharp profiles is now an OPEN documented hurdle; composite Path 2A verdict A unchanged).
**Purpose:** Honest accounting of every external result the project relies on, with a verification cost estimate for each.

The project has three categories of result:

- **A — Independently verified by us.** Computed from first principles in our notebooks; no faith required beyond standard GR.
- **B — Accepted on the literature's authority but spot-checkable.** A specific paper says it; we did not re-derive it but could without prohibitive cost.
- **C — Heuristic / order-of-magnitude.** Used as a quantitative ceiling or scaling argument, not a precise prediction. Revisiting these would change numbers but probably not conclusions.

The five major results of the project are tagged below. Each external dependency is graded **A / B / C** with a verification-cost estimate. After the per-result tables I summarise the *load-bearing* dependencies (the ones that, if wrong, would actually invalidate the project).

---

## Result 1: Static Fuchs-class spherical shell satisfies DEC with $\Delta_{\min}/R = \kappa\,\beta/C$

**Source:** Packages 1–2, `israel_junction.ipynb` + `thickness_bound.ipynb`.

| Component | Status | Detail |
|---|---|---|
| Israel junction formalism (Israel 1966; Poisson 2004 *Toolkit* §3.7–3.8) | **A** | Used the formalism directly; we reproduced the standard weak-field shell mass $\mu \approx M + GM^2/(2R)$ as a regression check (`matter_shell.ipynb` §3.2). |
| Schwarzschild extrinsic curvature on a constant-$r$ surface (cell 4 of `israel_junction.ipynb`) | **B** | We cited "Poisson 2004 §3.8" for the formula $K^+_{tt} = -(GM/R^2)\sqrt{f}$, $K^+_{\theta\theta} = R\sqrt{f}$, etc., rather than rederiving on the spot. **Cost to verify:** ~30 min — write an 8-line SymPy snippet computing $K_{ab}$ from the unit normal $n^\mu = (0, \sqrt{f}, 0, 0)$ and the Schwarzschild metric. Worth doing as a separate validation cell. |
| Alcubierre-shift $K^-_{ij} = -\tfrac12(\partial_i\beta_j + \partial_j\beta_i)$ on a flat slice | **A** | Derived in `LINEARIZATION_CALCULATION.md` §3 from the standard ADM formula $K_{ij} = -\tfrac12 \mathcal{L}_n g_{ij}$ with $\alpha = 1$. Self-contained. |
| The $l = 0 + l = 1$ angular structure of $[K_{ab}]$ | **A** | Derived symbolically by Legendre-decomposing the jump (cell 6 of `israel_junction.ipynb`). |
| The Fuchs et al. 2024 *existence* of a DEC-satisfying static warp shell | **B** | **Critical input.** We used Fuchs's published parameters ($R = 15$ m, $M = 4.49\times10^{27}$ kg, $\beta = 0.02$, $\Delta = 10$ m) as a benchmark and structural analogy. We did not re-run their numerical relativity. **Cost to verify:** install Warp Factory (Helmerich et al. 2024, MATLAB), reproduce Fuchs Fig. 10. ~1 session, but Warp Factory installation on Windows is non-trivial. This is Phase 3 Task 3.1 in the roadmap. |
| The DEC failure at the anti-motion pole for thin walls | **A** | Derived numerically from our own surface stress-energy expression (cell 7 of `israel_junction.ipynb`). |
| The scaling law $\Delta_{\min}/R = \kappa\,\beta/C$ with $\kappa \in [0.05, 0.75]$ | **A** | Analytical leading-order ($\kappa = 3/4$) derived in `thickness_bound.ipynb` cells 3–5; empirical lower bound ($\kappa = 0.05$) measured from our own HF Jobs sweep. |

**Honest health check.** Only one critical item is **B**: the Fuchs existence result. If their numerics were wrong (which is unlikely — the paper has been peer-reviewed and the construction is conceptually clean), our scaling-law analysis still stands but loses its anchor in a known-existing solution. Our scaling law is independent of theirs and was derived from our own Israel-junction calculation, so the math survives even if the *example* doesn't.

---

## Result 2: No classical mechanism accelerates a Fuchs-class shell in vacuum to $\Delta v \sim v_{\rm warp}$

**Source:** Package 3, `acceleration.ipynb`.

| Component | Status | Detail |
|---|---|---|
| ADM 4-momentum is conserved at infinity for asymptotically flat spacetimes | **A** | Standard result, derived in `acceleration.ipynb` cell 3 from the ADM formula. We also computed the ADM mass of Schwarzschild symbolically as a regression check. |
| Initially-static shell ($K_{ij} = 0$) has $P^i_{\rm ADM} = 0$ | **A** | Direct from the ADM 4-momentum integrand. Self-contained. |
| Three-mechanism catalog (A spin-up, B mass ejection, C GW recoil) is exhaustive | **B** | We argued by elimination: any non-zero $\Delta P^i$ at infinity must come from non-vacuum exterior, expelled matter, or radiation. This is morally a theorem but we did not write a proof. **Cost to verify:** ~1 hour to write a careful proof using the ADM-mass + Bianchi-identity argument (Schuster, Santiago & Visser 2023 do something similar in their Theorem 3). Low risk of being wrong. |
| Mechanism A reduces to "push-from-a-wall" (requires $\sim M_{\rm shell}$ of comoving exterior mass) | **B** | Order-of-magnitude argument: the exterior matter must carry equal-and-opposite momentum, so for non-relativistic motion its rest mass must be $\sim M_{\rm shell}$. This is Newtonian momentum conservation; not subtle. |
| Mechanism B (Tsiolkovsky rocket) is "DEC-trivial and mass-budget-trivial at $\beta \sim 0.02$" | **A** | We computed the Tsiolkovsky mass ratio $e^{\beta} \approx 1.02$ and the DEC for a rocket exhaust is well-understood. |
| Mechanism C (GW recoil) is bounded by **$\Delta v \lesssim 0.25\%$ of $v_{\rm warp}$** for Fuchs-compatible parameters | **C** | **This is the most delicate quantitative claim in the project.** Two independent estimates: |
|  ↳ Approach A: SXS rescaling $v_{\rm kick}^{\rm Fuchs} = v_{\rm kick}^{\rm BBH} \cdot \beta^2 \cdot C^{3/2}$ | **C** | The $\beta^2$ scaling is justified (quadrupole power $\propto v^4$ → momentum $\propto v^4 \cdot t \propto v^2$ at fixed inspiral time). The $C^{3/2}$ scaling is a *heuristic*; the actual NR-fit relations of Lousto & Zlochower 2008 use mass-ratio + spin variables, not bare compactness. **Cost to verify properly:** install `sxs` Python package and pull a real waveform from an extreme-mass-ratio binary, then rescale to Fuchs parameters. Half a session; would tighten the ceiling but not change its order of magnitude. |
|  ↳ Approach B: PN binary analog (shell + 1% beacon at separation $a = 2R$) using Fitchett–Blanchet leading-order quadrupole formula | **B** | Standard post-Newtonian formula `dP/dt = (8 G^4 M1^2 M2^2 |M1-M2|) / (105 c^7 a^5)` is in any GW textbook (e.g. Maggiore *Gravitational Waves* Vol. 1, §3.3). We did not derive it. **Cost to verify:** ~1 hour against any standard reference. |
| Varma et al. 2022 record BBH kick of ~5000 km/s | **B** | Used as numerical input to Approach A. **Cost to verify:** read Varma 2022 Table 2 directly. ~10 min. |
| Schuster–Santiago–Visser 2023 Theorem 3 ("warp-bubble acceleration is bounded by boundary flux") | **B** | We claim our result "strictly strengthens" theirs by giving a quantitative ceiling. **Cost to verify the comparison:** ~30 min reading their Theorem 3 statement carefully and confirming our three-mechanism catalog is a refinement of their boundary-flux term. |

**Honest health check.** The qualitative conclusion (no classical mechanism for warp-relevant $\Delta v$) is **robust** — it's a composite of three independent obstructions, two of which are essentially trivial (Mechanism A is push-from-a-wall, Mechanism B is just a rocket). The **quantitative ceiling** ($\Delta v \lesssim 0.25\%$ of $v_{\rm warp}$) for Mechanism C is at the order-of-magnitude level, not better. Could be off by a factor of 2–10 either way without changing the conclusion. **The most defensible version of our result:** "GW recoil is parametrically suppressed by $(v/c)^2 (R_S/R)^{3/2}$ relative to BBH kicks; numerical examples give 100–10000 m/s, far below warp targets of $10^7$+ m/s." We should present it that way, not as a sharp 0.25% number.

---

## Result 3: Krasnikov tube classical wall has $\rho_p^{\min} \propto -\eta/\epsilon^2$, WEC fails for any $\eta > 0$

**Source:** Task 2A.13, `krasnikov_tube.ipynb`.

| Component | Status | Detail |
|---|---|---|
| Krasnikov 4D metric (Everett & Roman 1997 Eq. 13) | **B** | Used their published metric form. **Cost to verify:** ~5 min reading their §3 — the construction is geometrical and elementary. |
| Smooth step $\theta_\epsilon$ form (their Eq. 35) | **B** | A specific choice of profile; the qualitative results are profile-independent (cf. Cell 6 confirming $\epsilon$-independence to 14 decimals). **Cost to verify:** trivial; would be most useful to repeat with a different smoothing function (e.g. Alcubierre's tanh profile) to confirm the no-go is profile-independent. ~30 min. |
| Static-observer orthonormal tetrad (their Eqs. 24–27) | **B** | We used their tetrad. **Cost to verify:** ~10 min — `krasnikov_tube.ipynb` Cell 7 already includes a symbolic orthonormality check ($\eta_{\hat\mu\hat\nu} = $ Minkowski) that passed. So it *is* effectively verified. |
| Einstein tensor of the cylindrical metric, including $T_{tt}$ matching their Eq. 14 | **A** | **Computed from scratch in our framework.** Cell 5 of the notebook is a literal zero-difference symbolic identity check against Eq. 14. |
| Universal scaling law $\rho_p^{\min}(\eta, \epsilon) = -\kappa_K(\eta)/\epsilon^2$ with $\kappa_K \approx 0.122\,\eta$ | **A** | Derived empirically from our sweep, fit slope $1.001$. The functional form ($\eta/\epsilon^2$) is dimensionally forced; the coefficient $0.122$ is profile-dependent (specific to the chosen $\theta_\epsilon$). |
| WEC failure at every $\eta > 0$ in the parameter sweep | **A** | Direct numerical sweep result, 300/300 points fail. |
| The unobservability tradeoff (negative-energy density / observable lightcone-opening = const) | **A** | Both quantities scale linearly with $\eta$ in our framework; we observe this by inspection. |
| Network-implies-CTC theorem (Everett & Roman 1997 §4) | **B** | **Critical input.** We accept their global-causality result. **Cost to verify:** their §4 is a 2-page geometric argument; ~30 min to convince oneself. We have not written our own version. |

**Honest health check.** This is the cleanest result in the project. The bulk-stress-energy calculation is **A** (verified to symbolic identity); only minor ingredients are **B** (the metric form, the tetrad — both spot-checked or directly verifiable). The CTC theorem we cite from Everett-Roman is the only piece we have not independently rederived, and reading their §4 once would close that gap.

### Slice 4b extension (Task 2A.13b, Session 23, 2026-05-12)

**Source:** [`krasnikov_hybrid.ipynb`](krasnikov_hybrid.ipynb), [`KRASNIKOV_HYBRID_NOTES.md`](KRASNIKOV_HYBRID_NOTES.md).

| Component | Status | Detail |
|---|---|---|
| Pointwise DEC deficit profile $\Delta_{\rm DEC}(\rho)$ from the Result-3 wall | **A** | Computed via the same `_T_orthonormal` symbolic pipeline (regression-validated above) on a 1-D radial grid; integrated cylindrically to a per-length budget. |
| Per-length budget integral $\mathcal{I}(\eta,\epsilon,\rho_{\max}) = 2\pi \int \rho\,\Delta_{\rm DEC}\,d\rho$ | **A** | Composite trapezoid over 4001-point clamped grid; $\epsilon^2$-collapse Gate (ii) confirms $\mathcal{I}\cdot\epsilon^2$ depends only on $(\eta, n)$ as predicted by the Result-3 universal law. |
| Krasnikov 2003 §3.3 milligram budget $E_Q^- \sim 10^{-3}\,\mathrm{g}$ | **B** | Accepted from Krasnikov 2003 §3.3 (see [`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md)); the §3.3 argument itself is acknowledged as heuristic. |
| Geometrized-to-grams conversion $c^2/G \approx 1.347 \times 10^{30}\,\mathrm{g/m}$ | **A** | CODATA constants. |
| Gate (i): anchor inner-edge $\rho_p^{\min} = -0.067$ vs Everett-Roman saturation $-1/(8\pi\epsilon^2) \approx -0.0398$ at $\epsilon=1$ | **A** | Same factor-of-two regime as Everett-Roman §3 (their saturation bound is loose by $\mathcal{O}(1)$). |
| Gate (ii): universal $\epsilon^2$-collapse of $\mathcal{I}\cdot\epsilon^2$ at fixed $(\eta, n)$ | **A** | Confirmed across $\epsilon \in \{0.01, 0.1, 1\}$ to all retained decimal places. |
| Gate (iii): Everett-Roman $\alpha$-band recovery, $\alpha = 0.13 \in [0.01, 1]$ | **A** | Direct ratio of integral to $\eta D / \epsilon$. |
| Headline ratio $r_{\min} = 1.10 \times 10^{31}$ at $D=1\,\mathrm{m}$ across 360 sweep points | **A** | All gates pass; sweep schema sane; result is the deterministic product of A-grade ingredients above. |

**Slice scope.** $\eta \in [10^{-2}, 1)$, $\epsilon \in [10^{-2}, 1]\,\mathrm{m}$, $n=\rho_{\max}/\epsilon \in [2, 100]$, $D \ge 1\,\mathrm{m}$, static observer, Krasnikov-2003 §3.3 budget interpretation. Krasnikov 2003 §3.1 (Weyl/Ricci-ratio) and §3.2 (sub-Planckian-$E_{\rm tot}^-$) loopholes are *not* tested by Slice 4b.

**Honest health check.** Result inherits Result-3's grade-A backbone. The only B-grade input is the milligram budget itself (accepted from Krasnikov 2003); even loosening it by 10 OoM leaves a 21-OoM margin. Closure direction (NEGATIVE) would only flip if (a) someone shows the §3.3 mg estimate is wrong by $\ge 31$ OoM in the *favourable* direction, or (b) the §3.1/§3.2 loopholes admit a qualitatively different mechanism not captured here.

---

## Result 4: Rodal 2025 evaluation conclusions

**Source:** `RODAL2025_EVALUATION.md`.

This is **not** a project-derived result — it's a critical reading of an external paper. Trust assessment is different here: we are evaluating *their* claims, not making our own.

| Component | Status | Detail |
|---|---|---|
| Their construction: $\Phi(r,\theta,t) = v(t)\,r\,g(r)\,\cos\theta$ with the explicit $g(r)$ formula | **A** | We re-derived the construction symbolically in the evaluation document, including the linear ODE for $g(r)$ and its solution. |
| Their Type-I proof (Prop. 1, $G_{\hat 0 \hat i} = 0$ on flat slice with $\beta_i = -\partial_i \Phi$) | **A** | We followed the proof and confirmed the algebraic identity $D_{\hat k}(K^{\hat k}{}_{\hat i} - \delta^{\hat k}_{\hat i} K) = -[D_{\hat k}, D_{\hat i}] D^{\hat k}\Phi = 0$. |
| Their numerical comparison: 38× peak-deficit reduction vs. Alcubierre, 2,600× vs. Natário | **B** | We did not re-run their Mathematica pipeline; we accepted these numbers. **Cost to verify:** install Mathematica, request their code (or write our own Cartan-tetrad numerics — a few days of work). Lower priority than other items. |
| Their tail-extrapolated "net energy ≈ 0 to 0.04%" | **C** | We critically flagged this as a *proper-energy* statement, not a vanishing ADM mass; the paper itself acknowledges this. The two-point $1/R$ extrapolation is a model that the paper does not test against a third point. **Cost to verify:** would require running their pipeline at several integration radii $R \in \{6\rho, 8\rho, 10\rho, 12\rho, 16\rho\}$ and checking that the $1/R$ fit is robust. |
| Their NEC-still-violated finding | **A** | This is a logical deduction from their own Type-I eigenvalues; we re-derived it. |

**Honest health check.** Our evaluation is conservative — we explicitly downgraded Rodal's headline numbers and flagged the "net energy ≈ 0" claim as easily over-interpreted. If a future paper challenges Rodal 2025, our evaluation is unlikely to be embarrassed.

---

## Result 5: Composite "no classical positive-matter warp drive is simultaneously useful, accelerable, and DEC-compatible"

**Source:** Composite of Results 1–3 above + Bobrick-Martire 2021 + Everett-Roman 1997.

| Component | Status | Detail |
|---|---|---|
| Bobrick & Martire 2021 "any warp drive requires propulsion" | **B** | We accept this as a consequence of Bobrick-Martire's general framework. **Cost to verify:** ~1 session reading their §III–IV carefully. We have the full PDF in `papers/2102.06824v2.pdf`. |
| The composite logic itself (combining four results into a no-go) | **A** | Internal logic; nothing accepted externally. |

**Honest health check.** The composite statement is **as strong as its weakest component**. The components are: (1) Result 1 — depends on Fuchs existence (B); (2) Result 2 — depends on the GW-recoil ceiling (C); (3) Result 3 — almost fully A; (4) Bobrick-Martire — B. So the composite is at best **B-grade** strength; to make it A-grade we'd need to verify the Fuchs existence result, write a formal proof of the three-mechanism exhaustiveness, and re-derive Bobrick-Martire's propulsion theorem. None individually difficult; together about 3–4 sessions of work.

---

## Load-bearing dependencies (the "if these are wrong, the project is wrong" list)

Sorted by how much would actually break:

| Rank | Dependency | Grade | Risk if wrong | Cost to A-grade |
|---|---|---|---|---|
| 1 | **Israel junction formalism for matching warp interior to Schwarzschild exterior** | A | Project-ending; everything in Path 2A uses it | None — already A. |
| 2 | **Einstein tensor of the cylindrical Krasnikov metric (matches Everett-Roman Eq. 14 exactly)** | A | Task 2A.13 result invalid | None — already A, with literal symbolic regression check. |
| 3 | **Fuchs et al. 2024 has a real DEC-satisfying static warp shell** | **A** (was B) | Path 2A loses its anchor; our scaling law still holds in vacuum but we lose the existence example | **CLOSED 2026-04-21 (Session 18)**: Warp Factory installed on MATLAB R2023a Update 8; `metricGet_WarpShellComoving` + `evalMetric` reproduces Fuchs Fig. 10 at canonical $(R_1, R_2, M, \beta) = (10\,\text{m}, 20\,\text{m}, 4.49 \times 10^{27}\,\text{kg}, 0.02c)$ with in-shell pass-fractions NEC=WEC=DEC=SEC=1.0000. Concurrent κ-bracket cross-check (ROADMAP 2A.9b) finds $\kappa^{\rm num} \in (4.17, 5.83]$ vs analytic 2A.9a $\kappa \in [0.05, 0.875]$ — a 6× tightening attributable to distributed warp-gradient stress vs thin-shell pole jump. Existence anchor confirmed; analytic bound noted as optimistic. Full notes: [`WARP_FACTORY_NOTES.md`](WARP_FACTORY_NOTES.md). **Independent confirmation 2026-05-13 (Session 25)**: pure-Python NumPy port [`warp_factory_py/`](warp_factory_py/) (no MATLAB, no WarpFactory binary) reproduces the same Fig. 10 at the same parameters with rho diff $2.6\times 10^{-11}$ and EC reldiff(min) $\le 3\times 10^{-3}$ in `wf_compat=True` mode; in-shell NEC/WEC/DEC/SEC pass-fractions = 1.0000 also survive in `wf_compat=False` mode (with three identified WF source bugs corrected — `ricciT.m` typo, `getEulerianTransformationMatrix.m` sign flip, `getEnergyConditions.m` curved-coord re-lowering). Anchor is now A-grade against two independent pipelines. |
| 4 | **Schwarzschild extrinsic curvature formulas (Poisson 2004 §3.8)** | **A** (was B) | Israel-junction formalism still works but with wrong numbers | **CLOSED 2026-04-17 (Session 9)**: Cell 4b of `israel_junction.ipynb` is a SymPy first-principles derivation matching the cited formulas to literal `0`. |
| 5 | **GW-recoil ceiling: SXS rescaling $\beta^2 C^{3/2}$ heuristic** | C → B (Colab path) | Quantitative GW-recoil ceiling could shift by 10× either way; *qualitative* conclusion (negligible) survives | **PARTIALLY CLOSED 2026-04-17 (Session 9)**: Cell 17 of `time_dependent.ipynb` is a Colab-runnable `sxs` waveform-pull that replaces the heuristic. Locally falls back. To fully close, run Cell 17 on Colab. |
| 6 | **Three-mechanism catalog is exhaustive (no fourth acceleration mechanism)** | **A** (was B) | If a 4th mechanism exists, Result 2 has a hole | **CLOSED 2026-04-17 (Session 9)**: Appendix A of `MATTER_SHELL_PATH.md` is the formal proof using ADM + Bianchi. No fourth mechanism is possible under the stated assumptions. |
| 7 | **Bobrick & Martire 2021 propulsion theorem** | **A** (was B) | Our composite Result 5 weakens but doesn't break | **CLOSED 2026-04-17 (Session 9)**: §V.B of their paper read independently; "any warp drive requires propulsion" verified verbatim. Audit summary in `KRASNIKOV2003_EVALUATION.md` and `LITERATURE.md` Bobrick-Martire entry. |
| 8 | **Everett-Roman 1997 §4 (network-implies-CTC theorem)** | **A** (was B) | Half of the speculation-document-closure argument relies on this; the *other* half (our Task 2A.13 negative-energy result) is independently A | **CLOSED 2026-04-17 (Session 9)**: §4 re-read; the geometric argument (two non-overlapping oppositely-oriented tubes form a time machine) is convincing. Audit summary in `KRASNIKOV2003_EVALUATION.md` and `LITERATURE.md` Everett-Roman entry. |
| 9 | **Rodal 2025 numerical comparison (38×, 2,600× factors)** | B | Our Path 2B search-direction recommendation is partly motivated by these; if wrong, Path 2B target is just "anisotropic Casimir" without Rodal-specific motivation | Low priority; would require Mathematica or rebuilding their Cartan-tetrad pipeline. **STATUS: deferred.** |
| 10 | **Fell-Heisenberg strict-pass existence claim (Sessions 11-17)** | **A** (was B) | Headline finding of the Phase 2D landscape arc would not survive a sign error in the Python ADM pipeline | **CLOSED 2026-04-21 (Session 17, Phase E)**: Wolfram 14.3 + xAct 1.3.0 + xCoba 0.8.6 second pipeline cross-checks the Python `adm_stress_energy` 4th-order FD against `D[]` symbolic differentiation of `phi_FH_smooth`. 9-anchor sweep across $(V, \sigma, r) \in \{0.5, 1.5, 2.5\} \times \{5, 10, 20\} \times \{6, 9, 12\}$ on a 5×5×5 sub-grid (124 interior points / anchor) finds median rel-diff $2$–$4 \times 10^{-6}$, max rel-diff $3$–$4 \times 10^{-4}$ consistent with $O(h^4)$ FD truncation at $h \approx 0.19$ — full agreement on every smooth point. Single $\vec x = (0,0,0)$ outlier is the FH ansatz's own $\Pi=1/4$ non-smooth point, already flagged by Session 14 §9 as the continuum-zero passenger zone. Sessions 11-17 results (strict-pass classification, polynomial boundary, horizon test, vorticity, VIQ, B-M taxonomy, CTC sea, asymptotic-matching residual) inherit A-grade for smooth points. See [`XACT_PIPELINE_NOTES.md`](XACT_PIPELINE_NOTES.md) and [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) §16. Reopening criterion: any future high-resolution sweep (e.g. 2D.5f at $N_{\rm pts}=129$) that flips $\gtrsim 5\%$ of strict-pass classifications would warrant a 20-anchor stratified re-cross-check. |

---

## Concrete verification roadmap

If we want to upgrade the project from "B-grade composite" to "A-grade composite," the **highest-leverage interventions** are:

1. **Add a Schwarzschild extrinsic-curvature regression cell to `israel_junction.ipynb`.** ~30 min. Closes the most embarrassing **B** dependency (#4 above) for free. **CLOSED 2026-04-17 (Session 9, Slice 1 audit interleave)**: added Cell 4b to `israel_junction.ipynb`; SymPy first-principles derivation of $K^+_{ab}$ matches Cell 9's quoted Poisson §3.8 formulas to literal `0` for all three components.
2. **Add Warp Factory installation + Fuchs Fig. 10 reproduction as Phase 3.1.** ~1 session. Already on the roadmap. Closes **#3**. **STILL DEFERRED** as of Session 9 — Warp Factory is MATLAB on Windows, neither Colab nor HF Jobs help directly. Cleanly negative result of Slice 5 means NR validation is not blocking.
3. **Replace the SXS-heuristic rescaling with a real waveform pull.** ~1/2 session using the `sxs` Python package on extreme-mass-ratio waveforms. Closes **#5** and gives a defensible quantitative ceiling. **PARTIALLY CLOSED 2026-04-17 (Session 9, Slice 3 audit interleave)**: Cell 17 of `time_dependent.ipynb` implements the `sxs` waveform pull as a Colab-runnable upgrade; falls back to Package 3 heuristic locally. Locally executed: fallback. To finish the upgrade, open `time_dependent.ipynb` in Colab and re-run Cell 17.
4. **Write the three-mechanism exhaustiveness proof.** ~1 hour. Closes **#6**. **CLOSED 2026-04-17 (Session 9, Slice 2 audit interleave)**: added Appendix A "Three-Mechanism Exhaustiveness" to `MATTER_SHELL_PATH.md`. Proof uses ADM-flux + Bianchi argument; conclusion: change in $P^i_{\rm ADM}$ requires non-vacuum exterior (Mech A), expelled matter (Mech B), or outgoing GW radiation (Mech C). No "fourth mechanism" possible under the stated assumptions.
5. **Read and summarise Bobrick-Martire §III–IV and Everett-Roman §4.** ~1.5 sessions combined. Closes **#7** and **#8**, both at once. **CLOSED 2026-04-17 (Session 9, Slice 4 audit interleaves)**: Bobrick-Martire §V.B propulsion theorem verified verbatim; Everett-Roman §4 CTC theorem verified geometrically. Audit summaries in [`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md) §"TRUST_AUDIT #7" and §"TRUST_AUDIT #8" and the corresponding entries in [`LITERATURE.md`](LITERATURE.md).

**Status (2026-04-17, Session 9):** four of the five interventions are closed; #5 is half-closed (locally fallback, Colab-ready); only #2 (Warp Factory) remains fully deferred. The original "1 week of focused work" estimate was met within Session 9 by interleaving each audit upgrade into the corresponding Phase 2C slice that naturally touched the relevant code/literature.

If we're going to write up Path 2A as a paper or preprint, the only remaining gap is independent NR verification of Fuchs 2024 — which would close TRUST_AUDIT #3 and complete the audit programme.

---

## What would NOT change

Even if every single B/C dependency above turned out worse than expected:

- **Result 3 (Krasnikov no-go)** would survive intact; it's almost fully A-grade.
- **The qualitative composite "classical warp drives are highly constrained"** would survive; only the quantitative sharpness would be in question.
- **The Path 2A → Path 2B handoff** would still make sense; even if some quantitative claims weakened, the strategic direction (anisotropic Casimir as the natural QFT target) is supported by the Rodal-2025 *qualitative* observation that anisotropic transverse pressures are easier to source than isotropic negative density, which is independent of the specific 38×/2,600× factors.

---

## TL;DR

**Updated 2026-04-27 (Session 22 bookkeeping refresh; supersedes Session 9 wrap text below where they conflict).**

Post-Session-22 grade map of every load-bearing dependency:

- **The Krasnikov no-go (Result 3 / Task 2A.13) is rock-solid (A).**
- **Schwarzschild $K_{ab}$, three-mechanism exhaustiveness, Bobrick-Martire propulsion theorem, Everett-Roman CTC theorem** all upgraded to **A** during Session 9 audit interleaves.
- **GW-recoil ceiling (Result 2)** is *Colab-A-eligible* via the `sxs` waveform pull wired into [`time_dependent.ipynb`](time_dependent.ipynb) Cell 17; locally falls back to the C-grade heuristic. One Colab run upgrades it.
- **Path 2A static existence (Result 1) anchor on Fuchs et al. 2024** (TRUST_AUDIT #3) **closed Session 18 (2026-04-21) at A**: Warp Factory on MATLAB R2023a Update 8 reproduces Fuchs Fig. 10 in-shell at NEC=WEC=DEC=SEC=1.0000; concurrent 2A.9b $\kappa$-bracket cross-check refines analytic $\kappa \in [0.05, 0.875]$ to $\kappa^{\rm num} \in (4.17, 5.83]$ (6× tighter). [`WARP_FACTORY_NOTES.md`](WARP_FACTORY_NOTES.md).
- **Fell-Heisenberg strict-pass existence claim (Sessions 11-22)** (TRUST_AUDIT #10) **closed Session 17 Phase E at A**: Wolfram 14.3 + xAct 1.3.0 + xCoba 0.8.6 cross-check of the Python ADM pipeline at 9 anchors returns median rel-diff $2$–$4 \times 10^{-6}$, max rel-diff $\sim 3 \times 10^{-4}$ consistent with $O(h^4)$ FD truncation. [`XACT_PIPELINE_NOTES.md`](XACT_PIPELINE_NOTES.md), [`FELL_HEISENBERG_SWEEP_NOTES.md`](FELL_HEISENBERG_SWEEP_NOTES.md) §16. Session-22 direct $N_{\rm pts}=129$ re-sweep (Task 2D.5f) returned **6240/10080 strict-pass** (+5.8% above the §11.6 extrapolation, well within the 2D.16 reopening criterion of $\gtrsim 5\%$ classification flips), so the 9-anchor xAct cross-check is *not* superseded and no 20-anchor stratified re-cross-check is required.
- **The composite "no useful classical warp drive within the static + asymptotically-flat + classical-matter slice" claim (Result 5) is now A** — every B-grade dependency that fed into it (#3, #4, #6, #7, #8, #10) has been upgraded; only #5 (GW-recoil ceiling) remains C-with-Colab-A-path, and the qualitative GW-recoil conclusion (parametric suppression $(v/c)^2 (R_S/R)^{3/2}$) survives even at C.
- **None of the project's strategic conclusions depend on a single load-bearing C-grade dependency.** The qualitative landscape — static spherical Fuchs corner is the *only* positive Path 2A corner; cylindrical, slab, and toroidal corners admit no useful warp drive within the slice; multi-mode FH static corner solves the energy-condition bottleneck but loses the passenger zone, the asymptotic-decay envelope, the isotropic source, and 98.3% of strict-pass interiors to the CTC sea — is robustly A-grade.

**Session-9 wrap text (kept for historical context; superseded above where they conflict):**

- The Krasnikov no-go (Task 2A.13) is rock-solid (A).
- Schwarzschild $K_{ab}$, three-mechanism exhaustiveness, Bobrick-Martire propulsion theorem, Everett-Roman CTC theorem all upgraded to A during Session 9 audit interleaves.
- GW-recoil ceiling (Result 2) is now *Colab-A-eligible* — cell wired in `time_dependent.ipynb`, falls back to the C-grade heuristic locally; one Colab run upgrades it.
- Path 2A static existence (Result 1) still leans on Fuchs et al. 2024 (B); Warp Factory MATLAB install (TRUST_AUDIT #3) remains the only deferred item. *(Closed Session 18; see refreshed TL;DR above.)*
- The composite "no classical warp drive within the tested slice" claim (Result 5) is now A− (the Fuchs-existence dependency being the only B remaining). *(Composite is now A; see refreshed TL;DR above.)*
- None of the project's strategic conclusions depend on a single load-bearing C-grade dependency. The qualitative story is robust; only the GW-recoil quantitative ceiling has a residual C that downgrades to B with one Colab run.

The original "1 week of focused work" estimate to upgrade from "B-grade composite" to "A-grade composite" was fully realised within Session 9 by interleaving each audit upgrade into the natural Phase 2C slice. The two remaining post-Session-9 upgrades (#3 Warp Factory, #10 FH xAct cross-check) closed in Sessions 18 and 17 respectively without further reorganising the audit programme.


---

## Session 16 addendum � codimension-counting law (k=0,1,2)

**Result.** Three confirmed perturbative-DEC thickness bounds at k=2 (sphere), k=1 (cylinder), k=0 (slab patch). Linear-beta branch obeys Delta_min = (3/8)(beta/M) * Area / R_curv for k >= 1; quadratic branch Delta_min = (1/8) beta^2 Area / M takes over at k=0 where R_curv -> oo.

**Per-data-point grading:**

- **k=2 (sphere) datum** � grade A. Hermite-cubic Path-2A in [matter_shell.ipynb](matter_shell.ipynb) �9, derived in front of the user, slice-scope explicitly recorded.
- **k=1 (cylinder) datum** � grade A. [toroidal_fuchs.ipynb](toroidal_fuchs.ipynb) Task 2A.14, linearized Levi-Civita exterior + Israel junction, derived in front of the user.
- **k=0 (slab) datum** � grade A. [slab_patch.ipynb](slab_patch.ipynb), R -> oo limit of the cylindrical Israel-jump corrections + dimensional second-order shift-gradient stress, derived in front of the user.

**Codimension-counting *law* (the inductive generalization across the three points):** grade C. Heuristic / dimensional / structural pattern, not a theorem. Recorded in [speculation/CODIMENSION_SCALING.md](speculation/CODIMENSION_SCALING.md) with explicit reopening criteria. The connection to the Thorne 1972 hoop conjecture (via [Bronnikov-Santos-Wang 2019](LITERATURE.md) �IX.A) is structural, not derivational.

**Slice scope** (recorded in [speculation/CODIMENSION_SCALING.md](speculation/CODIMENSION_SCALING.md) �6): static thin matter shells, 3+1 GR, Israel-junction matching, small perturbative shift, classical DEC. The law is not asserted outside this slice.

**No load-bearing dependency change.** This work does NOT modify the existing Path 2A composite verdict � it explores the *mathematical structure* of the obstructions rather than adding new ones. The codimension-counting law is parallel to, not part of, the warp-drive no-go programme. Grade summary unchanged: composite Path 2A verdict remains A-.


---

## Session 26 addendum � nested concentric shells (Phase 3.3 item 4)

**Result.** Within the slice (axisymmetric, comoving, two constant-density concentric shells, fixed total mass $M_{tot} = 4.49\times 10^{27}$ kg, warp band fixed at outer wall $(R_1, R_2) = (10, 20)$ m, $v = 0.02c$, smoothFactor = 4000, $300\times 300\times 5$ grid at $dx = 0.2$ m), splitting ADM mass between an inner shell at $(5, 8)$ m and the outer Fuchs shell **strictly degrades the NEC margin** monotonically as the inner-shell fraction $f_{inner}$ grows: from min(NEC) = +1.24e+39 (single shell) to -1.36e+40 at $f_{inner} = 0.7$. Pass-fraction crosses 1 -> 0.999 between $f_{inner} = 0.10$ and 0.20. Full sweep table in [SESSION_LOG.md](SESSION_LOG.md) Session 26.

**Grade.** A within the slice (independent NumPy pipeline, two distinct sweeps cross-validate, derived in front of the user). Slice does not cover radial-profile optimization (which is what Fuchs §6 actually proposed), non-spherical shapes, time-dependent shifts, or multiple disjoint warp bands.

**No load-bearing dependency change.** This is a NEGATIVE result that *strengthens* the existing composite verdict by closing one obvious-looking loophole (mass nesting). The Path 2A composite remains A.

**WarpFactory issue #4 surfaced.** `TOVconstDensity.m` applies the Schwarzschild-interior closed form for a uniform solid sphere to a *shell* geometry. The closed-form's embedded $M(r) = M_{tot}(r/R)^3$ is wrong for a shell (true partial-shell $M(r)$ is much smaller in $[R_1, R_2]$). Effect on $\alpha$ is small ($\sim 2.4\times 10^{-5}$ rel) because the TOV source is dominated by $M(r)$ + a tiny $P/c^4$ correction; effect on shell-interior $P$ is $\sim 22\%$. Recorded in `/memories/repo/warp_factory_anchor.md` issue #4. Does **not** change Fuchs Fig.10 EC verdict (single-shell pass-fractions remain 1.0 in both `wf_compat=True` and `wf_compat=False` modes), so TRUST_AUDIT #3 grade unchanged.


---

## Session 27 addendum � non-spherical / oblate axisymmetric shells (Phase 3.3 item 5; Phase 3.3 fully closed)

**Result.** Within the slice (axisymmetric, comoving, single-shell with volume-preserving Legendre-2 deformation $r_{\rm eff}(r,\chi) = r/s(\chi)$ where $s(\chi) = (1 + \epsilon P_2(\cos\chi))^{1/3}$, fixed $M_{tot} = 4.49\times 10^{27}$ kg, fixed shell radii $(R_1, R_2) = (10, 20)$ m, warp band = $(R_1, R_2)$, $v = 0.02c$, smoothFactor = 4000, $300\times 300\times 5$ grid at $dx = 0.2$ m), the spherical reference ($\epsilon=0$) is a **local optimum (or very near one) of min(NEC) under shape deformation**:

- **Axis aligned with warp motion direction** (deformation symmetry axis = x): every nonzero $\epsilon \in \{\pm 0.1, \pm 0.2, \pm 0.3\}$ strictly degrades the NEC margin; the most generous nonzero point ($\epsilon = +0.1$, prolate along motion) still loses 42 % of the spherical NEC reference; oblate $\epsilon = -0.1$ already tips the margin negative (-101 %).
- **Axis perpendicular to warp motion** (deformation symmetry axis = z): asymmetric. Oblate $\epsilon = -0.1$ produces a **+3.09 %** NEC-margin improvement (the only non-degrading direction tested); $\epsilon = -0.2$ is essentially flat ($+0.01\%$); $\epsilon = -0.3$ degrades ($-2.79 \%$); all positive $\epsilon$ degrade monotonically.

Combined with Session 26's nested-shell NEGATIVE, both obvious geometric relaxations of Fuchs §6's "1-D radial-profile optimization" sketch are now closed. **No order-of-magnitude mass-reduction loophole exists in either slice.** Full sweep table in [SESSION_LOG.md](SESSION_LOG.md) Session 27.

**Grade.** A within the slice. Independent NumPy pipeline, two-axis sweep, three smoke-test gates pass (epsilon=0 byte-equality with spherical builder; M[-1] is epsilon-independent to machine precision; volume preservation to $\sim 2\times 10^{-7}$). Slice does *not* cover non-axisymmetric / multi-axis (e.g. ellipsoidal three-semi-axis) deformations, self-consistent oblate shells via a 2-D Einstein-equation solve, intra-shell radial-profile optimization (Fuchs §6's actual proposal, separate Phase 3.3+ task), or substantially different canonical $(M_{tot}, R_1, R_2, v)$.

**No load-bearing dependency change.** Like Session 26, this is a NEGATIVE result that *strengthens* the existing composite verdict by closing a second obvious-looking loophole (geometric shape variation at fixed mass). The Path 2A composite remains A. The Fuchs Fig.10 anchor (TRUST_AUDIT #3) is unaffected; the spherical builder smoke-test reproduces it exactly via `epsilon=0`.

**Phase 3.3 closeout (composite, Sessions 24-27).** Sub-items 1-3 (Fuchs Fig.10 reproduction): A; sub-item 4 (nested shells): A within slice (NEGATIVE); sub-item 5 (Legendre-2 shape deformation): A within slice (NEGATIVE); sub-item 6 (final bookkeeping): closed by Session 27 doc updates. Composite Phase 3.3 verdict: A within slice (NEGATIVE on the geometric-relaxation question; UNTESTED on the radial-profile-optimization question per Fuchs §6, recorded as Phase 3.3+ in [`NAVIGATOR.md`](NAVIGATOR.md) Open Lead #2).


---

## Session 28 addendum — Phase 3.3+ Step 1 (Fuchs §6 radial-profile optimization): Cartesian-objective result KILLED

**Claimed result (REJECTED).** A Powell optimizer over 6 $\rho$-knots + 6 $\beta$-knots (warp performance held fixed: $\beta\equiv1$ for $r\le R_1$, $v=0.02c$; P TOV-pinned; new builder [`metric_profile_warp_shell`](warp_factory_py/metrics/warp_shell.py)) reported a **30.7% mass reduction** (4.49→3.11e27 kg) with all four ECs passing strictly at one canonical grid (dx=0.2, N=300), baseline reproducing Session 26's min(NEC)=+1.240e39.

**Adversarial verification ([`agent-tools/test_profile_kill.py`](agent-tools/test_profile_kill.py)).**

| Kill test | Verdict | Evidence |
|---|---|---|
| 1 — const-density over-provisioning control | SURVIVES | const-density passes only to M=3.50e27, fails at 3.11e27 — the effect was not the trivial "use less mass". |
| 2 — resolution convergence dx∈[0.12,0.40], independent grid family | **KILL** | optimized min(EC) ≈ −2.7e38 at *every* resolution; const-density baseline robustly positive and *rising* with refinement (+3.3e38→+7.5e38). |
| 3 — EC sphere-sampling escalation 100/10→400/30 | **KILL** | optimized stably negative (−2.68→−2.75e38). |

**Grade.** The 30.7% mass-reduction claim is **rejected (C / artifact)**. Mechanism: a spherically-symmetric shell evaluated by 4th-order Cartesian FD has a staircased radial structure; the optimizer, run with the *Cartesian* EC pipeline as its objective, reshaped $\rho$ so the worst staircased wall-cell went positive only on its own loop lattice and the single canonical grid first checked (a measure-near-zero set). The constant-density Fuchs baseline has no such exploit and passes grid-robustly — the clean control proving the failure is profile-specific, not pipeline-wide.

The **methodological finding is A-grade**: the Cartesian WarpFactory-port pipeline must not be used as an optimizer objective for a symmetric source. A real positive must be invariant under refinement *and* across representations. The correct Step 1 evaluates the ECs in the radial / 1-D representation as the objective, with Cartesian `eval_metric` only as an independent high-resolution end cross-check (durable feedback memory `feedback-no-cartesian-optimizer-objective`). Recorded as Open Lead #2 (radial-frame redo) in [`NAVIGATOR.md`](NAVIGATOR.md).

**No load-bearing dependency change.** Nothing in the composite Path 2A verdict relied on this; it was an exploratory probe of a still-open lead. Notably, **this is the verification discipline working as designed** — the same resolution-convergence + sampling-escalation tooling that tempered the Fell-Heisenberg arc (Sessions 14/22) caught a seductive false positive *before* it entered the trust ledger as a finding. The `metric_profile_warp_shell` builder is retained (sound; independently re-confirms WarpFactory issue #4 from a third code path).

**Separate unverified lead (flagged, NOT claimed).** Kill Test 1 incidentally showed constant-density passing at M=3.50e27 (≈22% below Fuchs's canonical 4.49e27) — but at dx=0.2 only. Distinct question (Fuchs-mass over-provisioning) from profile optimization; requires its own convergence study before any grade.


---

## Session 29 addendum — Phase 3.3+ Step 1 radial-frame redo: NEGATIVE + an OPEN cross-representation hurdle

**New evaluator graded.** [`warp_factory_py/solvers/axisymmetric_ec.py`](warp_factory_py/solvers/axisymmetric_ec.py): exact-symbolic Einstein/stress-energy for the axisymmetric warp-shell metric. **Grade A as a correct GR stress-energy calculator on smooth inputs** — Schwarzschild is exactly Ricci-flat to **1.7×10⁻¹⁵** (analytic-derivative probe), flat → 0, Alcubierre energy density negative with exact v² and (F')² scaling. Reuses the already-A-graded `frame`+`energy_conditions` so EC definitions are byte-identical to the Cartesian path. Three correctness-preserving bug fixes during validation (unsimplified-G cancellation → `sp.cancel`; `np.gradient` → quintic-spline derivatives; `cse=True` 17× speedup). **Trust boundary now explicitly mapped: validated only on smooth profiles.**

**Step-1 profile-optimization claim: REJECTED (NEGATIVE).** The radial-objective optimum (M=3.505e27, −21.9%, radial min(EC)=+8.55e36 PASS) was killed two independent ways (Task 21):
- *Kill Test A* (cross-representation + refinement): Cartesian `eval_metric` gives the same metric min(EC) ≈ −6.3×10³⁹ at every dx∈[0.12,0.40] (stable); constant-density baseline robustly positive throughout. Not representation-invariant.
- *Kill Test B* (decisive, internal to the trusted radial evaluator): plain constant-density passes — in the radial evaluator's own *converged* judgment — down to ≤2.70×10²⁷, below the "optimized" 3.505×10²⁷ and with a healthier margin. The profile shaping is worse than trivial uniform mass reduction. No §6 profile benefit; "orders of magnitude" not in evidence.

| Component | Status | Detail |
|---|---|---|
| `axisymmetric_ec` on smooth metrics | **A** | Schwarzschild Ricci-flat to 1.7e-15; Alcubierre scaling exact; agrees with Cartesian on baseline (sign+feasibility). |
| Step-1 radial-frame mass-reduction claim | **C / rejected** | Killed by Test A (non-invariant) + Test B (beaten by uniform reduction within the trusted evaluator). |
| Fuchs-mass over-provisioning sub-finding | **B (weak, cross-representation)** | Constant-density passes far below the canonical 4.49e27 in *both* representations (≈3.5e27 Cartesian, ≤2.7e27 radial). Real but trivial uniform reduction, not §6, not OoM. |
| Sharp-profile EC evaluation | **OPEN HURDLE — ungraded** | The two validated pipelines agree on smooth metrics, diverge ~10 OoM with opposite sign on the sharp optimized profile (radial converged +2.67e38 PASS; Cartesian stable −6.3e39 FAIL). Predicted under-resolution mechanism (H2) was *refuted* — radial converges stably positive. Until resolved, **no sharp-profile EC claim is verifiable.** |

**No load-bearing dependency change.** The composite Path 2A verdict (A) is untouched — Step 1 was an exploratory lead. **But a new explicit limitation is now on the books:** the project has no trustworthy energy-condition evaluator for sharp / optimizer-driven profiles, and this *blocks* Phase 3.3+ Step 2 (anisotropic) until adjudicated. Resolution requires an independent third pipeline on the sharp optimum (the Session-17 xAct/xCoba Mathematica route is the natural arbiter) or an analytic sharp test case with a known closed-form stress-energy. Recorded as NAVIGATOR Open Lead #2 (top priority).

**Honest meta-finding (A-grade, generalises Sessions 28+29).** An optimizer pointed at *any* numerical EC objective mines that objective's specific numerical slack wherever it has any (Cartesian staircasing S28; on sharp profiles the two pipelines simply disagree S29). Validation gates are necessarily smooth; the optimizer hunts where the evaluator is *not* certified. Cross-representation invariance under refinement is the only reliable arbiter — and on sharp profiles it currently, honestly, returns "unresolved." This is a documented hurdle, not a failure: it sharpens exactly what must be true for any future positive sharp-profile result to be credible. *(Refined Session 30 — see below: cross-rep invariance is necessary but insufficient when one representation is itself untrustworthy in-regime; the reliable arbiter is a certified-exact ground truth.)*

---

## Session 30 addendum — Prong B adjudicates the hurdle; trust grades resolved

**Instrument.** A standalone closed-form Einstein tensor (independent of `axisymmetric_ec`), built once with abstract A,B,F + derivatives, fed **exact analytic** closed-form derivatives per sharpness. **Certified through the actual code path**: flat → `0.00e+00`, Schwarzschild → `5.55e-17` (machine-zero, Ricci-flat) — a stronger guarantee than fast-vs-slow self-consistency (matches GR exactly on a non-trivial curved vacuum). Harness retained: [`verification/test_prongB_groundtruth.py`](verification/test_prongB_groundtruth.py).

**Adjudication (sharpness sweep, GT vs Cartesian-FD vs radial-spline, identical shared EC contraction):**

| s | Cart vs certified GT | Radial vs certified GT |
|---:|---:|---:|
| 0.5–2 | 24.5% | **0.0%** |
| 4 | 12.0% | **0.0%** |
| 8 | 46.3% | **0.0%** |
| 16 | 80.7% | **0.0%** |
| 32 | 94.0% | **0.0%** |

Two independent symbolic G derivations + exact-analytic vs quintic-spline derivatives agree to displayed precision — a strong non-circular cross-validation, consistent with the Prong A localization (Cartesian FD on a staircased sharp feature).

**Grade changes:**

| Component | Old | **New (Session 30)** | Basis |
|---|---|---|---|
| `axisymmetric_ec` (radial) on **sharp** profiles | OPEN/ungraded | **A** | 0.0% vs GR-certified exact GT through s=32. Now the trusted absolute-magnitude EC oracle for shell profiles. |
| Cartesian `eval_metric` on **sharp** profiles | (implicitly trusted) | **C — unreliable; demoted** | 24% error even at low sharpness in this family, →94% at s=32, monotone, always under-estimating. Qualitative/smooth cross-check only. |
| "Sharp-profile EC evaluation" hurdle | OPEN HURDLE | **RESOLVED** | radial trustworthy, Cartesian not. ROADMAP 3.9 closed; Step-2 un-blocked. |
| Step-1 radial-frame mass-reduction claim | C / rejected (Kill A+B) | **C / rejected — Kill A retracted, Kill B strengthened** | Kill A used the now-untrustworthy Cartesian pipeline → retracted. Kill B is representation-internal to the now-certified radial oracle → stands; the optimized profile is *counterproductive* vs uniform mass reduction. NEGATIVE unchanged; justification rests on no open question. |
| Fuchs-mass over-provisioning sub-finding | B (weak, cross-rep) | **B → radial-certified** | Constant-density passes ≤2.70e27 ≪ 4.49e27 per the certified radial oracle. Real, but trivial *uniform* reduction — NOT Fuchs §6 profile optimization (the optimized profile is worse than uniform; §6 "orders of magnitude" remains unsupported). |

**Does NOT overturn Sessions 26–27.** The nested-shell and Legendre-2-shape NEGATIVEs were *relative/qualitative* NEC-degradation results, cross-checked, on the **smooth** Fuchs baseline where the pipelines agreed on sign. Cartesian's demotion is a magnitude-trust tightening for **sharp** profiles, not a retraction of those qualitative conclusions.

**No load-bearing dependency change.** Composite Path 2A verdict remains **A**. The change is that a previously-OPEN limitation is now CLOSED and a trusted sharp-profile oracle exists — strengthening, not weakening, the audit.

**Methodological refinement (supersedes the Sessions-28/29 meta-finding where they conflict).** Cross-representation invariance is *necessary but insufficient*: when one representation is itself untrustworthy in the regime under test, "they disagree" does not identify which is wrong. The reliable arbiter is comparison against a **certified-exact ground truth** (closed-form, exact derivatives, validated by exact-zero on known vacuum solutions). Build the ground truth; let it adjudicate. This is `feedback-exhaustive-survey-is-the-method` producing a clean answer instead of a standoff.

---

## Session 31 addendum — Phase 3.3+ Step 2 (anisotropic) NEGATIVE; Phase 3.3+ fully closed

**Setup.** Metric-first / Bobrick–Martire formulation: anisotropy automatic via independently-free, decoupled $\alpha(r)$ and $m(r)$ (no anisotropic-TOV solver). Correctness gate PASSED — the Fuchs isotropic baseline is representable in the free-(α,m,β) family and reproduces the Step-1 isotropic in-shell min(EC) to 5.7%, sign-consistent (one global C2 spline; the initial piecewise-C0 splice's −5.9e42 kink was fixed). Optimization scored against the **Prong-B-certified radial evaluator only** (Cartesian Prong-B-demoted).

**Result graded:**

| Component | Grade | Detail |
|---|---|---|
| Step-2 anisotropic mass-reduction claim | **C / rejected (KILL/KILL)** | Optimizer plateaued at M_opt/M_ref = 0.9632 (3.7%); full-res min(EC) = −3.72e39 (DEC FAIL). *Test A:* DEC violation converges genuine under refinement (522 r coarse "+2.9e35 PASS" → 2088 r −3.43e39 → 4175 r×120θ×na160 −3.72e39 stable) — coarse-loop pass = discrete-minimization-grid under-sampling mirage. *Test B (decisive, representation-internal):* constant-density passes (certified radial) to ADM ≈ 2.79e27 while the anisotropic optimum FAILS DEC at 4.46e27 — anisotropy counterproductive. |
| Fuchs §6 "orders of magnitude" claim | **rejected, both slices** | Unsupported in isotropic (Step 1) AND anisotropic (Step 2). |
| Fuchs-mass over-provisioning sub-finding | **B → radial-certified, strengthened** | Constant-density passes to ADM ≈ 2.79e27 (≪ canonical 4.49e27) on the certified evaluator — but trivial *uniform* mass reduction, which DOMINATES both profile-shaping (Step 1) and anisotropy (Step 2). NOT §6 profile optimization. |
| `verification/aniso_step2*` harnesses | **A (kept)** | Shared parameterization, gate, optimizer, adversarial battery — tracked, reusable. |

**Slice scope (honest).** NEGATIVE for this parameterization family (global-C2-spline free α,m,β), this optimizer (Powell, 28-dim, 700 evals, plateaued), this canonical config (R₁,R₂,v)=(10,20,0.02c). Not a proof no anisotropic shell can do better — but the decisive kill (Test B) is representation-internal to the certified oracle; across the whole Phase-3.3+ arc nothing approached beating constant-density-at-2.79e27.

**No load-bearing dependency change.** Composite Path 2A verdict remains **A** — strengthened (another exploratory loophole closed NEGATIVE; the verification discipline caught a coarse-mesh mirage before it was recorded).

**Methodological refinement (A-grade, 3rd distinct instance — supersedes prior where they conflict).** An optimizer mines *whatever discretization is in its objective*: Cartesian staircasing (S28); Cartesian-untrustworthy-for-sharp (S29); **and even with an exact-certified curvature engine, the under-sampled discrete (r,θ,direction) *minimization grid* (S31).** The reliable arbiter is jointly: cross-representation invariance + a certified-exact ground truth + a converged objective sampling mesh — with the optimum-plus-adversarial-battery as the catch (it caught all three). Recorded in `feedback-no-cartesian-optimizer-objective`.


---

## Session 32 addendum — Task 3.10 certified minimal-mass map (positive quantitative closure)

**Setup.** Constant-density Fuchs shells, minimal EC-passing mass bisected per (R1, R2, v) cell against the Prong-B-certified radial evaluator (`axisymmetric_ec`) at the Session-31 full-res accept/reject tier; coarse scout tier proposes brackets only (S28–S31 converged-objective rule). Grid mirrors 3.2's axes (18 cells). Gate battery: S31 anchor regression (ADM to 0.01%), canonical-threshold consistency (floor must sit at/below the mass already shown to pass), FULL↔CONF mesh-escalation stability at the threshold — ALL PASS, plus stability spot-checks at the two extreme-κ cells and the narrow-window cell.

**Results graded:**

| Component | Grade | Detail |
|---|---|---|
| Canonical floor M_min = 2.568e27 nominal / 2.650e27 ADM (over-provisioning 1.75× / 1.69×) | **A (within slice)** | Bisected on the certified oracle, rel_tol 0.5%; classification stable under mesh escalation both sides; reconciles S29/31 numbers (nominal 2.7e27 ↔ builder-ADM 2.786e27 — same probed point, two bookkeepings; both were upper bounds, not the floor). |
| Certified-radial κ surface: 4.64 ± 0.57 over 14 thresholds (range [3.61, 5.40], rising with R2) | **A (within slice)** | Canonical κ = 4.77 inside the 2A.9b Cartesian-era bracket (4.17, 5.83]; consistent with & refining 3.2's 18% spread. Protocol note: 2A.9b bisected Δ at fixed M (MATLAB WF, Cartesian era); 3.10 bisects M at fixed Δ on the certified evaluator. Thin-cell (Δ=3.75 m) κ inherits the ~5 m canonical smoothing length — convention, flagged. |
| Linear-in-β scaling of M_min (1–4% across map) | **A (within slice)** | Direct ratio check at fixed geometry; matches the 2A.5/2A.7 scaling-law form. |
| Binding condition at the floor: null (NEC) 13/14; strong (SEC) at the near-cap narrow-window cell | **A (within slice)** | From min_by_cond at the bisected threshold, full-res tier. |
| 4 null-configuration cells at v = 0.05c (no EC-passing constant-density mass) | **A (within slice, one stated structural assumption)** | Golden-section peak of min(EC) over the horizon-valid mass range robustly negative (−1.6e39 … −1.0e40) per cell. Verdict inherits the **unimodality assumption** (min-EC vs M = rising NEC-support margin ∧ falling high-compactness margin); assumption recorded in module + ledger reopening trigger (ii). Certified-radial confirmation of 3.2's "null configuration" phenomenon. |
| `hf_jobs/sweeps/mmin_map.py` + `verification/test_mmin_map_gate.py` + `sweeps/mmin_map_full_concat.parquet` | **A (kept)** | Sweep module, 3-gate battery, negation-tracked 18-row artifact. |

**Slice scope (honest).** Constant-density ρ(r) on [R1, R2]; TOV-pinned isotropic pressure; ℓ=1 dipole Alcubierre shift (canonical compact sigmoid); smooth_factor 4000 at fixed canonical radial sample spacing (physical smoothing length matched to Sessions 25–31 across cells); EC minima over the in-shell mask; radial representation only (Cartesian demoted per 3.9). Says nothing about non-constant profiles (Phase 3.3+ closed those NEGATIVE separately) or other shift/topology families.

**No load-bearing dependency change.** Composite Path 2A verdict remains **A**. The map quantifies the static-slice Fuchs family (over-provisioning = 1.75×, NOT orders of magnitude — Fuchs §6 stays unsupported in all three tested senses: profile, anisotropy, and now uniform-mass headroom).

**Methodological refinement (A-grade — the DUAL of the S28–S31 lesson).** Sessions 28–31 established that optimizers manufacture false POSITIVES by mining whatever discretization is in their objective. Session 32 adds: **search/bracketing logic manufactures false NEGATIVES through structural blind spots**, and "no result here" records need the same adversarial treatment as positive claims. Two in-session instances, both caught by kill-style spot-checks before recording: (1) a narrow passing window fell between scout-ladder rungs squeezed against the horizon wall — the cell was mis-recorded as horizon-capped while M = 7.41e27 passes cleanly; (2) the first fix still missed it because min-EC vs M is **unimodal, not monotone** — the window sits between two EC-FAIL rungs (fails low on NEC support, high on compactness). Correct pattern: search for the *peak* of the feasibility margin (golden-section maximize), and record the located peak value/location as the explicit basis of any no-pass verdict. Recorded in `feedback-exhaustive-survey-is-the-method` (refinement: the battery applies to negatives too).

---

## Session 33 addendum — Task 2D.11 Phase 3 (FH-form multi-mode A) NEGATIVE; Task 2D.11 fully closed

**Setup.** Per-component FH-form vector potentials (gradient-normalised, independent radii; asymmetry/exponent inherited from the FH anchor), curl added to the irrotational shift, evaluated through the same `adm_stress_energy_from_N` pipeline as Phases 1-2 (bit-exact baseline regression at the canonical anchor). Two previews: perturbative (N_vort <= 0.5) and non-perturbative (N_vort 1.5-5.0), 2914 rows, 0 errors.

**Results graded:**

| Component | Grade | Detail |
|---|---|---|
| Phase-3 negative (no improvement on any gate criterion; 100% strict degradation of both slacks; passenger zone unchanged) | **A (within slice)** | 2912 augmented points; monotone collapse in total amplitude; 1184 strong-amplitude rows develop NEW WEC violations. Pipeline cross-checked by bit-exact baseline regression + Phase-1/2 comparability (identical record schema, same anchor). |
| Task 2D.11 composite verdict (three vortical families all NEGATIVE; irrotational restriction not the driver of the all-wall-no-interior pathology) | **A (within slice)** | The three families are structurally independent (rotating-frame axisymmetric; fixed-direction Cartesian; FH-form multi-mode). Phase 3 has maximal structural overlap with the violating regions — the Phase-1/2 "unhelpful overlap" caveat is closed, not dodged. Slice: canonical anchor, static smooth-N, tested envelope/radius/amplitude ranges. |
| Spin-2 no-cavity bridge (Task 1.11) | **C (unchanged)** | Reinforced, not proven: consistent with, but not derived from, the Costa-Natario catalog. The 2B.8 assessment is the right instrument to test it. |
| `fell_heisenberg_vortical_multimode.py` + two preview configs | **A (kept)** | Tracked, reusable; parquets reproducible in ~2 min each. |

**No load-bearing dependency change.** Assumptions-table row 1's vorticity clause tightens from "does not lift it (Session 15)" to "does not lift it (Sessions 15, 33 — three families incl. FH-form multi-mode A)". Composite Phase-2D reading unchanged: every structural test degrades the warp-drive interpretation; none restores it.

**Methodological note.** The gate-driven preview discipline (decision gate stated in the config `_comment` before the run; definitive-at-anchor negative closes without dispatching the full sweep) held for the third consecutive vortical family — total Phase-3 compute cost ~4.5 min local, $0 remote.

---

## Session 34 addendum — Task 2B.8: Path 2B closed as a physical mechanism

**Setup.** Literature assessment (web-verified primary sources + one review) + a tracked even-if arithmetic harness ([`verification/test_2b8_casimir_gap.py`](verification/test_2b8_casimir_gap.py)). Canonical record: `QUANTUM_CLASSICAL_BRIDGE.md` §8.

**Results graded:**

| Component | Grade | Detail |
|---|---|---|
| Ordinary matter cannot reflect/absorb GWs (impedance $Z_G \sim 2.8\times10^{-18}$ SI mismatch; Dyson $\sim 10^{-41}$ cm²/g absorption; single-graviton detectors collapse to BHs) | **B** | Literature, uncontested across camps (the impedance statement appears in the pro-mirror school's own papers). Spot-checkable numbers; not re-derived here. |
| Superconductor H-C loophole: speculative, contested, unobserved | **B** | One programme + adopters; Quach 2015 explicitly conditional on H-C (erratum = units fix); 2022 review catalogs 55 years of contradictory results, no experimental support; originating programme's own 2022 refinement undercuts the mechanism. Not a refutation-theorem — a status assessment. |
| Even-if magnitude bound: perfect mirror + favourable sign ⇒ $|\rho_C| \le \hbar c/d^4$ ⇒ **63.5–69.6 OoM short** of every radial-certified target; required spacing sub-proton ($\sim 10^{-16}$ m) through a metre-scale wall | **A (within slice)** | Arithmetic derived in the tracked harness against the project's own certified numbers (S29–S32). Slice: 4D semiclassical GR, standard Casimir envelope ($K = 1$, ~73× generous vs $\pi^2/720$), macroscopic $d$. Independent of rows 1–2: holds even if a perfect gravitational conductor existed. |
| Composite verdict: Path 2B CLOSED as physical mechanism (static sliver + acceleration supplement) | **A (within slice)** | Decisive leg is the magnitude bound; legs 1–2 close the mirror question itself. Mode-decomposition math (2B.1–2B.6) survives as classification tool; Claim (a) and the §5 effective-boundary (Path 2A) reading untouched. |
| Task-1.11 spin-2 no-cavity bridge | **C (unchanged)** | Consistent with 2B.8 (no cavity-forming boundary for gravitons in known physics) but still not derived from a formal catalog. |

**Slice scope (honest).** The closure is within 4D semiclassical gravity ($G_{\mu\nu} = 8\pi G \langle T_{\mu\nu}\rangle$) with standard QFT Casimir scaling at macroscopic boundary scales. It does NOT exclude: modified gravity (Phase 2E.2 / Slice 6b), exotic field content or trans-QI vacuum states (Phase 2E.3), or horizon-based constructions incompatible with subluminal shells (none known). Those remain where they were — deliberately deferred with reopening criteria.

**No load-bearing dependency change to Path 2A.** Composite Path 2A verdict remains **A**; 2B.8 strengthens the overall landscape statement: within 4D semiclassical GR there is now no known candidate for a vacuum+DEC+dynamical warp realisation.

**Methodological note.** The decisive step deliberately repeated the Slice-4b pattern (grant the contested physics, bound the magnitude): the assessment does not need to win the contested superconductor argument — the loophole-independent bound closes the path at ~2× the 31-OoM Slice-4b standard, so the verdict is robust to any resolution of the mirror literature.

---

## Session 35 addendum — pre-Phase-2E deep audit + remediation: grade corrections and disclosures

**Setup.** Four-thread audit of the whole closure record (closure-basis classification; retroactive evidence review vs the Session-30/32 lessons; harness code review + battery re-runs; cross-doc numeric/logic tracing), then same-session remediation. Full chronology in SESSION_LOG Session 35. Nothing below flips a recorded verdict; the corrections are magnitude/provenance/wording-level.

**Disclosures and grade impacts:**

| Item | Impact | Detail |
|---|---|---|
| R1 mask bug (one-cell in-shell-mask misalignment, all Cartesian-path harnesses) | **Corrects Session-30 Prong-B recorded numbers; verdict unchanged** | Corrected sweep: Cartesian-vs-GT **9.1% → 94.0%** over s=0.5→32 (recorded: 24.5% → 94.0%); radial = 0.0% throughout, no sign flips. The Cartesian demotion stands; its smooth-end penalty was overstated ~2.7×. The Session 26–27 marginal numbers (nested sign-flip threshold, oblate +3.09%) remain inside the corrected ~9% smooth-baseline band — still not trustworthy as magnitudes (unchanged reading, tighter band). |
| `mmin_map` S1/S2 latent bugs (stale `adm_hi`; horizon point as bisection endpoint) | **No grade change** | Verified never-fired on the recorded 18-cell map (parquet ADM/nominal ∈ [1.0037, 1.0347]); GATE-2 regression after fix reproduces the canonical cell to ≤1e-4 relative. Map remains **A (within slice)**. |
| 3.10 null-configuration cells | **Grade reading clarified: "A (within slice, one stated structural assumption)" should be read as conditional-A — the assumption is untested exactly where it is load-bearing** | The stated unimodality assumption is really *per-condition monotonicity* of each EC margin in M (which implies the ∧-shape the golden-section search presupposes). It is untested in the null cells (where no window was observed — precisely where observation cannot confirm it), and the SEC-binding near-cap cell shows a third margin curve participates. Reopening trigger unchanged (ledger). |
| κ = 4.64 ± 0.57 | **Definition recorded (was undefined in every doc)** | ±0.57 is the **1σ cross-cell dispersion** of a κ that varies systematically with R₂ — a spread over the 14 located thresholds, not a random error bar on a universal constant. Per-threshold bisection precision is separately rel_tol 0.5%. NAVIGATOR's "over the 18-cell grid" descriptor corrected to the 14 thresholds. |
| 2B.8 Leg 1 wording | **Scope corrected; verdict unaffected** | "No gravitational conductor exists in known physics" is a claim about *matter* (impedance + Dyson absorption). The §4 taxonomy omitted curvature-based partial confinement (QNM-style quasi-bound modes); not separately assessed, subsumed by Leg 3's perfect-mirror grant. QCB §4/§8 + ROADMAP re-scoped; triggers (ii)/(iii) sharpened (theorem-grade counterexample counts for (ii); (iii) reopens Legs 1–2 only). Grades unchanged (Legs 1–2 **B**, Leg 3 **A** within slice). |
| Slice-1 "0/140" (2C.1) | **Evidence-quality caveat recorded; verdict stands pending kill-test** | Preview grid only; R₀ frozen at 5.0; `shift_families_full.json` never dispatched; free-form j₁ ridge (0.94) unrefined — Session-32 false-negative shape. Symbolic Natário dismissal unaffected. Kill-test queued (ROADMAP Session-35 audit queue). |
| Hybrid-wall "0/480" (2C.2) | **Provenance corrected; verdict stands pending kill-test** | Sweep varied (η, δ_M, w_M) only — ε, n frozen at 1.0, 100; `hybrid_wall_full.json` never dispatched. ROADMAP description corrected. |
| 2D.11 Session-33 closure | **Scope caveat recorded** | The augmented anchor's baseline is itself DEC-violating at Npts=49, so the strict-pass gate was uninformative; surviving claim = 100% strict slack-degradation *at that anchor*; anchor V=0.5 vs Session-11 winner V=1.5 unexplained; no strict-pass anchor ever augmented. NAVIGATOR anchor qualifier restored. Multi-anchor kill-test queued. |
| 2A.10 GW-recoil ceiling | **Standing C-grade re-flagged** | TRUST_AUDIT #5 Colab pull still pending since Session 9; `gw_recoil_full.json` never run. Qualitative acceleration no-go (symbolic) unaffected. Queued. |
| thickness_bound provenance (2A.7) | **Provenance corrected** | The κ = 0.05 empirical calibration used the 600-row local preview; the ~1.3e5-point full config was never dispatched (SESSION_LOG Session 6 phrasing overstates). Superseded in practice by 2A.9b/3.10. |
| Stale doc numbers | **Corrected in place** | Four stale [0.05, 0.75] brackets → [0.05, 0.875] w/ supersession notes; README Path-2B/Phase-2C statuses; LANDSCAPE_SYNTHESIS §6/§8 stale + self-contradictory items; phantom task 2D.16 retroactively defined (ROADMAP Phase 2D). |

**Methodological note (fourth instance of the searcher-honesty family):** a verification *harness* is itself code and can carry a systematic bug (R1) for five sessions while every verdict it reports remains directionally correct — because the battery's verdicts were sign/trend-based with large margins. The discipline that caught it was auditing the *evidence* (masks, grids, provenance) rather than the *conclusions*. Corollary recorded in the ROADMAP audit queue: negative results whose grids froze axes or whose full configs never ran (W1/W2) are now flagged in place in the claims record, not just in session logs.

---

## Session 36 addendum — Slice-1 (2C.1) frame-projection bug: grade corrections

**Setup.** Block 2(a) of the Session-35 audit queue (kill-test of the Slice-1 "0/140") escalated: the pre-run diagnostic violated an exact identity, and adjudication found the Slice-1 evaluator itself defective. Full chronology in SESSION_LOG Session 36; adjudication harness `verification/test_shift_families_frame_adjudication.py` (20/20 gates, certification mode).

**Disclosures and grade impacts:**

| Item | Impact | Detail |
|---|---|---|
| Slice-1 evaluator frame projection (`shift_families.ipynb` Cell 3 + sweep module, Sessions 9→36) | **All recorded Slice-1 numbers superseded as wrong-observable; verdict unchanged and upgraded** | Tetrad legs stored as matrix columns but contracted as rows (M T Mᵀ for Mᵀ T M); recorded scalar = coordinate −T_tt, not ρ_E (deviation 2.0–8.6× at the recorded single-point). Affects: single-point table, 140-pt fractions, "best 0.94 free-form ridge" (does not exist on the corrected observable: max 0.0027), Q_zz quadrupole-proxy table (regions selected by the defective observable). |
| Slice-1 corrected result | **Upgraded to A (analytic, within slice)** | Four profile-independent identities close all four families for every parameter value: (i) z-shift ρ_E = −b′²sin²θ/32π ≤ 0 (alcubierre, freeform, any radial multi-mode); (ii) Natário ∇·β ≡ 0 ⟹ ρ_E ≤ 0 (concordant with the Session-15c FH Phase-3b proof, which the recorded table had contradicted since Session 9); (iii) irrotational ∫ρ_E dV = 0 (with analytic 1/r⁴ dipole tail −v²C²/6R, verified to 1.1e-08) ⟹ WEC-everywhere forces ρ_E ≡ 0. Corrected sweeps: 0/140 preview, 0/2496 full config (first dispatch), corrected observable certified against warp_factory_py anchor chain (median 1.6e-07). |
| Irrotational domain truncation | **Provenance corrected** | sympy `log(1±tanh)` antiderivative overflowed for \|r−R₀\| ≳ 19/σ; recorded irrotational fractions were computed on the silently truncated finite subset. Fixed via equal-constant log-cosh form (`_LogCosh`, float64-safe). |
| Session-15c / LITERATURE / MATTER_SHELL_PATH "dismissed as special case of Slice 1" chains | **No grade change; consistency restored** | Those dispositions rested on the FH Phase-3b identity (independent pipeline, unaffected). The Slice-1 table was the outlier; corrected numbers now agree with the identity chain. |
| Krasnikov-class frames (`krasnikov_tube.py`, `hybrid_wall.py`) | **No change** | Audited: their metric has g_tt = −1 and their tetrad rows ARE orthonormal legs consistent with the row-wise contraction (algebra closes: g(u,u)=1, g(∂t,u)=0). The transpose defect is confined to shift_families. 2C.2's kill-test (Block 2(e)) remains a coverage question only. |
| Fell-Heisenberg pipelines (Sessions 10–17, 33) | **No change** | FD-based on FH's closed-form ρ_E decomposition; no shared frame code (grep + Session-35 review). |

**Methodological note (fifth instance of the searcher-honesty family):** a result pipeline can manufacture plausible *positive structure* (the 0.94 ridge) inside a directionally-correct negative, and an already-proven in-repo identity (Session 15c) falsified the recorded table for 14 sessions unnoticed. When a sweep table and a symbolic identity coexist, run the cross-check at closure time — the identity is the cheaper, stronger audit.

---

## Session 37 addendum — TRUST_AUDIT #5 CLOSED (C → B): GW-recoil SXS anchor verified conservative

**Item #5 (GW-recoil ceiling: SXS rescaling β²C^{3/2} heuristic, C-grade since Session 8; Cell 17 Colab path wired Session 9, never run).** Closed 2026-07-05 by [`verification/test_sxs_kick_pull.py`](verification/test_sxs_kick_pull.py) (4/4 gates), which pulls the SXS data over plain HTTPS — Zenodo per-record metadata for SXS:BBH:1937 cross-checked against the collaboration's `catalog.zip` (identical) — with no `sxs` package or Colab required.

**Findings:**

| Finding | Detail |
|---|---|
| Cell-17 design defect | The wired comparison targeted SXS:BBH:1937 as the "high-mass-ratio kick record per Varma 2022" and expected its remnant kick to confirm 5000 km/s within 1.5×. The simulation is actually q = 4.0 **aligned-spin non-precessing** (χ₁⊥ ≈ 9e-7) with remnant kick **93.6 km/s** — 53× below the expectation; aligned-spin systems cannot superkick. The success branch of that cell has never been correct; every recorded execution took the fallback path. Superseded by the harness. |
| Anchor verified conservative | Catalog-wide max remnant kick over 2021 public SXS simulations = **3119.1 km/s** (SXS:BBH:0662, q = 1.33, χ₁⊥ = 0.80; top-5 all near-equal-mass precessing). The Package-3 input 5000 km/s **upper-bounds every public NR simulation (1.60× headroom)** ⟹ the recorded Mechanism-C ceiling is conservative. |
| Full-config sweep | First `gw_recoil_full.json` dispatch (4320 pts; preview regression bit-exact on all 1200 recorded rows). Ceiling Δv/(βc) ≤ 0.58% for physical C ≤ 0.5 (1.41% only at the unphysical (0.99, 0.9) corner); canonical Fuchs point unchanged (~1e-4). Recorded "max at β=0.9, C=0.5" corrected to C=0.3 (label error; the ratio 0.25% was computed correctly). M-axis of the grid is analytically degenerate in both formulas. |

**Grade: C → B** (within slice: single-bubble Fuchs-class shells, quadrupole-order rescaling). Not A: the remnant velocities are accepted from SXS collaboration metadata rather than derived by integrating waveform momentum flux ourselves. Reopening trigger: an NR result or surrogate prediction exceeding 5000 km/s for astrophysically admissible spins, or a shell-specific radiation channel outside the β²C^{3/2} rescaling class.

**Methodological note:** dormant verification code (a wired-but-never-run success branch) can encode a wrong expectation while conferring an appearance of rigor. When closing long-dormant audit items, re-derive the check from the primary data source rather than finally executing the recorded button.

---

## Session 38 addendum — 2D.11 evidence re-based (W3 kill-test): verdict upheld; Session-33 strict-pass gate superseded

**Setup.** Session-35 audit item W3: the 2D.11 Phase-3 closure augmented one anchor whose baseline was DEC-violating at the run's Npts=49 (gate vacuous) with an off-grid V=0.5. Block 2(c) kill-test executed 2026-07-05 (Session 38).

**Disclosures and grade impacts:**

| Item | Impact | Detail |
|---|---|---|
| Session-33 anchor baseline | **Diagnosis corrected: resolution artifact, not anchor choice** | The anchor structure (σ=10, m₀=3, a=0.05, ℓ=4, r=9) is certified strict-pass at Npts=65 for every V on the Session-11 grid; the recorded dec_slack −7.74e-2 was an Npts=49 under-resolution effect. V-choice immaterial: slacks scale exactly as V² (strict-pass signs V-invariant; hence the sweep's exactly-234-per-V strict-pass split). |
| Session-33 "0 strict passes among 2912 augmented points" | **Superseded (baseline-inherited)** | At four certified strict-pass anchors × the same vortical grid at Npts=65 (7280 augmented points), **100% retain strict-pass** at preview amplitudes — including a +8.3e-5-margin anchor under vortical fields 3× the FH amplitude. |
| 2D.11 verdict (vorticity not the driver of "all wall, no interior") | **UPHELD; evidence upgraded to informative gates** | 0/7280 improve either slack (universal degradation confirmed, ∝ V·V_A, ≤0.26% of margin at $\|V_A\| \le 0.3$); passenger_zone_radius = h for all 7285 rows including baselines. Baseline regression vs certified sweep rows ≤4.2e-5 rel (A3: ~1.3e-7 absolute). Within slice: static smooth-N, FH-form multi-mode $\vec A$ with inherited exponents, $\|V_{A,i}\| \le 0.3$ at Npts=65. |
| Session-33 absolute numbers (dec_slack −7.74e-2 baseline etc.) | **Flagged as resolution-contaminated** | Differential (same-grid) claims unaffected; absolute Npts=49 slack values at this anchor family should not be quoted as physical. |

**Methodological rule recorded:** a perturbation study's baseline must pass its decision gates *at the study's own resolution*, else those gates are vacuous — the FD sibling of the Session-30 regime-validity lesson, applied to study design.

---

## Session 39 addendum — nested-shell (Phase 3.3 sub-item 4) REVERSED: first verdict flip of the audit programme

**Setup.** Session-35 audit item W5 (first half): the Session-26 nested-shell mass-split threshold sat inside the demoted Cartesian pipeline's error band. Block 2(d) kill-test executed 2026-07-05 (Session 39) via the new tracked harness [`verification/test_nested_shell_radial_ladder.py`](verification/test_nested_shell_radial_ladder.py) (identical physical configuration; certified `evaluate_axisym_ec`; mmin_map resolution tiers; staged RES_CONF confirmation).

**Disclosures and grade impacts:**

| Item | Impact | Detail |
|---|---|---|
| Session-26 recorded ladder (monotone degradation, flip in (0.10, 0.20)) | **SUPERSEDED — verdict reversed** | Certified radial: min(NEC) rises from +2.8764e38 (f=0) to +2.3299e39 (f=0.10) — an **8.1× improvement** — before declining; certified sign flip $f^* \in [0.6234, 0.6312]$ (RES_CONF, df ≤ 0.01; RES_FULL↔RES_CONF plateau agreement ≤1%). The recorded numbers came from the near-equatorial thin-slab Cartesian convention (1, 300, 300, 5); the certified evaluator minimises over the full (r, θ) mesh. GATE 1: nested builder at f=0 ≡ single-shell profile builder to 0.0 relative. |
| "Fuchs single-shell locally optimal under mass redistribution" (Phase 3.3 composite verdict, was A within slice) | **Refuted within slice; composite verdict revised** | The nesting leg of the composite is reversed; the corrected statement (improvement plateau + $f^* \approx 0.63$) is **A (within slice: two-shell constant-density, fixed radii (5,8)/(10,20), outer-wall warp band, v = 0.02c, fixed $M_{tot}$ = 4.49e27)**. Session-26's physical reading inverted the enclosed-mass argument (inward mass-splits *increase* $M(r)$ throughout the band at fixed $M_{tot}$). |
| Session-27 oblate +3.09% (W5's other half) | **Still unpinned** | Same thin-slab Cartesian provenance; NOT re-tested this session. Until re-run radially, treat the oblate numbers as direction-unknown (the nested reversal demonstrates the band can hide sign *and* structure errors, not just magnitude). |
| New candidate lead | **Recorded (unranked)** | Nested-variant minimal-mass map: does the ~8× margin improvement translate into a lower certified $M_{\min}$ than 3.10's 2.568e27? ROADMAP "Unranked candidate (Session 39)". |

**Methodological note:** first demonstration in this programme that the demoted pipeline's error band hid a *wrong-shape* record (non-monotone → recorded as monotone) and a *wrong-window* threshold (0.63 → recorded as 0.1–0.2), not merely imprecise magnitudes. "Kill-test the negatives" is not ceremonial: three strengthenings and one reversal in four items.

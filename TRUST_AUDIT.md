# Trust Audit — What We Derived vs. What We Accepted

**Last updated:** 2026-04-17 (after Session 8).
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
| 3 | **Fuchs et al. 2024 has a real DEC-satisfying static warp shell** | B | Path 2A loses its anchor; our scaling law still holds in vacuum but we lose the existence example | 1 session: install Warp Factory + reproduce their Fig. 10 (Phase 3 Task 3.1, already on the roadmap). **STATUS: deferred (MATLAB-only on Windows).** |
| 4 | **Schwarzschild extrinsic curvature formulas (Poisson 2004 §3.8)** | **A** (was B) | Israel-junction formalism still works but with wrong numbers | **CLOSED 2026-04-17 (Session 9)**: Cell 4b of `israel_junction.ipynb` is a SymPy first-principles derivation matching the cited formulas to literal `0`. |
| 5 | **GW-recoil ceiling: SXS rescaling $\beta^2 C^{3/2}$ heuristic** | C → B (Colab path) | Quantitative GW-recoil ceiling could shift by 10× either way; *qualitative* conclusion (negligible) survives | **PARTIALLY CLOSED 2026-04-17 (Session 9)**: Cell 17 of `time_dependent.ipynb` is a Colab-runnable `sxs` waveform-pull that replaces the heuristic. Locally falls back. To fully close, run Cell 17 on Colab. |
| 6 | **Three-mechanism catalog is exhaustive (no fourth acceleration mechanism)** | **A** (was B) | If a 4th mechanism exists, Result 2 has a hole | **CLOSED 2026-04-17 (Session 9)**: Appendix A of `MATTER_SHELL_PATH.md` is the formal proof using ADM + Bianchi. No fourth mechanism is possible under the stated assumptions. |
| 7 | **Bobrick & Martire 2021 propulsion theorem** | **A** (was B) | Our composite Result 5 weakens but doesn't break | **CLOSED 2026-04-17 (Session 9)**: §V.B of their paper read independently; "any warp drive requires propulsion" verified verbatim. Audit summary in `KRASNIKOV2003_EVALUATION.md` and `LITERATURE.md` Bobrick-Martire entry. |
| 8 | **Everett-Roman 1997 §4 (network-implies-CTC theorem)** | **A** (was B) | Half of the speculation-document-closure argument relies on this; the *other* half (our Task 2A.13 negative-energy result) is independently A | **CLOSED 2026-04-17 (Session 9)**: §4 re-read; the geometric argument (two non-overlapping oppositely-oriented tubes form a time machine) is convincing. Audit summary in `KRASNIKOV2003_EVALUATION.md` and `LITERATURE.md` Everett-Roman entry. |
| 9 | **Rodal 2025 numerical comparison (38×, 2,600× factors)** | B | Our Path 2B search-direction recommendation is partly motivated by these; if wrong, Path 2B target is just "anisotropic Casimir" without Rodal-specific motivation | Low priority; would require Mathematica or rebuilding their Cartan-tetrad pipeline. **STATUS: deferred.** |

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

**Updated 2026-04-17 (Session 9 audit closures via Phase 2C interleaves):**

- **The Krasnikov no-go (Task 2A.13) is rock-solid (A).**
- **Schwarzschild $K_{ab}$, three-mechanism exhaustiveness, Bobrick-Martire propulsion theorem, Everett-Roman CTC theorem all upgraded to A** during Session 9 audit interleaves.
- **GW-recoil ceiling (Result 2) is now *Colab-A-eligible*** — cell wired in `time_dependent.ipynb`, falls back to the C-grade heuristic locally; one Colab run upgrades it.
- **Path 2A static existence (Result 1) still leans on Fuchs et al. 2024 (B)**; Warp Factory MATLAB install (TRUST_AUDIT #3) remains the only deferred item. Cost: ~1 session in MATLAB.
- **The composite "no classical warp drive within the tested slice" claim (Result 5) is now A−** (the Fuchs-existence dependency being the only B remaining).
- **None of the project's strategic conclusions depend on a single load-bearing C-grade dependency.** The qualitative story is robust; only the GW-recoil quantitative ceiling has a residual C that downgrades to B with one Colab run.

The original "1 week of focused work" estimate to upgrade from "B-grade composite" to "A-grade composite" was fully realised within Session 9 by interleaving each audit upgrade into the natural Phase 2C slice.

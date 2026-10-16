# Le 2026 (three papers) — critical evaluation, reproduction, and placement

**Session 58 (2026-10-16).** An T. Le published three closely related preprints in 2026 that bear directly on this project's anchor (the Fuchs-class matter shell) and on its energy-condition methodology. None was in the repo before the 2026-10-15 closeout audit. This document records what each claims, what we reproduced through our own instruments, and where each sits against the project's slices. Grades follow TRUST_AUDIT (A = derived here; B = accepted from the paper, spot-checked; C = heuristic).

| Paper | arXiv | Local | Battery | Verdict |
|---|---|---|---|---|
| **2026a** *Observer-robust energy condition verification for warp drive spacetimes* | [2602.18023](https://arxiv.org/abs/2602.18023) (v6, 2026-09-24) | `papers/le2026a_observer_robust_ec_2602.18023v6.pdf` | [`verification/test_ec_exact_minimiser.py`](verification/test_ec_exact_minimiser.py) (7/7, incl. a `warpax` cross-check) | **Methodological critique confirmed and absorbed**: the project's EC verdicts were sampled, now exact; no verdict flips; floors +0.3 %. |
| **2026b** *Radiative steering of warp shells* | [2606.22531](https://arxiv.org/abs/2606.22531) (v4, 2026-09-13) | `papers/le2026b_radiative_steering_warp_shells_2606.22531v4.pdf` | [`verification/test_le2026_steering_shell.py`](verification/test_le2026_steering_shell.py) (5/5) | **Reproduced; is our Mechanism B made exact.** No warp content; EC-compliant photon rocket costs 3× the ideal log-mass. |
| **2026c** *Relativistic elastic shells: material support and cavity geometry* | [2605.25417](https://arxiv.org/abs/2605.25417) (v3, 2026-09-17) | `papers/le2026c_relativistic_elastic_shells_2605.25417v3.pdf` | mask-extension kill-test (SESSION_LOG S58; scratch probe) | **Sharpens a standing caveat**: our required-stress verdicts are honest, but *material support* was never posed. No reopening. |

---

## 1. Le 2026a — observer-robust energy conditions

### 1.1 What it asserts

Theorem 1 (S-lemma): at a point, with $\hat T$ the stress tensor in an orthonormal frame and $\eta$ the Minkowski metric, **NEC** holds iff $\hat T+\sigma\eta\succeq0$ for some real $\sigma$; **WEC** iff the same with $\sigma\ge0$; **SEC** iff WEC for the trace-reversed tensor; **DEC** needs two LMI tests. These decide the pointwise conditions for *every* observer and *every* Hawking–Ellis type, with no rapidity cutoff. Finite observer samples and single-frame (Eulerian) readings under-report violations: for Rodal's drive the Eulerian reading misses ≈73 % of the sampled wall WEC violations; Type-IV wall fractions are 75–100 % (Alcubierre), 56–99 % (Natário), 7–93 % (Van Den Broeck). The JAX toolkit `warpax` (MIT) implements the tests.

**Fuchs shell (their §3.6, Table 9).** At canonical parameters ($v_s=0.02$, $R_c=15$ m, 10–90 % width 4.42 m), on the sampled wall band $0.1\le f\le0.9$: **100 % Type I, 0 % Type IV, sampled Type-I slack $R_c^2\min(\rho+p_i)=+0.021$**, with the explicit caveat "margins are sampled Type-I slacks, with no global enclosure". The Garattini–Zatrimaylov row is negative ($-3.5\times10^{-4}$) with a 100 % Eulerian WEC miss.

### 1.2 Why it bit this project

The certified radial oracle ([`warp_factory_py/solvers/axisymmetric_ec.py`](warp_factory_py/solvers/axisymmetric_ec.py)) certifies the **Einstein tensor** against a closed-form ground truth (Prong B, Session 30). The **energy-condition verdict** built on it, however, used WarpFactory's sampled observer field ([`energy_conditions.py`](warp_factory_py/solvers/energy_conditions.py)): 100 Fibonacci directions × 10 speeds at the accept tier, 160 × 16 at RES_CONF. A finite sample is an *upper bound* on the true minimum over observers, so every recorded margin was optimistic by an unknown amount, and "RES_CONF escalation" did not tighten the observer search (the two Fibonacci sets are not nested — Session 58 measured the 160×16 margin *above* the 100×10 one at the floor).

### 1.3 What we did (Session 58)

- **Exact minimiser** [`warp_factory_py/solvers/ec_exact.py`](warp_factory_py/solvers/ec_exact.py): NEC and the DEC flux form as trust-region subproblems on the unit sphere (secular equation in the eigenbasis of the spatial block, hard case included); WEC and SEC as the Euclidean Rayleigh quotient of the 4×4 tensor restricted to the causal cone (interior critical points = Euclidean eigenvectors inside the cone; boundary = the null minimum). Same normalisation conventions as the sampled evaluator, so numbers are comparable. Wired behind `exact=True` in both oracle evaluators and all `mmin_map*` / `spinup_margin` callers; default off, so every pre-S58 battery regresses byte-identically.
- **Battery** 7/7: exact ≤ dense (20k directions) ≤ sampled on random tensors; Type-I closed forms to $10^{-12}$; boosted Type-I signs frame-invariant; trust-region hard case to $10^{-15}$; canonical-cell upper-bound property at every in-shell point for both sampling tiers; sign flip across the S32 floor; **`warpax` LMI cross-check 350/350 sign agreement on all four conditions and 100 % Type-I agreement** (independent pipeline, independent author).
- **Quantified bias** at the canonical cell (accept-tier mesh): mean sampled−exact null gap 0.19 % of the $\rho c^2$ scale at 100×10, 0.13 % at 160×16. **Re-based floors (exact oracle):** single-shell canonical $2.568\times10^{27}\to2.5754\times10^{27}$ kg nominal (**+0.29 %**, inside rel_tol 0.5 %; ADM $2.658\times10^{27}$; κ 4.78; NEC binding); two-body winner — see SESSION_LOG Session 58. **No verdict flips.** Maps (18-cell single-shell, 100-point nested, 456-snapshot spin-up) are queued for exact re-certification on jaga (`hf_jobs/configs/*_exact_full.json`).

### 1.4 Placement

- Their Fuchs row (Type I, positive slack at canonical parameters) is a **two-sided external anchor** for our canonical-cell verdict. Note it does *not* test our lower floors, and it samples a wall band, not the full in-matter mask; our exact oracle does both.
- Their Garattini–Zatrimaylov row (100 % Eulerian miss, locally negative) is consistent with our Session-46 sharpening (local NEC/WEC/DEC violations at a wall-shape multiple of $\hat\rho$).
- The S31/S56 Hawking–Ellis censuses in this project were already observer-aware for the *constructions we adjudicated*; the gap was confined to the shell-class floor machinery and is now closed.

**Grades.** Theorem 1: external, standard convex-analysis content (B; we use our own equivalent minimiser rather than their LMI, and cross-check against it). Fuchs Table-9 row: B, consistent with our A-within-slice canonical verdict. Project upgrade: A.

---

## 2. Le 2026b — radiative steering of warp shells

### 2.1 What it asserts

A compact **flat cavity** bounded by a thin timelike shell, matched exactly (Israel) to a **Kinnersley photon-rocket** exterior. The exterior is outgoing null dust with $4\pi n^2 = -\dot m - 3maq$ (q = cos of the angle from the acceleration axis); all pointwise ECs hold iff $-\dot m\ge3m|a|$. The shell carries strict surface DEC (Type I). Smooth static-to-static burns exist for $\gamma\ge3$ with $m_f=m_ie^{-\gamma d}$; exact steering by successive burns gives $m_j=m_0\exp(-3\sum d_\ell)$ with $d_\ell$ the rapidity-space distance of each velocity change; the cavity centre gains rapidity $\Delta\chi_c=\frac2\gamma(\operatorname{artanh}s_f-\operatorname{artanh}s_i)$. Bondi news vanishes (all flux is matter radiation). Open per the paper: self-gravitating settling after a turn; stability (frozen-surface modes grow under compression); a massive payload is not modelled.

### 2.2 What we reproduced ([`test_le2026_steering_shell.py`](verification/test_le2026_steering_shell.py), 5/5)

| Gate | Content | Result |
|---|---|---|
| L1 | Einstein tensor of the Kinnersley metric for generic $m(u),a(u)$ | **exact**: $G_{ab}=8\pi\,(n^2/r^2)\,\ell_a\ell_b$, $\ell$ null, $4\pi n^2=-\dot m-3maq$ |
| L2 | Static flat-interior shell: $\sigma_0=(1-s)/4\pi R$, $p_0=(1-s)^2/16\pi Rs$, margin $\propto(1-s)(5s-1)$ | **exact**; strict surface DEC iff $2m/R<24/25$; our Task-2A.3 weak-field $\mu=m+m^2/2R$ recovered |
| L3 | Rest-frame moments $\oint n^2=-\dot m$, $-\oint n^2q=ma$ ⟹ Bondi balance; pointwise EC ⟹ $m_f=m_ie^{-3L}$ | **exact**; dipole efficiency $\eta=1/3$ |
| L4 | Mass-cost lemma $\log(M_i/M_f)\ge L=\int\eta\,dw\ge d$ | numerically verified on a constructed causal-exhaust path |
| L5 | Fuel fraction for the cavity centre to reach $0.02c$ (project shells) | below |

**L5 numbers (centre law, $\gamma=3$, $R_0=20$ m):**

| Shell | $2m/R$ | fuel fraction (centre law) | exterior law $1-e^{-3d}$ | ideal photon rocket $1-e^{-d}$ |
|---|---|---|---|---|
| canonical vessel $4.49\times10^{27}$ kg | 0.333 | 4.8 % | 5.8 % | 2.0 % |
| S32 single-shell floor $2.568\times10^{27}$ | 0.191 | 5.3 % | 5.8 % | 2.0 % |
| S47 two-body floor $2.2256\times10^{27}$ | 0.165 | 5.4 % | 5.8 % | 2.0 % |

### 2.3 Placement

- **No warp content.** The cavity is flat and carries no shift: "flatness removes tidal curvature inside the cavity but does not carry those observers with its accelerating boundary." Test observers inside are inertial; the walls accelerate past them. This is the opposite of the Fuchs/Alcubierre design goal (a shift that carries the interior).
- **It is the project's Mechanism B** of the three-mechanism catalog ([`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md) Appendix A; Task 2A.10) made exact with surface-DEC bookkeeping and a real exterior solution. Our catalog entry quoted the ideal relativistic rocket ($1-e^{-d}\approx2\%$ for $0.02c$); **Le's pointwise-EC-compliant Kinnersley pattern costs three times the log-mass** ($e^{-3d}$) because the radiation must stay non-negative over the whole sphere while carrying dipole momentum — a sharpening we adopt for the Mechanism-B row.
- **Relation to the acceleration no-go (2A.10).** Our result was: no *in-vacuum self*-acceleration with DEC matter and no ejecta. Le's construction *is* ejecta (null dust), so it sits inside the one mechanism 2A.10 left open, confirms it works at the exact-solution level for an empty cavity, and prices it. It does not reopen 2A.10. It does address a piece of 2E.1 (manoeuvre with EC bookkeeping) for the *shift-free* cavity class — the 2E.1 criterion (a) is therefore **evaluated, not triggered** for the warp-shell class: a Fuchs shell with its ℓ=1 shift dipole would need the same exterior recoil *plus* the interior shift to survive the burn, which Le does not model.
- **Material question.** Le's Proposition on stress-free recoil (an empty cavity cannot be accelerated without stress or another force) and the growing frozen-surface modes under compression are the same physics as 2026c's point: EC-clean required stress ≠ a supportable material. Routes to the deferred 5.3 stability leg.

**Grades.** L1–L3: A (exact reproduction). Steering theorems (existence of smooth burns, stable causality): B (we verified the ingredients and the mass law, not the existence proofs). Placement: A within the project's slice definitions.

---

## 3. Le 2026c — relativistic elastic shells

### 3.1 What it asserts

**Proposition (isotropic inner-boundary obstruction):** a horizon-free static spherical shell with continuous non-negative density and *isotropic* pressure, $m(a)=0$ at the inner face and vacuum matching without a surface layer there, is impossible: TOV gives $p'\le0$, so $p(b)=0$ at the outer face forces $p\equiv0$, contradicting $\rho>0$ somewhere. **Truncating** a positive-pressure fluid at the inner face leaves a massless Israel layer with tangential pressure $P_\Sigma=a\,p(a^+)/2$ that **violates surface DEC**; **smoothing** the jump "produces a transition stress that must be included explicitly; it does not retain the original isotropic equilibrium." Tangential elastic stress *can* support two free faces with DEC and subluminal sound speeds (explicit smooth anisotropic example with $p_r=0$); radial linear stability holds in weak gravity; even-parity and rotating stability are open. The paper explicitly names subluminal warp shells (Fuchs et al.) as the motivating geometry and notes such bodies have non-constant lapse and curved slices — outside the unit-lapse flat-slice no-go class — but "neither propulsion nor a travel-time advantage follows from the cavity."

### 3.2 What this means for the Fuchs-class builder

The project's builder ([`warp_factory_py/metrics/warp_shell.py`](warp_factory_py/metrics/warp_shell.py), mirroring WarpFactory) computes an isotropic TOV-type pressure, **cuts it to zero inside $R_1$**, and then smooths both $\rho$ and $P$ four times with a ~5 m box kernel — exactly the "smoothing" branch of the proposition. Two consequences were checked in Session 58:

1. **Mask-extension kill-test (negative = good).** The oracle's energy conditions evaluated over the *whole* radial window $[0.5, 30]$ m rather than the in-shell mask $[R_1,R_2]$, at the canonical mass, the S32 floor and +5 %: **no violation anywhere** — the worst off-mask values are $\sim10^{-9}$ of the $\rho c^2$ scale (numerical noise in the vacuum regions). The smoothed transition stress at the inner face is EC-clean in the required-stress sense. So the in-shell mask convention did not hide a face violation.
2. **The smoothed density's real support** (canonical cell): $\rho_{\rm smooth}\ge10\%$ of peak on $[6.0, 24.0]$ m, $\ge50\%$ on $[9.7, 20.3]$ m, $\ge1\%$ on $[3.3, 26.7]$ m. The quadruple box smoothing has total support ±10 m, so the "cavity" at the 10 % level is $r<6$ m, not $r<10$ m. This is Fuchs's own convention (our Fig.-10 reproduction is byte-exact), but it should be read alongside every thin-cell κ caveat in the record.

### 3.3 Placement

- The project's verdicts are **required-stress** verdicts: $T_{\mu\nu}$ is read off $G_{\mu\nu}$ of the smoothed metric and tested pointwise. That is honest and now observer-robust (§1). What the project never posed — and Le does — is whether a **material** can supply that stress with its own equations of motion. Barzegar et al. 2026 make the same complaint from the other side (their `err:TOV`). This is a genuine, standing caveat on the Fuchs class and on every certified floor: *necessary, not sufficient*.
- Le's $p_r=0$ tangential-support family is a concrete alternative support ansatz. Our Phase 3.3+ Step 2 (metric-first free $\alpha$, $m$) already searched the general anisotropic space negatively, so no large mass gain is expected; a targeted $p_r=0$ check is recorded as an optional lead in ROADMAP, not opened.
- Nothing here reopens a closed item. It strengthens the project's own 5.3 (stability) deferral rationale.

**Grades.** Proposition: A (two-line TOV argument, reproduced in our reading; the shared 24/25 bound is certified in §2 L2). Mask-extension negative: A within slice. Material-support caveat: recorded as scope, not graded.

---

## 4. Reopening triggers evaluated

| Trigger | Status after Session 58 |
|---|---|
| ROADMAP 2E.1 (a): external inflate-then-coast / manoeuvre construction with explicit EC bookkeeping | **Evaluated — not triggered for the warp-shell class.** Le 2026b is the shift-free cavity (Mechanism B); the warp-shell version would need interior shift + exterior recoil together. |
| Phase 4 (a): published claim of a warp drive satisfying NEC/WEC | Not raised by Le (2026b claims surface DEC for a *rocket*, not a warp; 2026c claims DEC for *static* elastic shells). |
| TRUST_AUDIT methodology: observer-robust EC verdicts | **Closed** — exact minimiser adopted, cross-checked against `warpax`. |
| 5.3 stability (deferred) | Two new external inputs (frozen-surface growth under compression; elastic radial stability in weak gravity). Still deferred; now has literature to start from. |

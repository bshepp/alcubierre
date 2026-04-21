# Fell-Heisenberg vorticity-augmented sweep — notes

Companion to the new sweep modules `hf_jobs/sweeps/fell_heisenberg_vortical*.py` for **Task 2D.11**: generalise the Fell-Heisenberg irrotational shift $\vec N = \nabla\phi$ to a mixed irrotational + vortical $\vec N = \nabla\phi + \vec\nabla \times \vec A$ and ask whether the §9 "all wall, no interior" passenger-zone pathology is specific to $\nabla \times \vec N = 0$ within the static smooth-N slice.

Phases mirror the [`AGENTS.md`](AGENTS.md) "surfing, not paper-writing" discipline — three sub-families of $\vec A$ explored sequentially, each with its own slice-scoped headline. Plan lives at [`/memories/session/plan.md`](#); cumulative finding lands at the bottom (§4).

## §1 Phase 1 — axisymmetric $A_\phi(R, Z)$ — NEGATIVE within the explored slice

### §1.1 Pipeline

Refactored [`hf_jobs/sweeps/fell_heisenberg.py`](hf_jobs/sweeps/fell_heisenberg.py): the legacy `adm_stress_energy(phi, h)` is now a thin wrapper around the new `adm_stress_energy_from_N(N_vec, h)` which takes a precomputed shift vector. Bit-exact regression at the canonical anchor on Npts=49 (max abs diff = 0.0 across `rho_E`, `K`, `S_ij`).

New module [`hf_jobs/sweeps/fell_heisenberg_vortical.py`](hf_jobs/sweeps/fell_heisenberg_vortical.py) implements the axisymmetric ansatz

$$A_\phi(R, Z) \;=\; V_A \cdot R \cdot \exp\!\left(-\frac{(R - r_A)^2}{\sigma_A^2}\right) \cdot \tanh(Z/\ell_A) \cdot \exp\!\left(-\frac{Z^2}{2\sigma_A^2}\right)\,, \qquad R = \sqrt{X^2 + Y^2}.$$

The leading $R$ factor enforces axis-regularity ($A_x = -Y \cdot A_\phi/R$, $A_y = X \cdot A_\phi/R$ stay bounded; the quotient $A_\phi/R$ is evaluated directly to avoid the $R = 0$ singularity). curl is taken with the project's 4th-order FD stencil. Total shift $\vec N = \nabla\phi + \vec\nabla \times \vec A$ is fed into `adm_stress_energy_from_N`. The sweep also reports `passenger_zone_volume` and `passenger_zone_radius` inline (lifted from [`hf_jobs/analysis/fell_heisenberg_horizon.py`](hf_jobs/analysis/fell_heisenberg_horizon.py)) so we can triage without a separate horizon pass.

V_A=0 reduces the augmented pipeline to the irrotational baseline bit-exactly across all 12 record fields (regression check, `diff = 0` at the canonical anchor on Npts=49).

### §1.2 Two previews ran; both negative

**Preview 1** — [`fell_heisenberg_vortical_preview.json`](hf_jobs/configs/fell_heisenberg_vortical_preview.json), 81 points, V_A ∈ [0, 0.5, 1.0]. 11.2 s local. `passenger_zone_radius = 0.5 = h` for every point. `N_vortical_max` reaches ~9 at the upper V_A — non-perturbative regime. Strict-pass count = 0 (inherited from baseline `dec_pass_fraction = 0.999882 ≠ 1`).

**Preview 2 (perturbative)** — [`fell_heisenberg_vortical_preview_perturbative.json`](hf_jobs/configs/fell_heisenberg_vortical_preview_perturbative.json), 135 points, V_A ∈ [0.0, 0.05, 0.10, 0.15, 0.20] tightly inside the perturbative window. 15.6 s local. Per-V_A summary at the canonical FH anchor:

| V_A | best `dec_slack_min` | best `wec_slack_min` | best `passenger_R` | best `dec_pass_frac` | `N_vortical_max` |
|---|---|---|---|---|---|
| 0.000 | -7.74e-2 |  +4.82e-3 | 0.500 | 0.999882 | 0.000 |
| 0.050 | -7.74e-2 |  +4.96e-3 | 0.500 | 0.999882 | 0.460 |
| 0.100 | -7.74e-2 |  +5.09e-3 | 0.500 | 0.999882 | 0.920 |
| 0.150 | -7.74e-2 |  +5.20e-3 | 0.500 | 0.999882 | 1.379 |
| 0.200 | -7.74e-2 |  +4.95e-3 | 0.500 | 0.999882 | 1.839 |

Three observations:

1. `dec_slack_min` is **flat at the irrotational baseline** for any (V_A, σ_A, r_A, ℓ_A) where the support of $A_\phi$ does not reach the global DEC-violating cell. The global DEC violator is in a region of the FH bubble that axisymmetric A_φ doesn't touch.
2. Where A_φ *does* touch the violating region (e.g. r_A=6, σ_A=4 or r_A=9), `dec_slack_min` becomes **strictly more negative** with V_A — vorticity *worsens* the dec slack:

   | (σ_A, r_A, ℓ_A) | V_A=0 dec_slack_min | V_A=0.20 dec_slack_min |
   |---|---|---|
   | (2.5, 6.0, 2.5) | -0.0774 | -0.0799 |
   | (4.0, 6.0, 2.5) | -0.0774 | -0.0931 |
   | (1.0, 9.0, 2.5) | -0.0774 | -0.1005 |

3. WEC-pass actively **degrades** at moderate V_A in compact configurations: at (σ_A=1, r_A=6, ℓ_A=2.5) the wec_slack_min drops below zero already at V_A=0.10 (`wec_pass_fraction = 0.981`), and at (σ_A=1, r_A=9, ℓ_A=2.5) wec drops at V_A=0.05 (`wec_pass_fraction = 0.948`). Vorticity creates new WEC violations without fixing the existing DEC violation.

`passenger_zone_radius = 0.5 = h` for every one of the 135 points. The §9 zero-volume passenger-zone pathology is robust to perturbative axisymmetric vorticity at this anchor.

### §1.3 Slice scope (what this does and does not establish)

**Establishes:** within the slice {Session-11 canonical anchor (V=0.5, σ=10, m₀=3, a=0.05, ℓ=4, r=9), $\vec A = A_\phi(R, Z)\hat\phi$ with the specific Gaussian envelope above, V_A ∈ [0, 0.2], σ_A ∈ {1, 2.5, 4}, r_A ∈ {3, 6, 9}, ℓ_A ∈ {1, 2.5, 4}, Pi=0.25, Npts=49, L=12}, **no point recovers an extended passenger zone, no point achieves strict WEC+DEC pass, and the dec slack never improves over the irrotational baseline.** Most points either leave the dec slack unchanged or make it (and/or wec) worse.

**Does not establish:**

- Whether *non-axisymmetric* vector potentials behave differently. Phase 2 (Cartesian $\vec A$ with $\nabla\cdot\vec A = 0$) tests this directly.
- Whether *non-perturbative* axisymmetric A_φ at favourable phasing relative to the FH bubble might find an isolated strict-pass point. The Phase-1 broad preview reached `N_vortical_max ≈ 9` and saw the same behaviour; not exhaustive but suggestive.
- Whether varying the FH parameters $(V, \sigma, m_0, a, \ell, r)$ off the Session-11 anchor would change the picture for axisymmetric vorticity. The full Phase-1 sweep ([`fell_heisenberg_vortical_full.json`](hf_jobs/configs/fell_heisenberg_vortical_full.json), ~10 920 points, ~$3 cpu-xl) was prepared but **not dispatched** — Phase-1 preview was already definitive enough to justify advancing to Phase 2 under the gate documented in [`/memories/session/plan.md`](#). Re-open if Phase 2 / 3 finds the axisymmetric restriction was uniquely binding.

### §1.4 Decision per the plan's Phase-1 gate

Plan §"Phase 1 decision gate" listed three branches; we are in case "Phase 1 finds no extended passenger zone" → "Phase 2 becomes critical — could be that axisymmetric A is too restrictive and a Cartesian A is needed." Phase 2 begins.

### §1.5 Files

- Refactored: [`hf_jobs/sweeps/fell_heisenberg.py`](hf_jobs/sweeps/fell_heisenberg.py) (`adm_stress_energy_from_N` + thin compat wrapper)
- New module: [`hf_jobs/sweeps/fell_heisenberg_vortical.py`](hf_jobs/sweeps/fell_heisenberg_vortical.py)
- Configs: [`hf_jobs/configs/fell_heisenberg_vortical_preview.json`](hf_jobs/configs/fell_heisenberg_vortical_preview.json), [`hf_jobs/configs/fell_heisenberg_vortical_preview_perturbative.json`](hf_jobs/configs/fell_heisenberg_vortical_preview_perturbative.json), [`hf_jobs/configs/fell_heisenberg_vortical_full.json`](hf_jobs/configs/fell_heisenberg_vortical_full.json) (deferred)
- Sweep outputs (gitignored): `sweeps/fell_heisenberg_vortical_*.parquet`
- Triage analysis script: [`agent-tools/analyse_vortical_perturbative.py`](agent-tools/analyse_vortical_perturbative.py)

## §2 Phase 2 — Cartesian $\vec A$ with three constant amplitudes — NEGATIVE within the explored slice

### §2.1 Pipeline

Module [`hf_jobs/sweeps/fell_heisenberg_vortical_cartesian.py`](hf_jobs/sweeps/fell_heisenberg_vortical_cartesian.py) implements the simplest non-axisymmetric extension: three Cartesian components share a single Gaussian-modulated profile and carry independent constant amplitudes,

$$A_i(X, Y, Z) \;=\; V_{A,i} \cdot \exp\!\left(-\frac{(R - r_A)^2}{\sigma_A^2}\right) \cdot \exp\!\left(-\frac{Z^2}{2\sigma_A^2}\right) \cdot \tanh(Z/\ell_A) \,, \quad i \in \{x, y, z\}.$$

No gauge fix is enforced: the *physical* vortical shift $\vec\nabla \times \vec A$ is gauge-invariant, so different $(V_{Ax}, V_{Ay}, V_{Az})$ produce different physical curls regardless of $\nabla \cdot \vec A$. This is **not** a generalisation of Phase 1 — Phase 1's $\vec A = A_\phi \hat\phi$ has an amplitude that rotates with $\hat\phi(X, Y)$, whereas here $\vec A$ points in a fixed Cartesian direction. So Phase 2 tests a structurally different vorticity family.

### §2.2 Preview ran; bit-exact baseline regression + clean negative

[`fell_heisenberg_vortical_cartesian_preview.json`](hf_jobs/configs/fell_heisenberg_vortical_cartesian_preview.json), 27 points (V_Ax, V_Ay, V_Az ∈ {0, 0.1, 0.2}), profile params pinned at Phase-1 best-coverage values, FH at canonical anchor. 5.0 s local. **All 27 points OK.**

- **Baseline regression**: V_Ax=V_Ay=V_Az=0 row gives `dec_slack_min = -7.743132e-02`, `wec_slack_min = +4.820419e-03`, `passenger_zone_radius = 0.5`, `dec_pass_fraction = 0.999881547` — matches the irrotational FH baseline and the Phase-1 V_A=0 row to all printed digits. The refactored `adm_stress_energy_from_N` is consistent across both vortical modules.
- **0 of 27** points strictly improve `dec_slack_min` over baseline.
- **0 of 27** points strictly improve `wec_slack_min` over baseline. `wec_slack_min = +4.82042e-03` is *bit-identical* across all 27 rows — the WEC-violating cell sits in a region the Cartesian curl-A perturbation does not reach.
- **0 of 27** points achieve strict WEC+DEC pass.
- **0 of 27** points have `passenger_zone_radius > h`.
- `dec_slack_min` strictly degrades for every (V_Ax, V_Ay, V_Az) ≠ (0, 0, 0): range −7.74e-2 (baseline) → −7.84e-2 (worst, at V_Ax=V_Ay=V_Az=0.2). The maximum vortical magnitude reached is `N_vortical_max = 0.113` — well inside the perturbative regime, but even that's enough to see strict degradation.

### §2.3 Slice scope

**Establishes:** within the slice {Session-11 canonical FH anchor, $A_i = V_{A,i} \cdot g(X, Y, Z; \sigma_A=2.5, r_A=6, \ell_A=2.5)$ shared profile, $V_{A,i} \in \{0, 0.1, 0.2\}$ each, Pi=0.25, Npts=49, L=12}, **no Cartesian-amplitude vortical perturbation moves dec_slack_min in the helpful direction or extends the passenger zone.** Combined with Phase 1, *two structurally distinct vorticity families* (axisymmetric $A_\phi$ vs constant-direction Cartesian $\vec A$) both fail to recover an extended passenger zone or improve the dec slack at this FH anchor.

**Does not establish:**

- Whether a **richer vortical ansatz** — e.g. FH-style multi-mode $\vec A$ where each Cartesian component has its own independent FH-style structure $A_i(X, Y, Z) = $ FH-form rather than a shared Gaussian × tanh — could recover a passenger zone. Phase 3 would test this.
- Whether **jointly varying FH params + vortical params** finds isolated strict-pass points (the Phase-1 and Phase-2 full configs do this, ~$5 cpu-xl, **not dispatched**). The cumulative two-phase negative argues this is unlikely to overturn the slice-scoped no-go.
- Whether **non-perturbative** Cartesian-A configurations (V_A ~ O(1)) might find a sweet spot. The Phase-1 broad preview reached `N_vortical_max ≈ 9` and saw the same monotone-degradation behaviour, suggesting non-perturbative does not rescue this.

### §2.4 Cumulative finding (Phases 1 + 2)

Across **two structurally distinct vorticity families** at the Session-11 canonical FH anchor:

| family | # points | best Δ(dec_slack_min) | best Δ(wec_slack_min) | strict-pass | passenger_R > h |
|---|---|---|---|---|---|
| Phase 1 axisymmetric $A_\phi$ | 135 + 81 | 0.0 (flat) | +3.8e-4 (marginal) | 0 | 0 |
| Phase 2 Cartesian constant $\vec A$ | 27 | -1.0e-3 (worse) | 0.0 (flat) | 0 | 0 |

**Working interpretation (slice-scoped):** at the Session-11 canonical FH anchor, the §9 zero-volume passenger zone and the 4-cell DEC violation are *not* fixable by adding perturbative $\vec\nabla \times \vec A$ within smooth, well-localised vector-potential families. Where vorticity affects the dec slack, it makes it worse. Both negative families share the property that $\vec A$'s support is determined by ($\sigma_A, r_A, \ell_A$) profile parameters, and in both cases the *global* DEC violator sits in a region the curl A doesn't reach helpfully. This is structurally consistent with the Session 14 finding that the FH WEC+DEC-passing region is "all wall, no interior" — the wall location is set by the FH bubble geometry, and the curl A's support is set by the vortical envelope; getting them to overlap helpfully is not free.

### §2.5 Files

- New module: [`hf_jobs/sweeps/fell_heisenberg_vortical_cartesian.py`](hf_jobs/sweeps/fell_heisenberg_vortical_cartesian.py)
- Configs: [`hf_jobs/configs/fell_heisenberg_vortical_cartesian_preview.json`](hf_jobs/configs/fell_heisenberg_vortical_cartesian_preview.json), [`hf_jobs/configs/fell_heisenberg_vortical_cartesian_full.json`](hf_jobs/configs/fell_heisenberg_vortical_cartesian_full.json) (deferred)
- Sweep output (gitignored): `sweeps/fell_heisenberg_vortical_cartesian_*.parquet`
- Triage analysis: [`agent-tools/analyse_vortical_cartesian_preview.py`](agent-tools/analyse_vortical_cartesian_preview.py)

## §3 Phase 3 — FH-style multi-mode $\vec A$ — TBD

Not yet started. Decision gate: see §2.4 cumulative finding. The natural Phase 3 design would give each Cartesian component its own independent FH-style structure (multiple modes with sums of erf/exp factors at different scales) rather than a shared Gaussian envelope, matching the structural complexity of $\phi_{\rm FH}$ itself. This is more expensive (more parameters) and harder to interpret. Awaiting decision.

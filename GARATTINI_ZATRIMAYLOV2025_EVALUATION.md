# Garattini & Zatrimaylov 2025 — Critical Evaluation + Reproduction

**Paper:** R. Garattini, K. Zatrimaylov, *Positive-Energy Warp Drive in a De Sitter Universe*, Phys. Lett. B (2025), [arXiv:2502.13153v2](https://arxiv.org/abs/2502.13153). Local copy: `papers/2502.13153v2.pdf`.
**Executed:** Session 46 (2026-07-06) — audit-queue **Block 3(c)**, ROADMAP open-lead #2. Relaxes/probes **assumption 5b** of the NAVIGATOR load-bearing table (asymptotic flatness — energy-condition obligations).
**Battery:** [`verification/test_gz_desitter_reproduction.py`](verification/test_gz_desitter_reproduction.py) (9 gates; ~7 min). All equation references below are to the paper.

---

## Verdict

**Reproduced exactly — the first external construction in this programme to survive reproduction with every checked equation at machine precision.** Within its slice (de Sitter flat-slicing PG form + Ellis embedding + radial Hubble-matched trajectory; generic wall profile for the symbolic identities, tanh and compact-C² profiles numerically) the paper's claims are all **CONFIRMED and upgraded to A-grade**:

- Eq. 6 is exactly the ADM Hamiltonian constraint; Eqs. 14/17/18/20/23 all verified symbolically for a *generic* profile f, and against the **full 4D Einstein tensor of the exact time-dependent metric** (moving bubble x₀(t) = xᵢe^{t/L}) at machine precision (gate 3: 2e-15).
- Under Hubble matching, ρ_E ≥ 0 everywhere (gate 7: min ρ_E ≳ −1e-12, exactly 0 in the interior for compact f), the Eulerian momentum flux vanishes identically (≤1e-14), and the bubble is an **exact mass-conserving rearrangement of vacuum energy**: ∫(ρ−ρ̂)d³r and ∫(T_ij−T̂_ij)d³r → 0 (gate 6; ~2e-10 at Rbox=8, exponential in box size for tanh tails).
- The fixed-t **volume-averaged** WEC/NEC claims (Eqs. 26–31) hold: sorted-principal-pressure averages dilute exactly as 1/V (±1.6e-2 → ±8.7e-4 over Rbox 3→8), and Eq. 24–25's stress formula matches the full G_ij/8π to 1.4e-15 — pinning the paper's (unstated) sign convention to K_ij = +½(∂_iN_j+∂_jN_i).
- Local NEC/WEC violations exist as claimed (quantified below).

**But the reproduction sharpens the record in four ways that matter for assumption 5b:**

1. **The bubble is exactly comoving — the construction has zero transport content.** The matching condition v⃗ = r⃗₀/L integrates to r⃗₀(t) = r⃗ᵢe^{Ht}: the bubble center is a *comoving point* of the de Sitter flow. The interior (f≡1) is an exact Minkowski patch whose inertial observers move with the Hubble flow — exactly like a comoving galaxy. "Warp drive moving at the expansion velocity" = "vacuum-energy void carried by the expansion." The paper concedes the practical version of this (travel r−rᵢ ≪ rᵢ, else Hubble-time journeys; direction fixed radially); the sharp version is that the loophole buys **no motion at all relative to the comoving frame**. Within this project's usefulness criteria (transport-relevant, steerable, accelerable): not a warp-drive loophole.
2. **"Averaged" means fixed-Eulerian-time volume average only — ANEC is violated.** The averaged conditions the paper proves are integrals over d³r at constant t in the preferred slicing. They are *inherited from the background*: any mass-conserving, compactly-supported, flux-free rearrangement of de Sitter satisfies them identically (gate 6 is exactly this statement; the background saturates NEC pointwise). The averaged energy conditions that appear in the singularity/censorship/superluminal-no-go literature are **line integrals along causal geodesics** (ANEC/AWEC). Our gate-8 probe integrates T_μνk^μk^ν dλ along complete null geodesics of the exact metric (y=0 plane, totally geodesic; compact-support profile): **every wall-crossing ray tested has strictly negative ANEC** — near-axial ±z: −9.2e-5; wall-grazing b=0.5 (both directions): −8.0e-3 ≈ 1.3× the background density scale ρ̂ = 3/(8πL²) = 5.97e-3 (kt=1 launch normalization); side-on: −4.5e-4. A control ray missing the compact support returns +6e-14 ≡ 0. Slice scope: plain (not achronal-restricted) ANEC, meridional-plane family, one parameter set — but the sign is uniform across the family and the integrand is exactly zero outside the wall, so this is not marginal. *(Numerical-integrity footnote: the flat dS patch is past-incomplete — null rays reach the patch boundary at finite affine parameter with unbounded blueshift, so ANEC is only well-defined here for compactly-supported walls; with tanh tails the backward integral formally diverges. The probe therefore uses a C² compact wall and terminates integration only where the integrand is identically zero.)*
3. **The local violations are order-background, and scale-locked to it.** Under matching, N = −x/L + f(rs)(x−x₀)/L exactly — every bubble deviation is a function of x−x₀ with a single 1/L amplitude, so all stress deviations scale as (wall shape)/L², the same power as ρ̂. The local violation is a **fixed multiple of the background vacuum density, set only by wall shape** — independent of L and of bubble position. Measured: tanh wall (σ=3, R=1): min NEC/WEC/DEC slack = −0.843 (8π units) = **1.76× ρ̂**, at mid-wall rs = 1.01; compact quintic wall (battery gate 7): −1.636 at L=2.5 and −0.409 at L=5 — **3.41× ρ̂ at both**, ratio 0.250 (the 1/L² law confirmed to three digits). Physically: at the real Hubble scale the wall's NEC violation is **dark-energy-scale** (~10⁻⁹ J/m³ × shape factor) — utterly negligible in absolute terms, but structurally ineliminable.
4. **The underdensity theorem (Eqs. 32–40) is sound for the paper's class, but the written proof overreaches at Eq. 38.** Algebra of Eqs. 34/36 verified symbolically (gate 9). However "the only way to avoid this is Q ≡ 0" (Eq. 38) does not follow from WEC alone: WEC forces only Q ≥ 0, and explicit families exist with Q ≥ 0, Q ≢ 0 (e.g. δρ < 0 compensated by isotropic pressure δT_ij = cδ_ij, c ≥ −δρ — WEC holds for every observer; these have no underdensity in fast frames, so the theorem's conclusion is untouched). The proof closes rigorously for the paper's own class via a one-line repair: their perturbations are mass-conserving in every frame (Eq. 41), so ∫Q d³r = 0, and Q ≥ 0 ∧ ∫Q = 0 ⟹ Q ≡ 0 ⟹ δT ∝ g ⟹ δρ = const ⟹ trivial. The G-Z bubble itself illustrates the boundary case: its interior is underdense in *every* frame with WEC exactly *saturated* there (Q ≡ 0, T_μν ≡ 0 inside) — the violations live in the wall.

---

## What the paper does (compressed)

De Sitter in flat-slicing Painlevé-Gullstrand form: ds² = −dt² + (dr − (r/L)dt)² + r²dΩ², L = 1/H — a Natário-class metric (lapse 1, flat 3-metric) with shift N^i = −x^i/L. Ellis-style embedding N^i → −(1−f)x^i/L − f v^i with f = f(rs), rs = |x⃗−x⃗₀(t)|. The Santiago-Schuster-Visser theorem (their ref [25]) says asymptotically-flat Natário spacetimes always have ρ_E < 0 somewhere; the loophole exploited is a shift that is **irrotational AND asymptotically non-vanishing** (the de Sitter background). For general v⃗ the Eulerian density (Eq. 14) has a negative-definite curl term ∝ |(v⃗−r⃗/L)×r̂_s|²; setting v⃗ = r⃗₀/L kills it identically (the shift becomes the gradient Eq. 20), leaving Eq. 17 ≥ 0 for monotone f. Eq. 18 rewrites ρ as background + total divergence ⟹ the bubble is a vacuum-energy underdensity (ρ=0 inside) surrounded by an excess shell, total mass conserved. T_ni = 0; volume-averaged ⟨T_ij⟩ = −⟨ρ⟩δ_ij ⟹ averaged NEC saturated, averaged WEC satisfied, both violated locally. A generic theorem: vacuum perturbations underdense in every frame always violate NEC/WEC locally. Applications suggested: dark-energy fluids, Casimir-cavity analogy ("underdensities in positive vacuum energy, not true negative energy"), analogue-gravity realizations.

## Reproduction record (battery gates)

| Gate | Paper claim | Result |
|---|---|---|
| 1 | Eq. 6 (Natário-class ρ_E) | ≡ Hamiltonian constraint, generic N — symbolic 0 |
| 2 | Eqs. 14/17/18/23 | all symbolic 0 for generic f, generic v⃗, generic center |
| 3 | Eq. 14→17 vs full 4D G_μν, matched moving bubble | 2.0e-15; Eulerian flux 6.7e-16 |
| 4 | unmatched trajectory control | Eq. 14 exact (5.6e-16) but flux = 0.34 ≠ 0 — **Hubble matching is load-bearing** |
| 5 | Eq. 24–25 spatial stress | ≡ full G_ij/8π to 1.4e-15; K_ij = +½(∂N+∂Nᵀ) convention pinned |
| 6 | Eq. 18 / Eq. 26 mass-conserving rearrangement | ∫δρ, ∫δT_ij → 0 with box size (−9.0e-5 → −1.3e-9 → 2.1e-10 for Rbox 3/5/8, tanh) |
| 7 | Eq. 17 positivity + local violations | min ρ_E ≥ 0; flux ≡ 0; min NEC/WEC/DEC slack < 0 mid-wall, ∝ 1/L² (fixed multiple of ρ̂) |
| 8 | *(our extension)* ANEC probe | **ANEC < 0 on every wall-crossing null geodesic tested**; miss-ray control ≡ 0; null-constraint drift ≤ 4e-9 |
| 9 | Theorem Eqs. 32–40 | Eq. 34/36 algebra exact; Eq. 38 proof-step gap + repair recorded |

Session-record numbers not in the battery (same machinery, exploratory scans): tanh wall σ=3, R=1, L=2.5 — min NEC/WEC/DEC slack −0.843 (8π units) = 1.76ρ̂ at rs = 1.01; SEC slack −2.51 (background Λ violates SEC by construction); sorted-eigenvalue averaged NEC ±1.6e-2/±3.5e-3/±8.7e-4 at Rbox 3/5/8 (∝ 1/V exactly); interior (rs≈0.03): ρ = 4.9e-6, |T_ij| ≤ 5.7e-6 (tanh-tail residuals; exactly 0 for compact f).

## Relation to our slices

- **Assumption 5b** (NAVIGATOR): the qualifier "energy-condition obligations are modified in de Sitter for v = v_Hubble" is **real and now A-grade within slice** — but it is a statement about a *comoving void*, not about a vehicle. The pointwise conditions our no-go uses (WEC/DEC in the matter frame) are still violated in the wall; what the construction achieves is ρ_E ≥ 0 + volume-average bookkeeping inherited from the background. ANEC — the averaged condition with theorem weight — is violated.
- **Slice-1 connection:** the loophole is exactly the SSV fall-off assumption (shift asymptotically non-vanishing), the same assumption family our Session-36 analytic Slice-1 closure works within (asymptotically flat). No tension: different slice.
- **Lentz/FH contrast:** Lentz 2020 and Fell-Heisenberg 2021 claim Eulerian positivity and fail it under reproduction (S43–45: not reproducible from the published record / S42: box artifact). G-Z's positivity claim **survives exact reproduction** — the difference is that G-Z buy positivity by surrendering transport entirely (comoving lock) rather than by construction error.
- **The Casimir-underdensity reading** (their §4) is consistent with our Path-2B closure: they explicitly model Casimir cavities as *underdensities in positive vacuum energy*, i.e. "only relatively negative" — which is the same physics as the 2B.8 conclusion that no warp-relevant absolute negative density is available from that channel.

## Slice scope of this closure

Verified: the published ansatz class (PG-dS + Ellis embedding, radial Hubble-matched trajectory), generic wall profile for all symbolic identities; tanh and compact-C² profiles, parameter spot-checks (L ∈ {2.5, 4, 5}, one bubble geometry each) for the numerics; plain ANEC on a bounded meridional-plane ray family at one parameter set. Not asserted: the paper's suggested generalizations (stationary bubbles, non-spherical, f < 1 interiors, AdS); achronal-restricted ANEC; semiclassical/QI status of the wall stresses; behaviour under Λ ≠ exact (quintessence etc.).

## Trust grades (TRUST_AUDIT Session-46 addendum)

- Paper's Eqs. 6/14/17/18/20/23/24-27/30-31: **A within slice** (reproduced machine-exact, incl. against the full 4D Einstein tensor of the exact time-dependent metric).
- Underdensity theorem: **A for the mass-conserving class** (with our repaired proof step); the paper's Eq.-38 step as written: incorrect-in-general, conclusion unaffected.
- Our sharpenings (comoving lock; ANEC violation; violation-scale lock to ρ̂): **A within the stated probe scope**.

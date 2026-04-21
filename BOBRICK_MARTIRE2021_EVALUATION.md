# Bobrick & Martire 2021 — Critical Evaluation

**Paper:** Alexey Bobrick & Gianni Martire, *"Introducing physical warp drives,"* Class. Quantum Grav. **38**, 105009 (2021). arXiv: [2102.06824](https://arxiv.org/abs/2102.06824).

**Evaluator:** Phase 2D session 17, in support of [Task 2D.9](ROADMAP.md) (FH source-matter classification).

**Local copies:** `papers/2102.06824v2.pdf`, `papers/extracted/bobrick2021/`.

---

## TL;DR

B-M 2021 is **two distinct contributions glued together**, both worth taking seriously:

1. **A four-class taxonomy of stationary warp-drive spacetimes** (§2.1) based on whether the global Killing vector $\xi$ that aligns with $\partial \mathcal{D}_{\rm in}$ is timelike or spacelike inside vs. asymptotic infinity. This is a clean kinematic classification and is the right framework to ask "what *kind* of warp drive is this metric?"

2. **A spherically-symmetric, isotropic-fluid positive-energy construction** (§3) — the first explicit warp-drive metric that is manifestly positive-energy, satisfies WEC+DEC, and is causally trivial. The construction works because it relaxes the Alcubierre/Natário "Requirement 1" (flat exterior) and the "Requirement 2" (synchronized internal/external clocks). The price is a Schwarzschild exterior (gravitating bubble) and time dilation inside.

**Where it sits relative to our work:**

- The **taxonomy** is useful as a definitional anchor and gives us a vocabulary for [FELL_HEISENBERG_SWEEP_NOTES.md §14](FELL_HEISENBERG_SWEEP_NOTES.md) to report that **FH realises the Class III geometric signature ($\xi$ timelike inside, spacelike outside) at $v_s = 0$ — outside the regime any B-M class was designed for.**
- The **positive-energy construction** does *not* generalise straightforwardly to FH or to anything axisymmetric. B-M 2021 explicitly leaves axisymmetric positive-energy warp drives to future work (§4 opening paragraph). We have not attempted that generalisation; it is logged as a long-shot in [MATTER_SHELL_PATH.md](MATTER_SHELL_PATH.md).
- B-M 2021 makes **no claim that superluminal warp drives are possible with classical matter.** §3.2 in fact proves that all spherically-symmetric positive-energy drives are subluminal (Class I). The often-quoted "B-M 2021 made warp drives possible" framing is overstated — the paper made *one specific subluminal* warp drive class possible, with the physics of a Schwarzschild gravitating bubble plus time dilation.

---

## 1. The four-class taxonomy (§2.1)

B-M defines a stationary warp-drive spacetime as three nested regions: asymptotically-flat vacuum $\mathcal{D}_{\rm out}$, an arbitrarily-curved warping shell $\mathcal{D}_{\rm warp}$, and a flat passenger interior $\mathcal{D}_{\rm in}$. A global Killing vector $\xi$ aligned with the four-velocity of $\partial \mathcal{D}_{\rm in}$ defines the comoving rest frame.

The four classes are characterised by whether $\xi$ is timelike (TL) or null/spacelike (SL) inside $\mathcal{D}_{\rm in}$ vs. at asymptotic infinity:

| Class | $\xi$ in $\mathcal{D}_{\rm in}$ | $\xi$ at infinity | $v_s$ | Comment |
|-------|----|-----|-----|---------|
| I (mild subluminal)     | TL  | TL  | $<c$    | Contains weak-field shells, Alcubierre/Natário in subluminal regime, and the §3 positive-energy spherically-symmetric drives. |
| II (mild superluminal)  | SL/null | SL/null | $\geq c$ | Requires "superluminal matter" — DEC-violating in any perfect fluid description. Limited interest. |
| III (extreme superluminal) | TL | SL/null | $\geq c$ | Alcubierre/Natário in superluminal regime. Requires Killing horizon $\partial \mathcal{D}_{\rm K}$ not to intersect $\mathcal{D}_{\rm warp}$, otherwise DEC fails. |
| IV (extreme subluminal) | SL/null | TL  | $<c$    | Black-hole-like; Killing horizon must coincide with $\partial \mathcal{D}_{\rm in}$. |

**Key facts about the classification:**

- Classes II, III, and IV all *require* the existence of a Killing horizon somewhere in or on the boundary of $\mathcal{D}_{\rm warp}$, because $\xi$ has to change sign somewhere if the inside and the asymptotic infinity differ. B-M's positivity-of-energy results are limited to spacetimes that avoid this horizon falling inside the warping region.
- The Alcubierre and Natário drives, in the subluminal regime, are class I, but their positivity properties are nonetheless bad because they enforce two extra "Requirements" (flat exterior + synchronized internal clocks) that force the energy density to integrate to zero inside $\mathcal{D}_{\rm warp}$, thereby requiring negative energy regions. See §2.2 of the paper.
- The Eulerian observer four-velocity $u_\mu = (1/\sqrt{-g^{00}})\,(1,0,0,0)$, and the energy density in the comoving system, $w = (-g^{00})^{-1} T^{00}$, are the right invariants for comparing energy contents across classes (§2.3). For FH with $\alpha = 1$, $g^{00} = -1$ and $w = T^{00}$ trivially.

## 2. The §3 spherically-symmetric positive-energy construction

The setup is the most general spherically-symmetric stationary metric in Schwarzschild coordinates,

$$ds^2 = -N(r)\,c^2\,dt^2 + \Lambda(r)\,dr^2 + r^2\,d\Omega^2,$$

with $N(r), \Lambda(r)$ general. The energy density (B-M Eq. 3) is then

$$w(r) = \frac{1}{8\pi r^2}\left(1 - \left(\frac{r}{\Lambda(r)}\right)'\right),$$

and Birkhoff's theorem fixes $N(r)$ outside $\mathcal{D}_{\rm warp}$ to the Schwarzschild form $N = 1 - 2 m_{\rm enc}/r$ once an isotropic-fluid stress-energy ($T_{rr} = P\Lambda$, $T_{\theta\theta} = T_{\varphi\varphi} = P r^2$) is assumed.

The continuity equation $T^\mu_{~r;\mu} = 0$ then becomes the TOV equation:

$$\frac{N'}{N} = -\frac{2\,P'}{P + \rho}.$$

Under the simplifying assumption that $\rho = \rho(P)$ (e.g. polytropic), B-M derives that $N(r_{\rm in}) = N(r_{\rm out})$, i.e. **the lapse at the inner boundary equals the lapse at the outer boundary**. This means the time inside the bubble is dilated relative to a remote *observer at rest* by the same factor as ordinary Schwarzschild gravitational time dilation, but **runs at the same rate as the comoving observer at infinity**. Time dilation inside is bounded above by the trivial Schwarzschild bound: at Earth-mass / 10 m radius, $\Delta t/t \approx 4 \times 10^{-4}$. Useful as a propulsion mechanism this is not.

§3.2 then proves a strong negative result: **superluminal Class II/III warp drives cannot be spherically symmetric** (the $\mathrm{SO}(3)$ orbits would have to be orthogonal to a spacelike Killing field, forcing radially-moving comoving observers — incompatible with axisymmetric forward motion). And Class IV cannot be spherically symmetric either (would need non-zero energy in $\mathcal{D}_{\rm in}$, contradicting flatness there).

**Net of §3:** the only spherically-symmetric positive-energy warp drives are subluminal Class I, with bounded interior time dilation, gravitating Schwarzschild exterior, and no faster-than-light propulsion in any meaningful sense.

## 3. What B-M does *not* solve

- **No axisymmetric positive-energy construction.** §4 opens by saying explicitly that axisymmetric closed-form expressibility "is not possible for a general axisymmetric spacetime, [so] we leave generalizing the positive energy spherically symmetric warp drive solutions to the axisymmetric case to future studies." This is the open problem most directly relevant to FH.
- **No acceleration analysis.** B-M 2021 is strictly stationary. Whatever propulsion mechanism would accelerate the bubble is left to "future studies of the propulsion mechanism" (§5). This dovetails with the obstruction we proved in [acceleration.ipynb](acceleration.ipynb) for the boosted Alcubierre family.
- **No quantum-inequality analysis beyond a citation.** Eq. (4) in the paper notes that quantum inequalities like Pfenning-Ford 1997 may permit small negative energies, but the §3 construction is purely classical and the QI analysis is left implicit.
- **The "shell of ordinary material" framing is qualitative.** Once you ask what happens when a finite-mass-density shell is moved through Minkowski background at $v_s < c$, you are doing TOV plus boost — interesting, but not a warp drive in any propulsion sense. The "drive" is moved by ordinary thrusters; the metric simply describes the gravitating shell.

## 4. Where FH lies in the B-M framework

See [FELL_HEISENBERG_SWEEP_NOTES.md §14](FELL_HEISENBERG_SWEEP_NOTES.md) for the full numerical analysis. Headline:

- The FH static Killing vector $\partial_t$ has $g_{tt} = -1 + |\vec N|^2$. Across all 8 representative strict-pass points at $N_{\rm pts}=65$, $g_{tt} < 0$ at the central single passenger voxel only and $g_{tt} > 0$ everywhere else (~$10^7$ cells across the box). This is geometrically the Class III pattern (TL inside, SL outside).
- But FH is statically constructed: $v_s = 0$ by design. Class III requires $v_s \geq c$. **FH realises a Class III geometric signature in a kinematic regime no B-M class was designed to cover.**
- The FH stress tensor is **not isotropic**: median $(p_3 - p_1)/|\rho| \approx 0.49$ across cells, isotropic-fraction $\sim 7 \times 10^{-6}$ (central voxel only). B-M §3's isotropic-fluid framework therefore does not apply; the FH source matter is best described as an anisotropic fluid (or stiffer — a solid).
- The FH bulk is positive-energy ($\rho > 0$ at all interior cells), but $p_1 < 0$ in some cells — so the stress-energy is anisotropic with negative principal pressures in pockets, while $\rho$ stays positive. This is consistent with WEC+DEC pass at the eigenvalue level.
- A Hawking-Ellis Type-I-like indicator passes at $\sim 0.99996$ of cells, broadly consistent with [Rodal 2025's](RODAL2025_EVALUATION.md) result that irrotational shifts give globally-Type-I stress-energy.

## 5. Honest accounting

This evaluation depends on:

- **A-grade (derived in our notebooks):** the per-cell eigenvalue computation, the $g_{tt}$ sign pattern, the anisotropy ratio, and the rho-positivity statistics for the 8 representative points. Files: [`hf_jobs/analysis/fell_heisenberg_matter.py`](hf_jobs/analysis/fell_heisenberg_matter.py), [`fell_heisenberg_matter/`](fell_heisenberg_matter/).
- **B-grade (accepted from the paper, spot-checkable):** the four-class taxonomy verbatim from B-M §2.1; the §3 spherically-symmetric positive-energy result; the §3.2 impossibility proofs for spherically-symmetric Class II/III/IV.
- **C-grade (heuristic):** the *labelling* of FH as "Class III geometric signature" is a heuristic mapping from $g_{tt}$ inside-vs-outside sign to B-M's classes; B-M's classes are defined in terms of a global Killing vector aligned with $\partial \mathcal{D}_{\rm in}$ and a Killing-horizon analysis we have not done in full. The Hawking-Ellis Type-I-like indicator is a $\rho>0 \wedge p_3 - p_1 < |\rho|$ proxy, not a full eigenvector decomposition.

## 6. Cross-references

- [FELL_HEISENBERG_SWEEP_NOTES.md §14](FELL_HEISENBERG_SWEEP_NOTES.md) — full numerical analysis behind §4 above.
- [MATTER_SHELL_PATH.md §3](MATTER_SHELL_PATH.md) — the matter-shell engineering wedge that B-M §3 leaves wide open in the axisymmetric case.
- [RODAL2025_EVALUATION.md](RODAL2025_EVALUATION.md) — irrotational-shift Type-I result.
- [LITERATURE.md](LITERATURE.md) — B-M 2021 entries.
- [TRUST_AUDIT.md](TRUST_AUDIT.md) — A/B/C grading framework used in §5.

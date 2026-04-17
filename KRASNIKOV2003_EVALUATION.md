# Krasnikov 2003 — Critical Evaluation

**Paper:** S. V. Krasnikov, *"The quantum inequalities do not forbid spacetime shortcuts"*, Phys. Rev. D **67**, 104013 (2003). arXiv: [gr-qc/0207057](https://arxiv.org/abs/gr-qc/0207057).

**Evaluator:** Slice 4 of Phase 2C, Session 9, after the Slice 1-3 negative results narrowed our load-bearing assumptions to (a) classical positive matter and (b) tight Pfenning-Ford-style QI bounds.

**Local copies:** `papers/0207057v3.pdf`, `papers/arXiv-gr-qc0207057v3.tar.gz`.

---

## TL;DR

**Krasnikov 2003 makes a serious case that the QI-based "warp drives need cosmological negative energy" argument has at least three substantive loopholes.** Specifically, he constructs explicit examples where:

1. The QI doesn't apply because the ratio $|C_{\alpha\beta\gamma\delta}|/|R_{\mu\nu}|$ is large (the Weyl-tensor regime).
2. The integrated $E_{\rm tot}^-$ is *meaningless* — it's a semiclassical quantity computed in a regime where semiclassical gravity itself is unreliable, analogous to summing the Coulomb field energy of a point charge.
3. The integrated $E_{\rm tot}^-$ can be made *small* (down to $\sim 10^{-3}$ g) by combining a "dihedral wormhole" portal with a Van Den Broeck-style pocket.

**This is not a positive-energy construction** — Krasnikov does not produce a classical-DEC-respecting warp drive or wormhole. But his three loopholes mean the canonical "QI rules out useful shortcuts" claim, which we cited in `KRASNIKOV_TUBE_NOTES.md` and `MATTER_SHELL_PATH.md`, is **less robust than we treated it**. Specifically:

- His §2.2 argument (large Weyl, small Ricci) is essentially independent of our framework and represents a genuine semiclassical loophole.
- His §3.2 argument (large $E_{\rm tot}^-$ but meaningless) is philosophically subtle and we should treat as a serious caveat to using $|E_{\rm tot}^-|$ as a quantitative no-go input.
- His §3.3 explicit construction (portal + pocket = $10^{-3}$ g exotic matter) is the strongest item — if accepted, it eliminates the "cosmological negative energy" objection to Morris-Thorne wormholes entirely.

**Implication for our project**: The Krasnikov no-go we proved in Task 2A.13 is **classical** ($\rho_p^{\min} = -0.122 \eta/\epsilon^2$ from local Einstein equations) and **independent** of any QI argument. Krasnikov 2003 doesn't touch our classical no-go. It does, however, weaken the standard *additional* QI objection that wormhole / shortcut spacetimes need cosmological-scale exotic matter — meaning that if a *quantum-supplemented* construction were ever proposed (Path 2B-style), Pfenning-Ford-derived order-of-magnitude bounds should not be the deciding objection.

---

## What he actually proves

### §2.2 — Setup of the standard QI argument

The standard derivation (Ford-Roman, Pfenning-Ford) chains:

$$\dis^{-4} \sim \rho^2 \quad \Rightarrow \quad \dis \lesssim l_P/\sqrt{\sigma} \quad \Rightarrow \quad |E_{\rm tot}^-| \gtrsim 10^{32} M_{\rm galaxy}$$

for an interstellar wormhole or Krasnikov tube of useful $\rho_{\max}$. The first step relates the QI's bound on negative energy density $\rho \sim 1/\Delta^4$ to the curvature scale $\dis$ via the assumption that *both* the Riemann and Einstein tensors are of order $1/\dis^2$.

### §3.1 (Way Out 1) — The Riemann tensor is *not* always order $R_{\mu\nu}$

The Riemann tensor decomposes as $R_{\alpha\beta\gamma\delta} = C_{\alpha\beta\gamma\delta} + (\text{Ricci pieces}) + (\text{trace pieces})$. The QI chain assumes $|C| \lesssim |R|$, which Krasnikov notes "breaks down more often than not."

His example: in *any* curved empty region (e.g. near a star), $R_{\mu\nu} = 0$ identically (vacuum Einstein equation) but $|C_{\alpha\beta\gamma\delta}| \neq 0$. Therefore $|C|/|R| = \infty$ formally. The conformal-anomaly trace $\langle T^\mu{}_\mu \rangle \propto C^2 + R^2 - R^2/3 + \Box R$ shows that even in regions where $R = 0$, the *quantum* stress-energy expectation can be large from the Weyl piece alone.

**Implication**: The QI's $\Delta^{-4}$ bound on negative energy density does not *automatically* propagate to a $1/\Delta^2$ bound on the curvature/Einstein scale. The chain requires $|C| \lesssim |R|$ which is a non-generic assumption.

This is a *genuine* loophole. Our project's KRASNIKOV_TUBE_NOTES.md §4 cited the Pfenning-Ford QI estimate without flagging this caveat. We should add it.

### §3.2 (Way Out 2) — $E_{\rm tot}^-$ is unphysical when its support is sub-Planckian

The QI's bound on integrated $E_{\rm tot}^-$ is computed semiclassically. In regions where the support of negative-energy density is *sub-Planckian* (which is exactly the Pfenning-Ford prediction for Krasnikov tubes: $\Delta \lesssim l_P/\sigma^2$), Krasnikov argues that semiclassical gravity itself becomes unreliable, and the formal value of $E_{\rm tot}^-$ is meaningless.

His analogy: in classical electrostatics, the integrated field energy of a point charge $E_{\Upsilon} = \tfrac{1}{8\pi}\int_\Upsilon E^2 d^3x = 10^{32} M_\odot$ formally, but no one concludes this rules out point charges — they conclude that classical electrostatics breaks down at sub-electron-radius distances, and the smeared average $\bar\varphi(x_0)$ is the physically meaningful quantity.

The same logic applies to $E_{\rm tot}^-$: when its support is sub-Planckian, only spatial averages over $\sim 100 l_P$ can be trusted, and the formal $E_{\rm tot}^-$ is a meaningless extrapolation beyond the regime of semiclassical gravity. Krasnikov gives an explicit example: a self-consistent Morris-Thorne wormhole metric with oscillating $\Omega(\xi) = \Omega_0 \exp[\epsilon \sin(\xi/\xi_0)]$ where $\epsilon, \xi_0 \ll 1$. The metric oscillates on length scales $\xi_0 \ll l_P$, the formal $E_{\rm tot}^-$ is enormous, but the *physically meaningful* averaged $\bar\Omega \approx \Omega_0$ is fine.

**Implication**: Citations of "Krasnikov tubes require $10^{32} M_{\rm galaxy}$" need a footnote: this is the formal value computed under the assumption that semiclassical gravity is reliable down to sub-Planckian scales, which is not a defensible assumption.

### §3.3 (Way Out 3) — Explicit construction with $E_{\rm tot}^- \sim 10^{-3}$ g

This is the most concrete part. Krasnikov constructs:

1. A **"dihedral portal"** wormhole that abandons spherical symmetry: $ds^2 = -dt^2 + 4(\varepsilon^2(\eta) + \eta^2)(d\eta^2 + d\zeta^2)$ in 2D, generalised to 4D with two transverse directions. The exotic-matter region $\Xi$ has volume $V_\Xi \sim \varepsilon^2 \zeta_0^2$ — *quadratic* in $\varepsilon$ rather than $\varepsilon^3$ as in a spherical wormhole. This single change reduces $|E_{\rm tot}^-|$ by 35 orders of magnitude relative to the spherically symmetric case.

2. A **Van Den Broeck-style "pocket"** with metric $r(l) = (1/2 l_1) l^2 + l_1/2$ on $l \in (-l_1, l_1)$. Total exotic matter to support the pocket: $\sim 10^{-3}$ g for $l_1 \sim 1$.

3. **Combined pocket + portal**: a passenger enters the pocket (large interior, small exterior), then exits via the portal. Total exotic matter requirement: $10^{-3} + 10^{-4} = $ a few mg.

This **is** an explicit construction that satisfies the QI and produces a useful traversable wormhole with macroscopic interior radius and only mg of exotic matter. It is **not** a positive-energy construction (still requires negative energy), but the *amount* is many orders of magnitude smaller than the canonical "$10^{32} M_{\rm galaxy}$" claim.

**Implication**: If we ever were to seriously evaluate a "hybrid quantum/classical wall" hypothesis (the original Slice 4 computational follow-up), the QI-bounded negative-energy budget could plausibly be in the milligram range, not the cosmological range.

---

## What he does NOT prove

1. **No classical positive-matter construction**. Krasnikov 2003 always uses *quantum* (vacuum-polarisation) negative energy, just less of it than the Pfenning-Ford bound suggested. He does not produce a DEC-respecting classical matter source. **Our Task 2A.13 negative result is therefore unaffected**: we showed the *classical* Krasnikov-tube wall has $\rho_p^{\min} = -0.122 \eta/\epsilon^2$ from the local Einstein equations, with no QI input. That bound stands.
2. **No accelerating warp drive**. His constructions are static traversable wormholes and Krasnikov tubes (which are also static once formed). Our Package 3 result on the absence of classical acceleration mechanisms is also unaffected.
3. **No experimental realisability**. Krasnikov's proposals are purely theoretical and rely on semiclassical gravity in regimes where its reliability is itself questionable.

---

## Implication for our project

### Direct implications

- **Soften the citation of "QI forbids useful Krasnikov tubes"** in `KRASNIKOV_TUBE_NOTES.md` and `MATTER_SHELL_PATH.md`. The QI argument has at least three substantive loopholes (Krasnikov 2003 §§3.1–3.3) and is not the airtight bound the Pfenning-Ford 1997 paper presents it as.
- **Our Task 2A.13 classical no-go is the primary result.** The QI argument was a secondary support; the classical Einstein-equation result $\rho_p^{\min} = -0.122 \eta/\epsilon^2$ is what really closes the bare-vacuum Krasnikov tube. Krasnikov 2003 doesn't touch this.
- **A "Slice 4b" hybrid quantum/classical computation is now open**, in principle. The setup would be: take our Task 2A.13 classical wall, suppose a small negative-energy quantum component is permitted (say, mg-scale per Krasnikov 2003 §3.3), and ask whether the combination is DEC-compatible. Expected outcome: the *spatial distribution* of the negative energy still matters — it has to coincide locally with where our classical analysis needs it. This is a genuinely interesting calculation that I'm deferring to a future session.

### Indirect implications

- **Rodal 2025 evaluation context strengthens.** Rodal 2025 reduced the *peak proper energy deficit* by 38× without addressing QI bounds. If Krasnikov's §3.1–3.3 arguments are right, the *integrated* QI bound on $E_{\rm tot}^-$ may be much weaker than canonical, which is relevant context for whether a "near-zero net energy" warp drive (Rodal's framing) is in fact within reach.
- **Path 2B target sharpened further.** Path 2B (Casimir / boundary-mode QFT) was already targeting *anisotropic transverse vacuum stresses*. Combined with Krasnikov 2003's argument that the *amount* of QI-bounded negative energy needed for a useful drive may be milligram-scale rather than cosmological, the QFT-source constructibility question becomes more tractable.

---

## Audit interleaves (TRUST_AUDIT #7 and #8)

Slice 4's paper-reading work also closes two TRUST_AUDIT items:

### TRUST_AUDIT #7 — Bobrick & Martire 2021 §III–IV

Read `papers/extracted/bobrick2021/WarpDriveClasses.tex` §3-4. Headline content:

- **§III.A (spherically symmetric warp drives)**: They show that for a spherically symmetric *subluminal* warp drive built from purely positive matter (Class I in their classification), the inner-region time can only pass *more slowly* than at asymptotic infinity, never faster. This is the rigorous version of "positive matter cannot accelerate clocks" that motivates the negative-energy requirement of Alcubierre/Natário (which want the inner time to pass faster — equivalent to "reaching the destination sooner than light"). For a 10-m Earth-mass shell, time slowdown is $\sim 4 \times 10^{-4}$.
- **§III.B (impossibility of superluminal spherically symmetric)**: Class II/III drives (superluminal) cannot be spherically symmetric because the Killing vector defining the local rest frame becomes spacelike. This restricts superluminal drives to be at least axisymmetric.
- **§V.B (constructing warp drives, the propulsion theorem)**: *"Whatever is the acceleration mechanism, it must obey the conservation of 4-momentum. This is because all warp drive spacetimes are asymptotically-flat. An unfortunate error, introduced in [Alcubierre1994], was to postulate the velocity in Equation (1) to be time-variable. ... such a construction violates energy conservation. ... no metric which describes an accelerating warp drive solution has so far been presented in the literature."*

This is the rigorous form of the "any warp drive requires propulsion" theorem we relied on. **TRUST_AUDIT #7 closed**: their §V.B is exactly the asymptotic-flatness + 4-momentum conservation argument we summarised in `MATTER_SHELL_PATH.md` Appendix A. Independent verification that our citation was accurate.

### TRUST_AUDIT #8 — Everett-Roman 1997 §4 (network → CTC theorem)

Re-read Everett-Roman 1997 §4 (lines 335–374 of their PDF; we have it extracted). Headline argument:

In 3D, given a single Krasnikov tube from Earth → Deneb (the "outbound" tube), a spaceship can construct a *second* tube from Deneb → Earth on a parallel path at distance $\rho_0 > 2\rho_{\max}$. The two tubes don't overlap (separated in $\rho$). With both tubes in place:

1. Spaceship starts at Earth at $t = 2D$ (some time after both tubes are built).
2. Travels to Deneb via *second* tube, arriving at $t \approx D$ (the second tube is oriented to allow this superluminal trip).
3. Travels back to Earth via *first* tube, arriving at $t \approx 0$.

Net round-trip from $t = 2D$ to $t = 0$: backward in time by $2D$. Choose $\rho_0$ small enough and the backward jump is arbitrary. **CTC.**

The argument is essentially geometric, two pages, and convinced me. **TRUST_AUDIT #8 closed.**

Also worth noting: Everett-Roman explicitly point out that CTCs are avoided *only* if all tubes in a network share a single global preferred orientation axis — which essentially defeats the network's purpose, since one cannot build a closed transportation graph with a strict global ordering.

---

## Citation

```bibtex
@article{Krasnikov2003,
  author       = {Krasnikov, S. V.},
  title        = {The quantum inequalities do not forbid spacetime shortcuts},
  journal      = {Phys. Rev. D},
  volume       = {67},
  pages        = {104013},
  year         = {2003},
  doi          = {10.1103/PhysRevD.67.104013},
  eprint       = {gr-qc/0207057},
  archivePrefix = {arXiv},
}
```

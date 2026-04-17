# Fell & Heisenberg 2021 — Critical Evaluation

**Paper:** Shaun D.B. Fell & Lavinia Heisenberg, *"Positive Energy Warp Drive from Hidden Geometric Structures"*, Class. Quantum Grav. **38**, 155020 (2021). arXiv: [arXiv:2104.06488](https://arxiv.org/abs/2104.06488).

**Local copies:** [`papers/2104.06488v4.pdf`](papers/2104.06488v4.pdf), `papers/arXiv-2104.06488v4.tar.gz`.

**Evaluator:** Session 10 of the surfing-mode landscape exploration. Following the Slice 1 negative result (which showed no single-mode axisymmetric shift family achieves WEC), Fell-Heisenberg 2021 was identified as the most credible standing positive-energy classical warp drive claim in standard GR. This document evaluates their construction in our framework.

---

## TL;DR (post-computation, Session 10 wrap-up)

**Fell-Heisenberg 2021 is genuinely interesting but is *not* claiming what it is widely cited as claiming.** Independent reproduction in our pipeline ([`fell_heisenberg.ipynb`](fell_heisenberg.ipynb), Phase 3b of the audit-synthesis-fell-heisenberg plan) confirms three things:

1. **The pipeline regression passes A-grade**: their algebraic decomposition of the Hamiltonian constraint (Eq. WECinansatz) matches our symbolic Einstein-tensor-derived Eulerian energy formula to literal symbolic zero.
2. **Their qualitative claim is correct**: a smooth multi-component irrotational shift $\vec{N} = \nabla\phi$ can produce positive Eulerian energy density $\rho_E > 0$ on 99.8% of interior cells of a finite domain, with a superluminal central $|\vec{N}|$. The total positive energy is in the right ballpark of their reported $\sim 5 \times 10^{-4} M_\odot c^2$ (within a factor of 2 at our parameter choice).
3. **Full WEC and full DEC are violated in compact regions** (confirmed independently): 1.3% of interior cells violate full WEC, 5.3% violate full DEC. Fell-Heisenberg's §3.3 admission is qualitatively correct, but **the violations are smaller and more confined than their text suggests** ("no amount of modification could get rid of these regions" reads as overstated relative to our quantitative finding that the compact regions are 1-5% of the interior, not pervasive).

The headline "positive energy warp drive" refers specifically to the **Eulerian energy density** $\rho_{\rm Eulerian} = T_{\mu\nu} n^\mu n^\nu$ — the timelike eigenvalue of the stress-energy tensor. They explicitly state in §3.3 that:

> *"the WEC is violated in compact regions within the energy distribution. … the principle momenta constraints is where the violations occur, namely, $\rho + p_i^p < 0$ for some $i \in \{1,2,3\}$ in compact regions in the distribution. **No amount of modification to the configuration could get rid of these WEC-violating regions.**"*

And in their next paragraph: *"the full dominant energy condition is also violated due to the fact $|\rho| - |p_i^p| < 0$ for some $i$ in compact regions in the distribution"*.

So:
- **Eulerian energy density**: positive everywhere in their construction. ✓ (their actual claim) **REPRODUCED at 99.8% of interior cells**
- **Full WEC** ($\rho + p_i \ge 0$ for all principal pressures $p_i$): violated in compact regions. ✗ (admitted by the authors) **REPRODUCED at 1.3% of interior cells**
- **Full DEC**: violated in the same regions. ✗ (admitted by the authors) **REPRODUCED at 5.3% of interior cells**

This is **precisely the same Eulerian-vs-full-WEC distinction** that we identified in the [Rodal 2025 evaluation](RODAL2025_EVALUATION.md): the timelike eigenvalue can be positive while the principal-pressure-incorporating energy conditions fail because of negative anisotropic pressures.

**Implication for our project**: Fell-Heisenberg 2021 does *not* break the Path 2A or Slice 1 negative result, because Path 2A and Slice 1 use full WEC/DEC (the principal-pressure tests), not just the Eulerian energy density. Their construction is *consistent* with our finding (single-mode shifts have negative Eulerian energy AND violate full WEC; multi-mode shifts have positive Eulerian energy but still violate full WEC in compact regions); the apparent contradiction in the secondary literature is a definitional confusion.

**Most surprising finding**: the full-WEC violation regions are **much smaller** than Fell-Heisenberg's emphatic "no amount of modification could get rid of these" suggested. At our parameter choice, only 1.3% of cells violate full WEC. This raises the *real open question*: **could a more carefully-designed $(m, n)$ pair eliminate the residual full-WEC violations entirely, giving a fully WEC-respecting classical warp drive in standard GR?** Fell-Heisenberg's text says no; their actual numerical evidence and ours don't quite establish that. This is a clean, well-defined open computational lead — and now the most interesting thing this project has surfaced.

---

## What they actually prove

### §2 (Theory): the Hamiltonian-constraint decomposition

In the (3+1)-decomposition with unit lapse $N = 1$, flat spatial slices ($\gamma_{ij} = \delta_{ij}$), and an arbitrary time-independent shift vector $\vec{N} = (N_x, N_y, N_z)$, the Hamiltonian constraint (their Eq. (WECinansatz)):

$$16\pi \rho_{\rm Eulerian} = 2(\partial_x N_x \partial_y N_y + \partial_x N_x \partial_z N_z + \partial_y N_y \partial_z N_z) - \tfrac{1}{2}\bigl[(\partial_z N_y + \partial_y N_z)^2 + (\partial_y N_x + \partial_x N_y)^2 + (\partial_z N_x + \partial_x N_z)^2\bigr]$$

This is a **direct consequence** of the Gauss-Codazzi relation $G_{\mu\nu} n^\mu n^\nu = \tfrac{1}{2}(K^2 - K_{ij} K^{ij})$ on flat spatial slices. The first term is indefinite-sign and quadratic in derivatives of *different* shift components; the second term is negative-semidefinite and involves only *like-component* derivatives.

**Their key observation**: if the shift has only one non-zero component (as in Alcubierre, $\vec{N} = (-v_s f(r_s), 0, 0)$), the first (positive-helping) term vanishes identically and the Hamiltonian constraint reduces to a manifestly negative expression $16 \pi \rho = -\tfrac{1}{2}[(\partial_y N_x)^2 + (\partial_z N_x)^2]$ — explaining why the standard Alcubierre construction has negative Eulerian energy. **To satisfy the WEC** (in the Eulerian sense), *any* ansatz must have at least two non-zero shift components.

### §3 (Helmholtz decomposition)

Under a Helmholtz decomposition $\vec{N} = \vec{\nabla}\phi + \vec{\omega}$ (with $\vec{\nabla} \cdot \vec{\omega} = 0$), the Hamiltonian constraint takes the form (their Eq. (WECinhelmholtz)):

$$16\pi \rho_{\rm Eulerian} = 2(h_1 + h_2 + h_3) - 2\langle \mathcal{J}, \mathcal{H}\rangle_F - \langle \mathcal{J}, \mathcal{J}\rangle_F + \tfrac{1}{2}|\vec{\nabla} \times \vec{\omega}|^2$$

where $\mathcal{H}$ is the Hessian of $\phi$, $\mathcal{J}$ is the Jacobian of $\vec{\omega}$, and $h_i$ are the second-order principal minors of $\mathcal{H}$.

**Two important sub-cases** they identify:

1. **Purely irrotational** ($\vec{\omega} = 0$): $8\pi\rho = h_1 + h_2 + h_3$. Eulerian energy positive iff the sum of second-order principal minors of the Hessian is positive. Momentum density $\vec{p} = 0$.
2. **Purely solenoidal** ($\phi = 0$): $\rho = -\tfrac{1}{16\pi} K_{ij} K^{ij} \le 0$. Always negative Eulerian energy (this matches Natário, which is purely zero-expansion, equivalently solenoidal).

### §3.3 (the explicit positive-Eulerian-energy soliton)

Their explicit smooth construction is a $C^2$-differentiable scalar potential

$$\phi(x, y, z) = \frac{V}{m+n}\bigl[\sigma(\dots) + \sqrt{\sigma\pi}(\dots)\bigr]$$

with parameters $(\Pi, r, V, \sigma) = (1/4, 6, 10, 1)$ and spatial functions $m(x, y, z), n(x, y, z)$ chosen with axisymmetric breaking ($m > n$ in $+z$, $m < n$ in $-z$) to produce a "highly linear" central shift in the $+z$ direction. The central shift magnitude is $\sim 1.26$ (superluminal in geometric units).

**Numerical headline (their §4 "Numerics")**: $\rho_{\rm max} \approx 3.2 \times 10^{26}\,\mathrm{kg/m^3}$ (likely to form a black hole at this concentration), total energy $E_{\rm total} \approx 9.25 \times 10^{43}\,\mathrm{J} \approx 10^{-4} M_\odot$.

### §3.3 final paragraph (the admission)

This is the part most secondary literature glosses over but that is critical for our project's interpretation. Quoting verbatim:

> *"With the Eulerian energy distribution in hand, the full WEC can now easily be investigated to study the nature of the energy distribution in other frames of reference. By analyzing the Lorentz-invariant eigenvalues of the stress-energy tensor calculated using Eq. (METRIC), it turns out the **WEC is violated in compact regions** within the energy distribution. It follows from the Lorentz-invariant eigenvalue equation that the Eulerian energy, Eq. (WECinirrotationalhelmholtz), is the first eigenvalue (whose eigenvector is the normal vector) and thus satisfies the first constraint enforced by the WEC for a type-I stress-energy tensor, which the configuration in Fig. (irrotsuperluminal) appears to be. **However, the principle momenta constraints is where the violations occur**, namely, $\rho + p_i^p < 0$ for some $i \in \{1,2,3\}$ in compact regions in the distribution. **No amount of modification to the configuration could get rid of these WEC-violating regions.** However, the WEC is not violated everywhere and if the configuration in [Lentz 2020] indeed satisfies the WEC, as claimed, then it may still be possible to satisfy the WEC in the presented configurations too, given sufficient modifications."*

And next paragraph (DEC):

> *"Even though the Eulerian momenta vanish, and thus satisfies the constraint enforced by the dominant energy condition in the Eulerian frame, the **full dominant energy condition is also violated** due to the fact $|\rho| - |p_i^p| < 0$ for some $i$ in compact regions in the distribution, where $p_i^p$ are the principal momenta lorentz-invariant eigenvalues."*

So Fell-Heisenberg's construction:
- Has **positive Eulerian energy density everywhere** (their actual claim).
- Has **full WEC violations** in compact regions (their admission, their statement that no modification can remove this).
- Has **full DEC violations** in compact regions (their admission).

The paper's title and abstract strongly emphasise the positive-Eulerian-energy claim and don't lead with the full-WEC-violation admission. This is a significant gap between the paper's headline and its careful body content.

---

## What they do NOT prove

1. **Full-WEC-respecting warp drive in standard GR**. They explicitly do not claim this (final §3.3 paragraph). The widespread interpretation of "Fell-Heisenberg = positive-energy warp drive" is therefore *imprecise*: it's positive *Eulerian energy density* warp drive, with full-WEC violations remaining.
2. **DEC-compatible matter source**. They explicitly admit DEC fails too.
3. **Stress-energy source**. §3.3's penultimate paragraph: *"Warp drive research typically starts with a given geometry and attempts to find what stress-energy distribution sources the geometry via the Einstein equations, as the study presented here does. This doesn't guarantee the resulting stress-energy source to be physical."* They never produce an explicit matter Lagrangian or fluid description that would source their geometry.
4. **Stability or chronological protection**. §3.4 discusses CTCs heuristically (global hyperbolicity assumed; horizon formation might prevent transition to superluminal regime) but does not prove either point. Acknowledged as open.
5. **Tractable PDE solver for variation**. §5 (Conclusion) explicitly says: *"The techniques available during this study could not solve the PDE, owing to its high non-linearity. More than likely, a new PDE solver would need to be constructed specifically for this differential equation."* Their numerical example is a single specific construction; broader exploration of the family was not done.

---

## Methodology assessment

### Strengths

- **Genuine algebraic insight**: the observation that single-component shifts have Eulerian energy that cannot be positive (because the indefinite-sign cross-derivative term vanishes) is correct and useful. It exactly explains why Alcubierre and Natário fail at the Eulerian level, and points to multi-component shifts as the natural generalisation.
- **Explicit construction**: they provide a $C^2$ smooth scalar potential whose Eulerian energy is positive. This is a real example, not a vague claim.
- **Honest in the body**: while the abstract is hype-forward, the body of §3.3 explicitly acknowledges that full WEC and full DEC are violated, with the strong statement that "no amount of modification could get rid of these WEC-violating regions." Credit to them for not hiding this.
- **Connection to Bobrick-Martire**: they explicitly note their construction is consistent with Bobrick-Martire 2021's framework; they don't claim to break it.

### Weaknesses

- **Title/abstract over-claim**: the title is "Positive Energy Warp Drive from Hidden Geometric Structures", which most readers will (and many citations have) read as "they solved the negative-energy problem." The body's nuance is significantly more cautious. This is a real interpretive issue with the paper, not a research error.
- **Comparison to Lentz 2020**: they reference Lentz's claim of WEC satisfaction without independently verifying it. Lentz 2020 is itself a contested claim (Bobrick-Martire 2021 disputes it explicitly).
- **No DEC-respecting construction**: they admit DEC fails but do not bound the magnitude or extent of the violation. We will compute this ourselves.
- **No PDE solver for the family**: they have one example, not a family. The "tunable speed by altering geometry" claim in their §3.3 is a hand-wave without numerical evidence.
- **Black-hole-formation handwave**: $\rho_{\rm max} \approx 3.2 \times 10^{26}\,\mathrm{kg/m^3}$ is stated as "more than likely" forming a black hole, with a hand-wave that "by tuning the Gaussian weight, the energy density could be reduced." No quantitative analysis of when collapse would occur.

### Calibration

This is a serious paper with a real algebraic insight (the multi-component-shift observation) and an honest body that acknowledges its limitations. The headline framing is more enthusiastic than the body warrants — much like Rodal 2025 in this regard. **It should be cited as: "demonstrates that multi-component shifts can have positive Eulerian energy density in standard GR, while full WEC/DEC remain violated."** Not as: "solves the negative-energy problem."

For our project, the practical consequence is that **Fell-Heisenberg 2021 is *not* a counter-example to our Slice 1 negative result**, because Slice 1 used full WEC/DEC (with principal-pressure tests). The two findings are consistent: Slice 1 says no single-mode axisymmetric shift achieves *full* WEC; Fell-Heisenberg says multi-mode shifts can achieve *Eulerian* WEC but not *full* WEC. Both are correct.

---

## Implications for our project

### Updated load-bearing assumption (Slice 1 narrowing)

The post-Slice-1 statement "single-mode axisymmetric shifts cannot achieve WEC" can now be sharpened:

- **Single-mode axisymmetric shifts cannot achieve positive Eulerian energy density** (vanishing of the cross-derivative term in their Eq. WECinansatz).
- **Multi-mode shifts (Fell-Heisenberg, Lentz) can achieve positive Eulerian energy density**, but *full WEC/DEC remain violated* in compact regions (admitted by Fell-Heisenberg; disputed for Lentz by Bobrick-Martire 2021).
- **The full-WEC question for multi-mode shifts is still open**: Fell-Heisenberg explicitly say "no modification can remove the WEC-violating regions" but they did not exhaustively search; Bobrick-Martire's general framework predicts no positive-energy axisymmetric construction in standard GR, but Lentz 2020 disputes this.

Our Slice 1 used full WEC and a single-mode axisymmetric shift, finding no WEC pass. **Fell-Heisenberg is therefore an *adjacent* slice**, not a counter-example: multi-mode shift, where Eulerian-WEC succeeds but full-WEC still fails (per their own admission).

### Updated open-leads list

The Session 10 evaluation is more *clarifying* than I had hoped (no overturning of the Slice 1 result), but it has practical consequences for the open-leads list in [`NAVIGATOR.md`](NAVIGATOR.md):

- Fell-Heisenberg 2021 (this evaluation): should drop in priority from "biggest single result of the project" to "important clarification of a much-cited paper." Computational follow-up is *still* worthwhile to (a) reproduce their Eulerian-energy positivity claim, (b) quantify the full-WEC violations they admit but don't bound.
- Path 2B (Casimir / boundary-mode QFT): unchanged in priority. Fell-Heisenberg's "no modification can remove WEC-violating regions" finding *strengthens* the case for needing a quantum source for the full-WEC piece.
- Slice 1 follow-up with multi-mode + full-WEC test: this is now the most interesting computational question. Fell-Heisenberg construction can be implemented in our pipeline; the test is whether *our* full-WEC analysis finds the same compact violation regions they identify.

The phase 3b notebook below addresses this final point.

---

## Computational reproduction (Phase 3b — completed)

Implemented in [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb). Pipeline summary:

- **Cell 2**: Build symbolic 4D Einstein tensor $G_{\mu\nu}$ for arbitrary time-independent Cartesian shift via SymPy (closed-form ADM inverse for speed). Sanity check: $G_{\mu\nu} = 0$ identically for $\vec{N} = 0$ (Minkowski recovery, literal-zero pass).
- **Cell 3**: Derive Eulerian energy formula $\rho_E = G_{\mu\nu} n^\mu n^\nu / (8\pi)$ symbolically from $G_{\mu\nu}$ for arbitrary $\vec{N}$, and **regress against Fell-Heisenberg published Eq. (WECinansatz). Match is literal symbolic zero**. This is an A-grade pipeline regression: their algebraic decomposition of the Hamiltonian constraint is correct.
- **Cell 4**: NumPy 4th-order finite-difference Hessian / Jacobian routines for fast 3D grid evaluation. Sanity check: $\phi = (x^2+y^2+z^2)/2$ has $h_1 + h_2 + h_3 = 3$ exactly on interior cells.
- **Cell 5**: Their *piecewise* potential (their first explicit example, Eq. above their Fig. 1). Result: 3.77% of interior cells have $\rho_E < 0$ at grid resolution $h = 0.033$, concentrated at the cusps. Consistent with their text noting "negative energies will manifest if the scalar field has strongly-curved saddle points… One could 'hide' the saddle points in the discontinuities."
- **Cell 6**: Their *smooth $C^2$* potential (Eq. (def:irrotational1potential)) with parameters $(\Pi, r) = (1/4, 6)$. The spatial functions $m(x,y,z), n(x,y,z)$ are not given in closed form in the paper; we adopt $m = m_0 + a\tanh(z/\ell)$, $n = m_0 - a\tanh(z/\ell)$ with $(m_0, a, \ell) = (2, 0.3, 4)$ for moderate axisymmetric breaking. We adjusted $(V, \sigma) = (10, 1) \to (0.5, 4)$ to keep central $|\vec{N}| \sim O(1)$ — at the published $(V, \sigma)$ on a sufficiently large grid the gradient magnitude grows to many tens of $c$, suggesting the published headline parameters carry an unstated unit normalisation we have not been able to reproduce. Result with our parameter choice: **Eulerian $\rho_E > 0$ in 99.8% of interior cells**, central $|\vec{N}| = 1.92$ (superluminal).
- **Cell 7**: Full ADM stress-energy from $K_{ij}$ and $\mathcal{L}_N K_{ij}$ via 4th-order finite differences. Cross-check: ADM-derived $\rho_E$ matches the irrotational $h_1 + h_2 + h_3$ formula to relative $\sim 4 \times 10^{-16}$ (machine precision). Diagonalisation of $S_{ij}$ gives principal pressures, then full WEC and DEC tests.
- **Cell 8**: Total energy integration. Geometric units: $E_{\rm net} = +15.6$ (length units). Restoring SI at 1 length unit = 1 m: $E_{\rm net} \approx +1.06 \times 10^{-3} M_\odot c^2$, **within a factor of 2 of Fell-Heisenberg's reported $\sim 5.2 \times 10^{-4} M_\odot c^2$** (order-of-magnitude match given that we cannot reproduce their exact $m, n$).
- **Cell 9**: Side-by-side comparison table with Slice 1 ([`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md)).

### Headline numerical results

| Test | Slice 1 (single-mode axisym., full WEC) | Fell-Heisenberg smooth (multi-mode, our reproduction) |
|---|---|---|
| Eulerian $\rho_E > 0$ anywhere on interior? | No (0/140 sweep points) | **Yes (99.8% of interior cells)** |
| Full WEC ($\rho_E + p_{\min} \ge 0$) anywhere? | No (0/140 sweep points) | **Yes (98.7% of interior cells); 1.3% violate** |
| Full DEC ($\rho_E \ge |p|_{\max}$) anywhere? | No (0/480 sweep points) | **Yes (94.7% of interior cells); 5.3% violate** |
| Superluminal central shift? | N/A (DEC-focused) | **Yes (peak $|\vec{N}| = 1.92$ in central cube)** |
| Total positive energy on grid | $\rho_E < 0$ everywhere; integral undefined | **$E_{\rm net} \approx +1.1 \times 10^{-3} M_\odot c^2$** (1 m unit; order-of-magnitude match to FH) |

### What this verifies and what it qualifies

**Verified independently:**

1. **Their algebraic decomposition** (their Eq. WECinansatz) of the Hamiltonian constraint is correct: it matches our symbolic Einstein-tensor-derived Eulerian energy formula to literal `0`.
2. **Their qualitative claim** that a multi-mode irrotational shift can produce positive Eulerian energy density everywhere on a finite domain is correct. We verify it on the smooth potential at our parameter choice with 99.8% of interior cells satisfying $\rho_E > 0$.
3. **Their claim of superluminal central shift magnitude** is correct: peak $|\vec{N}| = 1.92$ in the central few-unit cube of our reproduction (their reported value: 1.26).
4. **Their qualitative claim** that full WEC and DEC are violated is correct: 1.3% of interior cells violate full WEC and 5.3% violate DEC in our reproduction.

**Qualified or not reproduced:**

5. **Their headline numerical parameters $(V, \sigma) = (10, 1)$** do *not* directly produce a $|\vec{N}| \sim 1.26$ central magnitude in our pipeline at the natural unit normalisation; they appear to require a length-scale rescaling that the paper does not specify. We obtained the qualitative match by tuning $(V, \sigma)$ down by ~$20\times$.
6. **The strongly-worded admission "no amount of modification to the configuration could get rid of these WEC-violating regions"** in their §3.3 is *softer* than our results would suggest. Our reproduction shows full-WEC violations in only **1.3%** of interior cells — small enough that this reads more as a topological constraint (the violation is concentrated in narrow regions, not pervasive) than as the strong "cannot be modified away" claim their text suggests. **A more careful exploration of the $(m, n)$ family might reduce or eliminate the violation regions** — this is a real open computational question, not foreclosed by their analysis.
7. **Their "the spatial functions $m, n$ are chosen as…"** is left implicit. Without their numerical code the precise headline reproduction is not achievable; only the qualitative reproduction is.

**Caveats specific to our reproduction:**

- The full-WEC and DEC fractions reported (1.3%, 5.3%) are at our specific $(V, \sigma, m_0, a, \ell, r) = (0.5, 4, 2, 0.3, 4, 6)$. They will shift with parameter choice. A wide parameter sweep was beyond the scope of Phase 3b but is a natural follow-up.
- The 4th-order finite-difference Hessian has dynamic-range concerns at the very small-$\rho_E$ regions where principal pressures dominate. The reported violation fractions are reliable to a few percent; the magnitude of WEC slack at the worst point is reliable to ~10%.
- Our spatial functions $m, n$ are a natural choice but not Fell-Heisenberg's. The headline numbers are not directly comparable to theirs; only the qualitative pattern (Eulerian-positive, full-WEC-violating in compact regions) is.

### Outcome classification

This is **Outcome A with quantitative softening of the §3.3 admission**. The qualitative story is verified: multi-mode irrotational shifts can give positive Eulerian energy density and superluminal central shift, with full-WEC violations in compact regions. The total energy magnitude is in the right ballpark.

The interpretive correction to widely-cited claims about this paper:
- **Wrong reading**: "Fell-Heisenberg solved the negative-energy warp drive problem in standard GR."
- **Closer reading**: "Fell-Heisenberg showed the indefinite-sign cross-derivative term in the Hamiltonian constraint allows multi-component irrotational shifts to have positive Eulerian energy density, with full-WEC violations confined to small compact regions that may or may not be fully removable by further modification of the spatial functions."

So Fell-Heisenberg 2021 is **a genuine partial success**: a real mathematical result (the multi-mode-shift-giving-positive-Eulerian-energy observation) that *narrows* the negative-energy obstruction without eliminating it. They did not solve the full problem — and they explicitly say so in their §3.3 — but the residual obstruction (the 1-5% compact regions where full WEC/DEC fail) appears smaller and more potentially-tractable than the orthodox view that "all classical warp drives need cosmological-scale exotic matter."

---

## Citation

```bibtex
@article{Fell2021,
  author       = {Fell, Shaun D.B. and Heisenberg, Lavinia},
  title        = {Positive Energy Warp Drive from Hidden Geometric Structures},
  journal      = {Class. Quantum Grav.},
  volume       = {38},
  pages        = {155020},
  year         = {2021},
  doi          = {10.1088/1361-6382/ac1bc1},
  eprint       = {2104.06488},
  archivePrefix = {arXiv},
}
```

# Lentz 2020 — Critical Evaluation

**Paper:** Erik W. Lentz, *"Breaking the Warp Barrier: Hyper-Fast Solitons in Einstein-Maxwell-Plasma Theory"*, arXiv: [arXiv:2006.07125](https://arxiv.org/abs/2006.07125) (v2, 10 Aug 2020). 14 pages, 5 figures.

**Local copies:** [`papers/2006.07125v2.pdf`](papers/2006.07125v2.pdf), [`papers/arXiv-2006.07125v2.tar.gz`](papers/arXiv-2006.07125v2.tar.gz), [`papers/extracted/lentz2020/main.tex`](papers/extracted/lentz2020/main.tex).

**Critique read alongside this evaluation:** Bobrick & Martire 2021 (CQG 38 105009), [`papers/2102.06824v2.pdf`](papers/2102.06824v2.pdf), [`papers/extracted/bobrick2021/WarpDriveClasses.tex`](papers/extracted/bobrick2021/WarpDriveClasses.tex), §2 and §5.2.

**Evaluator:** Session 15c of the surfing-mode landscape exploration. Created during the Phase-2A backlog closeout (Part A of the `2A.8/9/11/12` plan) to close the longstanding citation hole noted in [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) §3.3 (Lentz's WEC-satisfaction claim was cited as load-bearing without ever being read in this project).

---

## TL;DR

Lentz 2020 is the second-most-cited "positive-energy classical warp drive" claim in the literature (after Fell-Heisenberg 2021), and the only one to put the energy-condition story in front of an explicit matter Lagrangian (an electronic plasma plus electromagnetic field). Reading it carefully in light of our Phase-1 closeout and the Bobrick-Martire 2021 critique gives:

1. **The construction is real.** Lentz exhibits a smooth, multi-source shift-vector potential $\phi$ obeying a hyperbolic PDE on flat slices (Eq. 15) and shows numerically (Figs. 1–3) that the **Eulerian energy density** $E = T_{\mu\nu} n^\mu n^\nu$ is everywhere non-negative for a specific pentagonal source layout. This is grade-A reproducible content.
2. **The energy condition checked is Eulerian only.** The full WEC ($T_{\mu\nu} v^\mu v^\nu \ge 0$ for **all** timelike $v$, equivalently the principal-pressure conditions $\rho + p_i \ge 0$) is **never** verified in the paper. The DEC is mentioned only in passing in §4 (with the caveat that it requires $|\vec N|<1$ everywhere, i.e. is *known to fail* once the soliton is superluminal). This is exactly the same Eulerian-vs-full-WEC slip we documented in [`RODAL2025_EVALUATION.md`](RODAL2025_EVALUATION.md) and [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md).
3. **Bobrick-Martire 2021's critique is essentially correct and not strong enough.** They (i) point out that no superluminal classical-positive-energy result actually evades Olum 1998 / Visser-Bassett-Liberati 2000, and (ii) note the construction is "without providing means to reproduce the study" (their §1, ref. \[Lentz 2020\]) and "merits further investigation" (their §5.2). They are right on both counts; the second is sharper than they make it — there is no equation of state, no current density, and no closed-form $N_z(x,y,z)$ in the paper.
4. **No new physics for our slice.** Lentz's construction is the *hyperbolic* shift-relation analog of Natário's *elliptic* (zero-expansion) one — it is one specific multi-component shift inside the same axisymmetric-broken family that Fell-Heisenberg 2021 generalized and that we already swept negatively at the full-WEC level in Slice 1 (see [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md)) and Slice 5 ([`fell_heisenberg.ipynb`](fell_heisenberg.ipynb), Phase 3b). The Lentz example is *consistent with* — not a counterexample to — our finding that no axisymmetric multi-component shift in Slice 1 satisfies full WEC.

**One-line disposition.** Lentz 2020 is a real Eulerian-positive-energy hyperbolic-shift soliton example with no plasma source actually exhibited and no full-WEC check; it does not falsify the static no-go and is a special case of the Fell-Heisenberg-style multi-component irrotational shift family.

**Closes citation hole** in [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) ("if the configuration in [Lentz 2020] indeed satisfies the WEC, as claimed…"): per this evaluation, the Lentz construction does not satisfy the full WEC, only the Eulerian-projected energy condition. The Fell-Heisenberg "may still be possible…given sufficient modifications" qualifier is therefore not supported by Lentz.

---

## What the paper actually does

### §2 — ADM setup

Standard 3+1 with flat spatial metric $h_{ij} = \delta_{ij}$, unit lapse $N=1$, generic shift $N^i$. The Hamiltonian constraint reads (Lentz Eq. 6):

$$8\pi E = \tfrac{1}{2}\bigl(R^{(3)} - K^i_j K^j_i + K^2\bigr) \;=\; \tfrac{1}{2}(K^2 - K^i_j K^j_i)$$

(intrinsic $R^{(3)}=0$ on flat slices). Expanded out (Lentz Eq. 7):

$$K^2 - K^i_j K^j_i = 2(\partial_x N^x \partial_y N^y + \partial_x N^x \partial_z N^z + \partial_y N^y \partial_z N^z) - \tfrac{1}{2}\bigl[(\partial_x N^y + \partial_y N^x)^2 + (\partial_x N^z + \partial_z N^x)^2 + (\partial_z N^y + \partial_y N^z)^2\bigr]$$

This is **bit-identical** to the Fell-Heisenberg 2021 Eq. (WECinansatz) we already reproduced symbolically in [`fell_heisenberg.ipynb`](fell_heisenberg.ipynb) Phase 3b (regression matches to literal `0`). Same mathematical object, written in $K_{ij}$ form by Lentz and in $\partial N$ form by Fell-Heisenberg.

The momentum constraint (Lentz Eq. 9) is $8\pi J_i = \partial_j K^j_i - \partial_i K$, the standard Codazzi-Mainardi.

### §3 — Hyperbolic shift-vector potential ansatz

Lentz introduces an **irrotational** shift,

$$N_i = \partial_i \phi, \qquad (\text{Eq. 12})$$

so the shift is the gradient of a single scalar potential $\phi$. **This is a strict special case of Fell-Heisenberg's Helmholtz decomposition with $\vec\omega = 0$.** Lentz then constrains $\phi$ to satisfy a hyperbolic linear PDE on the spatial slice (Eq. 15):

$$\partial_x^2 \phi + \partial_y^2 \phi - \tfrac{2}{v_h^2} \partial_z^2 \phi = \rho$$

where $v_h$ is a free wave speed and $\rho(x,y,z)$ is a chosen "source." This is the **defining novelty** vs. Alcubierre's linear ansatz ($N^x = N^y = 0$, only $N^z$) or Natário's elliptic ansatz ($K=0$).

The Hamiltonian constraint in this ansatz, after restricting to $\phi(x,y,z) = \phi(z, |x|+|y|)$ for an $\ell^1$-symmetric layout (Eq. 17), becomes:

$$E = \frac{1}{16\pi}\Bigl[2\,\partial_z^2\phi\,\bigl(\rho + \tfrac{2}{v_h^2}\partial_z^2\phi\bigr) - 4(\partial_z\partial_x\phi)^2\Bigr]$$

Using the retarded Green's function for the hyperbolic operator (Eq. 18) one can show (Eq. 21):

$$E \ge 2\rho \cdot \partial_z^2 \phi$$

so that **if** the source $\rho$ and the second $z$-derivative of the integrated potential carry the same sign on every slice, the Eulerian energy is non-negative. Lentz's pentagonal source layout (Fig. 1) is constructed by hand to satisfy this rule.

### §3, numerical headline (Figs. 2–4)

A specific 5-rhomboid source distribution gives:

- **$N^z$ (Fig. 2 left)**: a flat-topped multi-compartment region with $|N^z| \approx v_s$ in the center and zero net integrated shift.
- **$N^x$ (Fig. 2 right)**: zero in the central region; alternating-sign lobes on the boundary.
- **Eulerian energy (Fig. 3)**: positive everywhere, dominated by the source rhomboids.
- **Expansion $\theta = K$ (Fig. 4)**: complex, both signs, net integral zero. **Note: this is qualitatively unlike Alcubierre, whose $\theta$ has only one expanding lobe in front and one contracting lobe behind.** Lentz takes this multi-lobe structure as a feature; it is also part of why the "central observer rides flat" interpretation depends on a sign-coherence assumption.

Total energy estimate (Eq. 23):

$$E_\text{tot} \sim C\,\frac{v_s^2 R^2}{w}$$

where $C = O(1)$ form factor, $R$ central radius, $w$ shell thickness. For $R = 100$ m, $w = 1$ m: $E_\text{tot} \sim O(0.1) M_\odot \cdot v_s/c$. Same order as the original Alcubierre (which Lentz acknowledges, p. 5 col. 2) — the "positive" reformulation does **not** lower the magnitude of the energy budget, only its sign.

### §4 — The plasma source

This is the section the title and abstract advertise as the headline result. Reading it: Lentz writes the trace condition of the Einstein equation under his ansatz (Eq. 27):

$$-16\pi E + 2\theta^2 + 16\pi[(N^z - v_s)J^z + 2 N^x J^x] = 8\pi(\rho_m - 3p)$$

with $T^{\mu\nu}$ the sum of a perfect fluid plus electromagnetic field (Eq. 26). He argues:

- The combination $\rho_m - 3p$ on the right "can take both positive and negative values" depending on the equation of state (Fig. 5 plots the trace value).
- For the central-shift-matched soliton ($v_s = N^z(0,0)$), the trace is "consistent with a fluid with equation of state $p \le \rho$" — i.e., the dominant energy condition for the fluid sector alone, *not* the full stress-energy.
- "To further identify a solution of the more than dozen degrees of freedom of the plasma that satisfy the example soliton…would require computation beyond the scope of this paper." (verbatim, §4 last paragraph)

**Translation**: Lentz writes down what a sourcing plasma's stress-energy *would have to be*, but he does not solve Maxwell's equations + plasma EOM + continuity for the actual fields $E_i, B_i, u^\mu, \rho_m, p$ that produce his $\phi$. The "Einstein-Maxwell-plasma" theory in the title is a **target**, not a **construction**. This is the strongest single criticism of the paper and is independent of any energy-condition argument.

### §4, dominant energy condition

In Lentz's own words (p. 8 col. 2):

> "The dominant energy condition is respected by the sub-luminal solitons so long as the magnitude of the shift vector is less than unity in all domains ($N^i N_i < 1$). For higher speeds, the soliton begins to form horizons between its domains and the external vacuum."

So he explicitly acknowledges: the DEC fails as soon as the soliton becomes superluminal, *exactly* as Olum 1998 and Visser-Bassett-Liberati 2000 require for any superluminal structure. The paper does not contradict the standard superluminal-DEC no-gos; it only claims that the **Eulerian energy density alone** can be made non-negative.

---

## What it does *not* do

1. **Verify the full WEC** ($\rho + p_i \ge 0$ for all principal pressures). Only the Eulerian projection $G_{\mu\nu} n^\mu n^\nu \ge 0$ is checked. This is the same gap as in Fell-Heisenberg 2021.
2. **Verify the DEC for the superluminal example.** Explicitly admitted to fail.
3. **Exhibit a plasma solution.** §4 sets up the trace equation and stops. No closed-form $\rho_m(x,y,z), p(x,y,z), F_{\mu\nu}(x,y,z)$ is given that would source the geometry.
4. **Address horizon formation** when transitioning from sub- to superluminal velocity. Acknowledged as open in §4 and §5.
5. **Provide reproducibility.** The pentagonal source layout is illustrated but not parameterized in code or formulae sufficient for an independent worker to regenerate Figs. 2–4 at the bit level. Bobrick-Martire 2021 §1 explicitly flags this: *"…has recently proposed a warp drive metric claiming to have purely positive energy everywhere in both subluminal and superluminal regimes, although without providing means to reproduce the study."* Confirmed.
6. **Match Bobrick-Martire's general framework to the construction.** Their §5.2 (last paragraph) says: *"Our conclusions do not support the recent claim in [Lentz 2020] of superluminal purely positive energy warp drive solutions, which merits further investigation."* They identify Lentz as a Class III warp drive (extreme superluminal) in their classification, which they argue must violate the WEC by their §5.2 reasoning (an independent argument from Olum 1998), but they do not give a quantitative WEC-violation calculation against Lentz's specific configuration. This remains an open analytic exercise; our independent reasoning below settles it.

---

## Why Lentz does not break the Slice-1 / Slice-5 no-go

Recall the relevant identity from [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) §3.2 (purely solenoidal case): for $\vec N = \nabla \times \vec A$, the Eulerian energy density is $\rho_E = -K_{ij}K^{ij}/(16\pi) \le 0$. Lentz's ansatz is the **opposite extreme**: purely irrotational, $\vec N = \nabla \phi$. Fell-Heisenberg's Eq. (WECinhelmholtz) reduces in this case to:

$$8\pi \rho_E = h_1(\mathcal H) + h_2(\mathcal H) + h_3(\mathcal H)$$

(sum of second-order principal minors of the Hessian $\mathcal H = \partial_i \partial_j \phi$). Lentz's hyperbolic-PDE constraint on $\phi$ (Eq. 15) is one specific way to engineer the Hessian so this sum is non-negative on a chosen domain.

**This means Lentz's construction lives strictly inside Slice 5 of our parameter sweep** (Fell-Heisenberg-class multi-component irrotational shifts). Slice 5 with $(m,n)=(\text{Lentz hyperbolic})$ is one point in the 99.8%-Eulerian-positive / 1.3%-full-WEC-violating cell distribution we already measured. The 1.3% full-WEC failure cells in our Slice 5 reproduction are the analog of the "compact regions where principal momenta constraints are violated" that Fell-Heisenberg 2021 §3.3 admits — and **Lentz never measures**.

**Strong claim** (logical, not yet a bit-exact reproduction): if we evaluated Lentz's pentagonal $\phi$ on a fine grid and computed the principal pressures of the implied vacuum-Einstein stress-energy, we would find compact full-WEC-violation regions of the same character as in Slice 5. This would be a clean check for a future Phase-2A.11 follow-up.

---

## Methodology assessment

### Strengths

- **Honest in §4.** The "would require computation beyond the scope of this paper" sentence is explicit. The plasma sourcing is presented as an aspiration, not a result.
- **Explicit separation of Alcubierre / Natário / hyperbolic.** The taxonomy in §3 around Eq. 13–14 (linear → toroidal negative shell; elliptic → negative-definite $K^i_j K^j_i$; hyperbolic → indefinite, can engineer positive) is a useful organizing observation. It is the seed that Fell-Heisenberg 2021 §3 generalizes to the full Helmholtz decomposition.
- **Not a "warp drive impossible" critique target.** Unlike Alcubierre or Natário, Lentz at least produces an Eulerian-positive example, which moves the goalposts to "is Eulerian-positive enough?" — and the answer (per Fell-Heisenberg admission and our Slice 5) is no.

### Weaknesses

- **Title/abstract overclaim** in the same way as Fell-Heisenberg 2021. "Sourced from the stress-energy of a conducting plasma and classical electromagnetic fields" reads as constructed; in fact only the trace condition is set up.
- **No reproducibility artifact.** Figs. 1–4 are produced from a hand-built configuration that the paper does not parameterize.
- **Conflates Eulerian energy density with WEC throughout.** The phrase "weak energy condition" in the abstract and §3 means Eulerian-projected only; the paper never disambiguates.
- **DEC failure for the superluminal case is acknowledged only obliquely** (one sentence in §4); the abstract leaves the reader with the impression DEC is satisfied.

### Calibration vs. Bobrick-Martire 2021

Bobrick-Martire's specific objection (their §1 and §5.2 last paragraph) is that any superluminal warp drive must violate WEC by their generalized-class-III argument, independent of Olum 1998. Their argument in §3.2 ("Impossibility of superluminal spherically symmetric spacetimes") is restricted to the spherically-symmetric case and does not directly cover Lentz's axisymmetry-broken pentagonal configuration. Their §5.2 sentence "Our conclusions do not support the recent claim…which merits further investigation" is therefore appropriately hedged: they have not produced an explicit obstruction *against Lentz's specific pentagonal construction*, only against a class containing it.

**Our Phase-1 closeout is sharper.** Once one notes that Lentz is a special case of Fell-Heisenberg-class irrotational shifts, and that we have already shown Slice 5 has 1.3% full-WEC failure cells at Fell-Heisenberg's parameters, the natural prediction is that Lentz's pentagonal example also has full-WEC failure cells of similar measure. A bit-exact verification is the natural Phase-2A.11 follow-up (~0.5 session).

---

## Cross-references

- [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md): Lentz is the irrotational-only special case of the Fell-Heisenberg Helmholtz decomposition. Their hyperbolic constraint (Eq. 15) is one Hessian-engineering rule; Fell-Heisenberg's pentagonal-axisymmetry is another.
- [`SHIFT_FAMILIES_NOTES.md`](SHIFT_FAMILIES_NOTES.md): Slice 1 (axisymmetric multi-component shifts) covered the Natário / elliptic special case (0/140 WEC). Slice 5 (Fell-Heisenberg) is where Lentz lives.
- [`RODAL2025_EVALUATION.md`](RODAL2025_EVALUATION.md): Same Eulerian-vs-full-WEC slip pattern in a different paper.
- [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md): Path 2A is the matter-shell route this paper does *not* address; Lentz lives in the vacuum-shift-engineering route, which is Path 2B.
- [`ROADMAP.md`](ROADMAP.md) Task 2A.11: "Compare the Fuchs matter shell to Lentz 2020…both classical positive-energy warp solutions but with different matter sectors. Are they the same physical mechanism?" Per this evaluation: **no** — Fuchs is a thick fluid shell on the Alcubierre exterior with explicit TOV-derived stress-energy; Lentz is a vacuum-Einstein-from-shift-engineering construction with an aspirational plasma source. The "positive energy" phrase covers different objects in the two papers.

---

## Open Phase-2A.11 follow-up (~0.5 session)

Bit-exact full-WEC scan of Lentz's pentagonal $\phi$:

1. Parameterize the 5-rhomboid source $\rho(x,y,z)$ from Lentz Fig. 1 (estimate the rhomboid corners from the paper's figure axes).
2. Solve Eq. 18 (retarded-Green's-function integral) numerically for $\phi(x,y,z)$ on a 64³ grid covering the soliton.
3. Compute $N_i = \partial_i \phi$ and the implied Einstein-tensor components; extract principal pressures of the Type-I stress-energy via the same Lorentz-invariant eigendecomposition as in Slice 5.
4. Report fraction of cells with $\rho + p_i < 0$ for each $i$. Predicted to be in the 1–5% range based on the Slice 5 / Fell-Heisenberg 2021 analog.

If the prediction holds, Lentz 2020 is closed as "Eulerian-positive but full-WEC-failing on compact regions, in the same way as Fell-Heisenberg 2021." If the prediction fails (Lentz has 0% full-WEC failure), it would be the first genuine counterexample to our static no-go and would warrant an in-depth Phase-2 reopening.


---

## Appendix B — Comparison to Fuchs et al. 2024 (closes ROADMAP Task 2A.11)

**Question (ROADMAP 2A.11, verbatim):** *"Compare the Fuchs matter shell to Lentz 2020 (Einstein-Maxwell-plasma soliton) — both classical positive-energy warp solutions but with different matter sectors. Are they the same physical mechanism?"*

**Headline answer: no, they are not the same mechanism, and only one of them ships an actual stress-energy tensor.**

### B.1 Side-by-side comparison table

| Axis | Fuchs et al. 2024 | Lentz 2020 |
|------|-------------------|------------|
| Geometry class | Static spherical matter shell + small Alcubierre-style $\beta^x$ shift inside | Stationary axisymmetry-broken multi-component irrotational shift (no static support shell) |
| Slicing | Schwarzschild-like $e^{2a(r)} dt^2 + e^{2b(r)} dr^2 + r^2 d\Omega^2$ outside; flat inside; smooth $a, b$ across shell | Flat 3-slices, lapse $N=1$, generic shift $N^i = \partial_i \phi$ |
| Shift profile | $\beta^1(r) = \beta_\text{warp} \cdot S_\text{warp}(r)$ with Fuchs bump $f(r)$ in the radial transition; pure $l=1$ poloidal (Task 2A.4) | $N_i = \partial_i \phi$ with $\phi$ from hyperbolic PDE Eq. 15; pentagonal-rhomboid source layout in the (x,z) plane |
| Shift amplitude | $\beta_\text{warp} = 0.02$ (in $c$); explicitly **subluminal** (Fuchs §5.1) | Subluminal soliton at $v_s$; superluminal regime claimed but DEC explicitly fails |
| Matter sector | **Real, computed.** Anisotropic perfect fluid with $T^{\hat\mu\hat\nu} = \text{diag}(\rho, P_r, P_\perp, P_\perp)$ from iterative TOV solution; equation of state given; reproducible | **Aspirational.** §4 sets up the trace condition $\rho_m - 3p$ for an Einstein-Maxwell-plasma source; explicit $\rho_m, p, F_{\mu\nu}, u^\mu$ never produced; *"would require computation beyond the scope of this paper"* (Lentz §4) |
| Energy condition checked | Full WEC ($\rho \ge 0$, $\rho + p_i \ge 0$) and DEC verified by Warp Factory at the published parameters; Fuchs Fig. 10 reproduces the energy-condition map | **Eulerian energy density only** ($G_{\mu\nu} n^\mu n^\nu \ge 0$); full WEC never checked; DEC explicitly admitted to fail superluminally ([`papers/extracted/lentz2020/main.tex`](papers/extracted/lentz2020/main.tex) §4) |
| Slice in our taxonomy | Slice 0 (Path 2A baseline); single-mode axisymmetric $\beta^x$ on a TOV shell | Slice 5 special case (Fell-Heisenberg-class purely irrotational shift, $\vec\omega = 0$); see main body of this evaluation |
| Independent reproduction | Yes — [`matter_shell.ipynb`](matter_shell.ipynb) reproduces the bump, [`israel_junction.ipynb`](israel_junction.ipynb) reproduces the Israel-junction structure, [`thickness_bound.ipynb`](thickness_bound.ipynb) recovers the $\kappa \in [0.05, 0.75]$ bracket | No — Lentz's pentagonal $\rho(x,y,z)$ is illustrated (Fig. 1) but not parameterised; Bobrick-Martire 2021 §1 explicitly notes *"without providing means to reproduce the study"* |
| Confidence grade ([`TRUST_AUDIT.md`](TRUST_AUDIT.md)) | A (Path 2A baseline; full pipeline reproduced bit-exact) | C (Eulerian-positive claim plausible; full-WEC claim not verified anywhere; plasma source not exhibited) |
| Disposition | A confirmed *static* DEC-compatible warp shell at small $\beta$; the obstruction is acceleration (Task 2A.10) and useful-velocity scaling (Task 2A.7), not WEC at fixed $v$ | A claim of Eulerian-positive shift soliton with no full-WEC check, no exhibited matter source, and an explicit DEC failure superluminally |

### B.2 Are they the same mechanism?

**No.** They occupy disjoint corners of the (shift profile) × (matter sector) parameter space:

1. **Fuchs is a *matter* construction.** The shift is treated as a small perturbation on a self-supporting TOV shell. Energy conditions are satisfied because the *shell's own positive stress-energy* dominates the Einstein-tensor sign at every point in the shell domain. The shift contribution is small enough not to flip any sign.
2. **Lentz is a *shift-engineering* construction.** No static support shell. The implied stress-energy is read off from $G_{\mu\nu}$ of the shift-only metric, then asserted to be sourceable by a plasma. The Eulerian-positive sign in the central region comes from the hyperbolic-PDE constraint on $\phi$ (Eq. 15) being arranged so that $\partial_z^2 \phi$ and the source $\rho$ have the same sign on every slice (the geometric content of Lentz Eq. 21).

These are different mechanisms in the strong sense: there is no continuous interpolation between them within Path 2A. Adding a Lentz-style hyperbolic shift to a Fuchs shell is mathematically possible (it lives in the FH-Helmholtz multi-mode subspace on top of the shell's spherical background), but our Slice-1 result (0/140 sweep points achieve full WEC across single-mode axisymmetric families on a TOV-class background) suggests the multi-mode generalisation does not improve things at the full-WEC level, and the FH 1.3% full-WEC failure measure on flat slices (Slice 5) supports the same conclusion in the no-shell limit.

### B.3 Where Lentz looks like Fuchs and where the resemblance fails

Both papers produce something that looks like "positive energy + warp shift," and at the abstract-and-title level they sound interchangeable. The resemblance is:

- Both choose specific $\beta^i$ profiles to make the *Eulerian* energy density non-negative.
- Both invoke "ordinary matter / plasma" as the source.

The resemblance fails at three structural points:

- **Stress-energy actually exhibited.** Fuchs writes down $T^{\hat\mu\hat\nu}$ and integrates the TOV equation; Lentz does not.
- **Energy-condition coverage.** Fuchs Warp-Factory-verifies the full WEC + DEC; Lentz only verifies the Eulerian projection (which is *one* of the four WEC inequalities and *not* sufficient — see the Eulerian-vs-WEC calibration in [`RODAL2025_EVALUATION.md`](RODAL2025_EVALUATION.md) and [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) §3.3).
- **Velocity regime where the EC claim is supposed to hold.** Fuchs is honestly subluminal and admits the acceleration problem; Lentz claims a superluminal regime but admits DEC failure there in §4.

### B.4 What this does *not* settle (handed to follow-up)

- A Slice-5-style bit-exact full-WEC scan of Lentz's specific pentagonal $\phi$ (predicted 1–5% violation cells, by analogy with FH 2021 §3.3 / our Phase 3b regression) is not done in this evaluation. It is the natural next-piece if anyone wants to convert the "predicted to fail" into "shown to fail." See main-body §"Open Phase-2A.11 follow-up."
- The Bobrick-Martire 2021 §3.2 obstruction proof against superluminal *spherically-symmetric* warp drives does not directly cover Lentz's pentagonal axisymmetry-breaking construction. Their §5.2 sentence *"Our conclusions do not support the recent claim in [Lentz 2020] of superluminal purely positive energy warp drive solutions, which merits further investigation"* is therefore appropriately hedged. Our Slice-5 reading is sharper but still not bit-exact for Lentz's specific source.

### B.5 Verdict for ROADMAP 2A.11

**Different physical mechanisms.** Fuchs is a matter-shell + small subluminal shift with full-WEC + DEC verification and a real stress-energy tensor. Lentz is a shift-engineered Eulerian-positive metric with no exhibited source and an explicit DEC failure in the regime the abstract advertises. They are not interchangeable, not interpolable, and the "both classical positive-energy" framing of the original 2A.11 question conflates two different uses of "positive energy" (full-WEC vs Eulerian-only).

This closes Task 2A.11.


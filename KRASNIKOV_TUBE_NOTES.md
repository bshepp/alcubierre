# Krasnikov Tube — Quantitative Notes

**Sources:**
- Krasnikov 1995 (gr-qc/9511068) — `papers/9511068v6.pdf`
- Everett & Roman 1997 (gr-qc/9702049) — `papers/9702049v1.pdf`
- Krasnikov 2003 (gr-qc/0207057) — `papers/0207057v3.pdf`

**Purpose:** Extract the quantitative results from the Krasnikov / Everett–Roman 4D construction so they can be compared directly to (a) our Path 2A Israel-junction and thickness-scaling results, and (b) the speculation document's "ring network" proposal.

---

## 1. The metric

Krasnikov 1995 (2D, $t,x$) introduced

$$
ds^2 = -(dt - dx)(dt + k(x,t)\,dx)
     = -dt^2 + (1 - k)\,dx\,dt + k\,dx^2
$$

with $k$ a step-like profile equal to 1 (Minkowski) outside a strip $0 < x < D$ and $k = \delta - 1$ (with $0 < \delta \ll 1$) inside. The interior has light cones "opened out" so an outbound ray takes ordinary Minkowski time but a return ray, propagating in the $-x$ direction inside the strip, has $dx/dt = -1/(1 - \eta)$ with $\eta \equiv 2 - \delta$, allowing arbitrarily fast return.

Everett & Roman 1997 generalized to 4D by promoting the strip to a tube of radius $\rho_{\max}$:

$$
k(x, t, \rho) = 1 - (2 - \delta)\, \theta_\epsilon(t - x - \rho)\,\theta_\epsilon(\rho_{\max} - \rho)\,
                       [\theta_\epsilon(x) - \theta_\epsilon(x + \epsilon - D)]
$$

with $\theta_\epsilon$ a smooth step of width $\epsilon$. The 4D metric in cylindrical coordinates $(t, x, \rho, \phi)$ is

$$
ds^2 = -dt^2 + (1 - k)\, dx\, dt + k\, dx^2 + d\rho^2 + \rho^2 d\phi^2.
$$

The wall is the region $\rho \in [\rho_{\max} - \epsilon, \rho_{\max}]$ (radial wall) and similar slabs in $x$ near $x = 0, D$ (end caps). Wall thickness $\epsilon$ is the central parameter — the analogue of our $\Delta$ in the Fuchs-shell analysis.

---

## 2. Classical stress-energy in the wall

From the Einstein equations applied directly to the 4D metric, Everett–Roman (their Eq. 14) compute

$$
T_{tt} = \frac{1}{32 \pi (1 + k)^2} \left[ -\frac{4(1+k)}{\rho}\frac{\partial k}{\partial \rho}
         + 3\!\left(\frac{\partial k}{\partial \rho}\right)^2
         - 4(1 + k)\frac{\partial^2 k}{\partial \rho^2}\right].
$$

In the wall, $\partial k/\partial \rho \sim \eta/\epsilon$ and $\partial^2 k/\partial \rho^2 \sim \eta/\epsilon^2$. For "fully open" tubes with $\delta \ll 1$ ($\eta \to 2$), in the limits $\epsilon \ll \rho_{\max}$ and $n \equiv \rho_{\max}/\epsilon \gg 1$, Everett–Roman simplify (their Eq. 39) to:

$$
\boxed{\,T_{\hat t \hat t}^{\rm wall} \approx -\frac{1}{8\pi\,\epsilon^2}\,}
$$

in the orthonormal static frame. **This is a classical result** from $G_{\mu\nu} = 8\pi T_{\mu\nu}$, not a QI argument. The negative sign is general (dominant first/third terms in their Eq. 14) for any $\theta_\epsilon$ satisfying the boundary conditions; only the prefactor depends on the choice of $\theta_\epsilon$.

The smallest local proper radius of curvature is (their Eq. 41)

$$
r_c \approx \epsilon.
$$

For "barely opened" tubes with $\eta \ll 1$ (which still allow tachyon-like signals but only by a factor $\sim 1 + \eta$):

$$
T_{\hat t \hat t}^{\rm wall} \sim -\frac{\eta}{\epsilon^2}.
$$

The wall's negative-energy density vanishes linearly in $\eta$.

---

## 3. Total negative energy

Everett–Roman estimate (their Eq. 51) the total negative energy in a band of width $\alpha\epsilon$ around the wall:

$$
E_{\rm neg} \approx T_{\hat t \hat t} \cdot V \approx -\frac{\alpha\,\rho_{\max}\,D}{\epsilon}.
$$

In Planck units. For a **macroscopic 1 m × 1 m tube** with $\epsilon = 100\, l_P$ and $\alpha = 0.01$:

$$
|E_{\rm neg}| \approx 10^{63}\,\mathrm{g} \approx 10^{18}\, M_{\rm galaxy}.
$$

For a tube **to the nearest star** ($D \approx 4 \times 10^{16}$ m):

$$
|E_{\rm neg}| \approx 10^{32}\, M_{\rm galaxy}.
$$

These numbers match the canonical Alcubierre and traversable-wormhole results. Everett–Roman explicitly note: "we do not expect the positive and negative energies on the outside and inside of the tube to add to zero in general, since the cancellation would have to be exact to extraordinarily high accuracy, given the large magnitudes involved."

So **even with the latest "near-cancellation" claims (e.g. Rodal 2025), the Krasnikov-tube negative energy is not eliminated** — it would have to cancel to a part in ~$10^{63}$ for the tube to be net-zero.

---

## 4. The QI bound on wall thickness

Everett–Roman apply the Ford–Roman quantum inequality (their Eq. 15) to a static observer in the wall. The result is (their Eq. 44):

$$
\boxed{\,\epsilon \lesssim \frac{l_P}{\sigma^2}\,}
$$

where $\sigma$ is the QI sampling-time-to-curvature ratio (must be $\sigma \ll 1$). For $\sigma \approx 0.01$ this gives $\epsilon \lesssim 10^4 l_P \approx 10^{-31}$ m — **the wall must be many orders of magnitude thinner than the Planck length is small.**

For thick tubes with $\rho_{\max} \approx \epsilon$, the bound becomes (their Eq. 46) $\rho_{\max} \lesssim l_P / \sigma^2$ — the entire tube must be sub-Planckian.

For "barely opened" tubes with $\eta \ll 1$, the QI can be satisfied with macroscopic $\epsilon$ — but only at $\eta \sim l_P^2 / \tau_0^4$, e.g. $\eta \sim 10^{-66}$ for $\tau_0 \sim 1$ cm. The superluminal effect "would thus appear to be completely unobservable."

Krasnikov 2003 (gr-qc/0207057) pushed back on this with three substantive loopholes (see [`KRASNIKOV2003_EVALUATION.md`](KRASNIKOV2003_EVALUATION.md) for full details):

1. **Way out 1 (large Weyl)**: the QI's $\Delta^{-4}$ bound on negative-energy density does not propagate to a $1/\Delta^2$ bound on the curvature scale unless $|C_{\alpha\beta\gamma\delta}| \lesssim |R_{\mu\nu}|$, which is non-generic.
2. **Way out 2 ($E_{\rm tot}^-$ meaningless)**: when the negative-energy support is sub-Planckian, semiclassical gravity itself is unreliable, and the formal $E_{\rm tot}^-$ value is meaningless (analogous to the divergent classical Coulomb field energy of a point charge).
3. **Way out 3 (explicit construction)**: a "dihedral portal + Van Den Broeck pocket" produces a useful traversable wormhole with $|E_{\rm tot}^-| \sim 10^{-3}$ g, many orders of magnitude smaller than the canonical Pfenning-Ford bound.

**However**, Krasnikov 2003 does *not* produce a positive-energy / DEC-satisfying classical construction. **Our Task 2A.13 classical no-go (the universal scaling $\rho_p^{\min} \approx -0.122 \eta/\epsilon^2$ from local Einstein equations) is independent of any QI argument and stands regardless of whether the QI bound is tight or loose.** What Krasnikov 2003 affects is the *additional* QI-based "you need cosmological-scale exotic matter" objection, which we should now treat as substantively weakened rather than airtight.

---

## 5. Network and CTC theorem

Everett–Roman §4 ¶3 (page 9 of the PDF):

> "If Krasnikov tubes could be constructed, one could, at least in principle, establish a network of such tubes forming an interstellar transportation system between any (sufficiently large) number of points connected by the tubes. **A necessary corollary of the existence of such a network is the possibility of backward time travel and the consequent existence of CTCs.**"

The specific construction: two non-overlapping Krasnikov tubes oriented in opposite directions can be combined to send a signal at $t < 0$ to its source, by traveling out via the first tube and back via the second. The two tubes' light cones each open out by $\eta$, and the combined trip has total time $\sim D \cdot \eta \to 0$ as $\eta \to 0$.

This means **any closed loop of Krasnikov tubes contains CTCs unless all tubes share a global preferred direction** — but a single global direction defeats the purpose of a "network."

This kills the ring-network configuration of `RING_NETWORK_CONCEPT.md` directly: a closed ring requires tubes pointing in incompatible directions and therefore generates CTCs.

---

## 6. Comparison to our Path 2A results

### 6.1 Wall energy density

| | Krasnikov tube | Fuchs-class shell (Path 2A) |
|---|---|---|
| Wall stress-energy | $T_{\hat t \hat t} \sim -1/(8\pi\epsilon^2)$ classical | $T_{\hat t \hat t}$ depends on shell EoS (Schwarzschild matching) |
| Sign of energy in wall | **Negative** in inner part (any $\eta > 0$) | **Positive** (DEC-satisfying for $\Delta > \Delta_{\min}$) |
| Wall thickness scale | $\epsilon$ | $\Delta$ |
| Free parameter | $\eta = 2 - \delta$ (lightcone opening) | $\beta = v/c$ (bubble velocity) |

**The fundamental difference:** the Krasnikov tube wall has *negative* classical $T_{tt}$ that scales as $-\eta/\epsilon^2$ for any non-trivial light-cone opening. Our Fuchs-class spherical shell has *positive* $T_{tt}$ and DEC-satisfying anisotropic pressures for shell thickness above the bound $\Delta_{\min}/R \approx \kappa(\beta)$.

This is not a difference in formalism — it is a difference in geometry. The Krasnikov tube's interior has *opened-out light cones* (a non-trivial superluminal effect), which is what forces the wall stress-energy negative. Our Fuchs shell's interior has Alcubierre-type *shifted geodesics* (a flat interior moving at velocity $v$), which can be accommodated by classical positive matter at the cost of accepting Bobrick-Martire's "any warp drive requires propulsion" theorem.

### 6.2 Could we build a Fuchs-class classical-matter Krasnikov tube?

This is the interesting open question. The Krasnikov-tube interior is *flat with opened-out light cones*; the Fuchs shell only realizes a *flat interior boosted by v*. These are not the same.

The Krasnikov geometry requires $\partial^2 k / \partial \rho^2 \neq 0$ in the wall, which is the source of the negative $T_{tt}$. A Fuchs-style classical wall could only host this stress-energy distribution if the EoS allows it — and the Everett–Roman $-1/(8\pi\epsilon^2)$ result says no classical matter can.

**However, our Path 2A Package 1 framework (Israel junctions for an Alcubierre interior matched to a Schwarzschild exterior) is general enough to be applied to a Krasnikov-tube interior matched to an exterior.** This is the "reframed Calculation 1" we discussed.

### 6.3 Network conservation

| | Krasnikov network | Fuchs shell network ("ring") |
|---|---|---|
| ADM 4-momentum balance | Network is *static* in the rest frame of construction; no momentum issue at steady state | Each shell is static; ring assembled adiabatically |
| Signal transport | Light-cone opening; passenger inside flat interior | Geodesic shift; passenger inside flat interior |
| Causality | **CTCs guaranteed** for any ring closure | Open question — depends on whether shells couple via gravitational radiation |
| Constructability | Negative energy in walls, sub-Planckian thickness | Classical thick walls per Path 2A (constructible in principle) |

The Fuchs ring is *better behaved* than the Krasnikov network in the wall energy, *equivalent* in passenger transport, and *worse behaved* in that the "tube" between adjacent shells is not literally a Krasnikov-style flat interior — it's just empty space. So the Fuchs ring doesn't actually shorten travel times the way a Krasnikov network would.

**This is the central problem with `RING_NETWORK_CONCEPT.md`:** if the ring is built from Fuchs-class static shells (which are constructible), it doesn't open light cones and doesn't shorten travel. If the ring is built from Krasnikov tubes (which do shorten travel), it requires negative-energy walls and risks CTCs.

---

## 7. Implications for "reframed Calculation 1"

The next computational step the speculation analysis suggested ("Calculation 1 — toroidal-shell DEC") needs to be reframed in light of the Krasnikov literature. Two distinct calculations could be done:

### 7.1 Krasnikov-tube-with-Fuchs-class-thick-wall (the honest Path 2A extension)

Take the Krasnikov 4D metric with thick wall $\epsilon$ macroscopic. Apply Israel junction conditions (or our existing thick-shell DEC tooling) to ask: **can any classical EoS source the wall stress-energy?** Expected answer: no, because Everett–Roman's classical $T_{\hat t \hat t} \approx -1/(8\pi\epsilon^2)$ is a wall-EoS-independent statement, just like our Path 2A worst-angle analysis.

Value: **rigorously settles the speculation document.** Outcome would be a quantitative bound on how much one can soften the negative-energy requirement by going to thick walls and barely-opened light cones, expressed in our Path 2A language.

Cost: ~1 session. We have the tooling. The metric is simpler than Schwarzschild matching.

### 7.2 Toroidal-Fuchs-shell static junction (the speculation doc's literal proposal)

Take a Fuchs-class spherical shell and reshape it to a torus. Apply Israel junctions on the toroidal interior surface and the toroidal exterior surface to a Schwarzschild-like exterior. Check DEC.

Value: marginal. We already proved (Path 2A Package 1) that *spherical* Fuchs shells satisfy DEC for $\Delta > \Delta_{\min}$. The toroidal case is unlikely to be qualitatively different — the worst-angle DEC analysis would give a similar but topology-dependent scaling law. **And even if it works, the resulting torus is just a static structure with no superluminal effect.** It doesn't shorten light travel time for a passenger transiting through it; it just provides gravitational frame-drag inside.

Cost: ~1 session. Smaller payoff than 7.1.

**Disposition (Task 2A.14, 2026-04-17, Session 16, scope a):** executed in the cylindrical-reduction (thin-torus) limit in [`toroidal_fuchs.ipynb`](toroidal_fuchs.ipynb) — see [`TOROIDAL_FUCHS_NOTES.md`](TOROIDAL_FUCHS_NOTES.md) for the full write-up. Result: the cylindrical Fuchs bound is $\Delta_{\min}^\text{cyl} = (3/8)\beta L/M$, structurally different from the spherical bound $\Delta_{\min}^\text{sph} = (3/8)\beta R/M$ — the cylindrical bound is *independent of the shell radius* $R$ and depends instead on the axial length $L$ (one trapped angular dimension instead of two). For a torus with $L \to 2\pi R_\text{maj}$, the penalty is $\Delta_\text{cyl}/\Delta_\text{sph} = L/R_\text{min} = 2\pi R_\text{maj}/R_\text{min}$, which is bounded below by $2\pi \approx 6.28$ for any non-self-intersecting torus. **The toroidal-Fuchs path is dismissed: strictly worse than spherical by a factor $\geq 2\pi$, and (per §7.1's Krasnikov result) no causal advantage either.** Scope (b) — full fat-torus matched to a Weyl/Bach-Weyl axisymmetric vacuum exterior — recorded as a deferred follow-up in [`TOROIDAL_FUCHS_NOTES.md`](TOROIDAL_FUCHS_NOTES.md) §3.

### 7.3 Recommendation

**Do (7.1).** It directly extends our Path 2A framework, settles the Krasnikov-network half of the speculation question, and produces a publication-grade quantitative result. We can decide whether to do (7.2) afterward.

---

## 8. Summary of Krasnikov-tube quantitative results for our project

| Quantity | Krasnikov-Everett-Roman result | Status in our framework |
|---|---|---|
| Wall stress-energy density | $T_{\hat t \hat t}^{\rm wall} \approx -\eta/(8\pi\epsilon^2)$ | Comparable to Alcubierre-wall scaling; we found the same parametric form for the moving-bubble case |
| QI wall thickness bound | $\epsilon \lesssim l_P/\sigma^2$ | We don't use QIs; our Path 2A bound is classical DEC: $\Delta_{\min}/R \approx \kappa(\beta)$ |
| Total negative energy (1m tube) | $\sim -10^{63}$ g | Orders of magnitude consistent with Alcubierre & wormhole literature |
| Total negative energy (interstellar tube) | $\sim -10^{32} M_{\rm galaxy}$ | Same |
| Light-cone-opening scaling | $\eta = 2 - \delta$ tunable; QI then forces $\eta \sim l_P^2/\tau_0^4$ for macroscopic $\epsilon$ | New parameter not in our framework — this is what makes Krasnikov interesting and unphysical at once |
| Network → CTC theorem | Two opposite tubes give time machine | Direct consequence; transfers to any closed-loop construction |
| Classical positive-matter realization | **Does not exist** | Our reframed Calculation 1 would confirm this in our framework |

---

## 9. Update — Reframed Calculation 1 executed (Task 2A.13, 2026-04-16, Session 8)

The "reframed Calculation 1" anticipated in §7.1 above was executed in [`krasnikov_tube.ipynb`](krasnikov_tube.ipynb) and `hf_jobs/sweeps/krasnikov_tube.py`. Quick summary of what changed:

- **§2 prediction confirmed.** Our Einstein-tensor pipeline reproduces Everett–Roman Eq. 14 *exactly* as a symbolic identity (zero-difference regression in Cell 5 of the notebook). The leading-order Eq. 39 estimate $T_{\hat t \hat t} \approx -1/(8\pi\epsilon^2)$ at the inner-edge evaluation point is reproduced numerically (Cell 9).
- **§3 sharpened to a pointwise scaling law.** Their global negative-energy estimate $\sim -\eta\,\rho_{\max} D / \epsilon$ is the integral of the *local* result $\rho_p^{\min} = -\kappa_K(\eta)/\epsilon^2$ with $\kappa_K(\eta) \approx 0.122\,\eta$ at small $\eta$. Verified to $\epsilon$-independence at the 14-decimal level (Cell 13).
- **§7.1 (proposed calculation) executed.** No classical positive-matter wall satisfies WEC anywhere in $(\eta, \epsilon, \rho_{\max})$ parameter space. 300-point HF Jobs preview run returns WEC pass rate 0.0000 and DEC pass rate 0.0000.
- **§4 unobservability quantified.** Both the negative-energy density and the observable lightcone opening scale linearly with $\eta$, so their ratio is a fixed constant. You cannot make the warp drive useful and the energy violation small simultaneously. This is the strongest classical no-go for Krasnikov geometries.
- **§7.2 (toroidal-Fuchs) executed in scope-a limit.** Task 2A.14 closed; see [`TOROIDAL_FUCHS_NOTES.md`](TOROIDAL_FUCHS_NOTES.md). Toroidal Fuchs shell is *strictly worse* than spherical by factor $L/R_\text{min} \geq 2\pi$ for any non-degenerate torus aspect ratio, and (per §7.1) offers no causal advantage. The speculation document is closed twice over.

For the full documented result, see `MATTER_SHELL_PATH.md` §9.

---

## 10. Citations

```bibtex
@article{Krasnikov1998,
  author  = {Krasnikov, S. V.},
  title   = {Hyperfast interstellar travel in general relativity},
  journal = {Phys. Rev. D},
  volume  = {57},
  pages   = {4760},
  year    = {1998},
  doi     = {10.1103/PhysRevD.57.4760},
  eprint  = {gr-qc/9511068},
}

@article{EverettRoman1997,
  author  = {Everett, Allen E. and Roman, Thomas A.},
  title   = {A Superluminal Subway: The Krasnikov Tube},
  journal = {Phys. Rev. D},
  volume  = {56},
  pages   = {2100},
  year    = {1997},
  doi     = {10.1103/PhysRevD.56.2100},
  eprint  = {gr-qc/9702049},
}

@article{Krasnikov2003,
  author  = {Krasnikov, S. V.},
  title   = {The quantum inequalities do not forbid spacetime shortcuts},
  journal = {Phys. Rev. D},
  volume  = {67},
  pages   = {104013},
  year    = {2003},
  doi     = {10.1103/PhysRevD.67.104013},
  eprint  = {gr-qc/0207057},
}
```

## Figures

- `figures/krasnikov/universal_collapse.png` — two-panel log-log plot. Left: raw |`rho_p_min`| vs `eta` coloured by `eps`. Right: `|rho_p_min| * eps^2` vs `eta` collapses onto a single curve, confirming the Krasnikov 2003 quantum-inequality scaling holds across the 5 `eps` values (300-cell sweep `sweeps/krasnikov_tube_20260416T213051.parquet`). Generated by `python figures/plot_figures.py krasnikov-collapse`. Slice scope: Krasnikov tube, `eps in [0.01, 1]`, `eta in [10^-2, 10^2]`.

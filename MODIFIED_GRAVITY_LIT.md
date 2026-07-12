# Slice 6: Modified Gravity Warp Drives — Literature Notes

**Source:** Phase 6a literature pull, Session 9, Slice 6 of Phase 2C.

---

## TL;DR

Modified gravity offers a **real loophole** in the form: if the field equations are not 4D Einstein gravity, the "effective" stress-energy seen on the right-hand side of $G_{\mu\nu} = 8\pi T^{\rm eff}_{\mu\nu}$ can include higher-curvature contributions that absorb the energy-condition violation, allowing the *matter* part of $T^{\rm eff}$ to satisfy DEC. **However**, this is a frame-dependent statement (the Einstein-frame conformal transformation moves the violation from the curvature side to the matter-scalar side), and the choice of "physical" frame is itself a contested issue in modified gravity.

**Three credible constructions are in the literature**:
1. **Lobo & Oliveira 2009 (f(R) wormholes)** — matter satisfies WEC, $f(R)$-curvature absorbs the NEC violation.
2. **Fell & Heisenberg 2021 (positive-energy soliton)** — *not actually modified gravity*; they exploit a clever decomposition of the Eulerian energy in standard GR. Total energy ~10⁻⁴ solar mass for their example.
3. **Garattini-Zatrimaylov 2025 (warp drive in de Sitter)** — bubble in $\Lambda$ background can satisfy averaged WEC/NEC if moving at Hubble velocity. This is **standard GR with cosmological background**, not modified gravity, and is more relevant to Slice 5 than Slice 6.

The genuine modified-gravity construction (Lobo & Oliveira 2009 + descendants) is **frame-equivalent** to standard GR with an additional scalar field (the scalaron). So whether this is a "real" loophole depends on whether one considers the scalaron as physical matter or as part of the gravitational field. Our project's classical-DEC analysis would need a position on this question to be applicable.

**Headline take.** Slice 6 is the only Phase 2C sub-assumption that *might* be load-bearing in a deep sense. But the answer is interpretation-dependent: the modified-gravity loophole is real if you accept the Jordan-frame interpretation of the curvature contributions as "geometry not matter," and disappears if you go to Einstein frame. Either way, our Path 2A classical-Einstein-gravity analysis is *consistent within its assumptions*; modified gravity is genuinely outside our slice and we cannot meaningfully test it without committing to a specific theory.

---

## What was actually done

Phase 6a literature pull on f(R), Horndeski, and adjacent modified-gravity warp drive papers. No computational follow-up (Phase 6b deferred — would require building an f(R) Einstein tensor pipeline, which is a significant 4th-order PDE undertaking).

### Construction 1: Lobo & Oliveira 2009 (arXiv:0909.5539, Phys. Rev. D 80, 104012)

**Title:** *Wormhole geometries in f(R) modified theories of gravity.*

**Setup:** Apply the f(R) field equations
$$ f'(R) R_{\mu\nu} - \tfrac{1}{2}f(R) g_{\mu\nu} - (\nabla_\mu \nabla_\nu - g_{\mu\nu} \Box) f'(R) = 8\pi T^{\rm matter}_{\mu\nu} $$

to a Morris-Thorne wormhole geometry. Rewrite as $G_{\mu\nu} = 8\pi T^{\rm eff}_{\mu\nu}$ where

$$ T^{\rm eff}_{\mu\nu} = T^{\rm matter}_{\mu\nu} + T^{\rm curv}_{\mu\nu}, \qquad T^{\rm curv}_{\mu\nu} = \frac{1}{8\pi f'(R)}\bigl[(\nabla_\mu\nabla_\nu - g_{\mu\nu}\Box) f'(R) + (f - R f')/2 \cdot g_{\mu\nu}\bigr]$$

**Key result**: by choosing $f(R)$ appropriately, one can arrange $T^{\rm matter}$ to satisfy WEC/NEC while $T^{\rm curv}$ absorbs the geometric obligation to violate the energy conditions.

**Status**: this is a *real* mathematical construction with explicit examples. It is also *frame-dependent* — Einstein-frame transformation $\tilde g_{\mu\nu} = f'(R) g_{\mu\nu}$ gives standard GR + scalar field, where the scalar field's stress-energy can violate the energy conditions even though the original "matter" did not.

**Implication**: if the modified-gravity loophole is accepted, classical DEC-respecting wormholes (and likely warp drives) exist. If we instead require DEC-respecting matter in any frame, the loophole vanishes.

### Construction 2: Fell & Heisenberg 2021 (arXiv:2104.06488, Phys. Rev. D)

**Title:** *Positive Energy Warp Drive from Hidden Geometric Structures.*

**Setup**: Standard GR. The "modified gravity" framing in our search results was misleading. They use a careful decomposition of the Eulerian energy in terms of geometric variables (extrinsic curvature, shift gradients) and identify a sub-class of warp drives where the Eulerian energy is positive semi-definite.

**Key result**: example superluminal soliton with total energy $\sim 10^{-4} M_\odot$ and *purely positive energy density*. This is **not** modified gravity; it's an existence claim within GR using a different shift-vector ansatz than Alcubierre.

**Status**: directly relevant to Slice 1 (alternate shift families), not Slice 6. The construction is in principle within our Slice 1 analysis space, though we used single-mode axisymmetric ansätze and Fell-Heisenberg use multi-mode + non-trivial decomposition. This is a real candidate for a Slice 1 follow-up if we wanted to extend the family ansatz.

**Note from our LITERATURE.md**: we had Fell-Heisenberg 2021 in our references table for `MATTER_SHELL_PATH.md` already, listed as "Positive energy from hidden geometric structures." It is the *only* claimed positive-energy warp drive in standard GR that has not been independently refuted, and it is overdue for a careful evaluation.

### Construction 3: Garattini-Zatrimaylov 2025 (arXiv:2502.13153)

**Title:** *Positive-Energy Warp Drive in a De Sitter Universe.*

**Setup**: Standard GR with $\Lambda$. They embed a warp bubble in de Sitter background and require the bubble to move *radially at the Hubble expansion velocity*. Generalises Ellis's earlier embedding in a Schwarzschild background.

**Key result**: under the radial-Hubble-velocity condition, the Eulerian energy density is non-negative and *averaged* WEC/NEC are satisfied (though local violations remain). They also prove a more generic theorem: if vacuum-energy perturbations produce any underdense regions in all reference frames, they always result in local NEC/WEC violations.

**Implication for Slice 5**: my notebook concluded "the asymptotic-flatness assumption was not load-bearing" because dark-energy momentum exchange is 42 orders of magnitude below the GW-recoil channel. But Garattini-Zatrimaylov are making a different claim: it's not about *momentum* exchange but about whether the de Sitter background *changes the local energy-condition obligations*. Their result is that for a bubble at exactly Hubble velocity, averaged WEC/NEC are recoverable. **This is a real qualifier on Slice 5's conclusion** — in cosmological backgrounds, the energy-condition obligations on the warp bubble can be modified non-trivially. I should update the Slice 5 framing.

**Caveats on Garattini-Zatrimaylov**: (i) requires bubble velocity to match Hubble flow exactly — not arbitrary; (ii) only *averaged* energy conditions are satisfied, not local; (iii) it's still standard GR, not modified gravity per se.

**Reproduction EXECUTED — Session 46 (2026-07-06), audit-queue Block 3(c): CONFIRMED EXACTLY, sharpened against usefulness.** Full record in [`GARATTINI_ZATRIMAYLOV2025_EVALUATION.md`](GARATTINI_ZATRIMAYLOV2025_EVALUATION.md); battery [`verification/test_gz_desitter_reproduction.py`](verification/test_gz_desitter_reproduction.py) (9/9). Every checked equation verified at machine precision (including against the full 4D Einstein tensor of the exact time-dependent moving-bubble metric) — the first external construction in the programme to survive reproduction. The sharpenings: the Hubble-matched bubble is *exactly comoving* (zero transport content); the "averaged" conditions are fixed-$t$ volume averages inherited from the background; **ANEC along every wall-crossing null geodesic tested is strictly violated**; the local violations are a wall-shape-set multiple of the background vacuum density. Caveats (i)–(ii) above are thereby confirmed and strengthened: assumption 5b's qualifier is real (now A-grade within slice) but opens no useful-warp loophole.

### Other authors and constructions briefly noted

- **Capozziello, Luongo, Mauro 2021**: f(R) traversable wormholes with stable conditions and "no exotic matter" (in Jordan frame). Same frame-dependence caveat as Lobo-Oliveira.
- **Bobrick-Martire 2021** (already in our LITERATURE): general framework that proves "any warp drive requires propulsion" in *standard GR*. They discuss extensions to modified gravity briefly but do not produce explicit constructions.

---

## Slice 6b (computational follow-up): OPENED Session 51 (2026-07-12) — target selected, slice declared

**Superseding the deferral note below:** the "4th-order PDE solver" framing overestimated the cost. The project's method never solves field equations — it evaluates the *required* stress-energy on a metric ansatz. In f(R) the Jordan-frame matter tensor is **algebraic** in the metric and its derivatives:

$$8\pi T^{\rm matter}_{\mu\nu} = f'(R)\,R_{\mu\nu} - \tfrac12 f(R)\,g_{\mu\nu} - (\nabla_\mu\nabla_\nu - g_{\mu\nu}\Box)f'(R),$$

4th-order in metric derivatives (the $\nabla\nabla f'(R)$ term adds two derivatives to $R$), but for the axisymmetric warp-shell ansatz this is the same symbolic-build-then-lambdify pattern as the certified GR radial evaluator (and its Session-49 time-dependent extension) — plus the existing Eulerian orthonormalisation and EC machinery applied to $T^{\rm matter}$ unchanged.

**Deliberate theory target (the ROADMAP-required choice): $f(R) = R + \alpha R^2$** (quadratic/Starobinsky form), $\alpha$ swept. Rationale: (i) it is this document's own natural-6b proposal; (ii) one parameter, well-posed scalaron, the cleanest member of the class the Lobo–Oliveira loophole lives in; (iii) fixing the theory FIRST is methodologically essential — Lobo–Oliveira *reconstruct* $f$ from a chosen geometry, and allowing a designer $f$ makes "success" nearly tautological. The designer-$f$ question is kept as a separate second leg with real teeth: the reconstruction is **overdetermined** when $R(x)$ is non-monotonic (a warp shell takes the same $R$ value at many points, and $f$ must be a single function of $R$ globally) — a potential class-level obstruction worth deriving.

**Geometry targets:** (a) the canonical Alcubierre metric (literature-facing; our axisymmetric ansatz covers it exactly with $A_{\rm pos} = B = 1$, $F$ = Alcubierre profile); (b) the certified Fuchs-class configurations (programme-facing: the S32 floor and the canonical vessel).

**Slice declaration (accompanies every 6b claim):** the question tested is the Jordan-frame loophole *on its own terms* — "do the pointwise WEC/DEC hold for $T^{\rm matter}$ in the Jordan frame, with the theory viability conditions $f'(R) > 0$ (no graviton ghost) and $f''(R) \ge 0$ (non-tachyonic scalaron) holding pointwise on the configuration". The Einstein-frame reading, in which the conformal transformation moves any violation into the scalaron sector and the loophole dissolves, is recorded as the standing interpretive caveat (headline take above) — this slice does not adjudicate the frame question, it tests the claimed loophole inside its own frame. Static configurations; radial representation; quadratic $f$; $\alpha$ swept over decades around $1/R_{\rm shell}$; observational bounds on $\alpha$ recorded as context, not imposed (landscape mapping, not phenomenology).

**Build plan:** Session 51 — symbolic $T^{\rm matter}$ for the axisymmetric ansatz with $\alpha$ symbolic; the decisive regression gate is $\alpha \to 0$ reproducing the certified GR evaluator exactly; numerics need radial profile derivatives to 4th order (quintic-spline; convergence gates mandatory — the S42-era prefactor-amplification lesson applies doubly here). Then the $\alpha$-ladder at the geometry targets, the designer-$f$ overdetermination leg, and closure.

### Session-51 results (2026-07-12): infrastructure certified; first physics is strongly negative

**Infrastructure** (battery [`verification/test_fr_matter.py`](verification/test_fr_matter.py), 6/6): evaluator [`warp_factory_py/solvers/fr_matter.py`](warp_factory_py/solvers/fr_matter.py) with the split form $T = G_{\rm certified} + \alpha C$; the correction tensor $C$ per-component exact-cancelled once (~48 min) and emitted as the generated module `fr_correction_generated.py` (4,409 shared subexpressions; regeneration cross-checked at 5.6e-7, the uncancelled noise floor). Anchors: $\alpha \to 0$ ≡ GR **exactly** (rel 0.0, full pipeline); Schwarzschild stays vacuum at any $\alpha$ (max|C| 6.8e-16); de Sitter's $C \equiv 0$ with $R = 12/L^2$ exact; small-$\alpha$ response linear/antisymmetric to machine precision (slope $-6.47\times10^{37}$ per m² at the floor config); the $\alpha R \sim 1$ collapse is resolution-robust (RES_SCOUT vs RES_FULL 5.8%). Derivative inventory: $A_{\rm pos}, F$ to 4th order, $B$ to 3rd.

**First physics (two geometry targets, quadratic $f$, Jordan frame):**

1. **Bare Alcubierre (the loophole's home turf — can $T^{\rm curv}$ absorb a GR EC violation?): NO.** Over $\alpha \in \pm[10^{-2}, 10^{5}]$ m² (8 decades, both signs), the best improvement to the WEC-violating minimum ($-9.121\times10^{39}$ in GR) is **0.036%** (at $\alpha = 0.1$); beyond $|\alpha| \sim 1$ the correction *amplifies* the violation linearly in $\alpha$ (300× worse by $\alpha R \sim 1$), and large $\alpha$ additionally breaks viability ($f' < 0$ — the Alcubierre wall has both signs of $R$).
2. **Certified Fuchs floor configuration (EC-passing in GR): the viable direction strictly degrades.** $\alpha > 0$ (the only $f'' \ge 0$ direction) monotonically shrinks the margin; the EC-preserving window is $\alpha \lesssim 0.76$ m², i.e. $\alpha R \lesssim 10^{-3}$ — the modification must stay dynamically negligible. The marginally helpful direction ($\alpha < 0$, small) is theory-non-viable (tachyonic scalaron) and turns destructive by $\alpha = -10$ anyway.

**Reading (slice-scoped):** within the quadratic-$f(R)$, Jordan-frame, static, radial slice at these two geometry classes, the "curvature absorbs the energy-condition obligation" mechanism does not materialize — the $\nabla\nabla f'(R)$ terms at a warp wall *add* EC obligations rather than absorbing them, in both $\alpha$ signs. Remaining before closing 2E.2: the full $\alpha \times$ geometry map (S52) and the designer-$f$ overdetermination leg (can *any* viable $f$ do better, given that $f$ must be a single function of $R$ on a geometry where $R(x)$ is highly non-monotonic).

### Session-52 closure (2026-07-12): 2E.2 CLOSED NEGATIVE — both legs

**Leg 1 — the α × geometry map** (161 points: 4 Alcubierre walls incl. a $v=0.1$ variant + 3 certified Fuchs-class configs × 23 α values; `sweeps/fr_alpha_map_full_concat.parquet`; battery `map` mode 4/4): **no EC-violating configuration is rescued at any α** (best Alcubierre improvement 0.002–0.2%, at a tiny α that tracks the wall-curvature scale, before monotone degradation), and **every EC-passing configuration's best *viable* α is exactly 0** — any α > 0 strictly degrades. EC-compatibility windows at RES_FULL: floor < 0.01 m² ($\alpha R < 1.4\times10^{-5}$), canonical vessel < 3 m² — dynamically negligible in all cases. The α < 0 margin boosts (up to 40× at the floor, α = −3) all require the tachyonic scalaron and are theory-non-viable.

**Leg 2 — the designer-$f$ NEC feasibility theorem** (`hf_jobs/analysis/fr_designer_lp.py`; battery [`verification/test_fr_designer_lp.py`](verification/test_fr_designer_lp.py) 4/4): on null vectors the $g_{\mu\nu}$ terms drop, so Jordan-frame NEC constrains only $(f', f'', f''')$ at each $R$ value — *linearly*. Normalising by $f' > 0$ (ghost-free graviton, the minimum for the theory to exist), each level set of $R$ gives a 2-variable LP. **On the bare Alcubierre wall: 24/24 level-set bins are infeasible in both modes ($f''$ free and $f'' \ge 0$), and the obstruction is *pointwise* — 23.4% of sampled wall points individually admit NO $(f', f'', f''')$ across their own null-direction fan.** No $f(R)$ whatsoever — any shape, any $f''$ sign, any $f'''$ — yields NEC-respecting Jordan matter on that geometry; level sets and global integrability of $f$ never even enter. Machinery certified against the quadratic evaluator at 1.15e-10 (GATE Q). The Fuchs floor is LP-feasible everywhere (0/24), as it must be — GR itself ($u = w = 0$) passes there; the loophole is dead in both directions: it cannot *rescue* violating geometry and can only *degrade* passing geometry.

**Slice scope of the closure:** Jordan-frame ECs on the matter tensor (the loophole on its own terms); static, radial representation; the tested geometry classes (Alcubierre tanh walls $w \in [0.75, 3]$, $v \in \{0.02, 0.1\}$; certified Fuchs-class configurations); quadratic $f$ for the map, arbitrary $f$ with $f' > 0$ for the LP theorem; NEC (the weakest condition — its failure implies WEC/DEC failure). Other modified-gravity families (Horndeski, $f(R,T)$, EGB, …) remain untested and outside this closure. **Reopening criteria unchanged** (ROADMAP 2E.2).

*(Original deferral note, retained for the record:)* A natural Slice 6b would be: take f(R) = R + αR², compute the Einstein/Jordan-frame split for the Alcubierre metric, and ask whether the matter-side stress-energy can be made DEC-respecting for some α > 0. ~~This requires building a 4th-order field-equation solver and is significantly more involved than our standard pipeline. **Deferred** as outside the scope of the surfing-mode landscape mapping.~~

---

## Implication for the project

**Slice 6 is genuinely open.** Modified gravity provides a real loophole (in Jordan frame); whether this counts as "DEC-respecting matter" depends on frame interpretation. Our Path 2A analysis was explicitly within standard 4D Einstein gravity; modified-gravity constructions are by definition outside our slice.

**Updated narrowing of load-bearing assumptions** (after all six slices):

**Canonical post-Phase-2C table** (this is the authoritative version; mirrored in [`NAVIGATOR.md`](NAVIGATOR.md)):

| Sub-assumption | Status (Slices 1-6) |
|---|---|
| Single-mode axisymmetric shift | Slice 1: not load-bearing within tested family. Fell-Heisenberg 2021 may break this with multi-mode (Session 10 follow-up — see [`FELL_HEISENBERG2021_EVALUATION.md`](FELL_HEISENBERG2021_EVALUATION.md) when present). |
| Single-bump matter perturbation cancellation | Slice 2: not load-bearing |
| Steady-state metric + Lorentz boost | Slice 3: not load-bearing |
| Pfenning-Ford-style tight QI bound | Slice 4: substantively weakened by Krasnikov 2003 |
| Asymptotic flatness vs. FRW + $\Lambda$ | Slice 5: momentum-exchange channel is not load-bearing, **BUT** Garattini-Zatrimaylov 2025 shows that local energy-condition obligations *do* change in de Sitter background under specific conditions. Mixed verdict. |
| 4D Einstein gravity | **Slice 6: the f(R) corner CLOSED NEGATIVE (Sessions 51–52).** Quadratic f(R) cannot rescue EC-violating warp geometry and strictly degrades EC-passing configurations (viable direction); the designer-f LP theorem kills *every* f(R) with f′ > 0 on the Alcubierre-class wall (pointwise infeasibility). Other modified-gravity families (Horndeski, f(R,T), EGB, …) remain untested — the assumption is narrowed, not fully closed. |

**Headline composite take.** After all six slices, the load-bearing assumptions for the Path 2A negative result are:
- **Standard 4D Einstein gravity** (Slice 6 modifies this);
- **Local DEC required in the matter frame** (modified gravity in Jordan frame moves the violation to the curvature side);
- **Single-mode shift profiles** (Fell-Heisenberg 2021 may break this with multi-mode);
- **Specific-velocity condition not met** (Garattini-Zatrimaylov 2025 needs $v = v_{\rm Hubble}$).

These are **interpretation-dependent and somewhat contrived** loopholes, but they are also *real*. None of them are "easy" engineering paths to a working warp drive — they require either (a) accepting modified-gravity-as-physical, (b) finding a multi-mode shift profile with the Fell-Heisenberg property, or (c) co-moving the warp drive with cosmological expansion at exactly the right rate.

**Phase 2C overall verdict**: Path 2A's negative result is robust within its slice. The slice has well-defined load-bearing assumptions, and there exist published constructions outside the slice that claim positive-energy warp drives. None of those constructions has been independently verified by us, and several are subject to interpretation-dependent caveats. The honest summary is "no useful classical positive-matter warp drive within the slice we tested; positive-energy claims exist outside the slice but face interpretive challenges."

## References

- Lobo & Oliveira 2009 ([arXiv:0909.5539](https://arxiv.org/abs/0909.5539), Phys. Rev. D 80, 104012) — f(R) wormholes.
- Fell & Heisenberg 2021 ([arXiv:2104.06488](https://arxiv.org/abs/2104.06488)) — positive-energy soliton in standard GR.
- Garattini & Zatrimaylov 2025 ([arXiv:2502.13153](https://arxiv.org/abs/2502.13153)) — warp drive in de Sitter.
- Capozziello, Luongo, Mauro 2021 (Eur. Phys. J. P) — stable f(R) wormholes.
- Garattini 2024 ([arXiv:2408.04495](https://arxiv.org/abs/2408.04495)) — warp drives in Schwarzschild background using Painlevé-Gullstrand coordinates.

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

### Other authors and constructions briefly noted

- **Capozziello, Luongo, Mauro 2021**: f(R) traversable wormholes with stable conditions and "no exotic matter" (in Jordan frame). Same frame-dependence caveat as Lobo-Oliveira.
- **Bobrick-Martire 2021** (already in our LITERATURE): general framework that proves "any warp drive requires propulsion" in *standard GR*. They discuss extensions to modified gravity briefly but do not produce explicit constructions.

---

## Slice 6b (computational follow-up): NOT done

A natural Slice 6b would be: take f(R) = R + αR², compute the Einstein/Jordan-frame split for the Alcubierre metric, and ask whether the matter-side stress-energy can be made DEC-respecting for some α > 0.

This requires building a 4th-order field-equation solver and is significantly more involved than our standard pipeline. **Deferred** as outside the scope of the surfing-mode landscape mapping. The literature note above is sufficient for Phase 2C.

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
| 4D Einstein gravity | **Slice 6: genuinely open.** Modified gravity (Jordan frame) provides a real loophole; frame-dependence makes the verdict interpretation-sensitive. |

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

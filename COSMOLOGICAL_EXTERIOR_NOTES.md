# Slice 5: Cosmological Exterior — Notes

**Source:** [`cosmological_exterior.ipynb`](cosmological_exterior.ipynb).
**Written:** 2026-04-17 (Session 9).

## TL;DR

**The momentum-exchange channel from the asymptotic-flatness assumption is *not* load-bearing.** Replacing the vacuum exterior with a McVittie + $\Lambda$ background gives a cosmological-exterior contribution to Mechanism A (push-from-a-wall) with $\Delta v \le 10^{-36}$ m/s for $R_{\rm BY} = 100 \, R_{\rm shell}$, scaling as $R_{\rm BY}^3$. Even at galactic scales ($R_{\rm BY} = 10^9 R_{\rm shell}$) the ceiling is $\sim 10^{-15}$ m/s — 42 orders of magnitude below the GW-recoil channel of Package 3, which itself was already negligible compared to warp targets.

**Hubble drag** acts on cosmological timescales ($1/H_0 \sim 10^{10}$ yr) and is irrelevant operationally.

**However** (added Slice 6 lit-pull, see [`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md)): **Garattini & Zatrimaylov 2025 (arXiv:2502.13153)** show that a warp bubble *moving at the Hubble expansion velocity* in de Sitter background can satisfy *averaged* (not local) WEC/NEC. This is a different kind of "cosmological loophole" than the momentum-exchange channel I tested — it's about modified energy-condition obligations rather than reaction mass. Under their specific velocity-matching condition, the cosmological background *does* change the Slice 5 conclusion. **The right summary** is therefore: "the cosmological-exterior momentum-exchange channel is not load-bearing (this notebook), but the cosmological-exterior energy-condition obligation is non-trivially modified for the special case $v = v_{\rm Hubble}$ (Garattini-Zatrimaylov)." This is a real qualifier I should acknowledge.

## What was actually computed

1. **McVittie metric** (the static central mass in an FRW background): $ds^2 = -((1-\tilde m/2r)/(1+\tilde m/2r))^2 dt^2 + (1+\tilde m/2r)^4 a(t)^2 (dr^2 + r^2 d\Omega^2)$ with $\tilde m = m/a$. For pure $\Lambda$: $a(t) = e^{Ht}$.
2. **Symbolic $G_{tt}$**: lambdified, evaluated at $r \in \{1, 10, 100, 1000\}$, $m=H=0.1$. **Asymptotic limit matches FRW value $3H^2$** (within McVittie corrections); this is a regression check on the symbolic pipeline.
3. **Order-of-magnitude momentum-exchange ceiling** for Mechanism A: $\Delta v_{\rm shell} \le (M_\Lambda(R_{\rm BY}) / M_{\rm shell}) \cdot c$, where $M_\Lambda = \rho_\Lambda \cdot \frac{4\pi}{3} R_{\rm BY}^3$ is the dark-energy mass enclosed in a sphere of radius $R_{\rm BY}$. For $R_{\rm BY} = 100 R_{\rm shell} = 1500$ m and Fuchs-class $M_{\rm shell}$: $\Delta v \le 5.7 \times 10^{-36}$ m/s.

## What this notebook does NOT establish

1. **Brown-York quasi-local momentum** computed from first principles. We used an order-of-magnitude argument; the BY calculation would give the same answer to within order unity but isn't necessary given the 42-order-of-magnitude headroom.
2. **Inflation or matter-radiation FRW**: only de Sitter tested. Adding ordinary matter/radiation increases the available reaction mass by at most factor ~10 (matter is comparable in density to $\Lambda$ today).
3. **TRUST_AUDIT #3 (Warp Factory install)**: deferred. The result is so cleanly negative that NR validation is not needed for this slice.

## Implication

The narrowing of load-bearing assumptions continues. After all six slices the picture is **(updated post-Slice-6 lit pull)**:

| Sub-assumption | Status (after Slices 1–6, canonical) |
|---|---|
| Single-mode axisymmetric shift (Slice 1) | Not load-bearing within tested family. Fell-Heisenberg 2021 may break this with multi-mode (untested in our framework as of Session 9; queued for Session 10). |
| Single-bump matter perturbation cancellation (Slice 2) | Not load-bearing |
| Steady-state metric + Lorentz boost (Slice 3) | Not load-bearing |
| Pfenning-Ford-style tight QI bound (Slice 4) | Substantively weakened by Krasnikov 2003, but our classical no-go is QI-independent |
| Asymptotic flatness vs. FRW + $\Lambda$ — momentum exchange (Slice 5, this notebook) | Not load-bearing (42+ orders of magnitude headroom) |
| Asymptotic flatness vs. FRW + $\Lambda$ — energy-condition obligations (Slice 5 + Garattini-Zatrimaylov 2025) | **Modified for special case $v = v_{\rm Hubble}$**: bubble at Hubble velocity in de Sitter satisfies *averaged* WEC/NEC. Real qualifier on this notebook's conclusion. |
| 4D Einstein gravity (Slice 6) | Real loophole in Jordan-frame f(R) (Lobo-Oliveira 2009); interpretation-dependent (Einstein-frame transformation moves violation to scalar field). |

The canonical version of this table now lives in [`NAVIGATOR.md`](NAVIGATOR.md); see [`MODIFIED_GRAVITY_LIT.md`](MODIFIED_GRAVITY_LIT.md) for the Slice 6 lit pull and the Garattini-Zatrimaylov caveat.

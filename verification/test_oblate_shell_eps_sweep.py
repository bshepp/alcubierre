"""EC sweep over Legendre-2 deformation amplitude epsilon.

Question: at fixed total ADM mass M_tot and fixed warp-shell radii (R1, R2),
does volume-preserving oblate (epsilon<0) or prolate (epsilon>0) deformation
of a Fuchs single shell improve the energy-condition margins relative to the
spherical (epsilon=0) reference?

Geometry (held fixed):
- Outer shell wall: R1=10, R2=20  (canonical Fuchs Fig. 10)
- Total mass: M_tot = 4.49e27 kg
- v_warp = 0.02 c
- smoothFactor = 4000
- Warp band: same (R1, R2) as the shell

Deformation: r_eff = r / s(theta) with s(theta) = (1 + epsilon*P_2(cos theta))^(1/3),
which is volume-preserving on the unit sphere (P_2 integrates to zero).

Grid: (1, 300, 300, 5) at dx=0.2 m, WC=(0, 30, 30, 0.5). Identical for every
epsilon -> apples-to-apples comparison. Identical to Session 26 nested-shell
sweep grid for direct comparability.
"""

from __future__ import annotations

import time
import numpy as np

from warp_factory_py.metrics.warp_shell import metric_oblate_warp_shell
from warp_factory_py.solvers.evaluator import eval_metric


M_TOT = 4.49e27
R1 = 10.0
R2 = 20.0
SF = 4000.0
V = 0.02
GRID = (1, 300, 300, 5)
GS = (1.0, 0.2, 0.2, 0.2)
WC = (0.0, 30.0, 30.0, 0.5)


def _inshell_mask():
    Nx, Ny, Nz = GRID[1:]
    XC = ((np.arange(Nx) + 1) * GS[1] - WC[1])
    YC = ((np.arange(Ny) + 1) * GS[2] - WC[2])
    ZC = ((np.arange(Nz) + 1) * GS[3] - WC[3])
    R = np.sqrt(XC[:, None, None] ** 2 + YC[None, :, None] ** 2 + ZC[None, None, :] ** 2)
    ish = (R >= R1) & (R <= R2)
    bd = np.zeros_like(R, dtype=bool)
    bd[2:-2, 2:-2, 1:-1] = True
    m3 = ish & bd
    return m3[None, :, :, :]


def report(label, ec, mask):
    out = []
    for cond in ("null", "weak", "dominant", "strong"):
        v = ec[cond][mask]
        n_viol = int((v < -1e-12).sum())
        out.append((cond, float(v.min()), 1.0 - n_viol / v.size, n_viol, v.size))
    print(f"\n[{label}]")
    for cond, mn, pf, nv, nt in out:
        print(f"  {cond:8s}  min = {mn:+.3e}   pass = {pf:.6f}   n_viol = {nv}/{nt}")
    return {c[0]: (c[1], c[2]) for c in out}


def _run_sweep(axis: str, mask):
    print(f"\n{'#' * 86}")
    print(f"#  AXIS = {axis!r}  (deformation symmetry axis; warp motion is along x)")
    print(f"{'#' * 86}")
    epsilons = [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3]
    results = []
    for eps in epsilons:
        t0 = time.time()
        g, p = metric_oblate_warp_shell(
            GRID, WC, m=M_TOT, R1=R1, R2=R2, epsilon=eps, axis=axis,
            smooth_factor=SF, v_warp=V, do_warp=True, grid_scale=GS,
        )
        s_min, s_max = p["s_minmax"]
        h = p["horizon_min"]
        res = eval_metric(g, num_angular=100, num_temporal=10, wf_compat=False)
        ecs = report(
            f"axis={axis!r}  eps = {eps:+.2f}    s in [{s_min:.4f}, {s_max:.4f}]   "
            f"horizon_min={h:.4f}    ({time.time()-t0:.1f}s)",
            res.ec, mask,
        )
        results.append((eps, ecs, s_min, s_max, h))
    return results


def main():
    print(f"Oblate-shell epsilon sweep (Phase 3.3 sub-item 5)")
    print(f"v = {V}c, M_tot = {M_TOT:.3e} kg, sf = {SF}")
    print(f"R1, R2 = ({R1}, {R2}); warp band = (R1, R2)")
    print(f"Grid {GRID} @ dx={GS[1]} m, WC={WC}")

    mask = _inshell_mask()
    results_z = _run_sweep("z", mask)  # baseline (perpendicular to motion)
    results_x = _run_sweep("x", mask)  # aligned with motion direction
    results_by_axis = {"z": results_z, "x": results_x}

    for axis in ("z", "x"):
        results = results_by_axis[axis]
        print()
        print("=" * 92)
        print(f"HEADLINE (axis={axis!r}): in-shell EC margin vs Legendre-2 deformation amplitude epsilon")
        print("=" * 92)
        print(f"{'epsilon':>8s}  {'min(NEC)':>14s}  {'pass(NEC)':>10s}  "
              f"{'min(WEC)':>14s}  {'pass(WEC)':>10s}  {'min(DEC)':>14s}  {'pass(DEC)':>10s}")
        print("-" * 92)
        for eps, ecs, _smn, _smx, _h in results:
            n = ecs["null"]; w = ecs["weak"]; d = ecs["dominant"]
            print(f"{eps:>+8.2f}  {n[0]:>+14.3e}  {n[1]:>10.6f}  "
                  f"{w[0]:>+14.3e}  {w[1]:>10.6f}  {d[0]:>+14.3e}  {d[1]:>10.6f}")

        eps_zero = next(ecs for eps, ecs, *_ in results if eps == 0.0)
        nec_ref = eps_zero["null"][0]
        print(f"\nReference (axis={axis!r}, epsilon=0): min(NEC) = {nec_ref:+.3e}")
        print("Delta(NEC margin) vs reference (positive = improvement):")
        for eps, ecs, *_ in results:
            if eps == 0.0:
                continue
            delta = ecs["null"][0] - nec_ref
            sign = "improves" if delta > 0 else "degrades"
            pct = 100.0 * delta / abs(nec_ref) if nec_ref != 0 else float('nan')
            print(f"  eps = {eps:+.2f}    delta = {delta:+.3e}   ({sign}, {pct:+.2f}%)")


if __name__ == "__main__":
    main()

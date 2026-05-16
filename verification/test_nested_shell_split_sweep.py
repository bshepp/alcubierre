"""Mass-split sweep for the 2-shell config.

Vary the fraction f = M_inner / M_total in {0.05, 0.1, 0.2, 0.3, 0.5, 0.7}.
Warp ramp confined to the *outer* wall (10, 20) (the gentler of the two
configurations from the Item 4 EC test).

Question: does any split f > 0 improve over the f = 0 baseline?
"""

from __future__ import annotations

import time
import numpy as np

from warp_factory_py.metrics.warp_shell import (
    metric_nested_warp_shells,
    metric_warp_shell_comoving,
)
from warp_factory_py.solvers.evaluator import eval_metric

M_TOT = 4.49e27
SF = 4000.0
V = 0.02
GRID = (1, 300, 300, 5)
GS = (1.0, 0.2, 0.2, 0.2)
WC = (0.0, 30.0, 30.0, 0.5)


def _inshell_mask(intervals):
    Nx, Ny, Nz = GRID[1:]
    XC = (np.arange(Nx) * GS[1] - WC[1])
    YC = (np.arange(Ny) * GS[2] - WC[2])
    ZC = (np.arange(Nz) * GS[3] - WC[3])
    R = np.sqrt(XC[:, None, None] ** 2 + YC[None, :, None] ** 2 + ZC[None, None, :] ** 2)
    ish = np.zeros_like(R, dtype=bool)
    for (a, b) in intervals:
        ish |= (R >= a) & (R <= b)
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
    return out[0][1], out[0][2]  # (min(NEC), pass(NEC))


def main():
    print(f"Sweep over inner-shell mass fraction f = M_inner / M_total")
    print(f"v = {V}c, M_tot = {M_TOT:.3e} kg, sf = {SF}")
    print(f"warp band fixed at (10, 20); inner shell at (5, 8)\n")

    # Baseline (f = 0)
    t0 = time.time()
    g0, _ = metric_warp_shell_comoving(
        GRID, WC, m=M_TOT, R1=10.0, R2=20.0, smooth_factor=SF,
        v_warp=V, do_warp=True, grid_scale=GS,
    )
    res0 = eval_metric(g0, num_angular=100, num_temporal=10, wf_compat=False)
    m1 = _inshell_mask([(10, 20)])
    nec0, p0 = report(f"f = 0.00 (1-shell)  ({time.time()-t0:.1f}s)", res0.ec, m1)

    results = [(0.0, nec0, p0)]
    fractions = [0.05, 0.10, 0.20, 0.30, 0.50, 0.70]
    m23 = _inshell_mask([(5, 8), (10, 20)])
    for f in fractions:
        t0 = time.time()
        M_inner = f * M_TOT
        M_outer = (1 - f) * M_TOT
        shells = [(5.0, 8.0, M_inner), (10.0, 20.0, M_outer)]
        g, _ = metric_nested_warp_shells(
            GRID, WC, shells=shells, smooth_factor=SF,
            warp_R1=10.0, warp_R2=20.0,
            v_warp=V, do_warp=True, grid_scale=GS,
        )
        res = eval_metric(g, num_angular=100, num_temporal=10, wf_compat=False)
        nec, p = report(f"f = {f:.2f}    ({time.time()-t0:.1f}s)", res.ec, m23)
        results.append((f, nec, p))

    print()
    print("=" * 70)
    print(f"{'f_inner':>8s}  {'min(NEC)':>14s}  {'pass(NEC)':>12s}")
    print("=" * 70)
    for f, nec, p in results:
        print(f"{f:>8.2f}  {nec:>+14.3e}  {p:>12.6f}")


if __name__ == "__main__":
    main()

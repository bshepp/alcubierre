"""End-to-end EC comparison: 1-shell vs 2-shell at v_warp = 0.02c.

Question: with the warp shift confined to the innermost cavity wall,
does splitting ADM mass across nested shells change the EC margins
relative to a single shell of the same total mass?

Geometry (held fixed):
- Outer shell wall: R1=10, R2=20  (passenger cavity boundary in 1-shell case)
- 2-shell config: inner thin shell (5, 8, 0.2*M_tot)
                  + outer shell (10, 20, 0.8*M_tot)
                  warp ramp confined to the *inner* shell (5..8)
- Total mass: M_tot = 4.49e27 kg (Fuchs canonical)
- v_warp = 0.02 c
- smoothFactor = 4000

Grid: (1, 100, 100, 5) at dx=0.6 m centered at (30, 30, 1.5).
Coarser than Fuchs Fig 10 but identical for both runs -> apples-to-apples.
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


def _summarize(name: str, ec: dict, T_eul: np.ndarray, t_elapsed: float,
               shell_intervals: list[tuple[float, float]]) -> None:
    rho = T_eul[0, 0]
    Nt, Nx, Ny, Nz = ec['null'].shape
    # Build in-shell mask in (Nx, Ny, Nz)
    xs = (np.arange(Nx) - (Nx - 1) / 2.0) * GS[1]
    ys = (np.arange(Ny) - (Ny - 1) / 2.0) * GS[2]
    zs = (np.arange(Nz) - (Nz - 1) / 2.0) * GS[3]
    # WC offsets shift origin: world coords = i*ds, comparing radius from WC
    # (ec is centered on WC by construction of the metric)
    XC = (np.arange(Nx) * GS[1] - WC[1])
    YC = (np.arange(Ny) * GS[2] - WC[2])
    ZC = (np.arange(Nz) * GS[3] - WC[3])
    R = np.sqrt(XC[:, None, None] ** 2 + YC[None, :, None] ** 2 + ZC[None, None, :] ** 2)
    in_shell = np.zeros_like(R, dtype=bool)
    for (a, b) in shell_intervals:
        in_shell |= (R >= a) & (R <= b)
    # Trim FD-border before mask
    border = np.zeros_like(R, dtype=bool)
    border[2:-2, 2:-2, 1:-1] = True
    mask3d = in_shell & border
    # Broadcast to (Nt, Nx, Ny, Nz)
    mask4d = mask3d[None, :, :, :].repeat(Nt, axis=0)

    print(f"\n[{name}]  ({t_elapsed:.1f} s)   in-shell cells = {mask4d.sum()}")
    for cond in ("null", "weak", "dominant", "strong"):
        arr = ec[cond]
        vals = arr[mask4d]
        n_viol = (vals < -1e-12).sum()
        n_tot = vals.size
        pass_frac = 1.0 - n_viol / n_tot
        mn = vals.min()
        print(f"  {cond:8s}  min(in-shell) = {mn:+.3e}    pass_frac = {pass_frac:.6f}    n_viol = {n_viol}/{n_tot}")
    rho_vals = rho[mask4d] if rho.ndim == 4 else rho[mask3d]
    print(f"  rho     min = {rho_vals.min():+.3e}   max = {rho_vals.max():+.3e}")


def main():
    print("=" * 78)
    print(f"EC test:  v_warp = {V}c,  M_tot = {M_TOT:.3e} kg,  sf = {SF}")
    print(f"Grid {GRID} @ dx={GS[1]} m,  WC={WC}")
    print("=" * 78)

    # --- 1-shell baseline ---
    t0 = time.time()
    g1, p1 = metric_warp_shell_comoving(
        GRID, WC, m=M_TOT, R1=10.0, R2=20.0, smooth_factor=SF,
        v_warp=V, do_warp=True, grid_scale=GS,
    )
    res1 = eval_metric(g1, num_angular=100, num_temporal=10, wf_compat=False)
    _summarize("1-shell (R1=10, R2=20, M=Mtot)", res1.ec, res1.T_eul, time.time() - t0,
               shell_intervals=[(10.0, 20.0)])

    # --- 2-shell: outer carries 80%, inner 20%; warp ramp in inner shell ---
    M_outer = 0.8 * M_TOT
    M_inner = 0.2 * M_TOT
    shells = [(5.0, 8.0, M_inner), (10.0, 20.0, M_outer)]

    t0 = time.time()
    g2, p2 = metric_nested_warp_shells(
        GRID, WC, shells=shells, smooth_factor=SF,
        warp_R1=5.0, warp_R2=8.0,
        v_warp=V, do_warp=True, grid_scale=GS,
    )
    res2 = eval_metric(g2, num_angular=100, num_temporal=10, wf_compat=False)
    _summarize("2-shell, warp@(5,8): outer (10,20,0.8M) + inner (5,8,0.2M)",
               res2.ec, res2.T_eul, time.time() - t0,
               shell_intervals=[(5.0, 8.0), (10.0, 20.0)])

    # --- 2-shell with same outer geometry but warp at outer wall ---
    t0 = time.time()
    g3, p3 = metric_nested_warp_shells(
        GRID, WC, shells=shells, smooth_factor=SF,
        warp_R1=10.0, warp_R2=20.0,
        v_warp=V, do_warp=True, grid_scale=GS,
    )
    res3 = eval_metric(g3, num_angular=100, num_temporal=10, wf_compat=False)
    _summarize("2-shell, warp@(10,20): outer (10,20,0.8M) + inner (5,8,0.2M)",
               res3.ec, res3.T_eul, time.time() - t0,
               shell_intervals=[(5.0, 8.0), (10.0, 20.0)])

    print()
    print("=" * 78)
    print("Headline (in-shell support, FD-border-trimmed):")
    # Recompute masks per config
    def _inshell_mask(intervals):
        Nt, Nx, Ny, Nz = res1.ec['null'].shape
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
        return m3[None, :, :, :].repeat(Nt, axis=0)

    m1 = _inshell_mask([(10, 20)])
    m23 = _inshell_mask([(5, 8), (10, 20)])
    n1 = res1.ec['null'][m1]
    n2 = res2.ec['null'][m23]
    n3 = res3.ec['null'][m23]
    print(f"  1-shell baseline    min(NEC) = {n1.min():+.3e}    pass = {1 - (n1<-1e-12).sum()/n1.size:.6f}")
    print(f"  2-shell warp@inner  min(NEC) = {n2.min():+.3e}    pass = {1 - (n2<-1e-12).sum()/n2.size:.6f}")
    print(f"  2-shell warp@outer  min(NEC) = {n3.min():+.3e}    pass = {1 - (n3<-1e-12).sum()/n3.size:.6f}")


if __name__ == "__main__":
    main()

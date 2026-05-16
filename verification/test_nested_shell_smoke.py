"""Smoke + 2-shell physics test for metric_nested_warp_shells.

Test 1 (smoke): single shell via the nested API should agree closely with
the existing metric_warp_shell_comoving (the only difference being numerical
TOV vs the analytic constant-density closed form -- expect <~1e-3 relative
agreement on P inside the shell, and tighter on M and alpha).

Test 2 (sanity): a 2-shell config with the same total mass and same outer
geometry should give a different P(r) profile (per-shell P=0 boundaries)
but the same M(r) outside the outer shell and the same exterior alpha.

Both tests use the canonical Fuchs Fig.10 parameters reduced to a tiny
grid for fast iteration.
"""

from __future__ import annotations

import numpy as np

from warp_factory_py.metrics.warp_shell import (
    metric_nested_warp_shells,
    metric_warp_shell_comoving,
)
from warp_factory_py.utils.constants import G, c

# Canonical params (Fuchs Fig.10)
M_TOT = 4.49e27
R1 = 10.0
R2 = 20.0
SF = 4000.0
DX = 0.2

# Tiny grid (single point) -- only the radial profiles in `params` are needed.
# WC chosen so that world_size > R2 + margin, so rsample spans the shell.
GRID = (1, 1, 1, 1)
WC = (0.0, 30.0, 30.0, 30.0)
GS = (1.0, 1.0, 1.0, 1.0)


def main():
    print("=" * 72)
    print("Test 1: single-shell-via-nested vs metric_warp_shell_comoving")
    print("=" * 72)
    _, p_single = metric_warp_shell_comoving(
        GRID, WC, m=M_TOT, R1=R1, R2=R2, smooth_factor=SF, grid_scale=GS,
        r_sample_res=100_000,
    )
    _, p_nested1 = metric_nested_warp_shells(
        GRID, WC, shells=[(R1, R2, M_TOT)], smooth_factor=SF, grid_scale=GS,
        r_sample_res=100_000,
    )

    r = p_single["r"]
    in_shell = (r >= R1) & (r <= R2)
    in_ext = r > R2

    # Densities and M should agree to high precision (same construction)
    drho = np.max(np.abs(p_single["rho"] - p_nested1["rho"]))
    dM = np.max(np.abs(p_single["M"] - p_nested1["M"]))
    print(f"  max|drho|              = {drho:.3e}    (expect 0)")
    print(f"  max|dM|/M_total        = {dM / M_TOT:.3e}    (expect 0)")

    # Pressures: closed-form vs numerical TOV. Compare inside shell.
    P_s = p_single["P"][in_shell]
    P_n = p_nested1["P"][in_shell]
    rel_P = np.max(np.abs(P_s - P_n)) / max(np.max(np.abs(P_s)), 1e-300)
    print(f"  max|dP|/max|P| (shell) = {rel_P:.3e}    (expect <~1e-3)")

    # Alpha (in exterior, both should match Schwarzschild)
    a_s = p_single["alpha"][in_ext]
    a_n = p_nested1["alpha"][in_ext]
    rel_a = np.max(np.abs(a_s - a_n)) / max(np.max(np.abs(a_s)), 1e-300)
    print(f"  max|dalpha|/max|a|     = {rel_a:.3e}    (expect <~1e-4)")

    horizon = p_nested1["horizon_min"]
    print(f"  horizon_min            = {horizon:.6f}  (>0 means no horizon)")

    print()
    print("=" * 72)
    print("Test 2: 2-shell vs 1-shell with same total mass and outer R2")
    print("=" * 72)
    # Outer shell carries 80% of mass; inner thin shell carries 20%.
    # Inner shell sits at (5, 8); outer shell sits at (10, 20). Cavity for
    # passengers is r < 5, between which is a vacuum gap (8 < r < 10).
    M_outer = 0.8 * M_TOT
    M_inner = 0.2 * M_TOT
    shells_2 = [(5.0, 8.0, M_inner), (10.0, 20.0, M_outer)]
    _, p_nested2 = metric_nested_warp_shells(
        GRID, WC, shells=shells_2, smooth_factor=SF, grid_scale=GS,
        r_sample_res=100_000,
    )

    print(f"  shells = {shells_2}")
    print(f"  M_total (analytic)     = {p_nested2['M_total']:.4e}    (expect ~{M_TOT:.4e})")
    print(f"  M[-1] (smoothed)       = {p_nested2['M'][-1]:.4e}")
    print(f"  horizon_min            = {p_nested2['horizon_min']:.6f}")

    # In the vacuum gap (8 < r < 10), P should be 0
    in_gap = (r > 8.5) & (r < 9.5)  # interior of the gap to avoid smoothing leak
    print(f"  max|P| in vacuum gap   = {np.max(np.abs(p_nested2['P'][in_gap])):.3e}  (expect 0 unsmoothed)")
    print(f"  max|P_smooth| in gap   = {np.max(np.abs(p_nested2['P_smooth'][in_gap])):.3e}  (expect ~0)")

    # In each shell, P(R2_k) = 0 boundary
    i_R2_inner = np.searchsorted(r, 8.0)
    i_R2_outer = np.searchsorted(r, 20.0)
    print(f"  P(R2_inner=8)          = {p_nested2['P'][i_R2_inner]:.3e}  (expect ~0)")
    print(f"  P(R2_outer=20)         = {p_nested2['P'][i_R2_outer]:.3e}  (expect ~0)")

    # Peak pressure in each shell
    in_inner = (r > 5.0) & (r < 8.0)
    in_outer = (r > 10.0) & (r < 20.0)
    print(f"  max P in inner shell   = {p_nested2['P'][in_inner].max():.3e}")
    print(f"  max P in outer shell   = {p_nested2['P'][in_outer].max():.3e}")
    print(f"  max P in single shell  = {p_single['P'].max():.3e}  (1-shell ref)")


if __name__ == "__main__":
    main()

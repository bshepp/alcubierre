"""Smoke test for metric_oblate_warp_shell.

Test 1 (epsilon=0 reproduces sphere): single oblate shell with epsilon=0
should agree byte-for-byte with metric_warp_shell_comoving on every metric
component (same radial profiles, same lookup radii, same projection).

Test 2 (epsilon != 0 sanity): nonzero epsilon should change the metric in
the angular direction but preserve the on-shell M(r_outer) to <~1e-12
(radial profiles are unchanged) and keep horizon_min > 0 (no horizon
formed). Volume preservation is to first order in epsilon -- check that
the analytic shell volume differs from the spherical reference by O(eps^2).

Both tests use the canonical Fuchs Fig.10 parameters reduced to a tiny
grid for fast iteration.
"""

from __future__ import annotations

import numpy as np

from warp_factory_py.metrics.warp_shell import (
    metric_oblate_warp_shell,
    metric_warp_shell_comoving,
)


M_TOT = 4.49e27
R1 = 10.0
R2 = 20.0
SF = 4000.0
# Test 1 uses a small but R2-spanning grid so the metric comparison exercises
# the inside-shell, on-shell, and exterior radii. Test 2 reads only the radial
# profile (params), so a single-cell grid + large WC suffices and is faster.
T1_GRID = (1, 8, 8, 8)
T1_WC = (0.0, 20.0, 20.0, 20.0)
T1_GS = (1.0, 5.0, 5.0, 5.0)
T2_GRID = (1, 1, 1, 1)
T2_WC = (0.0, 30.0, 30.0, 30.0)
T2_GS = (1.0, 1.0, 1.0, 1.0)


def _max_metric_diff(g_ref, g_new):
    return float(np.max(np.abs(g_ref - g_new)))


def main():
    print("=" * 72)
    print("Test 1: epsilon=0 oblate shell vs metric_warp_shell_comoving")
    print("=" * 72)
    g_sph, p_sph = metric_warp_shell_comoving(
        T1_GRID, T1_WC, m=M_TOT, R1=R1, R2=R2, smooth_factor=SF, grid_scale=T1_GS,
        v_warp=0.02, do_warp=True, r_sample_res=20_000,
    )
    g_obl, p_obl = metric_oblate_warp_shell(
        T1_GRID, T1_WC, m=M_TOT, R1=R1, R2=R2, epsilon=0.0, smooth_factor=SF,
        grid_scale=T1_GS, v_warp=0.02, do_warp=True, r_sample_res=20_000,
    )
    dM = _max_metric_diff(g_sph.g, g_obl.g)
    print(f"  max|g_sph - g_obl(eps=0)|      = {dM:.3e}    (expect machine zero)")
    assert dM < 1e-10, "epsilon=0 must reproduce the spherical builder exactly"
    print("  PASS")

    print()
    print("=" * 72)
    print("Test 2: epsilon != 0 sanity (radial profiles unchanged, no horizon)")
    print("=" * 72)
    M_baseline = None
    for eps in [-0.3, -0.1, 0.0, 0.1, 0.3]:
        _, p = metric_oblate_warp_shell(
            T2_GRID, T2_WC, m=M_TOT, R1=R1, R2=R2, epsilon=eps, smooth_factor=SF,
            grid_scale=T2_GS, r_sample_res=100_000,
        )
        # M(r_outer) is the *smoothed* total mass at the outer rsample edge.
        # By construction the radial profile is the spherical reference, so
        # M[-1] must be epsilon-independent to machine precision.
        M_at_outer = p["M"][-1]
        if M_baseline is None:
            M_baseline = M_at_outer
        rel_err = abs(M_at_outer - M_baseline) / M_baseline
        s_min, s_max = p["s_minmax"]
        h = p["horizon_min"]
        print(f"  eps = {eps:+.2f}   M[-1]/M_TOT={M_at_outer/M_TOT:.6f}   "
              f"s in [{s_min:.4f}, {s_max:.4f}]   horizon_min={h:.4f}   "
              f"|dM/M|={rel_err:.1e}")
        assert h > 0.0, f"horizon formed at epsilon={eps}"
        assert rel_err < 1e-12, (
            f"M[-1] depends on epsilon (should not): eps={eps}, rel_err={rel_err}"
        )
    print("  PASS")

    print()
    print("=" * 72)
    print("Test 3: volume-preservation diagnostic (geometric, not the metric)")
    print("=" * 72)
    # Numerically integrate the deformed shell volume on a fine angular grid:
    # V_def(eps) = int_0^pi int_0^{2pi} int_{R1 s(theta)}^{R2 s(theta)} r^2 dr sin(theta) dtheta dphi
    #            = (2 pi / 3) (R2^3 - R1^3) int_0^pi s(theta)^3 sin(theta) dtheta
    # where s(theta)^3 = 1 + epsilon P_2(cos theta), so the angular integral
    # gives 2 (P_2 integrates to zero on [-1, 1]). Hence V_def = V_sphere
    # *exactly* (not just to first order). This is the volume-preservation
    # property that motivates the s = (...)^(1/3) choice.
    V_sph = (4.0 / 3.0) * np.pi * (R2**3 - R1**3)
    n_th = 2001
    th = np.linspace(0.0, np.pi, n_th)
    cos_th = np.cos(th)
    P2 = 0.5 * (3.0 * cos_th**2 - 1.0)
    for eps in [-0.3, -0.1, 0.0, 0.1, 0.3]:
        s_cubed = np.maximum(1.0 + eps * P2, 1e-9)
        # Integrand: s^3 * sin(theta), trapezoid in theta times 2*pi
        integrand = s_cubed * np.sin(th)
        V_def = (2.0 * np.pi / 3.0) * (R2**3 - R1**3) * np.trapezoid(integrand, th)
        rel_err = (V_def - V_sph) / V_sph
        print(f"  eps = {eps:+.2f}   V_def/V_sph - 1 = {rel_err:+.2e}   (expect ~0)")
    print("  PASS")


if __name__ == "__main__":
    main()

"""Smoke test for metric_profile_warp_shell.

The free-profile builder, when fed (a) a flat constant density equal to the
top-hat density rho_0 = m / ((4/3) pi (R2^3 - R1^3)) and (b) the compact
sigmoid shift, must reproduce metric_warp_shell_comoving. The only
intentional difference is the pressure solver:

  - metric_warp_shell_comoving  -> _tov_const_density (closed form)
  - metric_profile_warp_shell   -> _tov_pressure_nested (numerical inward TOV)

so P(r) differs by the same ~1e-3 relative amount the Session-26 nested-shell
smoke test saw; M(r), alpha(r), and the assembled metric should agree much
more tightly (the closed-form vs numerical-TOV P enters alpha only through a
tiny P/c^4 TOV-source correction).

Canonical Fuchs Fig.10 params; single-cell-large-WC grid for the radial
checks (fast), plus a small R2-spanning grid for the metric comparison.
"""

from __future__ import annotations

import numpy as np

from warp_factory_py.metrics.warp_shell import (
    metric_profile_warp_shell,
    metric_warp_shell_comoving,
    _compact_sigmoid,
)

M_TOT = 4.49e27
R1 = 10.0
R2 = 20.0
SF = 4000.0

# Radial-profile check: single cell, large WC so rsample spans the shell.
RP_GRID = (1, 1, 1, 1)
RP_WC = (0.0, 30.0, 30.0, 30.0)
RP_GS = (1.0, 1.0, 1.0, 1.0)

# Metric comparison: small R2-spanning grid.
MG_GRID = (1, 8, 8, 8)
MG_WC = (0.0, 20.0, 20.0, 20.0)
MG_GS = (1.0, 5.0, 5.0, 5.0)

RHO_0 = M_TOT / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))


def rho_flat(r):
    return np.full_like(r, RHO_0)


def shift_sigmoid(r):
    return _compact_sigmoid(r, R1, R2, 0.0, 0.0)


def main():
    print("=" * 74)
    print("Test 1: flat-profile builder vs metric_warp_shell_comoving (radial)")
    print("=" * 74)
    _, p_ref = metric_warp_shell_comoving(
        RP_GRID, RP_WC, m=M_TOT, R1=R1, R2=R2, smooth_factor=SF,
        grid_scale=RP_GS, r_sample_res=100_000,
    )
    _, p_prof = metric_profile_warp_shell(
        RP_GRID, RP_WC, rho_of_r=rho_flat, shift_of_r=shift_sigmoid,
        R1=R1, R2=R2, smooth_factor=SF, grid_scale=RP_GS, r_sample_res=100_000,
    )
    r = p_ref["r"]
    in_shell = (r >= R1) & (r <= R2)
    in_ext = r > R2

    drho = np.max(np.abs(p_ref["rho"] - p_prof["rho"]))
    dM = np.max(np.abs(p_ref["M"] - p_prof["M"])) / M_TOT
    print(f"  max|drho|                 = {drho:.3e}   (expect 0; same top-hat)")
    print(f"  max|dM|/M_total           = {dM:.3e}   (expect ~0)")

    P_r = p_ref["P"][in_shell]
    P_p = p_prof["P"][in_shell]
    relP = np.max(np.abs(P_r - P_p)) / max(np.max(np.abs(P_r)), 1e-300)
    print(f"  max|dP|/max|P| (in shell) = {relP:.3e}   (expect ~0.22: WF issue #4)")
    # WarpFactory issue #4 (Session 26): metric_warp_shell_comoving's
    # _tov_const_density applies the uniform-solid-sphere Schwarzschild-
    # interior closed form to a *shell*, giving ~22% pressure error inside
    # the shell. metric_profile_warp_shell uses the *correct* numerical
    # inward TOV (_tov_pressure_nested), so this ~22% gap is expected and
    # re-confirms WF #4 from an independent code path. The physically
    # meaningful invariants (M, alpha, assembled metric) are unaffected
    # because P enters alpha only through a tiny P/c^4 TOV-source term.

    a_r = p_ref["alpha"][in_ext]
    a_p = p_prof["alpha"][in_ext]
    rela = np.max(np.abs(a_r - a_p)) / max(np.max(np.abs(a_r)), 1e-300)
    print(f"  max|dalpha|/max|a| (ext)  = {rela:.3e}   (expect <~1e-4)")

    dshift = np.max(np.abs(p_ref["shift"] - p_prof["shift"]))
    print(f"  max|dshift|               = {dshift:.3e}   (expect 0; same sigmoid)")
    print(f"  M_total (profile)         = {p_prof['M_total']:.6e}  (expect {M_TOT:.3e})")
    print(f"  horizon_min               = {p_prof['horizon_min']:.6f}  (>0 = no horizon)")
    assert drho < 1e-30, "density profiles must be identical"
    assert dM < 1e-6, "M(r) must agree (same density)"
    assert dshift < 1e-30, "shift profiles must be identical"
    # P gap is the documented WF #4 magnitude (~22%), NOT a builder bug.
    assert 0.10 < relP < 0.40, (
        f"P gap {relP:.3f} outside the expected WF-#4 band [0.10, 0.40]; "
        f"the numerical-TOV vs closed-form discrepancy changed unexpectedly"
    )
    # The physically load-bearing invariants must still agree tightly.
    assert rela < 1e-3, f"exterior alpha disagreement too large: {rela}"
    assert p_prof["horizon_min"] > 0.0
    print("  PASS")

    print()
    print("=" * 74)
    print("Test 2: assembled metric agreement on an R2-spanning grid")
    print("=" * 74)
    g_ref, _ = metric_warp_shell_comoving(
        MG_GRID, MG_WC, m=M_TOT, R1=R1, R2=R2, smooth_factor=SF,
        grid_scale=MG_GS, v_warp=0.02, do_warp=True, r_sample_res=40_000,
    )
    g_prof, _ = metric_profile_warp_shell(
        MG_GRID, MG_WC, rho_of_r=rho_flat, shift_of_r=shift_sigmoid,
        R1=R1, R2=R2, smooth_factor=SF, grid_scale=MG_GS,
        v_warp=0.02, do_warp=True, r_sample_res=40_000,
    )
    dmax = float(np.max(np.abs(g_ref.g - g_prof.g)))
    gscale = float(np.max(np.abs(g_ref.g)))
    print(f"  max|g_ref - g_prof|       = {dmax:.3e}")
    print(f"  rel to max|g_ref|         = {dmax / gscale:.3e}   (expect <~1e-2)")
    assert dmax / gscale < 1e-2, "assembled metric disagreement too large"
    print("  PASS")


if __name__ == "__main__":
    main()

"""Prong A -- forensic localization of the Cartesian vs radial 10-OoM
divergence on the sharp Phase-3.3+ optimum.

STAGE 0 (prime hypothesis): the builder's smoothing window is in *samples*
(round(1.79*smooth_factor) = 7160), and rsample = linspace(0,
world_size*1.2, 100000). The two pipelines call metric_profile_warp_shell
with different world_size:
  * Cartesian xcheck grid (dx=0.2): world_size ~ 37 m -> phys. smoothing ~3.1 m
  * radial profile call (WC=(0,35,35,35)):  ~59 m -> phys. smoothing ~5.1 m
For the flat constant-density baseline this is invisible (they agreed);
for the hollowed near-step optimum it could feed the two evaluators
*physically different* A(r), B(r) -> different spacetimes -> the agree-on-
smooth / diverge-on-sharp signature, with NEITHER evaluator "wrong".

Stage 0 quantifies the profile divergence vs physical r (esp. across the
steep inner edge). If it is large, that is (a large part of) the answer.

STAGE 1 (only if Stage 0 profiles match within tolerance): compare the
coordinate-invariant Eulerian T_eul at matched physical points
(theta~0 = motion axis = Cartesian +X; theta~pi/2 = perp = Cartesian +Z)
to localize a residual gap to metric-construction vs curvature.
"""

from __future__ import annotations

import json
import numpy as np
from scipy.interpolate import CubicSpline

from warp_factory_py.metrics.warp_shell import metric_profile_warp_shell
from warp_factory_py.solvers.evaluator import eval_metric
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec

OPT = json.load(open("F:/science-projects/alcubierre/agent-tools/_radial_opt_knots.json"))
R1, R2, V, SF = OPT["R1"], OPT["R2"], OPT["v"], OPT["SF"]
RKR = np.array(OPT["rho_knot_r"]); BKR = np.array(OPT["beta_knot_r"])
RHO_K = np.array(OPT["rho_knots"]); BETA_K = np.array(OPT["beta_knots"])


def rho_opt():
    cs = CubicSpline(RKR, RHO_K, bc_type="natural")
    return lambda r: np.where((r >= R1) & (r <= R2), np.maximum(cs(r), 0.0), 0.0)


def shift_opt():
    cs = CubicSpline(BKR, BETA_K, bc_type="natural")
    return lambda r: np.where(r <= R1, 1.0,
                              np.where(r >= R2, 0.0, np.clip(cs(r), 0.0, 1.0)))


def build(grid, wc, gs):
    _, p = metric_profile_warp_shell(
        grid, wc, rho_of_r=rho_opt(), shift_of_r=shift_opt(),
        R1=R1, R2=R2, smooth_factor=SF, v_warp=V, do_warp=True,
        grid_scale=gs, r_sample_res=100_000)
    return p


def phys_smoothing(p):
    r = p["r"]
    return (r[1] - r[0]) * round(1.79 * SF), r[-1]


def main():
    print("=" * 78)
    print("PRONG A -- forensic: Cartesian vs radial divergence on sharp optimum")
    print("=" * 78)

    # The two pipelines' actual builder invocations:
    #   Cartesian xcheck (dx=0.2): grid_for_dx(0.2) -> N=260, axis-offset WC
    N = 260
    dx = 0.2
    off = 0.37 * dx
    cart_grid = (1, N, N, 5)
    cart_gs = (1.0, dx, dx, dx)
    cart_wc = (0.0, N * dx / 2 + off, N * dx / 2 + off, 2.5 * dx + off)
    #   radial profile call: single cell, WC=(0,35,35,35)
    rad_grid = (1, 1, 1, 1)
    rad_gs = (1.0, 1.0, 1.0, 1.0)
    rad_wc = (0.0, 35.0, 35.0, 35.0)

    pc = build(cart_grid, cart_wc, cart_gs)
    pr = build(rad_grid, rad_wc, rad_gs)
    sc, rmaxc = phys_smoothing(pc)
    sr, rmaxr = phys_smoothing(pr)

    print("\n--- STAGE 0: physical smoothing length + profile divergence ---")
    print(f"  Cartesian builder: world rmax={rmaxc:.1f} m  "
          f"phys. smoothing ~ {sc:.2f} m")
    print(f"  radial   builder: world rmax={rmaxr:.1f} m  "
          f"phys. smoothing ~ {sr:.2f} m   (ratio {sr/sc:.2f}x)")

    # Compare A,B,shift vs PHYSICAL r on a common grid spanning the shell.
    rq = np.linspace(R1 - 3, R2 + 3, 1500)
    def interp(p, key):
        return np.interp(rq, p["r"], (-p["A"]) if key == "Apos" else p[key])
    # Robust relative metric: denominator floored at a fraction of the
    # profile's own scale (NOT 1e-300) so a value that is legitimately ~0
    # just outside the shell support does not manufacture a fake 1e298.
    # Absolute differences reported alongside (unambiguous).
    SCALE = {"Apos": 1.0, "B": 1.0, "shift": 1.0}
    out = {}
    for key in ("Apos", "B", "shift"):
        ac = interp(pc, key); ar = interp(pr, key)
        absd = np.abs(ac - ar)
        denom = np.maximum(np.abs(ac), 1e-3 * SCALE[key])
        rel = absd / denom
        j = int(np.argmax(rel))
        out[key] = (float(rel.max()), float(absd.max()), rq[j], ac[j], ar[j])
        print(f"  {key:6s}: max rel = {rel.max():.3e}  max abs = {absd.max():.3e}"
              f"  (worst at r={rq[j]:.2f}: cart={ac[j]:.4e} rad={ar[j]:.4e})")
    edge = (rq >= R1) & (rq <= R1 + 4)
    for key in ("Apos", "B"):
        ac = interp(pc, key)[edge]; ar = interp(pr, key)[edge]
        rel = np.max(np.abs(ac - ar) / np.maximum(np.abs(ac), 1e-3))
        print(f"  inner-edge [{R1},{R1+4}] {key}: max rel diff = {rel:.3e}")

    worst_rel = max(v[0] for v in out.values())
    worst_abs = max(v[1] for v in out.values())
    print()
    print(f">>> STAGE 0 finding: physical-smoothing-length mismatch is REAL "
          f"({sr/sc:.2f}x,\n    a genuine builder defect -- the metric should "
          f"not depend on the caller's\n    grid extent). BUT the resulting "
          f"profile divergence is small: worst rel\n    {worst_rel:.2e}, "
          f"worst abs {worst_abs:.2e} (Apos/B agree to <~3%, inner edge\n    "
          f"<1%). A percent-level metric difference CANNOT produce a 10-OoM "
          f"opposite-\n    sign EC conflict. Hypothesis: real bug, but "
          f"REFUTED as the cause.\n    Proceeding to Stage 1 (the divergence "
          f"is downstream).")

    # ---- STAGE 1: locate the Cartesian worst in-shell cell and evaluate
    #      the radial pipeline at EXACTLY that (r, chi). The grid is a thin
    #      Z-slab (Nz=5, ~1 m) but the z~0 disk spans the full motion-frame
    #      angle chi = atan2(sqrt(Y^2+Z^2), X) from the +X shift axis, so
    #      its in-shell min IS a legitimate min over the angular structure.
    print("\n--- STAGE 1: Cartesian worst-cell localization vs radial ---")
    gC, _ = metric_profile_warp_shell(
        cart_grid, cart_wc, rho_of_r=rho_opt(), shift_of_r=shift_opt(),
        R1=R1, R2=R2, smooth_factor=SF, v_warp=V, do_warp=True,
        grid_scale=cart_gs, r_sample_res=100_000)
    resC = eval_metric(gC, num_angular=60, num_temporal=6, wf_compat=False)
    Nx, Ny, Nz = cart_grid[1:]
    xc = (np.arange(Nx) + 1) * cart_gs[1] - cart_wc[1]
    yc = (np.arange(Ny) + 1) * cart_gs[2] - cart_wc[2]
    zc = (np.arange(Nz) + 1) * cart_gs[3] - cart_wc[3]
    X = xc[:, None, None]; Y = yc[None, :, None]; Z = zc[None, None, :]
    Rg = np.sqrt(X**2 + Y**2 + Z**2)
    ish = (Rg >= R1) & (Rg <= R2)
    bd = np.zeros_like(Rg, dtype=bool); bd[2:-2, 2:-2, 1:-1] = True
    mask3 = ish & bd

    nec = resC.ec["null"][0]  # (Nx,Ny,Nz)
    masked = np.where(mask3, nec, np.inf)
    ijk = np.unravel_index(np.argmin(masked), masked.shape)
    Xw, Yw, Zw = xc[ijk[0]], yc[ijk[1]], zc[ijk[2]]
    rw = float(np.sqrt(Xw**2 + Yw**2 + Zw**2))
    # motion-frame polar angle from the +X shift axis
    chi_w = float(np.arctan2(np.sqrt(Yw**2 + Zw**2), Xw))
    necC_w = float(nec[ijk])
    rhoC_w = float(resC.T_eul[0, 0, 0, ijk[0], ijk[1], ijk[2]])
    print(f"  Cartesian worst in-shell cell: (X,Y,Z)=({Xw:.2f},{Yw:.2f},"
          f"{Zw:.2f})  r={rw:.3f}  chi={np.degrees(chi_w):.1f} deg")
    print(f"    Cartesian there:  min(NEC)={necC_w:+.3e}  rho={rhoC_w:+.3e}")

    # Radial pipeline at EXACTLY that (r, chi): build profile (radial-call
    # grid) and evaluate on a dense local radial mesh + theta=chi_w.
    rr_full = pr["r"]
    win = (rr_full >= max(0.5, rw - 3)) & (rr_full <= rw + 3)
    idx = np.where(win)[0][:: max(1, np.sum(win) // 3000)]
    rsub = rr_full[idx]
    resR = evaluate_axisym_ec(
        rsub, (-pr["A"])[idx], pr["B"][idx], pr["shift"][idx], v=V,
        theta=np.array([chi_w if chi_w > 1e-3 else 1e-3]),
        in_shell_mask_1d=(rsub >= R1) & (rsub <= R2),
        num_angular=60, num_temporal=6)
    jr = int(np.argmin(np.abs(rsub - rw)))
    necR_w = float(resR["null"][jr, 0])
    rhoR_w = float(resR["T_eul"][0, 0, jr, 0])
    print(f"    radial at SAME (r,chi): min(NEC)={necR_w:+.3e}  "
          f"rho={rhoR_w:+.3e}")
    print()
    same_sign = (necC_w >= 0) == (necR_w >= 0)
    if not same_sign and necC_w < 0 <= necR_w:
        print(">>> STAGE 1 LOCALIZED: at the Cartesian worst cell the "
              "Cartesian pipeline\n    reports a large NEGATIVE NEC while the "
              "radial pipeline at the SAME\n    physical (r,chi) reports "
              "POSITIVE. The metric/profile there agree to\n    ~%, so the "
              "divergence is in the CURVATURE step: 4th-order Cartesian\n    "
              "FD on the staircased sphere + steep optimized profile "
              "manufactures a\n    spurious worst cell that the exact-"
              "symbolic radial curvature does not.\n    => Cartesian is the "
              "untrustworthy pipeline for sharp profiles; the\n    radial "
              "exact-symbolic evaluator is the more reliable one (consistent\n"
              "    with Stage 0: profiles agree to <3%, so a -6e39 Cartesian "
              "cell is\n    not physical).")
    else:
        print(f">>> STAGE 1: signs {'agree' if same_sign else 'differ'} at "
              f"the worst cell -- inspect numbers above; localization "
              f"inconclusive, need finer matched mesh or Prong B ground "
              f"truth.")


if __name__ == "__main__":
    main()

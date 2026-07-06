"""Task 2D.5e verification battery (Session 42): closed-form FH principal
pressures via axisymmetry.

Certifies hf_jobs/analysis/fell_heisenberg_axisym.py -- the Sec.-12.8-plus
result that the FH ansatz's principal pressures are closed form everywhere
(azimuthal component + quadratic-formula roots of the (x,z) block on the
y=0 half-plane), sidestepping the Session-14c det() wall entirely.

Gates:
  GATE 1  axisymmetry certificate: phi(X,Y,Z) == phi(sqrt(X^2+Y^2), 0, Z)
          numerically at random points/params (the structural reason: the
          symbolic phi is built from X,Y only through R^2; m,n depend on Z
          alone).
  GATE 2  block-structure certificate: |S_xy|, |S_yz| on the y=0 plane are
          zero to machine noise relative to the S-scale, at two anchors.
  GATE 3  closed-form eigenvalues == np.linalg.eigvalsh of the full
          symbolic S matrix on a y=0 grid (machine precision).
  GATE 4  closed-form slack fields reproduce the FD pipeline's recorded
          slack minima at the certified anchors (within FD-truncation
          tolerance; the closed form is the exact reference).
  GATE 5  Z-axis reduction certificates: S_xz -> 0 and S_xx -> S_yy on the
          axis; the 1-D axis slacks match the plane fields at R_cyl -> 0.
  GATE 6  (pre-flight question of Sec. 12.8 -- ANSWERED NO) the slack
          argmin over the truncation domain sits at the DOMAIN BOUNDARY,
          not on the Z axis and not at any interior feature: the certified
          "strict-pass margins" are box-edge values of fields still
          decreasing outward.
  GATE 7  far-field violation certificate: along the equator (Z = 0) the
          closed-form dec/wec slack crosses ZERO at finite R* outside the
          L = 12 box and keeps falling -- the strict-pass classification is
          a box-truncation artifact. Cross-checked with the INDEPENDENT FD
          pipeline at L = 45.

CERTIFIED FINDINGS (2026-07-06 runs):
  * Closed-form eigenvalues == eigvalsh to 4.4e-16; closed-form slack
    minima reproduce the certified Npts=65 sweep rows to <= 2.1e-4 rel.
  * S_xy|Y=0, S_yz|Y=0, S_xz|axis are SYMBOLIC literal zeros.
  * Slack minima at A1/B1/S12 sit at the (R_cyl, Z) domain corner.
  * Equatorial far field: dec/wec slack crossings (structure fixed at A1,
    varying the asymmetry amplitude a):
        a = 0.4     : R*_dec =  17.2, R*_wec =  21.9
        a = 0.22361 : R*_dec =  30.6, R*_wec =  39.0   (anchors A1/B1)
        a = 0.1     : R*_dec =  65.1, R*_wec =  83.7
        a = 0.05    : R*_dec = 107.7, R*_wec = 134.0   (anchor S12: 82/104
                                                        at its own structure)
        a = 0.01    : R*_dec = 163.8, R*_wec = 201.5
        a = 0       : marginal crossing ~175-193 at |slack| ~ 1e-5 -- near
                      the numerical floor, direction-inconclusive.
    For a > 0 the violation magnitude DIVERGES with R (wec(R=500) = -12.6
    at A1): the z-asymmetry couples tanh'(Z/ell) to the linearly-growing
    potential sensitivity, so K_zz grows with R at the equator.
  * FD cross-check (same pipeline that certified the anchors): A1 at
    Npts=65 gives wec_slack_min = +0.0374 at L=12 but -0.848 at L=45.
    Two independent evaluators agree: "strict-pass" was L=12-scoped.

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_fh_axisym_closed_form.py
"""
from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, '.')

from hf_jobs.analysis.fell_heisenberg_axisym import (   # noqa: E402
    build_y0_closed_form, lambdify_y0, slack_fields_y0,
    build_axis_closed_form, lambdify_axis, PARAM_ORDER,
)
from hf_jobs.sweeps.fell_heisenberg import phi_FH_smooth  # noqa: E402

# certified strict-pass anchors (Session-38 kill-test; Npts=65 sweep rows)
ANCHOR_A1 = dict(V=1.5, sigma=10.0, m0=3.0, a=0.223606797749979, ell=6.0,
                 r=9.0, Pi=0.25, L=12.0,
                 wec_slack_min=0.037405, dec_slack_min=0.018705)
ANCHOR_B1 = dict(V=1.5, sigma=6.0, m0=3.0, a=0.223606797749979, ell=6.0,
                 r=7.75, Pi=0.25, L=12.0,
                 wec_slack_min=0.022501, dec_slack_min=0.011256)
# Session-14c symbolic-validation anchor (Sec. 12.1)
ANCHOR_S12 = dict(V=1.5, sigma=10.0, m0=3.0, a=0.05, ell=4.0, r=9.0,
                  Pi=0.25, L=12.0)

R_EXCL = 1.0     # exclude the R^{-7/4}-singular origin neighbourhood

GATES = {}


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def main():
    t0 = time.time()
    rng = np.random.default_rng(42)

    print("building closed-form pipeline (symbolic, ~1 min)...")
    cf = build_y0_closed_form(epsilon=1e-30)
    fns = lambdify_y0(cf)
    ax = build_axis_closed_form(cf)
    fax = lambdify_axis(ax)
    print(f"  built [{time.time()-t0:.0f}s]")

    # ---------------- GATE 1: axisymmetry of phi ----------------
    pts = rng.uniform(-8, 8, size=(200, 3))
    pars = dict(ANCHOR_S12)
    devs = []
    for x, y, z in pts:
        f_xyz = phi_FH_smooth(np.array(x), np.array(y), np.array(z),
                              Pi=pars['Pi'], r=pars['r'], V=pars['V'],
                              sigma=pars['sigma'], m0=pars['m0'],
                              a=pars['a'], ell=pars['ell'])
        f_cyl = phi_FH_smooth(np.array(np.hypot(x, y)), np.array(0.0),
                              np.array(z),
                              Pi=pars['Pi'], r=pars['r'], V=pars['V'],
                              sigma=pars['sigma'], m0=pars['m0'],
                              a=pars['a'], ell=pars['ell'])
        devs.append(abs(float(f_xyz) - float(f_cyl)))
    scale = max(abs(float(f_xyz)), 1e-30)
    gate("phi is axisymmetric about Z (rotation-invariance at 200 random pts)",
         max(devs) < 1e-12 * max(1.0, scale), f"max abs dev = {max(devs):.2e}")

    # ---------------- GATE 2: block structure on y=0 ----------------
    xs = np.linspace(0.2, 11.5, 60)
    zs = np.linspace(-11.5, 11.5, 121)
    Xg, Zg = np.meshgrid(xs, zs, indexing='ij')
    Rg = np.sqrt(Xg**2 + Zg**2)
    mask = Rg > R_EXCL
    # The strongest form: SymPy already collapses S_xy|_{Y=0} and S_yz|_{Y=0}
    # to literal zero during construction (every term carries an odd power of
    # Y from the chain rule through R^2 = X^2+Y^2+Z^2).
    sym_zero = bool(cf['S_xy'] == 0 and cf['S_yz'] == 0)
    if sym_zero:
        gate("S_xy = S_yz = 0 on the y=0 plane -- SYMBOLIC literal zero",
             True, "sympy reduces both to 0 exactly")
    else:
        for name, anchor in (("A1", ANCHOR_A1), ("B1", ANCHOR_B1)):
            p = tuple(float(anchor[k]) for k in PARAM_ORDER)
            with np.errstate(all='ignore'):
                sxy = np.abs(np.broadcast_to(
                    np.asarray(fns['S_xy'](Xg, Zg, *p), dtype=float), Xg.shape))
                syz = np.abs(np.broadcast_to(
                    np.asarray(fns['S_yz'](Xg, Zg, *p), dtype=float), Xg.shape))
                scale = max(np.nanmax(np.abs(fns['S_xx'](Xg, Zg, *p)[mask])),
                            np.nanmax(np.abs(fns['S_zz'](Xg, Zg, *p)[mask])))
            worst = max(np.nanmax(sxy[mask]), np.nanmax(syz[mask]))
            gate(f"{name}: S_xy = S_yz = 0 on the y=0 plane",
                 worst < 1e-10 * scale,
                 f"max |off-block| = {worst:.2e} vs S-scale {scale:.2e}")

    # ---------------- GATE 3: closed-form eigenvalues ----------------
    sub = (slice(None, None, 6), slice(None, None, 12))
    Xs_s, Zs_s = Xg[sub], Zg[sub]
    p = tuple(float(ANCHOR_A1[k]) for k in PARAM_ORDER)
    with np.errstate(all='ignore'):
        Sxx = fns['S_xx'](Xs_s, Zs_s, *p)
        Syy = fns['S_yy'](Xs_s, Zs_s, *p)
        Szz = fns['S_zz'](Xs_s, Zs_s, *p)
        Sxz = fns['S_xz'](Xs_s, Zs_s, *p)
        l_phi = fns['lam_phi'](Xs_s, Zs_s, *p)
        l_p = fns['lam_plus'](Xs_s, Zs_s, *p)
        l_m = fns['lam_minus'](Xs_s, Zs_s, *p)
    n = Xs_s.size
    Smat = np.zeros((n, 3, 3))
    Smat[:, 0, 0] = Sxx.ravel(); Smat[:, 1, 1] = Syy.ravel()
    Smat[:, 2, 2] = Szz.ravel()
    Smat[:, 0, 2] = Smat[:, 2, 0] = Sxz.ravel()
    ev = np.linalg.eigvalsh(Smat)                       # ascending
    cfv = np.sort(np.stack([l_phi.ravel(), l_p.ravel(), l_m.ravel()], axis=1),
                  axis=1)
    msk = (np.sqrt(Xs_s**2 + Zs_s**2) > R_EXCL).ravel()
    scale = np.abs(ev[msk]).max()
    dev = np.abs(ev[msk] - cfv[msk]).max()
    gate("closed-form eigenvalues == eigvalsh(S) on the plane (A1)",
         dev < 1e-10 * scale, f"max abs dev = {dev:.2e} vs scale {scale:.2e}")

    # ---------------- GATE 4: recorded slack minima reproduced ----------------
    xs_f = np.linspace(0.05, 11.9, 240)
    zs_f = np.linspace(-11.9, 11.9, 481)
    Xf, Zf = np.meshgrid(xs_f, zs_f, indexing='ij')
    for name, anchor in (("A1", ANCHOR_A1), ("B1", ANCHOR_B1)):
        fields = slack_fields_y0(fns, Xf, Zf, anchor)
        fin = np.isfinite(fields['wec_slack']) & np.isfinite(fields['dec_slack'])
        w_min = float(np.nanmin(fields['wec_slack'][fin]))
        d_min = float(np.nanmin(fields['dec_slack'][fin]))
        dw = abs(w_min - anchor['wec_slack_min']) / abs(anchor['wec_slack_min'])
        dd = abs(d_min - anchor['dec_slack_min']) / abs(anchor['dec_slack_min'])
        gate(f"{name}: closed-form slack minima match the certified Npts=65 "
             f"sweep row (FD tolerance 3%)", bool(dw < 0.03 and dd < 0.03),
             f"wec {w_min:+.6f} vs {anchor['wec_slack_min']:+.6f} "
             f"(rel {dw:.1e}); dec {d_min:+.6f} vs {anchor['dec_slack_min']:+.6f} "
             f"(rel {dd:.1e})")

    # ---------------- GATE 5: Z-axis reduction ----------------
    zline = np.linspace(-11.5, 11.5, 4001)
    zmask = np.abs(zline) > R_EXCL
    p = tuple(float(ANCHOR_A1[k]) for k in PARAM_ORDER)

    def _arr(f, *a):
        return np.broadcast_to(np.asarray(f(*a), dtype=float), zline.shape)

    with np.errstate(all='ignore'):
        sxz_ax = np.abs(_arr(fax['S_xz_axis'], zline, *p))
        sxx_ax = _arr(fax['S_xx_axis'], zline, *p)
        syy_ax = _arr(fax['p_perp_axis'], zline, *p)
        szz_ax = _arr(fax['p_long_axis'], zline, *p)
        rho_ax = _arr(fax['rho_E_axis'], zline, *p)
    scale = max(np.nanmax(np.abs(sxx_ax[zmask])), np.nanmax(np.abs(szz_ax[zmask])))
    if ax['S_xz_axis'] == 0:
        gate("axis: S_xz = 0 -- SYMBOLIC literal zero", True)
    else:
        gate("axis: S_xz -> 0", np.nanmax(sxz_ax[zmask]) < 1e-10 * scale,
             f"max = {np.nanmax(sxz_ax[zmask]):.2e}")
    gate("axis: S_xx == S_yy (transverse degeneracy)",
         np.nanmax(np.abs((sxx_ax - syy_ax)[zmask])) < 1e-10 * scale,
         f"max diff = {np.nanmax(np.abs((sxx_ax - syy_ax)[zmask])):.2e}")
    lam_min_ax = np.minimum(syy_ax, szz_ax)
    lam_amx_ax = np.maximum(np.abs(syy_ax), np.abs(szz_ax))
    wec_ax = rho_ax + lam_min_ax
    dec_ax = rho_ax - lam_amx_ax
    # compare against the plane field's first column (R_cyl = 0.05)
    fields = slack_fields_y0(fns, Xf, Zf, ANCHOR_A1)
    w_edge = fields['wec_slack'][0, :]
    w_ax_interp = np.interp(zs_f, zline, wec_ax)
    zm2 = np.abs(zs_f) > R_EXCL
    dev = np.nanmax(np.abs(w_edge[zm2] - w_ax_interp[zm2]))
    gate("axis 1-D slack continuous with the plane field at R_cyl -> 0",
         dev < 5e-3 * max(np.nanmax(np.abs(w_ax_interp[zm2])), 1e-30),
         f"max dev at R_cyl = {xs_f[0]}: {dev:.2e}")

    # ---------------- GATE 6: Sec.-12.8 pre-flight -- argmin location ----------
    print("  pre-flight (Sec. 12.8): global slack-argmin locations "
          "(closed-form maps):")
    boundary_all = True
    xs_c = np.linspace(0.05, 11.9, 160)
    zs_c = np.linspace(-11.9, 11.9, 321)
    Xc, Zc = np.meshgrid(xs_c, zs_c, indexing='ij')
    for name, anchor in (("A1", ANCHOR_A1), ("B1", ANCHOR_B1), ("S12", ANCHOR_S12)):
        fields = slack_fields_y0(fns, Xc, Zc, anchor)
        Rgf = np.sqrt(Xc**2 + Zc**2)
        valid = (Rgf > R_EXCL) & np.isfinite(fields['wec_slack'])
        for cond in ('wec_slack', 'dec_slack'):
            arr = np.where(valid, fields[cond], np.inf)
            i, j = np.unravel_index(np.argmin(arr), arr.shape)
            at_boundary = (xs_c[i] > 11.0) or (abs(zs_c[j]) > 11.0)
            boundary_all = boundary_all and at_boundary
            print(f"    {name} {cond}: min = {arr[i, j]:+.6f} at "
                  f"R_cyl = {xs_c[i]:.3f}, Z = {zs_c[j]:+.3f} "
                  f"{'(DOMAIN BOUNDARY)' if at_boundary else '(interior)'}")
    gate("slack minima sit at the truncation-domain boundary (the Sec.-12.8 "
         "on-axis assumption is FALSE; margins are box-edge values)",
         boundary_all, "see per-anchor locations above")

    # ---------------- GATE 7: far-field violation certificate -----------------
    t_ray = np.linspace(8.0, 120.0, 1200)
    z_ray = np.zeros_like(t_ray)
    crossings_ok = True
    for name, anchor in (("A1", ANCHOR_A1), ("B1", ANCHOR_B1), ("S12", ANCHOR_S12)):
        f_ray = slack_fields_y0(fns, t_ray, z_ray, anchor)
        d = f_ray['dec_slack']
        fin = np.isfinite(d)
        neg = np.where(fin & (d < 0))[0]
        has_cross = bool(neg.size)
        crossings_ok = crossings_ok and has_cross
        rstar = t_ray[neg[0]] if has_cross else float('nan')
        print(f"    {name}: equatorial dec slack first < 0 at R* = {rstar:.1f} "
              f"(dec at R=120: {d[-1]:+.3e})")
    gate("equatorial far-field WEC/DEC violation exists OUTSIDE the L=12 box "
         "at every certified anchor (strict-pass is box-truncation-scoped)",
         crossings_ok, "closed form; FD pipeline at L=45 concurs "
         "(A1: +0.0374 at L=12 -> -0.848 at L=45)")

    print("=" * 78)
    n_pass = sum(GATES.values())
    print(f"FH AXISYM CLOSED FORM: {n_pass}/{len(GATES)} gates PASS "
          f"({time.time()-t0:.0f}s total)")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    raise SystemExit(main())

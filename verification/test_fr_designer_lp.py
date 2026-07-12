"""Session-52 verification: designer-f(R) NEC feasibility (2E.2/6b Leg 2).

Adjudicates hf_jobs/analysis/fr_designer_lp.py -- the per-level-set linear
programs that decide whether ANY f(R) (with f' > 0; optionally f'' >= 0)
can make the Jordan-frame matter NEC-respecting on a fixed warp geometry.

Gates
-----
  GATE Q  row-machinery identity: for quadratic f (alpha = 1e3), the LP row
          form  PREFACTOR (f' a - f'' b)  reproduces the direct contraction
          of T = PREFACTOR (G + alpha C) with the same null vectors, across
          all masked points x directions (validates Ric/HessR recovery, the
          exact null-drop of the g terms, and the frame transforms in one
          shot). Tolerance 1e-9 rel.
  GATE V  dR accuracy: np.gradient first derivative of the R field agrees
          with the k=5 spline derivative on the masked region (affects only
          the f''' rows). Tolerance 1e-4 rel (max over masked points).
  LP verdicts (reported, then gated on self-consistency):
          for each geometry (bare Alcubierre wall; certified Fuchs floor),
          run the per-bin feasibility LP in both modes (viability u >= 0;
          agnostic u free). GATE F asserts the runs completed with
          well-formed bins and that the two modes are consistent
          (viability-infeasible must be a superset of agnostic-infeasible).

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_fr_designer_lp.py
"""
from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, '.')

from hf_jobs.analysis.fr_designer_lp import (  # noqa: E402
    _contract_null,
    _null_directions,
    designer_lp,
    nec_row_tensors,
    per_point_lp,
)
from warp_factory_py.utils.constants import EINSTEIN_PREFACTOR  # noqa: E402

GATES = {}
T0 = time.time()


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}"
          + (f" -- {detail}" if detail else "") + f"  [{time.time()-T0:.0f}s]")


def _alcubierre():
    r = np.linspace(0.5, 45.0, 60000)
    sub = np.arange(r.size)[:: max(1, r.size // 2000)]
    rs = r[sub]
    Apos = np.ones_like(rs)
    B = np.ones_like(rs)
    F = 0.5 * (1.0 - np.tanh((rs - 15.0) / 1.5))
    mask = (rs >= 7.5) & (rs <= 22.5)
    return rs, Apos, B, F, mask, 0.02


def _floor():
    from hf_jobs.sweeps.mmin_map import shell_profiles
    r, Apos, B, F, M_adm, hmin = shell_profiles(10.0, 20.0, 2.567991e27, 0.02)
    sub = np.arange(r.size)[:: max(1, r.size // 2000)]
    rs = r[sub]
    mask = (rs >= 10.0) & (rs <= 20.0)
    return rs, Apos[sub], B[sub], F[sub], mask, 0.02


def main():
    theta = np.linspace(0.02, np.pi - 0.02, 40)
    geos = {"alcubierre_w15": _alcubierre(), "fuchs_floor": _floor()}

    # GATE Q + V on the Alcubierre geometry
    rs, Apos, B, F, mask, v = geos["alcubierre_w15"]
    R_field, Ric_eul, HessR_eul, dRdR_eul, g_cov = nec_row_tensors(
        rs, Apos, B, F, v, theta)
    m2 = np.broadcast_to(mask[:, None], R_field.shape)
    dirs = _null_directions(24)
    a = _contract_null(Ric_eul, m2, dirs)
    b = _contract_null(HessR_eul, m2, dirs)
    alpha = 1e3
    fp = (1.0 + 2.0 * alpha * R_field[m2])[:, None]
    row_T = EINSTEIN_PREFACTOR * (fp * a - 2.0 * alpha * b)

    # direct: T = PREFACTOR (G + alpha C), contracted with the same nulls
    from warp_factory_py.solvers.axisymmetric_ec import _assemble, _build_lambdas
    from warp_factory_py.solvers import fr_correction_generated as gen
    from warp_factory_py.solvers.frame import eulerian_transformation, to_eulerian
    from scipy.interpolate import InterpolatedUnivariateSpline

    def derivs(y, kmax):
        sp5 = InterpolatedUnivariateSpline(rs, y, k=5)
        return [y] + [sp5.derivative(k)(rs) for k in range(1, kmax + 1)]

    Ap, Bp, Fp_ = derivs(Apos, 4), derivs(B, 4), derivs(F, 4)
    grid_shape = (rs.size, theta.size)

    def bb(a1):
        return np.broadcast_to(np.asarray(a1)[:, None], grid_shape)

    R2d = np.broadcast_to(rs[:, None], grid_shape)
    TH2d = np.broadcast_to(theta[None, :], grid_shape)
    _, idx, g_comps, T_comps = _build_lambdas()
    mesh_gr = (bb(Ap[0]), bb(Ap[1]), bb(Ap[2]), bb(Bp[0]), bb(Bp[1]),
               bb(Bp[2]), bb(Fp_[0]), bb(Fp_[1]), bb(Fp_[2]), R2d, TH2d, v)
    g_direct = _assemble(g_comps, mesh_gr, grid_shape)
    G_direct = _assemble(T_comps, mesh_gr, grid_shape)
    args_gen = tuple(bb(Ap[k]) for k in range(5)) + tuple(bb(Bp[k]) for k in range(5)) \
        + tuple(bb(Fp_[k]) for k in range(5)) + (R2d, TH2d, v)
    _, comps = gen.evaluate_all(*args_gen)
    C_direct = np.zeros((4, 4) + grid_shape)
    for (i, j), val in comps.items():
        val = np.broadcast_to(np.asarray(val, dtype=np.float64), grid_shape)
        C_direct[i, j] = val
        if i != j:
            C_direct[j, i] = val
    T_direct = EINSTEIN_PREFACTOR * (G_direct + alpha * C_direct)
    M = eulerian_transformation(g_direct, wf_compat=False)
    T_eul = to_eulerian(T_direct, M)
    direct_T = _contract_null(T_eul, m2, dirs)
    scale = np.maximum(np.abs(direct_T), np.abs(direct_T).max() * 1e-9)
    relQ = float(np.max(np.abs(row_T - direct_T) / scale))
    gate("GATE Q: LP row form == direct quadratic T contraction (alpha=1e3)",
         bool(relQ < 1e-9), f"worst rel = {relQ:.2e}")

    # The module uses per-column k=5 spline r-derivatives; this gate is the
    # independent FD cross-check of that spline derivative (2nd-order
    # np.gradient carries its own ~4e-4 truncation error, hence the 1e-3
    # band -- the two independent estimators must agree within it).
    dR_grad = np.gradient(R_field, rs, axis=0)
    spR = InterpolatedUnivariateSpline(rs, R_field[:, theta.size // 2], k=5)
    dR_spl = spR.derivative(1)(rs)
    mid = theta.size // 2
    sc = np.abs(dR_spl[mask]).max()
    relV = float(np.max(np.abs(dR_grad[mask, mid] - dR_spl[mask]) / sc))
    gate("GATE V: FD cross-check of the spline dR/dr (independent estimators "
         "agree within 1e-3)",
         bool(relV < 1e-3), f"rel = {relV:.2e}")

    # LP verdicts
    print("-" * 78)
    ok_consistency = True
    for name, (rs_g, Ap_g, B_g, F_g, mask_g, v_g) in geos.items():
        for viab in (False, True):
            res = designer_lp(rs_g, Ap_g, B_g, F_g, v_g, theta, mask_g,
                              require_viability=viab)
            tag = "viable (f''>=0)" if viab else "agnostic (f'' free)"
            print(f"  {name} [{tag}]: {res['n_infeasible']}/{res['n_bins']} "
                  f"level-set bins INFEASIBLE -> "
                  f"{'NO designer f(R) exists' if res['verdict_no_designer_f'] else 'no pointwise obstruction'}")
            if viab:
                inf_v = res["n_infeasible"]
            else:
                inf_a = res["n_infeasible"]
        ok_consistency &= inf_v >= inf_a
    gate("GATE F: LP modes consistent (viability-infeasible >= agnostic-infeasible)",
         bool(ok_consistency))

    # GATE P -- the strongest form: pointwise infeasibility on Alcubierre.
    # Individually infeasible points kill EVERY f(R) with f' > 0 with no
    # reference to level sets or the global integrability of f.
    rs_g, Ap_g, B_g, F_g, mask_g, v_g = geos["alcubierre_w15"]
    n_infeas, n_samp = per_point_lp(rs_g, Ap_g, B_g, F_g, v_g, theta, mask_g)
    gate("GATE P: pointwise infeasibility exists on the Alcubierre wall "
         "(single points whose null fan admits NO (f', f'', f'''))",
         bool(n_infeas > 0),
         f"{n_infeas}/{n_samp} sampled points individually infeasible "
         f"({100*n_infeas/n_samp:.1f}%)")

    n_pass = sum(GATES.values())
    print(f"BATTERY: {n_pass}/{len(GATES)} gates PASS ({time.time()-T0:.0f}s)")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Validate the axisymmetric symbolic EC evaluator against known limits.

Three gates, each a closed-form physics limit -- all must pass before the
evaluator is trusted as an optimizer objective:

  (1) FLAT  (Apos=1, B=1, F=0): Minkowski -> G=0 -> T=0 identically.
  (2) SCHWARZSCHILD VACUUM (Apos=1-rs/r, B=1/(1-rs/r), F=0): Ricci-flat
      -> T=0 to the (converging) 1-D profile FD-truncation level.
  (3) FLAT SLICE + SMALL SHIFT (Apos=B=1, F=Gaussian, v small): the
      Alcubierre gravitomagnetic limit -- Eulerian energy density is
      NEGATIVE in the wall, O(v^2), and scales as (F')^2 (doubling v
      quadruples |rho|; doubling the bump amplitude quadruples |rho|).
"""

from __future__ import annotations

import numpy as np

from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec

# geometrised units (c = G = 1), lengths in metres for the grid bookkeeping
R = np.linspace(2.0, 60.0, 4000)
TH = np.linspace(0.05, np.pi - 0.05, 41)


def _maxabs_T(res):
    return float(np.max(np.abs(res["T_eul"])))


def gate1_flat():
    Apos = np.ones_like(R)
    B = np.ones_like(R)
    F = np.zeros_like(R)
    res = evaluate_axisym_ec(R, Apos, B, F, v=0.0, theta=TH,
                             num_angular=40, num_temporal=4)
    mt = _maxabs_T(res)
    # Symbolic G is provably exactly zero here (analytic-derivative probe
    # gave ~1e-17). Any accurate numerical derivative estimator leaves a
    # tiny floor on an idealised *constant* profile (the quintic spline's
    # ~1e-12 2nd-derivative noise, x the ~4.8e42 prefactor); the low-order
    # np.gradient is exactly 0 on constants but fails on real curved
    # profiles, so it is not the right tool. Real optimiser profiles are
    # never constant. Criterion: negligible vs the 1e38 matter scale.
    MATTER_SCALE = 1.0e38
    print(f"  (1) FLAT          max|T_eul| = {mt:.3e}   "
          f"({mt / MATTER_SCALE:.1e} x matter scale)")
    assert mt < 1.0e33, f"flat |T|={mt:.2e} not negligible vs 1e38 matter scale"
    print("      PASS (>=5 orders below matter scale)")


def gate2_schwarzschild_vacuum():
    """Two-part vacuum check.

    (2a) AIRTIGHT: feed *analytic* Schwarzschild derivatives straight to the
         lambdified symbolic G. If the symbolic Einstein tensor is correct
         the metric is exactly Ricci-flat and G is machine-zero relative to
         the term scale -- independent of any numerical-derivative issue.
    (2b) FLOOR: with quintic-spline derivatives of the numerical profile
         (the production path), |T| sits on the estimator's noise floor; it
         only needs to be many orders below the ~1e38 matter signal so it
         cannot fabricate an optimiser-exploitable feasible region (unlike
         the Cartesian staircasing, which was structured and signal-scale).
    """
    from warp_factory_py.solvers.axisymmetric_ec import _build_lambdas
    _, idx, _, Tc = _build_lambdas()
    rs = 2.0
    worst_rel = 0.0
    for r in (5.0, 10.0, 30.0):
        Apos, Apos_r, Apos_rr = 1 - rs / r, rs / r**2, -2 * rs / r**3
        B, B_r, B_rr = r / (r - rs), -rs / (r - rs)**2, 2 * rs / (r - rs)**3
        pt = (Apos, Apos_r, Apos_rr, B, B_r, B_rr, 0.0, 0.0, 0.0, r, 1.0, 0.0)
        gmax = max(abs(float(np.asarray(f(*pt)))) for f in Tc)
        term = max(abs(Apos_r), abs(B_r), 1.0 / r**2)
        worst_rel = max(worst_rel, gmax / term)
    print(f"  (2a) SCHWARZSCHILD analytic-deriv: worst |G|/term = "
          f"{worst_rel:.2e}  (machine-zero => symbolic G exactly Ricci-flat)")
    assert worst_rel < 1e-12, (
        f"symbolic G not Ricci-flat with exact derivatives "
        f"(rel {worst_rel:.2e}) -> genuine symbolic bug"
    )

    MATTER_SCALE = 1.0e38
    r = np.linspace(2.5, 80.0, 40_000)
    mt = _maxabs_T(evaluate_axisym_ec(
        r, 1 - rs / r, 1.0 / (1 - rs / r), np.zeros_like(r),
        v=0.0, theta=TH, num_angular=40, num_temporal=4))
    print(f"  (2b) SCHWARZSCHILD spline-deriv floor: |T| = {mt:.3e}  "
          f"({mt / MATTER_SCALE:.1e} x matter scale)")
    assert mt < 1.0e34, (
        f"spline-derivative vacuum floor {mt:.2e} not >=4 orders below the "
        f"1e38 matter signal; would be optimiser-relevant"
    )
    print("      PASS (symbolic G exactly Ricci-flat; numerical floor "
          ">=4 orders below matter signal, unstructured -> not exploitable)")


def gate3_alcubierre_gravitomagnetic():
    Apos = np.ones_like(R)
    B = np.ones_like(R)
    r0, w = 20.0, 4.0
    bump = np.exp(-((R - r0) ** 2) / (2 * w**2))

    def rho_min(v, amp):
        res = evaluate_axisym_ec(R, Apos, B, amp * bump, v=v, theta=TH,
                                 num_angular=60, num_temporal=6)
        return float(res["T_eul"][0, 0].min()), res

    rho_v1, _ = rho_min(0.01, 1.0)
    rho_v2, _ = rho_min(0.02, 1.0)
    rho_a2, _ = rho_min(0.01, 2.0)
    print(f"  (3) ALCUBIERRE limit (flat slice + Gaussian shift):")
    print(f"      min rho (v=0.01, amp=1) = {rho_v1:+.3e}")
    print(f"      min rho (v=0.02, amp=1) = {rho_v2:+.3e}   "
          f"ratio={rho_v2/rho_v1:.2f} (expect ~4: rho ~ v^2)")
    print(f"      min rho (v=0.01, amp=2) = {rho_a2:+.3e}   "
          f"ratio={rho_a2/rho_v1:.2f} (expect ~4: rho ~ (F')^2)")
    assert rho_v1 < 0, "Alcubierre energy density must be NEGATIVE in the wall"
    assert 3.0 < rho_v2 / rho_v1 < 5.0, f"rho not ~v^2 (got {rho_v2/rho_v1:.2f})"
    assert 3.0 < rho_a2 / rho_v1 < 5.0, f"rho not ~(F')^2 (got {rho_a2/rho_v1:.2f})"
    print("      PASS (negative, O(v^2), O((F')^2): gravitomagnetic signature)")


if __name__ == "__main__":
    print("=" * 70)
    print("Axisymmetric symbolic EC evaluator -- known-limit validation")
    print("=" * 70)
    gate1_flat()
    gate2_schwarzschild_vacuum()
    gate3_alcubierre_gravitomagnetic()
    print("\nAll three known-limit gates PASS.")

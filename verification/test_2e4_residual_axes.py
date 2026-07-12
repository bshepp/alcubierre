"""Session-50 verification: 2E.4 residual axes — topology (symbolic) + joint vortical+Pi (sweep).

Two legs close the remaining 2E.4 sub-axes:

TOPOLOGY LEG (symbolic, exact; gates T1-T4)
-------------------------------------------
The S42/S44 far-field mechanism is made exact with Pi SYMBOLIC. At
R -> infinity (Gaussians -> 0, erfs saturated) the adopted FH potential is
exactly

    phi_sat = -V sqrt(sigma pi) R  -  V sqrt(sigma pi) (a/m0) tanh(Z/ell) R^{2 Pi}

  * The R-linear coefficient is -V sqrt(sigma pi): independent of Pi, a,
    m0, ell, r, and Z. It is the term that makes |grad phi| non-decaying
    (S17's flat decay-slope finding) and it cannot be removed by ANY
    exponent choice (S44) or vortical addition (this session's sweep leg).
  * The growing anisotropic term has coefficient proportional to
    a * tanh(Z/ell): it vanishes iff a = 0 (the fore-aft-symmetric case,
    already marginal-inconclusive at 1e-5 -- S42) or V = 0 (trivial).

Topology corollaries recorded on these two facts (FELL_HEISENBERG_SWEEP_
NOTES Sec. 20): (i) compact quotients (T^3, lens spaces) admit NO member
of the adopted family -- the R-linear term is incompatible with any closed
3-manifold (no global potential; for V != 0 the formula has no periodic or
closed-manifold realization; the only H^1 freedom on T^3 is a constant
shift = a global boost, and lens spaces have no harmonic 1-forms at all);
(ii) interior-only topological surgeries (handlebody / lens-space interior
glued inside the bubble) leave the exterior untouched, so the S42
finite-R* global-EC violation stands for every such variant.

JOINT VORTICAL+PI LEG (sweep parquet; gates J1-J4)
--------------------------------------------------
Adjudicates the Session-50 dual-box sweep
(hf_jobs/sweeps/fell_heisenberg_joint_2e4.py): baselines must regress
against the certified S44 rows; the far-field gate must be checked at
EVERY joint cell; passenger zone and box-slack improvement counted per
cell against the cell's own (anchor, Pi) baseline.

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_2e4_residual_axes.py topology
      ... joint <parquet>
"""
from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, '.')

GATES = {}


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def mode_topology():
    import sympy as sp
    print("=" * 78)
    print("TOPOLOGY LEG -- exact far-field coefficients, Pi symbolic")
    print("=" * 78)
    X, Y, Z = sp.symbols("X Y Z", real=True)
    V, sigma, m0, a, ell, r = sp.symbols("V sigma m0 a ell r", positive=True)
    Pi = sp.Symbol("Pi", positive=True)
    R = sp.Symbol("R", positive=True)  # radius along a fixed-Z ray

    m = m0 + a * sp.tanh(Z / ell)
    n = m0 - a * sp.tanh(Z / ell)
    R2Pi = R ** (2 * Pi)

    # phi with Gaussians -> 0 and erf0 -> 1, erf1 -> -1, erf2 -> +1
    # (arg1 = r - R^{2Pi}/m -> -inf, arg2 = r + R^{2Pi}/n -> +inf for
    # Pi > 0, m, n > 0 -- the saturation certified numerically in GATE T4)
    inner_erf_sat = sp.sqrt(sigma * sp.pi) * (
        -((m + n) * R * 1)
        + n * (m * R - R2Pi) * (-1)
        + m * (n * R - R2Pi) * (+1)
    )
    phi_sat = V / (m + n) * inner_erf_sat

    target = (-V * sp.sqrt(sigma * sp.pi) * R
              - V * sp.sqrt(sigma * sp.pi) * (a / m0) * sp.tanh(Z / ell) * R2Pi)
    diff = sp.simplify(phi_sat - target)
    gate("GATE T1: saturated far field == -Vsqrt(sigma pi)[R + (a/m0)tanh(Z/ell)R^{2Pi}] (exact)",
         diff == 0, f"residual = {diff}")

    lin_coeff = sp.simplify(phi_sat.coeff(R, 1)) if Pi != sp.Rational(1, 2) else None
    # coefficient of the linear term extracted via limit (works for all Pi < 1/2
    # and by construction for Pi >= 1/2 the R^{2Pi} term is separate in target):
    lin = sp.simplify(target.coeff(R, 1))
    checks = [sp.simplify(sp.diff(lin, s)) == 0 for s in (Pi, a, m0, ell, r, Z)]
    gate("GATE T2: R-linear coefficient = -Vsqrt(sigma pi), independent of "
         "(Pi, a, m0, ell, r, Z)",
         bool(sp.simplify(lin + V * sp.sqrt(sigma * sp.pi)) == 0 and all(checks)),
         f"coefficient = {lin}")

    grow = sp.simplify(target.coeff(R2Pi))
    vanish_at_a0 = sp.simplify(grow.subs(a, 0)) == 0
    nonzero_generic = sp.simplify(grow / (a * sp.tanh(Z / ell))) != 0
    gate("GATE T3: growing-term coefficient proportional to a*tanh(Z/ell); "
         "vanishes iff a = 0 (or V = 0)",
         bool(vanish_at_a0 and nonzero_generic),
         f"coefficient = {grow}")

    # GATE T4 -- numeric saturation certification against the EXACT phi.
    # The erf arguments saturate only once R^{2 Pi} / m >> r + few*sqrt(sigma),
    # i.e. R >> ((m0 + a)(r + 8 sqrt(sigma)))^{1/(2 Pi)} -- strongly
    # Pi-dependent (at Pi = 0.125 the asymptotic regime starts ~1e8). Test
    # radii are therefore scaled per Pi.
    from hf_jobs.sweeps.fell_heisenberg import phi_FH_smooth
    lamt = sp.lambdify((R, Z, V, sigma, m0, a, ell, Pi), target, "numpy")
    worst = 0.0
    for pars in (dict(V=1.5, sigma=10.0, m0=3.0, a=0.223606797749979, ell=6.0, r=9.0),
                 dict(V=1.5, sigma=6.0, m0=3.0, a=0.05, ell=4.0, r=7.75)):
        for Pi_v in (0.125, 0.25, 0.5, 1.0):
            R_sat = ((pars["m0"] + pars["a"])
                     * (pars["r"] + 8.0 * np.sqrt(pars["sigma"]))) ** (1.0 / (2 * Pi_v))
            for Zv in (0.0, 3.0, -8.0):
                for Rv in (max(10.0 * R_sat, 1e4), max(100.0 * R_sat, 1e5)):
                    Xv = np.sqrt(max(Rv**2 - Zv**2, 0.0))
                    exact = float(phi_FH_smooth(
                        np.array(Xv), np.array(0.0), np.array(Zv),
                        Pi=Pi_v, r=pars["r"], V=pars["V"], sigma=pars["sigma"],
                        m0=pars["m0"], a=pars["a"], ell=pars["ell"]))
                    sat = float(lamt(Rv, Zv, pars["V"], pars["sigma"],
                                     pars["m0"], pars["a"], pars["ell"], Pi_v))
                    rel = abs(exact - sat) / max(abs(exact), 1e-300)
                    worst = max(worst, rel)
    gate("GATE T4: saturation is the true asymptotics (exact phi vs phi_sat, "
         "Pi-scaled radii 10x/100x R_sat, 2 anchors x 4 Pi x 3 Z)",
         bool(worst < 1e-10), f"worst rel = {worst:.2e}")

    n_pass = sum(GATES.values())
    print(f"TOPOLOGY LEG: {n_pass}/{len(GATES)} gates PASS")
    return 0 if n_pass == len(GATES) else 1


# Certified S44 baseline rows (background Pi = 0.25) for the J1 regression.
S44_BASELINES = {
    "A1": dict(wec=+0.037405, dec=+0.018705, far=-0.848),
}


def mode_joint(parquet_path):
    import pandas as pd
    df = pd.read_parquet(parquet_path)
    print("=" * 78)
    print(f"JOINT LEG -- {parquet_path} ({len(df)} cells)")
    print("=" * 78)
    errs = df[(df.ok == False) | (df.error.astype(str) != "")]  # noqa: E712
    gate("no failed cells", len(errs) == 0, f"{len(errs)} failed")

    base = df[(df.V_Ax == 0) & (df.V_Ay == 0) & (df.V_Az == 0)]

    # J1 -- baseline regression vs the certified S44 A1 row
    b = base[(base.anchor == "A1") & (base.Pi == 0.25)]
    ok1 = (len(b) == 1
           and abs(b.iloc[0].wec_slack_min - S44_BASELINES["A1"]["wec"]) < 5e-6
           and abs(b.iloc[0].dec_slack_min - S44_BASELINES["A1"]["dec"]) < 5e-6
           and abs(b.iloc[0].far_wec_slack_min - S44_BASELINES["A1"]["far"]) < 5e-3)
    gate("GATE J1: A1 Pi=0.25 baseline regresses against the certified S44 row",
         bool(ok1),
         (f"wec {b.iloc[0].wec_slack_min:+.6f} dec {b.iloc[0].dec_slack_min:+.6f} "
          f"far {b.iloc[0].far_wec_slack_min:+.3f}") if len(b) == 1 else "row missing")

    # J2 -- the far-field gate at EVERY cell
    worst_far = df[["far_wec_slack_min", "far_dec_slack_min"]].min(axis=1)
    n_neg = int((worst_far < 0).sum())
    gate(f"GATE J2: far-field gate negative at every one of {len(df)} joint cells",
         n_neg == len(df),
         f"{n_neg}/{len(df)} negative; max(far slack) = {worst_far.max():+.3e}")

    # J3 -- passenger zone single-voxel everywhere
    h = 2 * df.L_box.iloc[0] / (df.Npts.iloc[0] - 1)
    pz_ok = bool((df.passenger_zone_radius <= h + 1e-12).all())
    gate("GATE J3: passenger zone remains single-voxel (radius <= h) at every cell",
         pz_ok, f"max radius = {df.passenger_zone_radius.max():.4f} vs h = {h:.4f}")

    # J4 -- no augmented cell improves either box slack over its own baseline
    n_improve = 0
    for (anchor, Pi_v), sub in df.groupby(["anchor", "Pi"]):
        b0 = sub[(sub.V_Ax == 0) & (sub.V_Ay == 0) & (sub.V_Az == 0)]
        if len(b0) != 1:
            continue
        aug = sub.drop(b0.index)
        n_improve += int(((aug.wec_slack_min > b0.iloc[0].wec_slack_min + 1e-12)
                          | (aug.dec_slack_min > b0.iloc[0].dec_slack_min + 1e-12)).sum())
    gate("GATE J4: no augmented cell improves either box slack over its "
         "(anchor, Pi) baseline",
         n_improve == 0, f"{n_improve} improving cells")

    print("-" * 78)
    print("far-field slack extrema by background Pi (informational):")
    for Pi_v, sub in df.groupby("Pi"):
        w = sub[["far_wec_slack_min", "far_dec_slack_min"]].min(axis=1)
        print(f"  Pi = {Pi_v:g}: far slack in [{w.min():+.2f}, {w.max():+.2f}]")
    n_pass = sum(GATES.values())
    print(f"JOINT LEG: {n_pass}/{len(GATES)} gates PASS")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "topology":
        raise SystemExit(mode_topology())
    if len(sys.argv) >= 3 and sys.argv[1] == "joint":
        raise SystemExit(mode_joint(sys.argv[2]))
    print(__doc__)
    raise SystemExit(2)

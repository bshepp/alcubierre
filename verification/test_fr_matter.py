"""Session-51 verification: f(R) = R + alpha R^2 Jordan-frame matter evaluator.

Certifies warp_factory_py/solvers/fr_matter.py + the generated correction
module fr_correction_generated.py (Session-51 one-time exact-cancel build).

Gates
-----
  GATE 0  alpha = 0 reproduces the certified GR evaluator EXACTLY on the
          canonical floor configuration (full pipeline; observed rel 0.0).
  GATE B  Schwarzschild stays vacuum at any alpha: the generated correction
          C vanishes on analytic Schwarzschild profiles (observed 6.8e-16).
  GATE D  static de Sitter (Einstein space): C vanishes identically and the
          computed Ricci scalar equals 12/L^2 (observed 6.0e-15 / exact).
  GATE R  regeneration cross-check: a FRESH symbolic derivation of C
          (uncancelled -- fast) matches the generated module on random
          meshes to 1e-6 relative (the uncancelled build carries ~1e-9
          float-cancellation noise; the generated build is exact-cancelled).
  GATE L  small-alpha linearity: the min-EC response at the floor config is
          linear and antisymmetric for |alpha| <= 0.1 m^2 (slope
          ~ -6.5e37 / m^2 at RES_SCOUT) -- certifies the perturbative regime
          used for EC-window estimates.
  GATE S  resolution robustness: the alpha = 1e3 collapse at the floor
          config agrees between RES_SCOUT and RES_FULL within 15%
          (observed 6% -- the collapse is physical within the convention,
          not spline-derivative noise).

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_fr_matter.py [fast|full]
      fast = gates 0, B, D, L (~30 s); full adds R and S (~46 min -- GATE R
      lambdifies the fresh uncancelled components, which is the slow leg).
"""
from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, '.')

GATES = {}
T0 = time.time()


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}"
          + (f" -- {detail}" if detail else "") + f"  [{time.time()-T0:.0f}s]")


def _floor_profiles():
    from hf_jobs.sweeps.mmin_map import shell_profiles
    return shell_profiles(10.0, 20.0, 2.567991e27, 0.02)


def _eval(res, alpha, profs):
    from hf_jobs.sweeps.mmin_map import RES_FULL, RES_SCOUT  # noqa: F401
    from warp_factory_py.solvers.fr_matter import evaluate_axisym_ec_fr
    r, Apos, B, F, M_adm, hmin = profs
    n_r, n_th, na, nt = res
    sub = np.arange(r.size)[:: max(1, r.size // n_r)]
    rs = r[sub]
    mask = (rs >= 10.0) & (rs <= 20.0)
    theta = np.linspace(0.02, np.pi - 0.02, n_th)
    return evaluate_axisym_ec_fr(
        rs, Apos[sub], B[sub], F[sub], v=0.02, alpha=alpha, theta=theta,
        in_shell_mask_1d=mask, num_angular=na, num_temporal=nt)


def _profile_derivs(expr_of_x, xsym, xs):
    import sympy as sp
    fs = [sp.lambdify(xsym, sp.diff(expr_of_x, xsym, k), "numpy") for k in range(5)]
    return [np.asarray(f(xs), dtype=np.float64) * np.ones_like(xs) for f in fs]


def gates_fast():
    import sympy as sp
    from hf_jobs.sweeps.mmin_map import RES_SCOUT
    from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec
    import warp_factory_py.solvers.fr_correction_generated as gen

    profs = _floor_profiles()
    r, Apos, B, F, _, _ = profs
    n_r, n_th, na, nt = RES_SCOUT
    sub = np.arange(r.size)[:: max(1, r.size // n_r)]
    rs = r[sub]
    mask = (rs >= 10.0) & (rs <= 20.0)
    theta = np.linspace(0.02, np.pi - 0.02, n_th)
    gr = evaluate_axisym_ec(rs, Apos[sub], B[sub], F[sub], v=0.02,
                            theta=theta, in_shell_mask_1d=mask,
                            num_angular=na, num_temporal=nt)
    fr0 = _eval(RES_SCOUT, 0.0, profs)
    rel = abs(fr0["min"] - gr["min"]) / abs(gr["min"])
    gate("GATE 0: alpha=0 == certified GR evaluator (full pipeline)",
         bool(rel < 1e-12), f"rel = {rel:.2e}")

    x = sp.Symbol("x", positive=True)
    rr = np.linspace(4.0, 30.0, 400)
    Ap = _profile_derivs(1 - 2 / x, x, rr)
    Bp = _profile_derivs(1 / (1 - 2 / x), x, rr)
    Fp = [np.zeros_like(rr)] * 5
    R_out, comps = gen.evaluate_all(*Ap, *Bp, *Fp, rr, np.full_like(rr, 1.1), 0.02)
    worstB = max(float(np.max(np.abs(np.asarray(c) * np.ones_like(rr))))
                 for c in comps.values())
    gate("GATE B: Schwarzschild correction C == 0 (any alpha)",
         bool(worstB < 1e-10), f"max|C| = {worstB:.2e}")

    L = 100.0
    rr = np.linspace(1.0, 40.0, 400)
    Ap = _profile_derivs(1 - x**2 / L**2, x, rr)
    Bp = _profile_derivs(1 / (1 - x**2 / L**2), x, rr)
    R_out, comps = gen.evaluate_all(*Ap, *Bp, *Fp, rr, np.full_like(rr, 0.7), 0.02)
    worstD = max(float(np.max(np.abs(np.asarray(c) * np.ones_like(rr))))
                 for c in comps.values())
    R_err = abs(float(np.mean(R_out)) - 12 / L**2) / (12 / L**2)
    gate("GATE D: de Sitter C == 0 and R == 12/L^2",
         bool(worstD < 1e-10 and R_err < 1e-10),
         f"max|C| = {worstD:.2e}, R rel err = {R_err:.2e}")

    base = fr0["min"]
    d = {}
    for alpha in (0.01, -0.01, 0.1, -0.1):
        d[alpha] = _eval(RES_SCOUT, alpha, profs)["min"] - base
    lin1 = abs(d[0.01] + d[-0.01]) / abs(d[0.01])
    lin2 = abs(d[0.1] + d[-0.1]) / abs(d[0.1])
    scal = abs(d[0.1] / d[0.01] - 10.0) / 10.0
    gate("GATE L: small-alpha response linear + antisymmetric (|alpha| <= 0.1)",
         bool(lin1 < 0.01 and lin2 < 0.01 and scal < 0.01),
         f"antisym {lin1:.1e}/{lin2:.1e}, scaling dev {scal:.1e}; "
         f"slope = {d[0.01]/0.01:+.3e} per m^2")
    return profs


def gates_full(profs):
    import sympy as sp
    import warp_factory_py.solvers.fr_correction_generated as gen
    from hf_jobs.sweeps.mmin_map import RES_FULL, RES_SCOUT

    # GATE R -- fresh (uncancelled) symbolic derivation vs generated module
    t, r, th, ph = sp.symbols("t r theta phi", real=True)
    v = sp.Symbol("v", real=True)
    Af, Bf, Ff = (sp.Function(n)(r) for n in ("Af", "Bf", "Ff"))
    g = sp.Matrix([
        [-Af, -Ff * v * sp.cos(th), Ff * v * r * sp.sin(th), 0],
        [-Ff * v * sp.cos(th), Bf, 0, 0],
        [Ff * v * r * sp.sin(th), 0, r**2, 0],
        [0, 0, 0, r**2 * sp.sin(th)**2]])
    coords = (t, r, th, ph)
    gi = g.inv()
    N = 4
    Gamma = [[[sp.S.Zero] * N for _ in range(N)] for _ in range(N)]
    for a_ in range(N):
        for b in range(N):
            for cc in range(N):
                s = sp.S.Zero
                for dd in range(N):
                    s += gi[a_, dd] * (sp.diff(g[dd, b], coords[cc])
                                       + sp.diff(g[dd, cc], coords[b])
                                       - sp.diff(g[b, cc], coords[dd]))
                Gamma[a_][b][cc] = s / 2
    Ric = sp.zeros(N, N)
    for a_ in range(N):
        for b in range(N):
            s = sp.S.Zero
            for cc in range(N):
                s += sp.diff(Gamma[cc][a_][b], coords[cc]) \
                    - sp.diff(Gamma[cc][a_][cc], coords[b])
                for dd in range(N):
                    s += Gamma[cc][cc][dd] * Gamma[dd][a_][b] \
                        - Gamma[cc][b][dd] * Gamma[dd][a_][cc]
            Ric[a_, b] = s
    Rs = sum(gi[a_, b] * Ric[a_, b] for a_ in range(N) for b in range(N))
    dR = [sp.diff(Rs, c) for c in coords]
    idxs = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2),
            (1, 3), (2, 2), (2, 3), (3, 3)]
    HessR = {}
    boxR_terms = []
    for a_ in range(N):
        for b in range(N):
            expr = sp.diff(dR[a_], coords[b])
            for cc in range(N):
                expr -= Gamma[cc][a_][b] * dR[cc]
            if (a_, b) in idxs:
                HessR[(a_, b)] = expr
            boxR_terms.append(gi[a_, b] * expr)
    boxR = sum(boxR_terms)
    P = {}
    for base_ in ("Apos", "B", "F"):
        for k in range(5):
            sfx = "" if k == 0 else "_" + "r" * k
            P[base_ + sfx] = sp.Symbol(base_ + sfx, real=True)
    subs = [
        (sp.Derivative(Af, r, 4), P["Apos_rrrr"]), (sp.Derivative(Af, r, 3), P["Apos_rrr"]),
        (sp.Derivative(Af, r, r), P["Apos_rr"]), (sp.Derivative(Af, r), P["Apos_r"]), (Af, P["Apos"]),
        (sp.Derivative(Bf, r, 4), P["B_rrrr"]), (sp.Derivative(Bf, r, 3), P["B_rrr"]),
        (sp.Derivative(Bf, r, r), P["B_rr"]), (sp.Derivative(Bf, r), P["B_r"]), (Bf, P["B"]),
        (sp.Derivative(Ff, r, 4), P["F_rrrr"]), (sp.Derivative(Ff, r, 3), P["F_rrr"]),
        (sp.Derivative(Ff, r, r), P["F_rr"]), (sp.Derivative(Ff, r), P["F_r"]), (Ff, P["F"]),
    ]
    argnames = ("Apos", "Apos_r", "Apos_rr", "Apos_rrr", "Apos_rrrr",
                "B", "B_r", "B_rr", "B_rrr", "B_rrrr",
                "F", "F_r", "F_rr", "F_rrr", "F_rrrr")
    arg_syms = tuple(P[n] for n in argnames) + (r, th, v)
    rng = np.random.default_rng(11)
    n = 400
    mesh = {nm: rng.normal(0, 0.1, n) for nm in argnames}
    mesh["Apos"] = rng.uniform(0.5, 1.5, n)
    mesh["B"] = rng.uniform(0.8, 2.0, n)
    mesh["F"] = rng.uniform(0, 1, n)
    rv = rng.uniform(2, 30, n)
    tv = rng.uniform(0.02, np.pi - 0.02, n)
    margs = tuple(mesh[nm] for nm in argnames) + (rv, tv, 0.02)
    R_gen, C_gen = gen.evaluate_all(*margs)
    worst = 0.0
    for ij in idxs:
        Cf = (2 * Rs * Ric[ij[0], ij[1]] - sp.Rational(1, 2) * Rs**2 * g[ij[0], ij[1]]
              - 2 * HessR[ij] + 2 * g[ij[0], ij[1]] * boxR).subs(subs)
        lam = sp.lambdify(arg_syms, Cf, "numpy", cse=True)
        fresh = np.asarray(lam(*margs), dtype=np.float64)
        genv = np.asarray(C_gen[ij], dtype=np.float64) * np.ones(n)
        scale = np.maximum(np.abs(fresh), 1e-20)
        worst = max(worst, float(np.max(np.abs(fresh - genv) / scale)))
    gate("GATE R: fresh symbolic derivation matches the generated module",
         bool(worst < 1e-6), f"worst rel = {worst:.2e} (uncancelled noise floor ~1e-9)")

    # GATE S -- resolution robustness of the alpha-collapse
    m_scout = _eval(RES_SCOUT, 1e3, profs)["min"]
    m_full = _eval(RES_FULL, 1e3, profs)["min"]
    rel = abs(m_full - m_scout) / abs(m_full)
    gate("GATE S: alpha=1e3 collapse agrees RES_SCOUT vs RES_FULL (<15%)",
         bool(rel < 0.15), f"{m_scout:+.3e} vs {m_full:+.3e} (rel {rel:.2%})")


def gates_map(parquet_path):
    """Audit the Session-52 alpha x geometry map parquet (seconds)."""
    import pandas as pd
    df = pd.read_parquet(parquet_path)
    gate("MAP: no evaluate() errors",
         bool((df.error.astype(str) == "").all()), f"{len(df)} rows")
    fl0 = df[(df.name == "fuchs_floor") & (df.alpha == 0.0)]
    rel = abs(float(fl0.iloc[0].min_ec) - 5.689346e36) / 5.689346e36
    gate("MAP: floor alpha=0 row equals the certified RES_FULL margin",
         bool(rel < 1e-6), f"rel = {rel:.2e}")
    rescued = []
    viable_best_nonzero = []
    for name, sub in df.groupby("name"):
        base = float(sub[sub.alpha == 0].min_ec.iloc[0])
        best = float(sub.min_ec.max())
        if base < 0 and best >= 0:
            rescued.append(name)
        vsub = sub[sub.viable == True]  # noqa: E712
        if base >= 0 and float(vsub.loc[vsub.min_ec.idxmax()].alpha) != 0.0:
            viable_best_nonzero.append(name)
    gate("MAP: no EC-violating configuration is rescued at any alpha",
         len(rescued) == 0, f"rescued: {rescued}")
    gate("MAP: every EC-passing configuration's best VIABLE alpha is 0 "
         "(any alpha > 0 strictly degrades)",
         len(viable_best_nonzero) == 0,
         f"exceptions: {viable_best_nonzero}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    print("=" * 78)
    print(f"f(R) MATTER EVALUATOR BATTERY ({mode})")
    print("=" * 78)
    if mode == "map":
        gates_map(sys.argv[2])
    else:
        profs = gates_fast()
        if mode == "full":
            gates_full(profs)
    n_pass = sum(GATES.values())
    print(f"BATTERY: {n_pass}/{len(GATES)} gates PASS ({time.time()-T0:.0f}s)")
    raise SystemExit(0 if n_pass == len(GATES) else 1)

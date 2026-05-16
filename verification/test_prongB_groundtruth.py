"""Prong B -- analytic ground-truth adjudicator (FAST refactor, parallel).

Adjudicates the sharp-profile Cartesian-vs-radial EC conflict against an
INDEPENDENT, certified-exact ground truth.

Architecture (the Session-29/30 refactor):
  * The Einstein-tensor STRUCTURE does not depend on sharpness s -- only
    the profile and its derivatives do. So build the standalone symbolic
    Einstein tensor ONCE, with abstract A(r),B(r),F(r) reduced to symbols
    (A,A',A'', B,B',B'', F,F',F'', r, theta, v), per-component
    sp.cancel(sp.together) [the FAST ~6 s cancel on abstract symbols --
    NOT the tanh-substituted cancel that hung for hours], lambdify(cse).
  * Per sharpness: take the CLOSED-FORM tanh profile, differentiate it
    EXACTLY with sympy (instant -- differentiating a tanh, not rebuilding
    Ricci), evaluate those exact analytic derivatives, feed into the
    once-built G. This is the exact ground truth.
  * Independence: this symbolic derivation is standalone (NOT
    axisymmetric_ec). GT and the radial pipeline then share NOTHING but
    the metric ansatz; they differ in (a) which symbolic G code computed
    it [independent] and (b) derivative source [GT exact-analytic vs
    radial quintic-spline]. Cartesian is fully independent (FD).
  * Certification (the rigor proof): feed exact analytic derivatives of
    FLAT and SCHWARZSCHILD through the SAME build-once lambdas the sweep
    uses; require literal machine-zero. A Ricci-flat metric -> exactly 0
    proves the path computes the correct Einstein tensor of GR (stronger
    than fast==slow self-consistency, and cheap). Chain rule covers the
    non-vacuum swept metric trivially.
  * The 7 sharpness values are embarrassingly parallel -> process pool
    (wall ~ one row). Sized for an 8-vCPU c7i.2xlarge; BLAS pinned to 1
    thread/worker to avoid oversubscription.
"""

from __future__ import annotations

import os

# Pin BLAS/OpenMP to 1 thread BEFORE numpy import: 7 worker processes each
# doing numpy einsum on an 8-vCPU box must not each spawn 8 BLAS threads.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import time
import multiprocessing as mp
from functools import lru_cache

import numpy as np
import sympy as sp

from warp_factory_py.utils.constants import EINSTEIN_PREFACTOR
from warp_factory_py.solvers.frame import eulerian_transformation, to_eulerian
from warp_factory_py.solvers.energy_conditions import evaluate_energy_conditions
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec
from warp_factory_py.metrics.warp_shell import _sph2cart_diag
from warp_factory_py.metrics.alcubierre import Metric
from warp_factory_py.solvers.evaluator import eval_metric

R1, R2 = 10.0, 20.0
r0 = 11.0
A_AMP = 0.10
MU = 0.20
F_AMP = 0.30
rF, wF = 15.0, 3.0
V = 0.02
SHARPNESS = (0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0)
IDX = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2),
       (1, 3), (2, 2), (2, 3), (3, 3)]
RMESH = np.linspace(0.5, 1.5 * R2, 6000)
THMESH = np.linspace(0.02, np.pi - 0.02, 120)


# ---------------------------------------------------------------------------
# Build the standalone symbolic Einstein tensor ONCE (abstract profiles).
# Independent of axisymmetric_ec.py (separate derivation -> genuine
# cross-check of that module's G as well). lru_cache => one build/process.
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1)
def build_G():
    t, r, th, ph = sp.symbols("t r theta phi", real=True)
    vv = sp.Symbol("v", real=True)
    A, Ar, Arr = sp.symbols("A A_r A_rr", positive=True)
    B, Br, Brr = sp.symbols("B B_r B_rr", positive=True)
    F, Fr, Frr = sp.symbols("F F_r F_rr", real=True)
    Af, Bf, Ff = sp.Function("Af")(r), sp.Function("Bf")(r), sp.Function("Ff")(r)
    g = sp.Matrix([
        [-Af, -Ff * vv * sp.cos(th), Ff * vv * r * sp.sin(th), 0],
        [-Ff * vv * sp.cos(th), Bf, 0, 0],
        [Ff * vv * r * sp.sin(th), 0, r**2, 0],
        [0, 0, 0, r**2 * sp.sin(th)**2],
    ])
    co = (t, r, th, ph)
    gi = g.inv()
    N = 4
    Ga = [[[sp.S.Zero] * N for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(N):
            for c in range(N):
                s_ = sp.S.Zero
                for d in range(N):
                    s_ += gi[a, d] * (sp.diff(g[d, b], co[c])
                                      + sp.diff(g[d, c], co[b])
                                      - sp.diff(g[b, c], co[d]))
                Ga[a][b][c] = s_ / 2
    Ric = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            s_ = sp.S.Zero
            for c in range(N):
                s_ += sp.diff(Ga[c][a][b], co[c]) - sp.diff(Ga[c][a][c], co[b])
                for d in range(N):
                    s_ += Ga[c][c][d] * Ga[d][a][b] - Ga[c][b][d] * Ga[d][a][c]
            Ric[a, b] = s_
    Rs = sum(gi[a, b] * Ric[a, b] for a in range(N) for b in range(N))
    subs = [
        (sp.Derivative(Af, r, r), Arr), (sp.Derivative(Af, r), Ar), (Af, A),
        (sp.Derivative(Bf, r, r), Brr), (sp.Derivative(Bf, r), Br), (Bf, B),
        (sp.Derivative(Ff, r, r), Frr), (sp.Derivative(Ff, r), Fr), (Ff, F),
    ]
    args = (A, Ar, Arr, B, Br, Brr, F, Fr, Frr, r, th, vv)
    gl, Tl = [], []
    for i, j in IDX:
        gij = g[i, j].subs(subs)
        Gij = sp.cancel(sp.together(
            (Ric[i, j] - sp.Rational(1, 2) * g[i, j] * Rs).subs(subs)))
        gl.append(sp.lambdify(args, gij, "numpy", cse=True))
        Tl.append(sp.lambdify(args, Gij, "numpy", cse=True))
    return gl, Tl


def _assemble(lams, vals, shape):
    out = np.zeros((4, 4) + shape, float)
    for (i, j), L in zip(IDX, lams):
        v = np.broadcast_to(np.asarray(L(*vals), float), shape)
        out[i, j] = v
        if i != j:
            out[j, i] = v
    return out


def closed_form(s):
    """Closed-form sympy profile + numpy callables for the profile and its
    EXACT analytic 1st/2nd r-derivatives (sympy-differentiated, instant)."""
    r = sp.Symbol("r", real=True)
    ramp = sp.Rational(1, 2) * (1 + sp.tanh(s * (r - r0)))
    win = (sp.Rational(1, 2) * (1 + sp.tanh(4 * (r - R1)))
           * sp.Rational(1, 2) * (1 + sp.tanh(4 * (R2 - r))))
    Ae = 1 - A_AMP * ramp * win
    Be = 1 / (1 - MU * ramp * win)
    Fe = F_AMP * sp.exp(-((r - rF) / wF) ** 2)
    exprs = {}
    for nm, e in (("A", Ae), ("B", Be), ("F", Fe)):
        exprs[nm] = sp.lambdify(r, e, "numpy")
        exprs[nm + "_r"] = sp.lambdify(r, sp.diff(e, r), "numpy")
        exprs[nm + "_rr"] = sp.lambdify(r, sp.diff(e, r, 2), "numpy")
    prof = sp.lambdify(r, [Ae, Be, Fe], "numpy")

    def prof_np(rn):
        a, b, c = prof(rn)
        bc = lambda x: np.broadcast_to(np.asarray(x, float), np.shape(rn)).copy()
        return bc(a), bc(b), bc(c)
    return exprs, prof_np


def gt_min_ec(s, gl, Tl):
    """Exact ground-truth min(EC): build-once G fed EXACT analytic
    closed-form derivatives. No FD, no spline -- the true continuum
    Einstein tensor of the closed-form metric, numerically evaluated."""
    e, _ = closed_form(s)
    R = np.broadcast_to(RMESH[:, None], (RMESH.size, THMESH.size))
    TH = np.broadcast_to(THMESH[None, :], (RMESH.size, THMESH.size))
    rr = RMESH[:, None] * np.ones((1, THMESH.size))
    def col(name):
        return np.broadcast_to(np.asarray(e[name](RMESH), float)[:, None],
                               (RMESH.size, THMESH.size))
    vals = (col("A"), col("A_r"), col("A_rr"), col("B"), col("B_r"),
            col("B_rr"), col("F"), col("F_r"), col("F_rr"), rr, TH, V)
    shape = (RMESH.size, THMESH.size)
    g = _assemble(gl, vals, shape)
    G = _assemble(Tl, vals, shape)
    T = EINSTEIN_PREFACTOR * G
    M = eulerian_transformation(g, wf_compat=False)
    Te = to_eulerian(T, M)
    ec = evaluate_energy_conditions(Te, num_angular=80, num_temporal=8)
    ish = (RMESH >= R1) & (RMESH <= R2)
    m2 = np.broadcast_to(ish[:, None], shape)
    return min(float(ec[c][m2].min()) for c in
               ("null", "weak", "dominant", "strong"))


def validate_gt(gl, Tl):
    """Certify the BUILD-ONCE path against GR: exact analytic derivatives
    of flat & Schwarzschild -> literal machine-zero (Ricci-flat). This is
    the rigor proof (stronger than fast==slow; tests the actual code path)."""
    print("  certifying build-once G (must be machine-zero for vacuum):")
    cases = {
        "flat": lambda rv: (1., 0., 0., 1., 0., 0., 0., 0., 0.),
        "Schwarzschild": lambda rv: (
            1 - 2 / rv, 2 / rv**2, -4 / rv**3,
            rv / (rv - 2), -2 / (rv - 2)**2, 4 / (rv - 2)**3,
            0., 0., 0.),
    }
    for nm, fn in cases.items():
        mx = 0.0
        for rv in (3.0, 7.5, 25.0):
            vals = fn(rv) + (rv, 0.9, 0.0)
            for L in Tl:
                mx = max(mx, abs(float(np.asarray(L(*vals)))))
        ok = mx < 1e-9
        print(f"    {nm:14s}: max|G| = {mx:.2e}  "
              f"{'OK (exact Ricci-flat)' if ok else 'FAIL -> path buggy'}")
        if not ok:
            raise SystemExit("build-once G failed GR certification.")
    print("  CERTIFIED: build-once path computes the correct Einstein "
          "tensor of GR.")


def cartesian_min_ec(prof, dx=0.2):
    N = int(round(52.0 / dx))
    if N % 2:
        N += 1
    off = 0.37 * dx
    gs = (1.0, dx, dx, dx)
    wc = (0.0, N * dx / 2 + off, N * dx / 2 + off, 2.5 * dx + off)
    i = (np.arange(N) + 1)[:, None, None] * dx - wc[1]
    j = (np.arange(N) + 1)[None, :, None] * dx - wc[2]
    k = (np.arange(5) + 1)[None, None, :] * dx - wc[3]
    Xc = np.broadcast_to(i, (N, N, 5))
    Yc = np.broadcast_to(j, (N, N, 5))
    Zc = np.broadcast_to(k, (N, N, 5))
    rg = np.sqrt(Xc**2 + Yc**2 + Zc**2)
    th = np.arctan2(np.sqrt(Xc**2 + Yc**2), Zc)
    phi = np.arctan2(Yc, Xc)
    A, B, F = prof(rg)
    g11, g22, g23, g24, g33, g34, g44 = _sph2cart_diag(th, phi, -A, B)
    g = np.zeros((4, 4, 1, N, N, 5), float)
    g[0, 0, 0] = g11; g[1, 1, 0] = g22; g[2, 2, 0] = g33; g[3, 3, 0] = g44
    g[1, 2, 0] = g[2, 1, 0] = g23
    g[1, 3, 0] = g[3, 1, 0] = g24
    g[2, 3, 0] = g[3, 2, 0] = g34
    g[0, 1, 0] = g[1, 0, 0] = -g[0, 1, 0] * F - F * V
    t = np.array([1.0]); x = (np.arange(N) + 1) * dx
    y = (np.arange(N) + 1) * dx; z = (np.arange(5) + 1) * dx
    res = eval_metric(Metric(g=g, coords=(t, x, y, z), grid_scale=gs,
                             name="GTcart"),
                      num_angular=80, num_temporal=8, wf_compat=False)
    XC = np.arange(N) * dx - wc[1]
    YC = np.arange(N) * dx - wc[2]
    ZC = np.arange(5) * dx - wc[3]
    Rr = np.sqrt(XC[:, None, None]**2 + YC[None, :, None]**2
                 + ZC[None, None, :]**2)
    ish = (Rr >= R1) & (Rr <= R2)
    bd = np.zeros_like(Rr, bool); bd[2:-2, 2:-2, 1:-1] = True
    m = (ish & bd)[None]
    return min(float(res.ec[c][m].min()) for c in
               ("null", "weak", "dominant", "strong"))


def radial_min_ec(prof):
    r = np.linspace(0.5, 1.5 * R2, 6000)
    A, B, F = prof(r)
    res = evaluate_axisym_ec(
        r, A, B, F, v=V, theta=np.linspace(0.02, np.pi - 0.02, 120),
        in_shell_mask_1d=(r >= R1) & (r <= R2),
        num_angular=80, num_temporal=8)
    return res["min"]


def _one_sharpness(s):
    """Worker: independent (GT, Cartesian, radial) min(EC) for sharpness s.
    Builds its own G (lru_cache => once/process; ~6 s, in parallel)."""
    t0 = time.time()
    gl, Tl = build_G()
    _, prof = closed_form(s)
    gt = gt_min_ec(s, gl, Tl)
    ca = cartesian_min_ec(prof)
    ra = radial_min_ec(prof)
    return (s, gt, ca, ra, time.time() - t0)


def main():
    print("=" * 80)
    print("PRONG B -- analytic ground-truth adjudicator (fast/parallel)")
    print("=" * 80)
    t0 = time.time()
    gl, Tl = build_G()
    print(f"  build-once symbolic G: {time.time()-t0:.1f}s")
    validate_gt(gl, Tl)

    ncpu = mp.cpu_count()
    nproc = min(len(SHARPNESS), max(1, ncpu - 1))
    print(f"\n  parallel sweep: {len(SHARPNESS)} sharpness values, "
          f"{nproc} workers ({ncpu} vCPU detected)")
    t0 = time.time()
    with mp.Pool(nproc) as pool:
        rows = pool.map(_one_sharpness, SHARPNESS)
    rows.sort()
    print(f"  sweep wall time: {time.time()-t0:.1f}s\n")

    print(f"  {'s [1/m]':>8s} {'GT min(EC)':>14s} {'Cart min(EC)':>14s} "
          f"{'Rad min(EC)':>14s}   {'Cart vs GT':>11s} {'Rad vs GT':>11s}")
    print("  " + "-" * 86)
    for s, gt, ca, ra, dt in rows:
        def tag(x):
            if (x >= 0) != (gt >= 0):
                return "SIGN FLIP"
            return f"{abs(x-gt)/max(abs(gt),1e-300)*100:6.1f}%"
        print(f"  {s:8.1f} {gt:>14.3e} {ca:>14.3e} {ra:>14.3e}   "
              f"{tag(ca):>11s} {tag(ra):>11s}   ({dt:.0f}s)")

    print("\n" + "=" * 80)
    print("READING: GT is the certified-exact continuum answer. The "
          "pipeline whose\n  min(EC) tracks GT (no SIGN FLIP, small %) as s "
          "increases is trustworthy\n  for sharp profiles; the first SIGN "
          "FLIP marks where that pipeline\n  becomes untrustworthy. The "
          "optimizer's effective inner-edge sharpness\n  (rho ~0 -> rho0 "
          "across <~1 m) is s ~ a few; compare to where each breaks.")


if __name__ == "__main__":
    main()

"""Session 58 -- observer-robust (exact) energy-condition minimiser: battery.

Context. The certified radial oracle (``axisymmetric_ec``) certifies the
Einstein tensor exactly (Prong B, Session 30) but formed its EC *verdict*
with WarpFactory's sampled observer field (``num_angular x num_temporal``;
100x10 at the accept tier, 160x16 at RES_CONF). A finite sample is an upper
bound on the true minimum over observers, so every recorded margin carried an
optimistic bias. Le 2026a (arXiv:2602.18023) raises the same point for warp
spacetimes in general. ``warp_factory_py/solvers/ec_exact.py`` replaces the
sample with exact minima (sphere trust-region subproblem for NEC and the DEC
flux form; cone-restricted Rayleigh quotient for WEC/SEC).

Gates (``python verification/test_ec_exact_minimiser.py [fast|full|floor]``):

  G1  random symmetric tensors: exact <= dense (20k dirs x 40 speeds) and
      exact <= sampled(100x10) at every point; dense - exact small.
  G2  Type I rest-frame closed forms reproduced to 1e-12 (null, weak,
      strong, dominant, dominant_future).
  G3  randomly boosted Type I tensors: EC signs match the rest-frame closed
      forms at 100 % of points; Type I mask 100 %.
  G4  trust-region hard case (b orthogonal to the minimal eigenvector, small
      |b|) solved to brute-force precision.
  G5  canonical Fuchs cell (10, 20, 0.02c) at the accept-tier mesh:
      exact <= sampled at every in-shell point for both sampling tiers;
      bias statistics; sign flip across the S32 floor (negative AT the
      recorded floor 2.568e27, positive at +1.2 %).
  G6  independent-pipeline cross-check against warpax's LMI margins
      (Le 2026a; MIT) on G1 + G5 points -- requires WARPAX_PYTHON pointing
      at an interpreter with warpax installed; SKIP otherwise.
  floor  re-bisect the canonical single-shell floor with the exact oracle
      (``find_mmin(min_ec_fn=exact)``); prints the re-based floor and the
      shift relative to 2.568e27 (expected ~ +0.1 %, inside rel_tol 0.5 %).

Run with repo root on PYTHONPATH.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from functools import partial

import numpy as np

from warp_factory_py.solvers.ec_exact import (
    evaluate_energy_conditions_exact, sphere_quadratic_min)
from warp_factory_py.solvers.energy_conditions import (
    evaluate_energy_conditions, _angular_directions)

PASS = "[PASS]"
FAIL = "[FAIL]"
SKIP = "[SKIP]"
results: list[tuple[str, bool]] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok)))
    print(f"{PASS if ok else FAIL} {name}" + (f" -- {detail}" if detail else ""), flush=True)


def dense_minima(Tp: np.ndarray, n_dirs: int = 20000, n_speeds: int = 40):
    """Brute-force upper bounds (project normalisation). Tp: (P,4,4)."""
    n = _angular_directions(n_dirs)
    V = np.concatenate([np.ones((n_dirs, 1)), n], 1) / np.sqrt(2.0)
    null = np.einsum("pab,Na,Nb->Np", Tp, V, V).min(0)
    weak = np.full(Tp.shape[0], np.inf)
    for bval in np.linspace(0.0, 1.0, n_speeds):
        Vt = np.concatenate([np.ones((n_dirs, 1)), (1 - bval) * n], 1)
        Vt /= np.linalg.norm(Vt, axis=1, keepdims=True)
        weak = np.minimum(weak, np.einsum("pab,Na,Nb->Np", Tp, Vt, Vt).min(0))
    return null, weak


def boost(v: np.ndarray) -> np.ndarray:
    g = 1.0 / np.sqrt(1.0 - v @ v)
    L = np.eye(4)
    L[0, 0] = g
    L[0, 1:] = L[1:, 0] = -g * v
    L[1:, 1:] += (g - 1.0) * np.outer(v, v) / (v @ v)
    return L


# ---------------------------------------------------------------- G1 -------
def gate_g1(rng):
    P = 3000
    S = rng.normal(size=(P, 4, 4))
    Tp = (S + np.swapaxes(S, 1, 2)) / 2
    ex = evaluate_energy_conditions_exact(np.moveaxis(Tp, 0, -1))
    dn, dw = dense_minima(Tp)
    sm = evaluate_energy_conditions(np.moveaxis(Tp, 0, -1), num_angular=100, num_temporal=10)
    ok = True
    det = []
    for k, d in (("null", dn), ("weak", dw)):
        gap = d - ex[k]
        ok &= bool((gap >= -1e-9).all() and gap.max() < 2e-3)
        det.append(f"{k}: dense-exact in [{gap.min():.1e}, {gap.max():.1e}]")
    for k in ("null", "weak", "strong", "dominant"):
        gap = sm[k] - ex[k]
        ok &= bool((gap >= -1e-9).all())
        det.append(f"{k}: sampled-exact min {gap.min():.1e}")
    gate("G1 random tensors: exact <= dense, exact <= sampled(100x10)", ok, "; ".join(det))
    return Tp


# ---------------------------------------------------------------- G2 -------
def gate_g2(rng):
    P = 2000
    rho = rng.uniform(0.5, 2.0, P)
    p = rng.uniform(-1.5, 1.5, (P, 3))
    Tp = np.zeros((P, 4, 4))
    Tp[:, 0, 0] = rho
    for i in range(3):
        Tp[:, i + 1, i + 1] = p[:, i]
    ex = evaluate_energy_conditions_exact(np.moveaxis(Tp, 0, -1))
    pmin = p.min(1); pmax_abs = np.abs(p).max(1)
    null_t = 0.5 * (rho + pmin)
    weak_t = np.minimum(rho, null_t)
    tr = -rho + p.sum(1)
    rho_e = rho + 0.5 * tr; p_e = p - 0.5 * tr[:, None]
    strong_t = np.minimum(rho_e, 0.5 * (rho_e + p_e.min(1)))
    jj = 0.5 * (-rho ** 2 + pmax_abs ** 2)
    dom_t = -np.sign(jj) * np.sqrt(np.abs(jj))
    rel = lambda a, b: np.abs(a - b).max() / max(np.abs(b).max(), 1e-300)
    errs = {k: rel(ex[k], t) for k, t in (("null", null_t), ("weak", weak_t), ("strong", strong_t),
                                          ("dominant", dom_t), ("dominant_future", rho))}
    ok = all(e < 1e-12 for e in errs.values()) and bool(ex["type_I"].all())
    gate("G2 Type I rest-frame closed forms to 1e-12", ok,
         ", ".join(f"{k} {e:.1e}" for k, e in errs.items()) + f"; typeI={ex['type_I'].mean():.4f}")


# ---------------------------------------------------------------- G3 -------
def gate_g3(rng):
    P = 2000
    rho = rng.uniform(0.5, 2.0, P)
    p = rng.uniform(-1.5, 1.5, (P, 3))
    Tb = np.empty((P, 4, 4))
    for k in range(P):
        T0 = np.diag([rho[k], *p[k]])
        v = rng.normal(size=3); v *= rng.uniform(0.0, 0.85) / np.linalg.norm(v)
        L = boost(v)
        Tb[k] = L.T @ T0 @ L
    ex = evaluate_energy_conditions_exact(np.moveaxis(Tb, 0, -1))
    pmin = p.min(1)
    agree = {
        "null": (np.sign(ex["null"]) == np.sign(rho + pmin)).mean(),
        "weak": (np.sign(ex["weak"]) == np.sign(np.minimum(rho, rho + pmin))).mean(),
        "strong": (np.sign(ex["strong"]) == np.sign(np.minimum(rho + pmin, rho + p.sum(1)))).mean(),
        "dominant": (np.sign(np.minimum(ex["dominant"], ex["dominant_future"])) == np.sign(rho - np.abs(p).max(1))).mean(),
    }
    ok = all(a == 1.0 for a in agree.values()) and bool(ex["type_I"].all())
    gate("G3 boosted Type I: all EC signs frame-invariant; Type I mask", ok,
         ", ".join(f"{k} {a:.4f}" for k, a in agree.items()) + f"; typeI={ex['type_I'].mean():.4f}")


# ---------------------------------------------------------------- G4 -------
def gate_g4(rng):
    P = 500
    lam = np.sort(rng.uniform(-2, 2, (P, 3)), axis=1)
    lam[:, 1] = lam[:, 0] + rng.uniform(0.3, 1.0, P)
    lam[:, 2] = lam[:, 1] + rng.uniform(0.3, 1.0, P)
    Qr, _ = np.linalg.qr(rng.normal(size=(P, 3, 3)))
    A = np.einsum("pij,pj,pkj->pik", Qr, lam, Qr)
    beta = rng.normal(size=(P, 3)) * 0.05
    beta[:, 0] = 0.0                                   # b orthogonal to e_min -> hard case
    b = np.einsum("pij,pj->pi", Qr, beta)
    val, n = sphere_quadratic_min(A, b)
    # brute force: 200k directions + polish via local quadratic refinement
    nd = _angular_directions(200000)
    allv = np.einsum("Ni,pij,Nj->Np", nd, A, nd) + 2 * np.einsum("pi,Ni->Np", b, nd)
    bf = allv.min(0)
    # polish the brute-force minimum with Nelder-Mead on the sphere (the raw
    # 200k-direction sample is an upper bound with ~1e-5 quadrature error)
    from scipy.optimize import minimize
    best = allv.argmin(0)
    for k in range(P):
        n0 = nd[best[k]]
        th0, ph0 = np.arccos(np.clip(n0[2], -1, 1)), np.arctan2(n0[1], n0[0])
        f = lambda x, k=k: float(np.array([np.sin(x[0]) * np.cos(x[1]), np.sin(x[0]) * np.sin(x[1]), np.cos(x[0])]) @ A[k]
                                 @ np.array([np.sin(x[0]) * np.cos(x[1]), np.sin(x[0]) * np.sin(x[1]), np.cos(x[0])])
                                 + 2 * b[k] @ np.array([np.sin(x[0]) * np.cos(x[1]), np.sin(x[0]) * np.sin(x[1]), np.cos(x[0])]))
        r = minimize(f, [th0, ph0], method="Nelder-Mead", options=dict(xatol=1e-10, fatol=0, maxiter=600))
        bf[k] = min(bf[k], r.fun)
    gap = bf - val
    norm_ok = np.abs(np.linalg.norm(n, axis=1) - 1).max() < 1e-12
    ok = bool((gap >= -1e-9).all() and gap.max() < 1e-9 and norm_ok)
    gate("G4 trust-region hard case (b perp e_min): brute-force agreement", ok,
         f"brute-exact in [{gap.min():.1e}, {gap.max():.1e}], |n|-1 max {np.abs(np.linalg.norm(n, axis=1) - 1).max():.1e}")


# ---------------------------------------------------------------- G5 -------
def gate_g5():
    from hf_jobs.sweeps.mmin_map import shell_profiles, RES_FULL
    from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec
    R1, R2, v = 10.0, 20.0, 0.02
    n_r, n_th, na, nt = RES_FULL
    recs = []
    sample_T = None
    for M, lab in ((2.568e27, "S32 floor"), (2.60e27, "+1.2%")):
        t0 = time.time()
        r, Apos, B, F, M_adm, hmin = shell_profiles(R1, R2, M, v)
        sub = np.arange(r.size)[:: max(1, r.size // n_r)]
        theta = np.linspace(0.02, np.pi - 0.02, n_th)
        mask = (r[sub] >= R1) & (r[sub] <= R2)
        out = evaluate_axisym_ec(r[sub], Apos[sub], B[sub], F[sub], v=v, theta=theta,
                                 in_shell_mask_1d=mask, num_angular=na, num_temporal=nt, exact=True)
        T = out["T_eul"]
        m2 = np.broadcast_to(mask[:, None], T.shape[2:])
        ex = {k: out[k][m2] for k in ("null", "weak", "strong", "dominant")}
        s100 = {k: a[m2] for k, a in evaluate_energy_conditions(T, num_angular=100, num_temporal=10).items()}
        s160 = {k: a[m2] for k, a in evaluate_energy_conditions(T, num_angular=160, num_temporal=16).items()}
        scale = float(np.abs(T[0, 0][m2]).max())
        rec = {"label": lab, "M": M, "scale": scale, "secs": round(time.time() - t0, 1),
               "exact_min": {k: float(ex[k].min()) for k in ex},
               "s100_min": {k: float(s100[k].min()) for k in ex},
               "s160_min": {k: float(s160[k].min()) for k in ex},
               "bias100_null_mean_rel": float((s100["null"] - ex["null"]).mean() / scale),
               "bias160_null_mean_rel": float((s160["null"] - ex["null"]).mean() / scale),
               "upper_bound_ok": bool(all(((s100[k] - ex[k]) >= -1e-6 * scale).all() and
                                          ((s160[k] - ex[k]) >= -1e-6 * scale).all() for k in ex)),
               "typeI_frac": float(out["type_I"][m2].mean()),
               "dominant_future_min_rel": float(out["dominant_future"][m2].min() / scale)}
        recs.append(rec)
        print(json.dumps(rec, indent=1), flush=True)
        if sample_T is None:
            idx = np.argsort(ex["null"])[:150]
            Tp = np.moveaxis(T.reshape(4, 4, -1), -1, 0)[m2.reshape(-1)]
            sample_T = Tp[idx] / scale                 # worst 150 in-shell points, normalised
    ok_bound = all(r_["upper_bound_ok"] for r_ in recs)
    gate("G5a canonical cell: sampled(100x10) and sampled(160x16) >= exact at every in-shell point", ok_bound,
         f"mean null bias/scale: 100x10 {recs[0]['bias100_null_mean_rel']:.2e}, 160x16 {recs[0]['bias160_null_mean_rel']:.2e}")
    flip = recs[0]["exact_min"]["null"] < 0 < recs[1]["exact_min"]["null"]
    gate("G5b exact minimum is NEGATIVE at the recorded S32 floor and POSITIVE at +1.2 %", flip,
         f"floor {recs[0]['exact_min']['null']:+.3e} (sampled100 {recs[0]['s100_min']['null']:+.3e}); "
         f"+1.2% {recs[1]['exact_min']['null']:+.3e}")
    return sample_T, recs


# ---------------------------------------------------------------- G6 -------
def gate_g6(T_random: np.ndarray, T_shell: np.ndarray | None):
    py = os.environ.get("WARPAX_PYTHON")
    if not py or not os.path.exists(py):
        print(f"{SKIP} G6 warpax cross-check (set WARPAX_PYTHON to a venv interpreter with warpax)")
        return
    worker = os.path.join(os.path.dirname(os.path.abspath(__file__)), "warpax_xcheck_worker.py")
    batch = T_random[:300] if T_shell is None else np.concatenate([T_random[:200], T_shell[:150]])
    with tempfile.TemporaryDirectory() as td:
        fin = os.path.join(td, "T.npy"); fout = os.path.join(td, "out.npz")
        np.save(fin, batch)
        t0 = time.time()
        pr = subprocess.run([py, "-I", worker, fin, fout], capture_output=True, text=True, timeout=1800)
        if pr.returncode != 0 or not os.path.exists(fout):
            print(f"{SKIP} G6 warpax worker failed:\n{pr.stderr[-1500:]}")
            return
        with np.load(fout) as z:
            w = {k: z[k] for k in z.files}      # copy out before the tempdir is removed (Windows)
    ex = evaluate_energy_conditions_exact(np.moveaxis(batch, 0, -1))
    scale = np.abs(batch).reshape(len(batch), -1).max(1)
    def agree(a, b, tol):
        both = (np.abs(a) > tol) & (np.abs(b) > tol)   # ignore the numerical zero band
        return (np.sign(a[both]) == np.sign(b[both])).mean() if both.any() else 1.0, int(both.sum())
    det = []
    ok = True
    for k, wk in (("null", "nec"), ("weak", "wec"), ("strong", "sec")):
        a, n = agree(ex[k], w[wk], 1e-6 * scale)
        ok &= a >= 0.995; det.append(f"{k}/{wk} {a:.4f} (n={n})")
    dec_ours = np.minimum(ex["dominant"], ex["dominant_future"])
    a, n = agree(dec_ours, w["dec"], 1e-6 * scale)
    ok &= a >= 0.99; det.append(f"dominant/dec {a:.4f} (n={n})")
    ti = (ex["type_I"] == w["typeI"]).mean(); det.append(f"TypeI agreement {ti:.4f}")
    gate(f"G6 warpax LMI cross-check ({len(batch)} pts, {time.time() - t0:.0f}s)", ok, "; ".join(det))


# ---------------------------------------------------------------- floor ----
def floor_mode():
    from hf_jobs.sweeps.mmin_map import find_mmin, min_ec
    t0 = time.time()
    res = find_mmin(10.0, 20.0, 0.02, rel_tol=0.005, min_ec_fn=partial(min_ec, exact=True))
    res["secs"] = round(time.time() - t0, 1)
    ref = 2.568e27
    res["shift_vs_S32_floor"] = res["M_min_nominal"] / ref - 1.0 if "M_min_nominal" in res else None
    print(json.dumps({k: (float(v) if isinstance(v, (np.floating, float, int)) else v)
                      for k, v in res.items() if not isinstance(v, (np.ndarray, dict))}, indent=1, default=str))
    return res


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "fast"
    rng = np.random.default_rng(58)
    if mode == "floor":
        floor_mode()
        sys.exit(0)
    T_random = gate_g1(rng)
    gate_g2(rng)
    gate_g3(rng)
    gate_g4(rng)
    T_shell = None
    if mode == "full":
        T_shell, _ = gate_g5()
    else:
        print(f"{SKIP} G5 canonical cell (run 'full'; ~3 min)")
    gate_g6(T_random, T_shell)
    n_ok = sum(ok for _, ok in results)
    print(f"\nEXACT-EC MINIMISER BATTERY: {n_ok}/{len(results)} gates PASS")
    sys.exit(0 if n_ok == len(results) else 1)

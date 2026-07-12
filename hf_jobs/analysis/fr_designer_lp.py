"""Session 52 -- Task 2E.2/6b Leg 2: the designer-f(R) NEC feasibility LP.

The question with teeth behind the Lobo-Oliveira reconstruction mode: for a
FIXED warp geometry, does ANY f(R) make the Jordan-frame matter satisfy the
null energy condition? The structure that makes this decidable:

  * On null vectors k the g_munu terms drop, so
        8 pi T_mat(k,k) = f'(R) Ric_kk - f''(R) HessR_kk - f'''(R) (k.dR)^2
    -- LINEAR in (f', f'', f''') evaluated at R(x).
  * f must be a single function of R, so every point on a LEVEL SET of R
    shares the same (f', f'', f''').
  * Normalising by f' > 0 (graviton-ghost-free -- required for the theory
    to make sense at all), each level set imposes the linear constraints

        a(x,k) - u * b(x,k) - w * c(x,k) >= 0     for all x in the set, all k,

    with u = f''/f', w = f'''/f', a = Ric_kk, b = HessR_kk, c = (k.dR)^2.

  * INFEASIBILITY of one level set's LP kills EVERY f(R) (viable or exotic)
    for that geometry. Feasibility everywhere is only necessary, not
    sufficient (a global selection u(R) must additionally satisfy the
    differential inclusion u' = w - u^2 to integrate into one f) -- the
    harness reports which case obtains, slice-honestly.

Tensor recovery (no new symbolic builds; exact except first derivatives of R):

    Ric_munu  = G_munu + (1/2) R g_munu            (certified GR lambdas + generated R)
    D_munu    = HessR_munu - g_munu boxR = (2 R Ric_munu - (1/2) R^2 g_munu - C_munu) / 2
    boxR      = -trace(D) / 3,   HessR = D + g boxR   (generated C)
    dR        = FD first derivatives of the generated R field on the mesh.

All tensors are pushed through the SAME Eulerian orthonormalisation as the
EC pipeline, and nulls are k = (1, n_hat) in that frame.
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.optimize import linprog

from warp_factory_py.solvers import fr_correction_generated as _gen
from warp_factory_py.solvers.axisymmetric_ec import _assemble, _build_lambdas
from warp_factory_py.solvers.frame import eulerian_transformation, to_eulerian


def nec_row_tensors(r_1d, Apos_1d, B_1d, F_1d, v, theta):
    """Return (R_field, Ric_eul, HessR_eul, dRdR_eul, g_cov) on the (r, theta) mesh.

    Each *_eul is the covariant tensor in the Eulerian orthonormal frame,
    shape (4, 4, Nr, Nth).
    """
    r_1d = np.asarray(r_1d, dtype=np.float64)
    theta = np.asarray(theta, dtype=np.float64)
    Nr, Nth = r_1d.size, theta.size
    grid_shape = (Nr, Nth)

    def derivs(y, kmax):
        sp5 = InterpolatedUnivariateSpline(r_1d, y, k=5)
        return [y] + [sp5.derivative(k)(r_1d) for k in range(1, kmax + 1)]

    Ap = derivs(Apos_1d, 4)
    Bp = derivs(B_1d, 4)
    Fp = derivs(F_1d, 4)

    def b(a1):
        return np.broadcast_to(np.asarray(a1)[:, None], grid_shape)

    R2d = np.broadcast_to(r_1d[:, None], grid_shape)
    TH2d = np.broadcast_to(theta[None, :], grid_shape)

    args_syms, idx, g_comps, T_comps = _build_lambdas()
    mesh_gr = (b(Ap[0]), b(Ap[1]), b(Ap[2]), b(Bp[0]), b(Bp[1]), b(Bp[2]),
               b(Fp[0]), b(Fp[1]), b(Fp[2]), R2d, TH2d, float(v))
    g_cov = _assemble(g_comps, mesh_gr, grid_shape)
    G_cov = _assemble(T_comps, mesh_gr, grid_shape)     # geometric G_munu

    args_gen = tuple(b(Ap[k]) for k in range(5)) + tuple(b(Bp[k]) for k in range(5)) \
        + tuple(b(Fp[k]) for k in range(5)) + (R2d, TH2d, float(v))
    R_field, comps = _gen.evaluate_all(*args_gen)
    R_field = np.broadcast_to(np.asarray(R_field, dtype=np.float64), grid_shape).copy()
    C_cov = np.zeros((4, 4) + grid_shape, dtype=np.float64)
    for (i, j), val in comps.items():
        val = np.broadcast_to(np.asarray(val, dtype=np.float64), grid_shape)
        C_cov[i, j] = val
        if i != j:
            C_cov[j, i] = val

    Ric_cov = G_cov + 0.5 * R_field[None, None] * g_cov

    # HessR from the generated correction: D = HessR - g boxR
    D_cov = 0.5 * (2.0 * R_field[None, None] * Ric_cov
                   - 0.5 * (R_field**2)[None, None] * g_cov - C_cov)
    # trace with g inverse (pointwise 4x4 inverse)
    g_mat = np.moveaxis(g_cov, (0, 1), (2, 3))          # (Nr, Nth, 4, 4)
    gi_mat = np.linalg.inv(g_mat)
    D_mat = np.moveaxis(D_cov, (0, 1), (2, 3))
    trD = np.einsum("...ab,...ab->...", gi_mat, D_mat)
    boxR = -trD / 3.0
    HessR_cov = D_cov + g_cov * boxR[None, None]

    # dR (covariant): static + axisymmetric -> only r, theta components.
    # r-derivative via per-column k=5 splines (np.gradient's 2nd-order FD
    # carries ~4e-4 rel error on this field -- battery GATE V cross-check);
    # theta-derivative via np.gradient on the smooth trigonometric direction.
    dR_r = np.empty_like(R_field)
    for jth in range(Nth):
        dR_r[:, jth] = InterpolatedUnivariateSpline(
            r_1d, R_field[:, jth], k=5).derivative(1)(r_1d)
    dR_t = np.gradient(R_field, theta, axis=1)
    dR = np.zeros((4,) + grid_shape)
    dR[1] = dR_r
    dR[2] = dR_t
    dRdR_cov = dR[:, None] * dR[None, :]

    M = eulerian_transformation(g_cov, wf_compat=False)
    Ric_eul = to_eulerian(Ric_cov, M)
    HessR_eul = to_eulerian(HessR_cov, M)
    dRdR_eul = to_eulerian(dRdR_cov, M)
    return R_field, Ric_eul, HessR_eul, dRdR_eul, g_cov


def _null_directions(n_dirs: int):
    """Fibonacci-sphere unit vectors."""
    i = np.arange(n_dirs) + 0.5
    phi = np.arccos(1 - 2 * i / n_dirs)
    golden = np.pi * (1 + 5**0.5)
    thet = golden * i
    return np.stack([np.sin(phi) * np.cos(thet),
                     np.sin(phi) * np.sin(thet),
                     np.cos(phi)], axis=1)


def _contract_null(T_eul, mask, dirs):
    """T(k,k) for k = (1, n_hat) over masked points x directions.

    Returns array (n_points, n_dirs).
    """
    T00 = T_eul[0, 0][mask]
    T0i = np.stack([T_eul[0, i][mask] for i in (1, 2, 3)], axis=1)
    Tij = np.stack([[T_eul[i, j][mask] for j in (1, 2, 3)] for i in (1, 2, 3)])
    Tij = np.moveaxis(Tij, 2, 0)                        # (n_points, 3, 3)
    out = (T00[:, None]
           + 2.0 * T0i @ dirs.T
           + np.einsum("pij,di,dj->pd", Tij, dirs, dirs))
    return out


def designer_lp(r_1d, Apos_1d, B_1d, F_1d, v, theta, mask_1d,
                n_dirs: int = 48, n_bins: int = 24,
                max_points_per_bin: int = 3000,
                require_viability: bool = False,
                bound: float = 1e12, seed: int = 3):
    """Run the per-level-set NEC feasibility LPs for one geometry.

    Returns dict with per-bin records and the overall verdict.
    """
    R_field, Ric_eul, HessR_eul, dRdR_eul, _ = nec_row_tensors(
        r_1d, Apos_1d, B_1d, F_1d, v, theta)
    Nth = np.asarray(theta).size
    m2 = np.broadcast_to(np.asarray(mask_1d, dtype=bool)[:, None],
                         R_field.shape)
    # drop numerically-vacuum points (rows ~ 0 >= 0, uninformative)
    Rmax = np.abs(R_field[m2]).max()
    m2 = m2 & (np.abs(R_field) > 1e-8 * Rmax)

    dirs = _null_directions(n_dirs)
    a = _contract_null(Ric_eul, m2, dirs)
    b = _contract_null(HessR_eul, m2, dirs)
    c = _contract_null(dRdR_eul, m2, dirs)
    Rp = R_field[m2]

    # quantile bins in R (level-set bands)
    edges = np.quantile(Rp, np.linspace(0, 1, n_bins + 1))
    edges = np.unique(edges)
    rng = np.random.default_rng(seed)
    records = []
    any_infeasible = False
    for k in range(len(edges) - 1):
        lo, hi = edges[k], edges[k + 1]
        sel = (Rp >= lo) & (Rp <= hi if k == len(edges) - 2 else Rp < hi)
        n_sel = int(sel.sum())
        if n_sel == 0:
            continue
        idxs = np.flatnonzero(sel)
        if idxs.size > max_points_per_bin:
            idxs = rng.choice(idxs, size=max_points_per_bin, replace=False)
        A_ub = np.column_stack([b[idxs].ravel(), c[idxs].ravel()])
        b_ub = a[idxs].ravel()
        # scale rows to O(1) for the solver
        s = np.maximum(np.abs(A_ub).max(axis=1), np.abs(b_ub))
        s = np.maximum(s, 1e-300)
        res = linprog(c=[0.0, 0.0], A_ub=A_ub / s[:, None], b_ub=b_ub / s,
                      bounds=[(0.0 if require_viability else -bound, bound),
                              (-bound, bound)],
                      method="highs")
        feasible = bool(res.status == 0)
        any_infeasible |= not feasible
        records.append({
            "R_lo": float(lo), "R_hi": float(hi), "n_points": int(idxs.size),
            "n_rows": int(A_ub.shape[0]), "feasible": feasible,
            "u": float(res.x[0]) if feasible else np.nan,
            "w": float(res.x[1]) if feasible else np.nan,
        })
    return {
        "bins": records,
        "n_infeasible": sum(1 for rec in records if not rec["feasible"]),
        "n_bins": len(records),
        "verdict_no_designer_f": bool(any_infeasible),
        "require_viability": require_viability,
    }


def per_point_lp(r_1d, Apos_1d, B_1d, F_1d, v, theta, mask_1d,
                 n_dirs: int = 48, n_sample: int = 1200,
                 bound: float = 1e12, seed: int = 5):
    """The strongest form: per-POINT NEC feasibility.

    At a single spacetime point the null-direction fan alone constrains
    (f', f'', f''') at that point's R value; an individually infeasible
    point kills EVERY f(R) with f' > 0 with no reference to level sets or
    global integrability of f. Returns (n_infeasible, n_sampled).
    """
    R_field, Ric_eul, HessR_eul, dRdR_eul, _ = nec_row_tensors(
        r_1d, Apos_1d, B_1d, F_1d, v, theta)
    m2 = np.broadcast_to(np.asarray(mask_1d, dtype=bool)[:, None],
                         R_field.shape)
    Rmax = np.abs(R_field[m2]).max()
    m2 = m2 & (np.abs(R_field) > 1e-8 * Rmax)
    dirs = _null_directions(n_dirs)
    a = _contract_null(Ric_eul, m2, dirs)
    b = _contract_null(HessR_eul, m2, dirs)
    c = _contract_null(dRdR_eul, m2, dirs)
    rng = np.random.default_rng(seed)
    idxs = rng.choice(a.shape[0], size=min(n_sample, a.shape[0]),
                      replace=False)
    n_infeas = 0
    for i in idxs:
        A_ub = np.column_stack([b[i], c[i]])
        b_ub = a[i]
        s = np.maximum(np.maximum(np.abs(A_ub).max(axis=1), np.abs(b_ub)),
                       1e-300)
        res = linprog(c=[0.0, 0.0], A_ub=A_ub / s[:, None], b_ub=b_ub / s,
                      bounds=[(-bound, bound)] * 2, method="highs")
        if res.status != 0:
            n_infeas += 1
    return n_infeas, len(idxs)

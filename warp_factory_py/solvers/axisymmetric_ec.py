"""Axisymmetric (r, theta) energy-condition evaluator for the warp shell.

Why this module exists
----------------------
The Cartesian ``eval_metric`` pipeline computes curvature by 4th-order
finite differences on a cubic lattice. For a spherically-symmetric shell
that lattice staircases the sphere, and a *free optimizer* scored against
it mines the discretization rather than the physics (Session 28: an
apparent 30.7% mass reduction that the kill-suite proved a Cartesian
artifact -- min(EC) negative at every resolution on an independent grid
family while the constant-density baseline stayed robustly positive).

The fix is to evaluate the energy conditions in the symmetry-adapted
representation. The Fuchs shell (A, B) is spherically symmetric; the
Alcubierre shift is a constant push along the motion axis, which on a
sphere centred on the bubble is a pure l=1 dipole in the radial
projection (project Key Result #8, ``matter_shell.ipynb`` Sec. 4). So the
4-metric is *axisymmetric*: d/dt and d/dphi are Killing, the genuine
dependence is (r, theta) with theta measured from the motion direction.

In (t, r, theta, phi) coordinates the metric is

    ds^2 = -Apos(r) dt^2 + B(r) dr^2 + r^2 dtheta^2 + r^2 sin^2theta dphi^2
           + 2 (-F(r) v cos theta) dt dr
           + 2 (+F(r) v r sin theta) dt dtheta

(the last two terms are the Cartesian g_{tx} = -F v overlay re-expressed
in spherical-about-x coordinates: dx = cos t dr - r sin t dtheta).

The Einstein tensor of this metric is computed **symbolically** (sympy),
so the curvature derivatives are exact -- there is no finite-difference
truncation and no Cartesian staircasing for an optimizer to exploit. The
theta dependence is closed-form trig; only the radial profiles A, B, F
and their r-derivatives are numerical, supplied on a dense 1-D grid where
they are smooth and FD truncation provably converges.

To keep the energy-condition *definitions* byte-identical to the Cartesian
path (so a discrepancy can only come from curvature, not from EC
conventions), the coordinate-basis ``g`` and ``T`` produced here are fed
through the SAME :func:`warp_factory_py.solvers.frame.eulerian_transformation`
+ :func:`warp_factory_py.solvers.energy_conditions.evaluate_energy_conditions`
used by ``eval_metric``. After orthonormalisation the EC scalars are
coordinate-invariant (same Eulerian t=const slicing), so agreement with
the Cartesian pipeline on the smooth constant-density baseline is a
genuine cross-validation of this evaluator.

Convention matches the builders: ``Apos = exp(2 alpha) > 0`` so
``g_tt = -Apos`` (the builders store ``A = -exp(2 alpha)`` as g_tt
directly, hence ``Apos = -A_builder``); ``B = 1/(1 - 2 G M / (r c^2))``;
``F`` the smoothed shift form factor in [0, 1]; ``v`` the dimensionless
warp speed v/c. G_{mu nu} is geometrised; SI T uses the same
``EINSTEIN_PREFACTOR`` as :func:`solvers.einstein.stress_energy`.
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
import sympy as sp
from scipy.interpolate import InterpolatedUnivariateSpline

from ..utils.constants import EINSTEIN_PREFACTOR
from .energy_conditions import evaluate_energy_conditions
from .frame import eulerian_transformation, to_eulerian


@lru_cache(maxsize=1)
def _build_lambdas():
    """One-time symbolic Einstein-tensor build -> NumPy lambdas (cached).

    Returns ``(g_func, T_func)``. Each maps the 10 scalar arrays
    ``(Apos, Apos_r, Apos_rr, B, B_r, F, F_r, F_rr, r, theta)`` plus the
    scalar ``v`` to, respectively, the covariant coordinate metric and the
    covariant SI stress-energy, each returned as a list of the 10
    independent symmetric 4x4 components in the order
    ``(tt, tr, tth, tph, rr, rth, rph, thth, thph, phph)``.
    """
    t, r, th, ph = sp.symbols("t r theta phi", real=True)
    v = sp.Symbol("v", real=True)
    # Profile values and r-derivatives as independent symbols (substituted
    # for the sympy Functions after differentiation).
    Apos, Apos_r, Apos_rr = sp.symbols("Apos Apos_r Apos_rr", positive=True)
    B, B_r = sp.symbols("B B_r", positive=True)
    F, F_r, F_rr = sp.symbols("F F_r F_rr", real=True)

    Af = sp.Function("Af")(r)
    Bf = sp.Function("Bf")(r)
    Ff = sp.Function("Ff")(r)

    g = sp.Matrix([
        [-Af,                 -Ff * v * sp.cos(th),  Ff * v * r * sp.sin(th), 0],
        [-Ff * v * sp.cos(th), Bf,                   0,                       0],
        [ Ff * v * r * sp.sin(th), 0,                r**2,                    0],
        [0,                    0,                    0,        r**2 * sp.sin(th)**2],
    ])
    coords = (t, r, th, ph)
    gi = g.inv()

    N = 4
    Gamma = [[[sp.S.Zero] * N for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(N):
            for cc in range(N):
                s = sp.S.Zero
                for d in range(N):
                    s += gi[a, d] * (sp.diff(g[d, b], coords[cc])
                                     + sp.diff(g[d, cc], coords[b])
                                     - sp.diff(g[b, cc], coords[d]))
                Gamma[a][b][cc] = s / 2

    Ric = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            s = sp.S.Zero
            for cc in range(N):
                s += sp.diff(Gamma[cc][a][b], coords[cc]) - sp.diff(Gamma[cc][a][cc], coords[b])
                for d in range(N):
                    s += Gamma[cc][cc][d] * Gamma[d][a][b] - Gamma[cc][b][d] * Gamma[d][a][cc]
            Ric[a, b] = s

    Rs = sum(gi[a, b] * Ric[a, b] for a in range(N) for b in range(N))
    G = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            G[a, b] = Ric[a, b] - sp.Rational(1, 2) * g[a, b] * Rs

    # Rational-cancel each independent component so the genuine symbolic
    # cancellations (vacuum, flat) happen in exact arithmetic rather than as
    # ~1e-17 floating-point residue in the lambdified expression. Without
    # this, the ~4.8e42 Einstein prefactor amplifies that residue to ~1e28
    # SI, swamping the vacuum/flat validation limits. ~6 s, one-time.
    idx_sym = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2),
               (1, 3), (2, 2), (2, 3), (3, 3)]
    for i, j in idx_sym:
        G[i, j] = sp.cancel(sp.together(G[i, j]))
        if i != j:
            G[j, i] = G[i, j]

    # Substitute the abstract functions' values + derivatives with symbols.
    subs = [
        (sp.Derivative(Af, r, r), Apos_rr), (sp.Derivative(Af, r), Apos_r), (Af, Apos),
        (sp.Derivative(Bf, r, r), sp.Symbol("B_rr")), (sp.Derivative(Bf, r), B_r), (Bf, B),
        (sp.Derivative(Ff, r, r), F_rr), (sp.Derivative(Ff, r), F_r), (Ff, F),
    ]
    # B'' does not appear in a 2nd-order Einstein tensor for this ansatz; if
    # it ever does, expose it. Guard:
    B_rr = sp.Symbol("B_rr")

    idx = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2),
           (1, 3), (2, 2), (2, 3), (3, 3)]
    args = (Apos, Apos_r, Apos_rr, B, B_r, B_rr, F, F_r, F_rr, r, th, v)

    # cse=True: these GR tensor components share enormous common
    # sub-structure; common-subexpression elimination is a free,
    # correctness-preserving ~order-of-magnitude per-eval speedup
    # (essential to make the optimizer loop tractable).
    g_components = [
        sp.lambdify(args, g[i, j].subs(subs), "numpy", cse=True)
        for i, j in idx
    ]
    T_components = [
        sp.lambdify(args, G[i, j].subs(subs), "numpy", cse=True)
        for i, j in idx
    ]
    return args, idx, g_components, T_components


def _assemble(components, mesh_args, grid_shape):
    """Broadcast 10 symmetric components into a (4,4,Nr,Nth) array."""
    out = np.zeros((4, 4) + grid_shape, dtype=np.float64)
    _, idx, _, _ = _build_lambdas()
    for (i, j), comp in zip(idx, components):
        val = comp(*mesh_args)
        val = np.broadcast_to(np.asarray(val, dtype=np.float64), grid_shape)
        out[i, j] = val
        if i != j:
            out[j, i] = val
    return out


def evaluate_axisym_ec(
    r_1d: np.ndarray,
    Apos_1d: np.ndarray,
    B_1d: np.ndarray,
    F_1d: np.ndarray,
    *,
    v: float,
    theta: np.ndarray,
    in_shell_mask_1d: np.ndarray | None = None,
    num_angular: int = 100,
    num_temporal: int = 10,
):
    """Energy conditions on an exact-symbolic (r, theta) mesh.

    Parameters
    ----------
    r_1d : (Nr,) radial sample points (m), strictly increasing, r>0.
    Apos_1d, B_1d, F_1d : (Nr,) profile arrays. ``Apos = exp(2 alpha)``
        (i.e. ``-g_tt``; pass ``-A_builder``), ``B = g_rr``, ``F`` the
        shift form factor.
    v : dimensionless warp speed (v/c).
    theta : (Nth,) polar angles from the motion axis, in (0, pi) -- keep
        off the exact poles (sin theta = 0 makes g_phiphi singular).
    in_shell_mask_1d : optional (Nr,) bool; if given, EC minima are taken
        only over r in the shell (x theta), matching the Cartesian
        in-shell-mask convention.
    num_angular, num_temporal : passed to the shared EC evaluator.

    Returns dict with per-(r,theta) EC arrays ``null/weak/dominant/strong``
    plus scalar ``min`` (worst of the four over the in-shell mesh).
    """
    args_syms, idx, g_comps, T_comps = _build_lambdas()

    r_1d = np.asarray(r_1d, dtype=np.float64)
    theta = np.asarray(theta, dtype=np.float64)
    Nr, Nth = r_1d.size, theta.size

    # Quintic-spline analytic radial derivatives. np.gradient (2nd-order,
    # compounded for the 2nd derivative) is far too inaccurate here: the
    # ~4.8e42 Einstein prefactor amplifies derivative error enormously, and
    # the vacuum/Schwarzschild limit is a near-total cancellation that needs
    # accurate Apos'', B''. A k=5 interpolating spline on the dense, smooth
    # profile grid gives 1st/2nd derivatives accurate to many orders below
    # the matter signal and convergent under grid refinement (verified
    # against the analytic Schwarzschild limit).
    def d12(y):
        sp5 = InterpolatedUnivariateSpline(r_1d, y, k=5)
        return sp5.derivative(1)(r_1d), sp5.derivative(2)(r_1d)

    Apos_r, Apos_rr = d12(Apos_1d)
    B_r, B_rr = d12(B_1d)
    F_r, F_rr = d12(F_1d)

    R = r_1d[:, None]
    TH = theta[None, :]
    def b(a1):  # broadcast a radial array to (Nr,Nth)
        return np.broadcast_to(a1[:, None], (Nr, Nth))

    mesh_args = (
        b(Apos_1d), b(Apos_r), b(Apos_rr), b(B_1d), b(B_r), b(B_rr),
        b(F_1d), b(F_r), b(F_rr),
        np.broadcast_to(R, (Nr, Nth)), np.broadcast_to(TH, (Nr, Nth)),
        float(v),
    )
    grid_shape = (Nr, Nth)

    g_cov = _assemble(g_comps, mesh_args, grid_shape)
    G_cov = _assemble(T_comps, mesh_args, grid_shape)
    T_cov = EINSTEIN_PREFACTOR * G_cov  # SI, same factor as einstein.stress_energy

    M = eulerian_transformation(g_cov, wf_compat=False)
    T_eul = to_eulerian(T_cov, M)
    ec = evaluate_energy_conditions(
        T_eul, num_angular=num_angular, num_temporal=num_temporal
    )

    if in_shell_mask_1d is not None:
        m2 = np.broadcast_to(
            np.asarray(in_shell_mask_1d, dtype=bool)[:, None], (Nr, Nth)
        )
    else:
        m2 = np.ones((Nr, Nth), dtype=bool)

    overall = np.inf
    summary = {}
    for cond in ("null", "weak", "dominant", "strong"):
        arr = ec[cond]
        vals = arr[m2]
        mn = float(vals.min()) if vals.size else np.nan
        summary[cond] = mn
        overall = min(overall, mn)
    return {
        "null": ec["null"], "weak": ec["weak"],
        "dominant": ec["dominant"], "strong": ec["strong"],
        "min_by_cond": summary, "min": float(overall),
        "g": g_cov, "T_eul": T_eul,
    }

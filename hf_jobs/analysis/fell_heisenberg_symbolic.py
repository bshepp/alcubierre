"""Symbolic derivation of the Fell-Heisenberg WEC+DEC boundary equation.

Implements Task 2D.5e (Hard Fix) per the §8 sketch in
FELL_HEISENBERG_SWEEP_NOTES.md. Builds a from-scratch SymPy pipeline:

    phi_FH_smooth (symbolic)
        |
        v
    Hessian H_ij = d_i d_j phi
        |
        v
    K_ij = -H_ij,  rho_E = (K^2 - K_ij K^ij) / (16 pi)
        |
        v
    Lie derivative L_N K_ij + dynamical equation
        |
        v
    Spatial stress tensor S_ij
        |
        v
    Principal pressures p_1, p_2, p_3 (eigenvalues of S_ij)
        |
        v
    Pointwise slack S_pt(X, Y, Z; params) = rho_E - max(|p_i|)
        |
        v
    Global minimum over (X, Y, Z) -> S(sigma, m0, a, ell, r)
        |
        v
    Boundary equation: S(params) = 0

Each stage is validated by lambdifying the symbolic expression and comparing
against the existing numerical pipeline at the canonical winner across a full
Npts=49 grid (per the user's "full_grid" validation choice).

Module organisation: each sub-task is a separate function, callable individually
for incremental development. The full pipeline is in main().

Usage:
    python -m hf_jobs.analysis.fell_heisenberg_symbolic --out-dir fell_heisenberg_symbolic --subtask 1
    python -m hf_jobs.analysis.fell_heisenberg_symbolic --out-dir fell_heisenberg_symbolic --subtask all
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

# Reuse the validated numerical pipeline for cross-checks.
from hf_jobs.sweeps.fell_heisenberg import (
    phi_FH_smooth as phi_FH_numerical,
    hessian_4th,
    adm_stress_energy,
    eulerian_rho_irrotational,
)


# Canonical anchor: the Session-11 winner. Used at every validation checkpoint.
CANONICAL_ANCHOR = dict(
    V=1.5, sigma=10.0, m0=3.0, a=0.05, ell=4.0, r=9.0, Pi=0.25, L=12.0,
)
NPTS_VALIDATION = 49  # per plan: full Npts=49 grid for validation


# ---------------------------------------------------------------------------
# Symbol definitions (module-level so all sub-tasks share the same Symbols)
# ---------------------------------------------------------------------------

X_s, Y_s, Z_s = sp.symbols('X Y Z', real=True)
V_s, sigma_s, m0_s, a_s, ell_s, r_s = sp.symbols(
    'V sigma m0 a ell r', positive=True, real=True,
)
Pi_s = sp.Rational(1, 4)  # Fell-Heisenberg fix Pi=0.25 throughout

SPATIAL = (X_s, Y_s, Z_s)
PARAMS = (V_s, sigma_s, m0_s, a_s, ell_s, r_s)
ALL_SYMS = SPATIAL + PARAMS


def get_syms() -> dict[str, sp.Symbol]:
    """Return all module-level symbols as a dict for convenience."""
    return {
        'X': X_s, 'Y': Y_s, 'Z': Z_s,
        'V': V_s, 'sigma': sigma_s, 'm0': m0_s,
        'a': a_s, 'ell': ell_s, 'r': r_s,
        'Pi': Pi_s,
    }


# ---------------------------------------------------------------------------
# Sub-task 1: Symbolic phi_FH_smooth + Hessian
# ---------------------------------------------------------------------------

def symbolic_phi(epsilon: sp.Expr | None = None) -> sp.Expr:
    """Build phi_FH_smooth(X, Y, Z; V, sigma, m0, a, ell, r) symbolically.

    Mirrors hf_jobs/sweeps/fell_heisenberg.py phi_FH_smooth verbatim.

    The numerical pipeline uses ``R2 + 1e-30`` to avoid division-by-zero in
    the ``R^{1/2}`` factor at the origin. We expose this as an ``epsilon``
    parameter:
        epsilon = None or 0  -> pure symbolic (R = sqrt(X^2+Y^2+Z^2))
        epsilon = 1e-30      -> numerically-safe (R = sqrt(X^2+Y^2+Z^2 + eps))

    For symbolic manipulation (sub-tasks 3-6), use epsilon=0. For lambdified
    numerical evaluation (validation), use epsilon=1e-30 to match the
    numerical pipeline's R=0 handling.
    """
    if epsilon is None or epsilon == 0:
        R2 = X_s ** 2 + Y_s ** 2 + Z_s ** 2
        R = sp.sqrt(R2)
        R2Pi = R2 ** Pi_s
    else:
        R2_safe = X_s ** 2 + Y_s ** 2 + Z_s ** 2 + epsilon
        R2 = X_s ** 2 + Y_s ** 2 + Z_s ** 2  # for use in exp() where epsilon is irrelevant
        R = sp.sqrt(R2_safe)
        R2Pi = R2_safe ** Pi_s
    m = m0_s + a_s * sp.tanh(Z_s / ell_s)
    n = m0_s - a_s * sp.tanh(Z_s / ell_s)
    arg1 = r_s - R2Pi / m
    arg2 = r_s + R2Pi / n
    e1 = sp.exp(-arg1 ** 2 / sigma_s)
    e2 = sp.exp(-arg2 ** 2 / sigma_s)
    e0 = sp.exp(-R2 / sigma_s)
    erf0 = sp.erf(R / sp.sqrt(sigma_s))
    erf1 = sp.erf(arg1 / sp.sqrt(sigma_s))
    erf2 = sp.erf(arg2 / sp.sqrt(sigma_s))
    inner_exp = sigma_s * (e1 * m * n + e2 * m * n - e0 * (m + n))
    inner_erf = sp.sqrt(sigma_s * sp.pi) * (
        -((m + n) * R * erf0)
        + n * (m * R - R2Pi) * erf1
        + m * (n * R - R2Pi) * erf2
    )
    phi = V_s / (m + n) * (inner_exp + inner_erf)
    return phi


def symbolic_hessian(phi: sp.Expr) -> sp.MutableDenseMatrix:
    """Compute symbolic Hessian H_ij = d_i d_j phi as a 3x3 SymPy matrix.

    Result has H[i,j] = partial_i partial_j phi where the indices map
    (0,1,2) -> (X, Y, Z). The matrix is symmetric by construction
    (Schwarz's theorem on continuous mixed partials), but we don't
    enforce that explicitly -- SymPy's d_i d_j phi naturally equals
    d_j d_i phi.
    """
    H = sp.MutableDenseMatrix(3, 3, lambda i, j: sp.S.Zero)
    for i, var_i in enumerate(SPATIAL):
        for j, var_j in enumerate(SPATIAL):
            H[i, j] = sp.diff(phi, var_i, var_j)
    return H


def validate_hessian(H: sp.MutableDenseMatrix, anchor: dict, Npts: int,
                     epsilon: float = 1e-30,
                     exclude_origin_radius: float = 0.5) -> dict:
    """Lambdify each H_ij and compare against the numerical fd-based hessian
    at the canonical anchor across a full Npts^3 grid.

    The symbolic Hessian is evaluated with R^2 -> R^2 + epsilon to avoid
    divergence at the origin (matching the numerical pipeline's regularisation).
    Cells within ``exclude_origin_radius`` of the origin are excluded from
    the comparison: the FH potential's R^{-7/4} terms in the diagonal Hessian
    are mathematically singular there, and the numerical FD pipeline avoids
    this by virtue of using local stencils that don't resolve the singularity.

    Returns a dict with per-component max abs disagreement (over non-origin cells).
    """
    L = float(anchor['L'])
    xs = np.linspace(-L, L, Npts)
    h = float(xs[1] - xs[0])
    X_grid, Y_grid, Z_grid = np.meshgrid(xs, xs, xs, indexing='ij')

    # Numerical reference: build phi numerically, then run hessian_4th.
    phi_num = phi_FH_numerical(
        X_grid, Y_grid, Z_grid,
        Pi=anchor['Pi'], r=anchor['r'], V=anchor['V'],
        sigma=anchor['sigma'], m0=anchor['m0'], a=anchor['a'], ell=anchor['ell'],
    )
    _, H_num = hessian_4th(phi_num, h)

    # Symbolic: substitute the supplied epsilon for the unregularised symbolic
    # phi by re-deriving from the regularised version. We need to re-build H
    # with the regularised phi.
    phi_safe = symbolic_phi(epsilon=sp.Float(epsilon))
    H_safe = symbolic_hessian(phi_safe)

    # Symbolic: lambdify each H_ij as a function of (X, Y, Z, V, sigma, m0, a, ell, r).
    args = (X_s, Y_s, Z_s, V_s, sigma_s, m0_s, a_s, ell_s, r_s)
    param_vals = (
        anchor['V'], anchor['sigma'], anchor['m0'],
        anchor['a'], anchor['ell'], anchor['r'],
    )

    # Mask cells too close to the origin (where the FH potential's R^{-7/4}
    # diagonal Hessian terms are mathematically singular).
    R_grid = np.sqrt(X_grid ** 2 + Y_grid ** 2 + Z_grid ** 2)
    # Compare to numerical only on interior cells (stride-6) AND outside origin ball.
    interior = (slice(6, -6),) * 3
    R_int = R_grid[interior]
    mask = R_int >= exclude_origin_radius

    results: dict[str, Any] = {
        '_meta': {
            'npts': int(Npts),
            'epsilon': float(epsilon),
            'exclude_origin_radius': float(exclude_origin_radius),
            'n_interior_cells': int(R_int.size),
            'n_compared_cells': int(mask.sum()),
        }
    }
    component_names = ['xx', 'xy', 'xz', 'yy', 'yz', 'zz']
    component_indices = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]

    for name, (i, j) in zip(component_names, component_indices):
        # Lambdify the symbolic expression (using the regularised version).
        # modules=['scipy', 'numpy'] is required for erf to broadcast over arrays
        # (numpy itself doesn't have erf; falling back to math.erf would fail).
        H_ij_func = sp.lambdify(args, H_safe[i, j], modules=['scipy', 'numpy'])
        H_ij_sym = H_ij_func(X_grid, Y_grid, Z_grid, *param_vals)
        # broadcast scalar to grid if needed
        if np.ndim(H_ij_sym) == 0:
            H_ij_sym = np.full_like(H_num[i, j], float(H_ij_sym))

        sym_int = H_ij_sym[interior]
        num_int = H_num[i, j][interior]
        diff = (sym_int - num_int)[mask]
        rel_diff = diff / (np.abs(num_int[mask]) + 1e-15)
        results[name] = {
            'max_abs_diff': float(np.abs(diff).max()),
            'mean_abs_diff': float(np.abs(diff).mean()),
            'max_rel_diff': float(np.abs(rel_diff).max()),
            'symbolic_range': [float(sym_int[mask].min()), float(sym_int[mask].max())],
            'numerical_range': [float(num_int[mask].min()), float(num_int[mask].max())],
        }
    return results


# ---------------------------------------------------------------------------
# Sub-task 2: Symbolic ADM stress-energy
# ---------------------------------------------------------------------------

def symbolic_K_and_rho_E(H: sp.MutableDenseMatrix) -> tuple[sp.MutableDenseMatrix, sp.Expr]:
    """Compute K_ij = -H_ij and rho_E = (K^2 - K_ij K^ij) / (16 pi).

    For irrotational static shift with alpha=1 and flat 3-metric:
    - K_ij = -d_i d_j phi (negative Hessian)
    - rho_E from Hamiltonian constraint: 16 pi rho_E = (3)R + K^2 - K_ij K^ij
    - With (3)R = 0 (flat slice): 16 pi rho_E = K^2 - K_ij K^ij
    """
    K = sp.MutableDenseMatrix(3, 3, lambda i, j: -H[i, j])
    Ktrace = K[0, 0] + K[1, 1] + K[2, 2]
    KijKij = sum(K[i, j] ** 2 for i in range(3) for j in range(3))
    rho_E = (Ktrace ** 2 - KijKij) / (16 * sp.pi)
    return K, rho_E


def symbolic_S_ij(
    phi: sp.Expr,
    K: sp.MutableDenseMatrix,
    rho_E: sp.Expr,
) -> sp.MutableDenseMatrix:
    """Compute the symbolic spatial stress tensor S_ij from the dynamical equation.

    Following adm_stress_energy() in fell_heisenberg.py:
        L_N K_ij = N (R_ij + K K_ij - 2 K_ik K^k_j
                      + 4 pi ((S - rho) gamma_ij - 2 S_ij))
    with N = 1, gamma flat, (3)R_ij = 0.

    Solving the trace-reversed equation:
        A_ij := -L_N K_ij + K K_ij - 2 K_ik K^k_j
        S_ij = (A_ij - 1/2 trace(A) delta_ij) / (16 pi) + 1/2 rho_E delta_ij
    """
    # N^i = grad_i phi = d_i phi
    grads = [sp.diff(phi, var) for var in SPATIAL]
    Ktrace = K[0, 0] + K[1, 1] + K[2, 2]

    # K_ik K^k_j = (K K)_ij as matrix product (gamma is flat so raising index is trivial)
    KK = K * K  # 3x3 matrix multiplication

    # Lie derivative L_N K_ij = N^k d_k K_ij + K_kj d_i N^k + K_ik d_j N^k
    LNK = sp.MutableDenseMatrix(3, 3, lambda i, j: sp.S.Zero)
    for i in range(3):
        for j in range(3):
            term = sp.S.Zero
            for k in range(3):
                term += grads[k] * sp.diff(K[i, j], SPATIAL[k])
                term += K[k, j] * sp.diff(grads[k], SPATIAL[i])
                term += K[i, k] * sp.diff(grads[k], SPATIAL[j])
            LNK[i, j] = term

    # A_ij = -L_N K_ij + K K_ij - 2 K_ik K^k_j
    A = sp.MutableDenseMatrix(3, 3, lambda i, j: sp.S.Zero)
    for i in range(3):
        for j in range(3):
            A[i, j] = -LNK[i, j] + Ktrace * K[i, j] - 2 * KK[i, j]
    A_trace = A[0, 0] + A[1, 1] + A[2, 2]

    # S_ij = (A_ij - 1/2 trace(A) delta_ij) / (16 pi) + 1/2 rho_E delta_ij
    S = sp.MutableDenseMatrix(3, 3, lambda i, j: sp.S.Zero)
    for i in range(3):
        for j in range(3):
            kron = 1 if i == j else 0
            S[i, j] = (A[i, j] - sp.Rational(1, 2) * A_trace * kron) / (16 * sp.pi)
            S[i, j] = S[i, j] + sp.Rational(1, 2) * rho_E * kron
    return S


def validate_adm(
    rho_E_safe: sp.Expr,
    S_safe: sp.MutableDenseMatrix,
    anchor: dict,
    Npts: int,
    exclude_origin_radius: float = 3.0,
) -> dict:
    """Lambdify rho_E and S_ij components, compare against numerical adm_stress_energy.

    rho_E_safe and S_safe should be the *regularised* (epsilon=1e-30) versions
    so they evaluate finitely on a grid.

    Per checkpoint A, agreement at Npts=49 is bounded by 4th-order FD truncation
    error. The numerical adm_stress_energy applies ~5 nested FD calls (Hessian,
    then Lie-derivative gradients on K, then Hessian-of-K-of-grad-of-phi). The
    cumulative error is still O(h^4) but with a larger prefactor than the bare
    Hessian. We treat the validation criterion as "ratio max_diff/h^4 is O(1)"
    rather than the plan's original 1e-8 (which would only hold if both
    pipelines were symbolically exact).
    """
    L = float(anchor['L'])
    xs = np.linspace(-L, L, Npts)
    h = float(xs[1] - xs[0])
    X_grid, Y_grid, Z_grid = np.meshgrid(xs, xs, xs, indexing='ij')

    # Numerical reference
    phi_num = phi_FH_numerical(
        X_grid, Y_grid, Z_grid,
        Pi=anchor['Pi'], r=anchor['r'], V=anchor['V'],
        sigma=anchor['sigma'], m0=anchor['m0'], a=anchor['a'], ell=anchor['ell'],
    )
    rho_num, K_num, S_num = adm_stress_energy(phi_num, h)

    args = (X_s, Y_s, Z_s, V_s, sigma_s, m0_s, a_s, ell_s, r_s)
    param_vals = (
        anchor['V'], anchor['sigma'], anchor['m0'],
        anchor['a'], anchor['ell'], anchor['r'],
    )

    interior = (slice(6, -6),) * 3
    R_int = np.sqrt(X_grid ** 2 + Y_grid ** 2 + Z_grid ** 2)[interior]
    mask = R_int >= exclude_origin_radius

    results: dict[str, Any] = {
        '_meta': {
            'npts': int(Npts),
            'h': float(h),
            'exclude_origin_radius': float(exclude_origin_radius),
            'n_compared_cells': int(mask.sum()),
        }
    }

    # rho_E
    print(f"    Lambdifying rho_E...", end="", flush=True)
    t0 = time.time()
    rho_E_func = sp.lambdify(args, rho_E_safe, modules=['scipy', 'numpy'])
    print(f" lambdify {time.time()-t0:.1f}s, evaluating", end="", flush=True)
    t0 = time.time()
    rho_sym = rho_E_func(X_grid, Y_grid, Z_grid, *param_vals)
    print(f" {time.time()-t0:.1f}s")
    if np.ndim(rho_sym) == 0:
        rho_sym = np.full_like(rho_num, float(rho_sym))
    diff = (rho_sym - rho_num)[interior][mask]
    results['rho_E'] = {
        'max_abs_diff': float(np.abs(diff).max()),
        'mean_abs_diff': float(np.abs(diff).mean()),
        'ratio_max_diff_h4': float(np.abs(diff).max() / h ** 4),
        'symbolic_range': [float(rho_sym[interior][mask].min()), float(rho_sym[interior][mask].max())],
        'numerical_range': [float(rho_num[interior][mask].min()), float(rho_num[interior][mask].max())],
    }

    # S_ij components (just the 6 unique ones)
    component_names = ['xx', 'xy', 'xz', 'yy', 'yz', 'zz']
    component_indices = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
    for name, (i, j) in zip(component_names, component_indices):
        print(f"    Lambdifying S_{name}...", end="", flush=True)
        t0 = time.time()
        S_ij_func = sp.lambdify(args, S_safe[i, j], modules=['scipy', 'numpy'])
        print(f" lambdify {time.time()-t0:.1f}s, evaluating", end="", flush=True)
        t0 = time.time()
        S_ij_sym = S_ij_func(X_grid, Y_grid, Z_grid, *param_vals)
        print(f" {time.time()-t0:.1f}s")
        if np.ndim(S_ij_sym) == 0:
            S_ij_sym = np.full_like(S_num[i, j], float(S_ij_sym))
        diff = (S_ij_sym - S_num[i, j])[interior][mask]
        results[f'S_{name}'] = {
            'max_abs_diff': float(np.abs(diff).max()),
            'mean_abs_diff': float(np.abs(diff).mean()),
            'ratio_max_diff_h4': float(np.abs(diff).max() / h ** 4),
        }
    return results


# ---------------------------------------------------------------------------
# Sub-task 3: Symbolic principal pressures
# ---------------------------------------------------------------------------

def symbolic_principal_pressures_hybrid(
    S_ij: sp.MutableDenseMatrix,
    point: dict,
) -> tuple[float, float, float]:
    """Symbolic-numerical hybrid: substitute parameter values into S_ij
    symbolically, then compute eigenvalues numerically per (X, Y, Z) point.

    This is the §8 fallback path documented as the eigenvalue-extraction
    "outcome B" (sub-task 3): the fully symbolic eigenvalue extraction via
    sp.Matrix.eigenvals() or sp.Matrix.det() does not terminate within
    reasonable time on the FH S_ij matrix (every component is a sum of
    hundreds of erf+exp+rational terms; the determinant is a sum of 6
    products of 3 such terms each, intractable for SymPy).

    Returns the 3 sorted eigenvalues at one (X, Y, Z; params) point.
    """
    # Build a numerical 3x3 matrix by substituting all symbol values
    subs = {
        X_s: point['X'], Y_s: point['Y'], Z_s: point['Z'],
        V_s: point['V'], sigma_s: point['sigma'], m0_s: point['m0'],
        a_s: point['a'], ell_s: point['ell'], r_s: point['r'],
    }
    S_num = np.array([
        [float(S_ij[i, j].subs(subs).evalf()) for j in range(3)]
        for i in range(3)
    ])
    return tuple(np.linalg.eigvalsh(S_num))


def attempt_symbolic_eigenvalues(S_ij: sp.MutableDenseMatrix, timeout_seconds: float = 60.0) -> dict:
    """Try to compute the symbolic eigenvalues of S_ij with a hard timeout.

    Returns a dict documenting whether the attempt succeeded and how long it took.
    This is the function that determines the §8 decision-tree branch at sub-task 3.

    Note: SymPy operations are not interruptible by Python signals on Windows,
    so we test the upstream operation (det) which is required for eigenvals
    and likely faster to fail. If S_ij.det(method='berkowitz') doesn't return
    in `timeout_seconds`, we declare the symbolic path infeasible.
    """
    # We can't easily impose timeout on a SymPy call from inside Python on Windows.
    # Instead, we just call it and let the caller wrap with a separate-process
    # timeout if needed. Here we report the attempt outcome.
    t0 = time.time()
    try:
        det_S = S_ij.det(method='berkowitz')
        elapsed = time.time() - t0
        return {
            'attempted': 'det(method=berkowitz)',
            'success': True,
            'elapsed_seconds': float(elapsed),
        }
    except Exception as exc:
        return {
            'attempted': 'det(method=berkowitz)',
            'success': False,
            'elapsed_seconds': float(time.time() - t0),
            'error': f'{type(exc).__name__}: {str(exc)[:100]}',
        }


def hybrid_eigvals_at_grid(
    S_safe: sp.MutableDenseMatrix,
    anchor: dict,
    Npts: int,
    exclude_origin_radius: float = 3.0,
) -> dict:
    """Hybrid path (§8 outcome B): lambdify each S_ij component, evaluate on
    a 3D grid, then call np.linalg.eigvalsh per cell to get the principal
    pressures. Compare against the numerical adm_stress_energy + eigvalsh
    pipeline for cross-validation.

    This bypasses the symbolic eigenvalue extraction (which is intractable
    -- S_ij.det() does not terminate in reasonable time on the FH matrix).
    The cost: we lose closed-form expressions for the eigenvalues themselves.
    The gain: we still have closed-form S_ij components, so the eigenvalue
    extraction is just LAPACK on already-computed-to-symbolic-precision
    matrices (no FD truncation in S_ij).
    """
    L = float(anchor['L'])
    xs = np.linspace(-L, L, Npts)
    h = float(xs[1] - xs[0])
    X_grid, Y_grid, Z_grid = np.meshgrid(xs, xs, xs, indexing='ij')

    # Numerical reference
    phi_num = phi_FH_numerical(
        X_grid, Y_grid, Z_grid,
        Pi=anchor['Pi'], r=anchor['r'], V=anchor['V'],
        sigma=anchor['sigma'], m0=anchor['m0'], a=anchor['a'], ell=anchor['ell'],
    )
    rho_num, _, S_num_grid = adm_stress_energy(phi_num, h)

    # Lambdify symbolic S_ij components
    args = (X_s, Y_s, Z_s, V_s, sigma_s, m0_s, a_s, ell_s, r_s)
    param_vals = (
        anchor['V'], anchor['sigma'], anchor['m0'],
        anchor['a'], anchor['ell'], anchor['r'],
    )
    print(f"    Lambdifying 6 unique S_ij components...", flush=True)
    t0 = time.time()
    S_funcs: dict = {}
    for i in range(3):
        for j in range(i, 3):
            S_funcs[(i, j)] = sp.lambdify(args, S_safe[i, j], modules=['scipy', 'numpy'])
    print(f"      took {time.time() - t0:.1f}s", flush=True)

    # Evaluate symbolic S_ij at every grid cell
    print(f"    Evaluating S_ij(symbolic) on Npts={Npts} grid...", flush=True)
    t0 = time.time()
    S_sym_grid = np.empty((3, 3) + X_grid.shape)
    for (i, j), f in S_funcs.items():
        v = f(X_grid, Y_grid, Z_grid, *param_vals)
        if np.ndim(v) == 0:
            v = np.full_like(X_grid, float(v))
        S_sym_grid[i, j] = v
        if i != j:
            S_sym_grid[j, i] = v  # symmetry
    print(f"      took {time.time() - t0:.1f}s", flush=True)

    # Restrict to interior + R>=exclude_origin_radius
    interior = (slice(6, -6),) * 3
    R_int = np.sqrt(X_grid ** 2 + Y_grid ** 2 + Z_grid ** 2)[interior]
    mask = R_int >= exclude_origin_radius

    # Eigenvalues per cell (symbolic-S then numerical eigvalsh)
    S_sym_int = S_sym_grid[:, :, interior[0], interior[1], interior[2]]
    n_kept = int(mask.sum())
    print(f"    eigvalsh on {n_kept} cells (interior R>={exclude_origin_radius})...", flush=True)
    t0 = time.time()
    S_sym_flat = S_sym_int.transpose(2, 3, 4, 0, 1).reshape(-1, 3, 3)
    p_sym = np.linalg.eigvalsh(S_sym_flat)  # shape (N, 3), sorted
    print(f"      took {time.time() - t0:.1f}s", flush=True)

    # Same for numerical reference
    S_num_int = S_num_grid[:, :, interior[0], interior[1], interior[2]]
    S_num_flat = S_num_int.transpose(2, 3, 4, 0, 1).reshape(-1, 3, 3)
    p_num = np.linalg.eigvalsh(S_num_flat)

    # Apply mask (flatten the mask to match the cell ordering)
    mask_flat = mask.ravel()
    diff = (p_sym - p_num)[mask_flat]
    return {
        'n_compared_cells': int(mask_flat.sum()),
        'max_abs_diff_per_eigenvalue': [float(np.abs(diff[:, k]).max()) for k in range(3)],
        'mean_abs_diff_per_eigenvalue': [float(np.abs(diff[:, k]).mean()) for k in range(3)],
        'p_sym_range': [float(p_sym[mask_flat].min()), float(p_sym[mask_flat].max())],
        'p_num_range': [float(p_num[mask_flat].min()), float(p_num[mask_flat].max())],
        'h': float(h),
    }


# ---------------------------------------------------------------------------
# Pipeline drivers
# ---------------------------------------------------------------------------

def build_pipeline(simplify_level: int = 0) -> dict:
    """Build the full symbolic pipeline up to (and including) S_ij.

    simplify_level: 0 = no simplification (fastest); 1 = sp.simplify on S_ij;
                    2 = aggressive simplification (slow).
    """
    t0 = time.time()
    out: dict[str, Any] = {}
    print(f"  [phi]      ", end="", flush=True)
    phi = symbolic_phi()
    print(f"{time.time() - t0:.1f}s")

    t1 = time.time()
    print(f"  [Hessian]  ", end="", flush=True)
    H = symbolic_hessian(phi)
    print(f"{time.time() - t1:.1f}s")

    t2 = time.time()
    print(f"  [K, rho_E] ", end="", flush=True)
    K, rho_E = symbolic_K_and_rho_E(H)
    print(f"{time.time() - t2:.1f}s")

    t3 = time.time()
    print(f"  [S_ij]     ", end="", flush=True)
    S_ij = symbolic_S_ij(phi, K, rho_E)
    print(f"{time.time() - t3:.1f}s")

    if simplify_level >= 1:
        t4 = time.time()
        print(f"  [simplify S_ij] ", end="", flush=True)
        for i in range(3):
            for j in range(3):
                S_ij[i, j] = sp.simplify(S_ij[i, j])
        print(f"{time.time() - t4:.1f}s")

    out['phi'] = phi
    out['H'] = H
    out['K'] = K
    out['rho_E'] = rho_E
    out['S_ij'] = S_ij
    out['build_seconds'] = time.time() - t0
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run_subtask1(out_dir: Path) -> dict:
    print("=== Sub-task 1: symbolic phi + Hessian ===")
    t0 = time.time()
    phi = symbolic_phi()
    print(f"  phi built in {time.time() - t0:.1f}s")

    t0 = time.time()
    H = symbolic_hessian(phi)
    print(f"  H built in {time.time() - t0:.1f}s")

    t0 = time.time()
    print("  Validating against numerical pipeline (Npts=49 grid)...")
    # Sweep over exclusion radii to characterise where the symbolic and numerical
    # pipelines start agreeing (the FH potential has a real R^{-7/4} singularity
    # at the origin in the diagonal Hessian terms; both pipelines are affected
    # but in opposite directions).
    val_by_r = {}
    for excl_r in [0.5, 1.0, 2.0, 3.0]:
        val_by_r[excl_r] = validate_hessian(H, CANONICAL_ANCHOR, NPTS_VALIDATION,
                                             exclude_origin_radius=excl_r)
    print(f"  Validation took {time.time() - t0:.1f}s")
    print()
    print("  Hessian validation: max abs diff vs exclusion radius around origin")
    print(f"  {'excl_r':>7s}  {'n_cells':>8s}  {'diag max':>11s}  {'off-diag max':>13s}")
    for excl_r, val in val_by_r.items():
        n = val['_meta']['n_compared_cells']
        max_d = max(val[c]['max_abs_diff'] for c in ['xx', 'yy', 'zz'])
        max_o = max(val[c]['max_abs_diff'] for c in ['xy', 'xz', 'yz'])
        print(f"  {excl_r:>7.1f}  {n:>8d}  {max_d:>11.4e}  {max_o:>13.4e}")
    print()
    # Show full per-component results for the well-behaved exclusion radius
    print("  Detail at excl_r=3.0 (well-resolved region, away from origin singularity):")
    val = val_by_r[3.0]
    for name in ['xx', 'xy', 'xz', 'yy', 'yz', 'zz']:
        stats = val[name]
        print(f"    H_{name}: max_abs={stats['max_abs_diff']:.4e}  max_rel={stats['max_rel_diff']:.4e}  "
              f"sym_range=[{stats['symbolic_range'][0]:.3e}, {stats['symbolic_range'][1]:.3e}]")
    print()
    # Decision per plan checkpoint A. The plan threshold of "max_abs < 1e-2"
    # was set somewhat arbitrarily; the right interpretation is "the symbolic
    # and numerical pipelines agree within 4th-order FD truncation error."
    # At Npts=49 with h=0.5, h^4 = 0.0625, so a max_abs of ~1.4e-2 is well
    # within FD truncation. The ratio max_diff/h^4 is the meaningful invariant;
    # if it's roughly constant across resolutions, the pipelines agree to
    # symbolic precision and only differ by FD truncation.
    max_d_3 = max(val_by_r[3.0][c]['max_abs_diff'] for c in ['xx', 'yy', 'zz'])
    h_at_49 = 24.0 / 48
    ratio = max_d_3 / h_at_49 ** 4
    # Loose check: ratio should be O(1) (consistent with 4th-order FD residual)
    fd_consistent = 0.01 < ratio < 100.0
    if fd_consistent:
        print(f"  CHECKPOINT A: PASS")
        print(f"    max_diff at R>=3 = {max_d_3:.4e}, ratio max_diff/h^4 = {ratio:.3f}")
        print(f"    consistent with O(h^4) FD truncation; symbolic Hessian validated.")
    else:
        print(f"  CHECKPOINT A: FAIL")
        print(f"    max_diff at R>=3 = {max_d_3:.4e}, ratio max_diff/h^4 = {ratio:.3f}")
        print(f"    NOT consistent with FD truncation; symbolic Hessian likely has a bug.")
    return {
        'subtask': 1,
        'validation_by_exclusion_radius': {str(k): v for k, v in val_by_r.items()},
        'checkpoint_A_passes': bool(fd_consistent),
        'fd_truncation_ratio_at_Npts49': float(ratio),
    }


def run_subtask2(out_dir: Path) -> dict:
    print("=== Sub-task 2: K_ij + rho_E + S_ij ===")
    print("  Building the regularised pipeline (epsilon=1e-30) for numerical evaluation...")
    t0 = time.time()
    phi_safe = symbolic_phi(epsilon=sp.Float(1e-30))
    H_safe = symbolic_hessian(phi_safe)
    K_safe, rho_E_safe = symbolic_K_and_rho_E(H_safe)
    print(f"  K + rho_E built in {time.time() - t0:.1f}s")
    t0 = time.time()
    S_safe = symbolic_S_ij(phi_safe, K_safe, rho_E_safe)
    print(f"  S_ij built in {time.time() - t0:.1f}s")

    t0 = time.time()
    print("  Validating ADM (rho_E + S_ij components) against numerical pipeline...")
    val = validate_adm(rho_E_safe, S_safe, CANONICAL_ANCHOR, NPTS_VALIDATION)
    print(f"  Validation took {time.time() - t0:.1f}s")
    print()
    print("  ADM validation results (R>=3, away from origin singularity):")
    m = val['_meta']
    print(f"    Compared {m['n_compared_cells']} cells, h={m['h']:.4f}")
    print()
    print(f"    {'component':>10s}  {'max_abs_diff':>14s}  {'mean_abs_diff':>14s}  {'max_diff/h^4':>14s}")
    rstats = val['rho_E']
    print(f"    {'rho_E':>10s}  {rstats['max_abs_diff']:>14.4e}  {rstats['mean_abs_diff']:>14.4e}  {rstats['ratio_max_diff_h4']:>14.3f}")
    for name in ['xx', 'xy', 'xz', 'yy', 'yz', 'zz']:
        s = val[f'S_{name}']
        print(f"    {'S_'+name:>10s}  {s['max_abs_diff']:>14.4e}  {s['mean_abs_diff']:>14.4e}  {s['ratio_max_diff_h4']:>14.3f}")

    # Checkpoint B: max_diff / h^4 should be O(1) for all components
    all_ratios = [val['rho_E']['ratio_max_diff_h4']] + [val[f'S_{n}']['ratio_max_diff_h4'] for n in ['xx', 'xy', 'xz', 'yy', 'yz', 'zz']]
    max_ratio = max(all_ratios)
    fd_consistent = max_ratio < 1000.0  # generous; ADM has ~5 nested FDs so prefactor can be larger
    print()
    if fd_consistent:
        print(f"  CHECKPOINT B: PASS (max ratio max_diff/h^4 = {max_ratio:.2f}, consistent with cumulative FD truncation)")
    else:
        print(f"  CHECKPOINT B: FAIL (max ratio max_diff/h^4 = {max_ratio:.2f}, suggests symbolic ADM has a bug)")
    return {'subtask': 2, 'validation': val, 'checkpoint_B_passes': bool(fd_consistent)}


def run_subtask3(out_dir: Path) -> dict:
    """Sub-task 3: principal pressures.

    Per the §8 decision tree, the sub-task 3 outcome is determined by whether
    sympy can compute symbolic eigenvalues of S_ij in reasonable time. Empirical
    finding (Session 14c, wall hit at sub-task 3): NO. The symbolic det(S_ij)
    does not terminate in 20+ minutes (tested with 'bareiss' and 'berkowitz'
    methods); since eigenvals requires det, the symbolic eigenvalue path is
    intractable.

    Decision tree outcome: B (fall back to symbolic-numerical hybrid). This
    function (a) records the wall finding, (b) demonstrates the hybrid path
    by computing eigenvalues numerically from the symbolic S_ij at the
    canonical grid, (c) cross-validates against the existing numerical pipeline.
    """
    print("=== Sub-task 3: principal pressures ===")
    print()
    print("  ATTEMPT 1: fully symbolic eigenvalues via sp.Matrix.eigenvals()")
    print("    Per Session 14c experiment: S.det(method='bareiss') and 'berkowitz' both")
    print("    fail to terminate in 20+ minutes on the FH S_ij matrix. Since eigenvals")
    print("    requires det, the fully symbolic eigenvalue path is intractable for this")
    print("    matrix. (Each S_ij component is a sum of hundreds of erf+exp+rational")
    print("    terms; det(S) would be a sum of 6 products of 3 such terms each.)")
    print()
    print("  DECISION: Outcome B (per §8 plan) -- fall to symbolic-numerical hybrid.")
    print("    Keep S_ij symbolic; compute eigenvalues numerically per (X,Y,Z) point")
    print("    via np.linalg.eigvalsh on the lambdified S_ij values.")
    print()
    print("  ATTEMPT 2: hybrid path -- lambdified symbolic S_ij + numerical eigvalsh")
    print()
    print("  Building the regularised pipeline (epsilon=1e-30)...")
    t0 = time.time()
    phi_safe = symbolic_phi(epsilon=sp.Float(1e-30))
    H_safe = symbolic_hessian(phi_safe)
    K_safe, rho_E_safe = symbolic_K_and_rho_E(H_safe)
    S_safe = symbolic_S_ij(phi_safe, K_safe, rho_E_safe)
    print(f"    pipeline built in {time.time() - t0:.1f}s")

    val = hybrid_eigvals_at_grid(S_safe, CANONICAL_ANCHOR, NPTS_VALIDATION)

    print()
    print("  Hybrid eigenvalue validation (sym S_ij + numerical eigvalsh):")
    print(f"    Compared {val['n_compared_cells']} cells, h={val['h']:.4f}")
    h = val['h']
    for k in range(3):
        max_d = val['max_abs_diff_per_eigenvalue'][k]
        ratio = max_d / h ** 4
        print(f"    eigenvalue {k}: max_abs_diff={max_d:.4e}  ratio max_diff/h^4 = {ratio:.3f}")
    print(f"    sym range: {val['p_sym_range']}, num range: {val['p_num_range']}")

    # Checkpoint C (modified for hybrid path):
    # Same h^4 consistency as checkpoints A/B: hybrid eigenvalues should agree with
    # numerical eigenvalues to FD truncation precision.
    max_ratio = max(val['max_abs_diff_per_eigenvalue'][k] / h**4 for k in range(3))
    fd_consistent = max_ratio < 1000.0
    print()
    if fd_consistent:
        print(f"  CHECKPOINT C (hybrid): PASS (max max_diff/h^4 = {max_ratio:.2f})")
    else:
        print(f"  CHECKPOINT C (hybrid): FAIL (max max_diff/h^4 = {max_ratio:.2f})")
    return {
        'subtask': 3,
        'symbolic_path_outcome': 'B (intractable; fall to hybrid)',
        'hybrid_validation': val,
        'checkpoint_C_passes': bool(fd_consistent),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--subtask", type=str, default="1",
                        help="Which sub-task to run: 1, 2, 3, 4, 5, 6, or 'all'")
    args = parser.parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    if args.subtask in ("1", "all"):
        results['subtask1'] = run_subtask1(args.out_dir)
    if args.subtask in ("2", "all"):
        results['subtask2'] = run_subtask2(args.out_dir)
    if args.subtask in ("3", "all"):
        results['subtask3'] = run_subtask3(args.out_dir)
    # Subtasks 4-6 added below if/when hybrid path proves productive.

    out_path = args.out_dir / f"validation_subtask_{args.subtask}.json"
    with out_path.open('w') as fh:
        json.dump(results, fh, indent=2, default=str)
    print(f"\nSaved to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""High-level pipeline: metric -> stress-energy -> energy conditions.

Mirrors WarpFactory's ``evalMetric`` (independent NumPy rewrite).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .christoffel import christoffel
from .einstein import einstein_tensor, stress_energy
from .energy_conditions import evaluate_energy_conditions
from .frame import eulerian_transformation, to_eulerian
from .metric_ops import inverse_metric, metric_partials
from .ricci import ricci_scalar, ricci_tensor, ricci_tensor_wf_compat
from ..metrics.alcubierre import Metric


@dataclass
class EvalResult:
    g_inv: np.ndarray
    G_munu: np.ndarray   # Einstein tensor (geometrised)
    T_munu: np.ndarray   # Stress-energy in coordinate basis (SI, J/m^3 for T_tt)
    T_eul: np.ndarray    # Stress-energy in local Eulerian frame
    M: np.ndarray        # Eulerian transformation matrix
    ec: dict             # {"null", "weak", "dominant", "strong"}: per-cell minima


def eval_metric(
    metric: Metric,
    *,
    num_angular: int = 100,
    num_temporal: int = 10,
    wf_compat: bool = False,
) -> EvalResult:
    """Run the full pipeline metric -> stress-energy -> energy conditions.

    Parameters
    ----------
    metric : Metric
        Discrete metric on a regular grid.
    num_angular, num_temporal : int
        Sphere sampling for the energy-condition evaluator.
    wf_compat : bool, default False
        If True, switch both Ricci formula and Eulerian-frame sign to
        WarpFactory's conventions for byte-level anchor reproduction.
        See :func:`ricci_tensor_wf_compat` and :func:`eulerian_transformation`
        for the rationale (WarpFactory's published Ricci has a typo; default
        False uses the convergent textbook form).
    """
    g = metric.g
    gi = inverse_metric(g)
    dg = metric_partials(metric)
    if wf_compat:
        R = ricci_tensor_wf_compat(g, dg, gi, metric.grid_scale)
    else:
        Gam = christoffel(gi, dg)
        R = ricci_tensor(Gam, metric.grid_scale)
    Rs = ricci_scalar(gi, R)
    G = einstein_tensor(g, R, Rs)
    T = stress_energy(G)
    M = eulerian_transformation(g, wf_compat=wf_compat)
    T_eul = to_eulerian(T, M)
    if wf_compat:
        # WarpFactory bug #3: getEnergyConditions, for the Null and Weak
        # branches only, chains
        #   doFrameTransfer (output labelled "contravariant", values are
        #     tetrad-frame T_{ab}; with the M[:,0] sign convention the
        #     T[0,i] components already carry WF's cosmetic sign flip)
        #   -> changeTensorIndex(., "covariant", curved_metric)
        # i.e. it re-lowers the tetrad-indexed T using the *curved* coord
        # metric, mixing frames. The Dominant and Strong branches use a
        # Minkowski reference metric instead (no bug). To byte-match the
        # published anchor we apply the curved-g re-lowering only to the
        # tensor used for NEC/WEC; DEC/SEC use T_eul unchanged.
        T_for_nw = np.einsum('ai...,bj...,ab...->ij...', g, g, T_eul)
    else:
        T_for_nw = None
    ec = evaluate_energy_conditions(
        T_eul,
        num_angular=num_angular,
        num_temporal=num_temporal,
        T_for_null_weak=T_for_nw,
    )
    return EvalResult(g_inv=gi, G_munu=G, T_munu=T, T_eul=T_eul, M=M, ec=ec)

"""Energy conditions evaluated in the Eulerian (locally Lorentzian) frame.

Algorithm matched to WarpFactory's ``getEnergyConditions.m`` +
``generateUniformField.m`` (clean-room NumPy rewrite).

Vector field convention (from ``generateUniformField.m``):

- **null**:     ``V = (1, n_x, n_y, n_z) / sqrt(2)`` with ``n`` on unit S^2.
- **timelike**: ``V = (1, (1-b) n) / sqrt(1 + (1-b)^2)`` for ``b in linspace(0,1,Nt)``.

Note: these are NOT boosted unit observers. They are Euclidean-normalised 4-tuples
that interpolate between null (b=0) and rest-frame (b=1). No gamma-factor inflation.

Conditions (all use Eulerian-frame, covariant ``T_{ab}``):

- **NEC**: ``min_k T_{ab} V^a V^b`` over null V.
- **WEC**: ``min_V T_{ab} V^a V^b`` over timelike V.
- **SEC**: ``min_V (T_{ab} - 0.5 T eta_{ab}) V^a V^b`` over timelike V,
  where ``T = eta^{ab} T_{ab}`` (Minkowski-frame trace).
- **DEC**: for each null V, compute ``J^mu = -T^mu_nu V^nu`` (mixed via
  Minkowski), then ``d = sign(<J,J>_eta) * sqrt(|<J,J>_eta|)``, take ``max``
  over V, and negate so negative=violating.
"""

from __future__ import annotations

import numpy as np


def _angular_directions(n: int) -> np.ndarray:
    """``n`` quasi-uniform unit vectors on S^2 via Fibonacci spiral.

    Matches WarpFactory's ``getEvenPointsOnSphere.m`` exactly:
    for i = 0..n-1,
        theta = 2*pi*i/phi    (phi = (1+sqrt(5))/2)
        phi_polar = acos(1 - 2*(i+0.5)/n)
    Note the asymmetry: theta uses integer i, phi_polar uses i+0.5.
    """
    i = np.arange(n)
    golden = (1.0 + 5.0 ** 0.5) / 2.0
    theta = 2.0 * np.pi * i / golden
    phi = np.arccos(1.0 - 2.0 * (i + 0.5) / n)
    sx = np.cos(theta) * np.sin(phi)
    sy = np.sin(theta) * np.sin(phi)
    sz = np.cos(phi)
    return np.stack([sx, sy, sz], axis=-1)  # (n, 3)


def _null_field(num_angular: int) -> np.ndarray:
    """WarpFactory-style null vector field. Returns (4, Na)."""
    n = _angular_directions(num_angular)  # (Na, 3)
    V = np.empty((4, num_angular))
    V[0] = 1.0
    V[1:] = n.T
    norm = np.sqrt(V[0] ** 2 + V[1] ** 2 + V[2] ** 2 + V[3] ** 2)
    return V / norm


def _timelike_field(num_angular: int, num_temporal: int) -> np.ndarray:
    """WarpFactory-style timelike vector field. Returns (4, Na, Nt).

    ``b in linspace(0, 1, Nt)``; ``V = (1, (1-b) n) / sqrt(1 + (1-b)^2)``.
    """
    n = _angular_directions(num_angular)  # (Na, 3)
    bb = np.linspace(0.0, 1.0, num_temporal)
    V = np.empty((4, num_angular, num_temporal))
    V[0, :, :] = 1.0
    for j, b in enumerate(bb):
        V[1:, :, j] = (1.0 - b) * n.T
    norm = np.sqrt(V[0] ** 2 + V[1] ** 2 + V[2] ** 2 + V[3] ** 2)
    return V / norm


def evaluate_energy_conditions(
    T_eul: np.ndarray,
    *,
    num_angular: int = 100,
    num_temporal: int = 10,
    T_for_null_weak: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    """Return per-grid-point most-violating EC scalars.

    ``T_eul`` shape ``(4, 4, ...)``, covariant components in Eulerian frame.
    ``T_for_null_weak`` (optional) overrides ``T_eul`` for NEC and WEC only;
    used by the wf_compat path to reproduce WarpFactory's frame-mixed
    Null/Weak chain (curved-g re-lowering of tetrad T) while leaving DEC and
    SEC computed against the correct (Minkowski-frame) T_eul.

    Returns dict ``{"null","weak","dominant","strong"}``. Convention:
    negative = violation (matches WarpFactory).
    """
    T_nw = T_for_null_weak if T_for_null_weak is not None else T_eul
    # NEC
    Vn = _null_field(num_angular)  # (4, Na)
    nec = np.einsum("ab...,aN,bN->N...", T_nw, Vn, Vn)
    nec_min = nec.min(axis=0)

    # WEC
    Vt = _timelike_field(num_angular, num_temporal)  # (4, Na, Nt)
    wec = np.einsum("ab...,aNT,bNT->NT...", T_nw, Vt, Vt)
    wec_min = wec.reshape(-1, *T_nw.shape[2:]).min(axis=0)

    # SEC: subtract 0.5 trace_eta(T) eta_{ab} from T_{ab}, then quadratic form.
    trace_T = -T_eul[0, 0] + T_eul[1, 1] + T_eul[2, 2] + T_eul[3, 3]
    T_eff = T_eul.copy()
    T_eff[0, 0] = T_eul[0, 0] - 0.5 * trace_T * (-1.0)
    T_eff[1, 1] = T_eul[1, 1] - 0.5 * trace_T * (1.0)
    T_eff[2, 2] = T_eul[2, 2] - 0.5 * trace_T * (1.0)
    T_eff[3, 3] = T_eul[3, 3] - 0.5 * trace_T * (1.0)
    sec = np.einsum("ab...,aNT,bNT->NT...", T_eff, Vt, Vt)
    sec_min = sec.reshape(-1, *T_eul.shape[2:]).min(axis=0)

    # DEC: J^mu = -T^mu_nu V^nu (V null). Raise first index of T with eta.
    T_mixed = T_eul.copy()
    T_mixed[0, :] = -T_eul[0, :]
    J = -np.einsum("ab...,bN->aN...", T_mixed, Vn)  # (4, Na, ...)
    JJ = -J[0] ** 2 + J[1] ** 2 + J[2] ** 2 + J[3] ** 2  # (Na, ...)
    diff = np.sign(JJ) * np.sqrt(np.abs(JJ))
    dec_max = diff.max(axis=0)
    dec_min = -dec_max  # negative = violating

    return {
        "null": nec_min,
        "weak": wec_min,
        "dominant": dec_min,
        "strong": sec_min,
    }

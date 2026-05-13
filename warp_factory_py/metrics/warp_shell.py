"""Comoving warp-shell metric (Fuchs et al. 2024, arXiv:2405.02709).

Builds an interior-Schwarzschild constant-density shell of mass ``m`` between
radii ``R1`` and ``R2``, optionally overlaid with an Alcubierre-style shift
(``vWarp``) localised to the shell wall via a compact sigmoid.

Mirrors WarpFactory's ``metricGet_WarpShellComoving`` (independent NumPy
rewrite). Same conventions as :mod:`warp_factory_py.metrics.alcubierre`:
geometrised internally (``c=1``) so metric components are O(1); SI factor is
restored downstream by :mod:`warp_factory_py.solvers.einstein.stress_energy`.

Profile pipeline (all SI):

1. ``rho(r) = rho_0 [R1 < r < R2]`` (top-hat) with ``rho_0`` set so that
   ``M(R2) = m``.
2. Smooth ``rho`` four times with a moving-average window of length
   ``round(1.79 * smoothFactor)`` (matches MATLAB ``smooth``).
3. ``M(r) = int 4 pi rho(r') r'^2 dr'`` via cumulative trapezoid.
4. ``P(r)`` from the constant-density Schwarzschild interior solution
   (``TOVconstDensity``), then smooth four times with window
   ``smoothFactor``.
5. ``alpha(r)`` from the TOV equation
   ``dalpha/dr = (G M / c^2 + 4 pi G r^3 P / c^4) / (r^2 - 2 G M r / c^2)``
   integrated with cumulative trapezoid; offset fixed by matching
   ``alpha(r_max) = 0.5 ln(1 - 2 G M_total / (r_max c^2))``.
6. ``A(r) = -exp(2 alpha(r))``, ``B(r) = (1 - 2 G M(r) / (r c^2))^{-1}``.
7. Sample ``A``, ``B`` at each Cartesian grid cell via 3rd-order Legendre
   interpolation, project the spherical-symmetric metric to Cartesian via
   :func:`_sph2cart_diag`, and (if ``do_warp``) overlay
   ``g_{tx} = -v * shift(r)`` localised by a compact sigmoid in ``[R1, R2]``.

Geometrised conversion: store ``g_{tt} = -exp(2 alpha)`` (drop the SI ``c^2``)
and use the dimensionless ``v_warp`` directly, so the resulting metric has the
same grid-scale convention as the Alcubierre port.
"""

from __future__ import annotations

import numpy as np

from ..utils.constants import G, c
from .alcubierre import Metric


def _smooth_ma(y: np.ndarray, window: int) -> np.ndarray:
    """Moving-average smoother matching MATLAB ``smooth(y, window)``.

    MATLAB's ``smooth`` with the default ``'moving'`` method uses an averaging
    window of length ``window`` rounded down to the nearest odd integer. End
    effects: the first and last ``(window-1)/2`` points use a shrinking window
    (mean of the first/last ``2k+1`` points for output index ``k``).
    """
    w = max(1, int(window))
    if w % 2 == 0:
        w -= 1
    if w <= 1:
        return y.astype(np.float64, copy=True)
    n = len(y)
    out = np.empty(n, dtype=np.float64)
    half = (w - 1) // 2
    cy = np.cumsum(np.concatenate(([0.0], y.astype(np.float64))))
    for i in range(n):
        if i < half:
            k = i
            out[i] = (cy[2 * k + 1] - cy[0]) / (2 * k + 1)
        elif i >= n - half:
            k = n - 1 - i
            out[i] = (cy[n] - cy[n - (2 * k + 1)]) / (2 * k + 1)
        else:
            out[i] = (cy[i + half + 1] - cy[i - half]) / w
    return out


def _smooth4(y: np.ndarray, window: int) -> np.ndarray:
    """Apply ``_smooth_ma`` four times (matches WF's quadruple-smooth)."""
    out = y
    for _ in range(4):
        out = _smooth_ma(out, window)
    return out


def _tov_const_density(R: float, M_total: float, rho: np.ndarray, r: np.ndarray) -> np.ndarray:
    """Schwarzschild-interior constant-density TOV pressure profile.

    ``P(r) = rho c^2 [(R sqrt(R - r_s) - sqrt(R^3 - r_s r^2)) /
                     (sqrt(R^3 - r_s r^2) - 3 R sqrt(R - r_s))] [r < R]``
    where ``r_s = 2 G M_total / c^2``. Mirrors WF's ``TOVconstDensity.m``.
    """
    rs = 2.0 * G * M_total / c**2
    rootR = np.sqrt(max(R - rs, 0.0))
    inside = R**3 - rs * r**2
    inside = np.where(inside < 0.0, 0.0, inside)
    root_in = np.sqrt(inside)
    num = R * rootR - root_in
    den = root_in - 3.0 * R * rootR
    factor = np.where(den != 0.0, num / den, 0.0)
    P = c**2 * rho * factor * (r < R)
    return P


def _alpha_solver(M: np.ndarray, P: np.ndarray, r: np.ndarray, M_total: float, r_max: float) -> np.ndarray:
    """Trapezoidal-rule TOV ``alpha(r)`` integrator.

    ``dalpha/dr = (G M / c^2 + 4 pi G r^3 P / c^4) / (r^2 - 2 G M r / c^2)``
    with the boundary condition ``alpha(r_max) = 0.5 ln(1 - 2 G M_total /
    (r_max c^2))`` (Schwarzschild exterior). Mirrors WF's
    ``alphaNumericSolver.m``.
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        dalpha_num = G * M / c**2 + 4.0 * np.pi * G * r**3 * P / c**4
        dalpha_den = r**2 - 2.0 * G * M * r / c**2
        dalpha = np.where(dalpha_den != 0.0, dalpha_num / dalpha_den, 0.0)
    dalpha[0] = 0.0
    alpha_temp = _cumtrapz(r, dalpha)
    C = 0.5 * np.log(max(1.0 - 2.0 * G * M_total / (r[-1] * c**2), 1e-300))
    offset = C - alpha_temp[-1]
    return alpha_temp + offset


def _cumtrapz(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """``cumtrapz(x, y)`` matching MATLAB (length-preserving, leading zero)."""
    out = np.empty_like(y, dtype=np.float64)
    out[0] = 0.0
    dx = np.diff(x)
    out[1:] = np.cumsum(0.5 * (y[:-1] + y[1:]) * dx)
    return out


def _compact_sigmoid(r: np.ndarray, R1: float, R2: float, sigma: float, Rbuff: float) -> np.ndarray:
    """Compactly-supported sigmoid that ramps 0 -> 1 across ``(R1, R2)``.

    Matches WF's ``compactSigmoid.m``:
    ``f(r) = |1/(exp(((R2-R1-2 Rbuff)(sigma+2))/2 *
                     (1/(r - R2 + Rbuff) + 1/(r - R1 - Rbuff))) + 1) *
             [R1+Rbuff < r < R2-Rbuff] + [r >= R2-Rbuff] - 1|``
    """
    a = R1 + Rbuff
    b = R2 - Rbuff
    in_band = (r > a) & (r < b)
    safe_arg = np.where(in_band, (r - b) + 0.0, -1.0)
    safe_arg2 = np.where(in_band, (r - a) + 0.0, 1.0)
    coef = ((R2 - R1 - 2.0 * Rbuff) * (sigma + 2.0)) / 2.0
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        expo = coef * (1.0 / safe_arg + 1.0 / safe_arg2)
        denom = np.exp(expo) + 1.0
        sig_band = np.where(in_band, 1.0 / denom, 0.0)
    out = np.abs(sig_band + (r >= b).astype(np.float64) - 1.0)
    return out


def _legendre_interp(arr: np.ndarray, idx: np.ndarray) -> np.ndarray:
    """3rd-order Legendre interpolation at fractional indices ``idx``.

    Mirrors WF's ``legendreRadialInterp.m``. ``arr`` is 1-D, ``idx`` may be
    any shape; values < 1 are clamped to index 0 of ``arr`` (1-based MATLAB).
    """
    n = len(arr)
    x0 = np.floor(idx - 1.0).astype(np.int64)
    x1 = np.floor(idx).astype(np.int64)
    x2 = np.ceil(idx).astype(np.int64)
    x3 = np.ceil(idx + 1.0).astype(np.int64)

    def get(xi):
        return arr[np.clip(xi - 1, 0, n - 1)]  # MATLAB 1-based -> Python 0-based

    y0 = get(x0)
    y1 = get(x1)
    y2 = get(x2)
    y3 = get(x3)
    x0f = x0.astype(np.float64)
    x1f = x1.astype(np.float64)
    x2f = x2.astype(np.float64)
    x3f = x3.astype(np.float64)
    x = idx.astype(np.float64)
    # Lagrange basis on (x0, x1, x2, x3); guard against equal consecutive nodes
    # (occurs when idx is an integer => x1 == x2). The Lagrange formula has
    # those zero factors cancel analytically, so use a small epsilon to avoid
    # 0/0 numerically.
    eps = 1e-12

    def safe_div(num, den):
        return num / np.where(np.abs(den) < eps, np.sign(den) * eps + eps, den)

    L0 = safe_div((x - x1f) * (x - x2f) * (x - x3f), (x0f - x1f) * (x0f - x2f) * (x0f - x3f))
    L1 = safe_div((x - x0f) * (x - x2f) * (x - x3f), (x1f - x0f) * (x1f - x2f) * (x1f - x3f))
    L2 = safe_div((x - x0f) * (x - x1f) * (x - x3f), (x2f - x0f) * (x2f - x1f) * (x2f - x3f))
    L3 = safe_div((x - x0f) * (x - x1f) * (x - x2f), (x3f - x0f) * (x3f - x1f) * (x3f - x2f))
    return y0 * L0 + y1 * L1 + y2 * L2 + y3 * L3


def _sph2cart_diag(theta: np.ndarray, phi: np.ndarray, g11_sph: np.ndarray, g22_sph: np.ndarray):
    """Project diagonal spherical metric (g_tt, g_rr) -> Cartesian g_ij.

    Mirrors WF's ``sph2cartDiag.m``. The spherical line element is

        ds^2 = g11_sph dt^2 + g22_sph dr^2 + r^2 (d theta^2 + sin^2 theta d phi^2),

    with the angular block normalised so that the orthonormal-frame form gives
    g_{ang,ang} = 1 (the WF code sets the non-radial spatial block to delta_ij
    in the limit ``g22_sph = 1``, hence the explicit ``+ sin(phi)^2`` etc.).

    ``theta`` is the polar angle from +z (``acos(z/r)``-like via WF's
    ``atan2(sqrt(x^2+y^2), z)``). ``phi`` is the azimuthal angle
    ``atan2(y, x)``.

    Returns ``(g11, g22, g23, g24, g33, g34, g44)`` in the WF index ordering
    where ``2,3,4 -> x,y,z``.
    """
    cos_phi = np.where(np.abs(np.abs(phi) - np.pi / 2) < 1e-15, 0.0, np.cos(phi))
    cos_theta = np.where(np.abs(np.abs(theta) - np.pi / 2) < 1e-15, 0.0, np.cos(theta))
    sin_phi = np.sin(phi)
    sin_theta = np.sin(theta)
    E = g22_sph

    g11_cart = g11_sph
    g22_cart = E * cos_phi**2 * sin_theta**2 + cos_phi**2 * cos_theta**2 + sin_phi**2
    g33_cart = E * sin_phi**2 * sin_theta**2 + cos_theta**2 * sin_phi**2 + cos_phi**2
    g44_cart = E * cos_theta**2 + sin_theta**2

    g23_cart = E * cos_phi * sin_phi * sin_theta**2 + cos_phi * cos_theta**2 * sin_phi - cos_phi * sin_phi
    g24_cart = E * cos_phi * cos_theta * sin_theta - cos_phi * cos_theta * sin_theta
    g34_cart = E * cos_theta * sin_phi * sin_theta - cos_theta * sin_phi * sin_theta

    return g11_cart, g22_cart, g23_cart, g24_cart, g33_cart, g34_cart, g44_cart


def metric_warp_shell_comoving(
    grid_size: tuple[int, int, int, int],
    world_center: tuple[float, float, float, float],
    *,
    m: float,
    R1: float,
    R2: float,
    Rbuff: float = 0.0,
    sigma: float = 0.0,
    smooth_factor: float = 1.0,
    v_warp: float = 0.0,
    do_warp: bool = False,
    grid_scale: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
    r_sample_res: int = 100_000,
) -> tuple[Metric, dict]:
    """Build the comoving warp-shell metric.

    Parameters mirror WF's ``metricGet_WarpShellComoving``:

    - ``m`` : total shell mass [kg].
    - ``R1``, ``R2`` : inner / outer shell radii [m].
    - ``Rbuff`` : buffer [m] inside which the shift is held constant.
    - ``sigma`` : shift-sigmoid sharpness (dimensionless).
    - ``smooth_factor`` : window length for the four MATLAB ``smooth`` passes.
    - ``v_warp`` : warp speed in factors of ``c``.
    - ``do_warp`` : if True, overlay an Alcubierre shift ``g_{tx} = -v shift(r)``.
    - ``grid_scale`` : ``(dt, dx, dy, dz)`` cell spacing in metres
      (``dt`` is geometrised: ``c * dt_seconds``).

    Returns ``(metric, params)`` where ``params`` carries the radial profiles
    (``r``, ``rho``, ``rho_smooth``, ``P``, ``P_smooth``, ``M``, ``alpha``,
    ``A``, ``B``, ``shift``) for diagnostics.
    """
    Nt, Nx, Ny, Nz = grid_size
    dt, dx, dy, dz = grid_scale
    t0, x0, y0, z0 = world_center
    if Nt != 1:
        raise ValueError("warp-shell port currently supports static (Nt=1) grids only")

    # World extent and radial sample grid
    world_size = np.sqrt(
        (Nx * dx - x0) ** 2 + (Ny * dy - y0) ** 2 + (Nz * dz - z0) ** 2
    )
    rsample = np.linspace(0.0, world_size * 1.2, r_sample_res)

    # 1. Top-hat density
    rho = np.zeros_like(rsample)
    rho_0 = m / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))
    rho[(rsample > R1) & (rsample < R2)] = rho_0

    # Pre-smooth M (WF computes M *before* smoothing then overwrites it after
    # smoothing rho). Reproduce exactly.
    _M = _cumtrapz(rsample, 4.0 * np.pi * rho * rsample**2)

    # 2. Pressure from un-smoothed rho (WF computes P from un-smoothed rho but
    # uses M_total = _M[-1]).
    P = _tov_const_density(R2, _M[-1], rho, rsample)

    # 3. Smooth rho (4 passes, window = round(1.79 * smoothFactor))
    rho_window = max(1, int(round(1.79 * smooth_factor)))
    rho_smooth = _smooth4(rho, rho_window)

    # 4. Smooth P (4 passes, window = smoothFactor)
    P_smooth = _smooth4(P, max(1, int(round(smooth_factor))))

    # 5. Recompute M from smoothed rho (WF behavior; ensures M(0) = 0 and
    # monotone-rising). Clip negatives to the running max.
    M = _cumtrapz(rsample, 4.0 * np.pi * rho_smooth * rsample**2)
    M_max = np.maximum.accumulate(np.maximum(M, 0.0))
    M = np.where(M < 0.0, M_max, M)

    # 6. alpha(r), A(r), B(r)
    alpha = _alpha_solver(M, P_smooth, rsample, M[-1], rsample[-1])
    A = -np.exp(2.0 * alpha)
    with np.errstate(divide="ignore", invalid="ignore"):
        B = 1.0 / (1.0 - 2.0 * G * M / (rsample * c**2))
    B[0] = 1.0

    # Shift profile (compact sigmoid + 2 smoothing passes per WF)
    shift_radial = _compact_sigmoid(rsample, R1, R2, sigma, Rbuff)
    shift_radial = _smooth_ma(_smooth_ma(shift_radial, max(1, int(round(smooth_factor)))),
                              max(1, int(round(smooth_factor))))

    # 7. Sample onto Cartesian grid
    i_arr = (np.arange(Nx) + 1).astype(np.float64)
    j_arr = (np.arange(Ny) + 1).astype(np.float64)
    k_arr = (np.arange(Nz) + 1).astype(np.float64)
    X = i_arr[:, None, None] * dx - x0
    Y = j_arr[None, :, None] * dy - y0
    Z = k_arr[None, None, :] * dz - z0
    eps = 0.0
    r_grid = np.sqrt(X**2 + Y**2 + Z**2) + eps
    theta_grid = np.arctan2(np.sqrt(X**2 + Y**2), Z)
    phi_grid = np.arctan2(Y, X)

    # Fractional index into rsample (matches WF's "snap to lower then add
    # linear-fraction" idiom). Use searchsorted for vectorised lookup.
    idx_low = np.searchsorted(rsample, r_grid.ravel(), side="right") - 1
    idx_low = np.clip(idx_low, 0, len(rsample) - 2)
    r_low = rsample[idx_low]
    r_high = rsample[idx_low + 1]
    frac = (r_grid.ravel() - r_low) / (r_high - r_low)
    # WF's minIdx is 1-based; we keep 1-based here for _legendre_interp.
    idx_frac = (idx_low + 1).astype(np.float64) + frac
    idx_frac = idx_frac.reshape(r_grid.shape)

    A_grid = _legendre_interp(A, idx_frac)
    B_grid = _legendre_interp(B, idx_frac)
    shift_grid = _legendre_interp(shift_radial, idx_frac)

    # WF stores ``A = -exp(2 alpha)`` directly as g_tt; ``alpha`` is
    # dimensionless (the SI ``c^2`` is restored downstream by
    # :func:`solvers.einstein.stress_energy`). This matches the geometrised
    # convention of :mod:`warp_factory_py.metrics.alcubierre`.
    g_tt_geo = A_grid

    g11, g22, g23, g24, g33, g34, g44 = _sph2cart_diag(theta_grid, phi_grid, g_tt_geo, B_grid)

    # Assemble (4,4,Nt=1,Nx,Ny,Nz)
    g = np.zeros((4, 4, Nt, Nx, Ny, Nz), dtype=np.float64)
    g[0, 0, 0] = g11
    g[1, 1, 0] = g22
    g[2, 2, 0] = g33
    g[3, 3, 0] = g44
    g[1, 2, 0] = g23
    g[2, 1, 0] = g23
    g[1, 3, 0] = g24
    g[3, 1, 0] = g24
    g[2, 3, 0] = g34
    g[3, 2, 0] = g34

    if do_warp:
        # WF: g_{tx} <- g_{tx} - g_{tx} * shift - shift * v_warp
        # With initial g_tx = 0 this simplifies to -shift * v_warp.
        # In our geometrised convention v_warp is dimensionless (v/c), matching
        # the alcubierre.py port.
        g_tx_new = -g[0, 1, 0] * shift_grid - shift_grid * v_warp
        g[0, 1, 0] = g[1, 0, 0] = g_tx_new

    # Coordinate arrays (cell-centred, 1-based to match alcubierre.py)
    t = (np.arange(Nt) + 1) * dt
    x = (np.arange(Nx) + 1) * dx
    y = (np.arange(Ny) + 1) * dy
    z = (np.arange(Nz) + 1) * dz

    metric = Metric(
        g=g,
        coords=(t, x, y, z),
        grid_scale=grid_scale,
        name="ComovingWarpShell",
    )
    params = dict(
        r=rsample,
        rho=rho,
        rho_smooth=rho_smooth,
        P=P,
        P_smooth=P_smooth,
        M=M,
        alpha=alpha,
        A=A,
        B=B,
        shift=shift_radial,
    )
    return metric, params

"""Alcubierre metric.

Builds the standard Alcubierre warp-bubble metric on a (t, x, y, z) grid in SI
units.

Line element (with c restored, ``v_s = v * c`` in m/s):

.. math::

   ds^2 = -c^2 dt^2 + (dx - v_s f(r) dt)^2 + dy^2 + dz^2

where the shape function is

.. math::

   f(r) = \\frac{\\tanh(\\sigma(r + R)) - \\tanh(\\sigma(r - R))}
                {2 \\tanh(\\sigma R)}

and ``r = sqrt((x - x_s(t))^2 + y^2 + z^2)``, ``x_s(t) = v_s * t``.

Mirrors WarpFactory's ``metricGet_Alcubierre`` (independent NumPy rewrite).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


# This module works in geometrized units (c = 1) internally to keep metric
# components O(1) and avoid the catastrophic cancellation that arises when an
# FD stencil divides g_tt ~ c^2 ~ 1e17 by dt ~ 1e-12 in SI units. Coordinates
# (t, x, y, z) are all in METRES (the t-axis is really c*t in geometrised
# units), and ``v`` is dimensionless (v/c). The factor of c is restored only
# at the SI-conversion step in ``solvers.einstein.stress_energy``.


def shape_function_alcubierre(r: np.ndarray, R: float, sigma: float) -> np.ndarray:
    """Alcubierre top-hat shape function ``f(r)``.

    ``f(0) = 1`` (interior), ``f(r) -> 0`` for ``r >> R`` (exterior),
    width of the wall set by ``1 / sigma``.
    """
    num = np.tanh(sigma * (r + R)) - np.tanh(sigma * (r - R))
    den = 2.0 * np.tanh(sigma * R)
    return num / den


@dataclass
class Metric:
    """4D Lorentzian metric on a regular (t, x, y, z) grid.

    ``g`` has shape ``(4, 4, Nt, Nx, Ny, Nz)``. ``coords`` is a tuple of four
    1-D coordinate arrays. ``grid_scale`` is the per-axis spacing
    ``(dt, dx, dy, dz)`` in SI units (s, m, m, m). ``signature`` is fixed at
    ``(-, +, +, +)``.
    """

    g: np.ndarray
    coords: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
    grid_scale: tuple[float, float, float, float]
    name: str = ""


def metric_alcubierre(
    grid_size: tuple[int, int, int, int],
    world_center: tuple[float, float, float, float],
    v: float,
    R: float,
    sigma: float,
    grid_scale: tuple[float, float, float, float],
) -> Metric:
    """Build an Alcubierre metric on a (t, x, y, z) grid.

    Parameters
    ----------
    grid_size : (Nt, Nx, Ny, Nz)
        Number of cells per axis. ``Nt = 1`` is allowed (snapshot).
    world_center : (t0, x0, y0, z0)
        Bubble centre in physical units (s, m, m, m). The bubble travels along
        +x with constant velocity ``v_s = v * c``; ``world_center`` gives the
        bubble centre at index ``(0, ?, Ny//2, Nz//2)`` (i.e. centred at t0).
    v : float
        Warp velocity in units of ``c``.
    R : float
        Bubble radius in metres.
    sigma : float
        Wall sharpness in 1/m.
    grid_scale : (dt, dx, dy, dz)
        Cell spacing in metres. The first entry is the geometrised time-step
        ``c * dt_seconds``.
    """
    Nt, Nx, Ny, Nz = grid_size
    dt, dx, dy, dz = grid_scale
    t0, x0, y0, z0 = world_center
    v_s = v  # dimensionless in geometrised units (v/c)

    # Coordinate arrays (cell-centred, indexed from 1 for parity with MATLAB
    # but converted to 0-indexed here).
    t = (np.arange(Nt) + 1) * dt
    x = (np.arange(Nx) + 1) * dx
    y = (np.arange(Ny) + 1) * dy
    z = (np.arange(Nz) + 1) * dz

    # Bubble x-position at each time slice
    xs_t = x0 + v_s * (t - t0)  # shape (Nt,)

    # Build r grid: shape (Nt, Nx, Ny, Nz)
    T_, X_, Y_, Z_ = np.meshgrid(t, x, y, z, indexing="ij")
    XS = xs_t[:, None, None, None]
    r = np.sqrt((X_ - XS) ** 2 + (Y_ - y0) ** 2 + (Z_ - z0) ** 2)
    f = shape_function_alcubierre(r, R, sigma)

    g = np.zeros((4, 4, Nt, Nx, Ny, Nz), dtype=np.float64)
    # Geometrised c=1: ds^2 = -(1 - v^2 f^2) dt^2 - 2 v f dt dx + dx^2 + dy^2 + dz^2
    g[0, 0] = -(1.0 - (v_s * f) ** 2)
    g[0, 1] = -v_s * f
    g[1, 0] = -v_s * f
    g[1, 1] = 1.0
    g[2, 2] = 1.0
    g[3, 3] = 1.0

    return Metric(g=g, coords=(t, x, y, z), grid_scale=grid_scale,
                  name=f"Alcubierre(v={v}c, R={R}, sigma={sigma})")

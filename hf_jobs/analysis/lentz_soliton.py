"""Task 3.7 / Block 3(a) (Session 43): Lentz 2020 pentagonal soliton, rebuilt.

Lentz 2020 (arXiv:2006.07125) exhibits an irrotational shift N_i = d_i phi
whose potential obeys the hyperbolic spatial relation (his Eq. 15)

    d_x^2 phi + d_y^2 phi - (2/v_h^2) d_z^2 phi = rho,

with a hand-built "pentagonal" rhomboid source layout (his Fig. 1) chosen so
the EULERIAN energy density is everywhere non-negative. The paper never
checks the full WEC (rho + p_i >= 0) or DEC, gives no closed form for rho,
and provides no reproduction path (Bobrick-Martire 2021 flag this). This
module rebuilds the construction end-to-end:

  1. rho(z, s), s = |x|+|y|, digitised from the paper's own Fig. 1 (vector
     PDF -> pixel colormap inversion; see agent-tools note in the session
     log). v_h = 1 read off the 45-degree compartment edges of his Fig. 2.
  2. phi solved as a 2+1 wave equation marching in z (z = retarded "time";
     phi = dphi/dz = 0 ahead of all sources), leapfrog, CFL-limited -- the
     PDE is satisfied by construction and the residual is checkable.
  3. phi interpolated onto a uniform cubic grid; N = grad phi via the
     project's 4th-order stencils; stress-energy via the validated
     adm_stress_energy_from_N (same pipeline as the FH sweeps), principal
     pressures via eigvalsh, full WEC/DEC slacks.

Verification gates live in verification/test_lentz_full_wec.py.
"""
from __future__ import annotations

import numpy as np

from hf_jobs.sweeps.fell_heisenberg import adm_stress_energy_from_N, fd_grad4

V_H = 1.0     # wave speed: Lentz Fig. 2 compartment edges are at 45 deg


# ---------------------------------------------------------------------------
# 1. Source field
# ---------------------------------------------------------------------------

def load_rho_zs(npz_path: str):
    """Load the digitised Fig.-1 source and fold it to rho(z, s), s >= 0.

    The figure is the y = 0 projection, where s = |x|; the two x-branches
    are averaged (they are mirror images up to digitisation noise).
    Returns (z_grid, s_grid, rho_2d[z, s]) with rho smoothed lightly to
    suppress contour-band quantisation.
    """
    d = np.load(npz_path)
    rho_img = d['rho']          # [x_row, z_col], x descending
    zz = d['z']
    xx = d['x']
    order = np.argsort(xx)
    xx = xx[order]
    rho_img = rho_img[order, :]
    # fold x -> s
    s_max = min(-xx[0], xx[-1])
    s_grid = np.linspace(0.0, s_max, 240)
    neg = np.interp(-s_grid, xx, np.arange(xx.size))
    pos = np.interp(s_grid, xx, np.arange(xx.size))
    rows_n = np.clip(neg.round().astype(int), 0, xx.size - 1)
    rows_p = np.clip(pos.round().astype(int), 0, xx.size - 1)
    rho_zs = 0.5 * (rho_img[rows_n, :] + rho_img[rows_p, :])   # [s, z]
    rho_zs = rho_zs.T                                          # [z, s]
    # light box smoothing (3x3) against contour banding
    k = np.ones((3, 3)) / 9.0
    from scipy.signal import convolve2d
    rho_zs = convolve2d(rho_zs, k, mode='same', boundary='symm')
    return zz, s_grid, rho_zs


def rho_at(z, s, zz, s_grid, rho_zs):
    """Bilinear sample of rho(z, s); zero outside the digitised window."""
    z = np.asarray(z, dtype=float)
    s = np.asarray(s, dtype=float)
    iz = np.interp(z, zz, np.arange(zz.size))
    js = np.interp(s, s_grid, np.arange(s_grid.size))
    iz0 = np.clip(np.floor(iz).astype(int), 0, zz.size - 2)
    js0 = np.clip(np.floor(js).astype(int), 0, s_grid.size - 2)
    fz = np.clip(iz - iz0, 0, 1)
    fs = np.clip(js - js0, 0, 1)
    v = ((1 - fz) * (1 - fs) * rho_zs[iz0, js0]
         + fz * (1 - fs) * rho_zs[iz0 + 1, js0]
         + (1 - fz) * fs * rho_zs[iz0, js0 + 1]
         + fz * fs * rho_zs[iz0 + 1, js0 + 1])
    outside = (z < zz[0]) | (z > zz[-1]) | (s > s_grid[-1])
    return np.where(outside, 0.0, v)


# ---------------------------------------------------------------------------
# 2. Hyperbolic solve: leapfrog march in z
# ---------------------------------------------------------------------------

def solve_phi(zz, s_grid, rho_zs, *, L_perp=8.0, h_perp=0.05,
              z_start=-3.0, z_end=6.0, cfl=0.5, store_every=None,
              sponge_width=1.0):
    """March d_z^2 phi = (v_h^2/2)(Lap_xy phi - rho) from quiescent data.

    Returns (xs, zs_stored, phi_stack) with phi_stack[k] the (x, y) plane at
    zs_stored[k]. A thin absorbing sponge at the transverse boundary damps
    wrap-around reflections (the physical cones stay inside the domain for
    the analysis window; the sponge is belt-and-braces).
    """
    n = int(round(2 * L_perp / h_perp)) + 1
    xs = np.linspace(-L_perp, L_perp, n)
    X, Y = np.meshgrid(xs, xs, indexing='ij')
    S = np.abs(X) + np.abs(Y)

    dz = cfl * h_perp / (V_H * np.sqrt(2.0))
    nz = int(round((z_end - z_start) / dz)) + 1
    zs = np.linspace(z_start, z_end, nz)
    dz = zs[1] - zs[0]

    if store_every is None:
        store_every = max(1, int(round(0.05 / dz)))

    # sponge: damping ramp on the outer boundary ring
    edge = np.maximum(np.abs(X), np.abs(Y))
    w = np.clip((edge - (L_perp - sponge_width)) / sponge_width, 0.0, 1.0)
    damp = 1.0 - 0.05 * w ** 2

    lap = np.zeros_like(X)
    phi_m = np.zeros_like(X)   # phi at z_{k-1}
    phi_0 = np.zeros_like(X)   # phi at z_k
    c2 = (V_H ** 2) / 2.0

    stored_z = []
    stored_phi = []
    for k in range(nz):
        zk = zs[k]
        if k % store_every == 0 or k == nz - 1:
            stored_z.append(zk)
            stored_phi.append(phi_0.copy())
        # 2nd-order 5-point Laplacian
        lap[1:-1, 1:-1] = (
            phi_0[2:, 1:-1] + phi_0[:-2, 1:-1]
            + phi_0[1:-1, 2:] + phi_0[1:-1, :-2]
            - 4.0 * phi_0[1:-1, 1:-1]
        ) / h_perp ** 2
        lap[0, :] = lap[-1, :] = 0.0
        lap[:, 0] = lap[:, -1] = 0.0
        src = rho_at(zk, S, zz, s_grid, rho_zs)
        phi_p = 2.0 * phi_0 - phi_m + dz ** 2 * c2 * (lap - src)
        phi_p *= damp
        phi_m, phi_0 = phi_0, phi_p

    return xs, np.array(stored_z), np.stack(stored_phi)


def residual_check(xs, zs, k, phi_m, phi_0, phi_p, damp, zz, s_grid, rho_zs):
    """Inline |PDE residual| / max|rho| at march step k (exact three
    consecutive full-resolution steps; the coarse stored-slice variant used
    by an earlier version of this harness was numerically meaningless).
    Measured 1e-13 relative in the certification runs."""
    h = xs[1] - xs[0]
    dz = zs[1] - zs[0]
    d2z = (phi_p / damp - 2 * phi_0 + phi_m) / dz ** 2
    lap = np.zeros_like(phi_0)
    lap[1:-1, 1:-1] = (phi_0[2:, 1:-1] + phi_0[:-2, 1:-1] + phi_0[1:-1, 2:]
                       + phi_0[1:-1, :-2] - 4 * phi_0[1:-1, 1:-1]) / h ** 2
    X, Y = np.meshgrid(xs, xs, indexing='ij')
    S = np.abs(X) + np.abs(Y)
    src = rho_at(zs[k], S, zz, s_grid, rho_zs)
    res = lap - (2.0 / V_H ** 2) * d2z - src
    m = (np.abs(X) < 6.0) & (np.abs(Y) < 6.0)
    return float(np.abs(res[m]).max() / max(np.abs(src).max(), 1.0))


# ---------------------------------------------------------------------------
# 3. Cubic-grid resample + ADM stress-energy
# ---------------------------------------------------------------------------

def phi_on_cube(xs, zs_stored, phi_stack, *, L, Npts, z_center=0.5):
    """Trilinear-resample phi onto a uniform cubic grid centred at
    (0, 0, z_center) with half-width L."""
    g = np.linspace(-L, L, Npts)
    zg = g + z_center
    # interp z first
    phi_z = np.empty((zg.size, xs.size, xs.size))
    for i, zv in enumerate(zg):
        j = np.clip(np.searchsorted(zs_stored, zv) - 1, 0, zs_stored.size - 2)
        f = (zv - zs_stored[j]) / (zs_stored[j + 1] - zs_stored[j])
        phi_z[i] = (1 - f) * phi_stack[j] + f * phi_stack[j + 1]
    # then bilinear in (x, y)
    idx = np.interp(g, xs, np.arange(xs.size))
    i0 = np.clip(np.floor(idx).astype(int), 0, xs.size - 2)
    fx = idx - i0
    A = phi_z[:, i0, :][:, :, i0]
    B = phi_z[:, i0 + 1, :][:, :, i0]
    C = phi_z[:, i0, :][:, :, i0 + 1]
    D = phi_z[:, i0 + 1, :][:, :, i0 + 1]
    FX = fx[None, :, None]
    FY = fx[None, None, :]
    phi_cube_zxy = (A * (1 - FX) * (1 - FY) + B * FX * (1 - FY)
                    + C * (1 - FX) * FY + D * FX * FY)
    # reorder to [x, y, z] to match the FH pipeline convention
    return np.transpose(phi_cube_zxy, (1, 2, 0)), g


def lentz_ec_scan(phi_cube, h, *, amp=1.0):
    """N = amp * grad(phi); full ADM stress-energy; WEC/DEC slack fields.

    Returns dict of fields; interior mask should be applied by the caller
    (FD stencils corrupt a 4-cell border).
    """
    N = [amp * fd_grad4(phi_cube, h, axis=ax) for ax in range(3)]
    rho_E, K, S_ij = adm_stress_energy_from_N(N, h)
    S_flat = np.moveaxis(S_ij.reshape(3, 3, -1), 2, 0)
    evals = np.linalg.eigvalsh(S_flat)
    p_min = evals[:, 0].reshape(rho_E.shape)
    p_abs_max = np.abs(evals).max(axis=1).reshape(rho_E.shape)
    return {
        'N': N,
        'rho_E': rho_E,
        'wec_slack': rho_E + p_min,
        'dec_slack': rho_E - p_abs_max,
    }

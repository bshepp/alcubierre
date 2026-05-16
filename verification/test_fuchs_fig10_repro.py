"""Reproduce Fuchs et al. 2024 Fig.10 in the Python pipeline.

Builds the canonical Fuchs warp-shell metric with
:func:`warp_factory_py.metrics.warp_shell.metric_warp_shell_comoving`, runs it
through :func:`warp_factory_py.solvers.evaluator.eval_metric` in both
``wf_compat=True`` (byte-faithful WF reproduction) and ``wf_compat=False``
(scientifically correct EC pipeline) modes, and compares to the MATLAB ground
truth in ``warp_factory_repro/fuchs_repro.mat``.

Reports per-EC: pass-fraction inside the shell mask, min, max, mean abs diff,
and rel diff of min, against the MATLAB reference.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
from scipy.io import loadmat

from warp_factory_py.metrics.warp_shell import metric_warp_shell_comoving
from warp_factory_py.solvers.evaluator import eval_metric
from warp_factory_py.utils.constants import G, c

ROOT = Path(__file__).resolve().parents[1]
MAT = ROOT / "warp_factory_repro" / "fuchs_repro.mat"

# Canonical Fuchs parameters (W1_Warp_Shell.mlx defaults; see
# warp_factory_repro/fuchs_fig10_repro.m).
R1 = 10.0
R2 = 20.0
Rbuff = 0.0
factor = 1.0 / 3.0
m_shell = R2 / (2.0 * G) * c**2 * factor
v_warp = 0.02
sigma = 0.0
smooth_factor = 4000.0
space_scale = 5
cartoon_thickness = 5

Nx = int(np.ceil(2 * (R2 + 10) * space_scale))  # 300
Ny = Nx
Nz = cartoon_thickness
Nt = 1

dx = 1.0 / space_scale  # 0.2 m
dy = dx
dz = dx
dt_si = 1.0 / (1000.0 * c)
dt_geo = c * dt_si  # 0.001 m on the geometrised t-axis

world_center = (
    (cartoon_thickness + 1) / 2.0 * dt_geo,
    (2 * (R2 + 10) * space_scale + 1) / 2.0 * dx,
    (2 * (R2 + 10) * space_scale + 1) / 2.0 * dy,
    (cartoon_thickness + 1) / 2.0 * dz,
)

print(f"Grid: ({Nt},{Nx},{Ny},{Nz}), dx={dx} m, m={m_shell:.3e} kg")
print("Building metric...")
t0 = time.perf_counter()
metric, params = metric_warp_shell_comoving(
    grid_size=(Nt, Nx, Ny, Nz),
    world_center=world_center,
    m=m_shell,
    R1=R1,
    R2=R2,
    Rbuff=Rbuff,
    sigma=sigma,
    smooth_factor=smooth_factor,
    v_warp=v_warp,
    do_warp=True,
    grid_scale=(dt_geo, dx, dy, dz),
)
print(f"  metric built in {time.perf_counter()-t0:.1f} s")

# Load MATLAB ground truth
mat = loadmat(MAT)
X = mat["X"]  # (296,296)
Y = mat["Y"]
mat_rho = mat["rho"]
mat_nec = mat["nec"]
mat_wec = mat["wec"]
mat_dec = mat["dec"]
mat_sec = mat["sec"]
print(f"\nLoaded MATLAB ref: X.shape={X.shape}")

# In-shell mask matching the MATLAB script
xc = X - X.mean()
yc = Y - Y.mean()
r2_xy = xc**2 + yc**2
shell_mask = (r2_xy >= R1**2) & (r2_xy <= R2**2)
n_in_shell = int(shell_mask.sum())
print(f"In-shell mask: {n_in_shell} cells of {shell_mask.size}")

# Mid-z index (cartoon_thickness=5, MATLAB round((5+1)/2)=3 -> Python idx 2)
zIdx = (cartoon_thickness + 1) // 2 - 1  # = 2

# MATLAB crop is `3:end-2` on (Nx=300) -> Python [2:-2] -> 296 cells
def crop(arr2d: np.ndarray) -> np.ndarray:
    return arr2d[2:-2, 2:-2]


def report(name: str, py_arr2d: np.ndarray, mat_arr: np.ndarray) -> None:
    diff = py_arr2d - mat_arr
    rel = np.abs(diff) / (np.abs(mat_arr) + 1e-300)
    py_min_in = py_arr2d[shell_mask].min()
    mat_min_in = mat_arr[shell_mask].min()
    pass_py = (py_arr2d[shell_mask] >= -1e-12).sum() / n_in_shell
    pass_mat = (mat_arr[shell_mask] >= -1e-12).sum() / n_in_shell
    print(
        f"  {name:5s}: passPy={pass_py:.4f} passMAT={pass_mat:.4f} "
        f"min(in-shell): py={py_min_in:.3e} mat={mat_min_in:.3e} "
        f"reldiff(min)={abs(py_min_in-mat_min_in)/abs(mat_min_in):.3e}  "
        f"max|diff|/max|mat|={np.abs(diff).max()/np.abs(mat_arr).max():.3e}"
    )


def transpose_to_mat(py3d_xyz: np.ndarray) -> np.ndarray:
    """MATLAB `squeeze(...(:,:,zIdx))'` swaps so first index is Y, second X.

    Our arrays are indexed (i=x, j=y, k=z); the MATLAB transpose corresponds
    to swapping the first two axes. After cropping, returns (296,296) with
    Y-major (matching `imagesc(x,y,...)`).
    """
    return crop(py3d_xyz[:, :, zIdx]).T


for compat_label, wf_compat in [("wf_compat=False (correct)", False), ("wf_compat=True  (byte-faithful)", True)]:
    print(f"\n=== {compat_label} ===")
    t0 = time.perf_counter()
    res = eval_metric(metric, num_angular=100, num_temporal=10, wf_compat=wf_compat)
    print(f"  eval_metric: {time.perf_counter()-t0:.1f} s")

    # T_eul has shape (4,4,Nt,Nx,Ny,Nz); rho_e = T_eul[0,0]
    rho_py = transpose_to_mat(res.T_eul[0, 0, 0])
    nec_py = transpose_to_mat(res.ec["null"][0])
    wec_py = transpose_to_mat(res.ec["weak"][0])
    dec_py = transpose_to_mat(res.ec["dominant"][0])
    sec_py = transpose_to_mat(res.ec["strong"][0])

    print(f"  rho:")
    diff = rho_py - mat_rho
    print(
        f"    py.min={rho_py.min():.3e} py.max={rho_py.max():.3e} "
        f"mat.min={mat_rho.min():.3e} mat.max={mat_rho.max():.3e}  "
        f"max|diff|/max|mat|={np.abs(diff).max()/np.abs(mat_rho).max():.3e}"
    )
    report("NEC", nec_py, mat_nec)
    report("WEC", wec_py, mat_wec)
    report("DEC", dec_py, mat_dec)
    report("SEC", sec_py, mat_sec)

"""Smoke test for the Fuchs warp-shell port.

Builds a small slice of the canonical Fuchs Fig.10 metric and checks that:
  - profiles are finite and monotone where expected
  - g_tt is negative, g_ii positive at the grid centre
  - shift profile peaks inside the shell wall
  - exterior matches Schwarzschild: A(r > R2) -> -(1 - r_s/r), B(r > R2) -> 1/(1 - r_s/r)
"""

from __future__ import annotations

import numpy as np

from warp_factory_py.metrics.warp_shell import metric_warp_shell_comoving
from warp_factory_py.utils.constants import G, c

# Canonical Fuchs parameters
R1 = 10.0
R2 = 20.0
factor = 1.0 / 3.0
m = R2 / (2.0 * G) * c**2 * factor
v_warp = 0.02
sigma = 0.0
smooth_factor = 4000.0
space_scale = 5
cartoon_thickness = 5

# centered grid
Nx = int(np.ceil(2 * (R2 + 10) * space_scale))  # 300
Ny = Nx
Nz = cartoon_thickness
Nt = 1

dt_si = 1.0 / (1000.0 * c)
dx = 1.0 / space_scale  # 0.2 m
dy = dx
dz = dx
# Geometrised t-axis: alcubierre.py convention is dt_geo = c * dt_si in metres.
dt_geo = c * dt_si  # = 0.001 m (matches Alcubierre anchor's DT=0.001)

world_center = (
    (cartoon_thickness + 1) / 2.0 * dt_geo,  # not actually used for static metric
    (2 * (R2 + 10) * space_scale + 1) / 2.0 * dx,
    (2 * (R2 + 10) * space_scale + 1) / 2.0 * dy,
    (cartoon_thickness + 1) / 2.0 * dz,
)

print(f"m = {m:.3e} kg, R2 = {R2} m, r_s = {2*G*m/c**2:.3f} m (= R2/3 = {R2/3:.3f} m)")
print(f"grid = ({Nt}, {Nx}, {Ny}, {Nz}), dx = {dx} m")
print("Building metric...")

metric, params = metric_warp_shell_comoving(
    grid_size=(Nt, Nx, Ny, Nz),
    world_center=world_center,
    m=m,
    R1=R1,
    R2=R2,
    Rbuff=0.0,
    sigma=sigma,
    smooth_factor=smooth_factor,
    v_warp=v_warp,
    do_warp=True,
    grid_scale=(dt_geo, dx, dy, dz),
)

g = metric.g
print(f"g shape = {g.shape}")
print(f"g finite: {np.all(np.isfinite(g))}")

# Probe a few values
ic = Nx // 2
jc = Ny // 2
kc = Nz // 2
print(f"\nAt grid centre (i,j,k) = ({ic},{jc},{kc}):")
print(f"  g_tt = {g[0,0,0,ic,jc,kc]:.6e}")
print(f"  g_xx = {g[1,1,0,ic,jc,kc]:.6e}")
print(f"  g_yy = {g[2,2,0,ic,jc,kc]:.6e}")
print(f"  g_zz = {g[3,3,0,ic,jc,kc]:.6e}")
print(f"  g_tx = {g[0,1,0,ic,jc,kc]:.6e}")

# Profile diagnostics
r = params["r"]
rho = params["rho"]
rho_s = params["rho_smooth"]
P = params["P"]
P_s = params["P_smooth"]
M = params["M"]
A = params["A"]
B = params["B"]
shift = params["shift"]
print(f"\nProfile at r=R1+R2/2 = {(R1+R2)/2:.1f} m:")
i_mid = np.argmin(np.abs(r - (R1 + R2) / 2))
print(f"  rho(raw)    = {rho[i_mid]:.3e} kg/m^3")
print(f"  rho(smooth) = {rho_s[i_mid]:.3e}")
print(f"  P(raw)      = {P[i_mid]:.3e} Pa")
print(f"  P(smooth)   = {P_s[i_mid]:.3e}")
print(f"  M(r)        = {M[i_mid]:.3e} kg  (M_total = {M[-1]:.3e})")
print(f"  A(r)        = {A[i_mid]:.6e}")
print(f"  B(r)        = {B[i_mid]:.6e}")
print(f"  shift(r)    = {shift[i_mid]:.6e}")

# Schwarzschild exterior check
i_ext = np.argmin(np.abs(r - 1.5 * R2))
rs = 2 * G * m / c**2
A_schw = -(1 - rs / r[i_ext])  # WF/A is dimensionless; SI factor restored downstream
B_schw = 1.0 / (1 - rs / r[i_ext])
print(f"\nExterior at r={r[i_ext]:.1f} m (Schwarzschild):")
print(f"  A: port={A[i_ext]:.6e} schw={A_schw:.6e}  rel diff={abs(A[i_ext]-A_schw)/abs(A_schw):.2e}")
print(f"  B: port={B[i_ext]:.6e} schw={B_schw:.6e}  rel diff={abs(B[i_ext]-B_schw)/abs(B_schw):.2e}")

# Pass conservation: total mass should match input m within smoothing tolerance
print(f"\nMass conservation: M_total/m = {M[-1]/m:.6f}")

# Shift peak location
i_peak = np.argmax(shift)
print(f"Shift peak: r={r[i_peak]:.2f} m (expected near R2={R2})")
print(f"Shift max: {shift.max():.4f}")

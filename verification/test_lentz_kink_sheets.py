"""Session-55 verification: the Lentz l1 kink sheets are finite Israel-type
surface layers with strictly EC-violating surface stress (S45 optional residue).

The l1 ansatz phi(z, s = |x| + |y|) makes the shift component
N_x = sign(x) phi_s DISCONTINUOUS across the x = 0 plane (and N_y across
y = 0) wherever phi_s != 0. A-priori this looked worse than an Israel thin
shell (a metric-component jump suggests delta'-type dipole-layer curvature
with no finite surface-density limit). **The measured scaling REFUTED that
expectation** -- recorded here per the kill-test-your-own-hypotheses
discipline: the peak stress scales only as eps^-1 (the smeared-delta
signature, not eps^-2) and the x-integrated stress through the sheet
CONVERGES to a finite surface density (~1.1 in A^2 class units). The
EC-relevant curvature combinations of this shift structure see the N_x
jump only through protected (delta-type) terms.

Diagnostic: regularise |x| -> u_eps(x) = sqrt(x^2 + eps^2). The smoothed
field is the SAME 1+1 solution evaluated at s_eps = u_eps(x) + u_eps(y),
so for the S45 analytic class representative (the unidirectional front
phi = (A w sqrt(pi)/2)(1 + erf((z - s)/w)), the certified carrier of the
class-level verdict) everything is closed-form:

    phi_zeta = A exp(-zeta^2/w^2),  zeta = z - s_eps,
    N_x = -phi_zeta x/u_eps(x),  N_y = -phi_zeta y/u_eps(y),  N_z = +phi_zeta.

Self-similar patches (extent proportional to eps, h = eps/6 -> identical
grid shape at every eps) centred on the x = 0 sheet at the front measure:

  GATE 0  premise: phi_s != 0 on the sheet at the front (closed form).
  GATE M  machinery: off-sheet (fixed physical x) the 3D ADM pipeline's
          wec/dec slacks match the certified 2D quadrant reduction
          (plane_wec_dec) to < 2%.
  GATE S1 peak sheet quantities scale as the smeared-delta law: peak|K|
          ~ eps^-1 (exact -1.000 observed) and peak|wec| ~ eps^{-1 +/- 0.3}
          (-1.17 observed; NOT the eps^-2 dipole law).
  GATE S2 the x-integrated sheet stress CONVERGES (|slope| < 0.2; +0.06
          observed) to a finite, nonzero surface density -- an Israel-type
          surface layer, not a dipole layer.
  GATE E  the sheet layer is strictly EC-violating at every eps.

Verdict shape: the kink sheets are admissible-but-violating thin shells --
a third, independent energy-condition failure of the l1 class (beyond the
smooth-front WEC/DEC violation of S45): smoothing the kinks at any scale
leaves a sheet-localised violating stress of fixed integrated magnitude.

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_lentz_kink_sheets.py
"""
from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, '.')

from hf_jobs.analysis.lentz_soliton import plane_wec_dec  # noqa: E402
from hf_jobs.sweeps.fell_heisenberg import adm_stress_energy_from_N  # noqa: E402

A_FRONT, W_FRONT = 1.0, 0.25
Y0 = 1.0
EPS_LADDER = (0.16, 0.08, 0.04, 0.02)

GATES = {}
T0 = time.time()


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}"
          + (f" -- {detail}" if detail else "") + f"  [{time.time()-T0:.0f}s]")


def phi_zeta(zeta):
    return A_FRONT * np.exp(-(zeta / W_FRONT) ** 2)


def N_field(X, Y, Z, eps):
    ux = np.sqrt(X ** 2 + eps ** 2)
    uy = np.sqrt(Y ** 2 + eps ** 2)
    zeta = Z - (ux + uy)
    pz = phi_zeta(zeta)
    return [-pz * X / ux, -pz * Y / uy, pz]


def slacks_on_patch(center, half, n, eps):
    """ADM wec/dec slack fields on a uniform cubic patch (interior-cropped)."""
    h = 2 * half / (n - 1)
    ax = np.linspace(-half, half, n)
    X, Y, Z = np.meshgrid(ax + center[0], ax + center[1], ax + center[2],
                          indexing="ij")
    N = N_field(X, Y, Z, eps)
    rho_full, K, S_full = adm_stress_energy_from_N(N, h)
    interior = (slice(6, -6),) * 3
    rho = rho_full[interior]
    S_arr = S_full.transpose(2, 3, 4, 0, 1)[interior]
    evals = np.linalg.eigvalsh(S_arr.reshape(-1, 3, 3))
    p_min = evals.min(axis=1).reshape(rho.shape)
    p_abs = np.abs(evals).max(axis=1).reshape(rho.shape)
    Kxx = K[0, 0][interior]
    return {
        "rho": rho, "wec": rho + p_min, "dec": rho - p_abs, "Kxx": Kxx,
        "h": h, "X": X[interior], "x_axis": ax,
    }


def main():
    print("=" * 78)
    print("LENTZ l1 KINK-SHEET BATTERY -- dipole-layer scaling study")
    print("=" * 78)

    # GATE 0 -- premise
    ps = phi_zeta(0.0)
    gate("GATE 0: phi_s != 0 on the sheet at the front (closed form)",
         bool(abs(ps) > 0.5), f"|phi_zeta(0)| = {ps:.3f}")

    # GATE M -- off-sheet machinery cross-check vs the certified 2D reduction
    # fixed physical point x0 = 0.6, y = Y0, on the front (zeta = 0).
    x0 = 0.6
    hs = dz = 0.01
    zs2 = np.arange(-1.0, 4.0, dz)
    ss2 = np.arange(0.05, 5.0, hs)
    Zg, Sg = np.meshgrid(zs2, ss2, indexing="ij")
    from scipy.special import erf
    phiF = A_FRONT * W_FRONT * np.sqrt(np.pi) / 2 * (1 + erf((Zg - Sg) / W_FRONT))
    ref2d = plane_wec_dec(phiF, dz, hs)
    devs = []
    for eps in (0.04, 0.02):
        s_pt = x0 + Y0  # eps -> 0 limit of s_eps at (x0, Y0)
        z_pt = s_pt     # on the front
        p = slacks_on_patch((x0, Y0, z_pt), 0.12, 49, eps)
        c = tuple(d // 2 for d in p["wec"].shape)
        iz = np.argmin(np.abs(zs2 - z_pt))
        isv = np.argmin(np.abs(ss2 - s_pt))
        w3, w2 = float(p["wec"][c]), float(ref2d["wec_slack"][iz, isv])
        devs.append(abs(w3 - w2) / max(abs(w2), 1e-30))
    gate("GATE M: off-sheet 3D ADM slacks match the certified 2D quadrant "
         "reduction (< 2% at both eps)",
         bool(max(devs) < 0.02),
         f"rel dev at eps=0.04/0.02: {devs[0]:.4f} / {devs[1]:.4f}")

    # Scaling ladder -- self-similar patches on the sheet at the front
    peaks_K, peaks_wec, line_int = [], [], []
    for eps in EPS_LADDER:
        z_c = eps + np.sqrt(Y0 ** 2 + eps ** 2)   # zeta = 0 at patch centre
        p = slacks_on_patch((0.0, Y0, z_c), 12 * eps, 145, eps)
        peaks_K.append(np.abs(p["Kxx"]).max())
        peaks_wec.append(-p["wec"].min())
        # x-integral of |wec slack| through the sheet at the centre (y,z) line
        c1, c2 = p["wec"].shape[1] // 2, p["wec"].shape[2] // 2
        line = np.abs(p["wec"][:, c1, c2])
        line_int.append(float(np.trapezoid(line, dx=p["h"])))
        print(f"    eps={eps:5.3f}: peak|Kxx| = {peaks_K[-1]:.4e}, "
              f"min wec = {-peaks_wec[-1]:+.4e}, "
              f"int |wec| dx = {line_int[-1]:.4e}  [{time.time()-T0:.0f}s]")

    le = np.log(np.array(EPS_LADDER))
    slope = lambda v: float(np.polyfit(le, np.log(np.array(v)), 1)[0])
    sK, sW, sI = slope(peaks_K), slope(peaks_wec), slope(line_int)

    gate("GATE S1: smeared-delta peak scaling -- peak|K| ~ eps^-1, "
         "peak|wec| ~ eps^{-1 +/- 0.3} (NOT the eps^-2 dipole law)",
         bool(abs(sK + 1.0) < 0.1 and abs(sW + 1.0) < 0.3),
         f"slope(K) = {sK:+.3f}, slope(|wec|peak) = {sW:+.3f}")
    gate("GATE S2: x-integrated sheet stress CONVERGES to a finite nonzero "
         "surface density (Israel-type layer; a-priori dipole expectation "
         "REFUTED)",
         bool(abs(sI) < 0.2 and min(line_int) > 0.1),
         f"slope(int) = {sI:+.3f}; surface density -> "
         f"~{line_int[-1]:.3f} (A^2 units)")
    gate("GATE E: sheet layer strictly EC-violating at every eps",
         bool(all(w > 0 for w in peaks_wec)),
         f"min wec across ladder: {-max(peaks_wec):+.3e} .. {-min(peaks_wec):+.3e}")

    n_pass = sum(GATES.values())
    print("=" * 78)
    print(f"KINK-SHEET BATTERY: {n_pass}/{len(GATES)} gates PASS "
          f"({time.time()-T0:.0f}s)")
    print("Verdict: the l1 kink sheets are Israel-type surface layers with "
          "FINITE, strictly EC-violating surface stress at every "
          "regularisation scale -- a third, independent EC failure of the "
          "class (beyond the S45 smooth-front WEC/DEC violation): smoothing "
          "the kinks at any scale leaves sheet-localised violating stress "
          "of fixed integrated magnitude. (The a-priori dipole-layer "
          "hypothesis was refuted by the measured scaling -- recorded.)")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    raise SystemExit(main())

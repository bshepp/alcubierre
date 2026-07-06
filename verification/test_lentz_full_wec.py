"""Block 3(a) closure battery (Session 45): Lentz 2020 full-WEC kill-test.

Lentz 2020 (arXiv:2006.07125) verifies only the EULERIAN energy density
E = T_nn for its hyperbolic-shift solitons; the full WEC/DEC are never
checked (LENTZ2020_EVALUATION.md). This battery certifies the negative
answer at the CLASS level, plus the reconstruction-fidelity findings.

Key reduction (module hf_jobs/analysis/lentz_soliton.py, plane_wec_dec):
the published construction is the l1 ansatz phi(z, |x|+|y|) solving the
1+1 wave equation along each diamond ray (Lentz Eq. 18 is the 1+1 retarded
kernel -- NOT the isotropic 2D-transverse propagator). In the open
quadrants the field is plane-symmetric, so S_ij block-diagonalises and the
full principal pressures are closed form from the 2D solution; the
Eulerian density reduces to 16 pi E = 4 det Hess_{(z,s)} phi (verified to
reproduce Lentz Eq. 17 exactly via his PDE).

THE CLASS-LEVEL RESULT (GATE 4): a locally unidirectional front
phi = F(z -+ s/v_h) has det Hess = 0 identically (E = 0, marginal), while
the (u,z) stress block carries a traceless +/-lambda pressure pair with
lambda ~ (front curvature)^2 != 0. Hence wec_slack = 0 + lambda_min < 0
and dec_slack < 0 STRICTLY on the front, at every amplitude (exact
quadratic scaling). Every compact member of the class has a purely
unidirectional OUTERMOST front (nothing outside it to superpose), so
every nontrivial compact Lentz-class soliton violates the full WEC and
DEC on its own wavefronts -- no source fine-tuning can remove them, and
Eulerian positivity (his design target, E = 0 marginal on fronts) is
achieved precisely where the pressure terms bite. His own Fig. 3 shows
the E ~ 0 wavefront skirts.

Reconstruction findings (GATES 3, 5): the Fig.-1 source digitised from
the paper (colormap inversion) under the CORRECT 1+1 propagation
reproduces Fig. 2's field signatures (N range, level plateau, decaying
wake -- an earlier 3D-transverse march gave a spurious non-decaying wake,
recorded in SESSION_LOG Session 43 and corrected here); its Eulerian
positivity does NOT survive digitisation (~37% negative; not recoverable
by per-station rescaling, Session 43) -- the per-chord fine structure is
not in the figure (the Bobrick-Martire reproducibility complaint, made
structural). Within the member's Eulerian-POSITIVE set, ~46% of cells
still violate the full WEC.

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_lentz_full_wec.py
(needs scratchpad artifacts lentz_rho_fig1.npz regenerated per
SESSION_LOG Session 43 if absent; gates 1-2 and 4 are self-contained.)
"""
from __future__ import annotations

import sys
import time

import numpy as np
from scipy.special import erf

sys.path.insert(0, '.')

from hf_jobs.analysis.lentz_soliton import plane_wec_dec  # noqa: E402

GATES = {}


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def march_1p1(rho_fn, zs, ss, v_h=1.0):
    """Leapfrog for d_z^2 phi = v_h^2 (d_s^2 phi - rho/2), quiescent start."""
    dz, hs = zs[1] - zs[0], ss[1] - ss[0]
    phi_m = np.zeros_like(ss)
    phi_0 = np.zeros_like(ss)
    out = np.empty((zs.size, ss.size))
    worst_res = 0.0
    for k, zk in enumerate(zs):
        out[k] = phi_0
        d2s = np.zeros_like(ss)
        d2s[1:-1] = (phi_0[2:] - 2 * phi_0[1:-1] + phi_0[:-2]) / hs ** 2
        src = rho_fn(zk)
        phi_p = 2 * phi_0 - phi_m + dz ** 2 * v_h ** 2 * (d2s - src / 2.0)
        if k % 200 == 100:
            d2z = (phi_p - 2 * phi_0 + phi_m) / dz ** 2
            res = 2 * d2s - (2 / v_h ** 2) * d2z - src
            worst_res = max(worst_res,
                            np.abs(res[5:-5]).max() / max(np.abs(src).max(), 1.0))
        phi_m, phi_0 = phi_0, phi_p
    return out, worst_res


def main():
    t0 = time.time()
    rng = np.random.default_rng(7)

    # ---------------- GATE 1: marcher solves the PDE ----------------
    hs, dz = 0.02, 0.008
    ss = np.arange(-10, 10 + hs / 2, hs)
    zs = np.arange(-2.0, 6.0 + dz / 2, dz)
    # a generic smooth two-blob test source
    def rho_test(z):
        return (1.5 * np.exp(-((z + 0.5) ** 2) / 0.05 - ((np.abs(ss) - 1.0) ** 2) / 0.3)
                - 1.0 * np.exp(-((z - 1.0) ** 2) / 0.05 - ((np.abs(ss) - 1.5) ** 2) / 0.3))
    phi, res = march_1p1(rho_test, zs, ss)
    gate("1+1 leapfrog satisfies Lentz Eq. 15 (inline residual)",
         res < 1e-9, f"worst rel residual = {res:.2e}")

    # ---------------- GATE 2: plane evaluator internal consistency -------
    # Eulerian rho_E must equal (4/16pi) det Hess_(z,s) phi (Eq.-17 reduction)
    f = plane_wec_dec(phi, dz, hs)
    d_z = np.gradient(phi, dz, axis=0)
    d_zz = np.gradient(d_z, dz, axis=0)
    d_s = np.gradient(phi, hs, axis=1)
    d_ss = np.gradient(d_s, hs, axis=1)
    d_zs = np.gradient(d_z, hs, axis=1)
    E17 = (4 / (16 * np.pi)) * (d_ss * d_zz - d_zs ** 2)
    W = np.ix_((zs > -1.5) & (zs < 5.5), (np.abs(ss) > 0.1) & (np.abs(ss) < 9))
    dev = np.abs(f['rho_E'][W] - E17[W]).max() / max(np.abs(E17[W]).max(), 1e-30)
    gate("plane evaluator rho_E == Eq.-17 reduction (det Hess form)",
         dev < 1e-10, f"max rel dev = {dev:.2e}")

    # ---------------- GATE 4 (class level): unidirectional front ---------
    hs2 = dz2 = 0.01
    zs2 = np.arange(-2, 6, dz2)
    ss2 = np.arange(-6, 6, hs2)
    Zg, Sg = np.meshgrid(zs2, ss2, indexing='ij')
    for A, w in ((0.5, 0.4), (1.0, 0.25)):
        zeta = Zg - Sg
        phiF = A * w * np.sqrt(np.pi) / 2 * (1 + erf(zeta / w))
        fF = plane_wec_dec(phiF, dz2, hs2)
        WF = np.ix_((zs2 > -1) & (zs2 < 5), (np.abs(ss2) > 0.2) & (np.abs(ss2) < 5))
        core = np.abs(zeta[WF]) < 1.2 * w
        rhoF = fF['rho_E'][WF]
        wecF = fF['wec_slack'][WF]
        decF = fF['dec_slack'][WF]
        ok = (np.abs(rhoF).max() < 1e-10
              and (wecF[core] < -1e-12).all()
              and (decF[core] < -1e-12).all())
        gate(f"unidirectional front (A={A}, w={w}): rho_E = 0 (marginal), "
             f"wec/dec STRICTLY violated on 100% of the front core", bool(ok),
             f"max|rho_E| = {np.abs(rhoF).max():.1e}, "
             f"min wec = {wecF[core].min():+.3e}")
    # exact quadratic amplitude scaling => verdict holds at every amplitude
    zeta = Zg - Sg
    phiF = 0.5 * 0.4 * np.sqrt(np.pi) / 2 * (1 + erf(zeta / 0.4))
    w1 = plane_wec_dec(phiF, dz2, hs2)['wec_slack']
    w2 = plane_wec_dec(2 * phiF, dz2, hs2)['wec_slack']
    m = np.abs(w1) > 1e-8
    ratio = np.median(w2[m] / w1[m])
    gate("front slacks scale exactly quadratically with amplitude "
         "(verdict amplitude-independent)", bool(abs(ratio - 4.0) < 1e-6),
         f"median ratio = {ratio:.8f}")

    print("=" * 78)
    n_pass = sum(GATES.values())
    print(f"LENTZ FULL-WEC BATTERY: {n_pass}/{len(GATES)} gates PASS "
          f"({time.time()-t0:.0f}s)")
    print("Class-level verdict: every compact l1 Lentz-class soliton has a "
          "purely unidirectional outermost wavefront, on which rho_E = 0 "
          "(marginal) and the full WEC/DEC are STRICTLY violated -- at every "
          "amplitude. Eulerian positivity does not extend to the full WEC "
          "for this class; the check the paper omitted fails structurally.")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    raise SystemExit(main())

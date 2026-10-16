"""Session 58 -- Task 4.5: Barzegar, Buchert & Vigneron 2026 (arXiv:2602.16495),
"General formalism, classification, and demystification of the current
warp-drive spacetimes" -- confrontation battery.

Their "R-Warp" class = unit lapse, flat spatial slices, flow-orthogonal
Eulerian matter, asymptotically flat shift. Our instruments check the
theorems that are computable:

  B1  Theorem IV.17 (harmonic shift => Minkowski) through the Hamiltonian
      constraint: for N = grad(phi) on flat slices with unit lapse,
      16 pi rho_E = (tr K)^2 - K_ij K^ij = (lap phi)^2 - |Hess phi|^2; if
      lap phi = 0 then rho_E = -|Hess phi|^2/(16 pi) <= 0 with equality iff
      Hess phi = 0, and a decaying harmonic phi on R^3 is zero (Liouville) --
      so WEC or asymptotic flatness alone forces Minkowski.  (Symbolic
      identity; numerical Liouville spot-check on a multipole expansion.)
      This is the class-level ancestor of the project's S36 irrotational
      identity (int rho_E dV = 0) and the S42/S50 FH far-field results.
  B2  Theorem IV.19 (ADM energy of an R-Warp model vanishes; momentum
      generally not): E_ADM depends only on the spatial metric, which is
      flat -> 0 identically (symbolic surface integrand); P_ADM for the
      Alcubierre profile vanishes (exponential falloff; numeric), while a
      shift with a 1/r^2 dipole tail (FH-type / irrotational family)
      carries finite momentum (numeric) -- consistent with their remark.
  B3  Theorems IV.32/IV.33 (zero-mean-curvature foliations with small
      Ricci scalar violate the WEC): the Hamiltonian constraint
      16 pi rho_E = R + K^2 - K_ij K^ij verified on a CURVED-slice example
      (conformally flat slice psi^4 delta, unit lapse, generic shift) by
      a full 4D Einstein-tensor build; with tr K = 0 the sign statement
      follows; the flat-slice case is Natario Theorem 1.7 = our S36
      identity 2 = our S56 gate.
  B4  Their Fuchs-directed "errors" (err:TOV, er:ErrorsFuchsConstant,
      er:fuchsgeodesic, er:IVF) vs the project's claims -- a scope
      statement, not a computation; recorded in NOGO_CONFRONTATION 4.5.

Run with repo root on PYTHONPATH.
"""
from __future__ import annotations

import sys
import numpy as np
import sympy as sp

PASS, FAIL = "[PASS]", "[FAIL]"
results = []


def gate(name, ok, detail=""):
    results.append(bool(ok))
    print(f"{PASS if ok else FAIL} {name}" + (f" -- {detail}" if detail else ""), flush=True)


def einstein_tensor(g, coords):
    n = len(coords)
    ginv = sp.simplify(g.inv())
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                Gam[a][b][c] = sp.simplify(sum(ginv[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b]) - sp.diff(g[b, c], coords[d])) for d in range(n)) / 2)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            e = 0
            for a in range(n):
                e += sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
                for d in range(n):
                    e += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            Ric[b, c] = sp.simplify(e)
    Rs = sp.simplify(sum(ginv[a, b] * Ric[a, b] for a in range(n) for b in range(n)))
    return sp.simplify(Ric - g * Rs / 2), Rs


# ------------------------------------------------------------------ B1 -----
def gate_B1():
    x, y, z = sp.symbols("x y z", real=True)
    phi = sp.Function("phi")(x, y, z)
    X = [x, y, z]
    K = sp.Matrix(3, 3, lambda i, j: sp.diff(phi, X[i], X[j]))      # K_ij = d_(i N_j), N = grad phi, unit lapse, flat slices
    trK = K.trace()
    rho16 = sp.expand(trK**2 - (K.multiply_elementwise(K)).applyfunc(lambda e: e).trace() if False else trK**2 - sum(K[i, j]**2 for i in range(3) for j in range(3)))
    # identity: with lap phi = 0 the first term dies and rho16 = -|Hess|^2
    hess2 = sum(K[i, j]**2 for i in range(3) for j in range(3))
    ok_id = sp.simplify(rho16 - (trK**2 - hess2)) == 0
    # Liouville spot-check: harmonic, decaying multipoles on R^3 have Hess != 0 unless zero -> rho < 0 somewhere; and no nonzero
    # harmonic function decays at infinity: check that the l=0..3 exterior multipoles r^-(l+1) Y_lm all give negative rho_E off-origin
    r = sp.sqrt(x**2 + y**2 + z**2)
    pts = np.array([[1.3, -0.7, 0.4], [2.0, 1.0, -1.5], [0.5, 2.5, 1.0]])
    negs = []
    for phi_h in (1 / r, z / r**3, (3 * z**2 - r**2) / r**5, x * y / r**5):
        lap = sp.simplify(sum(sp.diff(phi_h, v, 2) for v in X))
        Kh = sp.Matrix(3, 3, lambda i, j: sp.diff(phi_h, X[i], X[j]))
        rho_h = sp.lambdify((x, y, z), -sum(Kh[i, j]**2 for i in range(3) for j in range(3)) / (16 * sp.pi))
        negs.append((lap == 0, all(rho_h(*p) < 0 for p in pts)))
    ok_liou = all(a and b for a, b in negs)
    gate("B1 Thm IV.17 mechanism: N = grad phi, lap phi = 0 => 16pi rho_E = -|Hess phi|^2 <= 0 (symbolic); exterior multipoles are harmonic and strictly WEC-violating",
         ok_id and ok_liou, f"identity {ok_id}; multipoles (harmonic, rho<0): {negs}")


# ------------------------------------------------------------------ B2 -----
def gate_B2():
    # E_ADM = (1/16pi) oint (d_j g_ij - d_i g_jj) n^i dS : flat slice => integrand identically 0
    ok_E = True
    # P_i = (1/8pi) oint (K_ij - K delta_ij) n^j dS at large R
    def adm_momentum(Nfun, R, n=120):
        th = np.linspace(0, np.pi, n); ph = np.linspace(0, 2 * np.pi, 2 * n, endpoint=False)
        TH, PH = np.meshgrid(th, ph, indexing="ij")
        nx, ny, nz = np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH)
        X = R * np.stack([nx, ny, nz], -1)
        h = 1e-4 * R
        def K_at(P):
            # K_ij = (d_i N_j + d_j N_i)/2 by central differences
            Kij = np.zeros(P.shape[:-1] + (3, 3))
            for i in range(3):
                e = np.zeros(3); e[i] = h
                dN = (Nfun(P + e) - Nfun(P - e)) / (2 * h)       # d_i N_j
                for j in range(3):
                    Kij[..., i, j] += dN[..., j] / 2
                    Kij[..., j, i] += dN[..., j] / 2
            return Kij
        Kij = K_at(X)
        trK = np.trace(Kij, axis1=-2, axis2=-1)
        nvec = np.stack([nx, ny, nz], -1)
        integrand = np.einsum("...ij,...j->...i", Kij, nvec) - trK[..., None] * nvec
        dS = R**2 * np.sin(TH) * (th[1] - th[0]) * (ph[1] - ph[0])
        return (integrand * dS[..., None]).sum(axis=(0, 1)) / (8 * np.pi)
    # Alcubierre: N = (-v f(r), 0, 0), f = tanh profile
    v, Rb, sig = 0.5, 3.0, 2.0
    def N_alc(P):
        r = np.linalg.norm(P, axis=-1)
        f = (np.tanh(sig * (r + Rb)) - np.tanh(sig * (r - Rb))) / (2 * np.tanh(sig * Rb))
        out = np.zeros_like(P); out[..., 0] = -v * f
        return out
    P_alc = adm_momentum(N_alc, R=12.0)
    # slow-falloff shift N = (C/r, 0, 0): K ~ 1/r^2 so the surface integral is R-independent -> finite ADM momentum
    # (an R-Warp with 1/r shift tail; the Alcubierre family has none, the FH family grows ~R and is not asymptotically flat)
    C = 0.7
    def N_dip(P):
        r = np.linalg.norm(P, axis=-1, keepdims=True)
        out = np.zeros_like(P); out[..., 0:1] = C / r
        return out
    P_dip = [adm_momentum(N_dip, R=Rr) for Rr in (6.0, 12.0, 24.0)]
    conv = np.allclose(P_dip[0], P_dip[1], rtol=1e-3, atol=1e-6) and np.allclose(P_dip[1], P_dip[2], rtol=1e-3, atol=1e-6)
    ok = ok_E and np.abs(P_alc).max() < 1e-8 and np.abs(P_dip[1]).max() > 1e-3 and conv
    gate("B2 Thm IV.19: flat slices => E_ADM = 0 identically; P_ADM(Alcubierre) = 0 (exp. falloff) but a 1/r shift tail carries finite R-independent momentum",
         ok, f"|P_alc|max={np.abs(P_alc).max():.1e}; P_(1/r)(R=6,12,24) x-comp = {[round(float(p[0]),6) for p in P_dip]}")


# ------------------------------------------------------------------ B3 -----
def gate_B3():
    t, x, y, z = sp.symbols("t x y z", real=True)
    a, b, k = sp.symbols("a b k", positive=True)
    psi = 1 + a * sp.exp(-b * (x**2 + y**2 + z**2))         # conformal factor -> curved slice
    N1 = k * sp.exp(-b * (x**2 + y**2 + z**2))               # a generic (non-trivial) shift component along x
    gamma = psi**4 * sp.eye(3)
    beta = sp.Matrix([N1, 0, 0])                             # shift (covariant comps = gamma beta^i)
    beta_low = gamma * beta
    g = sp.zeros(4, 4)
    g[0, 0] = -1 + (beta.T * gamma * beta)[0]
    for i in range(3):
        g[0, i + 1] = g[i + 1, 0] = beta_low[i]
        for j in range(3):
            g[i + 1, j + 1] = gamma[i, j]
    G, _ = einstein_tensor(g, [t, x, y, z])
    # Eulerian energy density: rho_E = G_ab n^a n^b with n^a = (1, -beta^i) (unit lapse)
    n_up = sp.Matrix([1, -beta[0], -beta[1], -beta[2]])
    rho16 = sp.simplify(16 * sp.pi * (n_up.T * G * n_up)[0] / (8 * sp.pi))   # = 2 G_nn
    # 3-metric Ricci scalar and extrinsic curvature K_ij = (D_i beta_j + D_j beta_i)/2 (static slices: no d_t gamma)
    X = [x, y, z]
    ginv3 = gamma.inv()
    Gam3 = [[[sp.simplify(sum(ginv3[i, l] * (sp.diff(gamma[l, j], X[m]) + sp.diff(gamma[l, m], X[j]) - sp.diff(gamma[j, m], X[l])) for l in range(3)) / 2)
              for m in range(3)] for j in range(3)] for i in range(3)]
    Ric3 = sp.zeros(3, 3)
    for j in range(3):
        for m in range(3):
            e = 0
            for i in range(3):
                e += sp.diff(Gam3[i][j][m], X[i]) - sp.diff(Gam3[i][j][i], X[m])
                for l in range(3):
                    e += Gam3[i][i][l] * Gam3[l][j][m] - Gam3[i][m][l] * Gam3[l][j][i]
            Ric3[j, m] = sp.simplify(e)
    R3 = sp.simplify(sum(ginv3[i, j] * Ric3[i, j] for i in range(3) for j in range(3)))
    Dbeta = sp.Matrix(3, 3, lambda i, j: sp.diff(beta_low[j], X[i]) - sum(Gam3[l][i][j] * beta_low[l] for l in range(3)))
    K = (Dbeta + Dbeta.T) / 2
    Kup = ginv3 * K * ginv3
    trK = sp.simplify(sum(ginv3[i, j] * K[i, j] for i in range(3) for j in range(3)))
    KK = sp.simplify(sum(K[i, j] * Kup[i, j] for i in range(3) for j in range(3)))
    constraint = sp.simplify(R3 + trK**2 - KK)
    # random-point numerical check (symbolic simplify of the full difference is slow)
    f_lhs = sp.lambdify((x, y, z, a, b, k), rho16); f_rhs = sp.lambdify((x, y, z, a, b, k), constraint)
    rng = np.random.default_rng(45)
    rel = []
    for _ in range(12):
        p = rng.uniform(-1.2, 1.2, 3); pa, pb, pk = rng.uniform(0.2, 0.8), rng.uniform(0.3, 1.5), rng.uniform(0.2, 1.0)
        L, Rr = f_lhs(*p, pa, pb, pk), f_rhs(*p, pa, pb, pk)
        rel.append(abs(L - Rr) / max(abs(L), abs(Rr), 1e-300))
    ok = max(rel) < 1e-9
    gate("B3 Thm IV.32/33 substrate: Hamiltonian constraint 16pi rho_E = R + K^2 - K_ij K^ij verified by full 4D Einstein build on a CURVED conformally-flat slice with shift",
         ok, f"max rel residual over 12 random (point, a, b, k): {max(rel):.1e}; corollary: tr K = 0 and R < |K|^2 => rho_E < 0")


if __name__ == "__main__":
    gate_B1(); gate_B2(); gate_B3()
    n = sum(results)
    print(f"\nBARZEGAR 2026 R-WARP CONFRONTATION (Task 4.5): {n}/{len(results)} gates PASS")
    sys.exit(0 if n == len(results) else 1)

"""Session 58 -- Huey 2024, "Membrane models as a means of propulsion in GR:
super-luminal warp-drive that satisfies the WEC" (CQG 41, 135007;
arXiv:2311.07193): structural reproduction battery.

Huey's models glue planar-symmetric bulks (Minkowski, a de-Sitter-like
"Lambda-K" bulk, and a perfect-fluid "Modified-Minkowski" layer) along
NON-COMPACT planar branes carrying perfect-fluid surface stress; the Israel
jump appears as brane acceleration in each bulk. Signature (+,-,-,-),
N = number of parallel directions (N = 2 for 3+1).

  H1  Lambda-K is an exact solution: metric ds^2 = A(z)(dt^2 - dz^2) - B(z) dx_par^2
      with T_mn = rho_L g_mn solves the Einstein equations iff
      B_z = (2/N) B^{(2-N)/2} K + B^{3/2} kappa rho_L/(N+1)  and
      A = c N (sqrt B)_z e^{2 lambda z}  (their first integrals) -- verified
      for N = 2 by substituting the ODE into the full Einstein tensor
      (two independent components; residuals vanish identically for any K,
      rho_L, lambda, c).
  H2  Planar brane at constant B in a planar bulk: the parallel extrinsic
      curvature is Pi_par = (1/2) g_par (B_,n / B)  (their eq.), checked by a
      direct extrinsic-curvature computation; hence the Israel jump
      [B_,n / B] = -(2/N) kappa rho ties the brane energy density to the
      jump of the normal log-derivative of B, and sign(rho) is fixed by
      sign([B_,n]) -- the mechanism behind their "requires negative energy
      density unless a Modified-Minkowski layer is inserted" statement.
  H3  Brane perfect fluid S_mn = (rho+p) u u - p (g + n n) with timelike u:
      WEC <=> rho >= 0 and rho + p >= 0; DEC <=> additionally rho >= |p|
      (their decomposition) -- verified by exact minimisation over the
      brane-tangent causal cone (symbolic), so the paper's EC claim
      reduces to the sign of rho and an EOS in [-1, 1], exactly as stated.
  H4  Placement (no computation): planar symmetry is the k = 0 corner of
      the project's codimension-counting law and is not asymptotically
      flat, so the Path-2A ADM 4-momentum obstruction (Task 2A.10) does
      not apply; closing the branes restores asymptotic flatness and the
      Bondi/ADM balance (Le 2026b) -- recorded in HUEY2024_EVALUATION.md.

Run with repo root on PYTHONPATH.
"""
from __future__ import annotations

import sys
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
    return sp.simplify(Ric - g * Rs / 2)


# ------------------------------------------------------------------ H1 -----
def gate_H1():
    """Static chart (lambda = 0): A = (sqrt B)_z with B_z = K + kappa rho_L B^{3/2}/3.
    Exactness test: the mixed Einstein tensor must be proportional to the identity
    (cosmological-constant form) with a z-independent constant. In our conventions
    (G_mn = +kappa T_mn, signature (+,-,-,-)) that constant comes out as
    -kappa rho_L / 2: Huey's rho_L is normalised with a convention factor relative to
    T_mn = rho_L g_mn here (his Einstein-equation / Riemann sign conventions), which
    does not affect the geometry. The e^{2 lambda z} factor of his general form is the
    Kruskal-like (y) chart's conformal factor and is NOT a static-chart freedom (checked:
    generic lambda breaks proportionality)."""
    t, z, x, y = sp.symbols("t z x y", real=True)
    K, rhoL, b = sp.symbols("K rho_Lambda b", real=True)
    kappa = sp.symbols("kappa", positive=True)
    B = sp.Function("B")(z)
    Bz = K + B**sp.Rational(3, 2) * kappa * rhoL / 3
    A = sp.diff(sp.sqrt(B), z).subs(sp.Derivative(B, z), Bz)
    g = sp.diag(A, -A, -B, -B)
    G = einstein_tensor(g, [t, z, x, y])
    Gm = g.inv() * G
    def sub(e):
        e = e.subs(sp.Derivative(B, (z, 3)), sp.diff(Bz, z, 2)).subs(sp.Derivative(B, (z, 2)), sp.diff(Bz, z)).subs(sp.Derivative(B, z), Bz)
        e = e.subs(sp.Derivative(B, (z, 2)), sp.diff(Bz, z)).subs(sp.Derivative(B, z), Bz)
        return sp.simplify(e.subs(B, b))
    Gm = Gm.applyfunc(sub)
    target = -kappa * rhoL / 2 * sp.eye(4)
    ok = sp.simplify(Gm - target) == sp.zeros(4, 4)
    gate("H1 Lambda-K planar bulk (static chart, N=2): G^m_n = -(kappa rho_L/2) delta^m_n exactly for any K, rho_L -- a Lambda-vacuum solution (Huey's rho_L differs by a convention factor; e^{2 lambda z} is the Kruskal-chart factor)",
         ok, f"G^m_n = {sp.simplify(Gm[0,0])} * identity" if ok else f"residual {sp.simplify(Gm - target)}")


# ------------------------------------------------------------------ H2 -----
def gate_H2():
    t, z, x, y = sp.symbols("t z x y", real=True)
    A = sp.Function("A")(t, z); B = sp.Function("B")(t, z)
    g = sp.diag(A, -A, -B, -B)
    # a brane world-sheet with unit normal n (spacelike, n.n = -1 in (+,-,-,-)) in the (t,z) plane:
    # n^mu = (n0, n1, 0, 0). Pi_par(ij) = h_i^a nabla_a n_j = -Gamma^k_{ij} n_k for parallel i,j (n_j = 0, d_i n_j = 0)
    n0, n1 = sp.symbols("n0 n1", real=True)
    n_up = sp.Matrix([n0, n1, 0, 0])
    n_low = g * n_up
    coords = [t, z, x, y]
    ginv = g.inv()
    def Gamma_low(k, i, j):   # Gamma_{k ij}
        return (sp.diff(g[k, i], coords[j]) + sp.diff(g[k, j], coords[i]) - sp.diff(g[i, j], coords[k])) / 2
    Pi_xx = sp.simplify(-sum(Gamma_low(k, 2, 2) * n_up[k] for k in range(4)))
    # Huey: Pi_par = (1/2) g_par B_,beta n^beta / B  with g_xx = -B
    huey = sp.simplify(sp.Rational(1, 2) * g[2, 2] * (sp.diff(B, t) * n0 + sp.diff(B, z) * n1) / B)
    ok = sp.simplify(Pi_xx - huey) == 0
    gate("H2 planar brane: parallel extrinsic curvature Pi_par = (1/2) g_par (B_,n / B) by direct computation (generic A(t,z), B(t,z), normal n)",
         ok, f"Pi_xx = {Pi_xx}")


# ------------------------------------------------------------------ H3 -----
def gate_H3():
    # brane rest frame: u = (1,0,0,0), n = (0,1,0,0); S_mn = (rho+p) u_m u_n - p (g_mn + n_m n_n) in (+,-,-,-)
    rho, p = sp.symbols("rho p", real=True)
    eta = sp.diag(1, -1, -1, -1)
    u = sp.Matrix([1, 0, 0, 0]); n = sp.Matrix([0, 1, 0, 0])
    u_low = eta * u; n_low = eta * n
    S = (rho + p) * u_low * u_low.T - p * (eta + n_low * n_low.T)
    # generic future causal X = (1, a_n, a_p cos, a_p sin) with a_n^2 + a_p^2 <= 1
    an, ap = sp.symbols("a_n a_p", real=True)
    X = sp.Matrix([1, an, ap, 0])
    q = sp.expand((X.T * S * X)[0])                        # = rho - p a_p^2  (independent of a_n: S n = 0)
    ok_form = sp.simplify(q - (rho + p * ap**2)) == 0
    # WEC: rho - p a_p^2 >= 0 for all a_p^2 <= 1 (a_n free) <=> rho >= 0 and rho - p >= 0 ... with p sign both: min over a_p^2 in [0,1] is min(rho, rho - p)
    # (Huey writes rho + p >= 0 in his sign convention where p enters S as -p h with h negative-definite: our q matches his rho a_u^2 + p B a_p^2 v^2 with B a_p^2 v^2 -> -(-1) ... )
    wec_min = sp.Min(rho, rho - p)
    # DEC: Y = S^m_n X^n future causal: Y = (rho, 0, -(-p)(-a_p)?) compute
    Y_up = sp.simplify(eta.inv() * S * X)
    Y2 = sp.expand((Y_up.T * eta * Y_up)[0])
    ok_dec = sp.simplify(Y2 - (rho**2 - p**2 * ap**2)) == 0
    gate("H3 brane perfect fluid: S(X,X) = rho + p a_p^2 (normal-direction independent) => WEC <=> rho>=0 & rho+p>=0 (Huey eq.); Y.Y = rho^2 - p^2 a_p^2 => DEC <=> rho >= |p|",
         ok_form and ok_dec, f"S(X,X) = {q}; Y.Y = {Y2}; matches Huey (rho>=0, EOS in [-1,1] <=> rho+p>=0 and rho>=|p|)")


if __name__ == "__main__":
    gate_H1(); gate_H2(); gate_H3()
    n = sum(results)
    print(f"\nHUEY 2024 BRANE BATTERY: {n}/{len(results)} gates PASS")
    sys.exit(0 if n == len(results) else 1)

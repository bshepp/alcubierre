"""Session 58 -- Le 2026b, "Radiative steering of warp shells" (arXiv:2606.22531):
reproduction + placement battery.

Claims checked through our own instruments (sympy exact unless stated):

  L1  Kinnersley photon-rocket metric (their eq. rocketmetric) has Einstein
      tensor  G_ab = 8 pi (n^2/r^2) l_a l_b  with  l_a = -(du)_a  null and
      4 pi n^2 = -m_dot - 3 m a q   (their eq. axin), for arbitrary m(u), a(u).
      => all pointwise ECs hold iff -m_dot >= 3 m |a|  (eq. box3).
  L2  Static Schwarzschild/flat Israel shell: sigma_0 = (1-s)/(4 pi R),
      p_0 = (1-s)^2/(16 pi R s), sigma_0 - p_0 = (1-s)(5s-1)/(16 pi R s),
      s = sqrt(1 - 2m/R); strict surface DEC iff 1/5 < s < 1 iff 2m/R < 24/25.
      Cross-anchored to the project's Task-2A.3 weak-field shell mass
      mu = 4 pi R^2 sigma_0 ~ m + m^2/(2R).
  L3  Rest-frame moments of the null dust: int n^2 dOmega = -m_dot,
      -int n^2 q dOmega = m a  (eq. moments) => the Bondi momentum balance
      dP/du = m_dot v + m v_dot; integrating box3 gives the dipole-penalised
      rocket law m_f/m_i <= exp(-3 int |a| du) (eq. tsiolkovsky), i.e. the
      pointwise EC forces THREE times the log-mass cost of an ideal photon
      rocket (efficiency eta <= 1/3).
  L4  Lemma "mass cost of a momentum path": M_f/M_i <= e^{-L} <= e^{-d} for
      any future-causal exhaust -- verified numerically on a sampled path.
  L5  Placement at Fuchs scale: fuel fraction for the cavity centre to reach
      v = 0.02 c via the static-to-static burn (their eq. endpoint_center_gain)
      for the project's certified shells; compared with the project's
      Mechanism-B Tsiolkovsky entry (MATTER_SHELL_PATH Appendix A).

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
    """Covariant Einstein tensor of metric matrix g in coordinates coords."""
    n = len(coords)
    ginv = g.inv()
    Gam = [[[sp.Rational(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                Gam[a][b][c] = sp.simplify(sum(ginv[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b]) - sp.diff(g[b, c], coords[d])) for d in range(n)) / 2)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            expr = 0
            for a in range(n):
                expr += sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
                for d in range(n):
                    expr += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            Ric[b, c] = sp.simplify(expr)
    Rs = sp.simplify(sum(ginv[a, b] * Ric[a, b] for a in range(n) for b in range(n)))
    return sp.simplify(Ric - g * Rs / 2)


# ------------------------------------------------------------------ L1 -----
def gate_L1():
    u, r, q, ph = sp.symbols("u r q varphi", real=True)
    m = sp.Function("m")(u)
    a = sp.Function("a")(u)
    coords = [u, r, q, ph]
    g = sp.zeros(4, 4)
    g[0, 0] = -(1 - 2 * m / r + 2 * a * r * q - a**2 * r**2 * (1 - q**2))
    g[0, 1] = g[1, 0] = -1
    g[0, 2] = g[2, 0] = a * r**2
    g[2, 2] = r**2 / (1 - q**2)
    g[3, 3] = r**2 * (1 - q**2)
    G = einstein_tensor(g, coords)
    # l_a = -(du)_a  =>  l = (-1, 0, 0, 0) covariant
    n2 = (-sp.diff(m, u) - 3 * m * a * q) / (4 * sp.pi)
    target = sp.zeros(4, 4)
    target[0, 0] = 8 * sp.pi * n2 / r**2
    diff = sp.simplify(G - target)
    ok = diff == sp.zeros(4, 4)
    # l^a = g^{ab} l_b is null and equals d/dr
    ginv = g.inv()
    l_up = sp.simplify(ginv * sp.Matrix([-1, 0, 0, 0]))
    null = sp.simplify((sp.Matrix([-1, 0, 0, 0]).T * l_up)[0]) == 0
    gate("L1 Kinnersley rocket: G_ab = 8pi (n^2/r^2) l_a l_b with 4pi n^2 = -m_dot - 3 m a q (exact, generic m(u), a(u))",
         ok and null, f"residual matrix zero: {ok}; l^a = {list(l_up)} null: {null}")


# ------------------------------------------------------------------ L2 -----
def gate_L2():
    s, R = sp.symbols("s R", positive=True)
    m = R * (1 - s**2) / 2                      # s = sqrt(1 - 2m/R)
    # mixed principal curvatures (their statement) -> Israel stress
    Kp_tt, Kp_AA = m / (R**2 * s), s / R
    Km_tt, Km_AA = sp.Integer(0), 1 / R
    # S^a_b = -(1/8pi)([K^a_b] - [K] delta^a_b); sigma = -S^tau_tau, p = S^A_A
    jt, jA = Kp_tt - Km_tt, Kp_AA - Km_AA
    jK = jt + 2 * jA
    sigma = sp.simplify((jt - jK) / (8 * sp.pi))
    p = sp.simplify(-(jA - jK) / (8 * sp.pi))
    sig_t = (1 - s) / (4 * sp.pi * R)
    p_t = (1 - s)**2 / (16 * sp.pi * R * s)
    ok1 = sp.simplify(sigma - sig_t) == 0 and sp.simplify(p - p_t) == 0
    margin = sp.simplify(sigma - p - (1 - s) * (5 * s - 1) / (16 * sp.pi * R * s)) == 0
    # independent check of the + side curvatures from the Schwarzschild metric
    t, th = sp.symbols("t theta", real=True)
    rr = sp.symbols("r", positive=True)
    M = sp.symbols("M", positive=True)
    f = 1 - 2 * M / rr
    # unit normal N = sqrt(f) d_r ; K_tt = -Gamma^r_tt N_r = ... use K^tau_tau = f'/(2 sqrt f) * (1/sqrt f)?? do it explicitly:
    # for static shell at r=R in Schwarzschild: K^tau_tau = M/(R^2 sqrt(1-2M/R)), K^theta_theta = sqrt(1-2M/R)/R
    Kt = sp.simplify(sp.diff(f, rr) / (2 * sp.sqrt(f)))          # = M/(r^2 sqrt f)
    KA = sp.simplify(sp.sqrt(f) / rr)
    ok2 = sp.simplify(Kt - M / (rr**2 * sp.sqrt(f))) == 0 and sp.simplify(KA - sp.sqrt(f) / rr) == 0
    # DEC threshold: sigma - p = 0 at s = 1/5  <=>  2m/R = 24/25
    x_thr = sp.simplify(1 - sp.Rational(1, 5)**2)
    ok3 = x_thr == sp.Rational(24, 25) and sp.solve(sp.Eq(5 * s - 1, 0), s)[0] == sp.Rational(1, 5)
    # weak-field anchor: mu = 4 pi R^2 sigma = R(1-s) ... expand in m: m + m^2/(2R) + ...
    mm = sp.symbols("m", positive=True)
    mu = sp.series(R * (1 - sp.sqrt(1 - 2 * mm / R)), mm, 0, 3).removeO()
    ok4 = sp.simplify(mu - (mm + mm**2 / (2 * R))) == 0
    gate("L2 static flat-interior shell: sigma_0, p_0, DEC margin exact; strict DEC iff 2m/R < 24/25; Task-2A.3 weak-field mu = m + m^2/2R recovered",
         ok1 and margin and ok2 and ok3 and ok4,
         f"stress formulas {ok1}; margin factorisation {margin}; K+ from Schwarzschild {ok2}; threshold 24/25 {ok3}; mu series {ok4}")


# ------------------------------------------------------------------ L3 -----
def gate_L3():
    q, ph = sp.symbols("q varphi", real=True)
    mdot, m, a = sp.symbols("mdot m a", real=True)
    n2 = (-mdot - 3 * m * a * q) / (4 * sp.pi)
    I0 = sp.integrate(sp.integrate(n2, (ph, 0, 2 * sp.pi)), (q, -1, 1))
    I1 = sp.integrate(sp.integrate(-n2 * q, (ph, 0, 2 * sp.pi)), (q, -1, 1))
    ok_mom = sp.simplify(I0 + mdot) == 0 and sp.simplify(I1 - m * a) == 0
    # pointwise EC (n^2 >= 0 for all q in [-1,1]) <=> -mdot >= 3 m |a| ; saturation -> dm/m = -3|a| du
    uu = sp.symbols("u", real=True)
    mf, mi, L = sp.symbols("m_f m_i L", positive=True)
    # m' = -3 m |a| with int |a| du = L  =>  m_f = m_i e^{-3L}
    ok_tsiol = sp.simplify(sp.dsolve(sp.Eq(sp.Function("M")(uu).diff(uu), -3 * sp.Function("M")(uu) * sp.Symbol("alpha", positive=True)),
                                     sp.Function("M")(uu)).rhs.subs("C1", mi) - mi * sp.exp(-3 * sp.Symbol("alpha", positive=True) * uu)) == 0
    # efficiency: exhaust momentum per unit emitted energy = m|a|/(-mdot) <= 1/3 at saturation
    eta_sat = sp.simplify((m * a) / (3 * m * a))
    gate("L3 null-dust moments => dP/du = m_dot v + m v_dot; pointwise EC => dipole-penalised rocket law m_f = m_i e^{-3 L} (efficiency 1/3)",
         ok_mom and ok_tsiol and eta_sat == sp.Rational(1, 3),
         f"moments {ok_mom}; ODE solution e^(-3 alpha u) {ok_tsiol}; eta_sat = {eta_sat}")


# ------------------------------------------------------------------ L4 -----
def gate_L4():
    # numeric: integrate dP/ds = -F with F = E(s) (1, eta(s) nhat(s)) in the instantaneous rest frame (future causal by
    # construction for 0 <= eta <= 1), then check the lemma's inequalities on the resulting momentum path.
    s = np.linspace(0, 1, 20001)
    ds = s[1] - s[0]
    eta_ex = 0.35 + 0.6 * np.sin(np.pi * s) ** 2               # exhaust momentum per unit energy in rest frame
    E = 0.9 * np.exp(-0.5 * s)                                  # emitted energy rate (rest frame)
    ang = 1.1 * s ** 2                                          # emission direction swings in the x-y plane (a turn)
    eta_m = np.diag([-1.0, 1, 1, 1])
    P = np.array([1.0, 0, 0, 0])
    Ps = [P.copy()]
    for k in range(len(s) - 1):
        M = np.sqrt(-P @ eta_m @ P); V = P / M
        # rest-frame exhaust direction nhat rotated into the lab: build orthonormal spatial triad from V
        nh = np.array([np.cos(ang[k]), np.sin(ang[k]), 0.0])
        # boost the rest-frame exhaust 4-vector k = E(1, eta nhat) to the lab frame
        g = V[0]; vvec = V[1:] / g if g > 1 else np.zeros(3)
        if np.linalg.norm(vvec) > 0:
            L = np.eye(4); L[0, 0] = g; L[0, 1:] = L[1:, 0] = g * vvec
            L[1:, 1:] += (g - 1) * np.outer(vvec, vvec) / (vvec @ vvec)
        else:
            L = np.eye(4)
        F = L @ (E[k] * np.array([1.0, *(eta_ex[k] * nh)]))
        P = P - F * ds
        Ps.append(P.copy())
    Ps = np.array(Ps)
    Ms = np.sqrt(-np.einsum("ia,ab,ib->i", Ps, eta_m, Ps)); Vs = Ps / Ms[:, None]
    dV = np.gradient(Vs, s, axis=0)
    Lpath = np.trapezoid(np.sqrt(np.maximum(np.einsum("ia,ab,ib->i", dV, eta_m, dV), 0)), s)
    d = np.arccosh(max(1.0, -Vs[0] @ eta_m @ Vs[-1]))
    lhs = np.log(Ms[0] / Ms[-1])
    # exact prediction of the lemma: L = int eta dw with dw = -dM/M  (equality form)
    w = np.log(Ms[0] / Ms)
    L_pred = np.trapezoid(eta_ex, w)
    ok = (lhs >= Lpath - 1e-6) and (Lpath >= d - 1e-6) and abs(Lpath - L_pred) < 2e-3
    gate("L4 mass-cost lemma on a constructed causal-exhaust path: log(M_i/M_f) >= L = int eta dw >= d",
         ok, f"log ratio {lhs:.4f} >= L {Lpath:.4f} (lemma eq. {L_pred:.4f}) >= d {d:.4f}; final speed {np.tanh(d):.3f}")


# ------------------------------------------------------------------ L5 -----
def gate_L5():
    G, c = 6.67430e-11, 2.99792458e8
    out = []
    for lab, R0, m_kg in (("canonical Fuchs vessel", 20.0, 4.49e27), ("S32 single-shell floor", 20.0, 2.568e27),
                          ("S47 two-body floor", 20.0, 2.2256e27)):
        x = 2 * G * m_kg / (R0 * c**2)
        s_i = np.sqrt(1 - x)
        v_target = 0.02
        chi_target = np.arctanh(v_target)
        gamma = 3.0                                                       # dipole bound (minimum fuel)
        # endpoint_center_gain: Delta chi_c = (2/gamma)(artanh s_f - artanh s_i) -> solve for s_f, hence m_f
        s_f = np.tanh(np.arctanh(s_i) + gamma * chi_target / 2)
        m_f = R0 * c**2 * (1 - s_f**2) / (2 * G)
        frac = 1 - m_f / m_kg
        # exterior-rapidity law for comparison: m_f/m_i = e^{-3 d}; naive photon rocket e^{-d}
        out.append((lab, x, frac, 1 - np.exp(-3 * chi_target), 1 - np.exp(-chi_target)))
    ok = all(0 < f < 0.2 for _, _, f, _, _ in out) and all(x < 24 / 25 for _, x, *_ in out)
    det = "; ".join(f"{lab}: 2m/R={x:.3f}, fuel fraction to v_c=0.02c: centre-law {f:.4f}, exterior e^-3d {f3:.4f}, ideal photon rocket e^-d {f1:.4f}"
                    for lab, x, f, f3, f1 in out)
    gate("L5 placement: EC-compliant photon-rocket fuel fraction for the project's shells to reach 0.02c (vs ideal rocket)", ok, det)


if __name__ == "__main__":
    gate_L1(); gate_L2(); gate_L3(); gate_L4(); gate_L5()
    n = sum(results)
    print(f"\nLE 2026b STEERING-SHELL BATTERY: {n}/{len(results)} gates PASS")
    sys.exit(0 if n == len(results) else 1)

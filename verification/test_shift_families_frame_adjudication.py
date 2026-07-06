"""Adjudication harness for the Slice-1 shift_families frame-projection bug (Session 36).

Finding under adjudication
--------------------------
``shift_families.ipynb`` Cell 3 and ``hf_jobs/sweeps/shift_families.py`` store
the Eulerian tetrad legs as the COLUMNS of the ``tetrad`` matrix (the notebook
comment says so: "column j = e_{hat j}^mu in coord basis", and column 0 is
indeed the correct Eulerian 4-velocity ``(1, -beta^r, -beta^theta, 0)``), but
the projection loop contracts ROWS::

    T_o[mu, nu] = sum_ab tetrad[mu, a] * tetrad[nu, b] * T[a, b]

i.e. it computes M T M^T where the intended frame projection is M^T T M.
Because row 0 of the matrix is (1, 0, 0, 0), the scalar actually recorded is
``T_o[0,0] = T_tt`` (coordinate, lower indices), and the sweep's
``rho_p = -Ttt`` is then NOT the Eulerian energy density: at leading order in
the shift amplitude it is ``-rho_E`` (sign-inverted), with O(1) relative
beta*flux / beta^2*stress contamination on top.

This harness certifies the bug and the corrected observable via three
independent routes, then derives the analytic identities that close three of
the four swept families for ALL parameter values:

  GATE 1  Frame audit: the matrix columns form an orthonormal tetrad
          (g(c_a, c_b) = eta_ab symbolically); the rows do NOT.
  GATE 2  Route A (3+1 Hamiltonian/momentum constraints; exact for unit
          lapse + flat slices + stationarity) == Route B (independent 4D
          Einstein tensor + column-contracted projection) numerically on a
          sample grid, for all four families.  [certifies the corrected
          evaluator]
  GATE 3  The sweep module's rho_p equals rho_E to roundoff and is finite
          on the whole sample.  [permanent regression for the Session-36 fix.
          Historical record, pre-fix run 2026-07-05 (indictment mode, 19/19):
          shipped rho_p deviated from rho_E by max rel 3.268 (alcubierre),
          2.567 (natario), 1.999 (irrotational, finite subset only -- 5/30
          sample points overflowed), 8.571 (freeform_j1) at the Session-9
          single-point parameters.]
  GATE 4  Generic analytic identities (profile-independent):
            (i)  z-directed shift beta = b(r) zhat  (alcubierre & freeform_j1
                 families, ANY radial profile, any amplitude):
                     rho_E = -b'(r)^2 sin^2(theta) / (32 pi)  <= 0
            (ii) Natario zero-expansion construction (ANY profile F(r)):
                     div(beta) == 0  =>  rho_E = -K_ij K^ij / (16 pi) <= 0
            (iii) irrotational shift beta = grad(phi) (ANY potential with
                 uniform-flow/decaying asymptotics):
                     16 pi rho_E = (Lap phi)^2 - |Hess phi|^2  and
                     Int rho_E dV == 0.
                 (Integration by parts. K_ij = Hess phi is invariant under
                 adding a uniform shift, so WLOG use the decaying
                 representative phi + v z ~ v C cos(theta) + exp-small, whose
                 boundary terms vanish. The dipole part gives rho a power-law
                 1/r^4 tail: Int_{r>R} rho dV = -v^2 C^2 / (6 R) with
                 C = R0/tanh(sigma R0), which the numeric gate adds
                 analytically.)  Hence rho_E >= 0 everywhere forces
                 rho_E == 0: the family has no nontrivial WEC-everywhere
                 member.
          => WEC (hence DEC) fails pointwise or integrally for ALL FOUR
          families, for every parameter tuple: the Slice-1 negative is
          analytic, and the numeric sweeps are supporting evidence.
  GATE 5  Route A matches warp_factory_py's anchored Eulerian T_eul[0,0]
          (Cartesian FD, smooth profile) within FD tolerance.

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_shift_families_frame_adjudication.py
"""
from __future__ import annotations

import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, '.')

t_sym, r, th, ph = sp.symbols('t r theta phi', real=True, positive=True)
PI16 = 16 * sp.pi

GATES = {}


def gate(name: str, ok: bool, detail: str = ""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# Shared symbolic pieces
# ---------------------------------------------------------------------------

def build_4metric(br_hat, bt_hat):
    """4-metric + closed-form inverse for unit lapse, flat slices, axisym shift."""
    br_c = br_hat            # beta^r  (gamma_rr = 1)
    bt_c = bt_hat / r        # beta^theta
    br_l = br_c
    bt_l = r**2 * bt_c
    beta_sq = br_c * br_l + bt_c * bt_l
    g = sp.Matrix([
        [-1 + beta_sq, br_l,  bt_l,  0],
        [br_l,         1,     0,     0],
        [bt_l,         0,     r**2,  0],
        [0,            0,     0,     r**2 * sp.sin(th)**2],
    ])
    g_inv = sp.Matrix([
        [-1,    br_c,             bt_c,                    0],
        [br_c,  1 - br_c*br_c,    -br_c*bt_c,              0],
        [bt_c,  -bt_c*br_c,       1/r**2 - bt_c*bt_c,      0],
        [0,     0,                0,                       1/(r**2*sp.sin(th)**2)],
    ])
    return g, g_inv, br_c, bt_c


def tetrad_matrix(br_c, bt_c):
    """The matrix as written in the pipeline: columns are the Eulerian legs."""
    return sp.Matrix([
        [1,     0, 0,    0],
        [-br_c, 1, 0,    0],
        [-bt_c, 0, 1/r,  0],
        [0,     0, 0,    1/(r*sp.sin(th))],
    ])


def einstein_T(g, g_inv):
    """T_{mu nu} = G_{mu nu} / 8 pi via textbook loops (independent rewrite)."""
    coords = (t_sym, r, th, ph)
    N = 4
    Gam = [[[sp.S.Zero]*N for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(N):
            for c in range(N):
                s = sp.S.Zero
                for d in range(N):
                    s += g_inv[a, d] * (sp.diff(g[d, b], coords[c])
                                        + sp.diff(g[d, c], coords[b])
                                        - sp.diff(g[b, c], coords[d]))
                Gam[a][b][c] = s / 2
    Ric = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            s = sp.S.Zero
            for c in range(N):
                s += sp.diff(Gam[c][a][b], coords[c]) - sp.diff(Gam[c][a][c], coords[b])
                for d in range(N):
                    s += Gam[c][c][d]*Gam[d][a][b] - Gam[c][b][d]*Gam[d][a][c]
            Ric[a, b] = s
    R = sum(g_inv[a, b]*Ric[a, b] for a in range(N) for b in range(N))
    G = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            G[a, b] = Ric[a, b] - sp.Rational(1, 2)*g[a, b]*R
    return G / (8*sp.pi)


def project_columns(T, M):
    """CORRECT frame projection: T_{hat a hat b} = M[mu,a] M[nu,b] T[mu,nu]."""
    out = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            s = sp.S.Zero
            for mu in range(4):
                for nu in range(4):
                    s += M[mu, a]*M[nu, b]*T[mu, nu]
            out[a, b] = s
    return out


def project_rows(T, M):
    """The SHIPPED (buggy) projection: rows contracted as if they were legs."""
    out = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            s = sp.S.Zero
            for mu in range(4):
                for nu in range(4):
                    s += M[a, mu]*M[b, nu]*T[mu, nu]
            out[a, b] = s
    return out


def route_A_constraints(br_hat, bt_hat):
    """Exact 3+1 route: rho_E and momentum density from the constraints.

    Unit lapse, flat slices, stationary => K_ij = (D_i beta_j + D_j beta_i)/2,
    16 pi rho_E = K^2 - K_ij K^ij  (R^(3) = 0),
    8 pi j_i    = D_j K^j_i - D_i K.
    """
    gam = sp.diag(1, r**2, r**2*sp.sin(th)**2)
    gam_inv = sp.diag(1, 1/r**2, 1/(r**2*sp.sin(th)**2))
    x3 = (r, th, ph)
    b_up = sp.Matrix([br_hat, bt_hat/r, 0])
    b_lo = gam * b_up

    Gam3 = [[[sp.S.Zero]*3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                s = sp.S.Zero
                for d in range(3):
                    s += gam_inv[a, d]*(sp.diff(gam[d, b], x3[c])
                                        + sp.diff(gam[d, c], x3[b])
                                        - sp.diff(gam[b, c], x3[d]))
                Gam3[a][b][c] = s / 2

    def cov_d(vi_lo, i, j):  # D_i v_j for a covariant 3-vector
        s = sp.diff(vi_lo[j], x3[i])
        for k in range(3):
            s -= Gam3[k][i][j]*vi_lo[k]
        return s

    K = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            K[i, j] = (cov_d(b_lo, i, j) + cov_d(b_lo, j, i)) / 2

    K_mix = gam_inv * K                      # K^i_j
    trK = sp.trace(K_mix)
    KK = sum((K_mix*K_mix)[i, i] for i in range(3))   # K^i_j K^j_i = K_ij K^ij
    rho = (trK**2 - KK) / PI16

    # momentum constraint: 8 pi j_i = D_j K^j_i - D_i trK
    j_lo = []
    for i in range(3):
        s = sp.S.Zero
        for jj in range(3):
            # D_j K^j_i  (mixed tensor divergence)
            s += sp.diff(K_mix[jj, i], x3[jj])
            for k in range(3):
                s += Gam3[jj][jj][k]*K_mix[k, i] - Gam3[k][jj][i]*K_mix[jj, k]
        j_lo.append((s - sp.diff(trK, x3[i])) / (8*sp.pi))
    # orthonormal components
    j_hat = (j_lo[0], j_lo[1]/r)
    return rho, j_hat, trK, K


FAMS = {
    "alcubierre":   dict(),
    "natario":      dict(),
    "irrotational": dict(),
    "freeform_j1":  dict(),
}


def family_shift(name, v, R0, sig, A1, k):
    f_alc = (sp.tanh(sig*(r + R0)) - sp.tanh(sig*(r - R0))) / (2*sp.tanh(sig*R0))
    f_nat = 1 - f_alc
    if name == "alcubierre":
        return v*f_alc*sp.cos(th), -v*f_alc*sp.sin(th)
    if name == "natario":
        return -v*f_nat*sp.cos(th), v*(f_nat + (r/2)*sp.diff(f_nat, r))*sp.sin(th)
    if name == "irrotational":
        # Numerically stable antiderivative. sympy's integrate() returns a
        # log(1 +- tanh(...)) form that overflows to -inf in float64 once
        # tanh saturates (|r - R0| >~ 19/sigma) -- the shipped module has the
        # same defect and its irrotational fractions were silently computed
        # on a sigma-dependent truncated domain (the finite mask absorbed the
        # infs).  Identity log(1+tanh(y)) = y - log(cosh(y)) shows sympy's
        # antiderivative equals the log-cosh form below EXACTLY (same
        # integration constant); log(cosh(x)) is float64-safe for |x| < 710,
        # which covers this harness's domain.
        def lch(x):
            return sp.log(sp.cosh(x))
        antider = r - (lch(sig*(r + R0)) - lch(sig*(r - R0))) / (2*sig*sp.tanh(sig*R0))
        g_irr = antider / r
        return -v*f_nat*sp.cos(th), v*g_irr*sp.sin(th)
    if name == "freeform_j1":
        j1 = sp.sin(k*r)/(k*r)**2 - sp.cos(k*r)/(k*r)
        return v*A1*j1*sp.cos(th), -v*A1*j1*sp.sin(th)
    raise ValueError(name)


def main():
    t0 = time.time()

    # =====================================================================
    print("=" * 78)
    print("GATE 1 -- frame audit (generic symbolic shift)")
    print("=" * 78)
    brf = sp.Function('br')(r, th)
    btf = sp.Function('bt')(r, th)
    g, g_inv, br_c, bt_c = build_4metric(brf, btf)
    M = tetrad_matrix(br_c, bt_c)
    eta = sp.diag(-1, 1, 1, 1)

    cols_ok = all(
        sp.simplify(sum(M[mu, a]*M[nu, b]*g[mu, nu]
                        for mu in range(4) for nu in range(4)) - eta[a, b]) == 0
        for a in range(4) for b in range(4)
    )
    gate("columns of the written matrix are an orthonormal tetrad", cols_ok)

    row_norms = [sp.simplify(sum(M[a, mu]*M[b, nu]*g[mu, nu]
                                 for mu in range(4) for nu in range(4)) - eta[a, b])
                 for (a, b) in ((0, 0), (1, 1), (2, 2), (0, 1))]
    rows_bad = any(x != 0 for x in row_norms)
    gate("rows are NOT orthonormal (the shipped contraction uses rows)", rows_bad,
         f"g(row0,row0)+1 = {sp.simplify(row_norms[0])}")

    # The shipped projection collapses to coordinate T_tt at [0,0]:
    # row 0 = (1,0,0,0) exactly, so T_o[0,0] = T[0,0] algebraically. (No gate
    # needed; verified numerically in GATE 3.)

    # =====================================================================
    print("=" * 78)
    print("GATE 4 -- generic analytic identities (profile-independent)")
    print("=" * 78)
    b_gen = sp.Function('b')(r)
    # z-directed shift: beta = b(r) zhat -> br_hat = b cos, bt_hat = -b sin
    rho_z, _, trK_z, _ = route_A_constraints(b_gen*sp.cos(th), -b_gen*sp.sin(th))
    ident = sp.simplify(rho_z + sp.diff(b_gen, r)**2 * sp.sin(th)**2 / (32*sp.pi))
    gate("z-shift identity rho_E = -b'(r)^2 sin^2(th)/(32 pi)  (<= 0 always)",
         ident == 0, f"residual = {ident}")

    F_gen = sp.Function('F')(r)
    br_n = -F_gen*sp.cos(th)
    bt_n = (F_gen + (r/2)*sp.diff(F_gen, r))*sp.sin(th)
    rho_n, _, trK_n, K_n = route_A_constraints(br_n, bt_n)
    gate("Natario construction has div(beta) == 0 for ANY profile F(r)",
         sp.simplify(trK_n) == 0)
    # trK == 0 => 16 pi rho = -K_ij K^ij <= 0: state, and spot-check numerically.
    rho_n_fn = sp.lambdify((r, th), rho_n.subs(F_gen, (1 - (sp.tanh(2*(r+5)) - sp.tanh(2*(r-5)))/(2*sp.tanh(sp.Integer(10))))).doit(), 'numpy')
    rs = np.linspace(0.3, 14.0, 60)
    ths = np.linspace(0.05, np.pi - 0.05, 50)
    Rg, Tg = np.meshgrid(rs, ths, indexing='ij')
    vals = rho_n_fn(Rg, Tg)
    gate("Natario rho_E <= 0 numerically on grid (v=1, R0=5, sig=2)",
         bool(np.nanmax(vals) <= 1e-18), f"max = {np.nanmax(vals):.3e}")

    # (iii) irrotational zero-integral identity: 16 pi rho = (Lap phi)^2 -
    # |Hess phi|^2 integrates to zero (by parts) when beta -> uniform flow
    # with exponentially decaying gradients, so WEC-everywhere => rho == 0.
    br_i, bt_i = family_shift("irrotational", 1, 5.0, 4.0, None, None)
    rho_i, _, _, _ = route_A_constraints(br_i, bt_i)
    f_i = sp.lambdify((r, th), rho_i, 'numpy')
    # fine quadrature; rho decays exponentially beyond the shell so r_max=25
    # captures the integral to float precision. Simpson (4th order) because
    # the signed integral is a fine cancellation; theta kept off the axis
    # (cot(theta) Christoffels are singular at exactly 0/pi, weight ~ theta^2
    # there so the excluded slivers are negligible).
    from scipy.integrate import simpson
    R_MAX = 25.0
    rq = np.linspace(1e-3, R_MAX, 4001)
    tq = np.linspace(1e-4, np.pi - 1e-4, 801)
    Rq, Tq = np.meshgrid(rq, tq, indexing='ij')
    w = Rq**2 * np.sin(Tq)
    vals_i = f_i(Rq, Tq)
    I_signed = 2*np.pi*simpson(simpson(vals_i * w, x=tq, axis=1), x=rq)
    I_abs = 2*np.pi*simpson(simpson(np.abs(vals_i) * w, x=tq, axis=1), x=rq)
    # analytic 1/r^4 dipole tail beyond R_MAX (v=1, R0=5, sigma=4)
    C_dip = 5.0 / np.tanh(4.0*5.0)
    I_tail = -C_dip**2 / (6.0*R_MAX)
    I_total = I_signed + I_tail
    gate("irrotational zero-integral identity Int rho dV == 0 "
         "(numeric interior + analytic dipole tail)",
         bool(abs(I_total) < 1e-3 * I_abs),
         f"interior = {I_signed:.4e}, tail = {I_tail:.4e}, "
         f"sum = {I_total:.3e}, Int |rho| dV = {I_abs:.3e}, "
         f"ratio = {abs(I_total)/I_abs:.2e}")

    # =====================================================================
    print("=" * 78)
    print("GATES 2+3 -- Route A vs Route B vs shipped pipeline, per family")
    print("=" * 78)
    print("(loading shipped pipeline -- builds 4 symbolic pipelines, ~1 min)")
    from hf_jobs.sweeps import shift_families as sf

    # validate the stable irrotational antiderivative against sympy integrate
    # on the safe (pre-overflow) part of the domain
    vv, rr0, ss = sp.symbols('v R0 sigma', positive=True)
    f_alc_chk = (sp.tanh(ss*(r + rr0)) - sp.tanh(ss*(r - rr0))) / (2*sp.tanh(ss*rr0))
    g_int = ((1/r)*sp.integrate(1 - f_alc_chk, r)).subs({rr0: 5.0, ss: 4.0})
    _, bt_stable = family_shift("irrotational", 1, 5.0, 4.0, None, None)
    g_stable = bt_stable / sp.sin(th)
    f_int = sp.lambdify(r, g_int, 'numpy')
    f_stb = sp.lambdify(r, g_stable, 'numpy')
    rs_safe = np.linspace(0.3, 8.0, 40)
    dstab = float(np.abs(f_int(rs_safe) - f_stb(rs_safe)).max()
                  / np.abs(f_int(rs_safe)).max())
    # tolerance is set by the REFERENCE form's own catastrophic cancellation
    # (1 - tanh(sigma(r-R0)) ~ 1e-11 near r = 8), not by the stable form
    gate("stable irrotational antiderivative == sympy integrate (safe domain)",
         dstab < 1e-6, f"max rel = {dstab:.2e}")

    v_n, R0_n, sig_n, A1_n, k_n = 0.1, 5.0, 4.0, 1.0, np.pi/10  # recorded single-point;
    # freeform at A1=1, k=pi/(2 R0) as in the NOTES single-point table
    sample_r = np.array([0.5, 2.1, 4.9, 5.6, 8.3, 12.7])
    sample_t = np.array([0.2, 0.7, 1.3, 1.9, 2.6])
    Rs, Ts = np.meshgrid(sample_r, sample_t, indexing='ij')

    corrected_rows = {}
    for name in ("alcubierre", "natario", "irrotational", "freeform_j1"):
        v, R0, sig = sp.symbols('v R0 sigma', positive=True)
        A1, k = sp.symbols('A1 k', positive=True)
        br_hat, bt_hat = family_shift(name, v, R0, sig, A1, k)
        subs = {v: v_n, A1: A1_n, k: k_n} if name == "freeform_j1" else \
               {v: v_n, R0: R0_n, sig: sig_n}
        br_s = br_hat.subs(subs).doit()
        bt_s = bt_hat.subs(subs).doit()

        # Route A
        rho_A, j_hat, _, _ = route_A_constraints(br_s, bt_s)
        fA = sp.lambdify((r, th), rho_A, 'numpy')

        # Route B: independent 4D Einstein tensor + CORRECT column projection
        gB, gB_inv, br_c, bt_c = build_4metric(br_s, bt_s)
        TB = einstein_T(gB, gB_inv)
        MB = tetrad_matrix(br_c, bt_c)
        T_hat = project_columns(TB, MB)
        fB = sp.lambdify((r, th), T_hat[0, 0], 'numpy')
        fB_flux_r = sp.lambdify((r, th), T_hat[0, 1], 'numpy')
        fA_flux_r = sp.lambdify((r, th), j_hat[0], 'numpy')

        # shipped pipeline
        pkg = sf._LAMBDAS[name]
        args = (Rs, Ts) + ((v_n, A1_n, k_n) if name == "freeform_j1"
                           else (v_n, R0_n, sig_n))
        with np.errstate(all='ignore'):
            # mirrors the module's evaluate(): rho_p = +Ttt after the
            # Session-36 fix (T_o[0,0] = T(n,n) = rho_E)
            rho_pipe = pkg["Ttt"](*args)
        fin_pipe = np.isfinite(rho_pipe)
        if not fin_pipe.all():
            print(f"    {name}: shipped lambdified NON-FINITE at "
                  f"{(~fin_pipe).sum()}/{fin_pipe.size} sample points "
                  f"(overflowing antiderivative; recorded fractions were "
                  f"computed on the truncated finite subset)")

        a = fA(Rs, Ts)
        b = fB(Rs, Ts)
        scl = np.abs(a).max()
        dAB = np.abs(a - b).max() / scl
        gate(f"{name}: Route A == Route B (rho_E)", dAB < 1e-8,
             f"max rel = {dAB:.2e}")

        # flux magnitudes agree up to sign convention
        fa = np.abs(fA_flux_r(Rs, Ts))
        fb = np.abs(fB_flux_r(Rs, Ts))
        if max(fa.max(), fb.max()) < 1e-10 * scl:
            # irrotational shifts on flat slices have j_i == 0 identically:
            # 8 pi j_i = D_j K^j_i - D_i K = [Delta, D_i] phi = R_ij D^j phi = 0
            # (flat 3-metric) -- both routes must return pure roundoff
            gate(f"{name}: momentum density vanishes identically "
                 f"(both routes < 1e-10 x rho scale)", True,
                 f"max|j| = {max(fa.max(), fb.max()):.2e}, rho scale = {scl:.2e}")
        else:
            dfl = np.abs(fa - fb).max() / fa.max()
            gate(f"{name}: |j_rhat| constraint == |T(n,e_r)| projection",
                 dfl < 1e-8, f"max rel = {dfl:.2e}")

        dpipe = np.abs(rho_pipe[fin_pipe] - a[fin_pipe]).max() / scl
        gate(f"{name}: sweep-module rho_p == rho_E and finite everywhere "
             f"(post-Session-36 fix)",
             bool(dpipe < 1e-8 and fin_pipe.all()),
             f"max rel = {dpipe:.2e}, non-finite = {(~fin_pipe).sum()}")

        # corrected single-point stats on the recorded preview grid geometry
        rs_g = np.linspace(0.1, 3.0*R0_n, 60)
        th_g = np.linspace(0.05, np.pi - 0.05, 50)
        Rg2, Tg2 = np.meshgrid(rs_g, th_g, indexing='ij')
        rho_c = fA(Rg2, Tg2)
        # full corrected DEC needs all components:
        comps = {}
        for lbl, (i, jx) in {"flux_r": (0, 1), "flux_t": (0, 2), "p_rr": (1, 1),
                             "p_tt": (2, 2), "p_pp": (3, 3)}.items():
            comps[lbl] = sp.lambdify((r, th), T_hat[i, jx], 'numpy')(Rg2, Tg2)
        flux = np.maximum(np.abs(comps["flux_r"]), np.abs(comps["flux_t"]))
        pmax = np.maximum.reduce([np.abs(comps["p_rr"]), np.abs(comps["p_tt"]),
                                  np.abs(comps["p_pp"])])
        slack = rho_c - np.maximum(flux, pmax)
        corrected_rows[name] = (
            float(np.mean(rho_c > 0)),
            float(np.mean((rho_c > 0) & (slack > 0))),
            float(np.nanmin(rho_c)),
            float(np.nanmin(slack)),
        )

    print()
    print("Corrected single-point table (v=0.1, R0=5, sigma=4; freeform A1=1, k=pi/10):")
    print(f"  {'family':<14} {'WEC frac':>9} {'DEC frac':>9} {'min rho_E':>12} {'min slack':>12}")
    for name, (wf, df, rm, sm) in corrected_rows.items():
        print(f"  {name:<14} {wf:>9.3f} {df:>9.3f} {rm:>12.3e} {sm:>12.3e}")
    print("  (recorded Session-9 table: alc 0.479/0.003, nat 0.696/0.020, "
          "irr 0.282/0.019, ff 0.473/0.000 -- wrong observable)")

    # =====================================================================
    print("=" * 78)
    print("GATE 5 -- Route A vs warp_factory_py anchored Eulerian density")
    print("=" * 78)
    from warp_factory_py.metrics.alcubierre import metric_alcubierre
    from warp_factory_py.solvers.evaluator import eval_metric

    VWF, RWF, SWF = 0.1, 4.0, 2.0
    NT, NX, NY, NZ = 1, 100, 100, 7
    DX = 0.2
    m = metric_alcubierre(
        (NT, NX, NY, NZ),
        ((NT+1)/2*0.001, (NX+1)/2*DX, (NY+1)/2*DX, (NZ+1)/2*DX),
        v=VWF, R=RWF, sigma=SWF, grid_scale=(0.001, DX, DX, DX),
    )
    res = eval_metric(m, num_angular=10, num_temporal=5)
    # warp_factory_py returns T_eul in SI units: T_SI = (c^4/8 pi G) G_munu
    # vs our geometric T = G_munu / 8 pi  =>  multiply by G/c^4.
    from warp_factory_py.utils.constants import G as G_SI, c as c_SI
    rho_wf = res.T_eul[0, 0][0, :, :, NZ//2] * (G_SI / c_SI**4)

    v, R0, sig = sp.symbols('v R0 sigma', positive=True)
    br_hat, bt_hat = family_shift("alcubierre", v, R0, sig, None, None)
    rho_A, _, _, _ = route_A_constraints(
        br_hat.subs({v: VWF, R0: RWF, sig: SWF}),
        bt_hat.subs({v: VWF, R0: RWF, sig: SWF}))
    fA = sp.lambdify((r, th), rho_A, 'numpy')

    xc = (np.arange(NX)+1)*DX - (NX+1)/2*DX
    yc = (np.arange(NY)+1)*DX - (NY+1)/2*DX
    Xg, Yg = np.meshgrid(xc, yc, indexing='ij')
    Rg = np.sqrt(Xg**2 + Yg**2)
    # motion axis in warp_factory is x; polar angle measured from it
    Tg = np.arccos(np.clip(np.where(Rg > 0, Xg/np.maximum(Rg, 1e-12), 1.0), -1, 1))
    interior = (Rg > 1.0) & (Rg < 8.0) & (np.abs(np.sin(Tg)) > 0.15)
    rho_ref = fA(Rg, Tg)

    num = rho_wf[interior]
    ref = rho_ref[interior]
    scl = np.abs(ref).max()
    med_rel = float(np.median(np.abs(num - ref)) / scl)
    max_rel = float(np.max(np.abs(num - ref)) / scl)
    corr = float(np.corrcoef(num, ref)[0, 1])
    gate("warp_factory_py T_eul[0,0] matches Route A rho_E (median rel < 5%)",
         med_rel < 0.05, f"median rel = {med_rel:.3e}, max rel = {max_rel:.3e}, corr = {corr:.5f}")

    # =====================================================================
    print("=" * 78)
    n_pass = sum(GATES.values())
    print(f"ADJUDICATION: {n_pass}/{len(GATES)} gates PASS "
          f"({time.time()-t0:.0f}s total)")
    for k_, v_ in GATES.items():
        if not v_:
            print(f"  FAILED: {k_}")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    raise SystemExit(main())

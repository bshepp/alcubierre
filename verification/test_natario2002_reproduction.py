# -*- coding: utf-8 -*-
"""Ground-truth reproduction battery for Natario 2002 (arXiv:gr-qc/0110086),
"Warp drive with zero expansion", CQG 19, 1157-1166 -- Session 56, Task 3.8.

The paper (i) defines the general warp-drive class ds^2 = -dt^2
+ sum_i (dx^i - X^i dt)^2 (flat Cauchy slices, unit lapse), (ii) proves
structural results: Eulerian observers are geodesic (Prop 1.3), K_ij is the
rate-of-strain tensor of X (Prop 1.4), theta = div X (Cor 1.5), flat wherever
X is Euclidean-Killing (Cor 1.6), and THEOREM 1.7: every non-flat warp drive
violates WEC or SEC (SEC forces theta == 0, then rho_E = -K_ij K^ij / 16pi <= 0
with equality iff K == 0); (iii) constructs the zero-expansion drive
X ~ -v(t) d[f(r) r^2 sin^2(theta) dphi] (a 2-form curl, hence divergenceless),
with explicit K_ij components and
rho = -(v^2/8pi) [ 3 f'^2 cos^2(theta) + (f' + (r/2) f'')^2 sin^2(theta) ];
(iv) Section 3 (v_s > 1 optics: Mach-cone horizon sin(alpha) = 1/|X|,
refraction, infinite blueshift) is OUTSIDE the subluminal slice -- noted in
NATARIO2002_EVALUATION.md, not reproduced here.

Gates (G = c = 1 throughout; f(r) an ARBITRARY smooth profile unless stated):
  1  [symbolic] The 2-form-curl construction: -v d[f r^2 sin^2(th) dphi] maps to
     X^rhat = -2 v f cos(th), X^thhat = v (2f + r f') sin(th); and div X == 0.
  2  [symbolic] All six spherical rate-of-strain components K_ab == paper list.
  3  [symbolic] theta = tr K == 0 (Cor 1.5); Alcubierre Example 1.8 in Cartesian:
     theta = v f'(rs) x/rs and rho = -(v^2/32pi) f'^2 (y^2+z^2)/rs^2.
  4  [symbolic] ADM Hamiltonian constraint rho_E = (theta^2 - K_ij K^ij)/16pi
     equals the paper's rho formula, arbitrary f.
  5  [random-pt, mpmath 40 dps] Full 4D Einstein tensor of the Natario metric,
     TIME-DEPENDENT v(t): G_mn n^m n^n / 8pi == paper rho at random spacetime
     points with v-dot != 0 -- the law is instantaneous (no v-dot dependence;
     same structure as the S49 spin-up result).
  6  [random-pt, mpmath 40 dps] Prop 1.3: nabla_n n == 0 (Eulerian observers
     geodesic) on the full 4D Natario metric with v(t).
  7  [symbolic] Theorem 1.7 / Cor 1.6 mechanics: f == const c gives K == 0
     identically and X = -2vc d/dx (a Euclidean Killing field -> flat).
  8  [symbolic + numeric] Repo tie + EC characterization: the paper family with
     f = (1 - f_Alc)/2 is EXACTLY the shift_families "natario" row (symbolic,
     instantiating the Session-36 identity-2 closure); numeric grid at
     (R0, sigma) = (5, 4): rho_E <= 0 everywhere and < 0 at EVERY wall point
     including the axis (no marginal directions, unlike Alcubierre); exact v^2
     scaling of rho_E; WEC violated at 100% of wall points.
  9  [numeric, B-grade anchors] Rodal 2025 (arXiv:2512.18008) Table-2 cross-
     checks at matched (rho, sigma) = (5, 4), v = 1: peak |rho_E| ratio
     Natario/Alcubierre ~ 67 (+-35%); peak NEC-violation ratio ~ 60 (+-45%);
     Natario has Hawking-Ellis Type IV pockets (present: yes).
 10  [symbolic + numeric] <d_t, d_t> = -1 + |X|^2 (so stationarity needs
     |X| < 1); the wall amplifies |X| above its asymptotic value v_s:
     sup|X|/v reported -> subluminal ergo-band threshold v* = 1/(sup|X|/v)
     for the canonical profile. Our sharpening; the paper only uses the
     asymptotic |X| = v_s.

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_natario2002_reproduction.py
Runtime ~5-10 min (two symbolic 4D Einstein builds + grids).
"""
import sys
import time
import warnings

import mpmath as mp
import numpy as np
import sympy as sp

warnings.filterwarnings("ignore", category=RuntimeWarning)
np.seterr(all="ignore")

T0 = time.time()
PASS = []


def gate(name, ok, detail=""):
    PASS.append(bool(ok))
    print(f"GATE {len(PASS)} [{'PASS' if ok else 'FAIL'}] {name}\n        {detail}  ({time.time()-T0:.0f}s)",
          flush=True)


# ----------------------------------------------------------------------------------
# shared symbols (spherical coords; the x/motion axis is the polar axis)
t, r, th, ph = sp.symbols("t r theta phi", real=True, positive=True)
v = sp.symbols("v", positive=True)
f = sp.Function("f")(r)
fp = sp.diff(f, r)
fpp = sp.diff(f, r, 2)

# Paper Section 2: orthonormal components of the zero-expansion shift
Xr_hat = -2 * v * f * sp.cos(th)
Xt_hat = v * (2 * f + r * fp) * sp.sin(th)

# Paper's Eulerian energy density
rho_paper = -(v**2 / (8 * sp.pi)) * (3 * fp**2 * sp.cos(th)**2
                                     + (fp + r * fpp / 2)**2 * sp.sin(th)**2)

# ----------------------------------------------------------------------------------
# GATE 1 -- the 2-form-curl construction and divergencelessness
# Natario: X ~ -v d[f r^2 sin^2(th) dphi] under the Hodge identifications
# e_r ~ r^2 sin(th) dth^dph,  e_th ~ -r sin(th) dr^dph,  e_ph ~ r dr^dth.
pot = f * r**2 * sp.sin(th)**2
c_dr_dph = sp.diff(pot, r)          # coefficient of dr^dph in d(pot dph)
c_dth_dph = sp.diff(pot, th)        # coefficient of dth^dph
Xr_from_form = -v * c_dth_dph / (r**2 * sp.sin(th))
Xt_from_form = v * c_dr_dph / (r * sp.sin(th))
ok_r = sp.simplify(Xr_from_form - Xr_hat) == 0
ok_t = sp.simplify(Xt_from_form - Xt_hat) == 0
Xr_c = Xr_hat                        # coordinate components (X^r, X^th = Xhat/r)
Xt_c = Xt_hat / r
divX = sp.simplify(sp.diff(r**2 * Xr_hat, r) / r**2
                   + sp.diff(sp.sin(th) * Xt_hat, th) / (r * sp.sin(th)))
gate("2-form curl -> paper's component formulas; div X == 0 (arbitrary f)",
     ok_r and ok_t and divX == 0, f"residuals: dXr==0 {ok_r}, dXth==0 {ok_t}, div = {divX}")

# ----------------------------------------------------------------------------------
# K_ij = (1/2) Lie_X h in coordinates, converted to the orthonormal frame
h = sp.diag(1, r**2, r**2 * sp.sin(th)**2)
SPH = [r, th, ph]
scale = [sp.Integer(1), r, r * sp.sin(th)]


def rate_of_strain_hat(Xc):
    K = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            K[i, j] = sp.Rational(1, 2) * (
                sum(Xc[k] * sp.diff(h[i, j], SPH[k]) for k in range(3))
                + sum(h[k, j] * sp.diff(Xc[k], SPH[i]) for k in range(3))
                + sum(h[i, k] * sp.diff(Xc[k], SPH[j]) for k in range(3)))
    return sp.Matrix(3, 3, lambda i, j: sp.simplify(K[i, j] / (scale[i] * scale[j])))


K_hat = rate_of_strain_hat([Xr_c, Xt_c, sp.Integer(0)])

# GATE 2 -- the paper's six components
K_paper = sp.Matrix([
    [-2 * v * fp * sp.cos(th), v * sp.sin(th) * (fp + r * fpp / 2), 0],
    [v * sp.sin(th) * (fp + r * fpp / 2), v * fp * sp.cos(th), 0],
    [0, 0, v * fp * sp.cos(th)],
])
dK = sp.simplify(K_hat - K_paper)
gate("all six K_ab rate-of-strain components == paper (arbitrary f)",
     dK == sp.zeros(3, 3), "exact" if dK == sp.zeros(3, 3) else f"residual: {dK.tolist()}")

# GATE 3 -- zero trace (Cor 1.5) + Alcubierre Example 1.8, arbitrary f
# (spherical coords about the motion axis, t = 0 bubble at origin:
#  X = v f(r) d/dx  ->  Xr_hat = v f cos(th), Xth_hat = -v f sin(th);
#  paper: theta = v f' (x-xs)/rs = v f' cos(th);
#  rho = -(v^2/32pi) f'^2 (y^2+z^2)/rs^2 = -(v^2/32pi) f'^2 sin^2(th).)
trK = sp.simplify(sum(K_hat[i, i] for i in range(3)))
K_alc_ex = rate_of_strain_hat([v * f * sp.cos(th), -v * f * sp.sin(th) / r, sp.Integer(0)])
theta_alc = sp.simplify(sum(K_alc_ex[i, i] for i in range(3)))
theta_paper_alc = v * fp * sp.cos(th)
rho_alc_ex = (theta_alc**2
              - sum(K_alc_ex[i, j]**2 for i in range(3) for j in range(3))) / (16 * sp.pi)
rho_paper_alc = -(v**2 / (32 * sp.pi)) * fp**2 * sp.sin(th)**2
ok3 = (trK == 0
       and sp.simplify(theta_alc - theta_paper_alc) == 0
       and sp.simplify(rho_alc_ex - rho_paper_alc) == 0)
gate("tr K == 0 (zero expansion); Example 1.8 theta and rho (Alcubierre, arbitrary f)",
     ok3, f"trK = {trK}")

# GATE 4 -- Hamiltonian-constraint rho_E == paper formula (arbitrary f)
K2 = sum(K_hat[i, j]**2 for i in range(3) for j in range(3))
rho_ham = (trK**2 - K2) / (16 * sp.pi)
gate("Hamiltonian constraint rho_E == paper rho (arbitrary f)",
     sp.simplify(rho_ham - rho_paper) == 0, "exact")

# ----------------------------------------------------------------------------------
# generic 4D Einstein builder for a lapse-1 axisymmetric spherical ADM metric
coords4 = [t, r, th, ph]


def build_einstein_spherical(Xr_hat_e, Xt_hat_e):
    """4D metric ds^2 = -dt^2 + h_ij (dx^i - X^i dt)(dx^j - X^j dt) with
    orthonormal shift components (Xr_hat_e, Xt_hat_e) possibly time-dependent.
    Returns (g, ginv, Gam, G4, n_up, tetrad)."""
    Xc_ = [Xr_hat_e, Xt_hat_e / r, sp.Integer(0)]
    g_ = sp.zeros(4, 4)
    g_[0, 0] = -1 + Xr_hat_e**2 + Xt_hat_e**2
    for i in range(3):
        g_[0, i + 1] = -h[i, i] * Xc_[i]
        g_[i + 1, 0] = g_[0, i + 1]
        g_[i + 1, i + 1] = h[i, i]
    hinv = sp.diag(1, 1 / r**2, 1 / (r**2 * sp.sin(th)**2))
    ginv_ = sp.zeros(4, 4)
    ginv_[0, 0] = -1
    for i in range(3):
        ginv_[0, i + 1] = -Xc_[i]
        ginv_[i + 1, 0] = -Xc_[i]
        for j in range(3):
            ginv_[i + 1, j + 1] = hinv[i, j] - Xc_[i] * Xc_[j]
    assert sp.simplify(g_ * ginv_ - sp.eye(4)) == sp.zeros(4, 4)
    dg = [[[sp.diff(g_[a, b], coords4[c]) for c in range(4)] for b in range(4)] for a in range(4)]
    Gam_ = [[[sp.together(sum(ginv_[a, d] * (dg[d][b][c] + dg[d][c][b] - dg[b][c][d])
                              for d in range(4)) / 2)
              for c in range(4)] for b in range(4)] for a in range(4)]
    Ric = sp.zeros(4, 4)
    for b in range(4):
        for c in range(b, 4):
            e = (sum(sp.diff(Gam_[a][b][c], coords4[a]) for a in range(4))
                 - sum(sp.diff(Gam_[a][b][a], coords4[c]) for a in range(4))
                 + sum(Gam_[a][a][d] * Gam_[d][b][c] for a in range(4) for d in range(4))
                 - sum(Gam_[a][c][d] * Gam_[d][b][a] for a in range(4) for d in range(4)))
            Ric[b, c] = e
            Ric[c, b] = e
    Rs = sum(ginv_[a, b] * Ric[a, b] for a in range(4) for b in range(4))
    G4_ = Ric - g_ * Rs / 2
    n_up_ = [sp.Integer(1), Xc_[0], Xc_[1], Xc_[2]]
    tetrad_ = [n_up_,
               [sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(0)],
               [sp.Integer(0), sp.Integer(0), 1 / r, sp.Integer(0)],
               [sp.Integer(0), sp.Integer(0), sp.Integer(0), 1 / (r * sp.sin(th))]]
    return g_, ginv_, Gam_, G4_, n_up_, tetrad_


vt = sp.Function("v")(t)
print("building 4D Einstein tensor #1 (Natario, v(t), arbitrary f)...", flush=True)
gN, ginvN, GamN, G4N, nupN, tetN = build_einstein_spherical(Xr_hat.subs(v, vt),
                                                            Xt_hat.subs(v, vt))
print(f"  done ({time.time()-T0:.0f}s)", flush=True)

rho_G = sum(G4N[a, b] * nupN[a] * nupN[b] for a in range(4) for b in range(4)) / (8 * sp.pi)
rho_paper_t = rho_paper.subs(v, vt)

# random-point certification (mpmath, 40 dps): substitute concrete smooth f, v(t)
mp.mp.dps = 40
F_CHOICES = [sp.Rational(1, 2) * (1 - sp.exp(-(r / sp.Rational(21, 10))**2)),
             sp.Rational(1, 2) * sp.tanh(r / 3)**2 + sp.Rational(3, 100) * r * sp.exp(-r)]
V_CONC = sp.Rational(1, 10) * (2 + sp.sin(sp.Rational(37, 10) * t))


def certify_zero(expr, tol=1e-25, npts=5, seed=7):
    rng = np.random.default_rng(seed)
    worst = mp.mpf(0)
    for f_conc in F_CHOICES:
        e = expr.subs(f, f_conc).subs(vt, V_CONC).doit()
        fn = sp.lambdify((t, r, th), e, modules="mpmath")
        for _ in range(npts):
            tv = mp.mpf(float(rng.uniform(0, 3)))
            rv = mp.mpf(float(rng.uniform(0.4, 6.0)))
            thv = mp.mpf(float(rng.uniform(0.25, np.pi - 0.25)))
            worst = max(worst, abs(fn(tv, rv, thv)))
    return worst < tol, float(worst)


# GATE 5 -- full-4D rho == paper rho, with v(t) (instantaneous; no v-dot)
ok5, worst5 = certify_zero(rho_G - rho_paper_t)
gate("full 4D G_nn/8pi == paper rho with v(t) (v-dot present in metric, absent in rho)",
     ok5, f"worst |residual| over 10 random spacetime points = {worst5:.2e} (40-digit arithmetic)")

# GATE 6 -- Prop 1.3: Eulerian observers geodesic, time-dependent v
ok6_all, worst6 = True, 0.0
for a in range(4):
    acc = (sum(nupN[b] * sp.diff(nupN[a], coords4[b]) for b in range(4))
           + sum(GamN[a][b][c] * nupN[b] * nupN[c] for b in range(4) for c in range(4)))
    okc, w = certify_zero(acc)
    ok6_all = ok6_all and okc
    worst6 = max(worst6, w)
gate("Prop 1.3: nabla_n n == 0 (Eulerian geodesic, time-dependent v)",
     ok6_all, f"worst |acc^a| = {worst6:.2e}")

# GATE 7 -- Cor 1.6 / Thm 1.7 equality case: f == const -> K == 0, X = const boost
c = sp.symbols("c", real=True)
K_flat = K_hat.subs(f, c).doit()
K_flat = sp.Matrix(3, 3, lambda i, j: sp.simplify(K_flat[i, j]))
is_const_boost = (sp.simplify(Xr_hat.subs(f, c) + 2 * v * c * sp.cos(th)) == 0
                  and sp.simplify(Xt_hat.subs(f, c).doit() - 2 * v * c * sp.sin(th)) == 0)
gate("Thm 1.7 equality case: f == const -> K == 0 identically; X = -2vc d/dx (Killing -> flat)",
     K_flat == sp.zeros(3, 3) and is_const_boost, f"K(f=c) all-zero: {K_flat == sp.zeros(3, 3)}")

# ----------------------------------------------------------------------------------
# GATE 8 -- repo tie (shift_families natario row) + numeric EC characterization
R0n, sgn = 5, 4  # canonical comparison cell (Rodal 2025 Table 2 parameters)
R0s, sigs = sp.symbols("R_0 sigma_0", positive=True)
f_alc = (sp.tanh(sigs * (r + R0s)) - sp.tanh(sigs * (r - R0s))) / (2 * sp.tanh(sigs * R0s))
f_nat_paper = (1 - f_alc) / 2

f_nat_repo = 1 - f_alc                    # shift_families convention (2x the paper's f)
br_repo = -v * f_nat_repo * sp.cos(th)
bt_repo = v * (f_nat_repo + (r / 2) * sp.diff(f_nat_repo, r)) * sp.sin(th)
Xr_sub = Xr_hat.subs(f, f_nat_paper).doit()
Xt_sub = Xt_hat.subs(f, f_nat_paper).doit()
ok8a = (sp.simplify(Xr_sub - br_repo) == 0 and sp.simplify(Xt_sub - bt_repo) == 0)

print("lambdifying Eulerian-frame T for the canonical profile (Natario)...", flush=True)
CONC = {R0s: R0n, sigs: sgn}


def frame_T_lambdified(G4_, tet_, fsub):
    T = []
    for a in range(4):
        row = []
        for b in range(4):
            if b < a:
                row.append(None)
                continue
            e = sum(G4_[m, nn] * tet_[a][m] * tet_[b][nn]
                    for m in range(4) for nn in range(4)) / (8 * sp.pi)
            e = e.subs(f, fsub).subs(vt, v).doit().subs(CONC)
            row.append(sp.lambdify((r, th, v), e, "numpy"))
        T.append(row)
    return T


TN = frame_T_lambdified(G4N, tetN, f_nat_paper)

rg = np.linspace(0.25, 12.0, 240)
tg = np.linspace(0.02, np.pi - 0.02, 121)
RG, TG = np.meshgrid(rg, tg, indexing="ij")


def T_grid(Tlam, vval):
    out = np.zeros(RG.shape + (4, 4))
    for a in range(4):
        for b in range(a, 4):
            val = np.broadcast_to(np.asarray(Tlam[a][b](RG, TG, vval), dtype=float), RG.shape)
            out[..., a, b] = val
            out[..., b, a] = val
    return out


TgN1 = T_grid(TN, 0.1)
TgN2 = T_grid(TN, 0.2)
rhoN1 = TgN1[..., 0, 0]
rhoN2 = TgN2[..., 0, 0]
scaleN = np.abs(rhoN1).max()
ok8b = rhoN1.max() <= 1e-10 * scaleN
ratio_v2 = rhoN2.min() / rhoN1.min()
ok8c = abs(ratio_v2 - 4.0) < 1e-9

wall = np.abs(rhoN1) > 1e-6 * scaleN
wec_wall_frac = float((rhoN1[wall] < 0).mean())
# on-axis strictness: smallest |rho| along near-axis wall column
axis_band = (np.abs(TG - tg[0]) < 1e-9) & wall
axis_strict = float(np.max(rhoN1[axis_band])) < 0 if axis_band.any() else False


def he_census(Tg, wall_mask, scale_):
    """Hawking-Ellis census + principal-pressure EC slacks on wall points."""
    eta = np.diag([-1.0, 1, 1, 1])
    pts = np.argwhere(wall_mask)
    n_t4, n_t1, n_deg = 0, 0, 0
    nec_min, dec_min, sec_min = np.inf, np.inf, np.inf
    for (i, j) in pts:
        M = eta @ Tg[i, j]
        w, V = np.linalg.eig(M)
        if np.abs(w.imag).max() > 1e-10 * scale_:
            n_t4 += 1
            continue
        w = w.real
        V = V.real
        norms = np.einsum("ia,ab,ib->i", V.T, eta, V.T)
        tl = np.where(norms < -1e-9)[0]
        if len(tl) != 1:
            n_deg += 1
            continue
        n_t1 += 1
        lam_t = w[tl[0]]
        prs = np.delete(w, tl[0])
        rho_p = -lam_t
        nec_min = min(nec_min, (rho_p + prs).min())
        dec_min = min(dec_min, rho_p - np.abs(prs).max())
        sec_min = min(sec_min, min((rho_p + prs).min(), rho_p + prs.sum()))
    ntot = len(pts)
    return dict(frac_t4=n_t4 / ntot, frac_t1=n_t1 / ntot, frac_deg=n_deg / ntot,
                nec_min=nec_min, dec_min=dec_min, sec_min=sec_min, n=ntot)


censN = he_census(TgN1, wall, scaleN)
gate("repo tie (paper f=(1-f_Alc)/2 == shift_families natario row); rho_E<=0; "
     "rho_E<0 at 100% of wall incl. axis; exact v^2 scaling",
     ok8a and ok8b and ok8c and wec_wall_frac == 1.0 and axis_strict,
     f"max rho_E = {rhoN1.max():.2e} (scale {scaleN:.2e}); v^2 ratio = {ratio_v2:.12f}; "
     f"wall WEC-viol frac = {wec_wall_frac:.3f}; axis strict: {axis_strict}; "
     f"HE census (v=0.1): TypeI {censN['frac_t1']:.3f} / TypeIV {censN['frac_t4']:.3f} "
     f"/ degenerate {censN['frac_deg']:.3f}; NEC/DEC/SEC min slack "
     f"{censN['nec_min']:.2e}/{censN['dec_min']:.2e}/{censN['sec_min']:.2e}")

# ----------------------------------------------------------------------------------
# GATE 9 -- Rodal 2025 Table-2 anchors at matched (rho, sigma) = (5, 4), v = 1
print("building 4D Einstein tensor #2 (Alcubierre comoving, arbitrary b)...", flush=True)
b_f = sp.Function("b")(r)
Xr_alc = -vt * (1 - b_f) * sp.cos(th)
Xt_alc = vt * (1 - b_f) * sp.sin(th)
gA, ginvA, GamA, G4A, nupA, tetA = build_einstein_spherical(Xr_alc, Xt_alc)
print(f"  done ({time.time()-T0:.0f}s)", flush=True)


def frame_T_lambdified_alc(G4_, tet_):
    T = []
    for a in range(4):
        row = []
        for bb in range(4):
            if bb < a:
                row.append(None)
                continue
            e = sum(G4_[m, nn] * tet_[a][m] * tet_[bb][nn]
                    for m in range(4) for nn in range(4)) / (8 * sp.pi)
            e = e.subs(b_f, f_alc).subs(vt, v).doit().subs(CONC)
            row.append(sp.lambdify((r, th, v), e, "numpy"))
        T.append(row)
    return T


TA = frame_T_lambdified_alc(G4A, tetA)
TgA = T_grid(TA, 1.0)
TgN_v1 = T_grid(TN, 1.0)
rhoA = TgA[..., 0, 0]
rhoN_v1 = TgN_v1[..., 0, 0]
scaleA = np.abs(rhoA).max()
wallA = np.abs(rhoA) > 1e-6 * scaleA
wallN1 = np.abs(rhoN_v1) > 1e-6 * np.abs(rhoN_v1).max()
censA = he_census(TgA, wallA, scaleA)
censN1 = he_census(TgN_v1, wallN1, np.abs(rhoN_v1).max())
ratio_rho = rhoN_v1.min() / rhoA.min()
ratio_nec = censN1["nec_min"] / censA["nec_min"]
ok9 = (abs(ratio_rho - 67) / 67 < 0.35
       and abs(ratio_nec - 60) / 60 < 0.45
       and censN1["frac_t4"] > 0)
gate("Rodal 2025 anchors (v=1): |rho_E| ratio Nat/Alc ~ 67; NEC ratio ~ 60; Nat Type IV present",
     ok9, f"rho ratio = {ratio_rho:.1f} (target ~67); NEC ratio = {ratio_nec:.1f} (target ~60); "
     f"Nat TypeIV frac (v=1) = {censN1['frac_t4']:.3f}; Alc TypeIV frac = {censA['frac_t4']:.3f}")

# ----------------------------------------------------------------------------------
# GATE 10 -- stationarity bound and the wall ergo-band sharpening
g00_ok = sp.simplify(gN[0, 0] - (-1 + Xr_hat.subs(v, vt)**2 + Xt_hat.subs(v, vt)**2)) == 0
Xnorm = sp.sqrt(Xr_hat**2 + Xt_hat**2).subs(f, f_nat_paper).doit().subs(CONC)
Xn_fn = sp.lambdify((r, th, v), Xnorm, "numpy")
Xn = Xn_fn(RG, TG, 0.1)
amp = float(np.nanmax(Xn) / 0.1)
gate("<d_t,d_t> = -1 + |X|^2 (symbolic); wall amplification of |X| (our sharpening)",
     g00_ok and amp > 1.0,
     f"sup|X|/v = {amp:.2f} at (R0,sigma)=({R0n},{sgn}) -> ergo-band threshold v* = {1.0/amp:.3f} "
     f"(paper Sec. 3 uses the asymptotic bound v* = 1)")

# ----------------------------------------------------------------------------------
n_pass = sum(PASS)
print(f"\n{'ALL GATES PASS' if all(PASS) else 'FAILURES PRESENT'}: {n_pass}/{len(PASS)}  "
      f"({time.time()-T0:.0f}s total)")
sys.exit(0 if all(PASS) else 1)

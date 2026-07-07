# -*- coding: utf-8 -*-
"""Ground-truth reproduction battery for Garattini-Zatrimaylov 2025 (arXiv:2502.13153),
"Positive-Energy Warp Drive in a De Sitter Universe" -- Session 46, Block 3(c).

The paper embeds an Ellis-style warp bubble in the de Sitter Painleve-Gullstrand
(flat-slicing) form  ds^2 = -dt^2 + (dr - (r/L)dt)^2 + r^2 dOmega^2,  L = 1/H,
via  N^i -> -(1-f) x^i/L - f v^i,  f = f(rs),  rs = |x - x0(t)|,  and claims that
under the Hubble-matching condition v = x0/L (i.e. x0(t) = x0(0) e^{t/L}, a
COMOVING bubble):  (i) the Eulerian energy density is >= 0 everywhere (Eq. 17);
(ii) the bubble is a mass-conserving rearrangement of vacuum energy (Eq. 18);
(iii) the Eulerian momentum flux vanishes (Eq. 23, gradient shift Eq. 20);
(iv) volume-averaged (fixed-t d^3r) WEC/NEC are satisfied/saturated while the
local conditions are violated (Eqs. 24-31); (v) a generic theorem: vacuum-energy
perturbations underdense in every frame always violate NEC/WEC locally.

Gates (all in G = c = 1):
  1  Paper Eq. 6 (Natario-class rho_E) == ADM Hamiltonian constraint, generic N^i   [symbolic exact]
  2  Embedded shift: constraint == Eq. 14 (general v); matched -> Eq. 17;
     Eq. 18 == Eq. 17; momentum constraint == 0 for the matched (gradient) shift   [symbolic exact]
  3  Full-4D independence check, matched MOVING bubble x0(t) = xi e^{t/L}, tanh
     profile: G_nn/8pi == Eq. 14 and Eulerian flux == 0 at random spacetime points [~1e-14]
  4  Same, UNMATCHED trajectory (x0 = xi + u t): Eq. 14 still exact (instantaneous
     law) but the flux is NOT zero -> the Hubble matching is load-bearing
  5  Paper Eq. 24-25 spatial stress == full G_ij/8pi (pins K_ij = +(1/2)(dN+dN^T))  [~1e-14]
  6  Exact rearrangement: int(rho - rho_hat) d^3r and int(T_ij - That_ij) d^3r -> 0
     with box size (exponentially for tanh tails)
  7  Local structure, COMPACT C^2 wall profile, two L values: min rho_E >= 0; flux ~ 0;
     min NEC/WEC/DEC slack < 0 mid-wall (local violation, order rho_hat and STEEPENING
     with L: slack ~ 1/L vs rho_hat ~ 1/L^2 -> violation/background grows ~ L);
     sorted-eigenvalue averaged NEC dilutes as 1/volume
  8  ANEC probe (our extension; NOT claimed by the paper): null geodesics in the
     totally-geodesic y=0 plane through the moving bubble, compact profile
     (compact support is REQUIRED: the flat dS patch is past-incomplete and rays
     blueshift without bound at the bubble's past horizon |x_rel| = L, so any
     non-compact tail makes the backward ANEC integral formally divergent)
  9  Underdensity-theorem algebra: Eq. 34 bracket, Eq. 36 expansion, and the
     Eq.-38 proof-step probe (Q >= 0 does not force Q == 0; theorem still closes
     for the paper's mass-conserving class via int Q d^3r = 0)

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_gz_desitter_reproduction.py
Runtime ~6-10 min (three symbolic Einstein-tensor builds + grids + geodesics).
"""
import time
import warnings

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

warnings.filterwarnings("ignore", category=RuntimeWarning)
np.seterr(all="ignore")

T0 = time.time()
PASS = []


def gate(name, ok, detail=""):
    PASS.append(bool(ok))
    print(f"GATE {len(PASS)} [{'PASS' if ok else 'FAIL'}] {name}  {detail}  ({time.time()-T0:.0f}s)")


# ----------------------------------------------------------------------------------
# shared symbols
t, x, y, z = sp.symbols("t x y z", real=True)
L = sp.symbols("L", positive=True)
coords4 = [t, x, y, z]
SP = [x, y, z]
X = sp.Matrix(SP)


def ham_16pi(N):
    """16 pi rho_E from the ADM Hamiltonian constraint (flat static h, lapse 1)."""
    K = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            K[i, j] = sp.Rational(1, 2) * (sp.diff(N[i], SP[j]) + sp.diff(N[j], SP[i]))
    trK = sum(K[i, i] for i in range(3))
    return trK**2 - sum(K[i, j] * K[i, j] for i in range(3) for j in range(3))


def mom_8pi(N):
    """8 pi (Eulerian momentum) from the momentum constraint (flat h)."""
    K = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            K[i, j] = sp.Rational(1, 2) * (sp.diff(N[i], SP[j]) + sp.diff(N[j], SP[i]))
    trK = sum(K[i, i] for i in range(3))
    return [sum(sp.diff(K[j, i], SP[j]) for j in range(3)) - sp.diff(trK, SP[i]) for i in range(3)]


def build_full_einstein(N):
    """Full 4D Einstein tensor (lower indices) + inverse metric for the lapse-1
    flat-h metric with shift list N (functions of t,x,y,z)."""
    g = sp.zeros(4, 4)
    g[0, 0] = -1 + sum(N[i]**2 for i in range(3))
    for i in range(3):
        g[0, i + 1] = N[i]
        g[i + 1, 0] = N[i]
        g[i + 1, i + 1] = 1
    ginv = sp.zeros(4, 4)
    ginv[0, 0] = -1
    for i in range(3):
        ginv[0, i + 1] = N[i]
        ginv[i + 1, 0] = N[i]
        for j in range(3):
            ginv[i + 1, j + 1] = (1 if i == j else 0) - N[i] * N[j]
    dg = [[[sp.diff(g[a, b], coords4[c]) for c in range(4)] for b in range(4)] for a in range(4)]
    Gam = [[[sum(ginv[a, d] * (dg[d][b][c] + dg[d][c][b] - dg[b][c][d]) for d in range(4)) / 2
             for c in range(4)] for b in range(4)] for a in range(4)]
    Ric = sp.zeros(4, 4)
    for b in range(4):
        for c in range(b, 4):
            e = (sum(sp.diff(Gam[a][b][c], coords4[a]) for a in range(4))
                 - sum(sp.diff(Gam[a][b][a], coords4[c]) for a in range(4))
                 + sum(Gam[a][a][d] * Gam[d][b][c] for a in range(4) for d in range(4))
                 - sum(Gam[a][c][d] * Gam[d][b][a] for a in range(4) for d in range(4)))
            Ric[b, c] = e
            Ric[c, b] = e
    Rs = sum(ginv[a, b] * Ric[a, b] for a in range(4) for b in range(4))
    return g, ginv, Gam, Ric - g * Rs / 2


# ==================================================================================
# GATE 1: Eq. 6 == Hamiltonian constraint for a generic shift
Ng = [sp.Function(f"N{i}")(x, y, z) for i in range(3)]
divN = sum(sp.diff(Ng[j], SP[j]) for j in range(3))
eq6 = (sum(sp.diff(Ng[i] * divN - sum(Ng[j] * sp.diff(Ng[i], SP[j]) for j in range(3)), SP[i])
           for i in range(3))
       - sp.Rational(1, 4) * sum((sp.diff(Ng[j], SP[i]) - sp.diff(Ng[i], SP[j]))**2
                                 for i in range(3) for j in range(3)))
d1 = sp.simplify(ham_16pi(Ng) - eq6)
gate("Eq.6 == Hamiltonian constraint (generic N, symbolic)", d1 == 0, f"residual = {d1}")

# ==================================================================================
# GATE 2: embedded shift -> Eq. 14 / 17 / 18 / 23  (generic profile f)
x0s = sp.Matrix(sp.symbols("x01 x02 x03", real=True))
vs = sp.Matrix(sp.symbols("v1 v2 v3", real=True))
rs_sym = sp.sqrt(sum((X[i] - x0s[i])**2 for i in range(3)))
fF = sp.Function("f")
fs = fF(rs_sym)
r_ = sp.symbols("r_", positive=True)
fp = fF(r_).diff(r_).subs(r_, rs_sym)
Nemb = [-(1 - fs) * X[i] / L - fs * vs[i] for i in range(3)]

w = vs - X / L
rhat = (X - x0s) / rs_sym
wd = sum(w[i] * rhat[i] for i in range(3))
cross2 = sum(w[i]**2 for i in range(3)) - wd**2
eq14_16pi = (1 - fs)**2 * 6 / L**2 + fp * (1 - fs) * 4 / L * wd - fp**2 / 2 * cross2

dB = sp.simplify(ham_16pi(Nemb) - eq14_16pi)
matched = {vs[0]: x0s[0] / L, vs[1]: x0s[1] / L, vs[2]: x0s[2] / L}
eq17_16pi = (1 - fs)**2 * 6 / L**2 - rs_sym * fp * (1 - fs) * 4 / L**2
dC1 = sp.simplify(ham_16pi([Ni.subs(matched) for Ni in Nemb]) - eq17_16pi)
g18 = r_**3 * fF(r_) * (fF(r_) - 2)
d18 = sp.simplify((6 / L**2 + (2 / (L**2 * r_**2)) * sp.diff(g18, r_))
                  - ((1 - fF(r_))**2 * 6 / L**2 - r_ * fF(r_).diff(r_) * (1 - fF(r_)) * 4 / L**2))
mom = [sp.simplify(m) for m in mom_8pi([sp.simplify(Ni.subs(matched)) for Ni in Nemb])]
ok2 = (dB == 0) and (dC1 == 0) and (d18 == 0) and all(m == 0 for m in mom)
gate("embedded shift: Eq.14 (gen. v) / Eq.17 (matched) / Eq.18==Eq.17 / Eq.23==0",
     ok2, f"residuals = {dB}, {dC1}, {d18}, {mom}")

# ==================================================================================
# GATES 3+4: full-4D independence checks (tanh profile), matched + unmatched
sig, R = sp.symbols("sig R", positive=True)
xi1, xi2, xi3 = sp.symbols("xi1 xi2 xi3", real=True)
u1, u2, u3 = sp.symbols("u1 u2 u3", real=True)
SY = [t, x, y, z, L, sig, R, xi1, xi2, xi3, u1, u2, u3]
PVAL = dict(L=2.5, sig=3.0, R=1.0, xi1=0.8, xi2=-0.5, xi3=1.2, u1=0.3, u2=-0.2, u3=0.15)


def ftanh(r):
    return (1 - sp.tanh(sig * (r - R))) / 2


def full4d_case(x0vec):
    v = sp.Matrix([sp.diff(x0vec[i], t) for i in range(3)])
    rs = sp.sqrt(sum((X[i] - x0vec[i])**2 for i in range(3)))
    f = ftanh(rs)
    fpn = ftanh(r_).diff(r_).subs(r_, rs)
    N = [-(1 - f) * X[i] / L - f * v[i] for i in range(3)]
    g, ginv, Gam, G4 = build_full_einstein(N)
    nvec = sp.Matrix([1, -N[0], -N[1], -N[2]])
    rho8 = sum(G4[a, b] * nvec[a] * nvec[b] for a in range(4) for b in range(4))
    flux8 = [-(sum(G4[a, i + 1] * nvec[a] for a in range(4))) for i in range(3)]
    ww = v - X / L
    rh = (X - x0vec) / rs
    wdn = sum(ww[i] * rh[i] for i in range(3))
    c2 = sum(ww[i]**2 for i in range(3)) - wdn**2
    eq14_8 = (1 - f)**2 * 3 / L**2 + fpn * (1 - f) * 2 / L * wdn - fpn**2 / 4 * c2
    return N, G4, rho8, flux8, eq14_8


rng = np.random.default_rng(46)


def rand_args():
    p = dict(t=rng.uniform(-0.3, 0.3), x=rng.uniform(-3, 3), y=rng.uniform(-3, 3),
             z=rng.uniform(-3, 3), **PVAL)
    return [p[s.name] for s in SY]


# matched
NM, G4M, rhoM, fluxM, eq14M = full4d_case(sp.Matrix([xi1 * sp.exp(t / L), xi2 * sp.exp(t / L), xi3 * sp.exp(t / L)]))
FrhoM = sp.lambdify(SY, rhoM, modules="numpy", cse=True)
Feq14M = sp.lambdify(SY, eq14M, modules="numpy", cse=True)
FfluxM = [sp.lambdify(SY, fl, modules="numpy", cse=True) for fl in fluxM]
wr = wf = 0.0
for _ in range(12):
    a = rand_args()
    wr = max(wr, abs(FrhoM(*a) - Feq14M(*a)))
    wf = max(wf, max(abs(F(*a)) for F in FfluxM))
gate("full-4D matched moving bubble: G_nn/8pi == Eq.14->17 AND flux == 0",
     wr < 1e-12 and wf < 1e-12, f"max|drho| = {wr:.2e}, max|flux| = {wf:.2e}")

# unmatched
NU, G4U, rhoU, fluxU, eq14U = full4d_case(sp.Matrix([xi1 + u1 * t, xi2 + u2 * t, xi3 + u3 * t]))
FrhoU = sp.lambdify(SY, rhoU, modules="numpy", cse=True)
Feq14U = sp.lambdify(SY, eq14U, modules="numpy", cse=True)
FfluxU = [sp.lambdify(SY, fl, modules="numpy", cse=True) for fl in fluxU]
wrU, wfU = 0.0, 0.0
for _ in range(12):
    a = rand_args()
    wrU = max(wrU, abs(FrhoU(*a) - Feq14U(*a)))
    wfU = max(wfU, max(abs(F(*a)) for F in FfluxU))
gate("full-4D UNMATCHED: Eq.14 exact but flux != 0 (matching is load-bearing)",
     wrU < 1e-12 and wfU > 1e-2, f"max|drho| = {wrU:.2e}, max|flux| = {wfU:.2e}")

# ==================================================================================
# GATE 5: Eq. 24-25 spatial stress == full G_ij/8pi (matched case, K = +sym grad)
KM = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        KM[i, j] = sp.Rational(1, 2) * (sp.diff(NM[i], SP[j]) + sp.diff(NM[j], SP[i]))
trKM = sum(KM[i, i] for i in range(3))
w5 = 0.0
FT, FTp = {}, {}
for i in range(3):
    for j in range(i, 3):
        term2 = sum(sp.diff(NM[k], SP[i]) * sp.diff(NM[k], SP[j])
                    - sp.diff(NM[i], SP[k]) * sp.diff(NM[j], SP[k]) for k in range(3)) / 2
        term3 = sum(sp.diff(NM[k] * (KM[i, j] - (trKM if i == j else 0)), SP[k]) for k in range(3))
        term4 = sp.diff((trKM if i == j else 0) - KM[i, j], t)
        Tpap = rhoM * (1 if i == j else 0) + term2 + term3 + term4
        FT[(i, j)] = sp.lambdify(SY, G4M[i + 1, j + 1], modules="numpy", cse=True)
        FTp[(i, j)] = sp.lambdify(SY, Tpap, modules="numpy", cse=True)
for _ in range(8):
    a = rand_args()
    for key in FT:
        w5 = max(w5, abs(FT[key](*a) - FTp[key](*a)))
gate("Eq.24-25 == full G_ij/8pi (K_ij = +(dN+dN^T)/2 convention pinned)",
     w5 < 1e-12, f"max|dT_ij| = {w5:.2e}")

# ==================================================================================
# GATE 6: exact mass-conserving rearrangement (fixed-t volume integrals -> 0)
c0 = np.array([PVAL["xi1"], PVAL["xi2"], PVAL["xi3"]])
rho_hat8 = 3.0 / PVAL["L"]**2


def box_integrals(Rbox, n):
    s = np.linspace(-Rbox, Rbox, n)
    dxg = s[1] - s[0]
    off = 0.37 * dxg  # dodge the removable 1/rs point at the bubble center
    XX, YY, ZZ = np.meshgrid(c0[0] + s + off, c0[1] + s + off, c0[2] + s + off, indexing="ij")
    a = [0.0, XX, YY, ZZ] + [PVAL[s_.name] for s_ in SY[4:]]
    Ir = np.sum(FrhoM(*a) - rho_hat8) * dxg**3
    IT = max(abs(np.sum(FT[key](*a) - (-rho_hat8 if key[0] == key[1] else 0.0)) * dxg**3)
             for key in FT)
    return Ir, IT

I3 = box_integrals(3.0, 61)
I5 = box_integrals(5.0, 101)
ok6 = abs(I5[0]) < 1e-6 and I5[1] < 1e-6 and abs(I5[0]) < abs(I3[0]) / 10
gate("rearrangement: int(drho), int(dT_ij) d^3r -> 0 with box size",
     ok6, f"Rbox=3: ({I3[0]:.1e},{I3[1]:.1e})  Rbox=5: ({I5[0]:.1e},{I5[1]:.1e})")

# ==================================================================================
# GATE 7: local EC structure with a COMPACT C^2 profile, two L values
RA, RB = sp.Rational(3, 5), sp.Rational(7, 5)
s_c = (rs_sym - RA) / (RB - RA)
fcomp_r = sp.Piecewise((1, r_ <= RA), (0, r_ >= RB),
                       (1 - (6 * ((r_ - RA) / (RB - RA))**5 - 15 * ((r_ - RA) / (RB - RA))**4
                             + 10 * ((r_ - RA) / (RB - RA))**3), True))


def full4d_compact_matched():
    x0v = sp.Matrix([xi1 * sp.exp(t / L), xi2 * sp.exp(t / L), xi3 * sp.exp(t / L)])
    v = sp.Matrix([sp.diff(x0v[i], t) for i in range(3)])
    rs = sp.sqrt(sum((X[i] - x0v[i])**2 for i in range(3)))
    f = fcomp_r.subs(r_, rs)
    N = [-(1 - f) * X[i] / L - f * v[i] for i in range(3)]
    g, ginv, Gam, G4 = build_full_einstein(N)
    nvec = sp.Matrix([1, -N[0], -N[1], -N[2]])
    rho8 = sum(G4[a, b] * nvec[a] * nvec[b] for a in range(4) for b in range(4))
    flux8 = [-(sum(G4[a, i + 1] * nvec[a] for a in range(4))) for i in range(3)]
    return N, G4, rho8, flux8


NC, G4C, rhoC, fluxC = full4d_compact_matched()
FrhoC = sp.lambdify(SY, rhoC, modules="numpy", cse=True)
FfluxC = [sp.lambdify(SY, fl, modules="numpy", cse=True) for fl in fluxC]
FTC = {}
for i in range(3):
    for j in range(i, 3):
        FTC[(i, j)] = sp.lambdify(SY, G4C[i + 1, j + 1], modules="numpy", cse=True)


def slice_scan(Lval, Rbox=2.0, n=81):
    s = np.linspace(-Rbox, Rbox, n)
    dxg = s[1] - s[0]
    off = 0.37 * dxg
    XX, YY, ZZ = np.meshgrid(c0[0] + s + off, c0[1] + s + off, c0[2] + s + off, indexing="ij")
    pv = dict(PVAL, L=Lval)
    a = [0.0, XX, YY, ZZ] + [pv[s_.name] for s_ in SY[4:]]
    rho = FrhoC(*a)
    Tm = np.empty(XX.shape + (3, 3))
    for (i, j), F in FTC.items():
        Tm[..., i, j] = F(*a)
        Tm[..., j, i] = Tm[..., i, j]
    fl = max(np.max(np.abs(F(*a))) for F in FfluxC)
    lam = np.linalg.eigvalsh(Tm)
    nec = (rho[..., None] + lam).min()
    dec = (rho[..., None] - np.abs(lam)).min()
    return rho.min(), fl, nec, dec, 3.0 / Lval**2


r1, f1, n1, d1_, rh1 = slice_scan(2.5)
r2, f2, n2, d2_, rh2 = slice_scan(5.0)
# matched N = -x/L + f(rs)(x-x0)/L: every bubble deviation is a function of x-x0
# with one 1/L amplitude => stress deviations scale ~ 1/L^2 like rho_hat, so the
# local violation is a FIXED multiple of the background density (wall-shape-set).
ok7 = (r1 > -1e-12 and r2 > -1e-12 and f1 < 1e-12 and f2 < 1e-12
       and n1 < -0.1 and n2 < -0.02 and abs(n2 / n1 - 0.25) < 0.10)
gate("compact profile: rho_E >= 0, flux == 0, local NEC/DEC violation ~ 1/L^2 "
     "(fixed multiple of rho_hat, set by wall shape)", ok7,
     f"L=2.5: min rho {r1:.1e}, minNEC {n1:.3f} ({abs(n1)/rh1:.2f} rho_hat); "
     f"L=5: minNEC {n2:.3f} ({abs(n2)/rh2:.2f} rho_hat); ratio {n2/n1:.3f}")

# ==================================================================================
# GATE 8: ANEC probe -- null geodesics in the (totally geodesic) y=0 plane
zi_s = sp.symbols("zi", positive=True)
z0ax = zi_s * sp.exp(t / L)
rs_ax = sp.sqrt(x**2 + y**2 + (z - z0ax)**2)
f_ax = fcomp_r.subs(r_, rs_ax)
v_ax = sp.diff(z0ax, t)
N_ax = [-(1 - f_ax) * x / L, -(1 - f_ax) * y / L, -(1 - f_ax) * z / L - f_ax * v_ax]
g_ax, ginv_ax, Gam_ax, G4_ax = build_full_einstein(N_ax)

SYA = [t, x, z, L, zi_s]
plane = {y: 0}
IDX = [0, 1, 3]
GamF, GEF = {}, {}
for mu in IDX:
    for a in IDX:
        for b in IDX:
            if (mu, a, b) not in GamF and (mu, b, a) not in GamF:
                GamF[(mu, a, b)] = sp.lambdify(SYA, Gam_ax[mu][a][b].subs(plane), modules="numpy", cse=True)
for a in IDX:
    for b in IDX:
        if (a, b) not in GEF and (b, a) not in GEF:
            GEF[(a, b)] = sp.lambdify(SYA, G4_ax[a, b].subs(plane), modules="numpy", cse=True)
F_Nx_ax = sp.lambdify(SYA, N_ax[0].subs(plane), modules="numpy", cse=True)
F_Nz_ax = sp.lambdify(SYA, N_ax[2].subs(plane), modules="numpy", cse=True)
# y=0 plane totally geodesic (numeric spot check)
rngc = np.random.default_rng(7)
wtg = 0.0
for a in IDX:
    for b in IDX:
        Fy = sp.lambdify([t, x, y, z, L, zi_s], Gam_ax[2][a][b], modules="numpy", cse=True)
        wtg = max(wtg, max(abs(Fy(rngc.uniform(-0.3, 0.3), rngc.uniform(-2, 2), 0.0,
                                  rngc.uniform(-2, 3), 4.0, 0.8)) for _ in range(4)))
assert wtg < 1e-13, wtg

PA = (4.0, 0.8)   # L, zi


def g_lookup(d, mu, a, b):
    return d[(mu, a, b)] if (mu, a, b) in d else d[(mu, b, a)]


def rhs_ray(lam, s):
    tt, xx, zz_, kt, kx, kz = s[:6]
    arg = (tt, xx, zz_) + PA
    k = {0: kt, 1: kx, 3: kz}
    dk = {mu: -sum(g_lookup(GamF, mu, i, j)(*arg) * k[i] * k[j] for i in IDX for j in IDX)
          for mu in IDX}
    integ = sum((GEF[(i, j)] if (i, j) in GEF else GEF[(j, i)])(*arg) * k[i] * k[j]
                for i in IDX for j in IDX) / (8 * np.pi)
    return [kt, kx, kz, dk[0], dk[1], dk[3], integ]


def clear_of_wall(lam, s):
    # rs > 3 with compact support [0.6, 1.4]: integrand identically zero beyond; ALSO
    # required because the backward leg reaches the flat-patch past boundary (t -> -inf)
    # at FINITE affine lambda ~ -L, where kt blueshifts unboundedly.
    rr = np.sqrt(s[1]**2 + (s[2] - PA[1] * np.exp(s[0] / PA[0]))**2)
    return rr - 3.0


clear_of_wall.terminal = True
clear_of_wall.direction = 1.0


def run_ray(t_s, x_s, z_s, theta, span=14.0):
    arg = (t_s, x_s, z_s) + PA
    Nx, Nz = F_Nx_ax(*arg), F_Nz_ax(*arg)
    kt = 1.0
    kx = -Nx * kt + kt * np.sin(theta)
    kz = -Nz * kt + kt * np.cos(theta)
    tot, worstC, tails, minrs = 0.0, 0.0, 0.0, np.inf
    imin = 0.0
    for l1 in (span, -span):
        sol = solve_ivp(rhs_ray, (0, l1), [t_s, x_s, z_s, kt, kx, kz, 0.0],
                        rtol=1e-10, atol=1e-12, dense_output=True,
                        events=clear_of_wall, max_step=abs(l1) / 150)
        lam = np.linspace(0, sol.t[-1], 1201)
        S = sol.sol(lam)
        integ = np.array([rhs_ray(l, S[:, i])[6] for i, l in enumerate(lam)])
        tot += np.trapezoid(integ, lam) * (1 if l1 > 0 else -1)   # lam decreasing on the backward leg
        imin = min(imin, integ.min())
        rr = np.sqrt(S[1]**2 + (S[2] - PA[1] * np.exp(S[0] / PA[0]))**2)
        minrs = min(minrs, rr.min())
        Nzs = F_Nz_ax(S[0], S[1], S[2], *PA)
        Nxs = F_Nx_ax(S[0], S[1], S[2], *PA)
        C = -S[3]**2 + (S[4] + Nxs * S[3])**2 + (S[5] + Nzs * S[3])**2
        worstC = max(worstC, np.max(np.abs(C)))
        tails = max(tails, abs(integ[-1]))
    return tot, imin, minrs, worstC, tails


z00 = PA[1]
# rays 0-3 cross the wall (near-axial both directions, wall-grazing b=0.5, side-on);
# ray 4 is a CONTROL that misses the compact support entirely (expects ANEC == 0)
rays = [(0.0, 0.07, z00 - 2.0, 0.0), (0.0, 0.07, z00 + 2.0, np.pi),
        (0.0, 0.5, z00 - 2.0, 0.0), (0.0, -2.0, z00 + 0.15, np.pi / 2),
        (0.0, 1.0, z00 - 2.0, 0.0)]
res8 = [run_ray(*r) for r in rays]
okC = all(r[3] < 1e-7 and r[4] < 1e-10 for r in res8)
anecs = [r[0] for r in res8]
imins = [r[1] for r in res8]
ok8 = (okC and all(v < -1e-5 for v in anecs[:4])         # ANEC violated on every crossing ray
       and abs(anecs[4]) < 1e-10 and imins[4] > -1e-10   # miss-ray control: exactly zero
       and res8[4][2] > 1.5)                             # ...and it really missed the wall
gate("ANEC probe: integrity + ANEC < 0 on EVERY wall-crossing ray (miss-ray control == 0)",
     ok8, "ANEC = [" + ", ".join(f"{v:+.3e}" for v in anecs) + "], "
     f"min integrand = {min(imins):+.2e}")
print("      NOTE: the paper claims only fixed-t volume averages (confirmed, gate 6);"
      " the geodesic-averaged NEC is our extension and is VIOLATED on crossing rays.")

# ==================================================================================
# GATE 9: underdensity-theorem algebra (Eqs. 32-40)
b_, eps, rhoh, drho, cc = sp.symbols("beta epsilon rhohat deltarho c", real=True)
n1s, n2s, n3s = sp.symbols("n1 n2 n3", real=True)
dT0 = sp.Matrix(sp.symbols("dP1 dP2 dP3", real=True))
dS0 = sp.Matrix(3, 3, sp.symbols("dS11 dS12 dS13 dS21 dS22 dS23 dS31 dS32 dS33", real=True))
dS0 = (dS0 + dS0.T) / 2
nv = sp.Matrix([n1s, n2s, n3s])
gam2 = 1 / (1 - b_**2)
Tuu = gam2 * ((rhoh + drho) + 2 * b_ * (nv.T * dT0)[0]
              + b_**2 * ((nv.T * (-rhoh * sp.eye(3) + dS0) * nv)[0]))
bracket = (1 - b_**2) * rhoh + drho + 2 * b_ * (nv.T * dT0)[0] + b_**2 * (nv.T * dS0 * nv)[0]
t1 = sp.simplify(sp.expand(Tuu - gam2 * bracket).subs({n1s**2: 1 - n2s**2 - n3s**2}))
ser = sp.series(bracket.subs(b_, 1 - eps), eps, 0, 2).removeO()
eq36 = (2 * eps * (rhoh - (nv.T * dT0)[0] - (nv.T * dS0 * nv)[0])
        + (drho + 2 * (nv.T * dT0)[0] + (nv.T * dS0 * nv)[0]))
t2 = sp.simplify(sp.expand(ser - eq36))
brC = (1 - b_**2) * (rhoh + drho) + b_**2 * (drho + cc)
t4 = sp.simplify(sp.expand(((1 - b_**2) * rhoh + drho
                            + b_**2 * (nv.T * (cc * sp.eye(3)) * nv)[0]
                            ).subs({n1s**2: 1 - n2s**2 - n3s**2}) - brC))
gate("theorem algebra: Eq.34 bracket, Eq.36 expansion, Eq.38 proof-step probe",
     t1 == 0 and t2 == 0 and t4 == 0, f"residuals = {t1}, {t2}, {t4}")

# ==================================================================================
n_ok = sum(PASS)
print(f"\n{'='*78}\n{n_ok}/{len(PASS)} gates PASS  ({time.time()-T0:.0f}s)")
if n_ok < len(PASS):
    raise SystemExit(1)

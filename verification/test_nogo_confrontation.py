# -*- coding: utf-8 -*-
"""Phase-4 no-go confrontation battery -- Session 57, Tasks 4.1-4.4.

Verifies, through this repo's own machinery, the checkable mathematical content
of the four no-go works the ROADMAP Phase 4 names, and instantiates their
central arguments on the canonical Alcubierre profile. The paper-by-paper
premise mapping and dispositions live in NOGO_CONFRONTATION.md; this battery
is the A-grade substrate for that document.

Papers:
  [SSV]  Santiago, Schuster & Visser 2021 (arXiv:2105.03079v2), "Generic warp
         drives violate the null energy condition" -- papers/2105.03079v2.pdf
  [PF]   Pfenning & Ford 1997 (gr-qc/9702026), "The unphysical nature of
         'Warp Drive'" -- papers/pfenning_ford1997_warp_qi_9702026.pdf
  [ER]   Everett & Roman 1997 (gr-qc/9702049), "A superluminal subway: the
         Krasnikov tube" -- papers/9702049v1.pdf  (carries the two-structure
         CTC mechanism of Everett 1996, PRD 53, 7365, which has no arXiv copy)
  [H]    Hiscock 1997 (gr-qc/9707024), "Quantum effects in the Alcubierre
         warp drive spacetime" -- papers/hiscock1997_quantum_alcubierre_9707024.pdf

Gates (G = c = 1; generic == undefined sympy functions):
  1  [symbolic] SSV Eq 4.3 == 4.4 == 4.5 (Eulerian density as 3-divergence +
     negative-semidefinite vorticity term), generic 3-flow v_i(t,x,y,z).
  2  [symbolic] SSV Eq 4.7 flux identity: (K_ij,j - K,i)/8pi ==
     (lap v_i - grad_i div v)/16pi, generic flow; the Eq 4.8 curl-curl form
     has the OPPOSITE sign (curl curl v = grad div v - lap v) -- recorded.
  3  [random-pt 1e-9] SSV Eqs 4.12 & 4.13 (rho + 3 pbar and rho + pbar in
     terms of L_n K, K^2, tr K^2) against the full 4D Einstein tensor of the
     generic-flow metric, random smooth time-dependent flows.
  4  [symbolic] Alcubierre-Lobo identity G_zz == 3 G_nn for any static
     z-directed flow v = v(x,y,z) zhat (the NEC kill SSV Sec 7.1 leans on:
     rho + T_zz = 4 rho <= 0).
  5  [numeric ODE] SSV Sec 7.4 / PF Sec 2 instantiation, canonical Alcubierre
     tanh (R=3, sigma=1, v_b=0.5, impact rho=2): an Eulerian observer overtaken
     by the bubble (a) reaches max coordinate speed v_b f(rho) at closest
     approach and is released at rest, displaced forward (PF Eq 7 passage
     phenomenology, the premise SSV's restoration argument borrows); (b) the
     NEC obligation dK/dtau <= -(3/2) tr([K^tf]^2) (SSV 7.34) is MEASURABLY
     violated on the trajectory; (c) the SEC obligation dK/dtau <= -K^2/3
     (SSV 7.23) is violated as well.  Localizes where: the rear-wall crossing.
  6  [symbolic] PF Eq 8 energy density == this repo's identity 1 (S36/S56).
  7  [symbolic] PF total-energy chain: Eq 26 E = -(v^2/12) int r^2 f'^2 dr
     (angular factor exact); Eq 28 closed form -(v^2/12)(R^2/Delta + Delta/12)
     for the piecewise wall; Eq 5 Delta(sigma) slope-matching relation and its
     large-sigma-R limit 2/sigma.
  8  [symbolic+numeric] PF QI arithmetic: Eq 16 contour integral (exact);
     Eq 22 -> Eq 23 wall bound Delta <= (3/4) sqrt(3/pi) v/alpha^2 L_P
     (= 73.3 v L_P at alpha = 1/10, quoted as 10^2); Eq 29 total energy at
     R = 100 m: E ~ -6.2e65 v_b grams (reproduced within 12%); Eq 31 ratio
     ~ -3e20 M_galaxy v_b.  (The Ford-Roman QI premise itself is EXTERNAL,
     grade B, and its scope is contested by Krasnikov 2003 -- Slice 4.)
  9  [symbolic] Hiscock chain: Eq 7 axis reduction of the Alcubierre metric;
     Eqs 9-10 static form (line-element equality) with A = 1 - v0^2 (1-f)^2;
     R_2D == -A'' for ds^2 = -A dtau^2 + dr^2/A; the anomaly-fixed RSET
     Eqs 21-22 satisfies 2D conservation with trace R/24pi; near-horizon
     Eq 24 leading term == -(f')^2/48pi [f - (1 - 1/v0)]^{-2}; Eq 25
     T_Hawking == v0 f'(r0)/2pi.
 10  [symbolic+numeric] Subluminal gating and its axis-blindness: A(r) >=
     1 - v0^2 > 0 for all f in [0,1] (no horizon, RSET finite -- the whole
     subluminal slice is Hiscock-safe); BUT for the Natario zero-expansion
     drive the S56 wall ergo-band (sup|X| = 5.53 v at (5,4)) lies OFF-AXIS:
     on the axis |X| = 2 v f <= v, so a Hiscock-style axis reduction sees no
     stationary-limit structure at any v < 1 while the equator crosses
     |X| = 1 at v* ~ 0.18.  Measured here.
 11  [symbolic] Everett-Roman Krasnikov-metric algebra: factored form Eq 4/5;
     light-cone branches dt/dx = 1, -k; interior transformation Eqs 8-9 gives
     exactly Minkowski for k = delta - 1; Eq 10 dt/dt' relation; Eq 11
     instantaneous-return slope -delta/(2-delta), in (-1, 0) for delta in (0,1).
 12  [arithmetic] Causality bookkeeping: single tube returns the ship at
     t_E = D delta > 0 (no CTC; matches Krasnikov's 2D no-CTC claim);
     the two-tube itinerary (Everett 1996's two-bubble pattern) closes a loop
     to t ~ 0 < departure 2D with every leg future-directed in its local
     cone -- the tachyonic-antitelephone assembly, which our subluminal
     discipline never enters.

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_nogo_confrontation.py
Runtime ~2-4 min.
"""
import sys
import time
import warnings

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

warnings.filterwarnings("ignore", category=RuntimeWarning)
np.seterr(all="ignore")

T0 = time.time()
PASS = []


def gate(name, ok, detail=""):
    PASS.append(bool(ok))
    print(f"GATE {len(PASS)} [{'PASS' if ok else 'FAIL'}] {name}\n        {detail}  ({time.time()-T0:.0f}s)",
          flush=True)


t, x, y, z = sp.symbols("t x y z", real=True)
SPC = [x, y, z]

# generic time-dependent 3-flow
V = [sp.Function(f"v{i}")(t, x, y, z) for i in range(3)]


def Kmat(flow):
    return sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2)
                     * (sp.diff(flow[i], SPC[j]) + sp.diff(flow[j], SPC[i])))


# ----------------------------------------------------------------------------------
# GATE 1 -- SSV 4.3 == 4.4 == 4.5
K = Kmat(V)
trK = sum(K[i, i] for i in range(3))
rho_43 = trK**2 - sum(K[i, j]**2 for i in range(3) for j in range(3))   # 16 pi rho
div_term = sum(sp.diff(V[i] * sp.diff(V[j], SPC[j]) - V[j] * sp.diff(V[i], SPC[j]), SPC[i])
               for i in range(3) for j in range(3))
asym2 = sum((sp.Rational(1, 2) * (sp.diff(V[i], SPC[j]) - sp.diff(V[j], SPC[i])))**2
            for i in range(3) for j in range(3))
rho_44 = div_term - asym2
omega = [sp.diff(V[2], y) - sp.diff(V[1], z),
         sp.diff(V[0], z) - sp.diff(V[2], x),
         sp.diff(V[1], x) - sp.diff(V[0], y)]
rho_45 = div_term - sp.Rational(1, 2) * sum(w**2 for w in omega)
ok1 = (sp.simplify(sp.expand(rho_43 - rho_44)) == 0
       and sp.simplify(sp.expand(rho_44 - rho_45)) == 0)
gate("SSV Eq 4.3 == 4.4 == 4.5 (density = divergence + vorticity), generic flow", ok1, "exact")

# ----------------------------------------------------------------------------------
# GATE 2 -- SSV 4.7 flux; 4.8 sign convention pinned
flux_adm = [sum(sp.diff(K[i, j], SPC[j]) for j in range(3)) - sp.diff(trK, SPC[i])
            for i in range(3)]                                            # 8 pi f_i
lap = lambda h: sum(sp.diff(h, s, 2) for s in SPC)
flux_47 = [sp.Rational(1, 2) * (lap(V[i]) - sp.diff(sum(sp.diff(V[j], SPC[j]) for j in range(3)),
                                                    SPC[i])) for i in range(3)]
curlcurl = [sp.diff(sum(sp.diff(V[j], SPC[j]) for j in range(3)), SPC[i]) - lap(V[i])
            for i in range(3)]
ok2a = all(sp.simplify(sp.expand(flux_adm[i] - flux_47[i])) == 0 for i in range(3))
ok2b = all(sp.simplify(sp.expand(flux_47[i] + sp.Rational(1, 2) * curlcurl[i])) == 0
           for i in range(3))
gate("SSV Eq 4.7 flux == (lap v - grad div v)/2 per 8pi f_i; Eq 4.8 curl-curl form is opposite-signed",
     ok2a and ok2b, "4.7 exact; curl curl v == grad div v - lap v pinned (4.8 sign convention noted)")

# ----------------------------------------------------------------------------------
# GATE 3 -- SSV 4.12 / 4.13 vs full 4D Einstein, random flows
def build_einstein_flow(flow):
    """4D Einstein for ds^2 = -dt^2 + sum (dx^i - v^i dt)^2 (SSV Eq 2.1/2.2)."""
    c4 = [t, x, y, z]
    g = sp.zeros(4, 4)
    g[0, 0] = -1 + sum(f_**2 for f_ in flow)
    for i in range(3):
        g[0, i + 1] = -flow[i]
        g[i + 1, 0] = -flow[i]
        g[i + 1, i + 1] = 1
    ginv = sp.zeros(4, 4)
    ginv[0, 0] = -1
    for i in range(3):
        ginv[0, i + 1] = -flow[i]
        ginv[i + 1, 0] = -flow[i]
        for j in range(3):
            ginv[i + 1, j + 1] = (1 if i == j else 0) - flow[i] * flow[j]
    dg = [[[sp.diff(g[a, b], c4[c]) for c in range(4)] for b in range(4)] for a in range(4)]
    Gam = [[[sum(ginv[a, d] * (dg[d][b][c] + dg[d][c][b] - dg[b][c][d]) for d in range(4)) / 2
             for c in range(4)] for b in range(4)] for a in range(4)]
    Ric = sp.zeros(4, 4)
    for b in range(4):
        for c in range(b, 4):
            e = (sum(sp.diff(Gam[a][b][c], c4[a]) for a in range(4))
                 - sum(sp.diff(Gam[a][b][a], c4[c]) for a in range(4))
                 + sum(Gam[a][a][d] * Gam[d][b][c] for a in range(4) for d in range(4))
                 - sum(Gam[a][c][d] * Gam[d][b][a] for a in range(4) for d in range(4)))
            Ric[b, c] = e
            Ric[c, b] = e
    Rs = sum(ginv[a, b] * Ric[a, b] for a in range(4) for b in range(4))
    return g, ginv, Gam, Ric - g * Rs / 2


FLOWS = [
    [sp.Rational(3, 10) * sp.exp(-((x - t / 2)**2 + y**2 + z**2) / 4),
     sp.Rational(1, 5) * sp.sin(x / 2) * sp.exp(-(y**2 + z**2 + x**2) / 5) * sp.cos(t / 3),
     sp.Rational(1, 10) * x * y * sp.exp(-(x**2 + y**2 + z**2) / 3)],
    [sp.Rational(1, 4) * sp.cos(y / 2) * sp.exp(-(x**2 + z**2) / 6),
     sp.Rational(1, 7) * z * sp.exp(-(x**2 + y**2 + z**2) / 4) * sp.cos(t / 3),
     sp.Rational(2, 9) * sp.exp(-((z - t / 3)**2 + x**2 + y**2) / 5)],
]

print("building concrete-flow 4D Einstein tensors for SSV 4.12/4.13...", flush=True)
w3a = w3b = 0.0
rng3 = np.random.default_rng(11)
for flow in FLOWS:
    gC, ginvC, GamC, G4C = build_einstein_flow(list(flow))
    nC = [sp.Integer(1)] + list(flow)
    rho_C = sum(G4C[a, b] * nC[a] * nC[b] for a in range(4) for b in range(4))   # 8 pi rho
    pbar_C = sum(G4C[i + 1, i + 1] for i in range(3)) / 3                        # 8 pi pbar
    KC = Kmat(list(flow))
    trKC = sum(KC[i, i] for i in range(3))
    trK2C = sum(KC[i, j]**2 for i in range(3) for j in range(3))
    LnKC = sp.diff(trKC, t) + sum(flow[i] * sp.diff(trKC, SPC[i]) for i in range(3))
    # SSV 4.12: rho + 3 pbar = -(LnK + trK2)/4pi ; 4.13: rho + pbar = (-2LnK + K^2 - 3trK2)/24pi
    e412 = (rho_C + 3 * pbar_C) / (8 * sp.pi) + (LnKC + trK2C) / (4 * sp.pi)
    e413 = (rho_C + pbar_C) / (8 * sp.pi) - (-2 * LnKC + trKC**2 - 3 * trK2C) / (24 * sp.pi)
    f412 = sp.lambdify((t, x, y, z), e412, "numpy")
    f413 = sp.lambdify((t, x, y, z), e413, "numpy")
    for _ in range(8):
        pt = rng3.uniform(-2, 2, 4)
        w3a = max(w3a, abs(float(f412(*pt))))
        w3b = max(w3b, abs(float(f413(*pt))))
ok3a, ok3b = w3a < 1e-10, w3b < 1e-10
gate("SSV Eqs 4.12 & 4.13 vs full 4D Einstein (two concrete time-dependent flows)",
     ok3a and ok3b, f"worst residuals {w3a:.2e} / {w3b:.2e} (float64)")

# ----------------------------------------------------------------------------------
# GATE 4 -- Alcubierre-Lobo identity for static z-directed flow
vz = sp.Function("v")(t, x, y, z)
flowZ = [sp.Integer(0), sp.Integer(0), vz]
gZ, ginvZ, GamZ, G4Z = build_einstein_flow(flowZ)
nZ = [sp.Integer(1), 0, 0, vz]
Gnn = sum(G4Z[a, b] * nZ[a] * nZ[b] for a in range(4) for b in range(4))
Gzz = G4Z[3, 3]
ok4 = sp.simplify(sp.expand(Gzz - 3 * Gnn)) == 0
gate("Alcubierre-Lobo identity G_zz == 3 G_nn (any z-directed flow, incl. time-dependent) -> rho + T_zz = 4 rho",
     ok4, "exact")

# ----------------------------------------------------------------------------------
# GATE 5 -- passage phenomenology + NEC/SEC obligations on the trajectory
Rb, sig, vb, rho_imp = 3.0, 1.0, 0.5, 2.0
r_s = sp.sqrt((x - vb * t)**2 + rho_imp**2)
f_alc = (sp.tanh(sig * (r_s + Rb)) - sp.tanh(sig * (r_s - Rb))) / (2 * sp.tanh(sig * Rb))
vfield = vb * f_alc                                     # x-directed flow at y = rho_imp, z = 0
K_xx = sp.diff(vfield, x)
K_trace = K_xx                                          # div v = d_x v here
# tr(K^2) for x-directed flow v(x, y-slice): use full 3D derivatives of v(x,y,z,t)
yv = sp.symbols("yv", real=True)
r_s3 = sp.sqrt((x - vb * t)**2 + yv**2 + z**2)
f3 = (sp.tanh(sig * (r_s3 + Rb)) - sp.tanh(sig * (r_s3 - Rb))) / (2 * sp.tanh(sig * Rb))
v3 = vb * f3
K2_3 = (sp.diff(v3, x)**2 + sp.Rational(1, 2) * sp.diff(v3, yv)**2
        + sp.Rational(1, 2) * sp.diff(v3, z)**2)
K_3 = sp.diff(v3, x)
Ktf2_3 = K2_3 - K_3**2 / 3
dK_dt = sp.diff(K_3, t)
dK_dx = sp.diff(K_3, x)

F_v = sp.lambdify((t, x), vfield, "numpy")
F_K = sp.lambdify((t, x, yv, z), K_3, "numpy")
F_dKdt = sp.lambdify((t, x, yv, z), dK_dt, "numpy")
F_dKdx = sp.lambdify((t, x, yv, z), dK_dx, "numpy")
F_Ktf2 = sp.lambdify((t, x, yv, z), Ktf2_3, "numpy")
F_K2 = sp.lambdify((t, x, yv, z), K2_3, "numpy")

t0f, t1f = -40.0, 80.0
sol = solve_ivp(lambda tt, xx: [F_v(tt, xx[0])], (t0f, t1f), [0.0],
                max_step=0.05, rtol=1e-10, atol=1e-12, dense_output=True)
ts = np.linspace(t0f, t1f, 12000)
xs = sol.sol(ts)[0]
vs = np.array([F_v(tt, xx) for tt, xx in zip(ts, xs)])
Ks = F_K(ts, xs, rho_imp, 0.0)
g_nec = (F_dKdt(ts, xs, rho_imp, 0.0) + vs * F_dKdx(ts, xs, rho_imp, 0.0)
         + 1.5 * F_Ktf2(ts, xs, rho_imp, 0.0))
g_sec = (F_dKdt(ts, xs, rho_imp, 0.0) + vs * F_dKdx(ts, xs, rho_imp, 0.0)
         + Ks**2 / 3.0)
xi = xs - vb * ts                                       # bubble-frame coordinate
vmax_pred = vb * float(sp.lambdify((), f_alc.subs({x: 0, t: 0}).subs(sp.Symbol("rho_imp", real=True), rho_imp))()) \
    if False else vb * float((np.tanh(sig * (rho_imp + Rb)) - np.tanh(sig * (rho_imp - Rb))) / (2 * np.tanh(sig * Rb)))
ok5a = abs(vs.max() - vmax_pred) < 5e-5                # PF Eq 7
ok5b = abs(vs[-1]) < 1e-6 and (xs[-1] - xs[0]) > 1.0   # released at rest, displaced forward
i_nec = int(np.argmax(g_nec))
nec_front = float(g_nec[xi > 0].max())                 # front-wall side (xi > 0)
nec_rear = float(g_nec[xi < 0].max())                  # rear-wall side (xi < 0)
ok5c = g_nec[i_nec] > 1e-6                             # NEC obligation violated
ok5d = g_sec.max() > 1e-6                              # SEC obligation violated
gate("passage phenomenology (PF Eq 7) + NEC (SSV 7.34) and SEC (SSV 7.23) obligations violated on trajectory",
     ok5a and ok5b and ok5c and ok5d,
     f"max dx/dt = {vs.max():.6f} vs v_b f(rho) = {vmax_pred:.6f}; final v = {vs[-1]:.1e}; "
     f"displacement = {xs[-1]-xs[0]:.2f}; NEC obligation max = {g_nec[i_nec]:.3e} at xi = {xi[i_nec]:+.2f} "
     f"(front {nec_front:.2e} / rear {nec_rear:.2e} -- violated on BOTH wall crossings); "
     f"max SEC obligation = {g_sec.max():.3e}")

# ----------------------------------------------------------------------------------
# GATE 6 -- PF Eq 8 == repo identity 1
r_pf, rho_p, vsym = sp.symbols("r rho_perp v_s", positive=True)
fS = sp.Function("f")(r_pf)
pf_eq8 = -(1 / (8 * sp.pi)) * (vsym**2 * rho_p**2 / (4 * r_pf**2)) * sp.diff(fS, r_pf)**2
th_s = sp.symbols("theta_s", positive=True)
ident1 = -(vsym**2 / (32 * sp.pi)) * sp.diff(fS, r_pf)**2 * sp.sin(th_s)**2
ok6 = sp.simplify(pf_eq8.subs(rho_p, r_pf * sp.sin(th_s)) - ident1) == 0
gate("PF Eq 8 energy density == repo identity 1 (rho_perp = r sin(theta))", ok6, "exact")

# ----------------------------------------------------------------------------------
# GATE 7 -- PF total-energy chain
th_i, ph_i = sp.symbols("theta phi", positive=True)
ang = sp.integrate(sp.sin(th_i)**3, (th_i, 0, sp.pi)) * 2 * sp.pi     # = 8 pi / 3
E26 = sp.simplify(-(vsym**2 / (32 * sp.pi)) * ang)                     # coefficient of int r^2 f'^2 dr
ok7a = sp.simplify(E26 + vsym**2 / 12) == 0
Rj, Dj = sp.symbols("R Delta", positive=True)
E28 = -(vsym**2 / 12) * sp.integrate(r_pf**2 * (1 / Dj)**2,
                                     (r_pf, Rj - Dj / 2, Rj + Dj / 2))
ok7b = sp.simplify(E28 + (vsym**2 / 12) * (Rj**2 / Dj + Dj / 12)) == 0
sg = sp.symbols("sigma", positive=True)
f_pf = (sp.tanh(sg * (r_pf + Rj)) - sp.tanh(sg * (r_pf - Rj))) / (2 * sp.tanh(sg * Rj))
slope_at_R = sp.diff(f_pf, r_pf).subs(r_pf, Rj)
Delta_eq5 = -1 / slope_at_R                            # piecewise slope -1/Delta matched
Delta_paper = (1 + sp.tanh(sg * Rj)**2)**2 / (2 * sg * sp.tanh(sg * Rj))
# tanh double-angle identity defeats simplify(); certify numerically at random (sigma, R)
d75 = sp.lambdify((sg, Rj), Delta_eq5 - Delta_paper, "mpmath")
mp.mp.dps = 30
rng7 = np.random.default_rng(5)
ok7c = all(abs(d75(mp.mpf(float(rng7.uniform(0.2, 3))), mp.mpf(float(rng7.uniform(0.5, 8)))))
           < mp.mpf("1e-25") for _ in range(8))
ok7d = sp.limit(Delta_paper * sg, sg, sp.oo) == 2
gate("PF Eq 26 angular factor; Eq 28 closed form; Eq 5 Delta(sigma) + 2/sigma limit",
     ok7a and ok7b and ok7c and ok7d, "all exact")

# ----------------------------------------------------------------------------------
# GATE 8 -- PF QI arithmetic and magnitudes
tt_, bpar, t0p = sp.symbols("t beta t_0", positive=True)
I16 = sp.integrate(1 / ((tt_**2 + bpar**2) * (tt_**2 + t0p**2)), (tt_, -sp.oo, sp.oo))
ok8a = sp.simplify(I16 - sp.pi / (t0p * bpar * (t0p + bpar))) == 0
alpha = 0.1
delta_bound = 0.75 * np.sqrt(3 / np.pi) / alpha**2      # in units of v_b L_P (= 73.3)
ok8b = 70 <= delta_bound <= 110                          # paper rounds this to '10^2'
# Eq 29: E = -(1/12) v^2 R^2/Delta with the paper's ROUNDED Delta = 10^2 v_b L_P, R = 100 m.
# PF state explicitly they make order-of-magnitude estimates; tolerance is a factor 3.
G_N, c_l, LP = 6.674e-11, 2.998e8, 1.616e-35
R_m = 100.0
E_geom = (1.0 / 12.0) * R_m**2 / (100.0 * LP)            # per v_b, metres
E_grams = E_geom * c_l**2 / G_N * 1e3
ok8c = 1 / 3 < E_grams / 6.2e65 < 3
M_gal_g = 2e45
ok8d = 1 / 3 < (E_grams / M_gal_g) / 3e20 < 3
gate("PF Eq 16 contour integral exact; Eq 23 wall bound ~1e2 v L_P; Eq 29 |E| ~ 6.2e65 v_b g (OoM); Eq 31 ~3e20 M_gal",
     ok8a and ok8b and ok8c and ok8d,
     f"Delta bound = {delta_bound:.1f} v L_P (paper: '10^2'); E = -{E_grams:.2e} v_b g "
     f"({E_grams/M_gal_g:.1e} M_gal; paper's own g-vs-L_P conversion carries a ~2x rounding)")

# ----------------------------------------------------------------------------------
# GATE 9 -- Hiscock 2D chain
v0 = sp.symbols("v_0", positive=True)
rH = sp.symbols("r", positive=True)
fH = sp.Function("f")(rH)
A = 1 - v0**2 * (1 - fH)**2
# Eq 7 -> Eq 9: substitute x = r + v0 t (dx = dr + v0 dt) into 2D metric
dt_, dr_ = sp.symbols("dt dr", real=True)
ds2_eq7 = -(1 - v0**2 * fH**2) * dt_**2 - 2 * v0 * fH * dt_ * (dr_ + v0 * dt_) + (dr_ + v0 * dt_)**2
ds2_eq9 = -A * (dt_ - v0 * (1 - fH) / A * dr_)**2 + dr_**2 / A
ok9a = sp.simplify(sp.expand(ds2_eq7 - ds2_eq9)) == 0
# diagonal static form curvature: R_2D = -A'' for ds^2 = -A dtau^2 + dr^2/A
tau_ = sp.symbols("tau", real=True)
g2 = sp.diag(-A, 1 / A)
c2 = [tau_, rH]
ginv2 = sp.diag(-1 / A, A)
dg2 = [[[sp.diff(g2[a, b], c2[c]) for c in range(2)] for b in range(2)] for a in range(2)]
Gam2 = [[[sum(ginv2[a, d] * (dg2[d][b][c] + dg2[d][c][b] - dg2[b][c][d]) for d in range(2)) / 2
          for c in range(2)] for b in range(2)] for a in range(2)]
Ric2 = sp.zeros(2, 2)
for b in range(2):
    for c in range(2):
        Ric2[b, c] = (sum(sp.diff(Gam2[a][b][c], c2[a]) for a in range(2))
                      - sum(sp.diff(Gam2[a][b][a], c2[c]) for a in range(2))
                      + sum(Gam2[a][a][d] * Gam2[d][b][c] for a in range(2) for d in range(2))
                      - sum(Gam2[a][c][d] * Gam2[d][b][a] for a in range(2) for d in range(2)))
R2 = sp.simplify(sum(ginv2[a, b] * Ric2[a, b] for a in range(2) for b in range(2)))
ok9b = sp.simplify(R2 + sp.diff(A, rH, 2)) == 0
# RSET Eqs 21-22 (mixed components), conservation + anomaly trace
Ap = sp.diff(A, rH)
T_r_r = -Ap**2 / (96 * sp.pi * A)
T_tau_tau = -sp.diff(A, rH, 2) / (24 * sp.pi) + Ap**2 / (96 * sp.pi * A)
trace_ok = sp.simplify((T_r_r + T_tau_tau) - R2 / (24 * sp.pi)) == 0
# conservation: for static diagonal T^mu_nu(r), the nu = r component reads
# d_r T^r_r + Gam^a_{a r} T^r_r - Gam^a_{r b} T^b_a = 0
cons = (sp.diff(T_r_r, rH)
        + sum(Gam2[a][a][1] for a in range(2)) * T_r_r
        - (Gam2[0][1][0] * T_tau_tau + Gam2[1][1][1] * T_r_r))
ok9c = sp.simplify(cons) == 0 and trace_ok
# near-horizon Eq 24: substitute A in <rho> ~ -A''/(24 pi A) - A'^2/(48 pi A^2),
# expand at f -> 1 - 1/v0: leading term -(f')^2/48pi [f - (1-1/v0)]^{-2}
fp_, fpp_ = sp.symbols("fp fpp", real=True)
eps = sp.symbols("epsilon", positive=True)
# treat f as independent small deviation: f = (1 - 1/v0) + eps, with f' = fp, f'' = fpp
one_mf = 1 / v0 - eps                              # (1 - f) near the horizon
A_h = 1 - v0**2 * one_mf**2
Ap_h = 2 * v0**2 * one_mf * fp_
App_h = 2 * v0**2 * (one_mf * fpp_ - fp_**2)       # A'' = 2 v0^2 [(1-f) f'' - f'^2]
rho_h = -App_h / (24 * sp.pi * A_h) - Ap_h**2 / (48 * sp.pi * A_h**2)
lead = sp.limit(rho_h * eps**2, eps, 0)
ok9d = sp.simplify(lead + fp_**2 / (48 * sp.pi)) == 0
# Eq 25: T_H = A'(r0)/4pi with (1 - f(r0)) = 1/v0  ->  A'(r0) = 2 v0 f'(r0)
Ap_horizon = 2 * v0**2 * (sp.Rational(1, 1) / v0) * fp_
ok9e = sp.simplify(Ap_horizon / (4 * sp.pi) - v0 * fp_ / (2 * sp.pi)) == 0
gate("Hiscock chain: Eq 7->9 equality; R_2D = -A''; RSET conservation + anomaly; Eq 24 leading term; Eq 25 T_H",
     ok9a and ok9b and ok9c and ok9d and ok9e, "all exact (Eq 24 at leading order in wall distance)")

# ----------------------------------------------------------------------------------
# GATE 10 -- subluminal gating + axis-blindness for the zero-expansion drive
fb = sp.symbols("f_b", nonnegative=True)               # f in [0, 1]
A_min = 1 - v0**2 * (1 - fb)**2
# exact identity A - (1 - v0^2) = v0^2 f (2 - f) >= 0 on f in [0, 1]
ok10a = sp.simplify(sp.expand(A_min - (1 - v0**2) - v0**2 * fb * (2 - fb))) == 0
# Natario axis vs equator: axis |X| = 2 v f <= v (f <= 1/2); equator overshoots
rN, thN = sp.symbols("r theta", positive=True)
R0n, sgn_ = 5, 4
f_aN = (sp.tanh(sgn_ * (rN + R0n)) - sp.tanh(sgn_ * (rN - R0n))) / (2 * sp.tanh(sgn_ * R0n))
fN = (1 - f_aN) / 2
Xr_N = -2 * fN * sp.cos(thN)                            # per unit v
Xt_N = (2 * fN + rN * sp.diff(fN, rN)) * sp.sin(thN)
Xnorm = sp.lambdify((rN, thN), sp.sqrt(Xr_N**2 + Xt_N**2), "numpy")
rr = np.linspace(0.25, 12, 600)
axis_max = float(np.nanmax(Xnorm(rr, 1e-6)))
eq_max = float(np.nanmax(Xnorm(rr, np.pi / 2)))
glob_max = float(np.nanmax(Xnorm(rr[:, None], np.linspace(0.01, np.pi - 0.01, 301)[None, :])))
ok10b = axis_max <= 1.0 + 1e-9 and glob_max > 5.0 and abs(glob_max - eq_max) < 0.2
gate("A >= 1 - v0^2 > 0 subluminally (Hiscock-safe); Natario ergo-band is OFF-AXIS (axis-blind reduction)",
     ok10a and ok10b,
     f"axis sup|X|/v = {axis_max:.3f} (<= 1); equator {eq_max:.2f}; global {glob_max:.2f} "
     f"-> v* = {1/glob_max:.3f}; a Hiscock-style axis reduction sees none of it below v = 1")

# ----------------------------------------------------------------------------------
# GATE 11 -- Everett-Roman Krasnikov algebra
kk, dt2, dx2, dlt = sp.symbols("k dt dx delta", real=True)
ok11a = sp.simplify(sp.expand(-(dt2 - dx2) * (dt2 + kk * dx2)
                              - (-dt2**2 + (1 - kk) * dt2 * dx2 + kk * dx2**2))) == 0
# interior k = delta - 1: transformation dt' = dt + (delta/2 - 1) dx, dx' = (delta/2) dx
dtp = dt2 + (dlt / 2 - 1) * dx2
dxp = (dlt / 2) * dx2
ds2_int = -dt2**2 + (1 - (dlt - 1)) * dt2 * dx2 + (dlt - 1) * dx2**2
ok11b = sp.simplify(sp.expand(ds2_int - (-dtp**2 + dxp**2))) == 0
# Eq 10: invert the interior map (dt' = dt + (d/2 - 1)dx, dx' = (d/2)dx) ->
# dt = dt' + ((2 - delta)/delta) dx'
dtp_s, dxp_s = sp.symbols("dtp dxp", real=True)
dx_from = 2 * dxp_s / dlt
dt_from = dtp_s - (dlt / 2 - 1) * dx_from
ok11c = sp.simplify(dt_from - (dtp_s + ((2 - dlt) / dlt) * dxp_s)) == 0
u = sp.symbols("u", real=True)                          # u = dx'/dt'
root = sp.solve(sp.Eq(1 + ((2 - dlt) / dlt) * u, 0), u)[0]
ok11d = sp.simplify(root + dlt / (2 - dlt)) == 0
in_range = all(-1 < float(root.subs(dlt, d_)) < 0 for d_ in (0.1, 0.5, 0.9))
gate("Everett-Roman algebra: factored metric; interior Minkowski map; Eq 10; Eq 11 root in (-1,0)",
     ok11a and ok11b and ok11c and ok11d and in_range, "exact")

# ----------------------------------------------------------------------------------
# GATE 12 -- causality bookkeeping (single tube vs two tubes)
D_ = 10.0
delta_ = 0.05
t_E_single = D_ * delta_                                # ER: return at t_E = D delta > 0
# two-tube itinerary (three-space separation makes the tubes non-overlapping):
# leg 1: Earth (t = 2D) -> Deneb via tube 2 (its interior cone allows dt = -D(1 - delta))
# leg 2: Deneb (t ~ D) -> Earth via tube 1 (same), arriving t ~ 2 D delta ~ 0+
t_arrive_deneb = 2 * D_ - D_ * (1 - delta_)
t_return_earth = t_arrive_deneb - D_ * (1 - delta_)
ok12 = (t_E_single > 0) and (t_return_earth < 2 * D_) and abs(t_return_earth - 2 * D_ * delta_) < 1e-12
gate("single tube: t_E = D delta > 0 (no CTC); two tubes: loop closes to t = 2 D delta << departure",
     ok12, f"single-tube return t = {t_E_single:.2f} > 0; two-tube return t = {t_return_earth:.2f} "
     f"vs departure {2*D_:.0f} -> closed timelike loop available (Everett 1996 pattern)")

# ----------------------------------------------------------------------------------
n_pass = sum(PASS)
print(f"\n{'ALL GATES PASS' if all(PASS) else 'FAILURES PRESENT'}: {n_pass}/{len(PASS)}  "
      f"({time.time()-T0:.0f}s total)")
sys.exit(0 if all(PASS) else 1)

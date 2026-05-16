(*
  fh_rho_at_points.wls
  Independent symbolic-pipeline computation of the FH static-slice
  Eulerian energy density rho(x,y,z) at the canonical anchor.

  Convention:
    alpha = 1, N^i = del_i phi, flat 3-slice ({}^{(3)}R = 0, partial_t N^i = 0).
    K_{ij}        = (1/2)(del_i N_j + del_j N_i)
    K             = del^i N_i  (= laplacian phi)
    K^{ij}K_{ij}  = sum (K_ij)^2  (3-metric is delta_{ij})
    2 rho         = K^{ij} K_{ij} - K^2

  Reads:  agent-tools/xact_io_in.json
            { "anchor": {"V":..,"sigma":..,"m0":..,"a":..,"ell":..,"r":..,"Pi":..},
              "points": [[x,y,z], ...] }
  Writes: agent-tools/xact_io_out.json
            { "rho": [...] }
*)

(* ----- canonical phi_FH_smooth, symbolic in (x,y,z) ----- *)

phiFH[x_, y_, z_, V_, sigma_, m0_, aa_, ell_, r_, Pi0_] := Module[
  {R2, R, R2Pi, mfun, nfun, arg1, arg2, e0, e1, e2, erf0, erf1, erf2,
   innerExp, innerErf},
  R2    = x^2 + y^2 + z^2;
  R     = Sqrt[R2 + 10^-60];
  R2Pi  = (R2 + 10^-60)^Pi0;
  mfun  = m0 + aa*Tanh[z/ell];
  nfun  = m0 - aa*Tanh[z/ell];
  arg1  = r - R2Pi/mfun;
  arg2  = r + R2Pi/nfun;
  e0    = Exp[-R2/sigma];
  e1    = Exp[-arg1^2/sigma];
  e2    = Exp[-arg2^2/sigma];
  erf0  = Erf[R/Sqrt[sigma]];
  erf1  = Erf[arg1/Sqrt[sigma]];
  erf2  = Erf[arg2/Sqrt[sigma]];
  innerExp = sigma*(e1*mfun*nfun + e2*mfun*nfun - e0*(mfun + nfun));
  innerErf = Sqrt[sigma*Pi]*(
       -((mfun + nfun)*R*erf0)
       + nfun*(mfun*R - R2Pi)*erf1
       + mfun*(nfun*R - R2Pi)*erf2);
  V/(mfun + nfun + 10^-60)*(innerExp + innerErf)
];

(* ----- read input ----- *)

inFile  = "agent-tools/xact_io_in.json";
outFile = "agent-tools/xact_io_out.json";

input  = Import[inFile, "RawJSON"];
anchor = input["anchor"];
pts    = input["points"];  (* list of {x,y,z} *)

V0     = anchor["V"];
sigma0 = anchor["sigma"];
m00    = anchor["m0"];
aa0    = anchor["a"];
ell0   = anchor["ell"];
r0     = anchor["r"];
Pi00   = anchor["Pi"];

(* substitute anchor; phi becomes a function of (x,y,z) only *)
phiSym = phiFH[xx, yy, zz, V0, sigma0, m00, aa0, ell0, r0, Pi00];

(* symbolic first/second derivatives -- needed for K_ij and K *)
Print["[xact] computing symbolic gradients at anchor..."];
phiX  = D[phiSym, xx];
phiY  = D[phiSym, yy];
phiZ  = D[phiSym, zz];

phiXX = D[phiX, xx]; phiXY = D[phiX, yy]; phiXZ = D[phiX, zz];
phiYY = D[phiY, yy]; phiYZ = D[phiY, zz];
phiZZ = D[phiZ, zz];

(* K_ij = (1/2)(del_i N_j + del_j N_i) where N_i = del_i phi
   (since flat 3-metric -> N_i = N^i)
   So K_ij = del_i del_j phi (already symmetric). *)
KK = {{phiXX, phiXY, phiXZ}, {phiXY, phiYY, phiYZ}, {phiXZ, phiYZ, phiZZ}};
trK = phiXX + phiYY + phiZZ;
KKsq = Total[Flatten[KK^2]];

(* Gauss-Codazzi with flat 3-slice + alpha=1 + dt N^i = 0:
   Python convention (adm_stress_energy_from_N):
     K_{ij}    = -(1/2)(del_i N_j + del_j N_i)         (note minus sign)
     K         = -(del^i N_i)  = -laplacian(phi)
     rho_E     = (K_trace^2 - K^{ij} K_{ij}) / (16 pi)
   Sign of K does not matter because K^2 and K_ij^2 are invariant; we use the
   positive-K convention here and match the rho formula directly. *)
rhoSym = (trK^2 - KKsq)/(16*Pi);

(* numerically evaluate at each point *)
Print["[xact] numerically evaluating rho at ", Length[pts], " points..."];

evalRhoAt[{px_, py_, pz_}] := Module[{val},
  val = rhoSym /. {xx -> px, yy -> py, zz -> pz};
  val = N[val, 30];
  Re[val]
];

rhoVals = evalRhoAt /@ pts;

(* write output *)
Export[outFile, <|
  "rho"            -> rhoVals,
  "n_points"       -> Length[pts],
  "anchor"         -> anchor,
  "convention"     -> "rho_python = (K_ij K^ij - K^2)/2 with alpha=1, N=grad phi, flat 3-slice",
  "wolfram_version"-> $Version
|>, "RawJSON"];

Print["[xact] wrote ", outFile];
Print["[xact] first 3 rho values: ", Take[rhoVals, Min[3, Length[rhoVals]]]];

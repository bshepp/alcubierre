(*
  fh_rho_at_points_multi.wls

  Multi-anchor variant: input JSON has list of {anchor, points} jobs; output
  JSON has list of {rho} arrays. Avoids re-paying kernel startup per anchor.

  Reads:  agent-tools/xact_io_in.json
            { "jobs": [ {"anchor": {...}, "points": [[x,y,z],...]}, ... ] }
  Writes: agent-tools/xact_io_out.json
            { "results": [ {"rho": [...]}, ... ] }
*)

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

input = Import["agent-tools/xact_io_in.json", "RawJSON"];
jobs  = input["jobs"];

allResults = Table[
  Module[{anchor, pts, V0, sigma0, m00, aa0, ell0, r0, Pi00,
          phiSym, phiX, phiY, phiZ, phiXX, phiXY, phiXZ, phiYY, phiYZ, phiZZ,
          trK, KKsq, rhoSym, rhoVals},
    anchor = jobs[[k]]["anchor"];
    pts    = jobs[[k]]["points"];
    {V0, sigma0, m00, aa0, ell0, r0, Pi00} = {anchor["V"], anchor["sigma"],
        anchor["m0"], anchor["a"], anchor["ell"], anchor["r"], anchor["Pi"]};
    Print["[xact] job ", k, " of ", Length[jobs],
          ": anchor V=", V0, " sigma=", sigma0, " r=", r0,
          " npts=", Length[pts]];
    phiSym = phiFH[xx, yy, zz, V0, sigma0, m00, aa0, ell0, r0, Pi00];
    phiX   = D[phiSym, xx]; phiY = D[phiSym, yy]; phiZ = D[phiSym, zz];
    phiXX  = D[phiX, xx]; phiXY = D[phiX, yy]; phiXZ = D[phiX, zz];
    phiYY  = D[phiY, yy]; phiYZ = D[phiY, zz]; phiZZ = D[phiZ, zz];
    trK    = phiXX + phiYY + phiZZ;
    KKsq   = phiXX^2 + phiYY^2 + phiZZ^2 + 2 phiXY^2 + 2 phiXZ^2 + 2 phiYZ^2;
    rhoSym = (trK^2 - KKsq)/(16*Pi);
    rhoVals = Re[N[rhoSym /. {xx -> #[[1]], yy -> #[[2]], zz -> #[[3]]}, 30]] & /@ pts;
    <|"rho" -> rhoVals|>
  ],
  {k, Length[jobs]}
];

Export["agent-tools/xact_io_out.json",
  <|"results" -> allResults, "wolfram_version" -> $Version|>, "RawJSON"];

Print["[xact] wrote agent-tools/xact_io_out.json (", Length[allResults], " jobs)"];

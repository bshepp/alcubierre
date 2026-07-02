"""Task 2B.8 -- the even-if magnitude bound for a gravitational Casimir wall.

Run with repo root on PYTHONPATH (no project imports needed; standalone):

    C:\\Python313\\python.exe verification/test_2b8_casimir_gap.py

The assessment's decisive step. Grant Path 2B everything the contested
literature could possibly deliver: a PERFECT graviton mirror (reflectivity 1
-- i.e. waive the impedance/absorption no-go for ordinary matter, assume the
Heisenberg-Coulomb superconductor claim true and perfectly efficient) and a
FAVOURABLE sign (waive Boyer 1968's repulsive-sphere result). The
renormalised vacuum-energy density available from boundary confinement of a
massless field at separation d is then bounded by the dimensional Casimir
envelope

    |rho_C| <= K * hbar c / d^4,   K = O(1)

(EM parallel plates: K = pi^2/720 ~ 0.0137 between perfect conductors;
graviton polarisation counting changes K by O(1); we take K = 1, generous by
~70x). Compare against the EC-deficit scales this project has certified in
its own slices. If the gap is tens of orders of magnitude at every relevant
separation, Path 2B is closed as a physical negative-energy mechanism
REGARDLESS of how the contested mirror question resolves.

Certified targets (SI J/m^3, radial evaluator, Sessions 29-32):
  - canonical-shell in-shell EC margin scale ~1e38 (e.g. min(EC) swings
    +1.7e38 (pass, S31 anchor) / -2.2e38 (fail just below M_min, S32));
  - the S31 anisotropic sharp-optimum DEC violation -3.72e39 (full-res);
  - shell rest-energy density scale rho*c^2 = M/(V_shell) * c^2 ~ 1.38e40
    (canonical Fuchs 4.49e27 kg in the (10,20) m shell).
Any Path-2B "negative sliver" or acceleration supplement must act at these
densities to matter.
"""

from __future__ import annotations

import math

hbar = 1.054571817e-34  # J s
c = 2.99792458e8        # m/s
G = 6.67430e-11         # SI
hbarc = hbar * c        # J m
l_planck = math.sqrt(hbar * G / c**3)

TARGETS = {
    "canonical shell EC-margin scale (S29-32 radial-certified)": 1.0e38,
    "S31 sharp-optimum DEC violation (full-res)": 3.72e39,
    "canonical Fuchs shell rest-energy density rho*c^2": 1.38e40,
}
SEPARATIONS = (10.0, 1.0, 0.1, 1e-3)  # m: R1, Delta-scale, sub-wall, mm


def main() -> int:
    print("=" * 78)
    print("Task 2B.8 even-if bound: perfect graviton mirror, K = 1 envelope")
    print(f"  hbar*c = {hbarc:.4e} J m   (EM plate coefficient pi^2/720 = "
          f"{math.pi**2/720:.4f} -- K=1 is ~{1/(math.pi**2/720):.0f}x generous)")
    print("=" * 78)

    print("\nCasimir density envelope |rho_C| <= hbar*c/d^4 at wall-relevant d:")
    for d in SEPARATIONS:
        print(f"  d = {d:>7.3g} m : |rho_C| <= {hbarc / d**4:.3e} J/m^3")

    print("\nRequired-density comparison (gap quoted at d = 1 m and d = 10 m):")
    ok = True
    for name, rho in TARGETS.items():
        d_req = (hbarc / rho) ** 0.25
        gap1 = math.log10(rho / (hbarc / 1.0**4))
        gap10 = math.log10(rho / (hbarc / 10.0**4))
        print(f"  {name}:")
        print(f"    rho_req = {rho:.3e} J/m^3 -> boundary separation needed "
              f"d = {d_req:.2e} m ({d_req / l_planck:.1e} l_P; sub-proton)")
        print(f"    shortfall: {gap1:.1f} OoM at d = 1 m; {gap10:.1f} OoM at "
              f"d = 10 m")
        ok = ok and gap1 > 30.0  # 'decisive' criterion: >> Krasnikov 31-OoM kill

    print("\nVERDICT:", "gap is DECISIVE (>> the Slice-4b 31-OoM standard) for "
          "every certified target" if ok else "gap NOT decisive -- re-examine")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

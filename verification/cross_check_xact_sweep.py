"""9-point cross-pipeline sweep across (V, sigma, r).

For each anchor variation:
  1. build a fresh FH grid at NPTS=65, L=12
  2. compute rho_python via adm_stress_energy
  3. build a 5x5x5 interior sub-grid (filtering near-origin points)
  4. accumulate (anchor, points) into a single multi-job request

Then invoke wolframscript ONCE on the combined input and compare.

Sweep design:
  V    in {0.5, 1.5, 2.5}     (low / canonical / high)
  sigma in {5, 10, 20}        (low / canonical / high)
  r    in {6, 9, 12}          (low / canonical / high)
  one parameter at a time, all others at canonical -> 3*3 = 9 anchors
  (V=1.5, sigma=10, r=9 appears 3x; deduped -> 7 unique anchors;
   keep all 9 jobs for redundancy / sanity check).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from hf_jobs.sweeps.fell_heisenberg import phi_FH_smooth, adm_stress_energy

WOLFRAMSCRIPT = r"C:\Program Files\Wolfram Research\WolframScript\wolframscript.exe"

CANON  = dict(V=1.5, sigma=10.0, m0=3.0, a=0.05, ell=4.0, r=9.0, Pi=0.25)
LBOX   = 12.0
NPTS   = 65
NGRID  = 5

VARIATIONS = (
    ("V",     [0.5, 1.5, 2.5]),
    ("sigma", [5.0, 10.0, 20.0]),
    ("r",     [6.0, 9.0, 12.0]),
)

def make_anchor(name, val):
    a = dict(CANON)
    a[name] = val
    return a

def main():
    coord = np.linspace(-LBOX/2, LBOX/2, NPTS)
    h = coord[1] - coord[0]
    X, Y, Z = np.meshgrid(coord, coord, coord, indexing="ij")

    margin = 6
    inner_idx = np.linspace(margin, NPTS - 1 - margin, NGRID).astype(int)

    jobs_in = []
    job_meta = []   # parallel list: (label, anchor, rho_py_pts list)

    for param, values in VARIATIONS:
        for v in values:
            anchor = make_anchor(param, v)
            label = f"{param}={v}"
            print(f"[python] computing rho_py for {label}")
            phi = phi_FH_smooth(X, Y, Z, **anchor)
            rho_py_grid, _, _ = adm_stress_energy(phi, h)

            pts = []
            rho_py_pts = []
            for ix in inner_idx:
                for iy in inner_idx:
                    for iz in inner_idx:
                        p = (float(coord[ix]), float(coord[iy]), float(coord[iz]))
                        # skip exact origin (Pi=1/4 non-smooth point)
                        if abs(p[0]) < 1e-12 and abs(p[1]) < 1e-12 and abs(p[2]) < 1e-12:
                            continue
                        pts.append(list(p))
                        rho_py_pts.append(float(rho_py_grid[ix, iy, iz]))

            jobs_in.append({"anchor": anchor, "points": pts})
            job_meta.append((label, anchor, np.array(rho_py_pts), pts))
            print(f"  rho_py range = [{min(rho_py_pts):.4e}, {max(rho_py_pts):.4e}], n={len(pts)}")

    in_file = REPO_ROOT / "agent-tools" / "xact_io_in.json"
    in_file.write_text(json.dumps({"jobs": jobs_in}, indent=2))
    print(f"\n[python] wrote {in_file.name} with {len(jobs_in)} jobs")

    print("[python] invoking wolframscript on combined multi-job request...")
    proc = subprocess.run(
        [WOLFRAMSCRIPT, "-file", str(REPO_ROOT / "agent-tools" / "fh_rho_at_points_multi.wls")],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=1800,
    )
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr)
        sys.exit(f"wolframscript exited {proc.returncode}")

    out = json.loads((REPO_ROOT / "agent-tools" / "xact_io_out.json").read_text())
    results = out["results"]

    rows = []
    print("\n" + "=" * 90)
    print(f"{'job':18s}  {'n':>3s}  {'rho_py range':28s}  {'med rel':>9s}  {'max rel':>9s}  grade")
    print("=" * 90)
    for (label, anchor, rho_py, pts), result in zip(job_meta, results):
        rho_x = np.array(result["rho"], dtype=float)
        abs_d = np.abs(rho_x - rho_py)
        denom = np.maximum(np.abs(rho_py), np.abs(rho_x))
        rel   = np.where(denom > 0, abs_d/denom, 0.0)
        med = float(np.median(rel))
        mx  = float(rel.max())
        if mx < 1e-3 and med < 1e-4:
            grade = "A"
        elif med < 1e-3:
            grade = "B"
        else:
            grade = "C"
        print(f"{label:18s}  {len(pts):3d}  "
              f"[{rho_py.min():+.3e}, {rho_py.max():+.3e}]  "
              f"{med:9.2e}  {mx:9.2e}  {grade}")
        rows.append({
            "label": label,
            "anchor": anchor,
            "n_points": len(pts),
            "rho_py_min": float(rho_py.min()),
            "rho_py_max": float(rho_py.max()),
            "rel_diff_median": med,
            "rel_diff_max":    mx,
            "rel_diff_p95":    float(np.percentile(rel, 95)),
            "grade": grade,
        })

    summary = {
        "npts_python": NPTS,
        "h_python":    float(h),
        "ngrid_subgrid": NGRID,
        "n_jobs": len(rows),
        "all_grade_A": all(r["grade"] == "A" for r in rows),
        "rows": rows,
    }
    out_path = REPO_ROOT / "agent-tools" / "cross_check_xact_sweep.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"\n[python] persisted summary to {out_path.name}")
    print(f"[python] all-A: {summary['all_grade_A']}")


if __name__ == "__main__":
    main()

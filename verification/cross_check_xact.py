"""Cross-pipeline check: Python FD ADM rho vs Mathematica symbolic rho.

Plan:
  1. Build the canonical-anchor FH grid at Npts=N_GRID (default 65), L=12.
  2. Compute rho_python = adm_stress_energy(phi, h)[0]  via the FD pipeline.
  3. Pick a 5x5x5 interior sub-grid (avoiding the FD boundary layer).
  4. Write the (x,y,z) coordinates and anchor to agent-tools/xact_io_in.json.
  5. Invoke wolframscript -file agent-tools/fh_rho_at_points.wls.
  6. Read agent-tools/xact_io_out.json (rho_xact at those points).
  7. Compute relative + absolute differences; print summary; persist to JSON.

Run:
  python agent-tools/cross_check_xact.py [--npts 65] [--ngrid 5]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

# allow `python agent-tools/cross_check_xact.py` from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hf_jobs.sweeps.fell_heisenberg import phi_FH_smooth, adm_stress_energy

REPO_ROOT = Path(__file__).resolve().parent.parent
IN_FILE   = REPO_ROOT / "agent-tools" / "xact_io_in.json"
OUT_FILE  = REPO_ROOT / "agent-tools" / "xact_io_out.json"
WLS_FILE  = REPO_ROOT / "agent-tools" / "fh_rho_at_points.wls"
RESULT    = REPO_ROOT / "agent-tools" / "cross_check_xact_result.json"

WOLFRAMSCRIPT = r"C:\Program Files\Wolfram Research\WolframScript\wolframscript.exe"

ANCHOR = dict(V=1.5, sigma=10.0, m0=3.0, a=0.05, ell=4.0, r=9.0, Pi=0.25)
LBOX   = 12.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--npts", type=int, default=65,
                        help="Python FD grid resolution (default 65, matches sweep)")
    parser.add_argument("--ngrid", type=int, default=5,
                        help="Cross-check sub-grid linear size (default 5 -> 125 points)")
    parser.add_argument("--label", type=str, default="anchor",
                        help="Label written into result JSON")
    args = parser.parse_args()

    # ---- step 1+2: Python pipeline ----
    print(f"[python] building FH grid Npts={args.npts}, L={LBOX}, anchor={ANCHOR}")
    coord = np.linspace(-LBOX / 2, LBOX / 2, args.npts)
    h = coord[1] - coord[0]
    X, Y, Z = np.meshgrid(coord, coord, coord, indexing="ij")
    phi = phi_FH_smooth(X, Y, Z, **ANCHOR)
    print(f"[python] phi range: [{phi.min():.6e}, {phi.max():.6e}]")

    rho_py, _, _ = adm_stress_energy(phi, h)
    print(f"[python] rho range: [{rho_py.min():.6e}, {rho_py.max():.6e}]")

    # ---- step 3: pick interior sub-grid ----
    # leave a 6-cell margin from each edge so the FD stencil sees clean data
    margin = 6
    inner_idx = np.linspace(margin, args.npts - 1 - margin, args.ngrid).astype(int)
    pts = []
    rho_py_pts = []
    for ix in inner_idx:
        for iy in inner_idx:
            for iz in inner_idx:
                pts.append([float(coord[ix]), float(coord[iy]), float(coord[iz])])
                rho_py_pts.append(float(rho_py[ix, iy, iz]))
    print(f"[python] sampled {len(pts)} interior points")

    # ---- step 4: write input for Mathematica ----
    IN_FILE.write_text(json.dumps({"anchor": ANCHOR, "points": pts}, indent=2))
    print(f"[python] wrote {IN_FILE.relative_to(REPO_ROOT)}")

    # ---- step 5: invoke wolframscript ----
    print(f"[python] invoking wolframscript -file {WLS_FILE.name} ...")
    proc = subprocess.run(
        [WOLFRAMSCRIPT, "-file", str(WLS_FILE)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=900,
    )
    print("[wolframscript stdout]")
    print(proc.stdout)
    if proc.returncode != 0:
        print("[wolframscript stderr]")
        print(proc.stderr)
        sys.exit(f"wolframscript exited {proc.returncode}")

    # ---- step 6: read output ----
    out = json.loads(OUT_FILE.read_text())
    rho_xact = np.array(out["rho"], dtype=float)
    rho_py_pts = np.array(rho_py_pts, dtype=float)

    # ---- step 7: compare ----
    abs_diff = np.abs(rho_xact - rho_py_pts)
    denom    = np.maximum(np.abs(rho_py_pts), np.abs(rho_xact))
    safe     = denom > 1e-30
    rel_diff = np.where(safe, abs_diff / denom, 0.0)

    print()
    print("=" * 72)
    print(f"Cross-check rho_python (FD, Npts={args.npts}) vs rho_xact (symbolic)")
    print("=" * 72)
    print(f"  n points       : {len(pts)}")
    print(f"  rho_py range   : [{rho_py_pts.min():.6e}, {rho_py_pts.max():.6e}]")
    print(f"  rho_xact range : [{rho_xact.min():.6e}, {rho_xact.max():.6e}]")
    print(f"  abs diff median: {np.median(abs_diff):.3e}")
    print(f"  abs diff max   : {abs_diff.max():.3e}")
    print(f"  rel diff median: {np.median(rel_diff):.3e}")
    print(f"  rel diff max   : {rel_diff.max():.3e}")
    print(f"  rel diff p95   : {np.percentile(rel_diff, 95):.3e}")
    print()

    grade = "C"
    if np.median(rel_diff) < 1e-4 and rel_diff.max() < 1e-3:
        grade = "A"
    elif np.median(rel_diff) < 1e-3:
        grade = "B"
    print(f"  decision-gate grade: {grade}")

    summary = {
        "label": args.label,
        "anchor": ANCHOR,
        "n_points": len(pts),
        "npts_python": args.npts,
        "h_python": float(h),
        "rho_py_range": [float(rho_py_pts.min()), float(rho_py_pts.max())],
        "rho_xact_range": [float(rho_xact.min()), float(rho_xact.max())],
        "abs_diff_median": float(np.median(abs_diff)),
        "abs_diff_max":    float(abs_diff.max()),
        "rel_diff_median": float(np.median(rel_diff)),
        "rel_diff_max":    float(rel_diff.max()),
        "rel_diff_p95":    float(np.percentile(rel_diff, 95)),
        "decision_grade":  grade,
    }
    RESULT.write_text(json.dumps(summary, indent=2))
    print(f"\n[python] persisted summary to {RESULT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

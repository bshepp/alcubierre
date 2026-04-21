"""Batch single-bubble CTC test for FH strict-pass region (Task 2D.7).

Implements ROADMAP Task 2D.7 single-bubble half. For each strict-pass row in
the full + refine FH parquets, builds the FH potential on a Cartesian box,
computes the static-Killing norm

    g_tt(x) = -alpha^2 + |N(x)|^2 = -1 + |grad phi|^2     (alpha = 1 for FH)

and reports per-row diagnostics:

  - max(g_tt)            sup over the box (largest spacelike-of-d/dt excursion)
  - frac_gtt_positive    fraction of cells where d/dt is spacelike (CTC region)
  - gtt_centre           g_tt at the origin (passenger-zone health)
  - worst_xyz            (x, y, z) of the max-g_tt cell

This is a cheap test: no eigenvalue diagonalization, no full ADM stress-energy.
For NPTS=49 the per-point cost is ~0.5 s on a single CPU. The default Npts
matches the full sweep's coarse-grid choice (49) so the batch matches the
parquet's strict-pass classification regime.

Reading: per FELL_HEISENBERG_SWEEP_NOTES.md §14, every strict-pass point is
expected to have frac_gtt_positive close to 1 (only the central voxel is
timelike). The headline aggregate is therefore (a) "all strict-pass rows are
CTC almost everywhere," (b) the distribution of max(g_tt) across the
strict-pass region (a proxy for how supraluminal the wall is), and (c) the
sanity check that gtt_centre < 0 for every row (passenger-zone is timelike).

CLI:

    python -m hf_jobs.analysis.fell_heisenberg_ctc \\
        --output fell_heisenberg_ctc \\
        [--npts 49] [--workers 4]

Outputs:
    fell_heisenberg_ctc/single_bubble.csv   one row per strict-pass point
    fell_heisenberg_ctc/summary.json        aggregate statistics
"""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from hf_jobs.sweeps.fell_heisenberg import phi_FH_smooth, fd_grad4


DEFAULT_FULL_PARQUET = Path(
    "sweeps_remote/full-20260420T022727/fell_heisenberg_20260420T022809.parquet"
)
DEFAULT_REFINE_PARQUET = Path(
    "sweeps_remote/refine-20260420T041817/fell_heisenberg_20260420T041859.parquet"
)


@dataclass
class CTCRow:
    """One row of the per-point CTC diagnostics."""
    V: float
    sigma: float
    m0: float
    a: float
    ell: float
    r: float
    Pi: float
    L: float
    Npts: int
    gtt_min: float
    gtt_max: float
    gtt_centre: float
    frac_gtt_positive: float
    Nmax: float
    worst_x: float
    worst_y: float
    worst_z: float


def _load_strict_pass(full: Path, refine: Path) -> pd.DataFrame:
    """Concatenate strict-pass rows from full + refine parquets, dropping dupes."""
    parts: list[pd.DataFrame] = []
    for p in (full, refine):
        if not p.exists():
            raise FileNotFoundError(f"Missing parquet: {p}")
        df = pd.read_parquet(p)
        s = df[(df.wec_slack_min >= 0) & (df.dec_slack_min >= 0) & df.ok].copy()
        parts.append(s)
    out = pd.concat(parts, ignore_index=True)
    # De-duplicate on the parameter tuple (refine grids may overlap full).
    keys = ["V", "sigma", "m0", "a", "ell", "r", "Pi", "L"]
    # Round to avoid floating-noise non-deduplication.
    rounded = out[keys].round(8)
    out = out.assign(**{f"_k_{k}": rounded[k] for k in keys})
    out = out.drop_duplicates(subset=[f"_k_{k}" for k in keys])
    out = out.drop(columns=[f"_k_{k}" for k in keys])
    return out.reset_index(drop=True)


def _evaluate_row(row: dict, npts: int) -> CTCRow:
    """Compute the CTC diagnostics for one parameter point."""
    L = float(row["L"])
    xs = np.linspace(-L, L, npts)
    h = float(xs[1] - xs[0])
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    phi = phi_FH_smooth(
        X, Y, Z,
        Pi=float(row.get("Pi", 0.25)),
        r=float(row["r"]),
        V=float(row["V"]),
        sigma=float(row["sigma"]),
        m0=float(row["m0"]),
        a=float(row["a"]),
        ell=float(row["ell"]),
    )
    gx = fd_grad4(phi, h, axis=0)
    gy = fd_grad4(phi, h, axis=1)
    gz = fd_grad4(phi, h, axis=2)
    N2 = gx ** 2 + gy ** 2 + gz ** 2
    gtt = -1.0 + N2
    flat = int(np.argmax(gtt))
    i, j, k = np.unravel_index(flat, gtt.shape)
    ic = npts // 2
    return CTCRow(
        V=float(row["V"]),
        sigma=float(row["sigma"]),
        m0=float(row["m0"]),
        a=float(row["a"]),
        ell=float(row["ell"]),
        r=float(row["r"]),
        Pi=float(row.get("Pi", 0.25)),
        L=L,
        Npts=int(npts),
        gtt_min=float(gtt.min()),
        gtt_max=float(gtt.max()),
        gtt_centre=float(gtt[ic, ic, ic]),
        frac_gtt_positive=float((gtt > 0).mean()),
        Nmax=float(np.sqrt(N2.max())),
        worst_x=float(xs[i]),
        worst_y=float(xs[j]),
        worst_z=float(xs[k]),
    )


def _evaluate_chunk(rows: list[dict], npts: int) -> list[CTCRow]:
    return [_evaluate_row(r, npts) for r in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--full", type=Path, default=DEFAULT_FULL_PARQUET)
    parser.add_argument("--refine", type=Path, default=DEFAULT_REFINE_PARQUET)
    parser.add_argument("--output", type=Path, default=Path("fell_heisenberg_ctc"))
    parser.add_argument("--npts", type=int, default=49,
                        help="grid resolution per axis (matches sweep default)")
    parser.add_argument("--workers", type=int, default=4,
                        help="parallel processes; capped at min(workers, cpu-1)")
    parser.add_argument("--limit", type=int, default=0,
                        help="if >0, only process the first N strict-pass rows (smoke test)")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    print(f"[ctc] loading strict-pass rows from {args.full} + {args.refine}")
    df = _load_strict_pass(args.full, args.refine)
    if args.limit > 0:
        df = df.head(args.limit)
    n_total = len(df)
    print(f"[ctc] {n_total} strict-pass rows after dedup; running at Npts={args.npts}")

    rows = df.to_dict("records")
    import os
    cpu = os.cpu_count() or 2
    workers = max(1, min(args.workers, cpu - 1))
    print(f"[ctc] using {workers} workers")

    # Chunk for ProcessPool (reduce pickling overhead).
    chunk_size = max(1, n_total // (workers * 4) or 1)
    chunks = [rows[i : i + chunk_size] for i in range(0, n_total, chunk_size)]

    results: list[CTCRow] = []
    t0 = time.time()
    if workers == 1:
        for ch in chunks:
            results.extend(_evaluate_chunk(ch, args.npts))
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(_evaluate_chunk, ch, args.npts) for ch in chunks]
            done = 0
            for fut in as_completed(futures):
                got = fut.result()
                results.extend(got)
                done += len(got)
                elapsed = time.time() - t0
                rate = done / elapsed if elapsed > 0 else float("inf")
                eta = (n_total - done) / rate if rate > 0 else float("inf")
                print(f"[ctc] {done}/{n_total} done  ({rate:.1f}/s, ETA {eta:.1f}s)")
    elapsed = time.time() - t0
    print(f"[ctc] all {n_total} rows done in {elapsed:.1f}s")

    out_df = pd.DataFrame([asdict(r) for r in results])
    csv_path = args.output / "single_bubble.csv"
    out_df.to_csv(csv_path, index=False)
    print(f"[ctc] wrote {csv_path}")

    # Aggregate summary.
    summary = {
        "n_rows": int(len(out_df)),
        "Npts": int(args.npts),
        "gtt_max":   {"min": float(out_df.gtt_max.min()),
                      "median": float(out_df.gtt_max.median()),
                      "max": float(out_df.gtt_max.max())},
        "gtt_centre": {"min": float(out_df.gtt_centre.min()),
                       "median": float(out_df.gtt_centre.median()),
                       "max": float(out_df.gtt_centre.max())},
        "frac_gtt_positive": {"min": float(out_df.frac_gtt_positive.min()),
                              "median": float(out_df.frac_gtt_positive.median()),
                              "max": float(out_df.frac_gtt_positive.max())},
        "all_centre_timelike": bool((out_df.gtt_centre < 0).all()),
        "all_walls_supraluminal": bool((out_df.gtt_max > 0).all()),
        "elapsed_seconds": float(elapsed),
    }
    sum_path = args.output / "summary.json"
    sum_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"[ctc] wrote {sum_path}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

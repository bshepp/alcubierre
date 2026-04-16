"""Hugging Face Jobs / local parameter-sweep dispatcher.

Thin wrapper used by the Path 2A notebooks to offload numerical sweeps to
external compute (HF Jobs, Colab, or just a longer-running local shell).

Each sweep is registered as a module under ``hf_jobs.sweeps`` exposing two
objects:

* ``build_grid(config: dict) -> list[dict]`` - expand a JSON param spec into
  a list of evaluation points.
* ``evaluate(point: dict) -> dict`` - evaluate one point, returning a scalar
  result record.

The wrapper writes results to
``sweeps/<package>_<timestamp>.parquet`` (alongside a sibling ``.json``
with the config), which is the convention expected by the notebooks.

Usage
-----
Local::

    python hf_jobs/run_sweep.py israel_junction_partA \
        --config hf_jobs/configs/israel_junction_partA_preview.json

HF Jobs (illustrative; the notebook cells wrap this)::

    hf jobs run --flavor cpu-upgrade \
        -e HF_JOB=1 -v $PWD:/work python:3.12 \
        python /work/hf_jobs/run_sweep.py israel_junction_partA \
            --config /work/hf_jobs/configs/israel_junction_partA_full.json

Each sweep module is intentionally a plain Python file rather than a nbconvert
export, because nbconvert round-tripping is fragile and we want sweeps to be
callable without executing the whole notebook first.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SWEEPS_DIR = REPO_ROOT / "sweeps"


def _load_sweep(name: str):
    try:
        return importlib.import_module(f"hf_jobs.sweeps.{name}")
    except ModuleNotFoundError as exc:
        raise SystemExit(
            f"Unknown sweep '{name}'. Available sweeps live in hf_jobs/sweeps/."
        ) from exc


def _default_workers() -> int:
    # HF Jobs cpu-upgrade has 8 vCPU. Locally we back off to leave the machine
    # usable; on Colab / HF Jobs we take everything.
    if os.environ.get("HF_JOB") or "google.colab" in sys.modules:
        return max(1, (os.cpu_count() or 2))
    # On Windows, spawning dozens of worker processes each loading numpy
    # can exhaust the OpenBLAS thread pool and heap; cap at 4.
    cpu = os.cpu_count() or 2
    if sys.platform.startswith("win"):
        return max(1, min(4, cpu - 1))
    return max(1, cpu - 1)


def run(
    sweep_name: str,
    config_path: Path,
    out_dir: Path = SWEEPS_DIR,
    workers: int | None = None,
    limit: int | None = None,
) -> Path:
    """Execute a sweep and persist results. Returns the output parquet path."""
    sweep = _load_sweep(sweep_name)
    with config_path.open("r", encoding="utf-8") as fh:
        config = json.load(fh)

    grid = sweep.build_grid(config)
    if limit is not None:
        grid = grid[:limit]
    if not grid:
        raise SystemExit("Empty grid; refusing to run.")

    workers = workers or _default_workers()
    print(
        f"[run_sweep] sweep={sweep_name} points={len(grid)} "
        f"workers={workers} HF_JOB={bool(os.environ.get('HF_JOB'))}"
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S")
    out_parquet = out_dir / f"{sweep_name}_{stamp}.parquet"
    out_json = out_dir / f"{sweep_name}_{stamp}.config.json"
    out_json.write_text(json.dumps(config, indent=2), encoding="utf-8")

    t0 = time.time()
    records: list[dict] = []

    if workers == 1:
        for i, point in enumerate(grid):
            records.append(sweep.evaluate(point))
            if (i + 1) % 500 == 0:
                print(f"  [{i + 1}/{len(grid)}] elapsed={time.time() - t0:.1f}s")
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(sweep.evaluate, point): i for i, point in enumerate(grid)}
            done = 0
            for fut in as_completed(futures):
                records.append(fut.result())
                done += 1
                if done % 500 == 0:
                    print(f"  [{done}/{len(grid)}] elapsed={time.time() - t0:.1f}s")

    df = pd.DataFrame.from_records(records)
    df.to_parquet(out_parquet, index=False)
    print(
        f"[run_sweep] wrote {out_parquet} "
        f"({len(df)} rows, {time.time() - t0:.1f}s total)"
    )
    return out_parquet


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("sweep", help="Name of sweep module under hf_jobs/sweeps/.")
    p.add_argument("--config", required=True, type=Path, help="JSON config path.")
    p.add_argument("--out-dir", type=Path, default=SWEEPS_DIR)
    p.add_argument("--workers", type=int, default=None)
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Cap the number of grid points (useful for smoke tests).",
    )
    args = p.parse_args(argv)
    run(args.sweep, args.config, out_dir=args.out_dir, workers=args.workers, limit=args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

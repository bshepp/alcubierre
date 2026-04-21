---
name: new-sweep
description: 'Scaffold a new HF Jobs parameter sweep for the Alcubierre repo: creates `hf_jobs/sweeps/<name>.py` (with `build_grid`/`evaluate` stubs), paired `<name>_preview.json` and `<name>_full.json` configs in `hf_jobs/configs/`, and prints the README-style dispatch invocations. Use when the user asks to add a new parameter sweep, factor a heavy notebook cell out to HF Jobs, or set up a new sweep module under `hf_jobs/sweeps/`. Trigger phrases: "new sweep", "add a sweep", "scaffold sweep", "factor this out to HF Jobs", "make this a sweep module".'
---

# New HF Jobs Sweep

Scaffold a new parameter sweep that follows the conventions in [AGENTS.md](../../AGENTS.md) "Heavy compute" and the dispatcher contract in [hf_jobs/run_sweep.py](../../hf_jobs/run_sweep.py).

## When to use

- A notebook cell takes more than ~30 s locally and is a parameter sweep (not just a long single computation).
- The user wants to factor a sweep out of a notebook into a reusable module.
- A new Phase 2C / 2D slice needs its own grid evaluation.

Do **not** use for one-off computations or symbolic derivations — those stay in the notebook.

## Procedure

1. **Confirm the sweep name** with the user. Use `snake_case` matching the slice or notebook (e.g. `shift_families`, `krasnikov_tube`, `fell_heisenberg`). The same name will be used for all three files.

2. **Inspect an existing sweep** as the template. Good references:
   - [hf_jobs/sweeps/shift_families.py](../../hf_jobs/sweeps/shift_families.py) — symbolic-pipeline-at-import-time pattern.
   - [hf_jobs/sweeps/krasnikov_tube.py](../../hf_jobs/sweeps/krasnikov_tube.py) — pure-numeric pattern.
   - [hf_jobs/configs/shift_families_preview.json](../../hf_jobs/configs/shift_families_preview.json) and `_full.json` for config shape.

3. **Create `hf_jobs/sweeps/<name>.py`** exposing exactly two callables:
   - `build_grid(config: dict) -> list[dict]` — expand the JSON axes spec into a list of point dicts.
   - `evaluate(point: dict) -> dict` — evaluate one point, return a flat scalar record (all values must be `parquet`-friendly: float/int/str/bool, no arrays).

   The module must be importable as `hf_jobs.sweeps.<name>` (no top-level side effects beyond the symbolic-build-once pattern that existing modules use).

4. **Create paired configs in `hf_jobs/configs/`:**
   - `<name>_preview.json` — small grid that runs locally in **under 30 seconds** on 4 workers. This is the smoke test.
   - `<name>_full.json` — the real grid for HF Jobs `cpu-upgrade`. Add a top-level `"_comment"` field describing the expected runtime and point count.

   Axes use the standard schema: `{"lo": float, "hi": float, "n": int, "scale": "log" | "linear"}`. Single-value axes use `"n": 1` or `"lo" == "hi"`.

5. **Run the preview locally** to verify the schema and rough timing:
   ```powershell
   python hf_jobs/run_sweep.py <name> --config hf_jobs/configs/<name>_preview.json
   ```
   Output lands in `sweeps/<name>_<timestamp>.parquet` with a sibling `.json`. Open the parquet and confirm the columns are what the consuming notebook expects.

6. **Print the HF Jobs dispatch invocation** for the user (do not run it — it costs money). Use the form from [README.md](../../README.md) "Hugging Face Jobs":
   ```bash
   hf jobs run --flavor cpu-upgrade \
       -e HF_JOB=1 -v $PWD:/work python:3.12 \
       bash -c "cd /work && pip install -q -r requirements.txt && \
                python -m hf_jobs.run_sweep <name> \
                    --config hf_jobs/configs/<name>_full.json"
   ```

7. **Don't update notebooks or NAVIGATOR.md** as part of this skill — that's the user's call. Just report the three files created and the preview's pass/fail.

## Anti-patterns

- Inlining sweep code in a notebook cell instead of a module — sweeps must be importable.
- Returning numpy arrays or nested dicts from `evaluate` — parquet can't round-trip them; flatten to scalars.
- Skipping the preview config — the only safety net before billable HF Jobs runs.
- Creating a `<name>_full.json` that runs in seconds — that should be the preview. The full grid should be order minutes-to-tens-of-minutes on `cpu-upgrade`.
- Adding new top-level keys to the config schema without checking [hf_jobs/run_sweep.py](../../hf_jobs/run_sweep.py) `_merge_config_defaults` — non-axis top-level keys are merged into every point as fixed scalars.

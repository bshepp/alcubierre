# Agent Instructions — Alcubierre Boundary-Mode Reformulation

This is a **personal research landscape exploration**, not a paper-driven programme and not a software product. There are no users, no releases, and no concrete deliverables. The goal is to map the structure of obstructions to a working classical warp drive.

Before doing anything non-trivial, read [NAVIGATOR.md](NAVIGATOR.md). It is the authoritative front door (load-bearing-assumptions table, current open question, document index). [README.md](README.md) is the public-facing version of the same material.

## Project mode and tone

- **Surfing, not paper-writing.** Don't add deliverable scaffolding, abstracts, or "publication-ready" framing.
- **Honest accounting is mandatory.** Every claim is reported with its **slice of parameter space** (which assumptions it depends on). See [TRUST_AUDIT.md](TRUST_AUDIT.md) for the A/B/C grading scheme — A = derived in our notebooks, B = accepted from a specific paper but spot-checkable, C = heuristic. New results inherit this discipline.
- **No oversold conclusions.** "Within the slice X, no useful classical warp drive exists" is acceptable. "Warp drives are impossible" is not.
- **Don't invent physics.** If a claim isn't in the literature, our notebooks, or derivable in front of the user, flag it as speculation.

## Repository layout

| Path | Purpose |
|------|---------|
| `*.ipynb` | Primary research artifacts. Each major notebook has a paired `*_NOTES.md` companion (e.g. [shift_families.ipynb](shift_families.ipynb) ↔ [SHIFT_FAMILIES_NOTES.md](SHIFT_FAMILIES_NOTES.md)). |
| `*_EVALUATION.md` | Critical readings of specific external papers (Rodal 2025, Krasnikov 2003, Fell-Heisenberg 2021). |
| `hf_jobs/sweeps/` | Pure-Python sweep modules — one per heavy parameter sweep. Each exposes `build_grid(config)` and `evaluate(point)`. Do not inline these into notebooks; notebooks call them via `hf_jobs.run_sweep`. |
| `hf_jobs/configs/` | JSON configs paired `*_preview.json` (small grid, runs locally in seconds) and `*_full.json` (HF Jobs `cpu-upgrade`). |
| `sweeps/`, `sweeps_remote/` | Sweep outputs (`.parquet` + sibling `.json`). Treat as artifacts, not source. |
| `agent-tools/` | Throwaway scripts written by previous agents (`diag_*`, `fix_*`, `inspect_*`, `dump_*`, `run_nb.py`, `clear_outputs.py`). Re-use the utility scripts; do not promote `diag_*`/`fix_*` scratch into permanent infrastructure. |
| `papers/`, `papers/extracted/`, `papers/_originals/` | Reference PDFs and slimmed text extracts. Do not commit new full-PDF originals; use `agent-tools/slim_pdf.py` / `slim_papers.py` if a paper needs to be added. |
| `speculation/` | Long-shot ideas explicitly flagged as not-yet-derived. |

## Working with notebooks

- Use `read_file` / `edit_notebook_file` / `run_notebook_cell` for notebook work — never edit `.ipynb` JSON by hand.
- To run a notebook end-to-end from the terminal: `python agent-tools/run_nb.py <notebook.ipynb>` (uses `nbclient`, 600 s timeout, executes in-place).
- To strip outputs before commit when needed: `python agent-tools/clear_outputs.py <notebook.ipynb>`. The repo does **not** auto-strip outputs — committed outputs are intentional documentation in most cases. Ask before clearing a notebook the user has been iterating on.
- Don't reorder, renumber, or "tidy" cells in research notebooks. Cell numbers are referenced from `_NOTES.md` files (e.g. "Cell 4b Schwarzschild regression").

## Heavy compute: HF Jobs and the preview/full discipline

Parameter sweeps that take more than ~30 s locally must be factored into `hf_jobs/sweeps/<name>.py` with two configs in `hf_jobs/configs/`:

1. `<name>_preview.json` — small grid; **always runs locally first** as a smoke test.
2. `<name>_full.json` — full grid; dispatched via the `hf jobs run --flavor cpu-upgrade ...` invocation shown in [README.md](README.md) "Running the notebooks → Hugging Face Jobs".

HF Jobs is billed per second. Never dispatch a full grid without first running the preview locally and checking the schema of the resulting `.parquet` matches what the notebook expects.

Local sweep dispatch:

```powershell
python hf_jobs/run_sweep.py <sweep_name> --config hf_jobs/configs/<sweep_name>_preview.json
```

On Windows the dispatcher caps workers at `min(4, cpu - 1)` to avoid OpenBLAS heap exhaustion — don't override this without a reason.

## Python environment

- Python 3.12+. Pinned versions in [requirements.txt](requirements.txt) (sympy 1.14, numpy 2.4, scipy 1.16, matplotlib 3.10, pandas 2.3, pyarrow 17–22, huggingface_hub 1.5+).
- Heavier numerics for the GW-recoil cells of [acceleration.ipynb](acceleration.ipynb) require [requirements-gw.txt](requirements-gw.txt) (used on HF Jobs / Colab).
- Don't add dependencies casually. New deps must be pinned and justified in the PR / notes.

## Documentation conventions

- **Link, don't duplicate.** [NAVIGATOR.md](NAVIGATOR.md), [README.md](README.md), and [LANDSCAPE_SYNTHESIS.md](LANDSCAPE_SYNTHESIS.md) reference the same material from different angles; cross-link rather than restate.
- **Don't create new top-level summary docs to "document changes."** Update the existing tables in [NAVIGATOR.md](NAVIGATOR.md) (load-bearing-assumptions table, document index) and the relevant `_NOTES.md`. Append-only updates to [SESSION_LOG.md](SESSION_LOG.md) and [TRUST_AUDIT.md](TRUST_AUDIT.md) are how progress is recorded.
- Use math in markdown: inline `$...$`, display `$$...$$`. SymPy expressions in notebooks are the canonical source; markdown reproduces them for readability.
- File references in markdown use repo-relative paths in `[backticks](path)` — see existing tables for the pattern.

## Things to avoid

- Refactoring notebooks "for clarity" without an explicit ask.
- Promoting `agent-tools/diag_*` or `fix_*` scratch into the main codebase.
- Adding test frameworks, CI, linters, or pre-commit hooks — none exist by design.
- Editing `papers/_originals/` or committing new full PDFs.
- Re-running long-finished sweeps on HF Jobs without checking whether the output already lives in `sweeps/` or `sweeps_remote/`.
- Dropping the slice-scope qualifier from a result when summarising it.

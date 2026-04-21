# `fell_heisenberg_symbolic/` — Task 2D.5e artifacts

Outputs of [`hf_jobs/analysis/fell_heisenberg_symbolic.py`](../hf_jobs/analysis/fell_heisenberg_symbolic.py) (Hard Fix — Symbolic Boundary Extraction). See [`FELL_HEISENBERG_SWEEP_NOTES.md`](../FELL_HEISENBERG_SWEEP_NOTES.md) §12 for the full story.

## Files (committed)

- `validation_subtask_1.json` — Hessian validation results vs numerical pipeline; Checkpoint A status
- `validation_subtask_2.json` — ADM stress-energy validation results; Checkpoint B status
- `validation_subtask_3.json` — Hybrid eigenvalue validation results + sub-task 3 wall finding; Checkpoint C status
- `symbolic_artifacts.tex` — LaTeX summary of the validated symbolic pipeline (sub-tasks 1-2). Stub: full expressions are too large to render.

## Files (gitignored, regeneratable)

- `symbolic_artifacts.py` — Python-loadable srepr serialisation of the validated symbolic Hessian + ADM stress-energy. **~15 MB**. Regenerate with:

  ```powershell
  cd F:\science-projects\alcubierre
  python -W ignore -m hf_jobs.analysis.fell_heisenberg_symbolic --out-dir fell_heisenberg_symbolic --subtask 2
  # then run the serialisation block from the bottom of this README, or
  # extract the artifacts directly from the module (functions are exported).
  ```

  Build time: ~5-10 sec for the symbolic pipeline + ~10 sec for srepr serialisation.

## Verdict

Sub-tasks 1 and 2 succeed: the symbolic Hessian and ADM stress-energy are validated to 4th-order FD truncation precision against the numerical pipeline at the canonical anchor. Sub-task 3 (symbolic eigenvalue extraction) **hits a wall**: `S.det()` does not terminate in reasonable time on the FH `S_ij` matrix. The symbolic-numerical hybrid path (sub-task 3 outcome B) succeeds technically but adds no information beyond what the existing numerical pipeline + §10 polynomial fit already provide.

The intended Task 2D.5e deliverable — a closed-form analytic boundary equation $S(\sigma, m_0, a, \ell, r) = 0$ — is **not achievable within the FH ansatz given current SymPy capabilities**. See §12 of the sweep notes for the calibrated honest summary.

## Un-attempted fallback (still open)

The original §8.2 plan listed two fallback paths if the symbolic interior minimisation failed; only one was tried (the symbolic-numerical hybrid, `validation_subtask_3.json`). The other — the **Z-axis-symmetry fallback** — was never executed:

- **Idea:** the FH potential is rotationally symmetric in the $X$-$Y$ plane (after the Pi=0.25 fixing), so on the $X=Y=0$ axis the off-diagonal components of $S_{ij}$ vanish by symmetry and the matrix is already diagonal. Eigenvalues are then read off the diagonal directly, sidestepping the `det()` wall entirely. The interior minimisation reduces to a 1-D problem $\min_Z S_{\rm pt}(0, 0, Z; \text{params})$ that SymPy can plausibly handle.
- **Pre-flight requirement:** before any symbolic effort, verify on the existing numerical sweep + horizon data that the slack-minimum location actually sits at $X = Y = 0$ for the canonical anchor. If the global slack minimum drifts off-axis the fallback is unsound.
- **Yellow flag from the horizon data:** [`fell_heisenberg_horizon/leaderboard.csv`](../fell_heisenberg_horizon/leaderboard.csv) reports `N_max_pos = (-0.5, 0, 0)` for the top-ranked configuration — i.e. the *shift-magnitude* maximum sits off-axis in the $X$ direction. This is *not* the slack minimum (different quantity), but it shows the FH bubble's spatial structure is not perfectly $X$-$Y$ axisymmetric in this slice and warrants checking before assuming axis-localised slack minima.

No work was performed on this path; it is recorded here so a future agent (or revisit) does not re-derive the option from scratch.


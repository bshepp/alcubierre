# warp_factory_py

Clean-room NumPy re-implementation of the
[WarpFactory](https://github.com/NerdsWithAttitudes/WarpFactory) (Helmerich &
Fuchs, MIT 2023) toolkit primitives needed by this repo's Phase 3 work.

## Why a port

`warp_factory_repro/` holds the canonical MATLAB ground-truth runs (Alcubierre
EC reproduction, Fuchs Fig.10 κ-bracket reproduction, κ-surface sweep).
Continuing Phase 3 work (e.g. Task 3.3 sweeps) currently requires MATLAB. No
license tier we have access to permits the kind of research use this repo
performs, so we re-implement the small slice of WarpFactory we actually depend
on, in NumPy, from the algorithm spec.

## License posture

Upstream is **MIT**; permissive. This port is an independent NumPy rewrite
from the published algorithms — no MATLAB source is copied or translated
line-by-line. Files that mirror an upstream concept (e.g. the 4th-order
central FD stencil, the Eulerian-frame transformation) cite the upstream
function name in their docstring for traceability.

This subpackage inherits the parent repository's license.

## Scope (Phase A + B)

Phase A — Alcubierre Eulerian-observer EC reproduction:

- `metrics/alcubierre.py` — `metric_alcubierre(grid, world_center, v, R, sigma)`
- `utils/fd_stencils.py` — 4th-order central first derivative
- `solvers/christoffel.py`, `ricci.py`, `einstein.py`, `energy_tensor.py`
- `solvers/frame.py` — Cholesky-based Eulerian transformation
- `solvers/energy_conditions.py` — null/weak/dominant/strong conditions

Phase B — Fuchs Warp Shell κ-bracket reproduction:

- `solvers/tov.py` — TOV interior solver
- `metrics/warpshell.py` — comoving Warp Shell

Anything beyond these (GUI, plotting helpers, additional metrics) is
explicitly out of scope.

## Anchors (must reproduce within tolerance)

- **Alcubierre canonical** (`v=1c`, `R=4`, `sigma=8`, grid 80×80×5,
  `dx=0.2`, in-mask `r ≤ 4.25 m`): Pass=0.0737, min(NEC)=−9.59e43,
  min(DEC)=−4.04e43, min(SEC)=−5.88e43. Tolerance: ±0.5 pp on Pass,
  ±5 % on min(EC).
- **Fuchs Fig.10** at full grid: κ-bracket `(5, 7]`. Session 18 finer
  bracket `(4.17, 5.83]`.

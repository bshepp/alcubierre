# Release notes — v0.1.0

First archived snapshot of the Alcubierre boundary-mode reformulation project. Tagged so it can be
mirrored to Zenodo for a citable DOI. This is a checkpoint of an active personal research
exploration, not a finished result.

## What this snapshot contains

- **Phase 1** (linearization & feasibility) — derivation in [`LINEARIZATION_CALCULATION.md`](LINEARIZATION_CALCULATION.md), symbolically + numerically verified in [`verification.ipynb`](verification.ipynb).
- **Phase 2A** (classical matter-shell, static slice) — Fuchs-shell existence anchor, $\Delta_{\min}/R = \kappa\beta/C$ thickness scaling, acceleration analysis, Israel-junction infrastructure ([`matter_shell.ipynb`](matter_shell.ipynb), [`thickness_bound.ipynb`](thickness_bound.ipynb), [`acceleration.ipynb`](acceleration.ipynb), [`israel_junction.ipynb`](israel_junction.ipynb), [`krasnikov_tube.ipynb`](krasnikov_tube.ipynb), [`hybrid_wall.ipynb`](hybrid_wall.ipynb)).
- **Phase 2C** (six adjacent slices) — alternate shift families, Fuchs+Krasnikov hybrid wall, time-dependent acceleration, Krasnikov-2003 QI, cosmological exterior, modified gravity. All six independently null inside their slice scopes.
- **Phase 2D** (Fell-Heisenberg multi-mode irrotational ansatz) — 1404/15000 strict-pass cells; 4 structural tests (anchor reproducibility, V² scaling, xAct re-implementation, connectivity/topology) plus VIQ + horizon dismantlings. Outputs in [`fell_heisenberg_topology_hires/`](fell_heisenberg_topology_hires/), [`fell_heisenberg_horizon/`](fell_heisenberg_horizon/), [`fell_heisenberg_symbolic/`](fell_heisenberg_symbolic/).
- **Phase 3** (independent numerical verification) — Warp Factory MATLAB cross-check of the Fuchs anchor (TRUST_AUDIT #3 closes B → A) and 162-build κ-surface sweep across $(M, R_2, \beta)$ identifying high-velocity + low-compactness cells as null configurations. Outputs in [`warp_factory_repro/`](warp_factory_repro/).
- **Static research website** ([`webpage/`](webpage/)) — eight pages with light/dark theme, rendering the results above with direct links to data artifacts.
- **Provenance** — [`NAVIGATOR.md`](NAVIGATOR.md), [`TRUST_AUDIT.md`](TRUST_AUDIT.md), [`SESSION_LOG.md`](SESSION_LOG.md), [`LANDSCAPE_SYNTHESIS.md`](LANDSCAPE_SYNTHESIS.md), [`ROADMAP.md`](ROADMAP.md) and per-notebook `*_NOTES.md` companions.

## What is explicitly *not* claimed

- This is **not** a no-go theorem against warp drives. The composite finding is "within the explored slices, no useful classical warp drive exists." Slice scopes are recorded in `NAVIGATOR.md`'s load-bearing-assumptions table.
- Phase 2B (Casimir / semiclassical) and Phase 3.3 (nested + non-spherical Fuchs constructions) remain open.
- A live cpu-xl Hugging Face Jobs run for Fell-Heisenberg at $N_\text{pts}=129$ was in flight at tag time; results land in [`sweeps_remote/`](sweeps_remote/) post-tag and will appear in v0.2.

## Companion artifacts

- Live mirror with Parquet preview: [Hugging Face Dataset `bshepp/alcubierre-sweeps`](https://huggingface.co/datasets/bshepp/alcubierre-sweeps).
- Source repository (canonical): <https://github.com/bshepp/alcubierre>.

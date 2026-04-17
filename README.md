# Alcubierre Warp Drive — Boundary-Mode Reformulation

## Project Overview

This project investigates whether the exotic matter required by the Alcubierre warp drive metric can be reinterpreted as a **boundary effect** rather than an independent material source. The original hypothesis proposed a "method of images" reformulation in linearized gravity; the mathematics has since refined this into a **boundary-mode decomposition** approach grounded in the Casimir analog.

## Core Claim

The negative energy density in the Alcubierre bubble wall is not a substance to be manufactured. It is the second-order energy stored in a gravitomagnetic field configuration constrained by boundary conditions — structurally analogous to how the Casimir effect produces negative energy density between conducting plates. Whether this analogy is merely structural, reflects a shared physical mechanism, or can be replaced by a purely classical matter-shell construction is pursued along two parallel tracks (see below).

## Current Status

**Phase 1 — Linearization and feasibility analysis: IN PROGRESS**
**Phase 2A — Classical matter-shell realization (primary track): CLASSICAL HALF COMPLETE (Sessions 5–8)**
**Phase 2B — Casimir / boundary-mode decomposition (parallel track): NEXT, with sharpened search target**

The explicit linearization calculation is complete; all key expressions are verified symbolically and numerically in `verification.ipynb`. Path 2A's classical research programme closed in Session 8 with four results: (i) DEC-compatible static spherical Fuchs shells exist with $\Delta_{\min}/R = \kappa\beta/C$; (ii) no classical mechanism accelerates such shells in vacuum; (iii) static-infrastructure Krasnikov tubes have no classical-matter wall for any $\eta > 0$; (iv) Krasnikov-tube networks generate CTCs (Everett–Roman 1997). Composite: no classical positive-matter warp drive is simultaneously useful, accelerable, and DEC-compatible.

- **Path 2A (primary, classical half done):** Anchored on Fuchs et al. 2024's *Constant Velocity Physical Warp Drive Solution* (arXiv:2405.02709). See [`MATTER_SHELL_PATH.md`](MATTER_SHELL_PATH.md), [`matter_shell.ipynb`](matter_shell.ipynb), and the Packages 1–3 + Task 2A.13 notebooks. The classical static and dynamical halves are both fully closed; the only remaining open question is whether a quantum-field source can supply the warp metric — that's Path 2B.
- **Path 2B (next, sharpened):** The Casimir / semiclassical programme is now the sole remaining candidate for any *useful* dynamical or transport-relevant warp geometry. The Rodal 2025 evaluation ([`RODAL2025_EVALUATION.md`](RODAL2025_EVALUATION.md)) sharpens the QFT-search target from generic isotropic vacuum energy to **anisotropic transverse vacuum stresses with positive normal energy density** (waveguide-confined Casimir, asymmetric-plate Casimir, repulsive-Casimir geometries). See [`QUANTUM_CLASSICAL_BRIDGE.md`](QUANTUM_CLASSICAL_BRIDGE.md) §6 and the new Session-7 update there.

See `MATTER_SHELL_PATH.md` §6 for the four outcome scenarios and §9 for the complete Path 2A closure.

## Documents

| File | Contents |
|------|----------|
| [ALCUBIERRE_IMAGE_METHOD.md](ALCUBIERRE_IMAGE_METHOD.md) | Original seed document — image-method hypothesis, GEM framework, proposed calculation sequence |
| [ALCUBIERRE_MARCH30_INTEGRATION.md](ALCUBIERRE_MARCH30_INTEGRATION.md) | Integration addendum — literature review, Casimir connection, research context |
| [LINEARIZATION_CALCULATION.md](LINEARIZATION_CALCULATION.md) | Complete linearization derivation, ADM stress-energy, Poisson structure, image method analysis, and boundary-mode pivot |
| **[MATTER_SHELL_PATH.md](MATTER_SHELL_PATH.md)** | **Path 2A (primary) — classical matter-shell realization, Fuchs et al. mapping, Israel junction conditions** |
| [QUANTUM_CLASSICAL_BRIDGE.md](QUANTUM_CLASSICAL_BRIDGE.md) | Path 2B (parallel) — quantum vs. classical gap, three-tiered claim structure, Casimir route |
| [LITERATURE.md](LITERATURE.md) | Full literature catalog with abstracts, arXiv links, and relevance notes |
| [ROADMAP.md](ROADMAP.md) | Research phases, decision points, and open questions |
| [SESSION_LOG.md](SESSION_LOG.md) | Chronological record of work sessions and findings |
| [verification.ipynb](verification.ipynb) | SymPy/numpy notebook verifying all key expressions from the linearization calculation |
| **[matter_shell.ipynb](matter_shell.ipynb)** | **Path 2A notebook — Fuchs bump function, Israel junction, angular decomposition, EC scaling** |
| **[israel_junction.ipynb](israel_junction.ipynb)** | **Path 2A Package 1 (Task 2A.6) — full Israel junction Part A (static) + Part B (boosted), angular decomposition of $[K_{ab}]$, DEC boundary, critical $\lambda_*$** |
| **[thickness_bound.ipynb](thickness_bound.ipynb)** | **Path 2A Package 2 (Task 2A.7) — minimum shell thickness scaling law $\Delta_{\min}/R = \kappa\beta/C$, numerical sweep, Fuchs comparison** |
| **[acceleration.ipynb](acceleration.ipynb)** | **Path 2A Package 3 (Task 2A.10) — ADM 4-momentum obstruction, three-mechanism catalog, GW-recoil quantitative ceiling via HF Jobs + Varma 2022 rescaling** |
| **[krasnikov_tube.ipynb](krasnikov_tube.ipynb)** | **Path 2A Task 2A.13 — Krasnikov 4D metric + Fuchs-class thick wall; reproduces Everett–Roman Eq. 14 symbolically; universal scaling law $\rho_p^{\min} \propto -\eta/\epsilon^2$; HF Jobs sweep returns WEC pass rate 0.0000. Closes the speculation document.** |
| [RODAL2025_EVALUATION.md](RODAL2025_EVALUATION.md) | Critical evaluation of arXiv:2512.18008 (Rodal, Gen. Rel. Grav. 58:1, 2026): irrotational warp drive with 38× peak-deficit reduction; updated Path 2B search target |
| [KRASNIKOV_TUBE_NOTES.md](KRASNIKOV_TUBE_NOTES.md) | Quantitative synthesis of Krasnikov 1995 / Everett–Roman 1997 / Krasnikov 2003 prior art; comparison to Path 2A; Task 2A.13 update note |

## Key Results So Far

1. The Alcubierre spatial geometry is **exactly flat** — all warp content lives in the shift vector $\beta^x = -v_s f(r_s)$
2. The warp drive is **gravitomagnetic at leading order** — frame-dragging, not Newtonian potential
3. The shift vector satisfies a **Poisson equation** with source localized at the bubble wall
4. Point-image decomposition **does not work** (constant interior field incompatible with point sources)
5. The **Casimir/boundary-mode interpretation is strengthened** — this is the correct mathematical framework
6. The project pivoted from "method of images" to **"boundary-mode decomposition"**
7. **Fuchs et al. 2024 is a direct realization of the boundary-mode framework** with a classical matter shell — no quantum effects required. This is the anchor for Path 2A.
8. On a sphere centered on the bubble, the Alcubierre shift is a **pure $l = 1$ dipole** in the radial projection (verified in `matter_shell.ipynb` §4)
9. Order-of-magnitude scaling for the matter-shell route: $\beta_\text{warp} \lesssim GM\Delta^2/(R^3 c^2)$ — agrees with Fuchs's empirical bound $\beta \le 0.02$ to within an order of magnitude
10. The thin-shell (Israel) junction for a static Schwarzschild + Minkowski match reproduces the standard weak-field shell mass $\mu \approx M + GM^2/(2R)$ — notebook framework validated against textbook result
11. **Path 2A minimum shell thickness scaling law** (Task 2A.7, `thickness_bound.ipynb`): $\Delta_{\min}/R = \kappa\,\beta/C$ with $C = 2GM/(Rc^2)$ and $\kappa \in [0.05, 0.75]$. Trades the Alcubierre exotic-energy requirement ($\sim 10^{30}$ kg of negative energy) for a positive-energy compactness requirement ($\sim 10^{19}$–$10^{20}$ kg of ordinary matter at $R = 100$ m, $\beta = 0.5$)
12. **Part B critical $\lambda_*$ acceleration obstruction** (Task 2A.6, `israel_junction.ipynb` Part B): for thin-wall parameters, DEC fails during accelerating transients at $\lambda = v_{\rm ext}/v_{\rm int} < \lambda_* \approx 0.55$. Isolates acceleration as the remaining open problem (Task 2A.10)
13. **Path 2A dynamical closure** (Task 2A.10, `acceleration.ipynb`): ADM 4-momentum conservation rules out self-acceleration in vacuum; three-mechanism catalog leaves only ordinary mass ejection as viable. GW-recoil ceiling $\lesssim 0.25\%$ of $v_{\rm warp}$ under most favourable Fuchs-compatible parameters (HF Jobs sweep + SXS rescaling of Varma et al. 2022). Strictly strengthens Schuster–Santiago–Visser 2023 Theorem 3; elevates Path 2B to the sole remaining route to a dynamical drive
14. **Path 2A static-infrastructure closure** (Task 2A.13, `krasnikov_tube.ipynb`): symbolic Einstein-tensor pipeline reproduces Everett–Roman 1997 Eq. 14 exactly; universal scaling law $\rho_p^{\min}(\eta, \epsilon) = -\kappa_K(\eta)/\epsilon^2$ with $\kappa_K(\eta) \approx 0.122\,\eta$ at small $\eta$, verified to 14-decimal $\epsilon$-independence; HF Jobs preview sweep returns **WEC pass rate 0.0000** across 300 $(\eta, \epsilon, n)$ points. Establishes the unobservability tradeoff: $|\rho_p^{\min}|$ and the observable lightcone opening both scale as $\eta$, so their ratio is fixed and a Krasnikov tube cannot be made simultaneously useful and energy-condition-friendly. Closes the `speculation/RING_NETWORK_CONCEPT.md` static-infrastructure-network branch

## Running the notebooks

All notebooks run locally on any Python 3.12+ environment with the pinned scientific stack from [`requirements.txt`](requirements.txt). For heavier parameter sweeps and the GW-recoil numerics in [`acceleration.ipynb`](acceleration.ipynb), two external compute paths are wired up:

| Notebook | Local default | Recommended for heavy cells |
|---|---|---|
| [verification.ipynb](verification.ipynb) | Yes | — (pure symbolic) |
| [matter_shell.ipynb](matter_shell.ipynb) | Yes | — (moderate numerics) |
| [israel_junction.ipynb](israel_junction.ipynb) | Yes for cells 1–7, 10–15 | Cell 8 sweep: HF Jobs `cpu-upgrade` or Colab CPU |
| [thickness_bound.ipynb](thickness_bound.ipynb) | Yes for analytical cells | Cell 6 sweep: HF Jobs `cpu-upgrade` |
| [acceleration.ipynb](acceleration.ipynb) | Yes for cells 1–8 | Cells 9–12 (NR / GW recoil): HF Jobs `cpu-upgrade` with `requirements-gw.txt` |
| [krasnikov_tube.ipynb](krasnikov_tube.ipynb) | Yes for all cells | Cell 19 sweep: HF Jobs `cpu-upgrade` recommended for full $\sim 30{,}000$-point grid; preview ($\sim 300$ points) runs in ~3 s locally |

### Google Colab

Click the "Open In Colab" badge at the top of any notebook. The first code cell auto-installs [`requirements.txt`](requirements.txt) when `google.colab` is detected, so no manual setup is needed. Free T4 GPUs work for any GPU-accelerated cell but none of the current notebooks require GPU.

### Hugging Face Jobs

Heavy parameter sweeps are factored out of the notebooks into sweep modules under [`hf_jobs/sweeps/`](hf_jobs/sweeps/) and dispatched via [`hf_jobs/run_sweep.py`](hf_jobs/run_sweep.py). Typical invocation from a notebook cell:

```bash
hf jobs run --flavor cpu-upgrade \
    -e HF_JOB=1 -v $PWD:/work python:3.12 \
    bash -c "cd /work && pip install -q -r requirements.txt && \
             python -m hf_jobs.run_sweep <sweep_name> \
                 --config hf_jobs/configs/<sweep_name>_full.json"
```

Outputs land in `sweeps/<sweep_name>_<timestamp>.parquet`. Each sweep ships with a `*_preview.json` config (small grid, runs locally in seconds) and a `*_full.json` config (full grid, runs on HF Jobs in minutes). Always validate the preview locally before dispatching the full grid — HF Jobs is billed per second and the preview is the safety net.

Large sweep outputs and the Package 3 NR data optionally mirror to a Hugging Face dataset repo; see `MATTER_SHELL_PATH.md` §3.4 and §7 for the specific dataset slugs once created.

## References (Core)

- Alcubierre 1994 (gr-qc/0009013) — The metric
- Lobo & Visser 2004a (gr-qc/0406083) — Fundamental limitations on warp drives; linearized analysis (must read)
- Lobo & Visser 2004b (gr-qc/0412065) — Linearized warp drive and energy conditions (companion paper)
- Fuchs, Helmerich, Bobrick et al. 2024 (2405.02709) — Physical warp drive with all energy conditions satisfied
- Santiago, Schuster & Visser 2021 (2105.03079) — No-go theorems for positive-energy superluminal drives
- Helmerich et al. 2024 (2404.03095) — Warp Factory numerical toolkit
- Quach 2015 (1502.07429) — Gravitational Casimir effect (key for quantum/classical bridge)
- Ford & Pfenning 1998 (gr-qc/9805037) — Quantum inequalities in curved spacetime
- Full literature table in [LITERATURE.md](LITERATURE.md)

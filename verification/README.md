# verification/

Tracked, version-controlled **reusable verification and adjudication
harnesses** — the instruments that implement this project's verification
methodology. These are kept (not discarded as scratch) so that *how* a
result was checked stays reproducible alongside the result itself.

Contents:

- **Validation suites** — certify a solver against closed-form limits
  (e.g. `test_axisym_validate.py`: flat → 0, Schwarzschild → exact
  Ricci-flat, Alcubierre gravitomagnetic scaling).
- **Cross-checks** — independent-pipeline agreement
  (`test_axisym_xcheck.py`; `cross_check_xact*` + `fh_rho_at_points*.wls`
  are the Wolfram/xAct cross-pipeline arbiter).
- **Ground-truth adjudicators** — `test_prongB_groundtruth.py`: a
  certified-exact (GR-validated) closed-form Einstein-tensor reference
  used to adjudicate which numerical pipeline is trustworthy for a given
  regime. `test_shift_families_frame_adjudication.py`: 20-gate battery
  behind the Session-36 Slice-1 frame-projection correction — symbolic
  tetrad-orthonormality certificate, 3+1-constraint vs 4D-Einstein route
  agreement, the profile-independent identities that close all four
  shift families analytically, permanent regression of the fixed sweep
  module, and a warp_factory_py anchor cross-check.
  `test_sxs_kick_pull.py`: plain-HTTPS pull of SXS catalog + per-record
  metadata behind the Session-37 TRUST_AUDIT #5 closure (GW-recoil kick
  anchor verified conservative vs every public NR simulation; offline =
  SKIP, never a false verdict).
  `test_nested_shell_radial_ladder.py`: the Session-39 certified-radial
  f_inner ladder that REVERSED the Session-26 nested-shell record
  (improvement plateau + sign flip at f* ~ 0.63; modes full / plateau /
  threshold for staged RES_CONF confirmation).
- **Adversarial kill-test batteries** — `test_profile_kill.py`,
  `test_radial_opt_xcheck.py`, `test_radial_opt_convergence.py`,
  `test_prongA_forensic.py`: resolution-convergence, cross-representation
  invariance, and forensic-localization tests that try to *falsify* an
  apparent positive.
- **Anchor reproductions / smokes / optimizer drivers** behind committed
  `warp_factory_py` results (`test_fuchs_fig10_repro.py`,
  `test_alcubierre_anchor_nt1.py`, `test_*_shell_*`,
  `test_profile_radial_optimize.py`).

Run with the repo root on `PYTHONPATH`, e.g.
`PYTHONPATH=. python verification/test_prongB_groundtruth.py`.

True one-off scratch (`diag_*`, `fix_*`, `*_scratch`, `dump_*`, run logs)
stays gitignored in `agent-tools/` — see `AGENTS.md` "Repository layout".

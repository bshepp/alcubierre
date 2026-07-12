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
  `test_delta_ladder_radial.py`: the Session-41 certified-radial
  27-cell Delta-ladder re-run (Session-18 anchor confirmed + tightened;
  kappa = 4.93 +/- 0.44 over genuine crossings; nulls verified at the
  scout peak, never at a boundary).
  `test_fh_axisym_closed_form.py`: the Session-42 battery behind Task
  2D.5e -- closed-form FH principal pressures via the axisymmetric block
  decomposition (symbolic zero certificates, machine-precision eigenvalue
  agreement) and the far-field certificate that the FH strict-pass record
  was L=12-box-scoped (equatorial WEC+DEC violation at finite R* for all
  tested a > 0; FD cross-check at L=45).
  `test_lentz_full_wec.py`: the Session-45 battery behind Task 3.7 --
  Lentz 2020 closed NEGATIVE at class level (inline 1+1 PDE residual,
  plane-evaluator == Eq.-17 det-Hess identity, unidirectional-front
  certificates: rho_E = 0 marginal while full WEC/DEC strictly violated
  on 100% of the front core, exact quadratic amplitude scaling).
  `test_gz_desitter_reproduction.py`: the Session-46 battery behind
  audit-queue Block 3(c) -- Garattini-Zatrimaylov 2025 reproduced
  EXACTLY (Eq. 6 == Hamiltonian constraint; Eqs. 14/17/18/23
  symbolic-exact for generic profiles; full-4D Einstein-tensor
  cross-checks of the exact moving-bubble metric at machine precision;
  exact mass-conserving rearrangement; the paper's K-convention pinned)
  plus the sharpenings: unmatched-trajectory control (Hubble matching
  is load-bearing), local-violation quantification (wall-shape-set
  multiple of rho_hat with an exact 1/L^2 scale lock), and the ANEC
  probe (strictly violated on every wall-crossing null geodesic;
  miss-ray control identically zero; compact-support profile required
  by the flat-patch past-incompleteness).
  `test_mmin_nested_map.py`: the Session-47 adjudicator for the nested
  two-body minimal-mass map -- audit gates (f=0 baselines EXACT vs
  the S32 single-shell map; bracket honesty on every pass row; no_pass
  basis explicit) + certify mode (RES_CONF escalation with walk-up
  correction and an improvement-survival gate; canonical-cell floor
  re-based 2.568e27 -> 2.2256e27 nominal, -13.3%).
  `test_mmin_graded_map.py`: the Session-48 adjudicator -- graded-wall
  map audit/certify (bounded NEGATIVE: 0/80 members below the
  single-shell floor, best +1.2% RES_CONF-confirmed) plus the
  reproducible S47 kill-tests: GATE M (mask equivalence at the S47
  winner, rel diff 0) and GATE D (cross-builder discriminator at
  identical nominal rho -- per-shell-TOV 0.8824x vs single-TOV 1.1409x
  of the S32 floor; the S47 lever is the two-body pressure ansatz).
  `test_spinup_margin.py`: the Session-49 adjudicator for the 2E.1
  spin-up margin surface -- static-limit row re-checks (<= 6e-14),
  quasi-static corridor gate (clean for all three certified configs),
  surface sanity, and tau* extraction (fastest EC-clean spin-up
  ~0.4-0.8 R2/c; DEC binds near the floor; log-grid precision stated);
  the S32 cross-anchor gate documents the Session-35
  behaviour-preserving value band (7.2e-6 observed vs <= 1e-4).
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

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Orientation — read these first

This is a **personal research-landscape exploration** (Alcubierre warp-drive boundary-mode reformulation), not a software product or paper-driven programme. There are no users, releases, deliverables, CI, tests, or linters — by design.

Two existing docs are authoritative; this file does not duplicate them:

- **[AGENTS.md](AGENTS.md)** — the canonical agent-instructions file. Project mode/tone, repository layout, notebook rules, HF Jobs discipline, and the "things to avoid" list. **Follow it.** This CLAUDE.md only adds Claude-Code-specific operational detail.
- **[NAVIGATOR.md](NAVIGATOR.md)** — the project's front door: current-state paragraph, headline result, load-bearing-assumptions table, document index. **Read it before any non-trivial work.** The ranked open leads and the closed-leads ledger live in [ROADMAP.md](ROADMAP.md); session-by-session history is in [SESSION_LOG.md](SESSION_LOG.md) (separation of concerns per DOC.1, Session 32).

## Environment & commands

**Use `C:\Python313\python.exe`** (Python 3.13.5 — has the pinned stack: sympy 1.14, numpy 2.4, scipy 1.16, pandas, pyarrow). Do **not** use the local `.venv\` in the repo root — it is stale/incomplete. AGENTS.md says "3.12+" generically; on this machine the global 3.13 interpreter is the one that works.

```powershell
# Run a notebook end-to-end in place (nbclient, 600 s timeout)
C:\Python313\python.exe agent-tools/run_nb.py <notebook.ipynb>

# Strip notebook outputs before commit (ask first — committed outputs are usually intentional docs)
C:\Python313\python.exe agent-tools/clear_outputs.py <notebook.ipynb>

# Run a parameter sweep locally (ALWAYS the *_preview config first; full grids go to HF Jobs)
C:\Python313\python.exe hf_jobs/run_sweep.py <sweep_name> --config hf_jobs/configs/<sweep_name>_preview.json

# Run a verification / adjudication harness (needs repo root on PYTHONPATH)
$env:PYTHONPATH="."; C:\Python313\python.exe verification/test_prongB_groundtruth.py
```

There is no build step and no test runner. The closest thing to a test suite is `verification/` — reusable, version-controlled harnesses (validation suites, cross-checks, ground-truth adjudicators, adversarial kill-tests) that certify whether a result is real or a discretization artifact. Run them directly with `PYTHONPATH=.`.

Heavy sweeps (>~30 s locally) are factored into `hf_jobs/sweeps/<name>.py` (each exposes `build_grid(config)` + `evaluate(point)`) with paired `*_preview.json` / `*_full.json` configs. **Never dispatch a `*_full.json` to HF Jobs without running the preview locally first** — HF Jobs is billed per second. See AGENTS.md "Heavy compute" and the `/new-sweep` skill.

## Architecture / big picture

The unit of work is a **"slice"** — an investigation that relaxes exactly one assumption from the static-slice classical no-go documented in NAVIGATOR.md's load-bearing-assumptions table. The mental model for the whole project lives in that table: each row is an assumption, its status (load-bearing / not / loophole), and where it was tested.

A slice is a paired **`<name>.ipynb` (primary artifact) + `<NAME>_NOTES.md` (companion)**. Notebooks are the canonical record; cell numbers are referenced from the `_NOTES.md` files, so **do not reorder, renumber, or "tidy" cells.** The `/new-slice` skill scaffolds a slice; `/new-sweep` scaffolds its sweep.

Code (as opposed to notebooks/prose) lives in four places:

| Path | Role |
|---|---|
| `hf_jobs/` | Sweep modules (`sweeps/`), JSON configs (`configs/`), the `run_sweep.py` dispatcher. Outputs land in `sweeps/` / `sweeps_remote/` as `.parquet` (treat as artifacts, not source). |
| `warp_factory_py/` | Clean-room NumPy port of the slice of [WarpFactory](https://github.com/NerdsWithAttitudes/WarpFactory) this repo depends on (metrics, Christoffel/Ricci/Einstein solvers, Eulerian frame transform, energy conditions). Used because MATLAB is unavailable. Anchors must reproduce within tolerance — see its README. The `axisymmetric_ec.py` radial-frame solver is the trusted EC evaluator for sharp profiles; the Cartesian path is a smooth-only cross-check (Sessions 28–31). |
| `verification/` | Tracked reusable verification/adjudication harnesses (see above). The verification battery is the artifact-vs-real discriminator — it is the method, not overhead. |
| `agent-tools/` | True throwaway scratch (gitignored), **except** four long-documented utilities tracked in place (`run_nb.py`, `clear_outputs.py`, `slim_pdf.py`, `slim_papers.py`) plus a few reproducibility-critical data artifacts. Do not put reusable harnesses here — promote them to `verification/`. |

The **documentation graph** is intentionally cross-linked, not hierarchical: README (public), NAVIGATOR (map), LANDSCAPE_SYNTHESIS (narrative by physics question), `*_EVALUATION.md` (critical paper readings), `*_NOTES.md` (per-notebook companions). SESSION_LOG.md and TRUST_AUDIT.md are **append-only** progress records.

## Conventions that override default behavior

- **Every claim is reported with its slice of parameter space** (which assumptions it depends on). "Within slice X, no useful classical warp drive exists" is acceptable; "warp drives are impossible" is not. Never drop the slice-scope qualifier when summarising a result.
- **A/B/C trust grading** (TRUST_AUDIT.md): A = derived in our notebooks, B = accepted from a specific paper but spot-checkable, C = heuristic. New results inherit this discipline. Don't invent physics — flag anything not in the literature, our notebooks, or derivable in front of the user as speculation.
- **Surfing, not paper-writing.** No deliverable scaffolding, abstracts, or "publication-ready" framing.
- **Link, don't duplicate.** Don't create new top-level summary docs to "document changes." Update the existing NAVIGATOR.md tables and the relevant `_NOTES.md`; append to SESSION_LOG.md / TRUST_AUDIT.md.
- **Don't add** test frameworks, CI, linters, or pre-commit hooks (none exist by design), and don't add dependencies casually — new deps must be pinned in `requirements.txt` and justified.
- **Don't curate by deletion**: a bounded *negative* survey is a real deliverable here, and the exhaustive verification battery is the point — don't economize rigor to save effort.

## Website bucket is public — pending OAC lockdown (noted 2026-10-02)

The project site is `webpage/` deployed by `webpage/deploy.ps1` (`-Bucket alcubierre.briansheppard.com -DistributionId E3FPT8574LNHQL -Invalidate`).

`alcubierre.briansheppard.com` is served by CloudFront `E3FPT8574LNHQL` (`alcubierre.briansheppard.com`) through the **S3 website endpoint**
(`alcubierre.briansheppard.com.s3-website-us-east-1.amazonaws.com`). That origin type only works while the bucket has
Block Public Access **off** and a public-read bucket policy, so anyone can also fetch objects straight from S3,
bypassing CloudFront. As of 2026-10-02 this is one of three buckets in the account still public
(`alcubierre.briansheppard.com`, `nbody-briansheppard-com`, `storm-water-simple-frontend`); every other site
bucket is private behind an Origin Access Control. Account-level Block Public Access is waiting on these three.

**To lock it down** (about 10 minutes; a brief blip on cache misses is acceptable, nothing else changes):

1. Create an Origin Access Control: `aws cloudfront create-origin-access-control --origin-access-control-config Name=alcubierre.briansheppard.com-oac,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3`
2. Update distribution `E3FPT8574LNHQL` (`get-distribution-config` → edit → `update-distribution --if-match <ETag>`):
   origin `DomainName` → `alcubierre.briansheppard.com.s3.us-east-1.amazonaws.com`; remove `CustomOriginConfig`; add
   `S3OriginConfig: {"OriginAccessIdentity": ""}` and `OriginAccessControlId: <oac id>`; set `DefaultRootObject: index.html`;
   add custom error responses for **403 and 404 → `/index.html`, 200** (S3 REST answers 403 for missing keys).
3. Replace the bucket policy with a single statement: `Allow s3:GetObject` to `Principal: {"Service": "cloudfront.amazonaws.com"}`
   on `arn:aws:s3:::alcubierre.briansheppard.com/*` with `Condition StringEquals AWS:SourceArn = arn:aws:cloudfront::290318879194:distribution/E3FPT8574LNHQL`.
   Do not write a policy that still contains the `Principal: "*"` statement — the Claude Code auto-mode classifier blocks that as a weakening, and it is unnecessary if step 2 runs first.
4. `aws s3api put-public-access-block --bucket alcubierre.briansheppard.com --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true`
   then `aws s3api delete-bucket-website --bucket alcubierre.briansheppard.com`.
5. `aws cloudfront wait distribution-deployed --id E3FPT8574LNHQL`, then verify `https://alcubierre.briansheppard.com/`, a static asset, and a bad path (should return `index.html` with 200)
   and confirm `https://s3.us-east-1.amazonaws.com/alcubierre.briansheppard.com/index.html` now returns **403**.
6. `webpage/s3-policy.json` is a sample IAM policy for the deploy user, not the bucket policy — it does not need to change.

Reference implementation: `F:\dark-forest-labs-projects\ubomw-site` — commit `cb6bf21` ("move S3 behind CloudFront OAC") and `scripts/deploy_s3.sh` there. Migrated 2026-10-02 with the exact steps below.

---
name: new-slice
description: 'Scaffold a new Phase-2C/2D-style "slice" exploration for the Alcubierre repo: creates a paired `<slice>.ipynb` + `<SLICE>_NOTES.md`, drafts the row to add to NAVIGATOR.md''s load-bearing-assumptions table, and links to existing slices as templates. Use when the user wants to relax a new assumption from the static-slice no-go, open a new investigative track, or add a slice to Phase 2C/2D. Trigger phrases: "new slice", "add a slice", "Phase 2C slice", "Phase 2D slice", "explore relaxing assumption", "scaffold an investigation of".'
---

# New Slice Exploration

Scaffold a new "slice" — the unit of investigation in this repo, where each slice relaxes one assumption from the static-slice no-go documented in [NAVIGATOR.md](../../NAVIGATOR.md) "Load-bearing assumptions table".

## When to use

- The user wants to test whether a specific assumption from the canonical slice is load-bearing.
- A new Phase 2C / 2D / future-phase track is starting.
- An external paper (Lentz, Rodal, Fell-Heisenberg, Lobo-Oliveira, Garattini-Zatrimaylov, etc.) needs to be evaluated *in our framework* rather than just summarised.

Do **not** use for: minor extensions of an existing slice (extend the existing notebook), critical readings of papers that don't require computation (write a `*_EVALUATION.md` directly), or sweeps factored out of an existing slice (use the `new-sweep` skill).

## Procedure

1. **Identify which assumption is being relaxed.** Open [NAVIGATOR.md](../../NAVIGATOR.md) "Load-bearing assumptions table" and confirm with the user which row this slice targets, or that it's a genuinely new dimension. Also confirm the slice number (e.g. "Phase 2C Slice 7" or "Phase 2D Task 2D.N"). The slice's lifetime status should follow the existing A/B/C grading discipline of [TRUST_AUDIT.md](../../TRUST_AUDIT.md).

2. **Pick a `snake_case` name** matching the assumption being relaxed (e.g. `cosmological_exterior`, `time_dependent`, `hybrid_wall`, `fell_heisenberg`). The same stem will be used for the notebook, notes file, and any sweep modules.

3. **Inspect a recent template slice.** Good references depending on the slice's character:
   - Pure-symbolic + small numeric: [time_dependent.ipynb](../../time_dependent.ipynb) ↔ [TIME_DEPENDENT_NOTES.md](../../TIME_DEPENDENT_NOTES.md).
   - Heavy parameter sweep: [shift_families.ipynb](../../shift_families.ipynb) ↔ [SHIFT_FAMILIES_NOTES.md](../../SHIFT_FAMILIES_NOTES.md) (paired with [hf_jobs/sweeps/shift_families.py](../../hf_jobs/sweeps/shift_families.py)).
   - Reproduction of a published construction: [fell_heisenberg.ipynb](../../fell_heisenberg.ipynb) ↔ [FELL_HEISENBERG2021_EVALUATION.md](../../FELL_HEISENBERG2021_EVALUATION.md) and [FELL_HEISENBERG_SWEEP_NOTES.md](../../FELL_HEISENBERG_SWEEP_NOTES.md).

4. **Create `<name>.ipynb`** with the standard cell structure used by existing slice notebooks:
   1. Title + "Open in Colab" badge cell (markdown).
   2. Setup cell — Colab-aware install of [requirements.txt](../../requirements.txt).
   3. A short "Question" markdown cell stating the slice scope (which assumption is being relaxed and what failure of the no-go would look like).
   4. Symbolic / numeric work cells.
   5. A final "Headline" markdown cell with the slice's headline result, explicitly slice-scoped per the AGENTS.md "honest accounting" rule.

   Use `edit_notebook_file` for cell creation; never write notebook JSON by hand.

5. **Create `<NAME>_NOTES.md`** as the companion document, mirroring the structure of [SHIFT_FAMILIES_NOTES.md](../../SHIFT_FAMILIES_NOTES.md):
   - YAML-free header with `**Source:**` (link to notebook + sweep module if any) and `**Written:**` date + session number.
   - `## TL;DR` — one paragraph with explicit slice scope.
   - `## What was actually computed` — the math/numerics summary.
   - `## Headline results` — tables / numbers.
   - `## What this does and does not establish` — the honest-accounting section.

6. **If the slice needs a parameter sweep**, invoke the sister skill `/new-sweep` with the same `<name>` stem so the sweep module and configs are scaffolded with matching naming.

7. **Draft (do not commit) the NAVIGATOR.md table row.** Print the proposed row for the user to paste into the load-bearing-assumptions table. The format is:

   ```markdown
   | <#> | <Sub-assumption> | **<Status>** | <Slice notes link> | <One-sentence finding with slice scope> |
   ```

   Status values used in the existing table: `Load-bearing`, `Not load-bearing`, `Real loophole; interpretation-dependent`, `Substantively weakened by <citation>`, etc. Match an existing precedent rather than inventing new statuses.

8. **Do not write to** [SESSION_LOG.md](../../SESSION_LOG.md), [TRUST_AUDIT.md](../../TRUST_AUDIT.md), or [README.md](../../README.md) as part of scaffolding. Those are append-only progress records the user maintains by hand once results land.

## Anti-patterns

- Skipping the `_NOTES.md` companion — every slice notebook in the repo has one; orphan notebooks fragment the doc graph.
- Stating the headline as "warp drives are impossible" or "this slice rules out warp drives" — only "within the slice X, no useful classical warp drive exists" is acceptable per AGENTS.md.
- Adding the slice's row to NAVIGATOR.md without computed results to back it — the table is the source of truth on what's actually been tested.
- Reusing a slice name from a closed slice — slice names are durable references in `_NOTES.md` and the trust audit.
- Promoting the slice to a new top-level summary doc instead of updating existing tables — see AGENTS.md "Things to avoid".

# Research-Surfing Discipline — A Project-Agnostic Process

A short, opinionated playbook for keeping a long-running theoretical / computational research exploration honest, navigable, and resumable across many sessions, without slipping into either paper-writing scaffolding or hand-wavy speculation.

This document is **physics-agnostic**. It works equally well for any landscape exploration where the goal is to map the structure of a problem (which assumptions hold up which conclusions, and where the obstructions live) rather than to ship a paper or a product.

---

## 0. Stance

Before any process: **decide what mode you are in.**

| Mode | Output | Discipline |
|---|---|---|
| **Surfing** | Map of the landscape; honest accounting of what is and isn't established | This document |
| **Paper-writing** | A specific claim defended for a specific audience | Different discipline (abstracts, narrative arc, peer review) |
| **Product** | A working artifact for users | Different discipline (releases, tests, support) |

This playbook is for **surfing**. If you find yourself adding deliverable scaffolding ("abstract", "publication-ready", "v1.0 release"), you have switched modes; either commit to the new mode or stop.

The single most important rule of surfing is:

> **Every claim is reported with the slice of parameter space it depends on.**
>
> "Within the slice $X$, no $Y$ exists" is acceptable.
> "$Y$ is impossible" is not.

---

## 1. The four standing documents

Every project needs exactly four "standing" documents at the top level. Resist the urge to add more — instead, update the existing ones.

### 1.1 `NAVIGATOR.md` — front door

The single authoritative map. If a returning collaborator (or you, after a break) reads only one file, this is it.

Required sections:

1. **Headline** — one paragraph, with explicit slice-scope qualifier.
2. **"Where to start" table** — "if you want X, go here" routing for the other documents.
3. **Load-bearing assumptions table** — the canonical version (other notes defer to this one). Each row: assumption · status (load-bearing / not load-bearing / broken / interpretation-dependent) · where tested · short note. This table is *the* artifact of the project.
4. **Document index** — what every other file in the repo is for.
5. **Open question** — the single most active line of investigation.

Update on every non-trivial finding. Do not duplicate content from other docs; link to them.

### 1.2 `TRUST_AUDIT.md` — what we derived vs. what we accepted

Honest accounting of every external result the project relies on. Use a three-tier grading scheme:

- **A** — Independently verified. Computed from first principles in this repo; no faith required beyond the underlying field's standard machinery.
- **B** — Accepted on the literature's authority but spot-checkable. A specific paper says it; we did not re-derive it but could without prohibitive cost. Each B entry includes a **cost-to-verify estimate** (e.g. "~30 min to write a SymPy snippet" or "~1 session to install package X and reproduce Fig Y").
- **C** — Heuristic / order-of-magnitude. Used as a quantitative ceiling or scaling argument, not a precise prediction. A C-grade claim should never appear in the headline without the qualifier "at the order-of-magnitude level".

For each major result of the project, list every component dependency with its grade. Then summarise the **load-bearing dependencies** — the ones that, if wrong, would actually invalidate the result. New results inherit this discipline before being added to the headline.

### 1.3 `SESSION_LOG.md` — append-only history

One section per working session. Each entry: date · who · short summary of work · key insight · pointer to the artifact(s) produced.

This is **append-only**. Old entries are never edited (except for typos). When a finding is later refined or retracted, the new session entry says so explicitly ("Session 14b §11 revises the Session 11 sweep count from 6818 to ~5900 because boundary points were over-counted at low resolution"); the original entry stays put. The log is the project's memory.

### 1.4 `LANDSCAPE_SYNTHESIS.md` (or `README.md`) — the long-form story

The narrative version of NAVIGATOR. Same material, prose form, written for a reader who wants the arc rather than the index. Update less often than NAVIGATOR; it's the place to integrate findings into a coherent picture every ~10 sessions.

---

## 2. Paired artifacts

For every non-trivial computation, produce **two paired files**:

- The artifact (notebook, script, or derivation file) — the primary research object.
- A `<artifact>_NOTES.md` companion — context, what the cells do, what was tried and rejected, what the result means in the project's language.

The notes file is what you read on return; the artifact is what you re-run when you doubt the result. Cell numbers in the artifact are referenced from the notes file ("Cell 4b Schwarzschild regression"), so do not reorder or renumber cells "for clarity" without an explicit reason.

For critical readings of specific external papers, use a `<paper>_EVALUATION.md` file. Keep evaluations separate from your own derivations.

---

## 3. The slice-scope qualifier

Every claim that escapes a notebook into a `.md` file gets a slice-scope qualifier. Concretely, every result of the form

> $X$ is true.

becomes

> Within the slice defined by [assumptions A, B, C], $X$ is true.

When summarising for the headline, the slice-scope qualifier comes **first**, not last. "Within the slice X, no useful classical Y exists" — not "no useful classical Y exists, assuming X". The first form refuses to be misread; the second invites it.

If a slice qualifier ever feels awkward to write, you have probably overgeneralised the claim. Tighten the claim, not the qualifier.

---

## 4. Heavy compute: the preview / full discipline

Any computation that takes more than ~30 s locally must be factored into a reusable module with **two configurations**:

1. **Preview config** — small grid, runs locally in seconds. Always run first as a smoke test. Verifies the schema of the output matches what the consumer expects.
2. **Full config** — full grid, dispatched to the heavy-compute backend (HPC, cloud job runner, GPU box).

Never dispatch a full grid without first running the preview locally. Heavy compute is billed per second (in dollars *or* in attention); a 5-second smoke test prevents an hour of wasted run time.

The output of a full sweep is an **artifact** (Parquet, CSV, JSON) committed alongside its config. Notebooks read the artifact; they do not regenerate it on every render.

---

## 5. Speculation handling

Long-shot ideas — interesting hunches that have not been derived, sourced, or computed — go in a dedicated `speculation/` directory with a header that says, in so many words,

> **This is not derived. It is a hunch. Do not cite from it.**

Speculation files can be promoted into the main repo only after they have been (a) derived in a notebook, or (b) backed by a specific citation, or (c) explicitly accepted as a heuristic and graded **C** in the trust audit.

This separation exists so that the headline never accidentally rests on speculation, and so that speculation isn't suppressed — it has a home, just not in the load-bearing tables.

---

## 6. What not to do

The discipline is largely defensive. Things to avoid:

- **Refactoring artifacts "for clarity"** without an explicit ask. Cell numbers and notebook layout are referenced from notes; reordering breaks the references.
- **Promoting throwaway scripts** (`diag_*`, `fix_*`, `inspect_*`) into permanent infrastructure. Diagnostic scratch lives in a clearly-marked scratch directory; it is not the system of record.
- **Adding test frameworks, CI, linters, or pre-commit hooks** unless the project has crossed into product mode. Surfing projects don't need them; they add maintenance burden and tempt you to satisfy the linter rather than understand the problem.
- **Creating new top-level summary docs** "to document changes". Update the existing standing documents instead. If a finding deserves a new doc, it deserves a `_NOTES.md` companion to a notebook, not a top-level summary.
- **Dropping the slice-scope qualifier** when summarising. The qualifier is the most fragile part of the discipline and the first thing to erode; protect it explicitly.
- **Oversold conclusions.** "Within the slice $X$, no useful $Y$ exists" is acceptable. "$Y$ is impossible" is not.
- **Inventing physics / math / facts.** If a claim isn't in the literature, in the repo's notebooks, or derivable in front of the reader, flag it as speculation.

---

## 7. AGENTS.md — wiring the discipline into automated assistants

If you use coding agents or LLMs as collaborators, write a short `AGENTS.md` at the repo root that tells them, in concrete terms:

1. **Mode.** "This is a surfing project, not paper-writing or product."
2. **The standing documents** and where to write what.
3. **The slice-scope rule.**
4. **The trust-audit grading scheme.**
5. **The "things to avoid" list above.**

A compact `AGENTS.md` is the cheapest way to keep a long-running project from drifting toward generic "publication-ready" framing every time a fresh model context starts.

---

## 8. Resumability checklist

You can tell the discipline is working if, after a six-week break, you can return to the project and within 15 minutes:

- Read NAVIGATOR.md and know what the headline is and which slice it lives in.
- Look at the load-bearing-assumptions table and know which assumption is currently the bottleneck.
- Look at the most recent SESSION_LOG entry and know what was being worked on.
- Open the relevant `_NOTES.md` and know what the next concrete step is.

If any of those takes longer than a few minutes, the discipline has slipped. The fix is not new infrastructure; it is updating the standing documents.

---

## 9. Minimum viable adoption

To bootstrap on a new project:

1. Create `NAVIGATOR.md`, `TRUST_AUDIT.md`, `SESSION_LOG.md`, `AGENTS.md` (4 files).
2. Write the headline with its slice-scope qualifier.
3. Make a one-row load-bearing-assumptions table for whatever the first finding rests on.
4. Grade the dependencies of that finding **A / B / C** in the trust audit.
5. Append the first session entry.

Everything else (paired notebooks, preview/full sweeps, speculation directory) accretes naturally as the project grows. The four standing documents are the spine.

---

*This playbook is itself a slice-scoped artifact: it is what worked for one specific landscape-exploration project, generalised. Adopt the parts that fit your project; ignore the rest.*

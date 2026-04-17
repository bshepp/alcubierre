# Papers — local mirror of literature referenced by the project

This folder contains PDFs and arXiv source tarballs of papers referenced from `LITERATURE.md`, `MATTER_SHELL_PATH.md`, `KRASNIKOV_TUBE_NOTES.md`, and `RODAL2025_EVALUATION.md`. Mirrored locally so the project remains analysable offline.

## Slim-by-default policy

Some papers ship with very large embedded raster figures (Rodal 2025 was 31.5 MB plus a 17.6 MB tarball). To keep the repo cloneable without git-lfs, the heavy items are slimmed before committing:

- **PDFs >10 MB:** all embedded raster images are downsampled to ≤1200 px (longest edge) and re-encoded as JPEG quality 60. Equations and text are unchanged. See `agent-tools/slim_papers.py`.
- **arXiv source tarballs >10 MB:** stripped to LaTeX source files only (`.tex`, `.bbl`, `.cls`, `.sty`, `.bib`, etc.) — figures live in the PDF anyway and are redundant in the tarball.

The originals are preserved locally in `papers/_originals/` (gitignored) for safe rollback. To restore a high-resolution PDF for local viewing, `cp papers/_originals/<file> papers/<file>`.

## Inventory

| File | Paper |
|---|---|
| `9511068v6.pdf` | Krasnikov 1995 — *Hyperfast interstellar travel in general relativity* (Phys. Rev. D 57, 4760). The original 2D Krasnikov-tube paper. |
| `9702049v1.pdf` | Everett & Roman 1997 — *A Superluminal Subway: The Krasnikov Tube* (Phys. Rev. D 56, 2100). 4D extension + classical $T_{\mu\nu}$ + network/CTC theorem. |
| `0207057v3.pdf` | Krasnikov 2003 — *The quantum inequalities do not forbid spacetime shortcuts* (Phys. Rev. D 67, 104013). |
| `2102.06824v2.pdf` | Bobrick & Martire 2021 — *Introducing Physical Warp Drives* (Class. Quant. Grav. 38, 105009). |
| `2105.03079v2.pdf` | Santiago, Schuster & Visser 2022 — *Generic warp drives violate the null energy condition* (Phys. Rev. D 105, 064038). |
| `2512.18008v1.pdf` | Rodal 2025 — *A warp drive with predominantly positive invariant energy density and global Hawking-Ellis Type I* (Gen. Rel. Grav. 58:1, 2026). **Slimmed (31.5 MB → 2.9 MB)**, raster figures only — full quality available in `_originals/`. |
| `arXiv-*.tar.gz` | LaTeX source tarballs (figures stripped on the slimmed Rodal item; otherwise full). |

The Lobo & Crawford 2002 paper (gr-qc/0204038) is supplied as source-only (`arXiv-gr-qc0204038v2.tar.gz`); we have not separately downloaded its PDF as the source contains everything we need.

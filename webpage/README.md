# Alcubierre Boundary-Mode — static website

Personal landing site for the Alcubierre boundary-mode reformulation
project. Five static HTML pages, one shared stylesheet, no build step,
no JavaScript framework.

## File layout

```
webpage/
├── index.html        # Dashboard — hero formula, stats, discovery cards
├── roadmap.html      # Phase tracker (0..5, dual-track Phase 2)
├── path-2a.html      # Path 2A technical detail (Fuchs anchor + κ + accel + Krasnikov)
├── notebooks.html    # Catalog of notebooks, MATLAB kit, HF-Jobs sweeps
├── about.html        # Project framing, slice discipline, citation
├── assets/
│   └── style.css     # Shared stylesheet (cyan/violet phosphor palette)
├── _partials/
│   └── head.html     # Reference snippet for the canonical <head> imports
├── deploy.ps1        # aws s3 sync wrapper (PowerShell 5.1 compatible)
├── s3-policy.json    # Sample IAM policy template
└── README.md         # This file
```

## Local preview

From the `webpage/` directory:

```powershell
python -m http.server 8000
```

Then open <http://localhost:8000>.

## Deploy to S3

The deploy script is a thin wrapper around `aws s3 sync` with the right
exclusions. Internal files (`*.ps1`, `_partials/`, `README.md`,
`s3-policy.json`) are not pushed.

```powershell
# Dry-run first to see what would change.
.\deploy.ps1 -Bucket your-bucket-name -DryRun

# Push for real.
.\deploy.ps1 -Bucket your-bucket-name

# With a non-default AWS CLI profile.
.\deploy.ps1 -Bucket your-bucket-name -Profile mybucket-admin

# With CloudFront in front of the bucket (invalidate on deploy).
.\deploy.ps1 -Bucket your-bucket-name `
             -DistributionId E1234567890ABCD `
             -Invalidate
```

## Required AWS setup

1. **Create a bucket.** `aws s3 mb s3://your-bucket-name`.
2. **Either** enable static-website hosting on the bucket directly
   (`aws s3 website s3://your-bucket-name --index-document index.html`)
   **or** front it with a CloudFront distribution and an Origin Access
   Identity / Origin Access Control.
3. **Attach an IAM policy** giving your deploy user the rights in
   `s3-policy.json` (replace `<YOUR-BUCKET-NAME>` with your bucket).
4. **Configure the AWS CLI** with credentials for that user
   (`aws configure --profile your-profile`).

## Design notes

The visual language is adapted from the sister project at
`F:\science-projects\3body\website\` (terminal/phosphor aesthetic, CRT
scanline overlay, mono+serif typography). Palette is shifted from
3body's green-phosphor to a cyan-violet (`#4ac8e8` primary) so the two
sites are visually distinct at a glance.

3body keeps CSS embedded per page; this project factors it into a
shared `assets/style.css` since five pages share an almost identical
component vocabulary and per-page duplication adds friction without
benefit.

## Maintenance

When project results change:

* **Stat cards** in `index.html` (`Phases Closed`, `κ-Sweep Cells`,
  etc.) — update inline values.
* **Phase status** in `roadmap.html` — sync the `.phase-row` block
  against `ROADMAP.md` Phase Index.
* **κ-surface** numbers in `path-2a.html` — sync against
  `WARP_FACTORY_NOTES.md` §3 (Session 19).
* **Notebook table** in `notebooks.html` — sync against the table in
  the project root `README.md`.

The site has no automated testing — visual regression is by eye.

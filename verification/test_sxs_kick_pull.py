"""TRUST_AUDIT #5 closure: real-SXS check of the GW-recoil ceiling's kick input (Session 37).

Package 3's GW-recoil ceiling (Task 2A.10; hf_jobs/sweeps/gw_recoil.py) uses
V_KICK_BBH_RECORD = 5000 km/s -- the literature record-scale black-hole
recoil (Varma et al. 2022 PRL 128:191102 / Lousto-Zlochower "hangup kick"
family) -- as the conservative anchor of the Approach-A rescaling
v_kick = V * beta^2 * C^(3/2).  TRUST_AUDIT #5 graded that anchor C because
it was accepted from the literature without pulling any real NR data; Cell 17
of time_dependent.ipynb wired a Colab `sxs` pull that was never run.

This harness closes the item WITHOUT the sxs package, by pulling the same
data over plain HTTPS:

  Route 1 (per-simulation): the Zenodo record for SXS:BBH:1937 (the specific
    simulation Cell 17 targets), highest-Lev metadata.json.
  Route 2 (catalog-wide): https://data.black-holes.org/catalog.zip -- the
    SXS collaboration's own catalog metadata for every public simulation.

Findings this harness certifies (2026-07-05 pull, catalog.zip of that date):

  * Cell 17's premise was WRONG: SXS:BBH:1937 is a q=4.0, aligned-spin
    (chi1=0.4 zhat, chi2~0), non-precessing run whose remnant kick is
    |v| = 3.12e-4 c ~ 93.5 km/s -- 53x BELOW the 5000 km/s "record" the
    cell's comparison expected to confirm within 1.5x.  Aligned-spin
    systems cannot superkick; the record configurations are near-equal-mass
    precessing ones.  Had the Colab run ever happened it would have printed
    the "differs significantly" branch.
  * The direction of the error is the SAFE one for a ceiling: the catalog-
    wide maximum remnant kick (GATE 4) is BELOW the 5000 km/s input, so the
    recorded ceiling is conservative with respect to every public SXS
    simulation.

Gates:
  GATE 1  catalog.zip fetch + parse; > 2000 simulations with remnant data.
  GATE 2  route agreement: catalog entry for SXS:BBH:1937 == Zenodo
          per-record metadata.json (independent hosting paths).
  GATE 3  SXS:BBH:1937 is NOT a record-kick configuration (kick < 500 km/s,
          q ~ 4, negligible in-plane spin) -- documents the Cell-17 defect.
  GATE 4  max |remnant_velocity| over the whole catalog <= 5000 km/s
          => the gw_recoil.py V_KICK_BBH_RECORD input upper-bounds every
          public NR simulation; report the actual maximum and its ID.

Network use: read-only GETs to data.black-holes.org and zenodo.org; the
catalog zip (~10 MB) is cached in agent-tools/sxs_cache/ (gitignored).
Offline: exits 2 with SKIP (never a false PASS/FAIL).

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_sxs_kick_pull.py
"""
from __future__ import annotations

import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

C_KM_S = 299792.458
V_INPUT_KM_S = 5000.0            # gw_recoil.py V_KICK_BBH_RECORD, in km/s
CACHE = Path(__file__).resolve().parent.parent / "agent-tools" / "sxs_cache"
CATALOG_URL = "https://data.black-holes.org/catalog.zip"
ZENODO_1937 = ("https://zenodo.org/api/records/3310634/files/"
               "Lev3%2Fmetadata.json/content")
HDRS = {"User-Agent": "alcubierre-verification/1.0"}

GATES = {}


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def fetch(url, timeout=120):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def main():
    # ---------------- fetch (cached) ----------------
    CACHE.mkdir(parents=True, exist_ok=True)
    zip_path = CACHE / "catalog.zip"
    try:
        if not zip_path.exists():
            print(f"downloading {CATALOG_URL} (~10 MB)...")
            zip_path.write_bytes(fetch(CATALOG_URL))
        zenodo_md = json.loads(fetch(ZENODO_1937))
    except Exception as exc:
        print(f"SKIP: network fetch failed ({type(exc).__name__}: {exc})")
        return 2

    with zipfile.ZipFile(io.BytesIO(zip_path.read_bytes())) as zf:
        names = zf.namelist()
        cat_name = next(n for n in names if n.endswith("catalog.json"))
        catalog = json.loads(zf.read(cat_name))

    sims = catalog["simulations"]

    # ---------------- GATE 1 ----------------
    kicks = {}
    for sxs_id, md in sims.items():
        v = md.get("remnant_velocity")
        if (isinstance(v, (list, tuple)) and len(v) == 3
                and all(isinstance(x, (int, float)) for x in v)):
            kicks[sxs_id] = float(np.linalg.norm(v)) * C_KM_S
    gate("catalog parsed with > 2000 remnant-velocity entries",
         len(kicks) > 2000, f"{len(sims)} simulations, {len(kicks)} with remnant kick")

    # ---------------- GATE 2 ----------------
    cat_1937 = sims.get("SXS:BBH:1937", {})
    v_cat = np.asarray(cat_1937.get("remnant_velocity", [np.nan] * 3), float)
    v_zen = np.asarray(zenodo_md["remnant_velocity"], float)
    agree = bool(np.allclose(v_cat, v_zen, rtol=0, atol=5e-6))
    gate("SXS:BBH:1937: catalog == Zenodo per-record metadata", agree,
         f"catalog {v_cat.tolist()} vs zenodo {v_zen.tolist()}")

    # ---------------- GATE 3 ----------------
    kick_1937 = float(np.linalg.norm(v_zen)) * C_KM_S
    q = float(zenodo_md["reference_mass_ratio"])
    chi1_perp = float(zenodo_md["reference_chi1_perp"])
    not_record = bool(kick_1937 < 500.0 and 3.5 < q < 4.5 and chi1_perp < 1e-3)
    gate("SXS:BBH:1937 is NOT a record-kick configuration "
         "(Cell-17 designation defect documented)", not_record,
         f"kick = {kick_1937:.1f} km/s = {kick_1937 / V_INPUT_KM_S:.4f} x input; "
         f"q = {q:.3f}, chi1_perp = {chi1_perp:.1e} (aligned, non-precessing)")

    # ---------------- GATE 4 ----------------
    max_id = max(kicks, key=kicks.get)
    max_kick = kicks[max_id]
    top = sorted(kicks.items(), key=lambda kv: -kv[1])[:5]
    print("  catalog top-5 kicks:")
    for sid, k in top:
        md = sims[sid]
        print(f"    {sid}: {k:7.1f} km/s  (q = {md.get('reference_mass_ratio', float('nan')):.2f}, "
              f"chi1_perp = {md.get('reference_chi1_perp', float('nan')):.3f})")
    gate("catalog-wide max kick <= 5000 km/s ceiling input (input is "
         "conservative vs every public SXS simulation)",
         bool(max_kick <= V_INPUT_KM_S),
         f"max = {max_kick:.1f} km/s ({max_id}); "
         f"input/max = {V_INPUT_KM_S / max_kick:.2f}x headroom")

    # ---------------- summary ----------------
    n_pass = sum(GATES.values())
    print(f"\nSXS KICK ADJUDICATION: {n_pass}/{len(GATES)} gates PASS")
    if n_pass == len(GATES):
        print("TRUST_AUDIT #5 closure basis: the 5000 km/s Approach-A anchor "
              "upper-bounds every public SXS NR simulation; the recorded "
              "recoil ceiling is conservative. (Cell 17's specific comparison "
              "was mis-designed and is superseded by this harness.)")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Pointwise lapse-shift ratio and foliation-health analysis for FH winners.

Implements the cheap horizon test (Task 2D.6 from ROADMAP.md / NAVIGATOR.md):
for a representative WEC+DEC-passing Fell-Heisenberg parameter point, build
the shift field |N(x,y,z)| on a 3D box and characterize the locus where
|N| >= 1 (superluminal -- the t=const foliation becomes spacelike there
and the lapse vector dt is no longer timelike).

The Fell-Heisenberg construction uses unit lapse alpha=1 by definition, so
|N|/alpha = |N| pointwise. The norm of dt as a vector field is
    g(dt, dt) = -alpha^2 + |N|^2
which is timelike (negative) iff |N| < 1. So the test reduces to mapping
the surface |N| = 1.

GEOMETRY note (corrected from initial assumption): the FH potential's shift
field |N| is ZERO at the bubble centre (origin), ramps up to a large value
in a "wall" region around radius ~r-2*sigma to ~r+2*sigma, then asymptotes
to a non-zero "background" value far from the bubble. This is opposite to
what "central frame-dragging" naming suggested. The *centre* of the bubble
has a healthy foliation; the *wall* and *exterior* are superluminal.

For warp-drive interpretation, the relevant region is the bubble interior
(inside the |N|=1 surface that bounds the central "calm" region) where an
observer at rest in the lapse foliation can sit safely. A useful warp
drive needs this interior region to be (i) non-empty, (ii) large enough
to contain a payload, and (iii) bounded by a horizon-like surface that
separates "passenger zone" from "wall".

Outputs (when run via main):
- summary.json with per-winner aggregate diagnostics
- foliation_<label>.png with 2D slices of |N|, |N|>=1 mask, cross-sections
- v_scan.png if multiple V values are processed
- leaderboard.csv summarising the foliation-health/passenger-zone-radius tradeoff

Usage::

    python -m hf_jobs.analysis.fell_heisenberg_horizon --out-dir fell_heisenberg_horizon
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from hf_jobs.sweeps.fell_heisenberg import phi_FH_smooth, fd_grad4


# Canonical winner from FELL_HEISENBERG_SWEEP_NOTES.md section 1.1.
CANONICAL_WINNER = dict(V=1.5, sigma=10.0, m0=3.0, a=0.05, ell=4.0, r=9.0, Pi=0.25, L=12.0)


@dataclass
class FoliationDiagnostics:
    """Per-point summary of the lapse-shift / foliation-health analysis.

    Key concept: the WEC+DEC-passing FH bubble has |N| ~ 0 at the origin
    (the "passenger zone") surrounded by a "wall" of superluminal shift
    |N| >= 1, surrounded by a non-zero asymptotic background. A useful
    warp drive needs the passenger zone to be non-empty and physically
    significant.
    """
    V: float
    sigma: float
    m0: float
    a: float
    ell: float
    r: float
    Pi: float
    L: float
    Npts: int
    # |N| diagnostics
    N_max_central: float          # max |N| in central 7^3 cube (legacy "central_N_max")
    N_max_box: float              # max |N| over the whole box
    N_max_pos: tuple              # (x, y, z) of N_max_box
    N_origin: float               # |N| at the origin
    # Superluminal-region geometry
    superluminal_volume: float    # volume where |N| >= 1
    superluminal_fraction: float  # fraction of box volume
    superluminal_connected: int   # number of connected components in |N|>=1
    superluminal_touches_edge: bool  # does the |N|>=1 region touch the box boundary?
    superluminal_contains_origin: bool  # if True, no passenger zone exists
    # Passenger zone (connected |N|<1 region containing the origin)
    passenger_zone_volume: float  # volume of connected |N|<1 region containing origin (0 if none)
    passenger_zone_radius: float  # radius of largest sphere centred at origin fitting inside passenger zone
    # Foliation-health summary
    dt_timelike_fraction: float   # fraction of box where g(dt, dt) < 0 (i.e. |N|<1)


def build_field(point: dict, Npts: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Compute (xs, X, Y, Z, |N|) on a Cartesian box for a single winner."""
    L = float(point["L"])
    xs = np.linspace(-L, L, Npts)
    h = float(xs[1] - xs[0])
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    phi = phi_FH_smooth(
        X, Y, Z,
        Pi=float(point.get("Pi", 0.25)),
        r=float(point["r"]),
        V=float(point["V"]),
        sigma=float(point["sigma"]),
        m0=float(point["m0"]),
        a=float(point["a"]),
        ell=float(point["ell"]),
    )
    grads = [fd_grad4(phi, h, axis=ax) for ax in range(3)]
    Nmag = np.sqrt(grads[0]**2 + grads[1]**2 + grads[2]**2)
    return xs, X, Y, Z, Nmag


def diagnostics(point: dict, Npts: int = 97) -> tuple[FoliationDiagnostics, np.ndarray, np.ndarray]:
    """Compute the foliation diagnostics + return Nmag and xs for plotting."""
    xs, X, Y, Z, Nmag = build_field(point, Npts)
    h = float(xs[1] - xs[0])
    superluminal = Nmag >= 1.0
    central_slice = (slice(Npts // 2 - 3, Npts // 2 + 4),) * 3
    N_central = float(Nmag[central_slice].max())

    flat_idx = int(np.argmax(Nmag))
    i, j, k = np.unravel_index(flat_idx, Nmag.shape)
    N_max_pos = (float(xs[i]), float(xs[j]), float(xs[k]))

    # Connected components of |N|>=1 region.
    from scipy import ndimage
    labels, n_components = ndimage.label(superluminal, structure=ndimage.generate_binary_structure(3, 1))

    # Does any superluminal cell touch the box boundary?
    edge_touch = bool(
        superluminal[0, :, :].any() or superluminal[-1, :, :].any() or
        superluminal[:, 0, :].any() or superluminal[:, -1, :].any() or
        superluminal[:, :, 0].any() or superluminal[:, :, -1].any()
    )
    contains_origin = bool(superluminal[Npts // 2, Npts // 2, Npts // 2])

    cell_vol = h ** 3
    super_vol = float(superluminal.sum() * cell_vol)
    box_vol = float(superluminal.size * cell_vol)

    # g(dt,dt) = -1 + |N|^2 (alpha=1). dt timelike (g<0) iff |N|<1.
    timelike_fraction = float((Nmag < 1).mean())

    # Passenger zone: connected component of |N|<1 containing the origin.
    subluminal = ~superluminal
    sub_labels, _ = ndimage.label(subluminal, structure=ndimage.generate_binary_structure(3, 1))
    origin_label = int(sub_labels[Npts // 2, Npts // 2, Npts // 2])
    if origin_label == 0:
        # No passenger zone: origin itself is in the superluminal region
        passenger_volume = 0.0
        passenger_radius = 0.0
    else:
        passenger_mask = sub_labels == origin_label
        passenger_volume = float(passenger_mask.sum() * cell_vol)
        # Largest sphere centred at origin that fits inside the passenger zone:
        # find min radius across rays where passenger_mask becomes False.
        R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
        # The "exit radius" is the smallest R among non-passenger cells in the box.
        non_pass_R = R[~passenger_mask]
        passenger_radius = float(non_pass_R.min()) if non_pass_R.size > 0 else float(R.max())

    diag = FoliationDiagnostics(
        V=float(point["V"]),
        sigma=float(point["sigma"]),
        m0=float(point["m0"]),
        a=float(point["a"]),
        ell=float(point["ell"]),
        r=float(point["r"]),
        Pi=float(point.get("Pi", 0.25)),
        L=float(point["L"]),
        Npts=int(Npts),
        N_max_central=N_central,
        N_max_box=float(Nmag.max()),
        N_max_pos=N_max_pos,
        N_origin=float(Nmag[Npts // 2, Npts // 2, Npts // 2]),
        superluminal_volume=super_vol,
        superluminal_fraction=super_vol / box_vol,
        superluminal_connected=int(n_components),
        superluminal_touches_edge=edge_touch,
        superluminal_contains_origin=contains_origin,
        passenger_zone_volume=passenger_volume,
        passenger_zone_radius=passenger_radius,
        dt_timelike_fraction=timelike_fraction,
    )
    return diag, Nmag, xs


def plot_foliation(point: dict, Nmag: np.ndarray, xs: np.ndarray, out_path: Path, label: str) -> None:
    """4-panel figure: |N| at central z=0 slice, |N|>=1 mask, |N| along axes, contour."""
    L = float(point["L"])
    Npts = len(xs)
    k = Npts // 2

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Panel 1: |N| at z=0 slice
    ax = axes[0, 0]
    vmax = float(Nmag.max())
    im = ax.imshow(
        Nmag[:, :, k].T,
        origin="lower",
        extent=[-L, L, -L, L],
        cmap="viridis",
        aspect="equal",
        vmin=0,
        vmax=vmax,
    )
    ax.contour(xs, xs, Nmag[:, :, k].T, levels=[1.0], colors="red", linewidths=2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(rf"$|\vec{{N}}|(x, y, 0)$  (red contour: $|\vec{{N}}|=1$,  max=${vmax:.2f}$)")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # Panel 2: |N| at y=0 slice
    ax = axes[0, 1]
    im = ax.imshow(
        Nmag[:, k, :].T,
        origin="lower",
        extent=[-L, L, -L, L],
        cmap="viridis",
        aspect="equal",
        vmin=0,
        vmax=vmax,
    )
    ax.contour(xs, xs, Nmag[:, k, :].T, levels=[1.0], colors="red", linewidths=2)
    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.set_title(r"$|\vec{N}|(x, 0, z)$ (red: $|\vec{N}|=1$ surface)")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # Panel 3: |N| along principal axes through origin
    ax = axes[1, 0]
    ax.plot(xs, Nmag[:, k, k], label=r"$|\vec{N}|$ along $x$-axis ($y=z=0$)")
    ax.plot(xs, Nmag[k, :, k], label=r"$|\vec{N}|$ along $y$-axis ($x=z=0$)")
    ax.plot(xs, Nmag[k, k, :], label=r"$|\vec{N}|$ along $z$-axis ($x=y=0$)")
    ax.axhline(1.0, color="red", linestyle="--", linewidth=1, label=r"$|\vec{N}|=1$ (horizon)")
    ax.set_xlabel("axis coordinate")
    ax.set_ylabel(r"$|\vec{N}|$")
    ax.set_yscale("log")
    ax.set_title(r"Cross-sections through origin")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 4: histogram of |N| over the box, with |N|=1 marked
    ax = axes[1, 1]
    flat = Nmag.ravel()
    ax.hist(flat, bins=60, edgecolor="black", linewidth=0.3, log=True)
    ax.axvline(1.0, color="red", linestyle="--", linewidth=2, label=r"$|\vec{N}|=1$")
    ax.set_xlabel(r"$|\vec{N}|$")
    ax.set_ylabel("cell count (log)")
    super_frac = float((flat >= 1).mean())
    ax.set_title(rf"$|\vec{{N}}|$ distribution ({100*super_frac:.2f}% of cells superluminal)")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3, which="both")

    fig.suptitle(
        f"Foliation-health analysis ({label}): "
        rf"$V={point['V']}, \sigma={point['sigma']}, m_0={point['m0']}, a={point['a']}, \ell={point['ell']}, r={point['r']}$",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    plt.close(fig)


def v_scan(base: dict, V_values: Iterable[float], Npts: int) -> list[FoliationDiagnostics]:
    """Vary V at fixed (sigma, m0, a, ell, r) to find the smallest V where the
    superluminal region first appears (the "subluminal-everywhere" upper-V limit)."""
    out = []
    for V in V_values:
        pt = {**base, "V": float(V)}
        diag, _, _ = diagnostics(pt, Npts=Npts)
        out.append(diag)
    return out


def plot_v_scan(scan: list[FoliationDiagnostics], out_path: Path, label: str) -> None:
    """Plot N_max_box, passenger zone radius, and dt_timelike_fraction vs V."""
    Vs = np.array([d.V for d in scan])
    Nmax = np.array([d.N_max_box for d in scan])
    pass_radius = np.array([d.passenger_zone_radius for d in scan])
    pass_volume = np.array([d.passenger_zone_volume for d in scan])
    timelike = np.array([d.dt_timelike_fraction for d in scan])

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))

    ax = axes[0, 0]
    ax.plot(Vs, Nmax, "o-")
    ax.axhline(1.0, color="red", linestyle="--", linewidth=1, label=r"$|\vec{N}|=1$ horizon")
    ax.set_xlabel("V")
    ax.set_ylabel(r"$|\vec{N}|_{\max}$ over box")
    ax.set_title(r"Max shift magnitude vs $V$ (where horizon first appears)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[0, 1]
    ax.plot(Vs, pass_radius, "o-")
    ax.set_xlabel("V")
    ax.set_ylabel("passenger-zone radius")
    ax.set_title("Passenger zone (largest sphere at origin with $|\\vec{N}|<1$)")
    ax.grid(True, alpha=0.3)

    ax = axes[1, 0]
    ax.plot(Vs, pass_volume, "o-")
    ax.set_xlabel("V")
    ax.set_ylabel("passenger-zone volume")
    ax.set_yscale("log")
    ax.set_title("Passenger-zone volume (log scale)")
    ax.grid(True, alpha=0.3, which="both")

    ax = axes[1, 1]
    ax.plot(Vs, timelike * 100, "o-")
    ax.axhline(100, color="green", linestyle="--", linewidth=1, label="100% timelike")
    ax.set_xlabel("V")
    ax.set_ylabel(r"% box where $\partial_t$ is timelike")
    ax.set_title("Foliation-healthy fraction")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.suptitle(f"V-scan: foliation health + passenger-zone vs V\n({label})", fontsize=11)
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    plt.close(fig)


def representative_winners() -> list[tuple[str, dict]]:
    """A small set of WEC+DEC-passing winners spanning the band, for the
    leaderboard analysis. Each tuple is (label, point_dict).
    """
    base = dict(Pi=0.25, L=12.0)
    return [
        ("canonical-V1p5", {**base, "V": 1.5, "sigma": 10.0, "m0": 3.0, "a": 0.05, "ell": 4.0, "r": 9.0}),
        # Same point at V=0.1 — subluminal everywhere?
        ("canonical-V0p1", {**base, "V": 0.1, "sigma": 10.0, "m0": 3.0, "a": 0.05, "ell": 4.0, "r": 9.0}),
        # Smaller r/sigma combo
        ("compact-V1",     {**base, "V": 1.0, "sigma": 6.0,  "m0": 3.0, "a": 0.1,  "ell": 4.0, "r": 6.0}),
        # Edge of band: small sigma
        ("edge-V0p5",      {**base, "V": 0.5, "sigma": 4.0,  "m0": 2.5, "a": 0.05, "ell": 4.0, "r": 5.0}),
        # Higher m0
        ("high-m0-V0p5",   {**base, "V": 0.5, "sigma": 8.0,  "m0": 3.5, "a": 0.05, "ell": 4.0, "r": 7.0}),
    ]


def main(out_dir: Path, Npts: int = 97) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary: dict = {"Npts": Npts, "winners": [], "v_scan": []}

    # Per-winner foliation-health diagnostics + plot.
    for label, point in representative_winners():
        diag, Nmag, xs = diagnostics(point, Npts=Npts)
        plot_foliation(point, Nmag, xs, out_dir / f"foliation_{label}.png", label)
        d_dict = asdict(diag)
        d_dict["label"] = label
        summary["winners"].append(d_dict)
        print(f"  {label:>16s}: |N|max={diag.N_max_box:>7.3f}  N_origin={diag.N_origin:>9.2e}  "
              f"super_frac={diag.superluminal_fraction:.4f}  pass_R={diag.passenger_zone_radius:>5.2f}  "
              f"pass_vol={diag.passenger_zone_volume:>9.3e}  timelike_frac={diag.dt_timelike_fraction:.4f}")

    # V-scan on canonical (sigma=10, m0=3, a=0.05, ell=4, r=9) to find the
    # smallest V with any superluminal cell.
    V_values = [0.01, 0.03, 0.05, 0.08, 0.10, 0.13, 0.15, 0.20, 0.30, 0.50, 0.75, 1.00, 1.50, 2.00]
    base = dict(Pi=0.25, L=12.0, sigma=10.0, m0=3.0, a=0.05, ell=4.0, r=9.0)
    scan = v_scan(base, V_values, Npts=Npts)
    summary["v_scan"] = [asdict(d) for d in scan]

    plot_v_scan(scan, out_dir / "v_scan.png", "canonical (sigma=10, m0=3, a=0.05, ell=4, r=9)")
    print()
    print("V scan on canonical (sigma=10, m0=3, a=0.05, ell=4, r=9):")
    for d in scan:
        marker = " <-- subluminal everywhere" if d.N_max_box < 1.0 else ""
        print(f"  V={d.V:>5.3f}: |N|max={d.N_max_box:>7.3f}  pass_R={d.passenger_zone_radius:>5.2f}  pass_vol={d.passenger_zone_volume:>9.3e}{marker}")

    # Find smallest V where superluminal region appears
    sub_threshold = next((d for d in scan if d.N_max_box >= 1.0), None)
    if sub_threshold is not None:
        sub_max_V = max((d.V for d in scan if d.N_max_box < 1.0), default=None)
        summary["sub_to_super_transition"] = {
            "V_last_subluminal": sub_max_V,
            "V_first_superluminal": sub_threshold.V,
        }

    # Leaderboard CSV
    import pandas as pd
    rows = summary["winners"] + [{**asdict(d), "label": f"V-scan-{d.V:.3f}"} for d in scan]
    pd.DataFrame(rows).to_csv(out_dir / "leaderboard.csv", index=False)

    with open(out_dir / "summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)

    return summary


def _cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--Npts", type=int, default=97)
    args = parser.parse_args(argv)
    main(args.out_dir, Npts=args.Npts)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())

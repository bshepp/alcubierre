"""Standalone PNG renders of the project's headline data.

Subcommand dispatch script. Each subcommand reads a sweep parquet or CSV and
writes one or more PNGs into ``figures/<topic>/``. See ``figures/README.md``.

Run ``python figures/plot_figures.py all`` to regenerate every figure,
or ``python figures/plot_figures.py <subcommand>`` for one at a time.
Per AGENTS.md, this is *permanent infrastructure* (not a ``diag_*``/``fix_*``
scratch script): it serves the documented figures programme and is
re-runnable.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm, colors

REPO = Path(__file__).resolve().parent.parent
SWEEPS = REPO / "sweeps"
SWEEPS_REMOTE = REPO / "sweeps_remote"
WF = REPO / "warp_factory_repro"
FIG = REPO / "figures"
WEB_FIG = REPO / "webpage" / "assets" / "figures"  # mirror for the website

# Consistent style.
DPI = 200
FIGSIZE_DEFAULT = (8.0, 6.0)
FACECOLOR = "white"

plt.rcParams.update(
    {
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "savefig.facecolor": FACECOLOR,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 10,
    }
)


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", facecolor=FACECOLOR)
    plt.close(fig)
    # Mirror into webpage/assets/figures/ for website deploys.
    rel = path.relative_to(FIG)
    web_path = WEB_FIG / rel
    web_path.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(path, web_path)
    print(f"  -> {path.relative_to(REPO)}  ({path.stat().st_size // 1024} KB)  [mirrored -> {web_path.relative_to(REPO)}]")


# ---------------------------------------------------------------------------
# A.2  Fell-Heisenberg 5x5 corner plot
# ---------------------------------------------------------------------------


def fh_corner() -> None:
    """5x5 hexbin corner of strict-pass FH cells in (sigma, m0, a, ell, r)."""
    parquet = (
        SWEEPS_REMOTE
        / "full-20260420T022727"
        / "fell_heisenberg_20260420T022809.parquet"
    )
    df = pd.read_parquet(parquet)
    strict = df[
        (df["ok"] == True)  # noqa: E712
        & (df["wec_pass_fraction"] == 1.0)
        & (df["dec_slack_min"] > 0)
    ].copy()
    print(f"fh_corner: {len(strict)}/{len(df)} strict-pass cells")

    axes_names = ("sigma", "m0", "a", "ell", "r")
    n = len(axes_names)
    fig, axs = plt.subplots(n, n, figsize=(13, 13), constrained_layout=True)
    cmap = cm.viridis
    norm = colors.Normalize(
        vmin=float(strict["dec_slack_min"].min()),
        vmax=float(strict["dec_slack_min"].max()),
    )

    for i, yi in enumerate(axes_names):
        for j, xj in enumerate(axes_names):
            ax = axs[i, j]
            if i == j:
                ax.hist(strict[xj], bins=20, color="#2a7fff", alpha=0.85)
                ax.set_yscale("log")
                ax.set_ylabel("count" if j == 0 else "")
            elif i > j:
                # 2D: color by mean dec_slack_min in each (xj, yi) cell.
                sc = ax.scatter(
                    strict[xj],
                    strict[yi],
                    c=strict["dec_slack_min"],
                    cmap=cmap,
                    norm=norm,
                    s=10,
                    alpha=0.7,
                    edgecolors="none",
                )
            else:
                ax.set_visible(False)
                continue
            if i == n - 1:
                ax.set_xlabel(xj)
            if j == 0 and i != 0:
                ax.set_ylabel(yi)

    cbar_ax = fig.add_axes([0.78, 0.62, 0.015, 0.25])
    cbar = fig.colorbar(
        cm.ScalarMappable(norm=norm, cmap=cmap),
        cax=cbar_ax,
    )
    cbar.set_label("dec_slack_min  (positive = strict pass)", fontsize=9)
    fig.suptitle(
        f"Fell-Heisenberg strict-pass manifold ({len(strict)} / {len(df)} cells)\n"
        f"Slice: V \u2208 [0.1, 1.5]; cells with WEC = 100 % and DEC > 0",
        fontsize=13, y=0.99,
    )
    _save(fig, FIG / "fell_heisenberg" / "strict_pass_corner.png")


# ---------------------------------------------------------------------------
# A.3  kappa-surface 3D scatter + facet grid
# ---------------------------------------------------------------------------


def kappa_surface_3d() -> None:
    """Two PNGs: 3D scatter (C, R2, beta) and facet grid kappa vs beta."""
    csv = WF / "kappa_surface_sweep.csv"
    df = pd.read_csv(csv)
    print(f"kappa_surface: {len(df)} rows")

    # ----- (a) 3D scatter -----
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    valid = df.dropna(subset=["kappa_mid"])
    capped = df[df["kappa_mid"].isna() | df["kappa_lower"].isna() | df["kappa_upper"].isna()]
    sc = ax.scatter(
        valid["C"],
        valid["R2"],
        valid["beta"],
        c=valid["kappa_mid"],
        cmap="plasma",
        s=80,
        edgecolors="black",
        linewidths=0.4,
    )
    if len(capped):
        ax.scatter(
            capped["C"],
            capped["R2"],
            capped["beta"],
            c="red",
            marker="x",
            s=70,
            label=f"cap-saturated / one-sided ({len(capped)})",
        )
    ax.set_xlabel("compactness $C$")
    ax.set_ylabel("$R_2$ [m]")
    ax.set_zlabel(r"$\beta$")
    ax.set_title(
        "Phase 3.2 κ-surface (Warp Factory, Fuchs comoving shell)\n"
        "Slice: spherical, single-shell, static, asymptotically flat"
    )
    cbar = fig.colorbar(sc, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label(r"$\kappa_{\rm mid}$")
    if len(capped):
        ax.legend(loc="upper left", fontsize=8)
    _save(fig, FIG / "warp_factory" / "kappa_surface_3d.png")

    # ----- (b) Facet grid: kappa vs beta, one panel per (C, R2) -----
    Cs = sorted(df["C"].unique())
    R2s = sorted(df["R2"].unique())
    nC, nR = len(Cs), len(R2s)
    fig, axs = plt.subplots(
        nC, nR, figsize=(3.0 * nR, 2.6 * nC), sharex=True, sharey=True,
        constrained_layout=True,
    )
    axs = np.atleast_2d(axs)
    kappa_anal = 0.875  # 2A.9a upper analytic
    for i, C in enumerate(Cs):
        for j, R2 in enumerate(R2s):
            ax = axs[i, j]
            sub = df[(df["C"] == C) & (df["R2"] == R2)].sort_values("beta")
            if len(sub) == 0:
                ax.set_visible(False)
                continue
            yerr_lo = sub["kappa_mid"] - sub["kappa_lower"]
            yerr_hi = sub["kappa_upper"] - sub["kappa_mid"]
            ax.errorbar(
                sub["beta"],
                sub["kappa_mid"],
                yerr=[yerr_lo.fillna(0), yerr_hi.fillna(0)],
                fmt="o-",
                color="#2a7fff",
                capsize=3,
                lw=1.0,
            )
            ax.axhline(kappa_anal, color="orange", lw=1, ls="--", alpha=0.7)
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_title(f"C={C:.3g}, $R_2$={R2}", fontsize=9)
            if i == nC - 1:
                ax.set_xlabel(r"$\beta$")
            if j == 0:
                ax.set_ylabel(r"$\kappa$ (numerical)")
    fig.suptitle(
        r"$\kappa$ vs $\beta$ across the Phase-3.2 surface "
        f"(orange dashed: analytic 2A.9a κ = {kappa_anal})",
        fontsize=12,
    )
    _save(fig, FIG / "warp_factory" / "kappa_surface_facets.png")


# ---------------------------------------------------------------------------
# A.4  Thickness-bound heatmap with analytic overlay
# ---------------------------------------------------------------------------


def thickness_heatmap() -> None:
    parquet = SWEEPS / "thickness_bound_20260416T145855.parquet"
    df = pd.read_parquet(parquet)
    print(f"thickness_bound: {len(df)} rows")

    Cs_avail = sorted(df["compactness"].unique())
    targets = [Cs_avail[len(Cs_avail) // 6],
               Cs_avail[len(Cs_avail) // 2],
               Cs_avail[(5 * len(Cs_avail)) // 6]]

    fig, axs = plt.subplots(1, 3, figsize=(15, 4.5), constrained_layout=True)
    vmax = float(np.nanpercentile(np.abs(df["worst_slack"]), 95))
    vmax = max(vmax, 0.05)
    norm = colors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    for ax, C in zip(axs, targets):
        sub = df[np.isclose(df["compactness"], C)]
        if len(sub) == 0:
            ax.set_visible(False)
            continue
        pivot = sub.pivot_table(
            index="Delta_over_R", columns="beta", values="worst_slack",
            aggfunc="mean",
        )
        im = ax.pcolormesh(
            pivot.columns, pivot.index, pivot.values,
            cmap="RdBu_r", norm=norm, shading="auto",
        )
        # Overlay analytic prediction lines: Delta_min/R = kappa * beta / C.
        beta_arr = np.array(sorted(sub["beta"].unique()))
        for kappa, ls, lab in [
            (0.05, ":", r"$\kappa=0.05$ (analytic lower)"),
            (0.875, "--", r"$\kappa=0.875$ (analytic upper / 2A.9a)"),
            (5.0, "-", r"$\kappa=5$ (Warp Factory numerical)"),
        ]:
            y = kappa * beta_arr / C
            ax.plot(beta_arr, y, ls=ls, color="black", lw=1.2, label=lab)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(r"$\beta$")
        ax.set_ylabel(r"$\Delta / R$")
        ax.set_title(f"compactness $C = {C:.3g}$", fontsize=10)
        ax.grid(False)

    cbar = fig.colorbar(im, ax=axs, shrink=0.85, pad=0.02)
    cbar.set_label(r"worst DEC slack  (red = violated, blue = passes)")
    axs[0].legend(loc="lower right", fontsize=7, framealpha=0.9)
    fig.suptitle(
        "Thickness bound: numerical DEC slack vs analytic prediction "
        r"$\Delta_{\min}/R = \kappa \beta / C$" + "\n"
        "Slice: spherical Fuchs shell, static, asymptotically flat (Path 2A.9)",
        fontsize=11,
    )
    _save(fig, FIG / "thickness_bound" / "heatmap_with_analytic.png")


# ---------------------------------------------------------------------------
# A.5  Krasnikov universal-collapse plot
# ---------------------------------------------------------------------------


def krasnikov_collapse() -> None:
    parquet = SWEEPS / "krasnikov_tube_20260416T213051.parquet"
    df = pd.read_parquet(parquet)
    print(f"krasnikov: {len(df)} rows")

    fig, axs = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)

    # ----- (a) raw rho_p_min vs eta, colored by eps -----
    ax = axs[0]
    eps_vals = sorted(df["eps"].unique())
    cmap = cm.viridis
    for k, eps in enumerate(eps_vals):
        sub = df[df["eps"] == eps].sort_values("eta")
        ax.plot(
            sub["eta"], -sub["rho_p_min"],
            "o-", color=cmap(k / max(1, len(eps_vals) - 1)),
            lw=1, ms=3, label=f"ε = {eps:.3g}",
        )
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"$\eta$ (tube speed parameter)")
    ax.set_ylabel(r"$|\rho_p^{\min}|$  (raw)")
    ax.set_title("Raw negative-energy density vs η")
    ax.legend(fontsize=7, loc="lower right")

    # ----- (b) collapsed: |rho_p_min| * eps^2 vs eta -----
    ax = axs[1]
    for k, eps in enumerate(eps_vals):
        sub = df[df["eps"] == eps].sort_values("eta")
        ax.plot(
            sub["eta"], -sub["rho_p_min"] * eps**2,
            "o-", color=cmap(k / max(1, len(eps_vals) - 1)),
            lw=1, ms=3, label=f"ε = {eps:.3g}",
        )
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"$\eta$ (tube speed parameter)")
    ax.set_ylabel(r"$|\rho_p^{\min}|\cdot\varepsilon^{2}$  (collapsed)")
    ax.set_title(r"Universal collapse: all $\varepsilon$ on one curve  $\Rightarrow\ \kappa_K$ scaling law")
    ax.legend(fontsize=7, loc="lower right")

    fig.suptitle(
        "Krasnikov tube — Task 2A.13 universal collapse "
        r"($|\rho_p^{\min}|\cdot\varepsilon^{2} \propto \eta^{-1}$)" "\n"
        "Slice: cylindrical Krasnikov tube, classical-curvature scan",
        fontsize=11,
    )
    _save(fig, FIG / "krasnikov" / "universal_collapse.png")


# ---------------------------------------------------------------------------
# A.6  GW-recoil cliff plot
# ---------------------------------------------------------------------------


def gw_recoil_cliff() -> None:
    paths = sorted(SWEEPS.glob("gw_recoil_*.parquet"))
    if not paths:
        raise SystemExit("No gw_recoil_*.parquet files found")
    df = pd.concat([pd.read_parquet(p) for p in paths], ignore_index=True)
    print(f"gw_recoil: {len(df)} rows from {len(paths)} parquets")

    Cs = sorted(df["C"].unique())
    nC = len(Cs)
    ncols = min(nC, 5)
    nrows = (nC + ncols - 1) // ncols
    fig, axs = plt.subplots(
        nrows, ncols, figsize=(3.4 * ncols, 4.5 * nrows),
        sharex=True, sharey=True, constrained_layout=True,
    )
    axs = np.atleast_1d(axs).reshape(-1)
    n_orbit_vals = sorted(df["n_orbits"].unique())
    cmap = cm.plasma
    norm = colors.LogNorm(vmin=min(n_orbit_vals), vmax=max(n_orbit_vals))

    c_light = 299792458.0
    for k, C in enumerate(Cs):
        ax = axs[k]
        sub = df[df["C"] == C]
        sc = ax.scatter(
            sub["beta"], sub["dv_kick"],
            c=sub["n_orbits"], cmap=cmap, norm=norm,
            s=15, alpha=0.8, edgecolors="none",
        )
        beta_line = np.logspace(np.log10(sub["beta"].min()), np.log10(sub["beta"].max()), 100)
        ax.plot(beta_line, c_light * np.tanh(beta_line), color="black", lw=1, ls="--", alpha=0.5)
        for v_ref, lbl in [(1, "1 m/s"), (1e3, "1 km/s"), (c_light, "c")]:
            ax.axhline(v_ref, color="grey", lw=0.8, ls=":", alpha=0.6)
            ax.text(beta_line[-1] * 1.02, v_ref, lbl, fontsize=7, va="center", color="grey")
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(f"C = {C:.3g}", fontsize=9)
        if k % ncols == 0:
            ax.set_ylabel(r"$\Delta v_{\rm kick}$  [m/s]")
        if k // ncols == nrows - 1:
            ax.set_xlabel(r"$\beta$")
    for k in range(nC, len(axs)):
        axs[k].set_visible(False)

    cbar = fig.colorbar(sc, ax=axs.tolist(), shrink=0.85, pad=0.02)
    cbar.set_label(r"$n_{\rm orbits}$")
    fig.suptitle(
        "GW recoil — kick velocity vs β, faceted by compactness C\n"
        "Slice: PN inspiral + SXS rescaling, single bubble (Path 2A acceleration null)",
        fontsize=11,
    )
    _save(fig, FIG / "gw_recoil" / "dv_cliff.png")


# ---------------------------------------------------------------------------
# A.7  Hybrid-wall pass-fraction heatmap
# ---------------------------------------------------------------------------


def hybrid_wall_heatmap() -> None:
    parquet = SWEEPS / "hybrid_wall_20260417T002249.parquet"
    df = pd.read_parquet(parquet)
    print(f"hybrid_wall: {len(df)} rows")

    eta_vals = sorted(df["eta"].unique())
    fig, axs = plt.subplots(
        len(eta_vals), 2,
        figsize=(11, 2.6 * len(eta_vals)),
        sharex=True, sharey=True, constrained_layout=True,
    )
    axs = np.atleast_2d(axs)
    for i, eta in enumerate(eta_vals):
        sub = df[np.isclose(df["eta"], eta)]
        for j, (col, title, cmap) in enumerate(
            [("wec_fraction", "WEC pass fraction", "viridis"),
             ("dec_fraction", "DEC pass fraction", "viridis")]
        ):
            ax = axs[i, j]
            pivot = sub.pivot_table(
                index="w_M", columns="delta_M", values=col, aggfunc="mean",
            )
            im = ax.pcolormesh(
                pivot.columns, pivot.index, pivot.values,
                cmap=cmap, vmin=0, vmax=1, shading="auto",
            )
            if j == 0:
                ax.set_ylabel(rf"$w_M$   (η = {eta:.3g})")
            if i == len(eta_vals) - 1:
                ax.set_xlabel(r"$\delta_M$")
            ax.set_title(title if i == 0 else "", fontsize=10)
            ax.grid(False)
            fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    fig.suptitle(
        "Hybrid-wall slice — WEC and DEC pass fractions over (δ_M, w_M), per η\n"
        "Slice: ε = 1, n = 100, n_rho = 1601 (Phase 2D Slice 6)",
        fontsize=11,
    )
    _save(fig, FIG / "hybrid_wall" / "pass_fraction.png")


# ---------------------------------------------------------------------------
# A.8  Shift-families bar chart
# ---------------------------------------------------------------------------


def shift_families_bars() -> None:
    parquet = SWEEPS / "shift_families_20260416T235319.parquet"
    df = pd.read_parquet(parquet)
    print(f"shift_families: {len(df)} rows, families = {sorted(df['family'].unique())}")

    families = sorted(df["family"].unique())
    metrics = [
        ("wec_fraction", "WEC pass fraction"),
        ("dec_fraction", "DEC pass fraction"),
        ("dec_slack_min", "DEC slack min  (positive = pass)"),
    ]
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.2), constrained_layout=True)
    x = np.arange(len(families))
    colors_per_fam = cm.tab10(np.linspace(0, 1, len(families)))
    for ax, (col, title) in zip(axs, metrics):
        med = df.groupby("family")[col].median().reindex(families)
        q25 = df.groupby("family")[col].quantile(0.25).reindex(families)
        q75 = df.groupby("family")[col].quantile(0.75).reindex(families)
        yerr = np.vstack([med.values - q25.values, q75.values - med.values])
        ax.bar(x, med.values, color=colors_per_fam, yerr=yerr, capsize=4,
               edgecolor="black", linewidth=0.5)
        ax.set_xticks(x); ax.set_xticklabels(families, rotation=20, ha="right", fontsize=9)
        ax.set_title(title, fontsize=10)
        ax.axhline(0, color="black", lw=0.8)
        if "fraction" in col:
            ax.set_ylim(-0.05, 1.05)
    fig.suptitle(
        "Shift-vector families — median pass fractions and DEC slack min "
        "(error bars: 25-75 percentile)\n"
        "Slice: 140 sweep cells across (v, R₀, σ); see "
        "SHIFT_FAMILIES_NOTES.md for parametric scope",
        fontsize=11,
    )
    _save(fig, FIG / "shift_families" / "family_comparison.png")


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

SUBCOMMANDS = {
    "fh-corner": fh_corner,
    "kappa-surface-3d": kappa_surface_3d,
    "thickness-heatmap": thickness_heatmap,
    "krasnikov-collapse": krasnikov_collapse,
    "gw-recoil-cliff": gw_recoil_cliff,
    "hybrid-wall-heatmap": hybrid_wall_heatmap,
    "shift-families-bars": shift_families_bars,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render standalone PNG figures from sweep data.",
    )
    parser.add_argument(
        "subcommand",
        choices=list(SUBCOMMANDS) + ["all"],
        help="Which figure to render. Use 'all' to render every figure.",
    )
    args = parser.parse_args(argv)

    if args.subcommand == "all":
        for name, fn in SUBCOMMANDS.items():
            print(f"\n=== {name} ===")
            try:
                fn()
            except Exception as exc:  # noqa: BLE001
                print(f"  FAILED: {exc!r}", file=sys.stderr)
        return 0

    SUBCOMMANDS[args.subcommand]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

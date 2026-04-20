"""Polynomial-surface fitting of the Fell-Heisenberg WEC+DEC slack response.

Tests whether the strict-pass region's boundary surface (the level set
``dec_slack_min = 0``) admits a low-degree polynomial implicit equation,
and whether the slack value field admits a low-degree polynomial expansion.

The two questions are answered separately because they have different
expected mathematical structure:

- The boundary surface (a 4-D hypersurface in 5-D parameter space) is
  the zero level set of the slack and may admit a low-degree polynomial
  approximation even if the slack itself has transcendental factors.
- The slack value field has transcendental contributions (FH potential
  contains exp + erf), so polynomial fits to slack values will have
  systematic non-Gaussian residuals.

Reads the strict-pass parquet output by ``hf_jobs/sweeps/fell_heisenberg.py``;
saves diagnostic plots and a JSON summary to the chosen output directory.

Usage::

    python -m hf_jobs.analysis.fell_heisenberg_polyfit \\
        sweeps_remote/refine-20260420T041817/fell_heisenberg_20260420T041859.parquet \\
        --out-dir fell_heisenberg_topology/
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

PARAM_AXES: tuple[str, ...] = ("sigma", "m0", "a", "ell", "r")


def fit_slack_polynomial(
    df_near: pd.DataFrame,
    degrees: tuple[int, ...] = (1, 2, 3, 4, 5),
) -> dict:
    """Fit polynomial regression of dec_slack_min on standardised parameters,
    over the near-boundary subset. Returns per-degree summary + best-degree
    residual analysis.
    """
    X = df_near[list(PARAM_AXES)].values
    y = df_near["dec_slack_min"].values
    X_std = StandardScaler().fit_transform(X)

    rows = []
    best = None
    for deg in degrees:
        poly = PolynomialFeatures(degree=deg, include_bias=False)
        Xp = poly.fit_transform(X_std)
        if Xp.shape[1] > len(df_near) - 50:
            continue
        reg = LinearRegression().fit(Xp, y)
        resid = y - reg.predict(Xp)
        cv = KFold(n_splits=5, shuffle=True, random_state=0)
        cv_r2 = float(np.mean([
            LinearRegression().fit(Xp[tr], y[tr]).score(Xp[te], y[te])
            for tr, te in cv.split(Xp)
        ]))
        rows.append({
            "degree": deg,
            "n_features": int(Xp.shape[1]),
            "r2_train": float(reg.score(Xp, y)),
            "r2_cv": cv_r2,
            "rmse": float(np.sqrt((resid ** 2).mean())),
            "resid_std": float(resid.std()),
            "resid_p95_abs": float(np.percentile(np.abs(resid), 95)),
        })
        best = (deg, resid, reg.predict(Xp))
    return {"per_degree": rows, "best_degree": best[0] if best else None,
            "best_resid": best[1] if best else None,
            "best_pred": best[2] if best else None}


def boundary_classifier_sweep(
    df_ok: pd.DataFrame,
    degrees: tuple[int, ...] = (1, 2, 3, 4, 5),
) -> list[dict]:
    """Logistic-regression classification of pass vs fail at increasing
    polynomial degree. Tests whether the boundary surface itself admits
    a low-degree polynomial approximation, regardless of whether the
    slack values do.
    """
    X = df_ok[list(PARAM_AXES)].values
    y_bin = (df_ok["dec_slack_min"] > 0).astype(int).values
    X_std = StandardScaler().fit_transform(X)

    rows = []
    for deg in degrees:
        Xp = PolynomialFeatures(degree=deg, include_bias=False).fit_transform(X_std)
        cv = KFold(n_splits=5, shuffle=True, random_state=0)
        accs, f1s = [], []
        for tr, te in cv.split(Xp):
            clf = LogisticRegression(C=1.0, max_iter=2000).fit(Xp[tr], y_bin[tr])
            accs.append(accuracy_score(y_bin[te], clf.predict(Xp[te])))
            f1s.append(f1_score(y_bin[te], clf.predict(Xp[te])))
        rows.append({
            "degree": deg,
            "n_features": int(Xp.shape[1]),
            "accuracy_cv": float(np.mean(accs)),
            "f1_cv": float(np.mean(f1s)),
        })
    return rows


def residual_structure_diagnostics(
    df_near: pd.DataFrame,
    resid: np.ndarray,
    pred: np.ndarray,
    out_path: Path,
    deg: int,
) -> dict:
    """Plot residual structure (histogram + scatter + QQ + per-axis) and
    return Spearman correlations of residuals with each input axis.
    """
    from scipy.stats import spearmanr
    spearman = {}
    for col in PARAM_AXES:
        rho, p = spearmanr(df_near[col].values, resid)
        spearman[col] = {"rho": float(rho), "p": float(p)}

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))

    ax = axes[0, 0]
    ax.hist(resid, bins=80, edgecolor="black", linewidth=0.3)
    ax.set_title(f"Residual distribution (deg {deg})")
    ax.set_xlabel("residual")
    ax.axvline(0, color="red", linestyle="--", alpha=0.5)
    ax.grid(True, alpha=0.3)

    ax = axes[0, 1]
    ax.scatter(pred, resid, s=2, alpha=0.3)
    ax.axhline(0, color="red", linestyle="--", alpha=0.5)
    ax.set_xlabel("predicted dec_slack")
    ax.set_ylabel("residual")
    ax.set_title(f"Residuals vs predicted (deg {deg})")
    ax.grid(True, alpha=0.3)

    ax = axes[0, 2]
    stats.probplot(resid, dist="norm", plot=ax)
    ax.set_title(f"QQ vs Gaussian (deg {deg}): straight line = Gaussian noise")
    ax.grid(True, alpha=0.3)

    for i, col in enumerate(("sigma", "m0", "r")):
        ax = axes[1, i]
        ax.scatter(df_near[col].values, resid, s=2, alpha=0.3)
        ax.axhline(0, color="red", linestyle="--", alpha=0.5)
        ax.set_xlabel(col)
        ax.set_ylabel("residual")
        ax.set_title(f"Residuals vs {col}")
        ax.grid(True, alpha=0.3)

    fig.suptitle(
        f"Residual analysis: polynomial fit deg={deg}, n_samples={len(df_near)}",
        fontsize=12,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    plt.close(fig)

    return {"spearman": spearman}


def plot_classifier_curve(rows: list[dict], out_path: Path) -> None:
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    degs = [r["degree"] for r in rows]
    ax.plot(degs, [r["accuracy_cv"] for r in rows], "o-", label="binary accuracy (CV)")
    ax.plot(degs, [r["f1_cv"] for r in rows], "s-", label="F1 (CV)")
    ax.set_xlabel("Polynomial degree")
    ax.set_ylabel("Score")
    ax.set_title("Boundary surface: pass-vs-fail classifier accuracy vs degree")
    ax.set_xticks(degs)
    ax.set_ylim([0.7, 1.01])
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    plt.close(fig)


def main(parquet_path: Path, out_dir: Path, near_threshold: float = 0.05) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(parquet_path)
    ok = df[df["ok"] == True]
    near = ok[np.abs(ok["dec_slack_min"]) < near_threshold].copy()

    slack_fit = fit_slack_polynomial(near)
    classifier_sweep = boundary_classifier_sweep(ok)

    if slack_fit["best_degree"] is not None:
        diag = residual_structure_diagnostics(
            near,
            slack_fit["best_resid"],
            slack_fit["best_pred"],
            out_dir / "poly_fit_residuals.png",
            slack_fit["best_degree"],
        )
    else:
        diag = {}
    plot_classifier_curve(classifier_sweep, out_dir / "boundary_classifier_curve.png")

    summary = {
        "n_ok": int(len(ok)),
        "n_near_boundary": int(len(near)),
        "near_threshold": float(near_threshold),
        "slack_polynomial_fit": {
            "per_degree": slack_fit["per_degree"],
            "best_degree": slack_fit["best_degree"],
            "residual_spearman": diag.get("spearman", {}),
        },
        "boundary_classifier": classifier_sweep,
    }
    with open(out_dir / "polyfit_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)
    return summary


def _cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("parquet", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument(
        "--near-threshold",
        type=float,
        default=0.05,
        help="Restrict slack-regression to |dec_slack_min| < this threshold.",
    )
    args = parser.parse_args(argv)

    summary = main(args.parquet, args.out_dir, near_threshold=args.near_threshold)
    print()
    print("=== Slack polynomial regression (near-boundary subset) ===")
    print(f"{'Deg':>3} {'#feat':>5} {'R^2 train':>10} {'R^2 CV':>9} {'RMSE':>11} {'Resid 95%':>11}")
    for r in summary["slack_polynomial_fit"]["per_degree"]:
        print(f"{r['degree']:>3d} {r['n_features']:>5d} "
              f"{r['r2_train']:>10.5f} {r['r2_cv']:>9.5f} "
              f"{r['rmse']:>11.5e} {r['resid_p95_abs']:>11.5e}")
    print()
    print("=== Residual Spearman correlations (best degree) ===")
    for ax, st in summary["slack_polynomial_fit"]["residual_spearman"].items():
        flag = "STRUCTURED" if abs(st["rho"]) > 0.05 else "noise-like"
        print(f"  resid vs {ax:>5s}: rho = {st['rho']:+.4f}  p = {st['p']:.2e}  {flag}")
    print()
    print("=== Boundary classifier (pass vs fail) ===")
    print(f"{'Deg':>3} {'#feat':>5} {'Acc CV':>8} {'F1 CV':>8}")
    for r in summary["boundary_classifier"]:
        print(f"{r['degree']:>3d} {r['n_features']:>5d} "
              f"{r['accuracy_cv']:>8.5f} {r['f1_cv']:>8.5f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())

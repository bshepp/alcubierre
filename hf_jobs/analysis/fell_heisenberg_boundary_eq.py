"""Extract a closed-form polynomial implicit boundary equation P(sigma, m0, a, ell, r) = 0
for the Fell-Heisenberg WEC+DEC strict-pass region (Task 2D.5b).

Per Session 13 (FELL_HEISENBERG_SWEEP_NOTES.md section 7.8) the boundary
surface is approximately a degree-4-5 polynomial implicit surface (binary
classifier accuracy at degree 5 is 99.4% on Npts=97 data).

This module:
1. Fits logistic regression of pass/fail vs polynomial features at multiple
   degrees, with no regularization (large C) so we get the true coefficients.
2. Extracts the coefficients in BOTH standardized and physical-units form.
3. Sorts terms by absolute magnitude, drops terms below a noise threshold.
4. Reports the surviving terms and tests if they have any clean dimensionless
   pattern.
5. Saves the surviving boundary equation as a structured JSON for downstream
   analysis or symbolic manipulation.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations_with_replacement
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

PARAM_AXES: tuple[str, ...] = ("sigma", "m0", "a", "ell", "r")


def feature_names(degree: int, axes: tuple[str, ...] = PARAM_AXES) -> list[str]:
    """Generate human-readable feature names for PolynomialFeatures(degree, include_bias=False).

    Order matches sklearn's: sorted lexicographically by (total_degree, monomial)
    using combinations_with_replacement.
    """
    names = []
    for d in range(1, degree + 1):
        for combo in combinations_with_replacement(axes, d):
            counts: dict[str, int] = {}
            for ax in combo:
                counts[ax] = counts.get(ax, 0) + 1
            term = " * ".join(
                ax if c == 1 else f"{ax}^{c}"
                for ax, c in counts.items()
            )
            names.append(term)
    return names


def standardised_to_physical(
    coefs_std: np.ndarray,
    intercept_std: float,
    feature_names_list: list[str],
    scaler: StandardScaler,
    axes: tuple[str, ...] = PARAM_AXES,
) -> tuple[np.ndarray, float]:
    """Convert standardized polynomial coefficients to physical-units coefficients.

    NOTE: this is non-trivial because the polynomial features are products of
    standardized vars, e.g. (sigma_std)^2 = ((sigma - mu_sigma)/std_sigma)^2.
    Expanding this gives a polynomial in sigma with coefficients that mix.

    For the lowest practical effort, we report the standardized coefficients
    and provide the linear scaler (mu, std) for each axis so a consumer can
    recover the physical form by hand if needed.

    Returns (coefs_std, intercept_std) unchanged for now -- the standardized
    form is what the analysis uses; physical-unit conversion is a separate
    symbolic exercise.
    """
    return coefs_std, intercept_std


def fit_boundary_polynomial(
    df: pd.DataFrame,
    degree: int,
    C_no_reg: float = 1e8,
) -> dict:
    """Fit logistic regression of pass/fail vs polynomial features."""
    X = df[list(PARAM_AXES)].values
    y_bin = (df["dec_slack_min"] > 0).astype(int).values

    scaler = StandardScaler().fit(X)
    X_std = scaler.transform(X)

    poly = PolynomialFeatures(degree=degree, include_bias=False)
    Xp = poly.fit_transform(X_std)

    # Use very large C (effectively no regularization) so coefs are not shrunk.
    clf = LogisticRegression(C=C_no_reg, max_iter=20000, solver="lbfgs").fit(Xp, y_bin)

    # In-sample diagnostics.
    pred = clf.predict(Xp)
    pred_proba = clf.predict_proba(Xp)[:, 1]
    train_acc = float((pred == y_bin).mean())

    feat_names = feature_names(degree)
    assert len(feat_names) == Xp.shape[1], f"feature names mismatch: {len(feat_names)} vs {Xp.shape[1]}"

    return {
        "degree": degree,
        "n_features": Xp.shape[1],
        "n_samples": int(len(df)),
        "train_accuracy": train_acc,
        "coefs": clf.coef_.ravel(),
        "intercept": float(clf.intercept_[0]),
        "feature_names": feat_names,
        "scaler_mean": scaler.mean_,
        "scaler_std": scaler.scale_,
        "predictions": pred,
        "probabilities": pred_proba,
        "labels": y_bin,
    }


def threshold_coefs(fit: dict, threshold_frac: float = 0.01) -> dict:
    """Drop coefficients with |coef| < threshold_frac * max|coef|.

    Returns a dict with only the surviving terms in sorted order.
    """
    coefs = fit["coefs"]
    max_abs = float(np.abs(coefs).max())
    threshold = threshold_frac * max_abs

    keep = np.abs(coefs) >= threshold
    survivors = sorted(
        [
            {"name": fit["feature_names"][i], "coef": float(coefs[i]), "rank": int(np.argsort(-np.abs(coefs))[i])}
            for i in range(len(coefs))
            if keep[i]
        ],
        key=lambda d: -abs(d["coef"]),
    )
    return {
        "n_total": len(coefs),
        "n_kept": int(keep.sum()),
        "threshold_frac": threshold_frac,
        "threshold_abs": threshold,
        "max_abs_coef": max_abs,
        "survivors": survivors,
    }


def evaluate_on_holdout(
    fit: dict,
    df: pd.DataFrame,
    coefs_thresholded: np.ndarray | None = None,
) -> dict:
    """Test the fitted (or thresholded) coefficients on the data and report
    accuracy, confusion-matrix-style breakdown.

    If coefs_thresholded is None, uses the full coefs from fit.
    """
    X = df[list(PARAM_AXES)].values
    y_bin = (df["dec_slack_min"] > 0).astype(int).values

    mean = fit["scaler_mean"]
    std = fit["scaler_std"]
    X_std = (X - mean) / std
    poly = PolynomialFeatures(degree=fit["degree"], include_bias=False)
    Xp = poly.fit_transform(X_std)

    coefs = coefs_thresholded if coefs_thresholded is not None else fit["coefs"]
    logit = Xp @ coefs + fit["intercept"]
    pred = (logit > 0).astype(int)

    correct = int((pred == y_bin).sum())
    n = len(y_bin)
    return {
        "n": n,
        "n_correct": correct,
        "accuracy": correct / n,
        "false_positive": int(((pred == 1) & (y_bin == 0)).sum()),
        "false_negative": int(((pred == 0) & (y_bin == 1)).sum()),
    }


def physical_dimension_check(survivors: list[dict]) -> dict:
    """Investigate whether the surviving terms have a clean dimensionless pattern.

    Counts how many survivors involve each axis, what total-degree they are at,
    and whether ratios like r/m0, r/sqrt(sigma) appear consistently.
    """
    by_degree: dict[int, list] = {}
    axis_counts: dict[str, int] = {ax: 0 for ax in PARAM_AXES}
    for s in survivors:
        # Total degree of the monomial
        terms = s["name"].split(" * ")
        d = sum(int(t.split("^")[1]) if "^" in t else 1 for t in terms)
        by_degree.setdefault(d, []).append(s)
        for t in terms:
            ax = t.split("^")[0]
            n = int(t.split("^")[1]) if "^" in t else 1
            axis_counts[ax] += n

    return {
        "by_degree": {d: len(rows) for d, rows in by_degree.items()},
        "axis_total_powers": axis_counts,
        "top_5_terms": survivors[:5] if survivors else [],
    }


def main(parquet_path: Path, out_dir: Path, degree: int = 4) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(parquet_path)
    ok = df[df["ok"] == True]
    print(f"Loaded {len(df)} points; {len(ok)} ok")
    print()

    summary: dict = {"degrees": {}}

    # Try degrees 3, 4, 5 to see how the picture changes.
    for d in [3, 4, 5]:
        print(f"=== Degree {d} fit (no regularization) ===")
        fit = fit_boundary_polynomial(ok, degree=d)
        n_thresh = threshold_coefs(fit, threshold_frac=0.01)

        # Test thresholded coefs against full data
        coefs_kept = fit["coefs"].copy()
        keep_mask = np.abs(coefs_kept) >= n_thresh["threshold_abs"]
        coefs_kept[~keep_mask] = 0.0
        eval_full = evaluate_on_holdout(fit, ok)
        eval_thresholded = evaluate_on_holdout(fit, ok, coefs_thresholded=coefs_kept)

        physical = physical_dimension_check(n_thresh["survivors"])

        print(f"  Train accuracy (all {fit['n_features']} features): {fit['train_accuracy']:.5f}")
        print(f"  Largest |coef|:                                      {n_thresh['max_abs_coef']:.4e}")
        print(f"  Surviving (|coef| > 1% of max):                      {n_thresh['n_kept']} / {fit['n_features']}")
        print(f"  Accuracy with thresholded coefs:                     {eval_thresholded['accuracy']:.5f}")
        print(f"  Top 5 by |coef|:")
        for s in n_thresh["survivors"][:5]:
            print(f"    {s['coef']:>+12.4f}  *  {s['name']}")
        print(f"  Surviving terms by degree: {physical['by_degree']}")
        print(f"  Total power per axis:       {physical['axis_total_powers']}")
        print()

        summary["degrees"][str(d)] = {
            "n_features": fit["n_features"],
            "train_accuracy": fit["train_accuracy"],
            "thresholded_accuracy": eval_thresholded["accuracy"],
            "intercept": fit["intercept"],
            "thresholded": n_thresh,
            "physical": physical,
            "scaler_mean": fit["scaler_mean"].tolist(),
            "scaler_std": fit["scaler_std"].tolist(),
        }

    # Save full degree-4 fit (the recommended one per session 13 §7.8) including all coefs
    full_fit = fit_boundary_polynomial(ok, degree=4)
    coefs_full = [
        {"name": full_fit["feature_names"][i], "coef": float(full_fit["coefs"][i])}
        for i in range(len(full_fit["coefs"]))
    ]
    coefs_full.sort(key=lambda d: -abs(d["coef"]))
    summary["degree_4_full_coefficients"] = coefs_full
    summary["degree_4_intercept"] = full_fit["intercept"]

    # Plot: thresholded vs full accuracy across degrees
    fig, ax = plt.subplots(1, 1, figsize=(9, 5))
    degs = sorted([int(d) for d in summary["degrees"].keys()])
    full_accs = [summary["degrees"][str(d)]["train_accuracy"] for d in degs]
    thresh_accs = [summary["degrees"][str(d)]["thresholded_accuracy"] for d in degs]
    n_kept = [summary["degrees"][str(d)]["thresholded"]["n_kept"] for d in degs]
    ax.plot(degs, full_accs, "o-", label="all features (no regularization)")
    ax.plot(degs, thresh_accs, "s-", label="thresholded (drop |coef| < 1% of max)")
    ax.set_xlabel("Polynomial degree")
    ax.set_ylabel("In-sample accuracy")
    ax.set_xticks(degs)
    ax.set_ylim([0.9, 1.005])
    ax.grid(True, alpha=0.3)
    ax.legend()
    for i, (d, n) in enumerate(zip(degs, n_kept)):
        ax.annotate(f"{n} kept", (d, thresh_accs[i]), textcoords="offset points", xytext=(0, -15), fontsize=8, ha="center")
    ax.set_title("Polynomial-boundary fit: thresholding effect")
    fig.tight_layout()
    fig.savefig(out_dir / "thresholding_effect.png", dpi=110, bbox_inches="tight")
    plt.close(fig)

    with open(out_dir / "boundary_eq_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)

    # Save the degree-4 surviving coefficients as CSV for easy inspection
    deg4 = summary["degrees"]["4"]["thresholded"]
    pd.DataFrame(deg4["survivors"]).to_csv(out_dir / "degree4_surviving_terms.csv", index=False)

    return summary


def _cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("parquet", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--degree", type=int, default=4)
    args = parser.parse_args(argv)
    main(args.parquet, args.out_dir, degree=args.degree)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())

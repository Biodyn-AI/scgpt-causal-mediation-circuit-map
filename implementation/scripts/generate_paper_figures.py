#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE = Path("/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map")
RESULTS = BASE / "implementation" / "results_refined"
FIG_DIR = BASE / "reports" / "figures"


def _savefig(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_mediator_mass(summary: pd.DataFrame) -> None:
    tissues = ["kidney", "lung", "immune"]
    heads = []
    mlp = []
    for tissue in tissues:
        h = summary[(summary["tissue"] == tissue) & (summary["granularity"] == "heads")]
        m = summary[(summary["tissue"] == tissue) & (summary["granularity"] == "mlp")]
        heads.append(float(h["top5_mediator_mass"].iloc[0]) if not h.empty else np.nan)
        mlp.append(float(m["top5_mediator_mass"].iloc[0]) if not m.empty else np.nan)

    x = np.arange(len(tissues))
    width = 0.36

    plt.figure(figsize=(7.2, 4.2))
    plt.bar(x - width / 2, heads, width, label="Heads", color="#4C78A8")
    plt.bar(x + width / 2, mlp, width, label="MLP", color="#F58518")
    plt.xticks(x, [t.capitalize() for t in tissues])
    plt.ylim(0.0, 1.05)
    plt.ylabel("Top-5 mediator mass")
    plt.title("Mediator Concentration Across Tissues")
    plt.legend(frameon=False)
    _savefig(FIG_DIR / "fig_mediator_mass_refined.png")


def plot_overlap(overlap: pd.DataFrame) -> None:
    pair_order = ["kidney-lung", "kidney-immune", "lung-immune"]
    granularity_order = ["heads", "mlp"]

    values = np.full((len(granularity_order), len(pair_order)), np.nan)
    for i, gran in enumerate(granularity_order):
        for j, pair in enumerate(pair_order):
            ta, tb = pair.split("-")
            row = overlap[
                (overlap["granularity"] == gran)
                & (overlap["tissue_a"] == ta)
                & (overlap["tissue_b"] == tb)
            ]
            if not row.empty:
                values[i, j] = float(row["mean_jaccard_top5"].iloc[0])

    plt.figure(figsize=(7.2, 3.1))
    im = plt.imshow(values, aspect="auto", cmap="YlGnBu", vmin=0.0, vmax=1.0)
    plt.colorbar(im, label="Top-5 Jaccard")
    plt.yticks(np.arange(len(granularity_order)), [g.upper() for g in granularity_order])
    plt.xticks(np.arange(len(pair_order)), [p.replace("-", " vs ") for p in pair_order])
    plt.title("Cross-Tissue Mediator Overlap")

    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            if np.isfinite(values[i, j]):
                plt.text(j, i, f"{values[i, j]:.2f}", ha="center", va="center", color="black", fontsize=9)

    _savefig(FIG_DIR / "fig_overlap_jaccard_refined.png")


def plot_effects_by_pair(base: Path) -> None:
    tissues = ["kidney", "lung", "immune"]
    records = []
    for tissue in tissues:
        path = base / tissue / "heads" / "causal_scores.tsv"
        df = pd.read_csv(path, sep="\t")
        df = df[df["intervention"] == "ablation"].copy()
        for _, row in df.iterrows():
            records.append(
                {
                    "tissue": tissue,
                    "pair": f"{row['source']}->{row['target']}",
                    "effect_mean": float(row["effect_mean"]),
                    "n_cells": int(row["n_cells"]),
                }
            )

    all_df = pd.DataFrame(records)
    pairs = sorted(all_df["pair"].unique())

    x = np.arange(len(tissues))
    width = 0.38
    plt.figure(figsize=(8.0, 4.6))

    # Limit to top two pairs expected in refined run for visual clarity.
    for idx, pair in enumerate(pairs[:2]):
        subset = all_df[all_df["pair"] == pair]
        vals = [float(subset[subset["tissue"] == t]["effect_mean"].iloc[0]) if not subset[subset["tissue"] == t].empty else np.nan for t in tissues]
        shift = (-width / 2) if idx == 0 else (width / 2)
        color = "#54A24B" if idx == 0 else "#E45756"
        bars = plt.bar(x + shift, vals, width, label=pair, color=color, alpha=0.9)

        for bar, tissue in zip(bars, tissues):
            cell_row = subset[subset["tissue"] == tissue]
            if not cell_row.empty:
                n_cells = int(cell_row["n_cells"].iloc[0])
                y = bar.get_height()
                va = "bottom" if y >= 0 else "top"
                offset = 0.004 if y >= 0 else -0.004
                plt.text(bar.get_x() + bar.get_width() / 2, y + offset, f"n={n_cells}", ha="center", va=va, fontsize=8)

    plt.axhline(0.0, color="black", linewidth=0.9)
    plt.xticks(x, [t.capitalize() for t in tissues])
    plt.ylabel("Ablation effect mean")
    plt.title("Cross-Tissue Effect Sizes for Shared Pairs")
    plt.legend(frameon=False)
    _savefig(FIG_DIR / "fig_pair_effects_refined.png")


def main() -> None:
    summary = pd.read_csv(RESULTS / "summary_metrics.tsv", sep="\t")
    overlap = pd.read_csv(RESULTS / "overlap_metrics.tsv", sep="\t")

    plot_mediator_mass(summary)
    plot_overlap(overlap)
    plot_effects_by_pair(RESULTS)


if __name__ == "__main__":
    main()

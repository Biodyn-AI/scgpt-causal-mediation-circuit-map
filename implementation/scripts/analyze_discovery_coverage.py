#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "implementation" / "results"
DEFAULT_SUMMARY_OUTPUT = PROJECT_ROOT / "implementation" / "results_refined" / "discovery_coverage_metrics.tsv"
DEFAULT_SHARED_OUTPUT = PROJECT_ROOT / "implementation" / "results_refined" / "discovery_shared_pairs.tsv"


def _read_scores(results_dir: Path, tissue: str, dataset: str) -> pd.DataFrame:
    score_path = results_dir / tissue / dataset / "causal_scores.tsv"
    if not score_path.exists():
        return pd.DataFrame(columns=["source", "target", "effect_mean", "n_cells"])
    df = pd.read_csv(score_path, sep="\t")
    if df.empty:
        return pd.DataFrame(columns=["source", "target", "effect_mean", "n_cells"])
    df = df[df["intervention"] == "ablation"].copy()
    df["pair"] = df["source"].astype(str) + "->" + df["target"].astype(str)
    return df


def _pair_set(df: pd.DataFrame, min_cells: int) -> set[str]:
    if df.empty:
        return set()
    return set(df.loc[df["n_cells"] >= min_cells, "pair"].tolist())


def _shared_pair_rows(
    by_tissue: dict[str, pd.DataFrame],
    dataset: str,
    min_cells: int,
    tissues: Iterable[str],
) -> list[dict[str, object]]:
    tissue_list = list(tissues)
    pair_sets = [_pair_set(by_tissue[tissue], min_cells) for tissue in tissue_list]
    shared_pairs = sorted(set.intersection(*pair_sets)) if pair_sets else []
    rows: list[dict[str, object]] = []
    for pair in shared_pairs:
        source, target = pair.split("->", maxsplit=1)
        cells = []
        abs_effects = []
        for tissue in tissue_list:
            tissue_df = by_tissue[tissue]
            row = tissue_df[(tissue_df["source"] == source) & (tissue_df["target"] == target)]
            if row.empty:
                break
            selected = row.iloc[0]
            cells.append(int(selected["n_cells"]))
            abs_effects.append(abs(float(selected["effect_mean"])))
        else:
            rows.append(
                {
                    "dataset": dataset,
                    "min_cells_threshold": min_cells,
                    "pair": pair,
                    "min_cells_across_tissues": min(cells),
                    "mean_abs_effect_across_tissues": sum(abs_effects) / len(abs_effects),
                    "kidney_cells": cells[0],
                    "lung_cells": cells[1],
                    "immune_cells": cells[2],
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize cross-tissue support coverage from discovery ablation outputs."
    )
    parser.add_argument(
        "--results-dir",
        default=str(DEFAULT_RESULTS_DIR),
        help="Base directory containing <tissue>/<dataset>/causal_scores.tsv outputs.",
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=["discovery", "discovery_fixed40"],
        help="Discovery dataset subdirectories to summarize.",
    )
    parser.add_argument(
        "--thresholds",
        nargs="+",
        type=int,
        default=[1, 3, 5, 10],
        help="Minimum n_cells thresholds for considering a pair as tissue-supported.",
    )
    parser.add_argument(
        "--summary-output",
        default=str(DEFAULT_SUMMARY_OUTPUT),
    )
    parser.add_argument(
        "--shared-output",
        default=str(DEFAULT_SHARED_OUTPUT),
    )
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    tissues = ["kidney", "lung", "immune"]

    summary_rows: list[dict[str, object]] = []
    shared_rows: list[dict[str, object]] = []

    for dataset in args.datasets:
        by_tissue = {tissue: _read_scores(results_dir, tissue, dataset) for tissue in tissues}
        all_pairs = sorted(set().union(*[set(df["pair"].tolist()) for df in by_tissue.values()]))
        for min_cells in args.thresholds:
            tissue_sets = [_pair_set(by_tissue[tissue], min_cells) for tissue in tissues]
            shared_all = set.intersection(*tissue_sets) if tissue_sets else set()
            union_all = set.union(*tissue_sets) if tissue_sets else set()
            summary_rows.append(
                {
                    "dataset": dataset,
                    "min_cells_threshold": min_cells,
                    "total_unique_pairs_observed": len(all_pairs),
                    "kidney_supported_pairs": len(tissue_sets[0]),
                    "lung_supported_pairs": len(tissue_sets[1]),
                    "immune_supported_pairs": len(tissue_sets[2]),
                    "union_supported_pairs": len(union_all),
                    "shared_all_tissues_pairs": len(shared_all),
                }
            )
            shared_rows.extend(
                _shared_pair_rows(
                    by_tissue=by_tissue,
                    dataset=dataset,
                    min_cells=min_cells,
                    tissues=tissues,
                )
            )

    summary_df = pd.DataFrame(summary_rows)
    shared_df = pd.DataFrame(shared_rows)
    summary_output = Path(args.summary_output)
    shared_output = Path(args.shared_output)
    summary_output.parent.mkdir(parents=True, exist_ok=True)
    shared_output.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(summary_output, sep="\t", index=False)
    shared_df.to_csv(shared_output, sep="\t", index=False)

    print(f"Wrote summary coverage table: {summary_output}")
    print(f"Wrote shared-pair table: {shared_output}")


if __name__ == "__main__":
    main()

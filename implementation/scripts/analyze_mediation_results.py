#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RunKey:
    tissue: str
    granularity: str


def _component_id(row: pd.Series) -> str:
    component = str(row["component"])
    layer = int(row["layer"]) if not pd.isna(row["layer"]) else -1
    if component == "head":
        head = int(row["head"]) if not pd.isna(row["head"]) else -1
        return f"L{layer}:H{head}"
    if component == "mlp":
        return f"L{layer}:MLP"
    return f"L{layer}:{component}"


def _read_run(base_dir: Path, tissue: str, granularity: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    run_dir = base_dir / tissue / granularity
    scores = pd.read_csv(run_dir / "causal_scores.tsv", sep="\t")
    circuits = pd.read_csv(run_dir / "circuit_maps.tsv", sep="\t")
    if circuits.empty:
        return scores, circuits
    circuits = circuits.copy()
    circuits["component_id"] = circuits.apply(_component_id, axis=1)
    return scores, circuits


def _pair_key(df: pd.DataFrame) -> pd.Series:
    return df["source"].astype(str) + "->" + df["target"].astype(str)


def _top_components(circuits: pd.DataFrame, top_k: int) -> Dict[Tuple[str, str], List[str]]:
    out: Dict[Tuple[str, str], List[str]] = {}
    if circuits.empty:
        return out
    grouped = circuits.copy()
    grouped["abs_restoration"] = grouped["restoration_mean"].abs()
    for (source, target), group in grouped.groupby(["source", "target"], sort=False):
        top = group.sort_values("abs_restoration", ascending=False).head(top_k)
        out[(str(source), str(target))] = top["component_id"].tolist()
    return out


def _jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    set_a = set(a)
    set_b = set(b)
    if not set_a and not set_b:
        return float("nan")
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def _restoration_ci95(mean: float, std: float, n: int) -> tuple[float, float]:
    if n <= 1 or not np.isfinite(std):
        return mean, mean
    half = 1.96 * (std / math.sqrt(float(n)))
    return mean - half, mean + half


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate mediation tracing results")
    parser.add_argument(
        "--results-dir",
        default="/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/implementation/results",
    )
    parser.add_argument(
        "--report-path",
        default="/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/reports/causal_mediation_circuit_map_report.md",
    )
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    base_dir = Path(args.results_dir)
    tissues = ["kidney", "lung", "immune"]
    granularities = ["heads", "mlp"]

    runs: Dict[RunKey, Tuple[pd.DataFrame, pd.DataFrame]] = {}
    for tissue in tissues:
        for granularity in granularities:
            runs[RunKey(tissue, granularity)] = _read_run(base_dir, tissue, granularity)

    summary_rows = []
    pair_rows = []
    top_rows = []
    observed_pairs: set[str] = set()

    for key, (scores, circuits) in runs.items():
        score_subset = scores[scores["intervention"] == "ablation"].copy()
        if score_subset.empty:
            continue
        score_subset["pair"] = _pair_key(score_subset)
        observed_pairs.update(score_subset["pair"].tolist())
        n_pairs = int(score_subset.shape[0])
        mean_effect = float(score_subset["effect_mean"].mean())
        mean_abs_effect = float(score_subset["effect_mean"].abs().mean())

        circuits_local = circuits.copy()
        if circuits_local.empty:
            mediator_concentration = float("nan")
        else:
            circuits_local["pair"] = _pair_key(circuits_local)
            circuits_local["abs_restoration"] = circuits_local["restoration_mean"].abs()
            concentration_vals = []
            for _, group in circuits_local.groupby("pair"):
                denom = float(group["abs_restoration"].sum())
                if denom <= 0:
                    continue
                numer = float(group.sort_values("abs_restoration", ascending=False).head(args.top_k)["abs_restoration"].sum())
                concentration_vals.append(numer / denom)
            mediator_concentration = float(np.mean(concentration_vals)) if concentration_vals else float("nan")

            top_comp = circuits_local.sort_values("abs_restoration", ascending=False).head(10)
            for _, row in top_comp.iterrows():
                ci_low, ci_high = _restoration_ci95(float(row["restoration_mean"]), float(row["restoration_std"]), int(row["n_cells"]))
                top_rows.append(
                    {
                        "tissue": key.tissue,
                        "granularity": key.granularity,
                        "pair": row["pair"],
                        "component": row["component_id"],
                        "restoration_mean": float(row["restoration_mean"]),
                        "ci95_low": ci_low,
                        "ci95_high": ci_high,
                        "n_cells": int(row["n_cells"]),
                    }
                )

        summary_rows.append(
            {
                "tissue": key.tissue,
                "granularity": key.granularity,
                "pairs_with_scores": n_pairs,
                "mean_effect": mean_effect,
                "mean_abs_effect": mean_abs_effect,
                f"top{args.top_k}_mediator_mass": mediator_concentration,
            }
        )

        if not circuits.empty:
            circuits_pair = circuits.copy()
            circuits_pair["pair"] = _pair_key(circuits_pair)
            circuits_pair["abs_restoration"] = circuits_pair["restoration_mean"].abs()
            per_pair = (
                circuits_pair.groupby("pair", as_index=False)
                .agg(
                    components=("component_id", "nunique"),
                    mean_abs_restoration=("abs_restoration", "mean"),
                    max_abs_restoration=("abs_restoration", "max"),
                )
                .sort_values("max_abs_restoration", ascending=False)
            )
            for _, row in per_pair.iterrows():
                pair_rows.append(
                    {
                        "tissue": key.tissue,
                        "granularity": key.granularity,
                        "pair": row["pair"],
                        "components": int(row["components"]),
                        "mean_abs_restoration": float(row["mean_abs_restoration"]),
                        "max_abs_restoration": float(row["max_abs_restoration"]),
                    }
                )

    overlap_rows = []
    for granularity in granularities:
        top_by_tissue: Dict[str, Dict[Tuple[str, str], List[str]]] = {}
        for tissue in tissues:
            _, circuits = runs[RunKey(tissue, granularity)]
            top_by_tissue[tissue] = _top_components(circuits, args.top_k)

        tissue_pairs = [("kidney", "lung"), ("kidney", "immune"), ("lung", "immune")]
        for ta, tb in tissue_pairs:
            shared_pairs = sorted(set(top_by_tissue[ta].keys()) & set(top_by_tissue[tb].keys()))
            if not shared_pairs:
                continue
            jaccards = []
            for pair in shared_pairs:
                jaccards.append(_jaccard(top_by_tissue[ta][pair], top_by_tissue[tb][pair]))
            overlap_rows.append(
                {
                    "granularity": granularity,
                    "tissue_a": ta,
                    "tissue_b": tb,
                    "shared_pairs": len(shared_pairs),
                    f"mean_jaccard_top{args.top_k}": float(np.nanmean(jaccards)) if jaccards else float("nan"),
                }
            )

    summary_df = pd.DataFrame(summary_rows)
    pair_df = pd.DataFrame(pair_rows)
    top_df = pd.DataFrame(top_rows)
    overlap_df = pd.DataFrame(overlap_rows)

    base_dir.mkdir(parents=True, exist_ok=True)
    summary_path = base_dir / "summary_metrics.tsv"
    pairs_path = base_dir / "pair_metrics.tsv"
    top_path = base_dir / "top_components.tsv"
    overlap_path = base_dir / "overlap_metrics.tsv"
    summary_df.to_csv(summary_path, sep="\t", index=False)
    pair_df.to_csv(pairs_path, sep="\t", index=False)
    top_df.to_csv(top_path, sep="\t", index=False)
    overlap_df.to_csv(overlap_path, sep="\t", index=False)

    report_path = Path(args.report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []
    lines.append("# Causal Mediation Circuit Map: Pilot Results")
    lines.append("")
    lines.append("## Scope")
    lines.append("- Task source: `market_research/ambitious_paper_questions/idea_02_causal_mediation_circuit_map.md`.")
    lines.append("- Data source: preprocessed `.h5ad` files referenced by run configs in this workspace.")
    lines.append(f"- Pair set: {len(observed_pairs)} unique TF-target pairs observed in ablation outputs.")
    lines.append("- Tracing modes: attention heads (top-2 heads per layer) and MLP blocks.")
    lines.append("")

    lines.append("## Aggregate Metrics")
    lines.append("")
    if not summary_df.empty:
        lines.append(summary_df.to_markdown(index=False))
    else:
        lines.append("No summary metrics available.")
    lines.append("")

    lines.append("## Cross-Tissue Mediator Overlap")
    lines.append("")
    if not overlap_df.empty:
        lines.append(overlap_df.to_markdown(index=False))
    else:
        lines.append("No overlap metrics available.")
    lines.append("")

    lines.append("## Strongest Components")
    lines.append("")
    if not top_df.empty:
        lines.append(top_df.head(30).to_markdown(index=False))
    else:
        lines.append("No component-level rows available.")
    lines.append("")

    lines.append("## Artifacts")
    lines.append("- Run outputs: `subproject_09_causal_mediation_circuit_map/implementation/results/<tissue>/<granularity>/`.")
    lines.append(f"- Summary table: `{summary_path}`")
    lines.append(f"- Pair table: `{pairs_path}`")
    lines.append(f"- Top components: `{top_path}`")
    lines.append(f"- Overlap table: `{overlap_path}`")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report: {report_path}")
    print(f"Wrote summary: {summary_path}")


if __name__ == "__main__":
    main()

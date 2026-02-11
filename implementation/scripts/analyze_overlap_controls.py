#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd

# Resolve project paths from this script location so the script is portable
# across clones and does not depend on machine-specific absolute paths.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "implementation" / "results_refined"
DEFAULT_OVERLAP_CONTROL_OUTPUT = PROJECT_ROOT / "implementation" / "results_refined" / "overlap_control_metrics.tsv"
DEFAULT_PAIR_ROBUSTNESS_OUTPUT = PROJECT_ROOT / "implementation" / "results_refined" / "pair_robustness_metrics.tsv"


def _component_id(row: pd.Series) -> str:
    """Construct stable component identifiers for heads and MLP blocks."""
    component = str(row["component"])
    layer = int(row["layer"])
    if component == "head":
        return f"L{layer}:H{int(row['head'])}"
    return f"L{layer}:MLP"


def _read_circuit_maps(base_dir: Path, tissue: str, granularity: str) -> pd.DataFrame:
    """Load component-level mediation outputs for one tissue and granularity."""
    path = base_dir / tissue / granularity / "circuit_maps.tsv"
    df = pd.read_csv(path, sep="\t")
    if df.empty:
        return df
    out = df.copy()
    out["pair"] = out["source"].astype(str) + "->" + out["target"].astype(str)
    out["component_id"] = out.apply(_component_id, axis=1)
    out["abs_restoration"] = out["restoration_mean"].abs()
    return out


def _read_pair_effects(base_dir: Path, tissue: str) -> pd.DataFrame:
    """Load ablation-only pair effects from the heads run (shared pair-level TE)."""
    path = base_dir / tissue / "heads" / "causal_scores.tsv"
    df = pd.read_csv(path, sep="\t")
    df = df[df["intervention"] == "ablation"].copy()
    df["pair"] = df["source"].astype(str) + "->" + df["target"].astype(str)
    return df


def _top_components(df: pd.DataFrame, pair: str, top_k: int) -> set[str]:
    """Return the top-k components by absolute restoration for one pair."""
    top = df[df["pair"] == pair].sort_values("abs_restoration", ascending=False).head(top_k)
    return set(top["component_id"].tolist())


def _jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    """Compute Jaccard similarity between two component sets."""
    set_a = set(a)
    set_b = set(b)
    if not set_a and not set_b:
        return float("nan")
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def _random_expected_jaccard(component_space_size: int, top_k: int) -> float:
    """
    Expected Jaccard overlap between two random top-k sets drawn without
    replacement from the same component space.
    """
    # E[intersection] = k^2 / N. Approximate E[J] by plugging into J = I/(2k-I),
    # which is accurate enough for reviewer-facing sanity controls.
    expected_intersection = (top_k * top_k) / float(component_space_size)
    return expected_intersection / (2.0 * top_k - expected_intersection)


def _build_component_spaces(circuit_maps: Dict[str, Dict[str, pd.DataFrame]]) -> Dict[str, List[str]]:
    """Build per-granularity component universes observed in refined runs."""
    spaces: Dict[str, set[str]] = {"heads": set(), "mlp": set()}
    for granularity in ["heads", "mlp"]:
        for tissue_df in circuit_maps[granularity].values():
            spaces[granularity].update(tissue_df["component_id"].unique().tolist())
    return {k: sorted(v) for k, v in spaces.items()}


def _collect_pairwise_jaccards(
    tissue_maps: Dict[str, pd.DataFrame], top_k: int
) -> tuple[list[float], list[dict[str, object]], dict[str, list[float]]]:
    """
    Collect pairwise Jaccard values across tissue pairs and per pair identity.

    Returns:
      - flat list of all pairwise Jaccard values,
      - detailed rows with tissue-pair metadata,
      - pair -> list of Jaccard values across tissue pairs.
    """
    pairwise_values: list[float] = []
    detailed_rows: list[dict[str, object]] = []
    by_pair: dict[str, list[float]] = {}
    tissues = sorted(tissue_maps.keys())
    for tissue_a, tissue_b in combinations(tissues, 2):
        df_a = tissue_maps[tissue_a]
        df_b = tissue_maps[tissue_b]
        shared_pairs = sorted(set(df_a["pair"]) & set(df_b["pair"]))
        for pair in shared_pairs:
            j = _jaccard(_top_components(df_a, pair, top_k), _top_components(df_b, pair, top_k))
            pairwise_values.append(j)
            by_pair.setdefault(pair, []).append(j)
            detailed_rows.append(
                {
                    "tissue_a": tissue_a,
                    "tissue_b": tissue_b,
                    "pair": pair,
                    "top_k": top_k,
                    "jaccard": j,
                }
            )
    return pairwise_values, detailed_rows, by_pair


def _permutation_pvalue(
    observed_mean: float,
    num_values: int,
    component_ids: list[str],
    top_k: int,
    num_permutations: int,
    rng: np.random.Generator,
) -> tuple[float, float]:
    """Permutation null for mean Jaccard under random top-k component sets."""
    sims = np.empty(num_permutations, dtype=float)
    n = len(component_ids)
    for i in range(num_permutations):
        j_vals = []
        for _ in range(num_values):
            a_idx = rng.choice(n, size=top_k, replace=False)
            b_idx = rng.choice(n, size=top_k, replace=False)
            set_a = {component_ids[j] for j in a_idx.tolist()}
            set_b = {component_ids[j] for j in b_idx.tolist()}
            j_vals.append(_jaccard(set_a, set_b))
        sims[i] = float(np.mean(j_vals))
    p_value = float((np.sum(sims >= observed_mean) + 1) / (num_permutations + 1))
    return float(np.mean(sims)), p_value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze overlap controls: null expectations, sensitivity, and pair robustness."
    )
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR))
    parser.add_argument("--top-k-values", nargs="+", type=int, default=[3, 5, 8, 10])
    parser.add_argument("--permutation-top-k", type=int, default=5)
    parser.add_argument("--permutations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--overlap-output", default=str(DEFAULT_OVERLAP_CONTROL_OUTPUT))
    parser.add_argument("--pair-output", default=str(DEFAULT_PAIR_ROBUSTNESS_OUTPUT))
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    tissues = ["kidney", "lung", "immune"]

    # Load all refined circuit maps once and reuse across control computations.
    circuit_maps: Dict[str, Dict[str, pd.DataFrame]] = {"heads": {}, "mlp": {}}
    for granularity in ["heads", "mlp"]:
        for tissue in tissues:
            circuit_maps[granularity][tissue] = _read_circuit_maps(results_dir, tissue, granularity)

    component_spaces = _build_component_spaces(circuit_maps)
    rng = np.random.default_rng(args.seed)

    overlap_rows: list[dict[str, object]] = []
    pair_rows: list[dict[str, object]] = []

    # Compute overlap controls and top-k sensitivity.
    for granularity in ["heads", "mlp"]:
        tissue_maps = circuit_maps[granularity]
        component_space_size = len(component_spaces[granularity])
        for top_k in args.top_k_values:
            j_values, detailed_rows, by_pair = _collect_pairwise_jaccards(tissue_maps, top_k)
            if not j_values:
                continue
            observed_mean = float(np.mean(j_values))
            expected_random = _random_expected_jaccard(component_space_size, top_k)
            enrichment = observed_mean / expected_random if expected_random > 0 else float("nan")
            row = {
                "granularity": granularity,
                "top_k": top_k,
                "component_space_size": component_space_size,
                "num_pairwise_values": len(j_values),
                "observed_mean_jaccard": observed_mean,
                "random_expected_jaccard": expected_random,
                "enrichment_vs_random": enrichment,
            }
            if top_k == args.permutation_top_k:
                null_mean, p_value = _permutation_pvalue(
                    observed_mean=observed_mean,
                    num_values=len(j_values),
                    component_ids=component_spaces[granularity],
                    top_k=top_k,
                    num_permutations=args.permutations,
                    rng=rng,
                )
                row["permutation_null_mean"] = null_mean
                row["permutation_p_value"] = p_value
            overlap_rows.append(row)

            # Add per-pair overlap means at the primary top-k for reviewer-facing heterogeneity checks.
            if top_k == args.permutation_top_k:
                for pair, values in sorted(by_pair.items()):
                    pair_rows.append(
                        {
                            "pair": pair,
                            "granularity": granularity,
                            "top_k": top_k,
                            "mean_pair_jaccard": float(np.mean(values)),
                            "min_pair_jaccard": float(np.min(values)),
                            "max_pair_jaccard": float(np.max(values)),
                            "num_tissue_pairs": len(values),
                        }
                    )

    # Add pair-level sign consistency and support from ablation effects.
    effect_frames = [_read_pair_effects(results_dir, tissue).assign(tissue=tissue) for tissue in tissues]
    effects = pd.concat(effect_frames, ignore_index=True)
    for pair, group in effects.groupby("pair"):
        sign_values = np.sign(group["effect_mean"].to_numpy(dtype=float))
        sign_consistency = float(abs(sign_values.sum()) / len(sign_values))
        pair_rows.append(
            {
                "pair": pair,
                "granularity": "pair_effect",
                "top_k": args.permutation_top_k,
                "mean_pair_jaccard": float("nan"),
                "min_pair_jaccard": float("nan"),
                "max_pair_jaccard": float("nan"),
                "num_tissue_pairs": 3,
                "effect_sign_consistency": sign_consistency,
                "mean_abs_effect": float(group["effect_mean"].abs().mean()),
                "min_cells_across_tissues": int(group["n_cells"].min()),
                "max_cells_across_tissues": int(group["n_cells"].max()),
            }
        )

    overlap_df = pd.DataFrame(overlap_rows).sort_values(["granularity", "top_k"]).reset_index(drop=True)
    pair_df = pd.DataFrame(pair_rows).sort_values(["pair", "granularity"]).reset_index(drop=True)

    overlap_output = Path(args.overlap_output)
    pair_output = Path(args.pair_output)
    overlap_output.parent.mkdir(parents=True, exist_ok=True)
    pair_output.parent.mkdir(parents=True, exist_ok=True)
    overlap_df.to_csv(overlap_output, sep="\t", index=False)
    pair_df.to_csv(pair_output, sep="\t", index=False)

    print(f"Wrote overlap control metrics: {overlap_output}")
    print(f"Wrote pair robustness metrics: {pair_output}")


if __name__ == "__main__":
    main()

# Causal Mediation Circuit Map: Results Summary

## Objective
Build a causal mediation circuit map for scGPT by decomposing TF->target effects into internal head/MLP mediators, using only data in `single_cell_mechinterp/data`.

## Data Sufficiency Check
- Data is sufficient for mediation tracing after preprocessing/mapping from Ensembl IDs to symbols.
- Raw Tabula Sapiens files are Ensembl-indexed; direct tracing against symbol pairs fails until `prepare-data` is run.
- Full immune (`tabula_sapiens_immune.h5ad`, ~18G) is computationally heavy in the current shared CPU context; for completed runs we used `tabula_sapiens_immune_subset_20000.h5ad`.

## What Was Run
1. Case-study mediation runs (5 curated pairs):
- Configs: `subproject_09_causal_mediation_circuit_map/implementation/configs/mediation_{kidney,lung,immune}_{heads,mlp}.yaml`
- Outputs: `subproject_09_causal_mediation_circuit_map/implementation/results/`

2. Discovery runs (no tracing, broad pair sweep):
- Random TRRUST subset (120 pairs per tissue): `discovery_{kidney,lung,immune}.yaml`
- Fixed 40-pair replay for cross-tissue comparability: `discovery_fixed40_{kidney,lung,immune}.yaml`

3. Refined mediation runs on cross-tissue shared pairs:
- Pair file: `subproject_09_causal_mediation_circuit_map/implementation/configs/pairs_cross_tissue_refined.tsv`
- Pairs: `KLF2->CXCR4`, `STAT4->S100A4`
- Configs: `mediation_refined_{kidney,lung,immune}_{heads,mlp}.yaml`
- Outputs: `subproject_09_causal_mediation_circuit_map/implementation/results_refined/`

## Key Findings
### 1. Cross-tissue shared pair coverage is sparse, but non-zero
- From fixed40 replay, only two pairs had evidence in all three tissues:
  - `KLF2->CXCR4` (kidney=12, lung=11, immune=12 cells)
  - `STAT4->S100A4` (kidney=6, lung=2, immune=9 cells)
- `KLF2->CXCR4` is the only robustly supported cross-tissue pair (min_cells=11).

### 2. Mediation is concentrated in small component subsets
Refined run (`results_refined/summary_metrics.tsv`):
- Top-5 mediator mass (heads):
  - kidney `0.6647`, lung `0.6353`, immune `0.6304`
- Top-5 mediator mass (MLP):
  - kidney `0.8689`, lung `0.9237`, immune `0.8244`

Interpretation: MLP mediation is consistently more concentrated than head mediation for this shared-pair setting.

### 3. MLP mediator overlap is stronger across tissues than head overlap
Refined overlap (`results_refined/overlap_metrics.tsv`):
- Mean top-5 Jaccard, heads:
  - kidney-lung `0.3393`, kidney-immune `0.1806`, lung-immune `0.1806`
- Mean top-5 Jaccard, MLP:
  - kidney-lung `0.5476`, kidney-immune `0.3393`, lung-immune `0.7143`

Interpretation: cross-tissue mediator conservation is stronger in MLP blocks than in heads.

### 4. Pair-specific conserved circuit pattern for `KLF2->CXCR4`
Top-5 mediator overlap for `KLF2->CXCR4`:
- Heads Jaccard:
  - kidney-lung `0.4286`
  - kidney-immune `0.2500`
  - lung-immune `0.2500`
- MLP Jaccard:
  - kidney-lung `0.4286`
  - kidney-immune `0.4286`
  - lung-immune `1.0000`

Shared high-contribution MLP layers across tissues include `L0`, `L3`, and `L4`.

## Practical Conclusion
- The mediation-map pipeline is operational and reproducible on available local data.
- We have one solid cross-tissue conserved mediation case (`KLF2->CXCR4`) with:
  - sufficient per-tissue support,
  - clear mediator concentration,
  - stronger MLP than head conservation.
- Cross-tissue pair support is currently the main bottleneck, not missing core data infrastructure.

## Limitations
- Cross-tissue overlap is constrained by sparse shared TF-target evidence under current sampling.
- Immune runs used the 20k subset for tractability in this execution context.
- Several component CIs remain wide, especially for lower-cell pairs (`STAT4->S100A4` in lung).

## Artifact Index
- Main configs: `subproject_09_causal_mediation_circuit_map/implementation/configs/`
- Main outputs: `subproject_09_causal_mediation_circuit_map/implementation/results/`
- Refined outputs: `subproject_09_causal_mediation_circuit_map/implementation/results_refined/`
- Shared-pair ranking: `subproject_09_causal_mediation_circuit_map/implementation/configs/discovery_fixed40_shared_ranked.tsv`
- Summary tables:
  - `subproject_09_causal_mediation_circuit_map/implementation/results/summary_metrics.tsv`
  - `subproject_09_causal_mediation_circuit_map/implementation/results_refined/summary_metrics.tsv`
- Overlap tables:
  - `subproject_09_causal_mediation_circuit_map/implementation/results/overlap_metrics.tsv`
  - `subproject_09_causal_mediation_circuit_map/implementation/results_refined/overlap_metrics.tsv`

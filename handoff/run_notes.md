# Run Notes

## Important execution details
- Raw Tabula files use Ensembl IDs; `prepare-data` is required before causal runs.
- Immune full dataset (`tabula_sapiens_immune.h5ad`) was too slow in this shared CPU context; runs used `tabula_sapiens_immune_subset_20000.h5ad`.

## Main result sets
- Case-study traces:
  - `implementation/results/`
- Discovery sweeps:
  - `implementation/results/{kidney,lung,immune}/discovery/`
  - `implementation/results/{kidney,lung,immune}/discovery_fixed40/`
- Refined shared-pair traces:
  - `implementation/results_refined/`

## Shared-pair artifacts
- Ranked overlap candidate list: `implementation/configs/discovery_fixed40_shared_ranked.tsv`
- Refined pair list used for final tracing: `implementation/configs/pairs_cross_tissue_refined.tsv`

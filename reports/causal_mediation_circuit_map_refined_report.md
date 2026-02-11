# Causal Mediation Circuit Map: Pilot Results

## Scope
- Task source: `market_research/ambitious_paper_questions/idea_02_causal_mediation_circuit_map.md`.
- Data source: preprocessed `.h5ad` files referenced by run configs in this workspace.
- Pair set: 2 unique TF-target pairs observed in ablation outputs.
- Tracing modes: attention heads (top-2 heads per layer) and MLP blocks.

## Aggregate Metrics

| tissue   | granularity   |   pairs_with_scores |   mean_effect |   mean_abs_effect |   top5_mediator_mass |
|:---------|:--------------|--------------------:|--------------:|------------------:|---------------------:|
| kidney   | heads         |                   2 |     0.02058   |         0.0520687 |             0.66473  |
| kidney   | mlp           |                   2 |     0.02058   |         0.0520687 |             0.868907 |
| lung     | heads         |                   2 |    -0.0413661 |         0.0413661 |             0.635346 |
| lung     | mlp           |                   2 |    -0.0413661 |         0.0413661 |             0.923674 |
| immune   | heads         |                   2 |    -0.0530406 |         0.103972  |             0.63041  |
| immune   | mlp           |                   2 |    -0.0530406 |         0.103972  |             0.824357 |

## Cross-Tissue Mediator Overlap

| granularity   | tissue_a   | tissue_b   |   shared_pairs |   mean_jaccard_top5 |
|:--------------|:-----------|:-----------|---------------:|--------------------:|
| heads         | kidney     | lung       |              2 |            0.339286 |
| heads         | kidney     | immune     |              2 |            0.180556 |
| heads         | lung       | immune     |              2 |            0.180556 |
| mlp           | kidney     | lung       |              2 |            0.547619 |
| mlp           | kidney     | immune     |              2 |            0.339286 |
| mlp           | lung       | immune     |              2 |            0.714286 |

## Strongest Components

| tissue   | granularity   | pair          | component   |   restoration_mean |    ci95_low |   ci95_high |   n_cells |
|:---------|:--------------|:--------------|:------------|-------------------:|------------:|------------:|----------:|
| kidney   | heads         | KLF2->CXCR4   | L0:H1       |          -6.13206  | -15.4563    |   3.1922    |        12 |
| kidney   | heads         | KLF2->CXCR4   | L4:H1       |           1.89653  |  -2.27417   |   6.06722   |        12 |
| kidney   | heads         | KLF2->CXCR4   | L1:H1       |           1.46792  |  -0.917844  |   3.85368   |        12 |
| kidney   | heads         | KLF2->CXCR4   | L0:H0       |           1.27492  |  -0.477036  |   3.02687   |        12 |
| kidney   | heads         | KLF2->CXCR4   | L3:H0       |           1.08941  |  -0.963064  |   3.14188   |        12 |
| kidney   | heads         | KLF2->CXCR4   | L4:H0       |           0.950386 |  -0.827594  |   2.72837   |        12 |
| kidney   | heads         | KLF2->CXCR4   | L7:H0       |           0.793182 |  -0.612509  |   2.19887   |        12 |
| kidney   | heads         | KLF2->CXCR4   | L3:H1       |           0.659802 |  -0.643592  |   1.9632    |        12 |
| kidney   | heads         | KLF2->CXCR4   | L6:H1       |          -0.5783   |  -1.78503   |   0.628432  |        12 |
| kidney   | heads         | KLF2->CXCR4   | L1:H0       |           0.56939  |  -1.46572   |   2.6045    |        12 |
| kidney   | mlp           | KLF2->CXCR4   | L4:MLP      |          18.4229   | -14.1864    |  51.0323    |        12 |
| kidney   | mlp           | KLF2->CXCR4   | L0:MLP      |          12.3619   | -14.8576    |  39.5814    |        12 |
| kidney   | mlp           | KLF2->CXCR4   | L3:MLP      |           9.69913  |  -6.55764   |  25.9559    |        12 |
| kidney   | mlp           | KLF2->CXCR4   | L1:MLP      |           3.90252  |  -3.11529   |  10.9203    |        12 |
| kidney   | mlp           | KLF2->CXCR4   | L2:MLP      |           3.73845  |  -4.00272   |  11.4796    |        12 |
| kidney   | mlp           | KLF2->CXCR4   | L7:MLP      |           2.23231  |  -3.29827   |   7.76289   |        12 |
| kidney   | mlp           | KLF2->CXCR4   | L5:MLP      |           1.96346  |  -0.886875  |   4.81379   |        12 |
| kidney   | mlp           | KLF2->CXCR4   | L6:MLP      |           1.95867  |  -1.6944    |   5.61174   |        12 |
| kidney   | mlp           | KLF2->CXCR4   | L9:MLP      |          -0.326361 |  -1.25884   |   0.606117  |        12 |
| kidney   | mlp           | STAT4->S100A4 | L0:MLP      |           0.312518 |  -0.0602834 |   0.68532   |         6 |
| lung     | heads         | STAT4->S100A4 | L0:H0       |           0.289142 |  -0.231995  |   0.810279  |         2 |
| lung     | heads         | STAT4->S100A4 | L1:H0       |           0.237092 |  -0.0680738 |   0.542259  |         2 |
| lung     | heads         | STAT4->S100A4 | L5:H0       |           0.172444 |  -0.119965  |   0.464852  |         2 |
| lung     | heads         | KLF2->CXCR4   | L0:H1       |           0.150248 |   0.0383687 |   0.262127  |        11 |
| lung     | heads         | STAT4->S100A4 | L0:H1       |           0.124961 |  -0.439033  |   0.688955  |         2 |
| lung     | heads         | KLF2->CXCR4   | L7:H0       |          -0.124308 |  -0.21754   |  -0.0310772 |        11 |
| lung     | heads         | KLF2->CXCR4   | L3:H0       |          -0.118896 |  -0.214745  |  -0.0230461 |        11 |
| lung     | heads         | KLF2->CXCR4   | L1:H1       |          -0.108606 |  -0.191618  |  -0.0255932 |        11 |
| lung     | heads         | STAT4->S100A4 | L4:H0       |           0.107321 |  -0.1714    |   0.386042  |         2 |
| lung     | heads         | KLF2->CXCR4   | L4:H0       |          -0.101856 |  -0.180174  |  -0.0235385 |        11 |

## Artifacts
- Run outputs: `subproject_09_causal_mediation_circuit_map/implementation/results/<tissue>/<granularity>/`.
- Summary table: `/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/implementation/results_refined/summary_metrics.tsv`
- Pair table: `/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/implementation/results_refined/pair_metrics.tsv`
- Top components: `/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/implementation/results_refined/top_components.tsv`
- Overlap table: `/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/implementation/results_refined/overlap_metrics.tsv`

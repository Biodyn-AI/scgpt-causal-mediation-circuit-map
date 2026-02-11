# Causal Intervention Case Studies


## STAT4 -> S100A4
- mean effect: 0.0726 ± 0.0523 (n=6)
- label: 1
- top components: L0-H1:0.056, L2-H1:0.027, L5-H0:0.020
```mermaid
graph LR
  n_STAT4_0[STAT4] --> n_S100A4_1[S100A4]
  n_L0_H1_2[L0-H1] --> n_S100A4_1
  n_L2_H1_3[L2-H1] --> n_S100A4_1
  n_L5_H0_4[L5-H0] --> n_S100A4_1
```

## KLF2 -> CXCR4
- mean effect: -0.0315 ± 0.0273 (n=12)
- label: 1
- top components: L0-H1:-6.132, L4-H1:1.897, L1-H1:1.468
```mermaid
graph LR
  n_KLF2_0[KLF2] --> n_CXCR4_1[CXCR4]
  n_L0_H1_2[L0-H1] --> n_CXCR4_1
  n_L4_H1_3[L4-H1] --> n_CXCR4_1
  n_L1_H1_4[L1-H1] --> n_CXCR4_1
```

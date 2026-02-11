# Causal Intervention Case Studies


## STAT4 -> S100A4
- mean effect: 0.0726 ± 0.0523 (n=6)
- label: 1
- top components: L0-MLP:0.313, L5-MLP:0.090, L2-MLP:-0.048
```mermaid
graph LR
  n_STAT4_0[STAT4] --> n_S100A4_1[S100A4]
  n_L0_MLP_2[L0-MLP] --> n_S100A4_1
  n_L5_MLP_3[L5-MLP] --> n_S100A4_1
  n_L2_MLP_4[L2-MLP] --> n_S100A4_1
```

## KLF2 -> CXCR4
- mean effect: -0.0315 ± 0.0273 (n=12)
- label: 1
- top components: L4-MLP:18.423, L0-MLP:12.362, L3-MLP:9.699
```mermaid
graph LR
  n_KLF2_0[KLF2] --> n_CXCR4_1[CXCR4]
  n_L4_MLP_2[L4-MLP] --> n_CXCR4_1
  n_L0_MLP_3[L0-MLP] --> n_CXCR4_1
  n_L3_MLP_4[L3-MLP] --> n_CXCR4_1
```

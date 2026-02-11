# Causal Intervention Case Studies


## KLF2 -> CXCR4
- mean effect: -0.1570 ± 0.1424 (n=12)
- label: 1
- top components: L4-MLP:-0.408, L3-MLP:-0.351, L7-MLP:-0.154
```mermaid
graph LR
  n_KLF2_0[KLF2] --> n_CXCR4_1[CXCR4]
  n_L4_MLP_2[L4-MLP] --> n_CXCR4_1
  n_L3_MLP_3[L3-MLP] --> n_CXCR4_1
  n_L7_MLP_4[L7-MLP] --> n_CXCR4_1
```

## STAT4 -> S100A4
- mean effect: 0.0509 ± 0.1753 (n=9)
- label: 1
- top components: L0-MLP:0.429, L1-MLP:-0.102, L8-MLP:-0.088
```mermaid
graph LR
  n_STAT4_0[STAT4] --> n_S100A4_1[S100A4]
  n_L0_MLP_2[L0-MLP] --> n_S100A4_1
  n_L1_MLP_3[L1-MLP] --> n_S100A4_1
  n_L8_MLP_4[L8-MLP] --> n_S100A4_1
```

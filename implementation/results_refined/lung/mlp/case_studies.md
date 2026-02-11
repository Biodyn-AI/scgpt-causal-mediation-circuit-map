# Causal Intervention Case Studies


## KLF2 -> CXCR4
- mean effect: -0.0818 ± 0.1602 (n=11)
- label: 1
- top components: L0-MLP:-0.860, L3-MLP:-0.671, L4-MLP:-0.522
```mermaid
graph LR
  n_KLF2_0[KLF2] --> n_CXCR4_1[CXCR4]
  n_L0_MLP_2[L0-MLP] --> n_CXCR4_1
  n_L3_MLP_3[L3-MLP] --> n_CXCR4_1
  n_L4_MLP_4[L4-MLP] --> n_CXCR4_1
```

## STAT4 -> S100A4
- mean effect: -0.0009 ± 0.0015 (n=2)
- label: 1
- top components: L0-MLP:-0.789, L3-MLP:-0.702, L4-MLP:0.654
```mermaid
graph LR
  n_STAT4_0[STAT4] --> n_S100A4_1[S100A4]
  n_L0_MLP_2[L0-MLP] --> n_S100A4_1
  n_L3_MLP_3[L3-MLP] --> n_S100A4_1
  n_L4_MLP_4[L4-MLP] --> n_S100A4_1
```

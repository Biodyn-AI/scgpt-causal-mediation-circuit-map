# Causal Intervention Case Studies


## GATA3 -> GATA3
- mean effect: -1.0681 ± 0.7279 (n=5)
- label: 1
- top components: L10-MLP:1.962, L0-MLP:-1.936, L2-MLP:-1.652, L9-MLP:1.441, L5-MLP:1.107, L7-MLP:-1.028, L4-MLP:-0.926, L6-MLP:-0.809
```mermaid
graph LR
  n_GATA3_0[GATA3] --> n_GATA3_1[GATA3]
  n_L10_MLP_2[L10-MLP] --> n_GATA3_1
  n_L0_MLP_3[L0-MLP] --> n_GATA3_1
  n_L2_MLP_4[L2-MLP] --> n_GATA3_1
  n_L9_MLP_5[L9-MLP] --> n_GATA3_1
  n_L5_MLP_6[L5-MLP] --> n_GATA3_1
  n_L7_MLP_7[L7-MLP] --> n_GATA3_1
  n_L4_MLP_8[L4-MLP] --> n_GATA3_1
  n_L6_MLP_9[L6-MLP] --> n_GATA3_1
```

## FOS -> FOS
- mean effect: 0.8637 ± 0.6095 (n=8)
- label: 1
- top components: L10-MLP:0.301, L9-MLP:0.257, L4-MLP:-0.246, L1-MLP:0.199, L5-MLP:0.199, L0-MLP:0.171, L3-MLP:0.100, L11-MLP:0.096
```mermaid
graph LR
  n_FOS_0[FOS] --> n_FOS_1[FOS]
  n_L10_MLP_2[L10-MLP] --> n_FOS_1
  n_L9_MLP_3[L9-MLP] --> n_FOS_1
  n_L4_MLP_4[L4-MLP] --> n_FOS_1
  n_L1_MLP_5[L1-MLP] --> n_FOS_1
  n_L5_MLP_6[L5-MLP] --> n_FOS_1
  n_L0_MLP_7[L0-MLP] --> n_FOS_1
  n_L3_MLP_8[L3-MLP] --> n_FOS_1
  n_L11_MLP_9[L11-MLP] --> n_FOS_1
```

## JUN -> JUN
- mean effect: -0.4194 ± 0.7276 (n=7)
- label: 1
- top components: L0-MLP:0.819, L6-MLP:0.401, L9-MLP:0.364, L10-MLP:0.283, L11-MLP:0.234, L5-MLP:-0.209, L7-MLP:0.189, L3-MLP:0.104
```mermaid
graph LR
  n_JUN_0[JUN] --> n_JUN_1[JUN]
  n_L0_MLP_2[L0-MLP] --> n_JUN_1
  n_L6_MLP_3[L6-MLP] --> n_JUN_1
  n_L9_MLP_4[L9-MLP] --> n_JUN_1
  n_L10_MLP_5[L10-MLP] --> n_JUN_1
  n_L11_MLP_6[L11-MLP] --> n_JUN_1
  n_L5_MLP_7[L5-MLP] --> n_JUN_1
  n_L7_MLP_8[L7-MLP] --> n_JUN_1
  n_L3_MLP_9[L3-MLP] --> n_JUN_1
```

## FOXP3 -> IL2RA
- mean effect: -0.2687 ± 0.0000 (n=1)
- label: 1
- top components: L0-MLP:0.037, L2-MLP:-0.032, L1-MLP:0.031, L3-MLP:-0.020, L4-MLP:0.011, L8-MLP:0.010, L5-MLP:0.007, L9-MLP:0.007
```mermaid
graph LR
  n_FOXP3_0[FOXP3] --> n_IL2RA_1[IL2RA]
  n_L0_MLP_2[L0-MLP] --> n_IL2RA_1
  n_L2_MLP_3[L2-MLP] --> n_IL2RA_1
  n_L1_MLP_4[L1-MLP] --> n_IL2RA_1
  n_L3_MLP_5[L3-MLP] --> n_IL2RA_1
  n_L4_MLP_6[L4-MLP] --> n_IL2RA_1
  n_L8_MLP_7[L8-MLP] --> n_IL2RA_1
  n_L5_MLP_8[L5-MLP] --> n_IL2RA_1
  n_L9_MLP_9[L9-MLP] --> n_IL2RA_1
```

## JUN -> TNF
- mean effect: -0.1734 ± 0.0000 (n=1)
- label: 1
- top components: L3-MLP:0.430, L0-MLP:0.382, L2-MLP:0.246, L4-MLP:-0.222, L5-MLP:0.136, L1-MLP:-0.077, L7-MLP:-0.038, L6-MLP:-0.025
```mermaid
graph LR
  n_JUN_0[JUN] --> n_TNF_1[TNF]
  n_L3_MLP_2[L3-MLP] --> n_TNF_1
  n_L0_MLP_3[L0-MLP] --> n_TNF_1
  n_L2_MLP_4[L2-MLP] --> n_TNF_1
  n_L4_MLP_5[L4-MLP] --> n_TNF_1
  n_L5_MLP_6[L5-MLP] --> n_TNF_1
  n_L1_MLP_7[L1-MLP] --> n_TNF_1
  n_L7_MLP_8[L7-MLP] --> n_TNF_1
  n_L6_MLP_9[L6-MLP] --> n_TNF_1
```

# Causal Intervention Case Studies


## JUN -> JUN
- mean effect: -1.4503 ± 0.5645 (n=8)
- label: 1
- top components: L11-MLP:0.330, L6-MLP:0.310, L0-MLP:0.273, L8-MLP:0.272, L9-MLP:0.254, L7-MLP:0.160, L1-MLP:-0.141, L3-MLP:0.125
```mermaid
graph LR
  n_JUN_0[JUN] --> n_JUN_1[JUN]
  n_L11_MLP_2[L11-MLP] --> n_JUN_1
  n_L6_MLP_3[L6-MLP] --> n_JUN_1
  n_L0_MLP_4[L0-MLP] --> n_JUN_1
  n_L8_MLP_5[L8-MLP] --> n_JUN_1
  n_L9_MLP_6[L9-MLP] --> n_JUN_1
  n_L7_MLP_7[L7-MLP] --> n_JUN_1
  n_L1_MLP_8[L1-MLP] --> n_JUN_1
  n_L3_MLP_9[L3-MLP] --> n_JUN_1
```

## FOS -> FOS
- mean effect: -0.0478 ± 1.3174 (n=8)
- label: 1
- top components: L8-MLP:0.717, L5-MLP:0.353, L6-MLP:0.338, L4-MLP:0.254, L1-MLP:-0.199, L10-MLP:0.124, L11-MLP:0.124, L2-MLP:-0.097
```mermaid
graph LR
  n_FOS_0[FOS] --> n_FOS_1[FOS]
  n_L8_MLP_2[L8-MLP] --> n_FOS_1
  n_L5_MLP_3[L5-MLP] --> n_FOS_1
  n_L6_MLP_4[L6-MLP] --> n_FOS_1
  n_L4_MLP_5[L4-MLP] --> n_FOS_1
  n_L1_MLP_6[L1-MLP] --> n_FOS_1
  n_L10_MLP_7[L10-MLP] --> n_FOS_1
  n_L11_MLP_8[L11-MLP] --> n_FOS_1
  n_L2_MLP_9[L2-MLP] --> n_FOS_1
```

# Causal Intervention Case Studies


## JUN -> JUN
- mean effect: -1.4503 ± 0.5645 (n=8)
- label: 1
- top components: L2-H1:0.123, L4-H1:0.116, L7-H0:0.081, L4-H0:-0.063, L6-H0:0.058, L8-H0:0.055, L0-H0:0.050, L1-H0:-0.045
```mermaid
graph LR
  n_JUN_0[JUN] --> n_JUN_1[JUN]
  n_L2_H1_2[L2-H1] --> n_JUN_1
  n_L4_H1_3[L4-H1] --> n_JUN_1
  n_L7_H0_4[L7-H0] --> n_JUN_1
  n_L4_H0_5[L4-H0] --> n_JUN_1
  n_L6_H0_6[L6-H0] --> n_JUN_1
  n_L8_H0_7[L8-H0] --> n_JUN_1
  n_L0_H0_8[L0-H0] --> n_JUN_1
  n_L1_H0_9[L1-H0] --> n_JUN_1
```

## FOS -> FOS
- mean effect: -0.0478 ± 1.3174 (n=8)
- label: 1
- top components: L6-H0:0.138, L0-H1:-0.087, L6-H1:-0.071, L5-H0:0.070, L1-H1:0.063, L3-H0:0.054, L2-H0:-0.051, L7-H1:-0.043
```mermaid
graph LR
  n_FOS_0[FOS] --> n_FOS_1[FOS]
  n_L6_H0_2[L6-H0] --> n_FOS_1
  n_L0_H1_3[L0-H1] --> n_FOS_1
  n_L6_H1_4[L6-H1] --> n_FOS_1
  n_L5_H0_5[L5-H0] --> n_FOS_1
  n_L1_H1_6[L1-H1] --> n_FOS_1
  n_L3_H0_7[L3-H0] --> n_FOS_1
  n_L2_H0_8[L2-H0] --> n_FOS_1
  n_L7_H1_9[L7-H1] --> n_FOS_1
```

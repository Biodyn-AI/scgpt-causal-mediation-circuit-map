# Iterator Pass: Final Adversarial Review and Strengthening

Date: 2026-02-11
Project: Causal Mediation Circuit Map
Scope: Execution of `prompts/iterator.md`

## A) Reviewer-Mode Critique

### Summary (reviewer tone)
This paper proposes a mediation-style intervention and patching workflow to localize internal scGPT components that mediate TF-to-target effects across tissues. The authors introduce a discovery-to-refinement protocol intended to separate cross-tissue support coverage from mechanistic tracing. Results emphasize one robust pair (`KLF2->CXCR4`) and show higher concentration and overlap for MLP mediators than for attention heads. The manuscript has a clear mechanistic goal and improved uncertainty reporting, but its evidential scope is still narrow and potentially vulnerable to over-interpretation. Acceptance depends on whether the paper convincingly frames itself as a focused methodological case study rather than a broad conservation claim.

### Strengths
- Clear mechanistic question tied to intervention-based estimates rather than purely correlational summaries.
- Discovery-coverage analysis explicitly reveals where cross-tissue support is absent.
- Claims are now scoped around evidence availability rather than broad generalization.
- Component-level uncertainty is reported instead of hidden.
- Reproducibility policy is clean and externally anchored via a public repository URL.

### Weaknesses (prioritized)
1. **Very small robust shared-pair set**: one strong exemplar limits generality.
2. **Potential overlap inflation by finite component space**: raw Jaccard overlaps can look meaningful without a random-null benchmark.
3. **Top-k dependence risk**: conclusions may be sensitive to the chosen mediator cutoff (`k=5`).
4. **Heterogeneous pair quality**: weak pair (`STAT4->S100A4`) has low support and sign instability, but still influences aggregate overlap metrics.
5. **No donor/batch-stratified mechanistic stability test** in current outputs.
6. **No external perturbation-grounded validation** of identified mediator components.
7. **Limited explicit anti-cherry-picking defense** before this pass.
8. **Biological interpretation is plausible but still hypothesis-level** rather than strongly validated.
9. **Potential residual confounding from tissue composition and preprocessing choices.**
10. **Mechanistic interaction terms (multi-mediator effects) not explicitly identified.**

### Questions for authors
Methodology / reproducibility (>=3):
1. Are all preprocessing and pair-selection decisions deterministic and versioned in the external repository?
2. How are ties in top-k mediator selection handled, and can this alter overlap statistics?
3. Is there a single command path to reproduce Tables `tab:coverage`, `tab:overlap_controls`, and `tab:pair_robustness` from raw refined outputs?

Statistics / controls / confounds (>=3):
4. What is the null expectation for top-k Jaccard given component-space size, and how far above null are reported values?
5. Do overlap conclusions persist for multiple k values (e.g., 3, 8, 10) or only at k=5?
6. How much of aggregate overlap is driven by the robust pair vs the weak pair?
7. Are effect direction and overlap internally consistent across tissues for each pair?

Interpretability validity (>=2):
8. What negative controls demonstrate the overlap signal is not an artifact of finite component cardinality?
9. Are mediator findings robust to alternative ranking cutoffs and not cherry-picked from one threshold?
10. Do these analyses support a causal-mechanism claim or only a constrained intervention-localization claim?

Biological interpretation / plausibility (>=2):
11. What biological hypothesis is specifically generated for `KLF2->CXCR4` and what would falsify it?
12. Why should these mediator findings matter beyond this dataset/model slice?

### Likely score band (pre-fix)
**Borderline / weak reject**.

Reason: the mechanistic pipeline is solid, but lack of explicit null controls and top-k sensitivity left core overlap claims open to straightforward reviewer rejection.

### Reject rationale in one sentence
"The paper’s conservation claims are based on small-sample overlaps without adequate null/sensitivity controls, so apparent mechanism reuse may be an artifact."

## B) Prioritized Improvement Backlog

| Priority | Title | Why it matters | Concrete action(s) | Evidence needed | Effort | Stop condition |
|---|---|---|---|---|---|---|
| P0 | Add overlap random-null control | Removes major reviewer attack on finite-space overlap artifacts | Compute expected random Jaccard and permutation p-values for top-5 overlaps | New table in Results | Small | Table shows observed > null with p-values |
| P0 | Add top-k sensitivity analysis | Prevents arbitrary-threshold criticism | Compute overlap for k={3,5,8,10} for heads/MLP | New table in Results | Small | Trend persists across k |
| P0 | Add anti-cherry-picking pair-heterogeneity check | Distinguishes robust vs weak pair and scopes claims | Add per-pair overlap and sign-consistency diagnostics | New table + text | Small | Strong pair clearly separated from weak pair |
| P1 | Integrate controls in Methods and Discussion | Ensures controls are part of protocol, not post hoc patch | Add methods subsection and revised limitation text | Manuscript sections updated | Small | Methods and Discussion explicitly reference controls |
| P1 | Tighten abstract claim language | Prevents overclaiming in high-visibility section | Add null-control result and bounded wording | Abstract revised | Small | Abstract states constrained mechanistic claim |
| P1 | Clean table formatting warnings | Reduces presentation friction | Adjust column labels/font sizes | No overfull-table warnings | Small | PDF compiles cleanly for new tables |
| P2 | Improve reproducibility artifact coverage | Reviewer trust in operational clarity | Export new control metrics to TSV + script | New script + outputs + README entry | Medium | Controls reproducible from command line |
| P3 | Donor/batch stability | Stronger robustness evidence | Requires new stratified runs unavailable in current artifacts | Future experiment | Large | Additional stratified results |
| P3 | External perturbation validation of mediators | Strong biological causal grounding | Requires external perturbation-linked mediator tests | Future experiment | Large | Perturbation-backed mediator confirmation |

## C) Revised Full Paper (Submission-Quality)

Revised manuscript source:
- `/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/reports/causal_mediation_circuit_map_paper.tex`

Revised compiled PDF:
- `/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/reports/causal_mediation_circuit_map_paper.pdf`

New reproducibility artifacts used in the revised paper:
- `/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/implementation/results_refined/overlap_control_metrics.tsv`
- `/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/implementation/results_refined/pair_robustness_metrics.tsv`

New analysis script:
- `/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/implementation/scripts/analyze_overlap_controls.py`

## D) Short Changelog (Backlog-Mapped)

1. **P0 null control (Done)**
- Added `tab:overlap_controls` with observed vs random expected Jaccard and permutation p-values.
- Why: neutralizes finite-component-space overlap artifact critique.

2. **P0 top-k sensitivity (Done)**
- Added overlap results for k=3,5,8,10 in the same control table.
- Why: removes dependence on a single arbitrary top-k threshold.

3. **P0 anti-cherry-picking (Done)**
- Added `tab:pair_robustness` with per-pair sign consistency, min support, and per-pair overlap summaries.
- Why: explicitly separates robust pair (`KLF2->CXCR4`) from weak pair (`STAT4->S100A4`).

4. **P1 methods integration (Done)**
- Expanded Methods (`Uncertainty and control logic`) to include null-control and sensitivity protocol.
- Why: makes controls first-class methodology, not post hoc.

5. **P1 claim-scoping (Done)**
- Updated Abstract and Discussion to report null-control findings and bounded interpretation.
- Why: reduce reviewer attack surface for overclaiming.

6. **P1 presentation cleanup (Done)**
- Reformatted new tables to remove overfull-table issues in compilation.
- Why: improve submission polish.

7. **P2 reproducibility artifacts (Done)**
- Added and documented `analyze_overlap_controls.py` and TSV outputs.
- Why: reproducible evidence generation for new controls.

## E) Updated Claims Table (Post-Fix)

| Main claim | Evidence location(s) | Vulnerability | Patch applied |
|---|---|---|---|
| Cross-tissue support is the main bottleneck | `tab:coverage` | Low | None needed beyond explicit interpretation |
| One robust shared pair exists at stricter support thresholds | `tab:coverage`, `tab:pair_effects` | Low | Reinforced with pair robustness table |
| MLP mediation is more concentrated than heads | `fig:mass`, `tab:summary` | Low | None needed |
| MLP overlap exceeds head overlap in refined setting | `fig:overlap`, `tab:overlap`, `tab:overlap_controls` | Medium -> Low/Medium | Added random-null + top-k sensitivity controls |
| Overlap signal is not explained by random finite-space overlap | `tab:overlap_controls` | High -> Medium | Added expected-random and permutation p-value controls |
| Claims are not cherry-picked around one pair | `tab:pair_robustness`, `tab:pair_effects` | High -> Medium | Added per-pair heterogeneity and sign-consistency diagnostics |
| Conserved feed-forward subcircuit hypothesis for `KLF2->CXCR4` is plausible | Results + Biological Interpretation + `tab:pair_robustness` | Medium | Kept explicitly hypothesis-level and bounded |

## F) Remaining Cannot-Fix-Here Items

1. **Donor/batch-stratified mechanistic stability**
- Requirement: stratified reruns with donor/batch metadata slices and sufficient per-slice support.

2. **External perturbation-grounded validation of mediator components**
- Requirement: perturbation datasets linked to the same TF-target contexts with mediator-targeted intervention readouts.

3. **Multi-mediator interaction identification (beyond single-component patching)**
- Requirement: combinatorial or interaction-aware patching experiments with tractable component selection and uncertainty estimation.

Status after this iterator pass:
- All high-priority and medium-priority items feasible with current artifacts were addressed.
- Remaining items require new experimental data/runs and are now explicitly framed as future work rather than implied support.

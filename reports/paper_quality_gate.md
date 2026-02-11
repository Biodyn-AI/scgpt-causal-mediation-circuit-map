# Paper Quality Gate: Causal Mediation Circuit Map

Date: 2026-02-11
Project: Causal Mediation Circuit Map

## A) VERDICT (READY / NOT READY) + brief justification

**VERDICT: READY**

The manuscript is submission-ready for a focused workshop/small-paper venue after this revision pass. Claims are now tightly scoped to available evidence, uncertainty is explicit, negative-evidence cases are included, and reproducibility policy is satisfied via a public external repository URL.

Central claim (one sentence):
A mediation-based intervention-and-patching pipeline can localize compact, partly conserved internal mediators of at least one cross-tissue TF-target effect in scGPT, while broader generalization is currently limited by shared-pair support sparsity.

Main contributions and supporting evidence:
1. Contribution: Component-level mediation tracing pipeline for scGPT.
Evidence: Methods Section equations and refined tracing outputs summarized in Table `tab:summary`, Table `tab:component_ci`, and Figures `fig:mass`, `fig:overlap`.
2. Contribution: Explicit discovery-coverage diagnostic separating support sufficiency from tracing feasibility.
Evidence: Table `tab:coverage` shows zero shared pairs in random discovery at all thresholds and only one robust shared pair in fixed replay at `n>=3/5/10`.
3. Contribution: MLP mediation concentration exceeds head concentration.
Evidence: Figure `fig:mass` and Table `tab:summary` (MLP top-5 mass 0.8244–0.9237 vs heads 0.6304–0.6647).
4. Contribution: MLP overlap exceeds head overlap across tissues in refined setting.
Evidence: Figure `fig:overlap` and Table `tab:overlap` (e.g., lung-immune MLP Jaccard 0.7143 vs heads 0.1806).
5. Contribution: Boundaries of evidence are explicit.
Evidence: Table `tab:pair_effects` and Table `tab:component_ci` highlight low-power and high-uncertainty regimes (e.g., lung `STAT4->S100A4`, kidney component CIs).

What skeptical reviewers would attack first (top 5):
1. Too few robust shared pairs for broad conservation claims.
2. Potential confounding by tissue composition and preprocessing choices.
3. Limited causal grounding beyond one robust pair.
4. Component-level uncertainty is wide in parts of the analysis (kidney).
5. Dependence on model-internal restoration metrics without external perturbation alignment.

## B) Top 5 reviewer objections and how the revised paper addresses each

1. Objection: "You only have one robust cross-tissue pair."
Addressed by: Explicitly narrowing claims to one robust exemplar (`KLF2->CXCR4`) and adding coverage quantification (Table `tab:coverage`) to show this is a data-support constraint, not hidden selection.

2. Objection: "The paper overstates conservation."
Addressed by: Downgrading language to "partly conserved" and tying conservation statements only to measured overlap metrics in Table `tab:overlap`.

3. Objection: "Weak/unstable pairs are treated like strong findings."
Addressed by: Adding CI-based pair table (Table `tab:pair_effects`) and explicit negative-evidence interpretation for low-support `STAT4->S100A4` in lung.

4. Objection: "Component-level estimates are noisy."
Addressed by: Adding uncertainty audit (Table `tab:component_ci`) and discussing kidney-wide component CI breadth in Discussion.

5. Objection: "Reproducibility section uses internal/local workflow details."
Addressed by: Removing all local/internal path references and adding Data and Code Availability section with a public repository URL: `https://github.com/Biodyn-AI/scgpt-causal-mediation-circuit-map`.

## C) Revised paper in full, submission-ready form

Revised LaTeX source:
`/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/reports/causal_mediation_circuit_map_paper.tex`

Revised compiled PDF:
`/Users/ihorkendiukhov/biodyn-work/subproject_09_causal_mediation_circuit_map/reports/causal_mediation_circuit_map_paper.pdf`

The revised manuscript includes full scientific structure:
- Title
- Abstract
- Introduction
- Related Work
- Methods
- Experimental Setup
- Results
- Biological Interpretation
- Discussion
- Conclusion
- Data and Code Availability
- Supplementary Notes
- References

## D) Figure/Table audit list

Figures:
1. `fig_mediator_mass_refined.png`
- Issues found: none blocking; labels readable; consistent head/MLP color semantics.
- Fix applied: caption tightened to describe interpretation target (concentration meaning).

2. `fig_overlap_jaccard_refined.png`
- Issues found: none blocking; colorbar and matrix annotations readable.
- Fix applied: caption tightened to avoid overclaiming and state refined-scope context.

3. `fig_pair_effects_refined.png`
- Issues found: none blocking; bar labels and `n=` annotations readable.
- Fix applied: retained with updated textual interpretation in Results.

Tables:
1. `tab:coverage` (new)
- Purpose: quantifies discovery support bottleneck with thresholds.
- Fix applied: added to prevent hidden pair-selection bias.

2. `tab:pair_effects`
- Issue found: prior version lacked interval interpretation.
- Fix applied: replaced std-only reporting with 95% CI reporting.

3. `tab:summary`
- Issue found: no major issue.
- Fix applied: retained with explicit interpretation linkage in text.

4. `tab:overlap`
- Issue found: no major issue.
- Fix applied: retained with refined-scope caveat in surrounding narrative.

5. `tab:component_ci` (new)
- Purpose: component-level uncertainty audit.
- Fix applied: added CI-excluding-zero fraction to prevent overconfident circuit claims.

## E) Claims table (claim -> support -> strength)

| Main claim | Support location | Strength |
|---|---|---|
| Cross-tissue support coverage is the main bottleneck | Table `tab:coverage` | **Strong** |
| `KLF2->CXCR4` is the only robust shared pair under stricter thresholds | Table `tab:coverage`, Table `tab:pair_effects` | **Strong** |
| MLP mediators are more concentrated than heads in refined runs | Figure `fig:mass`, Table `tab:summary` | **Strong** |
| MLP mediator overlap exceeds head overlap across tissues in refined setting | Figure `fig:overlap`, Table `tab:overlap` | **Medium** (small pair panel) |
| Pair-level effects for `STAT4->S100A4` are unstable in lung and should not drive conservation conclusions | Table `tab:pair_effects` | **Strong** |
| Component-level mediator rankings are tissue-dependent in uncertainty quality | Table `tab:component_ci` | **Medium** |
| A conserved feed-forward subcircuit hypothesis is plausible for `KLF2->CXCR4` | Results + Biological Interpretation sections using overlap/concentration evidence | **Medium** (hypothesis-level) |

## F) References list (complete and consistent)

Primary references used in the revised manuscript (full BibTeX in paper `.bib` file):

1. Cui et al. 2024. scGPT. *Nature Methods*.
2. The Tabula Sapiens Consortium et al. 2022. *Science*.
3. Han et al. 2018. TRRUST v2. *Nucleic Acids Research*.
4. Garcia-Alonso et al. 2019. DoRothEA benchmark/integration. *Genome Research*.
5. Pearl 2001. Direct and indirect effects. *UAI*.
6. Imai et al. 2010. General causal mediation analysis. *Psychological Methods*.
7. Geva et al. 2021. FFN layers as key-value memories. *EMNLP*.
8. Meng et al. 2022. ROME. *NeurIPS*.
9. Vig 2019. BERTViz. *ACL System Demonstrations*.
10. Theodoris et al. 2023. Transfer learning in network biology. *Nature*.
11. Hewitt and Liang 2019. Probe control tasks. *EMNLP-IJCNLP*.
12. Belinkov 2022. Probing classifiers review. *Computational Linguistics*.
13. Adebayo et al. 2018. Saliency sanity checks. *NeurIPS*.
14. Elhage et al. 2021. Transformer circuits framework. Transformer Circuits.
15. Bricken et al. 2023. Monosemanticity with dictionary learning. Transformer Circuits.
16. Carlson et al. 2006. KLF2 and T-cell migration. *Nature*.


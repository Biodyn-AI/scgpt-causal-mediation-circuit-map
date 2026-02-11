# Implementation

This folder stores mediation configs, run outputs, and analysis scripts for Idea 02.

Entry points:
- Run tracing jobs: `subproject_09_causal_mediation_circuit_map/implementation/scripts/run_mediation_jobs.sh`
- Aggregate results: `subproject_09_causal_mediation_circuit_map/implementation/scripts/analyze_mediation_results.py`
- Summarize discovery support coverage: `python subproject_09_causal_mediation_circuit_map/implementation/scripts/analyze_discovery_coverage.py`
- Analyze overlap controls and pair robustness: `python subproject_09_causal_mediation_circuit_map/implementation/scripts/analyze_overlap_controls.py`
- Generate paper figures: `subproject_09_causal_mediation_circuit_map/implementation/scripts/generate_paper_figures.py`

Key output roots:
- Initial case-study traces: `subproject_09_causal_mediation_circuit_map/implementation/results/`
- Refined shared-pair traces: `subproject_09_causal_mediation_circuit_map/implementation/results_refined/`


## Agent Completion Tracking
- Do this for your project: `tracking/prompt.md`.
- When you finish meaningful work, update `tracking/prompt.md` with the project status (progress, decisions, blockers, and next step).
- Skip the update only if nothing meaningful changed.

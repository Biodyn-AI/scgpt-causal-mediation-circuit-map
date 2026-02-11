#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SC_ROOT="$REPO_ROOT/single_cell_mechinterp"

cd "$SC_ROOT"
for tissue in kidney lung immune; do
  prep_cfg="../subproject_09_causal_mediation_circuit_map/implementation/configs/mediation_${tissue}_heads.yaml"
  echo "[mediation-prep] tissue=${tissue} cfg=${prep_cfg}"
  PYTHONPATH=. python -m src.cli --config "$prep_cfg" prepare-data

  for gran in heads mlp; do
    cfg="../subproject_09_causal_mediation_circuit_map/implementation/configs/mediation_${tissue}_${gran}.yaml"
    echo "[mediation-run] tissue=${tissue} granularity=${gran} cfg=${cfg}"
    PYTHONPATH=. python scripts/run_causal_interventions.py --config "$cfg" --device cpu
  done
done

echo "[mediation-run] all jobs completed"

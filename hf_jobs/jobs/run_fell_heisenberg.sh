#!/usr/bin/env bash
# HF Jobs entry script for the Fell-Heisenberg WEC-residual sweep (Task 2D.4).
#
# Usage (inside an HF Jobs container, image python:3.12):
#   bash hf_jobs/jobs/run_fell_heisenberg.sh <config_name> <upload_subdir> [points_path]
#
# If points_path is provided, the sweep runs in --points mode (point list bypasses
# build_grid). The config still provides per-point fixed scalars (Npts, L, Pi, ...).
#
# Example dispatch from a local shell with HF_TOKEN in env:
#   hf jobs run --flavor cpu-upgrade --secrets HF_TOKEN --timeout 2h \
#     python:3.12 \
#     bash -c "git clone --depth 1 https://github.com/bshepp/alcubierre /work && cd /work && bash hf_jobs/jobs/run_fell_heisenberg.sh preview preview-$(date -u +%Y%m%dT%H%M%S)"
#
# Example with --points:
#   bash hf_jobs/jobs/run_fell_heisenberg.sh pointlist_n129 conv-test-$(date ...) hf_jobs/configs/pointlist_5d.csv

set -euo pipefail

CONFIG_NAME="${1:-preview}"
UPLOAD_SUBDIR="${2:-${CONFIG_NAME}-$(date -u +%Y%m%dT%H%M%S)}"
POINTS_PATH="${3:-}"
SLICE_START="${4:-}"
SLICE_STOP="${5:-}"
CONFIG_PATH="hf_jobs/configs/fell_heisenberg_${CONFIG_NAME}.json"
RESULTS_REPO="bshepp/alcubierre-sweeps"

SLICE_ARGS=()
if [[ -n "${SLICE_START}" ]]; then
  SLICE_ARGS+=(--start "${SLICE_START}")
fi
if [[ -n "${SLICE_STOP}" ]]; then
  SLICE_ARGS+=(--stop "${SLICE_STOP}")
fi

if [[ ! -f "${CONFIG_PATH}" ]]; then
  echo "ERROR: config not found at ${CONFIG_PATH}" >&2
  exit 2
fi
if [[ -n "${POINTS_PATH}" && ! -f "${POINTS_PATH}" ]]; then
  echo "ERROR: points file not found at ${POINTS_PATH}" >&2
  exit 2
fi

echo "=== Environment ==="
python --version
pip --version
echo "Working dir: $(pwd)"
echo "Config: ${CONFIG_PATH}"
[[ -n "${POINTS_PATH}" ]] && echo "Points: ${POINTS_PATH}"
echo "Upload subdir: ${UPLOAD_SUBDIR}"
echo

echo "=== Installing requirements ==="
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q hf-transfer
echo

echo "=== Running sweep ==="
if [[ -n "${POINTS_PATH}" ]]; then
  HF_JOB=1 python -m hf_jobs.run_sweep fell_heisenberg --config "${CONFIG_PATH}" --points "${POINTS_PATH}" "${SLICE_ARGS[@]}"
else
  HF_JOB=1 python -m hf_jobs.run_sweep fell_heisenberg --config "${CONFIG_PATH}" "${SLICE_ARGS[@]}"
fi
echo

echo "=== Sweep output ==="
ls -la sweeps/
echo

echo "=== Uploading results to ${RESULTS_REPO}/${UPLOAD_SUBDIR}/ ==="
HF_HUB_ENABLE_HF_TRANSFER=1 hf upload "${RESULTS_REPO}" sweeps/ "${UPLOAD_SUBDIR}/" \
  --repo-type dataset \
  --commit-message "Task 2D.4 ${CONFIG_NAME} sweep results"
echo

echo "=== Done ==="

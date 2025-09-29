# scripts/make_dataset.sh
#!/usr/bin/env bash
set -euo pipefail

#block MAKE-PQCLEAN-TGT-001
# Simple dataset builder wrapper. Call as:
#   scripts/make_dataset.sh pqclean
#
# ENV overrides:
#   VENV_ACTIVATE=".venv/bin/activate"
#   PQCLEAN_ROOT="data/raw/pqclean"
#   OUT_PATH="data/interim/staging/pqclean_records.jsonl"
#   CANONICAL_MAP="src/validate/canonical_names.yaml"
#   PYTHON="python"
#
# This script does not create or fetch PQClean sources; drop them under $PQCLEAN_ROOT.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

VENV_ACTIVATE="${VENV_ACTIVATE:-.venv/bin/activate}"
PQCLEAN_ROOT="${PQCLEAN_ROOT:-data/raw/pqclean}"
OUT_PATH="${OUT_PATH:-data/interim/staging/pqclean_records.jsonl}"
CANONICAL_MAP="${CANONICAL_MAP:-src/validate/canonical_names.yaml}"
PYTHON="${PYTHON:-python}"

activate_venv() {
  if [[ -f "$REPO_ROOT/$VENV_ACTIVATE" ]]; then
    # shellcheck source=/dev/null
    source "$REPO_ROOT/$VENV_ACTIVATE"
  else
    echo "[WARN] venv not found at $VENV_ACTIVATE. Continuing with current interpreter." >&2
  fi
}

usage() {
  cat <<USAGE
make_dataset.sh — dataset build wrapper

USAGE:
  $0 pqclean          Parse PQClean api.h trees to JSONL

ENV:
  VENV_ACTIVATE=$VENV_ACTIVATE
  PQCLEAN_ROOT=$PQCLEAN_ROOT
  OUT_PATH=$OUT_PATH
  CANONICAL_MAP=$CANONICAL_MAP
  PYTHON=$PYTHON
USAGE
}

run_pqclean() {
  activate_venv
  mkdir -p "$REPO_ROOT/$(dirname "$OUT_PATH")"
  CMD=( "$PYTHON" "$REPO_ROOT/src/ingest/pqclean_ingest.py"
        --pqclean_root "$REPO_ROOT/$PQCLEAN_ROOT"
        --out          "$REPO_ROOT/$OUT_PATH" )
  # Only append --canonical if the file exists (ingest can run without it)
  if [[ -f "$REPO_ROOT/$CANONICAL_MAP" ]]; then
    CMD+=( --canonical "$REPO_ROOT/$CANONICAL_MAP" )
  fi
  echo "[INFO] ${CMD[*]}"
  "${CMD[@]}"
}

main() {
  local target="${1:-}"
  case "$target" in
    pqclean) run_pqclean ;;
    ""|-h|--help|help) usage ;;
    *) echo "[ERROR] Unknown target: $target" >&2; usage; exit 2 ;;
  esac
}

main "$@"
#/end of block MAKE-PQCLEAN-TGT-001

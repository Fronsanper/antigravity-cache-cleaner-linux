#!/bin/bash
set -euo pipefail
BASE_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required."; exit 1; }
exec python3 "$BASE_DIR/wizard.py" "$@"

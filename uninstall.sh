#!/bin/bash
set -euo pipefail
BASE_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$BASE_DIR/wizard.py" --uninstall

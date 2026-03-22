#!/usr/bin/env bash
# ------------------------------------------------------------------
# Local test harness for call-for-testing template rendering.
#
# Sets representative environment variables and renders template.md
# exactly the way the GitHub Actions step does, printing the
# rendered title and body to stdout so you can verify correctness.
#
# Usage:
#   cd call-for-testing
#   bash test-template-render.sh
# ------------------------------------------------------------------
set -euo pipefail

# ── Representative environment variables ──────────────────────────
export snap_name="signal-desktop"
export channel="latest/candidate"
export version="7.30.0"
export revisions="152,153,154"
export table='<table><thead><tr><th>CPU Architecture</th><th>Revision</th></tr></thead><tbody><tr><td>amd64</td><td>152</td></tr><tr><td>arm64</td><td>153</td></tr><tr><td>armhf</td><td>154</td></tr></tbody></table>'
export promotion_channel="latest/stable"

# ── Rendering helpers (same logic used in action.yaml) ────────────

# Render {{ env.VAR }} → actual value from environment
render() {
  sed 's/{{ *env\.\([a-zA-Z_][a-zA-Z0-9_]*\) *}}/${\1}/g' <<< "$1" | envsubst
}

TEMPLATE="template.md"
if [[ ! -f "$TEMPLATE" ]]; then
  echo "ERROR: $TEMPLATE not found. Run this script from the call-for-testing/ directory." >&2
  exit 1
fi

# ── Extract front-matter fields ──────────────────────────────────
title=$(yq --front-matter=extract '.title' "$TEMPLATE")
labels=$(yq --front-matter=extract '.labels' "$TEMPLATE")

# ── Extract body (everything after closing ---) ──────────────────
body=$(sed '1{/^---$/!q;};1,/^---$/d' "$TEMPLATE")

# ── Render ────────────────────────────────────────────────────────
rendered_title=$(render "$title")
rendered_body=$(render "$body")

# ── Output ────────────────────────────────────────────────────────
echo "============================================"
echo "TITLE:  $rendered_title"
echo "LABELS: $labels"
echo "============================================"
echo ""
echo "$rendered_body"

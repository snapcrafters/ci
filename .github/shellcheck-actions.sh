#!/usr/bin/env bash
set -euo pipefail
info() { echo -e "\e[92m[+] $@\e[0m"; }
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

export SHELLCHECK_OPTS=(
    "-s" "bash"
    "-e" "2296"
    "-e" "2157"
    "-e" "2129"
    "-e" "2154"
)

for f in "$DIR"/../**/*.yaml; do
    info "Linting scripts in $f"
    yq '.runs.steps[].run' "$f" | grep -v -P "^null$" | shellcheck "${SHELLCHECK_OPTS[@]}" -
done

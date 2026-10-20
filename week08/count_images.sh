#!/usr/bin/env bash
set -euo pipefail
root=${1:-.}
# NUL separation preserves directory names containing spaces or newlines.
while IFS= read -r -d '' directory; do
    printf '%s: ' "$directory"
    find "$directory" -type f -iname '*.jpg' -print0 | tr -cd '\000' | wc -c
done < <(find "$root" -type d -print0)

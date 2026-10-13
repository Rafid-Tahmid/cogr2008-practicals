#!/usr/bin/env bash
set -euo pipefail
script_dir=$(cd "$(dirname "$0")" && pwd)
# Match this practical's workers owned by this user, rather than unrelated shells.
pgrep -u "$(id -u)" -f '[p]rac07[.]sh' | while IFS= read -r pid; do
    command=$(ps -p "$pid" -o command= 2>/dev/null) || continue
    case "$command" in
        *"$script_dir/prac07.sh"*)
            printf 'Terminating PID %s: %s\n' "$pid" "$command"
            kill -TERM "$pid" 2>/dev/null || true
            ;;
    esac
done || true

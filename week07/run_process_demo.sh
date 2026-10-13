#!/usr/bin/env bash
set -euo pipefail
script_dir=$(cd "$(dirname "$0")" && pwd)
pids=()
cleanup() {
    for pid in "${pids[@]}"; do kill -TERM "$pid" 2>/dev/null || true; done
    for pid in "${pids[@]}"; do wait "$pid" 2>/dev/null || true; done
}
trap cleanup EXIT
date -u '+%Y-%m-%dT%H:%M:%SZ'
uname -srm
for i in $(seq 1 5); do
    bash "$script_dir/prac07.sh" &
    pids+=("$!")
done
nice -n 10 bash "$script_dir/prac07.sh" &
pids+=("$!")
sleep 1
ps -p "$(IFS=,; echo "${pids[*]}")" -o pid,ppid,ni,%cpu,command
renice -n 10 -p "${pids[0]}"
renice -n 15 -p "${pids[1]}"
sleep 1
ps -p "$(IFS=,; echo "${pids[*]}")" -o pid,ppid,ni,%cpu,command
kill -KILL "${pids[2]}"
wait "${pids[2]}" 2>/dev/null || true
bash "$script_dir/kill_workers.sh"
cleanup
trap - EXIT
for pid in "${pids[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
        printf 'Worker %s is still running\n' "$pid" >&2
        exit 1
    fi
done
printf 'All six workers have exited.\n'

#!/usr/bin/env bash
set -euo pipefail
work=$(mktemp -d "${TMPDIR:-/tmp}/cogr-tmux.XXXXXX")
socket="$work/tmux.sock"
cleanup() {
    tmux -S "$socket" kill-server 2>/dev/null || true
    rm -rf "$work"
}
trap cleanup EXIT
# Use an isolated server so existing personal sessions are not changed.
tmux -S "$socket" new-session -d -s prac08 -n counter \
    'for i in 1 2 3 4 5 6 7 8 9 10; do echo "$i"; sleep 1; done; sleep 10'
tmux -S "$socket" new-window -t prac08 -n other 'sleep 20'
tmux -S "$socket" select-window -t prac08:other
sleep 2
printf 'Counter while another window is selected:\n'
tmux -S "$socket" capture-pane -p -t prac08:counter
sleep 2
printf 'Counter two seconds later, with no attached client:\n'
tmux -S "$socket" capture-pane -p -t prac08:counter
tmux -S "$socket" list-windows -t prac08

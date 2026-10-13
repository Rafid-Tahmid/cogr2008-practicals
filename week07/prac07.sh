#!/usr/bin/env bash
set -eu
for i in $(seq 1 "${1:-100000}")
do
    expr 1 + 1 > /dev/null
done

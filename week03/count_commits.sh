#!/usr/bin/env bash
set -euo pipefail
repository=${1:?Usage: count_commits.sh /path/to/GNU-Make-repository}
git -C "$repository" rev-parse HEAD
git -C "$repository" log -1 --format='%aI %s'
git -C "$repository" rev-parse --is-shallow-repository
git -C "$repository" log --format='%an' | grep -x 'Paul Smith' | wc -l

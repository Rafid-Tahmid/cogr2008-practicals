#!/usr/bin/env bash
set -euo pipefail

# Supply the course science.txt as argument 1; otherwise use the labelled sample.
script_dir=$(cd "$(dirname "$0")" && pwd)
input=${1:-"$script_dir/practice_sample.txt"}
input=$(cd "$(dirname "$input")" && pwd)/$(basename "$input")
work=$(mktemp -d "${TMPDIR:-/tmp}/cogr-unix.XXXXXX")
job_pid=''
cleanup() {
    if [[ -n "$job_pid" ]]; then
        kill -CONT "$job_pid" 2>/dev/null || true
        kill -TERM "$job_pid" 2>/dev/null || true
        wait "$job_pid" 2>/dev/null || true
    fi
    rm -rf "$work"
}
trap cleanup EXIT
set -x

uname -srm
mkdir -p "$work/unixstuff/backups"
cd "$work/unixstuff"
pwd
ls -a
cd .
cd ..
pwd
cd unixstuff

cp "$input" science.txt
cp science.txt science.bak
mv science.bak backups/
cp science.txt tempfile.txt
rm tempfile.txt
mkdir tempstuff
rmdir tempstuff
cat science.txt
head -n 5 science.txt
tail -n 15 science.txt
grep -in science science.txt || true
grep -ivc science science.txt || true
wc -w science.txt
wc -l science.txt

printf '%s\n' pear apple banana > list1
printf '%s\n' plum apple >> list1
sort < list1 > sorted_list
sort list1 | uniq > unique_list
cat unique_list
ls ./*.txt
ls science.?xt
man -w ls || true

chmod 600 science.txt
chmod 700 backups
ls -ld science.txt backups
sleep 30 &
job_pid=$!
ps -p "$job_pid" -o pid,ppid,stat,command || printf 'Process inspection is blocked in this environment.\n'
kill -STOP "$job_pid"
ps -p "$job_pid" -o pid,stat,command || true
kill -CONT "$job_pid"
kill -TERM "$job_pid"
wait "$job_pid" || true
job_pid=''

df -h .
du -sk .
file science.txt
diff science.txt backups/science.bak
gzip -c science.txt > science.txt.gz
gzip -dc science.txt.gz | cmp - science.txt
find . -type f -name '*.txt' -print
date -u '+%Y-%m-%dT%H:%M:%SZ'

## Week 1: Unix essentials

### Tutorial 1: directories and paths

`ls` lists visible entries; `ls -a` includes dotfiles. `mkdir -p unixstuff/backups` creates both directories. `cd .` stays in the current directory, `cd ..` moves to its parent, and `pwd` displays the absolute working path. `~` expands to the current user's home directory, so `ls ~` lists that home and `ls ~/..` lists its parent. A relative path is interpreted from the current directory; an absolute path starts at `/`. These operations were exercised inside a temporary directory to keep the original materials intact.

Reference: [Tutorial One](https://www.cs.sfu.ca/~ggbaker/reference/unix/unix1.html).

### Tutorial 2: files and searches

```sh
cp science.txt science.bak
mv science.bak backups/
mkdir tempstuff
rmdir tempstuff
head -n 5 science.txt
tail -n 15 science.txt
grep -in science science.txt
grep -ivc science science.txt
wc -w science.txt
wc -l science.txt
```

`cp` duplicates content; `mv` relocates or renames a file. `rm` removes a file and `rmdir` removes an empty directory. A nonempty `backups` directory cannot be removed with `rmdir`. `head -n 5` changes the default ten lines to five; `tail -n 15` prints the last fifteen. `grep -i` ignores case, `-n` adds line numbers, `-v` inverts the match, and `-c` counts matching lines. A matching-line count is different from a count of all occurrences of a word. In `less`, `/science` searches and `n` advances to the next match.

Reference: [Tutorial Two](https://www.cs.sfu.ca/~ggbaker/reference/unix/unix2.html).

### Tutorial 3: redirection and pipelines

```sh
printf '%s\n' pear apple banana > list1
printf '%s\n' plum apple >> list1
sort < list1 > sorted_list
sort list1 | uniq > unique_list
```

`>` replaces the destination, `>>` appends, and `<` supplies a file as standard input. A pipe connects one command's standard output to the next command's standard input. Sorting before `uniq` makes equal lines adjacent so repeated entries can be removed. To combine two existing lists and retain distinct entries: `cat list1 list2 | sort | uniq > biglist`.

### Tutorial 4: wildcards and help

`ls *.txt` selects matching non-hidden names in the current directory. `?` matches one character, so `science.?xt` matches `science.txt`. The shell performs this expansion before executing `ls`. Quoting a pattern, as in `find . -name '*.txt'`, passes the pattern to `find` instead. `man ls` opens the command's manual; `man -k keyword` searches manual descriptions. File names are case-sensitive on typical Linux filesystems, while the usual macOS volume is case-insensitive.

### Tutorial 5: permissions and jobs

`chmod 600 science.txt` grants only its owner read/write access. `chmod 700 backups` grants only its owner directory read/write/search access. On directories, read lists names, search/execute permits traversal, and write together with search permits creating or removing entries, subject to restrictions such as the sticky bit.

Appending `&` starts a background job. `Ctrl-Z` suspends a foreground job, `bg` resumes it in the background, `jobs` lists shell jobs, and `fg` brings one forward. `kill -TERM PID` requests termination. `kill -KILL PID` forces termination without allowing cleanup. The script exercised stop, continue, terminate, and wait on its own child.

Reference: [Tutorial Five](https://www.cs.sfu.ca/~ggbaker/reference/unix/unix5.html).

### Tutorial 6: other utilities

`df -h .` reports space on the containing filesystem; `du -sk .` reports directory usage. `file science.txt` identifies the file type. `diff science.txt backups/science.bak` checks for content changes. `gzip -c science.txt > science.txt.gz` creates a compressed copy, and `gzip -dc science.txt.gz | cmp - science.txt` checks the decompressed content. `find . -type f -name '*.txt'` searches recursively. Quota and print utilities depend on the host's services.

The public tutorial index is [Unix Tutorial for Beginners](https://www.cs.sfu.ca/~ggbaker/reference/unix/). It covers the six topic groups above.

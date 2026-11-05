## Week 3: Git version control

### Q1. Count Paul Smith's commits in GNU Make

```sh
git clone https://github.com/mirror/make.git
cd make
git log --format='%an' | grep -x 'Paul Smith' | wc -l
```

The available full-history local clone produces **1,208** matching commits reachable from its current `HEAD`, at revision `c63a5bc6a2881d515bb3020ed477fcba08fb2f3d`. That revision's author date is `2024-08-04T23:48:51-04:00`. It is an existing snapshot, not a claim about today's upstream total; network access prevented fetching updates. `git rev-parse --is-shallow-repository` returned `false`. The pipeline emits one author name per commit, matches the complete name, and counts those lines. This counts commits, including matching merge commits, rather than changed files or lines.

Reproduce the count with `bash week03/count_commits.sh /path/to/make`.

### Q2. What does `git commit -a` replace?

It stages modifications and deletions of already tracked files and then creates a commit. It combines the relevant tracked-file staging normally done with `git add -u` and a subsequent `git commit`. It does **not** add untracked files: a newly created file must first be staged with `git add filename`. `git add` records content in the index; `git commit` records the staged snapshot in repository history. Without `-m`, Git normally opens an editor for the message.

Reference: [Git commit documentation](https://git-scm.com/docs/git-commit).

### Q3. Compare the three log commands

| Command | Meaning |
| --- | --- |
| `git log` | All commits reachable from `HEAD`, with the usual default ordering. |
| `git log HEAD~4..HEAD` | Commits reachable from `HEAD` excluding everything reachable from its fourth first-parent ancestor. |
| `git log HEAD..HEAD~4` | Commits reachable from that ancestor but not from `HEAD`; empty because the ancestor is already reachable from `HEAD`. |

In a linear history the middle command shows the latest four commits. In a merged history it can show more than four: the local exercise shows six because commits from the merged side branch are also reachable. `~4` follows the first parent four times; a two-dot range is a reachability difference, not a fixed commit count.

### Completed Git exercises

The Git exercise covered initialization, staging, committing, cached diffs, an experimental branch, divergent edits, a merge conflict and its resolution, a tag, a local clone, and a pull. It also used a local bare repository to practice pushes and merges.

The remote in that transcript is explicitly a **local bare repository**, not a hosted GitLab or GitHub account. GitLab merge requests and the Web IDE were not exercised. No remote GitHub push was performed.

The actual exercise history is preserved in `week03/git-exercise.bundle`, including both branches. To inspect a separate clone:

```sh
git clone week03/git-exercise.bundle /tmp/cogr-git-review
git -C /tmp/cogr-git-review log --graph --oneline --all
```

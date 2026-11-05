# COGR 2008 practical exercises

Practical code, worked answers, and execution records for modules 1–5 and 7–9. Module 6 has no practical.

The source handouts remain in the parent directory. Completed files are kept here so the supplied examples remain available for comparison.

## Reading the results

- [Practical_Answers.pdf](Practical_Answers.pdf) is the formatted report; [Practical_Answers.md](Practical_Answers.md) is its editable source.
- Each `weekNN` directory contains its code, notes, and relevant evidence. Raspberry Pi Linux measurements are in `evidence/pi_runs/`.
- [STATUS.md](STATUS.md) distinguishes completed work from unperformed activities. Jetson-specific hardware steps are left out as requested.
- `evidence/` contains records of actual executions. These are local catch-up runs, dated when performed.

## Running the code

Python dependencies: `python3 -m pip install -r requirements.txt`. A JDK and `make` are needed for Week 2. `tmux` is needed for its session exercise. Many Unix exercises can run on macOS; Jetson-specific observations and the supplied GPU inference setup require the course device, YOLOX installation, checkpoint, and input images.

```sh
make verify
```

Each week's notes also provide individual commands. Set `PYTHON=/path/to/python` when using a particular Python environment.

To rebuild the report, run `python3 build_answers.py` and `python3 prepare_report.py`. The native PDF renderer is macOS-specific: `swift render_report.swift report_blocks.json Practical_Answers.pdf`. The HTML version can also be printed from a browser.

## GitHub

The empty private repository is [Rafid-Tahmid/cogr2008-practicals](https://github.com/Rafid-Tahmid/cogr2008-practicals). Its URL is configured as this local repository's `origin`. No practical files have been uploaded. To push the prepared commits, run from this directory:

```sh
git push -u origin main
```

If Git requests authentication, sign in using your normal GitHub credentials or credential manager. To inspect the prepared history and remote first:

```sh
git log --oneline
git remote -v
```

The GitLab web exercise (merge requests and Web IDE) remains a separate account-specific activity. Local Git demonstrations and their saved history are in `week03`.

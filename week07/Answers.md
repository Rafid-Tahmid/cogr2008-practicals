## Week 7: processes, scheduling, and synchronization

### Practical Q1. Explain the CPU-consuming loop

`seq 1 100000` produces 100,000 loop values. Each iteration executes `expr 1 + 1`, which evaluates to 2, and redirects its output to `/dev/null`. The arithmetic result is discarded. Most of the cost comes from repeatedly launching the external `expr` program, including process creation and scheduling, rather than performing one addition. Five background copies create runnable work that competes for CPU time. The provided `week07/prac07.sh` uses the requested loop, with an optional iteration-count argument.

### Practical Q2. Nice level and CPU utilization

A larger nice value generally gives a normal Linux process a lower scheduling weight. Under CPU contention it normally receives a smaller share than an otherwise comparable process with a lower nice value. Nice values are relative scheduling preferences, not fixed CPU percentages. A lower-priority process can still use an idle CPU fully; multiple cores and waiting for child processes can also affect the observation. Increasing a process's priority usually needs additional permission.

`nice -n 10 command` starts at an adjusted nice level. On Linux, `renice -n 10 -p PID` requests a nice value of 10; exact `renice` option semantics should be checked on other Unix platforms. The Raspberry Pi Linux run succeeded: five ordinary workers started at nice 0, a sixth at nice 10, and two workers were changed to nice 10 and 15. The `ps` snapshots in `week07/processes.txt` show lower measured CPU percentages for the adjusted workers during that short run; the exact percentages depend on contention and sampling.

### Practical Q3. Kill all the practical's workers

`week07/kill_workers.sh` uses `pgrep` restricted to the current user, then checks each matched process's command line against the absolute path to this practical's `prac07.sh`. It sends `SIGTERM` only to matching workers. Checking the path avoids killing unrelated programs whose names happen to contain the same text. The bracketed pattern `[p]rac07[.]sh` prevents matching the literal search pattern itself. `SIGKILL` is suitable for the handout's forced-termination demonstration but should not replace graceful termination when cleanup matters.

`week07/run_process_demo.sh` starts five normal workers and one nice-adjusted worker, records process data, renices two workers, forcibly ends one, and terminates the others. It cleans up its own children even if a step fails. The Raspberry Pi run completed with all six workers exited; its transcript is `week07/processes.txt`. `tegrastats` remains Jetson-specific.

### In-class Q1. Round robin with a 500 ms quantum

Assume the CPU is busy whenever a job is runnable and a change between jobs costs 10 ms. Execution efficiency means useful CPU work divided by elapsed CPU-plus-switch time; it is not completed-jobs throughput for jobs that never finish.

**Two compute-bound jobs:** a full recurring cycle is 500 + 10 + 500 + 10 = 1020 ms. Efficiency is 1000/1020 = **98.04%**, and each job gets 500/1020 = **49.02%** of elapsed time. The jobs are treated equally. If both arrive at time zero and job 1 starts immediately, their first-response delays are 0 and 510 ms, giving **255 ms average first response**. After a job exhausts a slice, the time until its next slice is 10 + 500 + 10 = **520 ms**. These are different response-time definitions.

**A compute-bound job and an editor:** an editor request arriving just as the compute job starts can wait **510 ms** before executing, then use 20 ms. The input-arrival distribution is not specified, so a unique average interactive response cannot be calculated. If requests arrive uniformly during the compute job's 500 ms burst, the conditional mean delay to first execution is 250 + 10 = **260 ms**. An immediately ready editor can have a much shorter delay.

For an illustrative recurring cycle in which the editor becomes ready in time for its next turn, useful work is 500 + 20 = 520 ms and switching is 20 ms, giving efficiency **520/540 = 96.30%**. This is conditional on the editor's unspecified input timing. One 10 ms switch is 50% of a 20 ms editor burst, but that is not a 50% overhead for the whole workload. Equal turns do not guarantee acceptable interactive latency. A smaller quantum improves responsiveness at the cost of more switching; an MLFQ or an interactive-priority policy can respond to short bursts while preserving longer slices for CPU-bound work. Periodic priority boosts help prevent starvation.

### In-class Q2. Three round-robin tasks

All jobs arrive at time zero. The quantum is 19 and each switch costs 1. The following chart follows the supplied solution's convention of charging a switch after every CPU segment, including the final exit:

| Task | CPU interval | Switch interval | Remaining CPU |
| --- | --- | --- | --- |
| 1 | 0–19 | 19–20 | 47 |
| 2 | 20–39 | 39–40 | 5 |
| 3 | 40–59 | 59–60 | 24 |
| 1 | 60–79 | 79–80 | 28 |
| 2 | 80–85 | 85–86 | 0 |
| 3 | 86–105 | 105–106 | 5 |
| 1 | 106–125 | 125–126 | 9 |
| 3 | 126–131 | 131–132 | 0 |
| 1 | 132–141 | 141–142 | 0 |

Useful execution is 66 + 24 + 43 = **133 units**. Under that convention there are nine switches and 142 elapsed units, so switching consumes **9/142 × 100 = 6.34%**. Taking completion at the ends of the charged slots gives (86 + 132 + 142)/3 = **120 units**.

If completion means the instant a task finishes its CPU work, completion times are 85, 131, and 141, with mean **119 units**. If no final switch is charged after the last task, the makespan is 141 with eight intervening switches, giving **8/141 × 100 = 5.67%** switching overhead. These alternatives explain the one-unit convention difference rather than changing the CPU schedule.

### In-class Q3. First ten MLFQ iterations

An iteration here means one dispatch, matching the supplied solution. Queue front is shown on the left. A CPU-bound process using its entire quantum moves down a level; C returns to Q1 after its one-unit I/O. I/O overlaps CPU execution. As in the supplied table, an I/O completion does not preempt a lower-level process in the middle of its current quantum. A strictly preemptive MLFQ would produce a different timeline, so this assumption is necessary. Context-switch overhead is unspecified and treated as zero.

The parenthesized letter identifies the process that ran during that row, corresponding to the requested circled process. Queues and I/O are shown at the end of the dispatch, with remaining CPU amounts.

| Iteration | Time | Ran | Q1: 2 units | Q2: 4 units | Q3: 8 units | In I/O |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | — | A:10, B:20, C:10 | — | — | — |
| 1 | 0–2 | (A) | B:20, C:10 | A:8 | — | — |
| 2 | 2–4 | (B) | C:10 | A:8, B:18 | — | — |
| 3 | 4–5 | (C) | — | A:8, B:18 | — | C:9 until 6 |
| 4 | 5–9 | (A) | C:9 | B:18 | A:4 | — |
| 5 | 9–10 | (C) | — | B:18 | A:4 | C:8 until 11 |
| 6 | 10–14 | (B) | C:8 | — | A:4, B:14 | — |
| 7 | 14–15 | (C) | — | — | A:4, B:14 | C:7 until 16 |
| 8 | 15–19 | (A) | C:7 | — | B:14 | — |
| 9 | 19–20 | (C) | — | — | B:14 | C:6 until 21 |
| 10 | 20–28 | (B) | C:6 | — | B:6 | — |

A has completed by iteration 8. C still needs six CPU bursts and six I/O units after iteration 10. `week07/scheduling.py` reproduces the timeline and queue snapshots.

### In-class Q4. Semaphore outcomes

Treat each displayed instruction as atomic. `down(s)` blocks when the semaphore is zero; `up(s)` increments it and permits a waiting operation to proceed. Initial state: x=0, y=23, z=0, m=1, ml=0, mx=1. `week07/semaphore_outcomes.py` enumerates the complete instructions, including semaphore operations.

**(a) Final x is 24 or 25.** Both processes use `m` around their updates, so the two critical sections cannot overlap. P1 then P2 gives `z=x; z++; x=z` followed by `y++; x=y`, ending at 24. P2 then P1 first sets x=24, then increments it to 25. Both completed orders release `m` and neither deadlocks.

**(b) Final x is 25 only.** P1 initially blocks on `down(ml)`. P2 executes `down(m); y++; x=y; up(ml)`, establishing x=24 before P1 proceeds. P1 then executes `down(ml); z=x; z++; x=z; up(m)`, establishing x=25. This is an ordering constraint between processes.

**(c) Final x is 1, 24, or 25.** The `up` operations at the beginning and `down` operations at the end do not protect the updates. Example full schedules are:

```text
x=1:
P1 up(ml), z=x, z++;
P2 up(ml), y++, x=y;
P1 x=z, down(m);
P2 down(ml).

x=24:
P1 up(ml), z=x, z++, x=z, down(m);
P2 up(ml), y++, x=y, down(ml).

x=25:
P1 up(ml);
P2 up(ml), y++, x=y;
P1 z=x, z++, x=z, down(m);
P2 down(ml).
```

**(d) Successful completion gives x=24 or x=25, and deadlock is also reachable.** If P1 acquires both locks first, its full critical section precedes P2 and x ends at 24. If P2 acquires both first, the final value is 25. A deadlock schedule is P1 `down(mx)`, P2 `down(m)`, then P1 blocks on `down(m)` and P2 blocks on `down(mx)`. Here x remains zero, but this is a blocked intermediate state rather than a completed result. Requiring both processes to acquire locks in the same order prevents this circular wait.

### In-class Q5. Deadlock and starvation

Deadlock is a state in which a set of activities cannot progress because each waits for a resource or event that another member of that set must release or produce. Starvation means one activity waits indefinitely while other work can continue, for example because a priority policy never selects it. Fair scheduling can address some forms of starvation but cannot resolve a circular lock dependency on its own.

Deadlock requires mutual exclusion, holding resources while waiting for more, lack of preemption, and circular wait. Prevention breaks at least one condition: impose a global lock order, acquire needed resources together, avoid holding locks across waits, or use appropriate try-lock/retry designs. Avoidance can instead admit allocations only when the state remains safe, provided resource requirements are known.

Recovery can abort a selected process or transaction, roll it back, or preempt a recoverable resource. Recovery must restore application invariants; forcibly unlocking arbitrary live program state is unsafe. A single thread can deadlock by attempting to acquire the same nonrecursive mutex twice before releasing it, or by waiting for an event that only it can generate.

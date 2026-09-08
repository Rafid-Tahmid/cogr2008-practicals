## Week 5: Jupyter and debugging

### Q1. Why does Jupyter show `/` when started from `~/prac05`?

The file browser's `/` is the root of the directory tree exposed by the Jupyter server, not necessarily the operating system's filesystem root. With the ordinary configuration, launching the server from `~/prac05` makes that directory the server's root. Consequently the notebook browser displays it as `/`, even though its absolute OS path is under the user's home directory. An explicitly configured server root can override this default.

Reference: [Jupyter: running the notebook](https://docs.jupyter.org/en/latest/running.html).

### Q2. Explain the backtrace and recursion

The Variables panel shows the values in the selected stack frame, including `n` and the lists referenced by `source`, `target`, and `auxiliary`. The call stack/backtrace shows the active nested function calls. Repeated `move` frames with decreasing `n` demonstrate recursion. In the first move of the three-disk run, the active frames have `n=3`, then `n=2`, then `n=1`; they also assign different source/target roles to the same peg lists. The `n=0` base case returns without moving a disk.

The recursive algorithm moves the top `n-1` disks aside, moves the largest remaining disk to the destination, and moves the `n-1` disks onto it. Its recurrence is T(n) = 2T(n-1) + 1, giving 2^n - 1 moves, so three disks require seven moves.

`week05/Hanoi.ipynb` contains the three executable practical cells with saved outputs. `week05/create_notebook.py` executed those cells in a fresh Python namespace and captured actual stack frames using Python tracing. That record is `evidence/week05_actual_stack.json`; it is not a Jupyter GUI screenshot. The additional `hanoi.py` implementation validates every move and the final peg state. The run ended with A and B empty and C equal to `[3, 2, 1]`.

To perform the interactive part, open the notebook in JupyterLab, enable the debugger, place a breakpoint at `target.append(source.pop())` in the function cell, and run the cells in order. Defining the function does not execute its body, so the breakpoint is reached only when the third cell calls it.

### Q3. Combine VM forwarding and the SSH tunnel

```sh
ssh -p 2522 -N -L 127.0.0.1:8080:localhost:8888 tonystark@localhost
```

VirtualBox must forward host TCP port 2522 to the VM's SSH port 22. `-p 2522` connects to that forwarded SSH service; `-N` starts no remote command. `-L` listens on the host's loopback port 8080 and forwards traffic through SSH to `localhost:8888` as seen from the VM. Start Jupyter inside the VM on port 8888, keep the tunnel open, and use `http://localhost:8080` with Jupyter's authentication token. The host and guest occurrences of `localhost` identify different machines in their respective contexts.

The question sheet specifies guest port 8888. The last example in the practical handout instead says 8080; use the actual guest Jupyter port, which is normally 8888. No VM/SSH service was available to verify this connection locally.

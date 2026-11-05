## Week 9: memory management

### Practical Q1. Explain each NumPy allocation

`np.zeros(123456789)` uses the default `float64`, with eight bytes per element. Each array's data buffer therefore occupies **987,654,312 bytes**, about 0.920 GiB, excluding array-object and allocator overhead. The arithmetic operations create new arrays rather than changing `my_array`.

| Command | Live arrays | Total live array data |
| --- | --- | --- |
| `import numpy as np` | None from the exercise | 0 bytes, plus imported-library overhead |
| `my_array = np.zeros(123456789)` | Original | 987,654,312 bytes |
| `my_array1 = my_array + 1` | Original, +1 | 1,975,308,624 bytes |
| `my_array2 = my_array + 2` | Original, +1, +2 | 2,962,962,936 bytes |
| `my_array3 = my_array + 3` | Original, +1, +2, +3 | 3,950,617,248 bytes |
| `del my_array3` | Original, +1, +2 | 2,962,962,936 bytes |
| `del my_array1` | Original, +2 | 1,975,308,624 bytes |

The table gives logical array-buffer sizes, not measured RSS or guaranteed swap use. Demand-zero pages, allocator caching, and OS accounting mean physical usage need not immediately equal the allocated size. Producing the nonzero arrays touches their output pages. On a 2 GB Jetson the working set can exceed available RAM, leading to swapping or allocation failure if insufficient backing storage exists. `del` removes a reference; a buffer becomes reclaimable when no references remain, but it need not immediately reduce the process's RSS.

`week09/memory_demo.py` was run on the Mac with **1,000,000 elements per array**, rather than creating several gigabytes of pressure on the active machine. Recorded RSS rose from about 40.3 MB before the arrays to 72.4 MB with all four. In that run RSS remained near 72.4 MB after deletion, despite the live array data falling from 32 MB to 16 MB, illustrating retained allocator pages. Swap measurement was blocked and is recorded as unavailable, not zero. See `evidence/week09_memory_scaled.json`.

A separate Raspberry Pi Linux run at the same scale recorded RSS rising from about 26.0 MB to 50.0 MB with all four arrays, then falling to about 34.0 MB after the two deletions. The Pi reported zero swap in use throughout this scaled run. See `evidence/pi_runs/memory_arrays.txt`. These are observations of the Pi, not of the course Jetson or the full-size workload.

The Raspberry Pi also completed the handout's **123,456,789-element** run. With all four arrays live, logical array data was 3,950,617,248 bytes and process RSS was about 2.99 GB. The initially allocated zero array added almost nothing to RSS until the later operations touched its pages. After deleting `my_array3` and `my_array1`, RSS fell to about 1.01 GB. Pi swap usage stayed at zero throughout; the separate `free` inspection showed 7.6 GiB of RAM and 2.0 GiB of zram swap. The full measurements are in `evidence/pi_runs/memory_full.txt` and `evidence/pi_runs/memory_inspection.txt`. These are Pi results; the 2 GB Jetson could behave differently.

Reference for the default array type: [NumPy zeros](https://numpy.org/doc/stable/reference/generated/numpy.zeros.html).

### Practical Q2. Why do the parent and child branches both print?

`os.fork()` creates a child process. Both processes resume after the call, but the return value differs: the parent receives the child's positive PID and the child receives zero. Therefore the parent executes the `if n > 0` branch and the child executes `else`. One process does not execute both branches. Their outputs can appear in either order because they are independently scheduled. The completed demonstration also calls `waitpid` so the parent reaps the child before exiting.

Reference: [Python os.fork](https://docs.python.org/3/library/os.html#os.fork).

### Practical Q3. Same address, different values; integers versus floats

Each process has a separate virtual address space after `fork`. The same numerical virtual address in two processes can map to different physical storage. Initially many pages can be shared with copy-on-write; writes create private copies as needed. Consequently equal printed addresses across processes do not establish that the processes share a mutable Python object.

Python integers and floats are immutable. `x += 1` or `x += 2` rebinds `x` to the result rather than changing the original numeric object's value. In CPython, small integers are cached, so the preexisting objects for 11 and 12 have distinct identities. Floats produced after a fork can be allocated at corresponding virtual locations by the two copied allocators, producing equal numerical addresses for 11.0 and 12.0 in different processes. This outcome is implementation- and run-dependent; it is not guaranteed for every float operation.

The Mac run matched the handout's pattern: parent and child integer result IDs differed, while their float result IDs were equal. In the Raspberry Pi Linux run, the float result IDs differed too, confirming that equality is not guaranteed. Both runs produced the expected independent parent and child values. Exact values and addresses are in `evidence/week09_fork.txt` and `evidence/pi_runs/fork.txt`. Within the initial single process, `x=10; y=10` shared the same cached integer object, then `y += 1` changed only `y`'s binding. The `ctypes` demonstration retrieved 10 from the still-live `x` object.

`id()` is generally an object identity; its interpretation as an address is a CPython implementation detail. References: [Python id](https://docs.python.org/3/library/functions.html#id) and [CPython integer objects](https://docs.python.org/3/c-api/long.html). Do not assume a specific small-integer cache boundary across interpreter versions.

### Homework Q1. Virtual and physical addresses

A virtual address is an address interpreted within a process's address space. A physical address identifies a location in physical memory. The MMU translates a virtual page number through the current address-space mapping and combines the selected physical frame with the page offset. Page tables can map the same virtual page number to different frames for different processes. Thus two variables can have identical numerical virtual addresses yet independent stored values. Processes can also deliberately share a physical frame through explicit shared-memory mappings.

### Homework Q2. Swap-backed virtual memory and thrashing

Swap allows less-active memory pages to be moved out of RAM so more programs, or a larger total allocation, can remain supported than would fit entirely in physical memory. Demand paging can keep the actively used working set in RAM while leaving less-used data on storage. It does not make storage as fast as RAM, and not all virtual pages necessarily need swap: some are file-backed or can be recreated.

Page faults introduce storage latency, page-management work, and sometimes dirty-page writes. A swap file consumes disk space; on flash, write traffic also affects wear. If half of all memory references require swap retrieval, performance is extremely poor because storage access is orders of magnitude slower than a RAM access. A simplified model is effective access time = (1-p) × RAM-access-time + p × page-fault-service-time. For illustration, at p=0.5, 100 ns RAM and 1 ms fault service give about 0.50005 ms per reference, roughly 5000 times the RAM-only access time. Actual performance depends on hardware, locality, caching, and fault overlap; these numbers are illustrative, not measured.

At a zero swap-retrieval rate, execution is not delayed by reads from swap, although ordinary cache misses, file-backed page faults, and other overhead remain possible. Thrashing occurs when active working sets exceed available frames and repeated faults evict pages that are soon needed again. Reduce the active workload or its working set, add RAM, use locality-aware algorithms, or adjust admission/working-set policies. A larger swap file alone may avoid allocation failure without curing thrashing.

### Homework Q3. Memory and I/O protection

The OS installs page-table mappings with access permissions such as user/supervisor, readable, writable, and executable. On each access, the MMU checks translation and permissions; an invalid or forbidden access traps into the kernel. Different processes normally receive different page-table contexts, with translation caches handled appropriately during context switches.

User mode cannot normally alter the protected page tables, enter privileged CPU modes directly, or execute privileged I/O instructions. Device registers mapped into memory are kept outside ordinary user mappings unless the kernel explicitly grants access. Applications request I/O through system calls, and kernel drivers validate and perform it. An IOMMU can additionally restrict device DMA; this is distinct from a CPU MMU's protection of process accesses.

### Homework Q4. Implement second-chance FIFO

Keep resident pages in a circular list of frames and maintain a clock hand. Each frame has a reference bit that the MMU sets on an access. A hit marks that page referenced. On a page fault, inspect the frame at the hand: if its bit is one, clear it and advance; if its bit is zero, choose it as the victim. Install the new page and advance the hand. A free frame can be used without eviction. Write a dirty victim to backing storage before reusing its frame, and update page tables and invalidate stale translations as required.

Second chance approximates recency without moving pages on every reference or recording exact access timestamps. It needs O(F) frame entries and reference bits for F frames. A replacement may scan O(F) frames; if every reference bit is set, a complete pass clears them and the next visit selects a victim. Page lookup is normally assisted by the hardware mapping rather than a linear search. Sampling or clearing accessed bits can require architecture-specific page-table and TLB handling. The algorithm does not distinguish one recent use from many uses, may evict useful pages under some patterns, and is not exact LRU.

`week09/second_chance.py` provides a small runnable model with three frames. For accesses `1, 2, 3, 1, 4, 2, 5`, the saved trace has **five page faults**. Its list lookup is deliberately simple and costs O(F); a production implementation would use a direct mapping for resident-page lookup. See `evidence/week09_clock.json`.

## Week 8: filesystems and disk storage

### Practical Q1. Find the SD-card mount and filesystem type

The practical uses `mount | grep mmcblk` to select SD-card partition mounts. In a line such as `/dev/mmcblk0p1 on / type ext4 (...)`, `/` is the mount point and `ext4` is the filesystem type. `sudo fdisk -l` lists partitions but does not itself establish their current mount points. `cat /etc/fstab` shows configured mounts, which should be compared with the live mount output.

The course Jetson image is expected to use ext4 for its root filesystem, but no Jetson mount output was available to establish the actual device's type. Confirm with `findmnt -no SOURCE,FSTYPE /` on the device. `week08/inspect_device.sh` records these live values without modifying any partition.

### Practical Q2. Explain the image-counting loop

`find . -type d` produces the directory names below the current directory. The shell substitutes that output into the `for` loop; each iteration prints a directory and then runs a recursive search for names ending in `.jpg`, ignoring case. `wc -l` counts the output lines. Because each directory search is recursive, a parent's count includes images in all its descendants. The totals therefore overlap and must not be added to obtain a unique overall image count.

The original `for i in $(find ...)` and unquoted `$i` break on directory names containing whitespace or wildcard characters. Without `-type f`, directories whose names end in `.jpg` also count. `week08/count_images.sh` corrects these problems using NUL-delimited paths, quoted arguments, and `-type f`. A local fixture containing two JPEG files, one inside a directory with spaces, produced a root count of two and a subdirectory count of one. See `evidence/week08_image_count_fixture.txt`.

### Practical Q3. Why avoid nesting tmux?

An inner and outer session normally share the `Ctrl-b` prefix. The outer session intercepts it, making it less obvious which session receives commands; nested panes and status bars also become confusing. Use another window or pane in the existing session. If nesting is intentional, send a prefix through to the inner session or configure distinct prefixes. `tmux a || tmux` attaches to an existing session or creates one if attachment fails.

`week08/tmux_demo.sh` uses a separate tmux socket to avoid touching personal sessions. It demonstrates a counter continuing while another window is selected and no client is attached. This workspace denied creating the socket, so the demonstration remains unverified; the error is in `evidence/week08_tmux.txt`.

### Object detection exercise

On the course Jetson, activate `~/YOLOX/venv36` and run `week08/run_detection.sh`. It processes every `.jpg` file using the supplied experiment, checkpoint, and GPU settings. Set `CONFIDENCE=0.5` to repeat at a higher confidence threshold. Raising the threshold filters out lower-confidence detections, generally reducing displayed boxes and potentially missing true objects; lowering it generally displays more boxes and risks more false positives. It does not retrain the model.

The script retains `--nms 0.45`, `--tsize 640`, `--save_result`, and `--device gpu` from the handout. It handles filenames with spaces and fails clearly if the checkpoint or inputs are missing. These assets and the Jetson GPU were unavailable here, so no prediction images or detection counts are claimed.

### In-class Q1. Fairness and request ordering

For a continuous random stream, a conventional fairness ranking is **FCFS, C-SCAN, SCAN, SSTF**, from most to least fair. FCFS preserves arrival order. C-SCAN tends to give more uniform waits across positions. SCAN services requests in both directions, giving position-dependent waits. SSTF can indefinitely postpone distant requests under a stream of nearby arrivals. Fairness and minimum head movement are different objectives.

With the given finite queue, initial head position 9, upward motion, and reversal/wrap at the last requested cylinder rather than the physical disk edge:

| Algorithm | Service order | Total movement |
| --- | --- | --- |
| FCFS | 11, 15, 18, 6, 13, 7, 5, 8 | 39 cylinders |
| SSTF | 8, 7, 6, 5, 11, 13, 15, 18 | 17 cylinders |
| SCAN | 11, 13, 15, 18, 8, 7, 6, 5 | 22 cylinders |
| C-SCAN | 11, 13, 15, 18, 5, 6, 7, 8 | 25 cylinders |

The specified endpoint behaviour is often called LOOK and C-LOOK. The C-SCAN movement includes the return from 18 to 5, although no requests are serviced during that return. The script `week08/disk_calculations.py` computes these orders and distances.

### In-class Q2. Small queues and locality

With exactly one pending request there is no scheduling choice, so all algorithms choose that request. With two or three requests the algorithms need not become FCFS. For example, from cylinder 9, if requests arrive in order 18 then 8 and both are pending, FCFS chooses 18 while SSTF chooses 8. Small queues simply reduce opportunities for reordering.

Spatial locality usually reduces the practical differences because requests cluster within a small region, making long seeks less common. The exact effect still depends on head position and the arrival pattern; a persistent nearby stream can make SSTF's starvation of a distant request especially visible.

### In-class Q3. Disk timings and transfer rate

6000 rpm / 60 = **100 revolutions per second**, giving **10 ms per revolution**. A random request waits on average half a revolution, so average rotational delay is **5 ms**. Combined seek plus rotation is 10 ms, so average seek time is **10 - 5 = 5 ms**.

The average complete block read takes **6 seconds / 400 = 15 ms**. Subtracting seek and rotation leaves **5 ms transfer time**. At 10,000 bytes per block, raw transfer rate is **10,000 / 0.005 = 2,000,000 bytes/s = 2 MB/s**. If the question uses 10 KiB instead of decimal 10 kB, the equivalent result is 2,048,000 bytes/s; the time calculations do not change.

### In-class Q4. Inode maximum file size and block 1200

A 4096-byte pointer block holds 4096/4 = **1024 pointers**. The inode can therefore address:

```text
10 direct blocks
+ 1024 singly indirect blocks
+ 1024^2 doubly indirect blocks
+ 1024^3 triply indirect blocks
= 1,074,791,434 data blocks
```

Maximum file content size is **1,074,791,434 × 4096 = 4,402,345,713,664 bytes**, approximately **4.402 TB** or **4.00391 TiB**. Pointer blocks consume additional disk space but are not part of the file's data length. The stated disk capacity in the preceding independent question does not constrain this question's different hypothetical inode structure.

Direct and single-indirect addressing cover the first 10 + 1024 = 1034 blocks. The one-based 1200th data block is therefore in the double-indirect region. With only the inode cached, read the double-indirect root block, its first leaf pointer block, and then the requested data block: **three disk reads**. Its leaf entry is the 166th data pointer in that leaf, or zero-based index 165. Cached pointer blocks could reduce the reads.

### In-class Q5. A crash during journal recovery

A committed transaction remains in the journal until its home-location updates are safely persisted and the journal space can be reclaimed. After another crash, recovery can replay the still-valid committed record again. Redo operations must be idempotent, such as writing the recorded block contents, so repeating them does not corrupt an already updated block.

An incomplete transaction without a valid commit record is not replayed. If a recovery crash occurs after some home blocks have been written, retained committed records allow the rest to be recovered on the next boot. Safe checkpointing and journal reuse must distinguish complete records from partial writes, and ordering/flush guarantees must ensure that data does not appear committed before the required log records are durable. Thus repeated crashes can be tolerated by a correctly implemented protocol; deleting needed log data too early breaks that guarantee.

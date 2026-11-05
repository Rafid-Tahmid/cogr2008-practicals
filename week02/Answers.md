## Week 2: build automation

### Q1. Display commands without executing them

Use `make -n`, also called `make --dry-run`. For a particular target, use `make -n run`. Make prints the recipes it would normally execute. It does not print recipes for targets that are already up to date. Recursive make and recipes explicitly marked for execution have special dry-run behaviour; the Java recipes here contain neither.

The local dry run printed `java DriverATM` without running the program.

### Q2. Explain `javac -g SharedAccount.java`

`javac` compiles Java source into JVM bytecode, normally writing `SharedAccount.class`. `-g` includes debugging information for line numbers, source files, and local variables so a debugger can relate the bytecode to the source. It does not start the program. Run bytecode using `java DriverATM` for this exercise.

Reference: [Oracle javac documentation](https://docs.oracle.com/en/java/javase/25/docs/specs/man/javac.html).

### Q3. Implement `make run` even if a file named `run` exists

`run` must be a phony target and must depend on the build:

```make
.PHONY: all run clean

run: all
	$(JAVA) DriverATM
```

The complete Makefile is `week02/Makefile`. It also makes `clean` phony and records dependencies between the Java classes. Recipes begin with a tab. `run: all` ensures compilation finishes before execution. `.PHONY` prevents an unrelated file called `run` or `clean` from suppressing the recipe.

### Build and timestamp exercises

The three supplied Java files were copied without changing their program logic. `make clean all` compiled them, and `make run` executed both transactions. The recorded run deposited 100, increasing the balance from 1000 to 1100, then withdrew 100, returning it to 1000. Thread order can vary, but synchronization makes each transaction indivisible with respect to the other transaction.

The phony-target exercise created files named `run` and `clean`. Execution still ran and cleaning still removed the class files. The temporary files were removed afterwards.

With the original sample Makefile, touching `SharedAccountClient.java` rebuilds that class alone. This completed Makefile also declares that `DriverATM.class` depends on it, so a client change rebuilds the client and driver. Touching a file changes its modification time, not its content; make uses those timestamps to decide whether a target is stale.

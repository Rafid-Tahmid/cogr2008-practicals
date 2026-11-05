## Week 4: testing and bug tracking

### Q1. Explain each supplied assertion

In `test_count_students`, `response.status_code == 200` checks that a request to `/` succeeds. `int(response.data) <= n_max` converts the response body to an integer and checks that it does not exceed the total capacity: 40 + 20 + 20 + 40 = 120. A nonnumeric response also fails through a conversion error.

In `test_count_teachers`, the status assertion checks that `/teacher` succeeds. The body assertion checks the entire response, including wording and instructor count. The supplied expected count of three is inconsistent with the app's one lecturer plus one tutor. It was corrected to `b'There are 2 instructors'`, as the handout instructs fixing the test rather than changing the app.

### Q2. Include the minimum class size

Replace the upper-bound assertion with:

```python
assert 0 <= int(response.data) <= n_max
```

This also rejects negative totals. The application's current data is hard-coded at 120, so this verifies the allowed lower bound without pretending to exercise a separate configurable zero-enrolment state. Checking each class independently would require the app to expose its individual counts. Both current tests passed locally.

### Q3. Makefile implementation

```make
PYTHON ?= python3
.PHONY: all test deploy clean

all: test
	@trap '$(MAKE) clean' EXIT; $(MAKE) deploy

test:
	@$(PYTHON) -m pytest -v > unit_test.txt 2>&1; result=$$?; cat unit_test.txt; exit $$result

deploy:
	$(PYTHON) -m flask --app prac run --host 127.0.0.1

clean:
	rm -f unit_test.txt
```

`make test` captures standard output and standard error in `unit_test.txt`, displays the saved result, and preserves pytest's exit code so failing tests fail the build. `$$` passes a literal dollar sign through make to the shell. `make deploy` starts Flask locally and runs until stopped. `make clean` removes the temporary log. `make all` requires passing tests before deployment and installs an exit trap to clean the log after the deployment command exits. Using this ordered recipe avoids starting the server before tests finish under parallel make.

The application was checked using Flask's test client. `deploy` is a local development server, not a hosted deployment.

### Bug-tracker comparison

**OpenProj:** its [SourceForge bug tracker](https://sourceforge.net/p/openproj/bugs/) provides open/closed searches and columns for milestone, status, owner, dates, and priority. The fetched open list includes ticket 580 and ticket 233, illustrating that a ticket's age and its open status are separate facts. Opening the filtered closed-ticket view failed in this environment, so no particular closed-ticket result is asserted.

**GIMP:** [GNOME/gimp on GitHub](https://github.com/GNOME/gimp) is a read-only mirror. The branch listing showed `master`, `gimp-3-2`, and topic branches such as `bruno/mac-win-accent`. Their names suggest main development, release maintenance, and focused changes respectively; these purposes are an inference from names rather than verified policies. The repository exposes an Insights tab, but its activity page was rate-limited, so no activity total or graph is claimed. GIMP's [official bug page](https://www.gimp.org/bugs/) directs bug reports to GNOME GitLab and distinguishes open issues, closed issues, platform filters, and feature proposals.

**Blender:** the handout's workflow links development, source contributions, and issue tracking through Blender's developer site. All attempted official Blender pages returned access errors, so its current tracker interface and particular reports could not be inspected. A tracker integrated with code review can connect a report to its fix and review discussion; a separate platform adds another account and workflow to learn. These are general comparison points, not observations of an accessible Blender page.

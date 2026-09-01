PYTHON ?= python3

.PHONY: all test deploy clean

# Test first, then serve until stopped; always remove the temporary test log.
all: test
	@trap '$(MAKE) clean' EXIT; $(MAKE) deploy

test:
	@$(PYTHON) -m pytest -v > unit_test.txt 2>&1; result=$$?; cat unit_test.txt; exit $$result

deploy:
	$(PYTHON) -m flask --app prac run --host 127.0.0.1

clean:
	rm -f unit_test.txt

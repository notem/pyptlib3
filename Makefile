# This is only an ad-hoc way for running multi-language tests.
# Use setup.py for building/distributing.

TEST_DIR = pyptlib/test
BASE_DIR = $(realpath .)
PYTHONPATH = $(BASE_DIR):$(realpath $(TEST_DIR))

.PHONY: check check_py check_sh

check: check_py check_sh

check_py: $(TEST_DIR)/test_*.py
	export PYTHONPATH=$(PYTHONPATH); cd $(TEST_DIR); \
	  for i in $^; do python "$${i#$(TEST_DIR)/}" || exit 1; done

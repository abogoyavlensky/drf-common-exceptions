YELLOW := "\e[1;33m"
NC := "\e[0m"
INFO := @sh -c '\
    printf $(YELLOW); \
    echo "=> $$1"; \
    printf $(NC)' VALUE

.SILENT:  # Ignore output of make `echo` command

.PHONY: help  # Generate list of targets with descriptions
help:
	@$(INFO) "Commands:"
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/\1 > \2/' | column -tx -s ">"


# TODO: update linting
# .PHONY: lint  # Running linting
# lint: version
# 	@$(INFO) "Running flake8..."
# 	@flake8 --statistics --config=setup.cfg $(PEP8_CLEANED)
# 	@$(INFO) "Running pylint..."
# 	@pylint -j 4 $(PEP8_CLEANED)

.PHONY: clean # [Local] Clean temp files from projects: .pyc. .pyo, __pycache__
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf .pytest_cache .mypy_cache
	@$(INFO) "Python caching files has been cleaned."

.PHONY: test
test: version
	@pytest

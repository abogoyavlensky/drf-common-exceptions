YELLOW := "\e[1;33m"
NC := "\e[0m"
INFO := @sh -c '\
    printf $(YELLOW); \
    echo "=> $$1"; \
    printf $(NC)' VALUE

PEP8_CLEANED = drf_common_exceptions

.SILENT:  # Ignore output of make `echo` command

.PHONY: help  # Generate list of targets with descriptions
help:
	@$(INFO) "Commands:"
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/\1 > \2/' | column -tx -s ">"

.PHONY: install  # Install requirements to local virtualenv
install:
	@poetry install

.PHONY: lint  # Run linting and code auto formatting
lint:
	@autoflake --in-place --recursive $(PEP8_CLEANED)
	@$(INFO) "Formatting..."
	@black $(PEP8_CLEANED)
	@$(INFO) "Sorting..."
	@isort -rc $(PEP8_CLEANED)

.PHONY: clean # Clean temp files from projects: .pyc. .pyo, __pycache__
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf .pytest_cache .mypy_cache
	@$(INFO) "Python caching files has been cleaned"

.PHONY: test  # Test package
test:
	@pytest

.PHONY: watch  # Test package in watch mode
watch:
	@ptw

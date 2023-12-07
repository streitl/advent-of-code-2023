SHELL = /bin/bash

.DEFAULT_GOAL := all

## help: Display list of commands
.PHONY: help
help: Makefile
	@sed -n 's|^##||p' $< | column -t -s ':' | sed -e 's|^| |'

## all: Run all targets
.PHONY: all
all: init style test

## init: Bootstrap your application.
.PHONY: init
init:
	pre-commit install -t pre-commit -t commit-msg --install-hooks
	poetry install --no-root --all-extras

## style: Check lint, code styling rules.
.PHONY: style
style:
	bash style.sh --style

## format: Check lint, code styling rules.
.PHONY: format
format:
	bash style.sh --format

## clean: Remove temporary files
.PHONY: clean
clean:
	-pre-commit uninstall -t pre-commit -t commit-msg
	-rm -rf .mypy_cache ./**/.pytest_cache .coverage
	-poetry env remove python

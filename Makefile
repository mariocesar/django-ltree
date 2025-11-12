
BOLD := \033[1m
RESET := \033[0m
GREEN := \033[1;32m

default: help

install: ## Install all development dependencies in editable mode
	pip install -e .[develop]
.PHONY: install

test: ## Run tests
	pytest tests/
.PHONY: test

lint: ## Run ruff check and fix
	ruff check . --fix
.PHONY: lint

build: clean ## Build the package
	python -m build -s -w

publish: build
	twine upload dist/*
.PHONY: publish

clean:
	rm -rf dist/
	rm -rf build/
.PHONY: clean

backend:
	docker-compose run --rm --service-ports backend bash

help:
	@echo -e "$(BOLD)django-ltree Makefile$(RESET)"
	@echo -e "Please use 'make $(BOLD)target$(RESET)' where $(BOLD)target$(RESET) is one of:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-30s$(RESET) %s\n", $$1, $$2}'
.PHONY: help
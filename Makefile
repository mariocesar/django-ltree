.PHONY: test test-matrix lint build publish clean

BOLD := \033[1m
RESET := \033[0m
GREEN := \033[1;32m

POSTGRES_VERSION ?= 16
PYTHON_VERSION ?= 3.13

test:
	POSTGRES_VERSION=$(POSTGRES_VERSION) PYTHON_VERSION=$(PYTHON_VERSION) docker compose run --rm tests

test-matrix: ## Run tests across supported postgres versions
	@for postgres_version in 16 17 latest; do \
		printf "$(BOLD)⇨ postgres:%s$(RESET)\n" "$$postgres_version"; \
		POSTGRES_VERSION=$$postgres_version docker compose run --rm tests || exit 1; \
		docker compose down; \
	done

lint:
	uvx ruff check . --fix

build: clean
	python -m build -s -w

publish: build
	twine upload dist/*

clean:
	rm -rf dist/
	rm -rf build/

	docker compose down --volumes --remove-orphans
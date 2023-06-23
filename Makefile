# ===================================================================
# GLOBALS
# ===================================================================

SHELL=/bin/bash -o pipefail

ifeq ($(OS),Windows_NT)
	detected_OS := Windows
	MKDIR_CMD := mkdir
else
	detected_OS := $(shell uname -s)
	MKDIR_CMD := mkdir -p
endif

# Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://install.python-poetry.org | python3 - --uninstall

# Installation
.PHONY: poetry-install
poetry-install:
	poetry install --no-interaction

# Docker
docker-start:
	docker-compose down
	docker-compose up --build backend
SHELL=/bin/bash

# Virtual environment folder
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python

# Project directory path
PROJECT_DIR=.

.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "  create-virtual-environment:  Create and set up the virtual environment with dependencies."
	@echo "  activate-virtual-environment: Activate the virtual environment."

.PHONY: create-virtual-environment
create-virtual-environment:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r requirements.txt

.PHONY: activate-virtual-environment
activate-virtual-environment:
	@echo "Activating virtual environment..."
	./activate_venv.sh

.PHONY: run-main
run-main:
	@echo "Running main..."
	PYTHONPATH=$(PROJECT_DIR) $(PYTHON) src/main.py

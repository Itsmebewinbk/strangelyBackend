

APP_NAME=main
VENV=.venv

.PHONY: help install run lint format clean

help:
	@echo "Makefile commands:"
	@echo "  make install   - Create venv and install dependencies"
	@echo "  make run       - Run FastAPI app with uvicorn"
	@echo "  make lint      - Run flake8 for linting"
	@echo "  make format    - Format code with black"
	@echo "  make clean     - Remove virtual environment"

install:
	python -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install fastapi uvicorn sqlalchemy pydantic

run:
	$(VENV)/bin/uvicorn $(APP_NAME):app --reload

lint:
	$(VENV)/bin/pip install flake8
	$(VENV)/bin/flake8 .

format:
	$(VENV)/bin/pip install black
	$(VENV)/bin/black .

clean:
	rm -rf $(VENV)


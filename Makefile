.PHONY: help install run clean

help:
	@echo "Makefile commands:"
	@echo "  make install   - Create venv and install dependencies"
	@echo "  make run       - Run FastAPI app with uvicorn"
	@echo "  make clean     - Remove virtual environment"

install:
	rm -rf venv
	python -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

run:
	venv/bin/python -m uvicorn main:app --reload --port 5000

clean:
	rm -rf venv

.PHONY: help test lint smoke clean

help:
	@echo "Targets: test, lint, smoke, clean"

test:
	pytest tests/ -v

lint:
	flake8 main.py src schemas tests scripts

smoke:
	bash scripts/smoke_test.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf *.egg-info build dist

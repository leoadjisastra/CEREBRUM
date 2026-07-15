.PHONY: test lint format type run

test:
	pytest

lint:
	ruff check 
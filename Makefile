.PHONY: help install run clean lint format

help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make run         - Run the telegram bot"
	@echo "  make clean       - Remove cache and build files"
	@echo "  make lint        - Run linting checks"
	@echo "  make format      - Format code with black"

install:
	uv sync

run:
	python main.py

# Run the Telegram bot
bot:
	@echo "Running the Telegram bot..."
	python -m src.bot.app

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache

lint:
	ruff check .

format:
	black .

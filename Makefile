.PHONY: all
all: help

# --------------------------------------------

.PHONY: clean
clean: ## Remove cached files and build products
	@echo Cleaning caches and build products
	@find . -type d -name .mypy_cache -exec rm -rf {} \; -prune
	@find . -type d -name __pycache__ -exec rm -rf {} \; -prune
	@echo Cleaning complete

# --------------------------------------------

.PHONY: reset
reset: clean ## clean, then remove .venv and .mypy cache
	@echo Resetting project state
	rm -rf .mypy_cache .venv

# --------------------------------------------

.PHONY: help
help: ## Show help
	@echo Please specify a target. Choices are:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk \
	'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

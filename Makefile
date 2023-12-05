.PHONY: help
help:
	@echo "Usage:"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

.PHONY: lint
lint:
## lint: Lint the codebase with Prettier
	npx prettier --print-width=99 --check .
	bash ${CURDIR}/.github/shellcheck-actions.sh

.PHONY: format
format:
## format: Formats both Markdown documents and YAML documents to preferred repository style.
	npx prettier --print-width=99 --write .

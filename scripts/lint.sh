#!/usr/bin/env bash -ex

python3 -m mypy --install-types --non-interactive typer_cloup
black typer_cloup tests docs_src --check
isort typer_cloup tests docs_src --check-only

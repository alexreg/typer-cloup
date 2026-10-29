#!/usr/bin/env bash -ex

./scripts/test-files.sh

# Run pytest and its subprocesses with the same Python interpreter.
python3 -m pytest --cov-config=.coveragerc --cov --cov-report=term-missing -o console_output_style=progress --numprocesses=auto "$@"

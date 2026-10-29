import os
import subprocess
import sys

from docs_src.commands.index import tutorial001 as mod


def test_completion_invalid_instruction():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "bashsource",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert result.returncode != 0
    assert "Invalid completion instruction." in result.stderr


def test_completion_source_bash():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "bash_source",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "complete -o nosort -F _tutorial001py_completion tutorial001.py"
        in result.stdout
    )


def test_completion_source_invalid_shell():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "xxx_source",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Shell 'xxx' is not supported." in result.stderr


def test_completion_source_invalid_instruction():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "bash_explode",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Completion instruction 'explode' is not supported." in result.stderr


def test_completion_source_zsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "zsh_source",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "compdef _tutorial001py_completion tutorial001.py" in result.stdout


def test_completion_source_fish():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "fish_source",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "complete --no-files --command tutorial001.py" in result.stdout

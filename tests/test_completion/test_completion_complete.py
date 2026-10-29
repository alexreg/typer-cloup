import os
import subprocess
import sys

from docs_src.commands.help import tutorial001 as mod


def test_completion_complete_subcommand_bash():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "bash_complete",
            "COMP_WORDS": "tutorial001.py del",
            "COMP_CWORD": "1",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "plain,delete\n" "plain,delete-all\n" in result.stdout


def test_completion_complete_subcommand_bash_invalid():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "bash_complete",
            "COMP_WORDS": "tutorial001.py del",
            "COMP_CWORD": "42",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "plain,create\n"
        "plain,delete\n"
        "plain,delete-all\n"
        "plain,init\n" in result.stdout
    )


def test_completion_complete_subcommand_bash_argument():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "bash_complete",
            "COMP_WORDS": "tutorial001.py delete ",
            "COMP_CWORD": "2",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "plain" not in result.stdout


def test_completion_complete_subcommand_zsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "zsh_complete",
            "COMP_WORDS": "tutorial001.py del",
            "COMP_CWORD": "1",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "plain\ndelete\nDelete a user with USERNAME.\n"
        "plain\ndelete-all\nDelete ALL users in the database.\n" in result.stdout
    )


def test_completion_complete_subcommand_fish():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "fish_complete",
            "COMP_WORDS": "tutorial001.py del",
            "COMP_CWORD": "del",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "plain,delete\tDelete a user with USERNAME.\n"
        "plain,delete-all\tDelete ALL users in the database.\n" in result.stdout
    )

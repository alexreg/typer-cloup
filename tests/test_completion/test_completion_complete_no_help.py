import os
import subprocess
import sys

from docs_src.commands.index import tutorial002 as mod


def test_completion_complete_subcommand_zsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002.PY_COMPLETE": "zsh_complete",
            "COMP_WORDS": "tutorial002.py ",
            "COMP_CWORD": "1",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "plain\ncreate\n_\n" "plain\ndelete\n_\n" in result.stdout


def test_completion_complete_subcommand_fish():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002.PY_COMPLETE": "fish_complete",
            "COMP_WORDS": "tutorial002.py ",
            "COMP_CWORD": "",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "plain,create\n" "plain,delete\n" in result.stdout

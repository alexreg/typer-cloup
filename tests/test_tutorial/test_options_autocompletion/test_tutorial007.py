import os
import subprocess
import sys

from docs_src.options_autocompletion import tutorial007 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_completion():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL007.PY_COMPLETE": "zsh_complete",
            "COMP_WORDS": "tutorial007.py --name Sebastian --name ",
            "COMP_CWORD": "4",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "plain\nCamila\nThe reader of books.\n"
        "plain\nCarlos\nThe writer of scripts.\n" in result.stdout
    )
    assert "Sebastian" not in result.stdout


def test_1():
    result = runner.invoke(mod.app, ["--name", "Camila", "--name", "Sebastian"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output
    assert "Hello Sebastian" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout

"""Utilities that can be used in development. These are not intended for any deployments."""

import shutil
from pathlib import Path


def get_temp() -> Path:
    """Gets the `temp` folder for this project.
    It will be created if it does not exist yet.
    Note that this folder must only be used for development purposes, for deployment use the builtin `tempfile`.
    """
    folder = Path() / "temp"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def clear_temp():
    """Clears all content of this project's `temp` folder."""
    temp = get_temp()
    shutil.rmtree(temp)
    temp.mkdir()

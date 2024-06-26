from enum import Enum, StrEnum
# noinspection PyUnresolvedReferences
from typing import Union, Optional


class ANSI(StrEnum):
    """ANSI color codes."""
    black = "\033[30m",
    red = "\033[31m",
    green = "\033[32m",
    yellow = "\033[33m",
    blue = "\033[34m",
    magenta = "\033[35m",
    cyan = "\033[36m",
    white = "\033[37m",
    bold = "\033[1m",
    underline = "\033[4m"
    reset = "\033[0m"


A = ANSI
"""Shorthand for ANSI color codes enum."""

from enum import StrEnum


class ANSI(StrEnum):
    """ANSI color codes."""

    black = ("\033[30m",)
    red = ("\033[31m",)
    green = ("\033[32m",)
    yellow = ("\033[33m",)
    blue = ("\033[34m",)
    magenta = ("\033[35m",)
    cyan = ("\033[36m",)
    white = ("\033[37m",)
    bold = ("\033[1m",)
    underline = "\033[4m"
    reset = "\033[0m"


A = ANSI
"""Shorthand for ANSI color codes enum."""

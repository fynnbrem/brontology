from typing import Iterable


def is_true_iterable(__v: Iterable | str, /) -> bool:
    """Checks if the value is an actual iterable. This is false for `str` but true for all other iterables."""
    return isinstance(__v, Iterable) and not isinstance(__v, str)
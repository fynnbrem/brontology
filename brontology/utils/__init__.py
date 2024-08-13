from typing import Iterable, TypeVar, Callable

T = TypeVar("T")

def is_true_iterable(__v: Iterable | str, /) -> bool:
    """Checks if the value is an actual iterable. This is false for `str` but true for all other iterables."""
    return isinstance(__v, Iterable) and not isinstance(__v, str)


ROOT = 8206900633647566924
"""The hash value for spaCy's ROOT dep-tag."""


def partition(items: Iterable[T], func: Callable[[T], bool]) -> tuple[list[T], list[T]]:
    """Partitions an iterable into two lists:
    One where the condition of `func` is `true` and a second where it is `false`."""
    true_ = list()
    false_ = list()
    for item in items:
        if func(item):
            true_.append(item)
        else:
            false_.append(item)
    return (true_, false_)
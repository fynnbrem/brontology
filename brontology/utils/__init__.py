from typing import Iterable, TypeVar, Callable, Any, Sequence

T = TypeVar("T")


def is_true_iterable(__v: Iterable | str) -> bool:
    """Checks if the value is an actual iterable.
    This is false for `str` but true for all other iterables."""
    return isinstance(__v, Iterable) and not isinstance(__v, str)


ROOT = 8206900633647566924
"""The hash value for spaCy's ROOT dep-tag."""


def chunk(items: Sequence[T], func: Callable[[T], Any]) -> list[list[T]]:
    """Splits a list of items into sub-lists.
    For every item, the `func` will be evaluated for it and whenever its value changes,
    it will be put into a new sub-list and otherwise in the previous sub-list."""
    if len(items) == 0:
        return list()
    latest_value = func(items[0])
    chunks = [[items[0]]]
    for item in items[1:]:
        new_value = func(item)
        if new_value == latest_value:
            chunks[-1].append(item)
        else:
            latest_value = new_value
            chunks.append([item])
    return chunks


def partition(
    items: Iterable[T], predicate: Callable[[T], bool]
) -> tuple[list[T], list[T]]:
    """Partitions an iterable into two lists:
    One where the condition of `func` is `true` and a second where it is `false`."""
    true_ = list()
    false_ = list()
    for item in items:
        if predicate(item):
            true_.append(item)
        else:
            false_.append(item)
    return (true_, false_)

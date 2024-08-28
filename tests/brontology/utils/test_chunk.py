from typing import Callable, Any

import pytest

from brontology.utils import chunk

_NUMBER_LIST_1 = [1, 2, 3, 4, 5, 6]
_NUMBER_LIST_2 = [1, -1, 2, -2, 3, -3]


def _is_even(x: int):
    return x % 2 == 0


def _in_range(x: int):
    return 3 <= x <= 4


def _square(x: int):
    return x * x


@pytest.mark.parametrize(
    "title, test_input, expected",
    [
        ("single chunk", (_NUMBER_LIST_1, _is_even), [[1], [2], [3], [4], [5], [6]]),
        ("double chunk", (_NUMBER_LIST_1, _in_range), [[1, 2], [3, 4], [5, 6]]),
        ("chunk by non-bool", (_NUMBER_LIST_2, _square), [[1, -1], [2, -2], [3, -3]]),
        ("empty input", ([], lambda _: None), []),
        ("equal eval value", (_NUMBER_LIST_1, lambda _: 1), [_NUMBER_LIST_1]),
    ],
)
def test_chunk(
    title: str,
    test_input: tuple[list[int], Callable[[int], Any]],
    expected: list[list[int]],
):
    values, func = test_input
    resulted = chunk(values, func)
    assert expected == resulted

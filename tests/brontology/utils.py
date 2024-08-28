from typing import Generic, Generator, Any, TypeVar

import pytest

T = TypeVar("T")


class Fixtures(Generic[T]):
    """Fixtures for any test.
    They are defined in the `data` as (nested) dict and can be accessed via `yield_cases`.
    """

    case_type: type
    data: dict

    @staticmethod
    def _iter_dict(
        __d: dict, prev_keys: list[str], ignore_all: bool
    ) -> Generator[tuple[list[str], Any, bool], None, None]:
        """Iterates over a dict that has the shape expected in `data` and yields all cases.
        The yield contains all keys upto that case, the case data itself and whether it is ignored.

        Keys that start with an underscore will count as ignored."""
        for k, v in __d.items():
            ignore_this = k.startswith("_") or ignore_all
            new_keys = prev_keys + [k]
            if isinstance(v, dict):
                for v_ in Fixtures._iter_dict(
                    v, prev_keys=new_keys, ignore_all=ignore_this
                ):
                    yield v_
            else:
                yield (new_keys, v, ignore_this)

    @classmethod
    def yield_cases(cls) -> Generator[tuple[str, T], None, None]:
        """Yields all the cases of the `data` as flat list.
        The first item of the tuple is a title constructed from the keys and the second item the case data.

        Skips keys that begin with an underscore."""
        for (
            keys,
            data,
            ignored,
        ) in Fixtures._iter_dict(cls.data, list(), False):
            # ↓ Do not use the non-ascii arrow here as pytest will encode it.
            if ignored:
                yield pytest.param(" > ".join(keys), data, marks=pytest.mark.xfail)
            else:
                yield pytest.param(" > ".join(keys), data)

"""Functions to help prettifying console outputs.
Functions here are purely for indev uses and should not used to present data to an end user."""

import time
from typing import TypeVar, Iterable

from tqdm import tqdm

Iter = TypeVar("Iter", bound=Iterable)


def get_tqdm(__i: Iter, *, title: str = "", cols: int = 150, title_width=30) -> Iter:
    """Wrapper for `tqdm` with more common parameters."""
    return tqdm(
        __i,
        desc=title.ljust(title_width),
        ncols=cols,
        dynamic_ncols=False,
    )


if __name__ == "__main__":
    for _ in get_tqdm(range(100)):
        time.sleep(0.02)
    for _ in get_tqdm(range(10)):
        time.sleep(0.05)

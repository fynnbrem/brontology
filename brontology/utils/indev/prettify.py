"""Functions to help prettifying console outputs.
Functions here are purely for indev uses and should not used to present data to an end user."""

import time
from typing import TypeVar, Iterable

from spacy.tokens import Span, Token
from tqdm import tqdm

from brontology.utils.indev.color import A

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


def highlight_token_in_span(
    span: Span, tokens: Token | Iterable[Token], style: str = A.bold
) -> str:
    """Highlights all `tokens` with the ANSI `style`"""
    token_texts: list[str] = list()
    for token in span:
        if token in tokens:
            token_texts.append(style)
            token_texts.append(token.text_with_ws)
            token_texts.append(A.reset)
        else:
            token_texts.append(token.text_with_ws)
    text: str = "".join(token_texts)
    return text

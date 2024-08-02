"""Functions to help prettifying console outputs.
Functions here are purely for indev uses and should not used to present data to an end user."""

import time
from typing import Iterable, TypeVar

from spacy.tokens import Span, Token
from tqdm import tqdm

from brontology.utils import is_true_iterable
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


NO_KEY = object()


def _pretty_print_iterable(
        __d: Iterable, /, depth: int = 0, indent: str = "\t"
) -> list[str]:
    """Recursive worker function for `pretty_print_iterable`.

    Details
    =======
    Iterables will be wrapped, while non-iterables will be put into a single line.
    Dicts will have their keys printed as well.
    """
    lines = list()
    if isinstance(__d, dict):
        __d = list(__d.items())
    else:
        __d = [(NO_KEY, v) for v in __d]

    for key, value in __d:
        if key is NO_KEY:
            line = indent * depth
        else:
            line = (indent * depth) + f"{key!r}" + ": "

        if isinstance(value, dict):
            line += "{"
            lines.append(line)
            lines += _pretty_print_iterable(value, depth=depth + 1, indent=indent)
            lines.append((indent * depth) + "},")
        elif is_true_iterable(value):
            if isinstance(value, tuple):
                brackets = "()"
            else:
                brackets = "[]"
            if len(value) == 0:
                line += brackets + ","
                lines.append(line)
            else:
                line += brackets[0]
                lines.append(line)
                lines += _pretty_print_iterable(value, depth=depth + 1, indent=indent)
                lines.append((indent * depth) + brackets[1] + ",")
        else:
            line += str(f"{value!r},")
            lines.append(line)
    return lines


def pretty_print_iterable(
        __d: Iterable, /, indent: str = "  ", do_print: bool = True, init_depth: int = 0
) -> str:
    """Neatly wraps and indents iterables of any depth.

    :param __d:
        The iterable to pretty print.
    :param indent:
        The indent string to be used for every level.
    :param do_print:
        Flag to print the result to console in addition to returning it.
    :param init_depth:
        An initial value for the level of indentation.
    """
    result = "\n".join(_pretty_print_iterable(__d, indent=indent, depth=init_depth))
    if do_print:
        print(result)
    return result

# noinspection PyUnresolvedReferences
from typing import Union, Optional, Iterable

from spacy.tokens import Span, Token

from brontology.utils.color import A


def highlight_token_in_span(span: Span, tokens: Token | Iterable[Token], style: str = A.bold) -> str:
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

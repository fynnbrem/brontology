from dataclasses import dataclass
from typing import Optional, Generator

from spacy.tokens import Token

from brontology.extractor.text_model import Excerpt


def _get_isolated_token(token: Token | None) -> tuple[int, int] | None:
    if token is None:
        return None
    else:
        return (token.lemma, token.pos)


@dataclass(slots=True)
class TokenRelation:
    tail: Optional[Token]
    predicate: Token
    head: Optional[Token]

    source: Excerpt | None = None

    def __str__(self):
        items = [item.lemma_ if item is not None else "???" for item in self]
        return " → ".join(items)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: {str(self)}>"

    def __iter__(self) -> Generator[Token | None, None, None]:
        yield self.tail
        yield self.predicate
        yield self.head

    def __eq__(self, other: "TokenRelation"):
        """Equality is determined by the linguistic content but not the source."""
        if not isinstance(other, TokenRelation):
            return NotImplemented
        return tuple(_get_isolated_token(t) for t in self) == tuple(
            _get_isolated_token(t) for t in other
        )

from dataclasses import dataclass
from typing import Optional

from spacy.tokens import Token

from brontology.extractor.text_model import Excerpt


@dataclass(slots=True)
class TokenRelation:
    tail: Optional[Token]
    predicate: Token
    head: Optional[Token]

    source: Excerpt | None = None

    def __str__(self):
        items = [item.lemma_ if item is not None else "???" for item in self]
        return " → ".join(items)

    def __iter__(self):
        yield self.tail
        yield self.predicate
        yield self.head

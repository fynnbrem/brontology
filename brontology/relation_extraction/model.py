from dataclasses import dataclass

# noinspection PyUnresolvedReferences
from typing import Union, Optional

from spacy.tokens import Token


@dataclass(slots=True)
class TokenRelation:
    tail: Optional[Token]
    predicate: Token
    head: Optional[Token]

    def __str__(self):
        items = [item.lemma_ if item is not None else "???" for item in self]
        return " → ".join(items)

    def __iter__(self):
        yield self.tail
        yield self.predicate
        yield self.head

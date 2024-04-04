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
        items = [
            item.lemma_ if item is not None else "???"
            for item in (self.tail, self.predicate, self.head)
        ]
        return " → ".join(items)

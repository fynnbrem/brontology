from typing import Optional

from spacy.symbols import nsubj
from spacy.tokens import Token

from brontology.relation_extraction.model import TokenRelation


def extract_reflexive_relation(verb: Token) -> Optional[TokenRelation]:
    """Extracts a reflexive relation.
    The created relation will have the same tail as head if any was found."""
    # Determine whether the relation is reflexive by finding a reflexive child.
    is_reflex = False
    for token in verb.children:
        reflex = token.morph.get("Reflex")
        if reflex == ["Yes"]:
            # The head element is the token that the reflexive pronoun belongs to (verb)
            is_reflex = True
            break

    if not is_reflex:
        return None

    # Find the tail of the reflexive relation. In this case the head equals the tail.
    tail: Token | None = None
    for child in verb.children:
        if child.dep == nsubj:
            tail = child
            break

    # If both a reflexive pronoun and a subject are found, create a new TokenRelation
    return TokenRelation(tail, verb, tail)

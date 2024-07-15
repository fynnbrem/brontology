from typing import Optional

from spacy.tokens import Token

from brontology.relation_extraction.model import TokenRelation


def extract_reflexive_relation(verb: Token) -> Optional[TokenRelation]:
    doc = nlp(sentence)

    # Find the head when a reflexive pronoun is found
    head = None
    reflex = None
    for token in doc:
        reflex = token.morph.get("Reflex")
        if reflex == ["Yes"]:
            # The head element is the token that the reflexive pronoun belongs to (verb)
            head = token.head
            break

    # Find the head. It might be headless if it has no nominal subject.
    subject = None
    if head is not None:
        for child in head.children:
            if child.dep_ == "nsubj":
                subject = child
                break

    # If either the subject or the reflexive pronoun is not found, return None
    if subject is None or reflex is None:
        return None

    # If both a reflexive pronoun and a subject are found, create a new TokenRelation
    return TokenRelation(subject, verb, reflex)

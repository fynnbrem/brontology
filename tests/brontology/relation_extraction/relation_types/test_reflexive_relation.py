import spacy
from brontology.relation_extraction.model import TokenRelation

"""from brontology.relation_extraction.relation_types.reflexive_relation import (
    extract_reflexive_relation,
)"""
from spacy.tokens import Token
import en_core_web_trf
from typing import Optional
from spacy.tokens import Token
from typing import Optional

# Lade das Spacy Modell global
nlp = spacy.load("en_core_web_trf")


def extract_reflexive_relation(verb: Token) -> Optional[TokenRelation]:
    sentence = verb.sent.text  # Define sentence based on Verb
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


def test_reflexivepronoun_subject():
    sentence = "I wash myself"
    doc = nlp(sentence)
    verb = None

    # Finde das Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            verb = token
            break

    if verb is None:
        return False

    # Überprüfe die reflexive Relation
    result = extract_reflexive_relation(verb)
    if result is not None and isinstance(result, TokenRelation):
        return True
    else:
        return False


def test_no_reflexive_pronoun():
    sentence = "He washes the car"
    doc = nlp(sentence)
    verb = None

    # Finde das Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            verb = token
            break

    if verb is None:
        return False

    # Überprüfe die reflexive Relation
    result = extract_reflexive_relation(verb)
    if result is not None and isinstance(result, TokenRelation):
        return False
    else:
        return True


def test_no_reflexive_pronoun():
    sentence = "He washes my car"
    doc = nlp(sentence)
    verb = None

    # Finde das Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            verb = token
            break

    if verb is None:
        return False

    # Überprüfe die reflexive Relation
    result = extract_reflexive_relation(verb)
    if result is not None and isinstance(result, TokenRelation):
        return False
    else:
        return True


def test_no_head():
    sentence = "Washing oneself is important."
    doc = nlp(sentence)
    verb = None

    # Finde das Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            verb = token
            break

    if verb is None:
        return False

    # Überprüfe die reflexive Relation
    result = extract_reflexive_relation(verb)
    if result is not None and isinstance(result, TokenRelation):
        return False
    else:
        return True


def test_more_reflexive_pronouns():
    sentence = (
        "We taught ourselves new skills and encouraged each other to keep practicing."
    )
    doc = nlp(sentence)
    verb = None

    # Finde das Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            verb = token
            break

    if verb is None:
        return False

    # Überprüfe die reflexive Relation
    result = extract_reflexive_relation(verb)
    if result is not None and isinstance(result, TokenRelation):
        return True
    else:
        return False


def test_withoutverbs():
    sentence = "The car."
    doc = nlp(sentence)
    verb = None

    # Finde das Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            verb = token
            break

    if verb is None:
        return False

    # Überprüfe die reflexive Relation
    result = extract_reflexive_relation(verb)
    if result is not None and isinstance(result, TokenRelation):
        return False
    else:
        return True


# Beispielaufruf des Tests
result1 = test_reflexivepronoun_subject()
print("Ergebnis von Test 1:", result1)

result2 = test_no_reflexive_pronoun()
print("Ergebnis von Test 2:", result2)

result3 = test_no_head()
print("Ergebnis von Test 3:", result3)

result4 = test_more_reflexive_pronouns()
print("Ergebnis von Test 4:", result4)

result5 = test_withoutverbs()
print("Ergebnis von Test 5:", result5)

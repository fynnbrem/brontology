import en_core_web_trf

from brontology.relation_extraction.delegator import get_main_verbs
from brontology.relation_extraction.model import TokenRelation
from brontology.relation_extraction.relation_types.reflexive_relation import (
    extract_reflexive_relation,
)

nlp = en_core_web_trf.load()


def test_reflexive_pronoun_subject():
    """A reflexive pronoun is extracted properly and has the same head as tail."""
    # Arrange
    sentence = "I wash myself"
    doc = nlp(sentence)
    verb = get_main_verbs(doc)[0]
    # Act
    result = extract_reflexive_relation(verb)
    # Assert
    assert isinstance(result, TokenRelation)
    assert result.head.lemma_ == "I"
    assert result.predicate.lemma_ == "wash"
    assert result.tail == result.head


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

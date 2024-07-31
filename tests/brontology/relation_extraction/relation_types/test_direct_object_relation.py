from dataclasses import dataclass
from typing import Union, Optional
from spacy.tokens import Token, Doc
import en_core_web_trf
import unittest

from brontology.relation_extraction.relation_types.direct_object import (
    extract_direct_object_relation,
)
from brontology.relation_extraction.model import TokenRelation


# testfunctions
def test_verb_dobj_subj():
    nlp = en_core_web_trf.load()
    sentence = "The dog chases the cat."
    doc = nlp(sentence)

    # searching for a verb
    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            if relation is not None:
                return True
            else:
                return False
    return False


def test_checking_correct_tokenrelation():
    nlp = en_core_web_trf.load()

    expected_tail = "dog"
    expected_predicate = "chases"
    expected_head = "cat"

    aktiv = "The dog chases the cat."
    doc: Doc = nlp(aktiv)

    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            if relation:
                tail_text = (
                    relation.tail.text.lower() if relation.tail is not None else "None"
                )
                predicate_text = (
                    relation.predicate.text.lower()
                    if relation.predicate is not None
                    else "None"
                )
                head_text = (
                    relation.head.text.lower() if relation.head is not None else "None"
                )

                if (
                    tail_text == expected_tail
                    and predicate_text == expected_predicate
                    and head_text == expected_head
                ):
                    return True
                else:
                    print(
                        f"Expected Relation: Tail: {expected_tail}, Predicate: {expected_predicate}, Head: {expected_head}"
                    )
                    print(f"Extracted Relation: {relation}")
                    return False
            else:
                print("No direct object relation found.")
                return False


def test_verb_dobj():
    nlp = en_core_web_trf.load()

    sentence = "chases Cat"
    doc = nlp(sentence)

    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            if relation is None:
                return True
            else:
                return False
    return False


def test_subj_verb():
    nlp = en_core_web_trf.load()

    sentence = "The dog chases"
    doc = nlp(sentence)

    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            if relation is None:
                return True
            else:
                return False
    return False


def test_only_verb():
    nlp = en_core_web_trf.load()

    sentence = "catching"
    doc = nlp(sentence)

    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            if relation is None:
                return True
            else:
                return False
    return False


# Calling the test functions
result_test_1 = test_verb_dobj_subj()
print("Ergebnis von Test 1:", result_test_1)

result_test_2 = test_checking_correct_tokenrelation()
print("Ergebnis von Test 2:", result_test_2)

result_test_3 = test_verb_dobj()
print("Ergebnis von Test 3:", result_test_3)

result_test_4 = test_subj_verb()
print("Ergebnis von Test 4:", result_test_4)

result_test_5 = test_only_verb()
print("Ergebnis von Test 5:", result_test_5)

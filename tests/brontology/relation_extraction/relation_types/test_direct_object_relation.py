from dataclasses import dataclass

# noinspection PyUnresolvedReferences
from typing import Union, Optional
from spacy.tokens import Token, Doc
import en_core_web_trf
import unittest

# Funktion zur Extraktion der direkten Objektbeziehung
from brontology.relation_extraction.relation_types.direct_object import (
    extract_direct_object_relation,
)

# import TokenRelation Datenklasse
from brontology.relation_extraction.model import TokenRelation


# Definition der TokenRelation Datenklasse
"""
@dataclass
class TokenRelation:
    subj: Optional[Token]
    verb: Token
    dobj: Optional[Token]

    def __str__(self):
        subj_text = self.subj.text if self.subj is not None else "None"
        dobj_text = self.dobj.text if self.dobj is not None else "None"
        return f"Subj: {subj_text}, Verb: {self.verb.text}, Dobj: {dobj_text}"
"""


# Funktion zur Extraktion der direkten Objektbeziehung
"""
def extract_direct_object_relation(verb):
    # Initialisiere das Subjekt und das direkte Objekt mit "NONE"
    dobj = None
    subj = None

    # Durchlaufe die Kinder des Verbs
    for child in verb.children:
        # Überprüfe, ob die Beziehung ein direktes Objekt ist
        if child.dep_ == "dobj":
            dobj = child
        # Überprüfen, ob die Beziehung ein Subjekt ist
        elif child.dep_ in ["nsubj"]:
            subj = child
    if dobj is None:
        return None
    if subj is None:
        return None
    
    return TokenRelation(subj, verb, dobj)
"""


# Testfunktionen
def test_verb_dobj_subj():
    # Initialisierung des NLP-Modells
    nlp = en_core_web_trf.load()

    # Verarbeitung des Satzes
    sentence = "The dog chases the cat."
    doc = nlp(sentence)

    # Suche nach dem Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            # Überprüfung, ob eine TokenRelation zurückgegeben wird
            if relation is not None:
                return True
            else:
                return False
    # Falls kein Verb gefunden wurde
    return False


def test_checking_correct_tokenrelation():
    # Initialisierung des NLP-Modells
    nlp = en_core_web_trf.load()

    # Erwartete Beziehungen
    expected_subj = "dog"
    expected_verb = "chases"
    expected_dobj = "cat"

    # Verarbeitung des Satzes
    aktiv = "The dog chases the cat."
    doc: Doc = nlp(aktiv)

    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            if relation:
                subj_text = (
                    relation.subj.text.lower() if relation.subj is not None else "None"
                )
                verb_text = (
                    relation.verb.text.lower() if relation.verb is not None else "None"
                )
                dobj_text = (
                    relation.dobj.text.lower() if relation.dobj is not None else "None"
                )

                if (
                    subj_text == expected_subj
                    and verb_text == expected_verb
                    and dobj_text == expected_dobj
                ):
                    return True
                else:
                    print(
                        f"Expected Relation: Subj: {expected_subj}, Verb: {expected_verb}, Dobj: {expected_dobj}"
                    )
                    print(f"Extracted Relation: {relation}")
                    return False
            else:
                print("No direct object relation found.")
                return False


def test_verb_dobj():
    # Initialisierung des NLP-Modells
    nlp = en_core_web_trf.load()

    sentence = "chases Cat"
    doc = nlp(sentence)

    # Suche nach dem Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            # Überprüfung, ob keine TokenRelation zurückgegeben wird
            if relation is None:
                return True
            else:
                return False
    # Falls kein Verb gefunden wurde oder die Relation existiert
    return False


def test_subj_verb():
    # Initialisierung des NLP-Modells
    nlp = en_core_web_trf.load()

    sentence = "The dog chases"
    doc = nlp(sentence)

    # Suche nach dem Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            # Überprüfung, ob keine TokenRelation zurückgegeben wird
            if relation is None:
                return True
            else:
                return False
    # Falls kein Verb gefunden wurde oder die Relation existiert
    return False


def test_only_verb():
    # Initialisierung des NLP-Modells
    nlp = en_core_web_trf.load()

    sentence = "catching"
    doc = nlp(sentence)

    # Suche nach dem Verb im Satz
    for token in doc:
        if token.pos_ == "VERB":
            relation = extract_direct_object_relation(token)
            # Überprüfung, ob keine TokenRelation zurückgegeben wird
            if relation is None:
                return True
            else:
                return False
    # Falls kein Verb gefunden wurde oder die Relation existiert
    return False


# Aufruf der Testfunktionen
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

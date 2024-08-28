"""Utilities for differentiating between passive and active voice."""

from spacy.symbols import auxpass, aux, conj
from spacy.tokens import Token

from brontology.utils.language_utils import has_child


def _is_past_participle(verb: Token) -> bool:
    """Check if the `verb` is in past participle form."""
    return "Tense=Past" in verb.morph and "VerbForm=Part" in verb.morph


def check_passive(verb: Token):
    current_verb = verb
    while True:
        if has_child(current_verb, auxpass):
            return True
        if not _is_past_participle(current_verb):
            return False
        if has_child(current_verb, aux):
            return False
        if current_verb.dep == conj:
            current_verb = current_verb.head
        else:
            return False

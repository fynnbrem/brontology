"""Utilities for differentiating between passive and active voice."""

from spacy.symbols import auxpass, aux, conj
from spacy.tokens import Token

from brontology.utils.language_utils import has_child


def _is_past_participle(verb: Token) -> bool:
    """Check if the `verb` is in past participle form."""
    return "Tense=Past" in verb.morph and "VerbForm=Part" in verb.morph


def check_passive(verb: Token):
    """Checks if the verb is in passive voice."""
    current_verb = verb
    while True:
        # For conjuncts, this needs to check all verbs in the conjunct
        # as only the head verb will have the auxiliary verb.
        # Only one a guarantee for a passive has been found this returns `True`,
        # but it will return `False` if it encounters any non-matching verb before that.
        # Early aborts prevent this verb being associated with a conjunct it is not actually part of,
        # like it can happen in conjuncts of multiple clauses.
        if has_child(current_verb, auxpass):
            # This dep-tag is the only indicator for a passive.
            return True
        if not _is_past_participle(current_verb):
            # Passives are always in past-participle.
            return False
        if has_child(current_verb, aux):
            # If it has an aux verb, this is the leading verb of the conjunct but as it has no passive aux,
            # it cannot be passive.
            return False
        if current_verb.dep == conj:
            # Jump to the previous member of the conjunct if any.
            current_verb = current_verb.head
        else:
            # If this already is the head and itself was not detected as passive, it cannot be a passive.
            return False

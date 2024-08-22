"""Utilities for differentiating between passive and active voice."""

from spacy.symbols import auxpass
from spacy.tokens import Token

from brontology.utils.language_utils import has_child
from brontology.utils.language_utils.conjunct import get_conjunct_head


def check_passive(verb: Token) -> bool:
    """Check if the `verb` is part of a passive voice."""
    return has_child(get_conjunct_head(verb), auxpass)

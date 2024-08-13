"""Utilities that help in language processing. Mostly advanced syntax navigation for spaCy."""
from typing import Iterable, Generator

from spacy.symbols import auxpass, neg
from spacy.symbols import conj, VERB
from spacy.tokens import Token

from brontology.utils.typing import DocSpan


def has_child(token: Token, deps: Iterable[int] | int) -> bool:
    """Checks if any child of `token` has any of the dep-tags in `deps`."""
    if isinstance(deps, int):
        deps = [deps]
    return any((child.dep in deps) for child in token.children)


def get_child(token: Token, deps: Iterable[int] | int) -> Token | None:
    """Returns the first child of the `token` that has any of the dep-tags in `deps`."""
    if isinstance(deps, int):
        deps = [deps]
    try:
        return next(child for child in token.children if child.dep in deps)
    except StopIteration:
        return None


def is_neg(verb: Token) -> bool:
    """Check if the `verb` is negated."""
    return has_child(verb, neg)


def get_conjunct_members(token: Token) -> list[Token]:
    """Gets all members of the conjunct the `token` is the lead verb of.
    This includes the `token` itself.

    :raises ValueError:
        If the token is not the lead verb of the conjunct.
    """
    if token.dep == conj:
        raise ValueError("Can only get conjuncts of the lead verb")
    members = list()
    next_member = token
    while next_member is not None:
        members.append(next_member)
        next_member = get_child(next_member, conj)
    return members


def is_passive(verb: Token) -> bool:
    """Check if the `verb` is part of a passive voice."""
    return has_child(verb, auxpass)


def get_verbs(span: DocSpan) -> Generator[Token, None, None]:
    """Yield all verbs in the `span`.
    Only yields main verbs, not aux verbs."""
    for token in span:
        if token.pos == VERB:
            yield token



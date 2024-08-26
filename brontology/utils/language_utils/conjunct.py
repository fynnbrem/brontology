"""Consistent handling of linguistic conjuncts."""

import logging
from dataclasses import dataclass

from spacy.symbols import conj
from spacy.tokens import Token, Span

from brontology.utils.language_utils import get_child, get_verbs


@dataclass
class Conjunct:
    """Members of a coordinating conjunct."""

    members: tuple[Token, ...]

    def get_members_by_pos(self, *allowed_pos: int):
        """Returns all members that have any of the POS-tags in `allowed_pos`."""
        allowed_pos = set(allowed_pos)
        return [m for m in self.members if m.pos in allowed_pos]

    def __getitem__(self, item):
        return self.members.__getitem__(item)

    def __iter__(self):
        return self.members.__iter__()

    def __len__(self):
        return self.members.__len__()

    @property
    def head(self):
        """The leading token of the conjunct."""
        return self.members[0]

    @property
    def tail(self):
        """The trailing token of the conjunct."""
        return self.members[-1]


def get_verb_conjuncts(span: Span) -> list[Conjunct]:
    """Returns all conjuncts that consist of verbs within the `span`.
    Every `Conjunct` is exclusive."""
    conjuncts: list[Conjunct] = list()
    matched_tokens: set[int] = set()
    for verb in get_verbs(span):
        if verb.i in matched_tokens:
            continue
        try:
            conjunct = get_conjunct_members(verb)
        except ValueError:
            logging.warning("Could not extract a conjunct properly.")
            continue
        for v in conjunct:
            matched_tokens.add(v.i)
        conjuncts.append(conjunct)
    return conjuncts


def get_conjunct_members(token: Token) -> Conjunct:
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
    return Conjunct(tuple(members))


def get_conjunct_head(token: Token) -> Token:
    """Returns the head of the conjunct the `token` is part of.
    This can be the `token` itself it is either the head of the conjunct or not in a conjunct at all.
    """
    if token.dep != conj:
        return token
    else:
        return get_conjunct_head(token.head)

"""Consistent handling of linguistic conjuncts."""

from dataclasses import dataclass

from spacy.symbols import conj
from spacy.tokens import Token

from brontology.utils.language_utils import get_child


@dataclass
class Conjunct:
    """Members of a coordinating conjunct."""

    members: tuple[Token, ...]

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

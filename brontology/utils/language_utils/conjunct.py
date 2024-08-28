"""Consistent handling of linguistic conjuncts."""

from dataclasses import dataclass

from spacy.symbols import conj
from spacy.tokens import Token, Span

from brontology.utils import chunk
from brontology.utils.language_utils import get_child, get_verbs
from brontology.utils.language_utils.voice import check_passive


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


def _partition_verb_conjunct(verbs: list[Token]) -> list[Conjunct]:
    """Partitions verbs within a conjunct by active and passive voice.
    This can break down a large conjunct partially into its nested conjuncts."""
    return [Conjunct(tuple(c)) for c in chunk(verbs, check_passive)]


def get_verb_conjuncts(span: Span) -> list[Conjunct]:
    """Returns all conjuncts that consist of verbs within the `span`.
    Every `Conjunct` is exclusive.
    The conjuncts are split into smaller conjuncts separated by passive/active voice."""
    conjuncts: list[Conjunct] = list()
    matched_tokens: set[int] = set()
    for verb in get_verbs(span):
        if verb.i in matched_tokens:
            continue
        conjunct = get_conjunct_members(verb, allow_non_head=True)
        # ↑ Allow non-head to include conjuncts that are not lead by a verb.
        for v in conjunct:
            matched_tokens.add(v.i)
        sub_conjuncts = _partition_verb_conjunct(list(conjunct))
        for sub_conjunct in sub_conjuncts:
            conjuncts.append(sub_conjunct)
    return conjuncts


def get_conjunct_members(token: Token, *, allow_non_head: bool = False) -> Conjunct:
    """Gets all members of the conjunct the `token` is the lead verb of.
    This includes the `token` itself.

    :param token:
        The token from which to start from.
    :param allow_non_head:
        Flag to allow starting at tokens that are not the head of a conjunct.
        This will yield only the conjunct members after this token.
    :raises ValueError:
        If the token is not the lead verb of the conjunct.
    """
    if token.dep == conj and not allow_non_head:
        raise ValueError("Can only get conjuncts starting at a lead verb")
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

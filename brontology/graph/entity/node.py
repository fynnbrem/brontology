from dataclasses import dataclass
# noinspection PyUnresolvedReferences
from typing import Union, Optional, List, Tuple, Self
from random import choice

from spacy.tokens import Token

from brontology.graph.base.node import Node, Link, NO_CONTENT
from brontology.graph.iterable.node import IterableNode, IterableLink, M


@dataclass(frozen=True, slots=True)
class Lemma:
    """The lemma of a word, including its POS-tag. Should be instantiated via `.from_token`"""
    lemma_: str
    lemma: int
    pos_: str
    pos: int

    @classmethod
    def from_token(cls, token: Token):
        """Instantiate this class from a spacy-token."""
        return cls(
            lemma_=token.lemma_,
            lemma=token.lemma,
            pos_=token.pos_,
            pos=token.pos,
        )

    def __eq__(self, other: Union["Lemma", Token]) -> bool:
        if not isinstance(other, (Lemma, Token)):
            return NotImplemented
        return (self.lemma, self.pos) == (other.lemma, other.pos)

    def __str__(self):
        return '"' + self.lemma_ + '"'


class Synset:
    """A group a similar words, each identified by its `Lemma`."""

    def __init__(self):
        self.members: list[Lemma] = list()

    def __str__(self) -> str:
        """A random word from this synset."""
        if len(self.members) > 0:
            return str(choice(self.members))
        else:
            return "#EMPTY"

    def __contains__(self, item: Lemma | Token):
        return (item in self.members)

    def add_member(self, member: Lemma | Token):
        """Adds a member to this synset. This can be either a `Token` or `Lemma`.
        `Token` will be automatically converted into a `Lemma`."""
        if isinstance(member, Token):
            member = Lemma.from_token(member)
        self.members.append(member)


class Entity(IterableNode["Relation", Synset, Lemma]):
    """An entity of the ontology defined by its synset."""
    synset: Synset

    def __init__(self, content: Synset = NO_CONTENT):
        super().__init__(content=content)
        self.synset = Synset()

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: {str(self.synset)}>"

    @property
    def synset(self):
        """The synset of this entity. Equal to `.content`."""
        return self.content

    @synset.setter
    def synset(self, value):
        self.content = value

    def add_member(self, member: Lemma):
        """Adds the `member` to the synset."""
        self.synset.add_member(member)


class Relation(IterableLink[Entity, Synset, Lemma]):
    """A relation between two entities defined by predicate (expressed as synset).
    Also contains the source if this information."""
    synset: Synset
    source: str

    def __init__(self, head: Entity, tail: Entity, content=NO_CONTENT) -> None:
        super().__init__(head=head, tail=tail, content=content)
        self.synset = Synset()

    def __str__(self):
        items = [
            str(item.synset) if item is not None else "???"
            for item in [self.tail, self, self.tail]
        ]
        return " → ".join(items)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: {str(self)}>"

    @property
    def synset(self):
        """The synset of this relation. Equal to `.content`."""
        return self.content

    @synset.setter
    def synset(self, value):
        self.content = value

    def add_member(self, member: Lemma):
        """Adds the `member` to the synset."""
        self.synset.add_member(member)


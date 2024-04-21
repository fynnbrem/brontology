# noinspection PyUnresolvedReferences
from typing import Union, Optional, List, Tuple
from random import choice
from math import sqrt
from brontology.graph.node import Node, Link

Vector = Tuple[float]

class Synset:
    """A class to represent a Synset (a set of synonyms) in a semantic space."""
    def __init__(self, embeddings: List[Vector]):
        self.embeddings = embeddings
        self.center = self.calculate_center()
        self.repr = self.get_representative_word()

    def calculate_center(self) -> Vector:
        """Calculate the center of the vectors."""
        return tuple(sum(x) / len(x) for x in zip(*self.embeddings))

    def get_representative_word(self) -> str:
        """Select a representative word (in this case, randomly)."""
        return str(choice(self.embeddings))

    def distance(self, other_synset: "Synset") -> float:
        """Calculate the Euclidean distance to another Synset."""
        return sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(self.center, other_synset.center)))


class Entity(Node["Relation"]):
    """An entity of the ontology defined by its synset."""
    synset: Synset


class Relation(Link[Entity]):
    """A relation between two entities defined by predicate (expressed as synset).
    Also contains the source if this information."""
    synset: Synset
    source: str

    def __init__(self, synset: Synset, source: str, head: Entity, tail: Entity) -> None:
        super().__init__(head=head, tail=tail)
        self.synset = synset
        self.source = source

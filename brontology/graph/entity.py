# noinspection PyUnresolvedReferences
from typing import Union, Optional

from brontology.graph.node import Node, Link


class Synset:
    ...


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

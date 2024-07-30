from brontology.graph.entity.node import Entity, Relation, Lemma
from brontology.graph.iterable.graph import IterableGraph
from brontology.relation_extraction.model import TokenRelation


class EntityGraph(IterableGraph[Entity, Relation, Lemma]):
    """A graph that handles `Entity` objects that are connected via `Relation` objects."""

    def __init__(self):
        super().__init__(Entity, Relation)

    def add_token_relation(self, relation: TokenRelation):
        """Isolates the relation from the `TokenRelation` and adds it to this graph."""

        self.add_link_by_member(
            Lemma.from_token(relation.tail),
            Lemma.from_token(relation.predicate),
            Lemma.from_token(relation.head),
        )

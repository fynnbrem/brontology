# noinspection PyUnresolvedReferences
from typing import Union, Optional

from spacy.tokens import Token

from brontology.graph.entity import Entity, Relation
from brontology.graph.node import Link
from brontology.relation_extraction.model import TokenRelation


class Graph:

    def __init__(self):
        self.nodes: list[Entity] = list()

    def add_relation(self, relation: TokenRelation):
        if (relation.head is None or relation.tail is None):
            raise ValueError("Incomplete relations are not supported yet.")

        head_node = self.get_entity(relation.head)
        relation_link: Optional[Relation] = None
        if head_node is not None:
            for incoming_relation in head_node.incoming:
                if (
                        (relation.predicate in incoming_relation.synset) and
                        (relation.tail in incoming_relation.tail.synset)
                ):
                    relation_link = incoming_relation
                    break
        if relation_link is not None:
            return  # The relation already exists, no need for action

        tail_node = self.get_entity(relation.tail)
        # There cannot be a matching relation based on the tail as it would already have been found based on the head.

        if head_node is None:
            head_node = Entity()
            self.nodes.append(head_node)
            head_node.synset.add_member(relation.head)

        if tail_node is None:
            tail_node = Entity()
            self.nodes.append(tail_node)
            tail_node.synset.add_member(relation.tail)

        relation_link = Relation("head", head_node, tail_node)
        relation_link.synset.add_member(relation.predicate)

    def get_entity(self, token: Token) -> Optional[Entity]:
        """Gets the node which contains the `Token`.
        Returns `None` if there is no node with that token yet."""
        for node in self.nodes:
            if token in node.synset:
                return node
        return None

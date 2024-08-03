"""Transferring the internal graph object to the graph database."""

from brontology.database.connector import Connector
from brontology.graph.entity.node import Entity, Relation


def create_entity_node(entity: Entity):
    """Transfers the `entity` to the database."""
    with Connector.driver() as driver:
        driver.execute_query(
            """MERGE (:Entity {name: $name, id: $id})""",
            name=str(entity.synset),
            id=str(entity.id),
        )


def create_entity_relation(relation: Relation):
    """Transfers the `relation` to the database."""
    tail = relation.tail.id
    head = relation.head.id
    sources_formatted = "\n\n".join(
        f"====== Source {i + 1} ======\n\n{s}" for i, s in enumerate(relation.sources)
    )

    with Connector.driver() as driver:
        driver.execute_query(
            """MATCH (t:Entity {id: $tail})
            MATCH (h:Entity {id: $head})
            MERGE (t)-[:VERBS {
                name: $name,
                sources: $sources
            }]->(h)""",
            name=str(relation.synset),
            sources=sources_formatted,
            tail=tail,
            head=head,
        )

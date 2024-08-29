"""Transferring the internal graph object to the graph database."""

from brontology.database.connector import Connector
from brontology.graph.entity.node import Entity, Relation


def create_entity_node(entities: list[Entity]):
    """Transfers the `entity` to the database."""
    if any(e.id is None for e in entities):
        raise ValueError("All entities must have an ID.")
    data = [{"name": str(e.synset), "id": str(e.id)} for e in entities]
    with Connector.driver() as driver:
        driver.execute_query(
            """UNWIND $data AS entity
            MERGE (:Entity {name: entity.name, id: entity.id})""",
            data=data,
        )


def create_entity_relation(relations: list[Relation]):
    """Transfers the `relation` to the database."""

    data = list()
    for relation in relations:
        tail = relation.tail.id
        head = relation.head.id
        sources_formatted = "\n\n".join(
            f"====== Source {i + 1} ======\n\n{s}"
            for i, s in enumerate(relation.sources)
        )
        as_dict = {
            "name": str(relation.synset),
            "sources": sources_formatted,
            "source_count": len(relation.sources),
            "tail": tail,
            "head": head,
        }
        data.append(as_dict)
    with Connector.driver() as driver:
        driver.execute_query(
            """
            UNWIND $data AS relation
            MATCH (t:Entity {id: relation.tail})
            MATCH (h:Entity {id: relation.head})
            MERGE (t)-[:VERBS {
                name: relation.name,
                sources: relation.sources,
                source_count: relation.source_count
            }]->(h)""",
            data=data,
        )

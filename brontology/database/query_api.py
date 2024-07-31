from brontology.database.connector import Connector
from brontology.graph.entity.node import Entity, Relation


def create_entity_node(entity: Entity):
    with Connector.driver() as driver:
        driver.execute_query(
            """MERGE (:Entity {name: $name, id: $id})""",
            name=str(entity.synset),
            id=str(entity.id),
        )


def create_entity_relation(relation: Relation):
    tail = relation.tail.id
    head = relation.head.id
    with Connector.driver() as driver:
        driver.execute_query(
            """MATCH (t:Entity {id: $tail})
            MATCH (h:Entity {id: $head})
            MERGE (t)-[:VERBS {name: $name}]->(h)""",
            name=str(relation.synset),
            tail=tail,
            head=head,
        )


def entity_to_properties(entity: Entity):
    return {
        "name": str(entity.synset),
        "id": str(entity.id),
    }


def relation_to_properties(relation: Relation):
    return {
        "name": str(relation.synset),
    }

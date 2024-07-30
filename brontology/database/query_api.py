from brontology.database.connector import Connector
from brontology.graph.entity.node import Entity, Relation


def create_entity_node(entity: Entity):
    properties = entity_to_properties(entity)
    with Connector.driver() as driver:
        driver.execute_query(f"""CREATE (:Entity $properties)""", properties=properties)


def create_entity_relation(relation: Relation):
    tail = relation.tail.id
    head = relation.head.id
    properties = relation_to_properties(relation)
    with Connector.driver() as driver:
        driver.execute_query(
            """MATCH (t:Entity {id: $tail})
            MATCH (h:Entity {id: $head})
            CREATE (t)-[:VERBS $properties]->(h)""",
            properties=properties,
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

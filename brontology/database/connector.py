"""The connector to the neo4j database."""

import os
from contextlib import contextmanager
from dataclasses import dataclass

from dotenv import load_dotenv
from neo4j import GraphDatabase, Driver

load_dotenv()


@dataclass
class _Connector:
    """Singleton to connect to the neo4j database.
    Use the `.driver` contextmanager to retrieve a driver for this connection."""

    uri: str
    username: str
    password: str

    @contextmanager
    def driver(self) -> Driver:
        """Creates a neo4j driver for this connection."""
        with GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
        ) as driver:
            yield driver

    def reset_database(self):
        """Resets the database:
        - Deletes all nodes and relations
        - Creates basic constraints"""
        with Connector.driver() as driver:
            driver.execute_query("""MATCH (n) DETACH DELETE n;""")
            driver.execute_query(
                """CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE;"""
            )


Connector = _Connector(
    uri=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

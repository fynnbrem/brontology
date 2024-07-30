import os
from contextlib import contextmanager
from dataclasses import dataclass

from dotenv import load_dotenv
from neo4j import GraphDatabase, Driver

load_dotenv()


@dataclass
class _Connector:
    uri: str
    username: str
    password: str

    @contextmanager
    def driver(self) -> Driver:
        with GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
        ) as driver:
            yield driver

    def reset_database(self):
        with Connector.driver() as driver:
            driver.execute_query("""MATCH (n) DETACH DELETE n;""")
            driver.execute_query(
                """CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE"""
            )


Connector = _Connector(
    uri=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

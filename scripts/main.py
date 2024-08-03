from brontology.config import Model
from brontology.database.connector import Connector
from brontology.database.query_api import create_entity_node, create_entity_relation
from brontology.extractor.text_extractor import WikipediaExtractor
from brontology.graph.entity.graph import EntityGraph
from brontology.relation_extraction.delegator import (
    extract_relations_from_text,
)
from brontology.relation_extraction.model import TokenRelation
from brontology.utils.indev.prettify import get_tqdm
from tests.samples.misc import FAKE_LINKS


def is_processable(relation: TokenRelation):
    """Returns `True` if the `TokenRelation` is processable with the current implementation."""
    if relation.tail is None or relation.head is None:
        return False
    return True


if __name__ == "__main__":
    print("Starting")
    graph = EntityGraph()

    nlp = Model.inst
    token_relations: list[TokenRelation] = list()

    for web_link in get_tqdm(FAKE_LINKS[:1], title="Extracting from Text"):
        text = WikipediaExtractor(web_link).extract()
        unfiltered = extract_relations_from_text(text)
        token_relations.extend(filter(is_processable, unfiltered))

    for token_relation in get_tqdm(token_relations, title="Integrating into Graph"):
        graph.add_token_relation(token_relation)

    print("Uploading")
    Connector.reset_database()
    for node in get_tqdm(graph.nodes, title="Uploading Nodes"):
        create_entity_node(node)
    for node_relation in get_tqdm(list(graph.relations), title="Uploading Relations"):
        create_entity_relation(node_relation)

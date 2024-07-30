# noinspection PyUnresolvedReferences
from typing import Union, Optional

from tqdm import tqdm

from brontology.config import Model
from brontology.database.connector import Connector
from brontology.database.query_api import create_entity_node, create_entity_relation
from brontology.extractor.text_extractor import WikipediaExtractor
from brontology.graph.entity.graph import EntityGraph
from brontology.graph.entity.node import Relation
from brontology.relation_extraction.delegator import get_main_verbs, extract_relation
from brontology.relation_extraction.model import TokenRelation
from tests.samples.misc import FAKE_LINKS

if __name__ == "__main__":
    print("Starting")
    graph = EntityGraph()

    nlp = Model.inst
    relations: list[TokenRelation] = list()

    for link in tqdm(FAKE_LINKS, desc="Extracting"):
        text = WikipediaExtractor(link).extract()
        verbs = get_main_verbs(text.doc)

        for verb in verbs:
            try:
                relation = extract_relation(verb)
                if relation.tail is None or relation.head is None:
                    raise ValueError
                relations.append(relation)
            except ValueError:
                ...

        for relation in relations:
            graph.add_token_relation(relation)

    print("Uploading")
    Connector.reset_database()
    for node in tqdm(graph.nodes, desc="Creating Nodes"):
        create_entity_node(node)
    for node in tqdm(graph.nodes, desc="Creating Relations"):
        outgoing: list[Relation] = node.outgoing
        for node_relation in outgoing:
            create_entity_relation(node_relation)

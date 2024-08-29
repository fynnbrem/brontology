from brontology.database.connector import Connector
from brontology.database.query_api import create_entity_node, create_entity_relation
from brontology.extractor.text_extractor import WikipediaExtractor
from brontology.extractor.text_model import Text
from brontology.graph.entity.graph import EntityGraph
from brontology.relation_extraction.extraction_runner import extract_relations_from_text
from brontology.relation_extraction.model import TokenRelation
from brontology.utils.indev.prettify import get_tqdm
from tests.samples.misc import FAKE_LINKS


def is_processable(relation: TokenRelation):
    """Returns `True` if the `TokenRelation` is processable with the current implementation."""
    if relation.tail is None or relation.head is None:
        return False
    return True


if __name__ == "__main__":
    graph = EntityGraph()

    token_relations: list[TokenRelation] = list()
    texts: list[Text] = list()

    for web_link in get_tqdm(FAKE_LINKS, title="Extracting from Web"):
        texts.append(WikipediaExtractor(web_link).extract())

    for text in get_tqdm(texts, title="Parsing Texts"):
        _ = text.doc

    for text in get_tqdm(texts, title="Extracting Relations"):
        unfiltered = extract_relations_from_text(text)
        token_relations.extend(filter(is_processable, unfiltered))

    for token_relation in get_tqdm(token_relations, title="Integrating into Graph"):
        graph.add_token_relation(token_relation)

    print("Uploading")
    Connector.reset_database()
    print("Total Nodes:".ljust(30) + str(len(graph.nodes)))
    create_entity_node(graph.nodes)
    relations = list(graph.relations)
    print("Total Relations:".ljust(30) + str(len(relations)))
    create_entity_relation(list(graph.relations))
    print("All Done")

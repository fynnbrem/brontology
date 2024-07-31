from brontology.config import Model
from brontology.database.connector import Connector
from brontology.database.query_api import create_entity_node, create_entity_relation
from brontology.extractor.text_extractor import WikipediaExtractor
from brontology.graph.entity.graph import EntityGraph
from brontology.relation_extraction.delegator import get_main_verbs, extract_relation
from brontology.relation_extraction.model import TokenRelation
from brontology.utils.indev.prettify import get_tqdm
from tests.samples.misc import FAKE_LINKS


if __name__ == "__main__":
    print("Starting")
    graph = EntityGraph()

    nlp = Model.inst
    relations: list[TokenRelation] = list()

    for link in get_tqdm(FAKE_LINKS, title="Extracting"):
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
    for node in get_tqdm(graph.nodes, title="Creating Nodes"):
        create_entity_node(node)
    for node_relation in get_tqdm(list(graph.relations), title="Creating Relations"):
        create_entity_relation(node_relation)

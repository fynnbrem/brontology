# noinspection PyUnresolvedReferences
from typing import Union, Optional

import en_core_web_trf

from brontology.graph.entity.graph import EntityGraph
from brontology.relation_extraction.delegator import get_main_verbs, extract_relation
from brontology.relation_extraction.model import TokenRelation
from tests.samples.text import SAMPLE_4 as SAMPLE

if __name__ == "__main__":

    graph = EntityGraph()

    nlp = en_core_web_trf.load()
    doc = nlp(SAMPLE)
    verbs = get_main_verbs(doc)

    relations: list[TokenRelation] = list()
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

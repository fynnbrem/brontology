from itertools import product

from spacy.parts_of_speech import PROPN, NOUN, VERB

from brontology.relation_extraction.model import TokenRelation
from brontology.utils.language_utils.conjunct import (
    get_conjunct_members,
    Conjunct,
    get_verb_conjuncts,
)
from brontology.utils.language_utils.participant import get_subj, get_obj
from brontology.utils.language_utils.voice import check_passive
from brontology.utils.typing import DocSpan


def get_relations_from_span(span: DocSpan) -> list[TokenRelation]:
    """Extracts all relation from the `span`."""
    relations: list[TokenRelation] = list()
    for conjunct in get_verb_conjuncts(span):
        relations.extend(get_relations(conjunct))
    return relations


def get_relations(conjunct: Conjunct) -> list[TokenRelation]:
    """Extracts all relations from the `conjunct`.
    This function tries to handle shared subjects/objects between the members
    of the conjunct and create distinct relations accordingly."""
    relations = list()
    is_passive = check_passive(conjunct.head)
    for verb in conjunct.get_members_by_type(VERB):
        subj_token = get_subj(verb, is_passive)
        if subj_token is None:
            subj_token = get_subj(conjunct.head, is_passive)

        obj_token = get_obj(verb, is_passive)
        if obj_token is None:
            obj_token = get_obj(conjunct.tail, is_passive)

        combinations = product(
            (
                get_conjunct_members(subj_token).get_members_by_type(NOUN, PROPN)
                if subj_token is not None
                else [None]
            ),
            [verb],
            (
                get_conjunct_members(obj_token).get_members_by_type(NOUN, PROPN)
                if obj_token is not None
                else [None]
            ),
        )
        for subj_token_, verb_, obj_token_ in combinations:
            if is_passive:
                relation = TokenRelation(obj_token_, verb, subj_token_)
            else:
                relation = TokenRelation(subj_token_, verb, obj_token_)
            relations.append(relation)
    return relations

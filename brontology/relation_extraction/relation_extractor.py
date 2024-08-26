from itertools import product
from typing import Iterable

from spacy.parts_of_speech import PROPN, NOUN, VERB, PRON, ADJ, NUM
from spacy.tokens import Token

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
        relations.extend(_get_relations(conjunct))
    return relations


def _get_conjunct_noun_members(token: Token | None):
    """Gets all members of a noun conjunct. If the `Token` is `None`, this returns a list containing only `None`.
    The members of the conjunct will be filtered to only include valid verb arguments.
    """
    if token is None:
        return [None]
    else:
        return get_conjunct_members(token).get_members_by_pos(
            NOUN, PROPN, NUM, PRON, ADJ
        )
    # TODO: Once the coreference resolution has been implemented, limit this filter to just noun-likes.


def _permutate_relation(
    subj_token: Token | None, verb: Token, obj_token: Token | None
) -> Iterable[tuple[Token | None, Token, Token | None]]:
    """By retrieving the conjuncts of the `subj_token` and the `obj_token`,
    this function will create all permutations of relations this verb has between its tail and head arguments.
    """
    return product(
        _get_conjunct_noun_members(subj_token),
        [verb],
        _get_conjunct_noun_members(obj_token),
    )


def _is_reflexive(token: Token) -> bool:
    """Check if the token is a reflexive pronoun."""
    return token.morph.get("Reflex") == ["Yes"]


def _get_relations(conjunct: Conjunct) -> list[TokenRelation]:
    """Extracts all relations from the `conjunct`.
    This function tries to handle shared subjects/objects between the members
    of the conjunct and create distinct relations accordingly."""
    relations = list()
    is_passive = check_passive(conjunct.head)
    for verb in conjunct.get_members_by_pos(VERB):
        subj_token = get_subj(verb, is_passive)
        if subj_token is None:
            subj_token = get_subj(conjunct.head, is_passive)

        obj_token = get_obj(verb, is_passive)
        if obj_token is None:
            obj_token = get_obj(conjunct.tail, is_passive)

        combinations = _permutate_relation(subj_token, verb, obj_token)
        for subj_token_, verb_, obj_token_ in combinations:
            if obj_token_ is not None and _is_reflexive(obj_token_):
                # If the object is a reflexive pronoun, make the relation reflexive on the subject.
                obj_token_ = subj_token_
            if is_passive:
                relation = TokenRelation(obj_token_, verb, subj_token_)
            else:
                relation = TokenRelation(subj_token_, verb, obj_token_)
            relations.append(relation)
    return relations

from typing import TypeVar, Generic, Generator, Any

import pytest

from brontology.config import Model
from brontology.language_processing.clause_extraction import get_relations_from_span
from brontology.relation_extraction.model import TokenRelation

wolf = "wolf"
bear = "bear"

deer = "deer"
rabbit = "rabbit"
badger = "badger"

chase = "chase"
hunt = "hunt"
track = "track"
eat = "eat"
rest = "rest"

T = TypeVar("T")


class Fixtures(Generic[T]):
    data: dict

    @staticmethod
    def _iter_dict(
        __d: dict, prev_keys: list[str]
    ) -> Generator[tuple[list[str], Any], None, None]:
        """Iterates over a dict that has the shape expected in `data` and yields all cases.
        The yield contains all lists upto that case and the case data itself.

        Skips keys that begin with an underscore."""
        for k, v in __d.items():
            if k.startswith("_"):
                continue
            new_keys = prev_keys + [k]
            if isinstance(v, dict):
                for v_ in Fixtures._iter_dict(v, prev_keys=new_keys):
                    yield v_
            else:
                yield (new_keys, v)

    @classmethod
    def yield_cases(cls) -> Generator[tuple[str, T], None, None]:
        """Yields all the cases of the `data` as flat list.
        The first item of the tuple is a title constructed from the keys and the second item the case data.

        Skips keys that begin with an underscore."""
        for keys, data in Fixtures._iter_dict(cls.data, list()):
            yield (" > ".join(keys), data)
            # ↑ Do not use the non-ascii arrow here as pytest will encode it.


_CASE_TYPE = tuple[str, list[tuple[str | None, str, str | None]]]


class ClauseFixtures(Fixtures[_CASE_TYPE]):
    case_type = _CASE_TYPE

    data: dict[str, dict[str, case_type]] = {
        "non-clause active voice": {
            "one verb": (
                "The wolf chases the deer.",
                [(wolf, chase, deer)],
            ),
            "two verbs": (
                "The wolf chases and hunts the deer.",
                [(wolf, chase, deer), (wolf, hunt, deer)],
            ),
            "two subjects": (
                "The wolf and bear chases the deer.",
                [(wolf, chase, deer), (bear, chase, deer)],
            ),
            "two objects": (
                "The wolf chases the deer and rabbit.",
                [(wolf, chase, deer), (wolf, chase, rabbit)],
            ),
            "all two": (
                "The wolf and bear chase and hunt the deer and rabbit.",
                [
                    (wolf, chase, deer),
                    (wolf, chase, rabbit),
                    (wolf, hunt, deer),
                    (wolf, hunt, rabbit),
                    (bear, chase, deer),
                    (bear, chase, rabbit),
                    (bear, hunt, deer),
                    (bear, hunt, rabbit),
                ],
            ),
        },
        "pure-clause active voice": {
            "distinct objects": (
                "The wolf chases the deer and the bear hunts the rabbit.",
                [(wolf, chase, deer), (bear, hunt, rabbit)],
            ),
            "shared objects": (
                "The wolf chases and the bear hunts the rabbit.",
                [(wolf, chase, rabbit), (bear, hunt, rabbit)],
            ),
        },
        "non-transitive active voice": {
            "no object": (
                "The wolf eats and the bear rests.",
                [(wolf, eat, None), (bear, rest, None)],
            ),
            "object on last": (
                "The wolf eats and the bear hunts the rabbit.",
                [(wolf, eat, rabbit), (bear, hunt, rabbit)],
            ),
            "object on first": (
                "The wolf chases the deer and the bear eats.",
                [(wolf, chase, deer), (bear, eat, None)],
            ),
        },
        "non-clause passive voice": {
            "no actor": (
                "The deer was chased and hunted.",
                [(None, deer, chase), (None, deer, hunt)],
            ),
            "with actor": (
                "The deer was chased and hunted by the wolf.",
                [(wolf, chase, deer), (wolf, hunt, deer)],
            ),
            "two subjects with one actor": (
                "The deer was chased and the rabbit was hunted by the bear.",
                [(bear, chase, deer), (bear, hunt, rabbit)],
            ),
        },
        "pure-clause passive voice": {
            "no actor": (
                "The deer was chased and the rabbit was hunted.",
                [(None, chase, deer), (None, hunt, rabbit)],
            ),
            "actor on first": (
                "The deer was chased by the bear and the rabbit was hunted.",
                [(bear, chase, deer), (None, hunt, rabbit)],
            ),
            "actor on all": (
                "The deer was chased by the wolf and the rabbit was hunted by the bear.",
                [(wolf, chase, deer), (bear, hunt, rabbit)],
            ),
            "actor on middle": (
                "The deer was chased, the rabbit was hunted by the bear and the badger was tracked.",
                [(None, chase, deer), (bear, hunt, rabbit), (None, track, badger)],
            ),
        },
        "_pure-clause mixed voice": {
            "passive last": (
                "The wolf chases the deer and the rabbit was hunted.",
                [(wolf, chase, deer), (None, hunt, rabbit)],
            ),
            "passive first": (
                "The deer was chased and the bear hunts the rabbit.",
                [(None, chase, deer), (bear, hunt, rabbit)],
            ),
            "passive last with actor": (
                "The wolf chases the deer and the rabbit was hunted by the bear.",
                [(wolf, chase, deer), (None, hunt, rabbit)],
            ),
            "passive first with actor": (
                "The deer was chased by the wolf and the bear hunts the rabbit.",
                [(wolf, chase, deer), (bear, hunt, rabbit)],
            ),
            "two passives": (
                "The deer was chased, the badger was tracked and the  the bear hunts the rabbit.",
                [(None, chase, deer), (None, track, badger), (bear, hunt, rabbit)],
            ),
            "two actives": (
                "The deer was chased, the bear hunts the rabbit and the wolf chases the badger.",
                [(None, chase, deer), (bear, hunt, rabbit), (wolf, chase, badger)],
            ),
        },
        "_mixed-clause mixed voice": {
            "two verb passive last place": (
                "The wolf tracks the deer and the rabbit was hunted and chased.",
                [(wolf, track, deer), (None, hunt, rabbit), (None, chase, rabbit)],
            ),
            "two verb passive first place": (
                "The rabbit was hunted and chased and the wolf tracks the deer.",
                [(None, hunt, rabbit), (wolf, track, deer)],
            ),
            "two verb passive with actor": (
                "The rabbit was hunted and chased by the bear and the wolf tracks the deer.",
                [(bear, hunt, rabbit), (bear, chase, rabbit), (wolf, track, deer)],
            ),
            "two verb active first place": (
                "The wolf hunts and chases the deer and the rabbit was tracked.",
                [(wolf, hunt, deer), (wolf, chase, deer), (None, track, rabbit)],
            ),
            "two verb active last place": (
                "The rabbit was tracked and the wolf hunts and chases the deer.",
                [(None, track, rabbit), (wolf, hunt, deer), (wolf, chase, deer)],
            ),
        },
    }


def _compare_to_token_relation(
    lemmas: tuple[str | None, str, str | None], relation: TokenRelation
):
    for lemma, token in zip(lemmas, relation):
        if token is None:
            is_match = lemma == token
        else:
            is_match = lemma == token.lemma_
        if not is_match:
            return False
    return True


def _extract_lemmas(relation: TokenRelation) -> list[str | None]:
    lemmas = list()
    for token in relation:
        if token is None:
            lemmas.append(None)
        else:
            lemmas.append(token.lemma_)
    return lemmas


@pytest.mark.parametrize("title, case", ClauseFixtures.yield_cases())
def test_extract_relation(title: str, case: ClauseFixtures.case_type):
    case_text, case_result = case
    relations = get_relations_from_span(Model.inst(case_text))

    relation_lemmas = {tuple(_extract_lemmas(r)) for r in relations}
    case_result = set(case_result)

    assert relation_lemmas == case_result, title

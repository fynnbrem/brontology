from dataclasses import dataclass

# noinspection PyUnresolvedReferences
from typing import Union, Optional

from spacy.tokens import Span

from brontology.relation_extraction.delegator import get_main_verbs
from brontology.relation_extraction.relation_types.passive_voice import (
    extract_passive_voice_relation,
)
from tests.samples.doc.sentence import Passive


def test_extract_passive_voice_relation():
    """Tests that all passive voice relations are extracted properly."""

    @dataclass
    class TestSet:
        doc: Span
        relation: tuple[Optional[str], str, Optional[str]]

    def _test(test_set: TestSet):
        verb = get_main_verbs(test_set.doc)[0]
        result_relation = extract_passive_voice_relation(verb)

        relation_as_str = tuple(
            token.lemma_ if token is not None else None for token in result_relation
        )
        assert relation_as_str == test_set.relation

    tail = "lumberjack"
    predicate = "fell"
    head = "tree"
    test_sets = [
        TestSet(Passive.default.doc, (tail, predicate, head)),
        TestSet(Passive.auxiliary.doc, (tail, predicate, head)),
        TestSet(Passive.no_actor.doc, (None, predicate, head)),
        TestSet(Passive.preposition.doc, (None, predicate, head)),
    ]
    for _test_set in test_sets:
        _test(_test_set)


if __name__ == "__main__":
    test_extract_passive_voice_relation()

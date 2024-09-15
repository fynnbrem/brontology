"""Tests for passive voice detection."""

import pytest

from brontology.config import Model
from brontology.utils.language_utils import get_verbs
from brontology.utils.language_utils.voice import check_passive
from tests.brontology.testing_utils import Fixtures

chase = "chase"
hunt = "hunt"
follow = "follow"
eat = "eat"


CASE_TYPE = tuple[str, list[tuple[str, bool]]]


class PassiveDetectFixtures(Fixtures[CASE_TYPE]):
    case_type = CASE_TYPE
    data = {
        "passive voice": {
            "past single verb": ("The deer was chased.", [(chase, True)]),
            "past multi verb": (
                "The deer was hunted and chased.",
                [(hunt, True), (chase, True)],
            ),
            "present single verb": ("The deer is chased.", [(chase, True)]),
            "present multi verb": (
                "The deer is hunted and chased.",
                [(hunt, True), (chase, True)],
            ),
            "present perfect single verb": (
                "The deer has been chased.",
                [(chase, True)],
            ),
            "present perfect multi verb": (
                "The deer has been hunted and chased.",
                [(hunt, True), (chase, True)],
            ),
            "multi clause no actor": (
                "The deer was hunted and chased and the rabbit was followed and eaten.",
                [(hunt, True), (chase, True), (follow, True), (eat, True)],
            ),
            "multi clause with actor": (
                "The deer was hunted and chased by the wolf and the rabbit was followed and eaten by the bear.",
                [(hunt, True), (chase, True), (follow, True), (eat, True)],
            ),
        },
        "active voice": {
            "present single verb": ("The wolf hunts the deer.", [(hunt, False)]),
            "present multi verb": (
                "The wolf hunts and chases the deer.",
                [(hunt, False), (chase, False)],
            ),
            "present progressive single verb": (
                "The wolf is hunting the deer.",
                [(hunt, False)],
            ),
            "present progressive multi verb": (
                "The wolf is hunting and chasing the deer.",
                [(hunt, False), (chase, False)],
            ),
            "past progressive single verb": (
                "The wolf was hunting the deer.",
                [(hunt, False)],
            ),
            "past progressive multi verb": (
                "The wolf was hunting and chasing the deer.",
                [(hunt, False), (chase, False)],
            ),
            "present perfect single verb": (
                "The wolf has hunted the deer.",
                [(hunt, False)],
            ),
            "present perfect multi verb": (
                "The wolf has hunted and chased the deer.",
                [(hunt, False), (chase, False)],
            ),
            "multi clause": (
                "The wolf hunts and chases the deer and the bear follows and eats the rabbit.",
                [(hunt, False), (chase, False), (follow, False), (eat, False)],
            ),
        },
        "mixed voice": {
            "passive first single verb": (
                "The deer was hunted and the wolf chases the rabbit.",
                [(hunt, True), (chase, False)],
            ),
            "passive first multi verb": (
                "The deer was hunted and chased, and the wolf follows and eats the rabbit.",
                [(hunt, True), (chase, True), (follow, False), (eat, False)],
            ),
            "active first": (
                "The wolf follows and eats the rabbit and the deer was hunted and chased.",
                [(hunt, True), (chase, True), (follow, False), (eat, False)],
            ),
            "active first past tense": (
                "The deer was hunted and the wolf chased the rabbit.",
                [(hunt, True), (chase, False)],
            ),
            "passive first past tense": (
                "The wolf chased the rabbit and the deer was hunted.",
                [(hunt, True), (chase, False)],
            ),
        },
    }


@pytest.mark.parametrize("title, case", PassiveDetectFixtures.yield_cases())
def test_check_passive(title: str, case: PassiveDetectFixtures.case_type):
    sent, expected = case
    expected = set(expected)
    resulted = set()
    doc = Model.spacy_model(sent)
    for verb in get_verbs(doc):
        resulted.add((verb.lemma_, check_passive(verb)))
    assert expected == resulted, title

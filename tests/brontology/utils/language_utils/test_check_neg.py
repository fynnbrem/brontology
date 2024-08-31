from tests.brontology.testing_utils import Fixtures

chase = "chase"
hunt = "hunt"
follow = "follow"
eat = "eat"


class CheckNegFixtures(Fixtures):
    data = {
        "simplex negative": {
            "present": ("The wolf does not chase the deer.", [(chase, True)]),
            "past": ("The wolf did not chase the deer.", [(chase, True)]),
            "contraction": ("The wolf doesn't chase the deer.", [(chase, True)]),
            "alternate": ("The wolf cannot chase the deer.", [(chase, True)]),
            "modal verb": ("The wolf must not chase the deer.", [(chase, True)]),
            "adverb of frequency": ("The wolf never chases the deer.", [(chase, True)]),
        },
        "simplex non-negative": {
            "present": ("The wolf does chase the deer.", [(chase, False)]),
            "past": ("The wolf did chase the deer.", [(chase, False)]),
            "modal verb": ("The wolf must not chase the deer.", [(chase, False)]),
            "adverb of frequency 1": (
                "The wolf sometimes chases the deer.",
                [(chase, False)],
            ),
            "adverb of frequency 2": (
                "The wolf always chases the deer.",
                [(chase, False)],
            ),
        },
        "1": "The wolf chases the deer and does not hunt the rabbit.",
        "2": "The wolf chases the deer and the bear does not hunt the rabbit",
        "3": "The wolf does not chase and hunt the rabbit.",
    }

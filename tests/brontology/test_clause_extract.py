wolf = "wolf"
bear = "bear"

deer = "deer"
rabbit = "rabbit"

chase = "chase"
hunt = "hunt"
track = "track"
eat = "eat"
rest = "rest"


fixtures = {
    "non-clause active voice": {
        "one verb": (
            "The wolf chases the deer.",
            [[chase]],
        ),
        "two verbs": (
            "The wolf chases and hunts the deer.",
            [[chase, hunt]],
        ),
        "two subjects": (
            "The wolf and bear chases the deer.",
            [[chase]],
        ),
        "two objects": (
            "The wolf chases the deer and rabbit.",
            [[chase]],
        ),
        "all two": (
            "The wolf and bear chase and hunt the deer and rabbit.",
            [[chase, hunt]],
        ),
    },
    "pure-clause active voice": {
        "distinct objects": (
            "The wolf chases the deer and the bear hunts the rabbit.",
            [[chase], [hunt]],
        ),
        "shared objects": (
            "The wolf chases and the bear hunts the rabbit.",
            [[chase], [hunt]],
        ),
    },
    "non-transitive active voice": {
        "no object": (
            "The wolf eats and the bear rests.",
            [[eat], [rest]],
        ),
        "object on last": (
            "The wolf eats and the bear hunts the rabbit.",
            [[eat], [hunt]],
        ),
        "object on first": (
            "The wolf chases the deer and the bear eats.",
            [[chase], [eat]],
        ),
    },
    "non-clause passive voice": {
        "no actor": (
            "The deer was chased and hunted.",
            [[chase, hunt]],
        ),
        "with actor": (
            "The deer was chased and hunted by the wolf.",
            [[chase, hunt]],
        ),
        "two subjects with one actor": (
            "The deer was chased and the rabbit was hunted by the bear.",
            [[chase, hunt]],
        ),
    },
    "pure-clause passive voice": {
        "no actor": (
            "The deer was chased and the rabbit was hunted.",
            [[chase], [hunt]],
        ),
        "actor on first": (
            "The deer was chased by the bear and the rabbit was hunted.",
            [[chase], [hunt]],
        ),
        "actor on all": (
            "The deer was chased by the wolf and the rabbit was hunted by the bear.",
            [[chase], [hunt]],
        ),
        "actor on middle": (
            "The deer was chased, the rabbit was hunted by the bear and the badger was tracked.",
            [[chase], [hunt], [track]],
        ),
        "actor on last": (
            "The deer was chased by the wolf and the rabbit was hunted by the bear.",
            [[chase], [hunt]],
        ),
    },
    "pure-clause mixed voice": {
        "passive last": (
            "The wolf chases the deer and the rabbit was hunted.",
            [[chase], [hunt]],
        ),
        "passive first": (
            "The deer was chased and the bear hunts the rabbit.",
            [[chase], [hunt]],
        ),
    },
    "mixed-clause mixed voice": {
        "two verb passive last place": (
            "The wolf tracks the deer and the rabbit was hunted and chased.",
            [[track], [hunt, chase]],
        ),
        "two verb passive first place": (
            "The rabbit was hunted and chased and the wolf tracks the deer.",
            [[hunt, chase], [track]],
        ),
        "two verb passive with actor": (
            "The rabbit was hunted and chased by the bear and the wolf tracks the deer.",
            [[hunt, chase], [track]],
        ),
        "two verb active first place": (
            "The wolf hunts and chases the deer and the rabbit was tracked.",
            [[hunt, chase], [track]],
        ),
        "two verb active last place": (
            "The rabbit was tracked and the wolf hunts and chases the deer.",
            [[track], [hunt, chase]],
        ),
    },
}

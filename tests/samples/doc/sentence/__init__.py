"""This module contains sample sentences, accessible as `Doc` and `str`."""

from enum import Enum
from pathlib import Path


from typing import Union, Optional, TYPE_CHECKING

from spacy.tokens import Doc

from brontology.utils.spacy import MODEL

BIN_FOLDER = Path(__file__).parent / "bin"
"""The folder where all binary data gets stored."""


class SentenceEnum(Enum):
    """A base class for Enums used to store sentences used as `Doc`.
    Supports lazy loading for the contained `Doc`.

    The `Doc`s get loaded from binary files.
    After creating new sentences, refresh these files with the `create_bin.py`-module.
    """

    _doc: Doc

    @property
    def file(self):
        """The file path of the binary data."""
        return BIN_FOLDER / self.keys[0] / (self.keys[1] + ".bin")

    @property
    def keys(self):
        """The two keys by which this sentence is uniquely identified."""
        return (self.__class__.__qualname__.lower(), self.name.lower())

    @property
    def doc(self):
        """The doc object. Lazy loaded from binary data."""
        try:
            return self._doc
        except AttributeError:
            self._doc = Doc(MODEL.vocab).from_disk(self.file)
            return self.doc


class Passive(SentenceEnum):
    """Passive sentences."""

    default = "The tree was felled by the lumberjack."
    no_actor = "The tree was felled."
    auxiliary = "The tree has been felled by the lumberjack."
    preposition = "The tree has been felled near the ocean."


def construct_minimal_clause(subject: str, verb: str, object_: str):
    """Construct a minimal clause formed just from the subject, verb and object.
    Adds proper casing and a closing dot."""
    return " ".join([subject.capitalize(), verb, (object_ + ".")])


n1 = "monkeys"
n2 = "bananas"
n3 = "trees"
v1 = "eat"
v2 = "climb"
v3 = "need"


class MinimalClause(SentenceEnum):
    """Minimal sentences, consisting just of subject-verb-object."""

    s_1_1_2 = construct_minimal_clause(n1, v1, n2)
    s_2_1_1 = construct_minimal_clause(n2, v1, n1)

"""This module contains sample sentences, accessible as `Doc` and `str`."""
from enum import StrEnum, Enum
from pathlib import Path
# noinspection PyUnresolvedReferences
from typing import Union, Optional, TYPE_CHECKING

from spacy.tokens import Doc

from brontology.utils.spacy import MODEL

BIN_FOLDER = Path(__file__).parent / "bin"
"""The folder where all binary data gets stored."""


class SentenceEnum(Enum):
    """A base class for Enums used to store sentences used as `Doc`.
    Supports lazy loading for the contained `Doc`.

    The `Doc`s get loaded from binary files.
    After creating new sentences, refresh these files with the `create_bin.py`-module."""
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
    default = "The tree was felled by the lumberjack."
    no_actor = "The tree was felled."
    auxiliary = "The tree has been felled by the lumberjack."
    preposition = "The tree has been felled near the ocean."

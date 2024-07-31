"""The data models for extracted text."""

import webbrowser
from dataclasses import dataclass, field
from typing import Union

from spacy.tokens import Doc, Span

from brontology.config import Model


@dataclass
class Text:
    """Test extracted by the extractor. Stores its source, plaintext and spacy doc."""

    plain: str
    source: Union["Source", None] = field(default=None, kw_only=True)

    _doc: Doc | None = field(default=None, init=False)
    """The document generated from the plaintext. Use `.doc` for lazy loaded access."""

    def __post_init__(self):
        self.source.origin = self

    @property
    def doc(self):
        """The spacy doc generated from the plain text. Lazily loaded."""
        if self._doc is None:
            self._doc = Model.inst(self.plain)
        return self._doc


@dataclass
class Excerpt:
    """An excerpt from a document that can be used to display the exact source of some information."""

    origin: Text
    slice: slice

    @property
    def span(self) -> Span:
        """The span of the excerpt."""
        return self.origin.doc[self.slice]

    @property
    def plain(self) -> str:
        """The plaintext of the excerpt."""
        return str(self.span)


@dataclass
class Source:
    """A class that represents the source of a `Text`."""

    link: str
    origin: Text = field(init=False)

    def open(self):
        """Opens the link in the default browser."""
        webbrowser.open(self.link)

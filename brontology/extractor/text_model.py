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
        self.source.text = self

    @property
    def doc(self):
        """The spacy doc generated from the plain text. Lazily loaded."""
        if self._doc is None:
            self._doc = Model.inst(self.plain)
        return self._doc


@dataclass
class Source:
    """A class that represents the source of a `Text`."""

    link: str
    """The hyperlink to the origin website."""
    text: Text = field(init=False)

    def open(self):
        """Opens the link in the default browser."""
        webbrowser.open(self.link)


@dataclass
class Excerpt:
    """An excerpt from a document that can be used to display the exact source of some information."""

    source: Source
    slice: tuple[int, int]

    @property
    def span(self) -> Span:
        """The span of the excerpt."""
        return self.source.text.doc[self.slice[0] : self.slice[1]]

    @property
    def plain(self) -> str:
        """The plaintext of the excerpt."""
        return str(self.span)

    def __str__(self):
        return f"{self.plain}\n\n({self.source.link})"

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: {self.__str__()}>"

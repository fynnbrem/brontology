"""The data models for extracted text."""

import webbrowser
from dataclasses import dataclass, field

from spacy.tokens import Doc, Span

from brontology.config import Model


@dataclass
class Text:
    """Test extracted by the extractor. Stores its source, plaintext and spacy doc."""

    source_link: str
    plain: str

    _doc: Doc | None = field(default=None, init=False)
    """The document generated from the plaintext. Use `.doc` for lazy loaded access."""

    @property
    def doc(self):
        """The spacy doc generated from the plain text. Lazily loaded."""
        if self._doc is None:
            self._doc = Model.inst(self.plain)
        return self._doc

    def open_source(self):
        """Opens the source link in the default browser."""
        webbrowser.open(self.source_link)


@dataclass
class Excerpt:
    """An excerpt from a document that can be used to display the source of some information."""

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

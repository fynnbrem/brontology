import webbrowser
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from spacy.tokens import Doc, Span

from brontology.config import Model


class Text:
    def __init__(self, source: str, content: str):
        self.source_link: str = source
        self.plain: str = content
        self._doc: Doc | None = None

    @property
    def doc(self):
        """The spacy doc generated from the plain text. Lazily loaded."""
        if self._doc is None:
            self._doc = Model.inst(self.plain)
        return self._doc

    def open_source(self):
        """Opens the source link in the default browser."""
        webbrowser.open(self.source_link)


class Excerpt(BaseModel):
    """An excerpt from a document that can be used to display the source of some information."""

    origin: Text
    span_range: slice

    @property
    def span(self) -> Span:
        """The span of the excerpt."""
        return self.origin.doc[self.span_range]

    @property
    def plain(self) -> str:
        """The plaintext of the excerpt."""
        return str(self.span)


class Extractor(ABC):
    @abstractmethod
    def extract(self) -> Text:
        pass


class WikipediaExtractor(Extractor):
    def __init__(self, url: str):
        self.url = url

    def extract(self) -> Text:
        return self._extract_page(self.url)

    def _extract_page(self, url: str) -> Text:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Removes all sup tags containing citations (numbers after text)
        for sup in soup.find_all("sup"):
            sup.decompose()

        content_div = soup.find("div", id="mw-content-text")
        if content_div is not None:
            content = " ".join(p.text for p in content_div.find_all("p"))
        else:
            content = ""

        return Text(url, content)


if __name__ == "__main__":
    extractor = WikipediaExtractor("https://en.wikipedia.org/wiki/Blue_whale")
    text = extractor.extract()
    with open("temp/extracted_texts.py", "w") as file:
        file.write(text.plain)

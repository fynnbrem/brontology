from abc import ABC, abstractmethod

import en_core_web_trf
import requests
from bs4 import BeautifulSoup
from spacy.tokens import Doc


class Text:
    def __init__(self, source: str, content: str):
        self.source: str = source
        self.plain: str = content
        self._doc: Doc | None = None

    @property
    def doc(self):
        if self._doc is None:
            self._doc = en_core_web_trf.load()
        return self._doc


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

from abc import ABC, abstractmethod
from typing import List
from bs4 import BeautifulSoup
import requests
import textwrap

class Extractor(ABC):
    @abstractmethod
    def extract(self):
        pass

class Text:
    def __init__(self, source: str, content: str):
        self.source = source
        self.content = content

class WikipediaExtractor(Extractor):
    def __init__(self, url: str):
        self.url = url

    def extract(self) -> List[Text]:
        return self._extract_page(self.url)

    def _extract_page(self, url: str) -> List[Text]:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Entfernt alle sup-Tags, die Einzelnachweise enthalten (Zahlen hinter Text)
        for sup in soup.find_all('sup'):
            sup.decompose()

        content_div = soup.find('div', id='mw-content-text')
        if content_div is not None:
            content = ' '.join(p.text for p in content_div.find_all('p'))
        else:
            content = ''

        return [Text(url, content)]

extractor = WikipediaExtractor('https://de.wikipedia.org/wiki/Python_(Programmiersprache)')
texts = extractor.extract()

with open('extracted_texts.txt', 'w', encoding='utf-8') as f:
    for text in texts:
        # Text bündig machen
        wrapper = textwrap.TextWrapper(width=120)  # Anpassbare Breite
        bundig_content = wrapper.fill(text.content)
        f.write(f'Source: {text.source}\nContent: {bundig_content}\n\n')
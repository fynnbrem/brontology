from abc import ABC, abstractmethod
from typing import List
from bs4 import BeautifulSoup
import requests

#Alle weiteren Extraktorklassen erben von dieser abstrakten Basisklasse
class Extractor(ABC):
    @abstractmethod
    def extract(self):
        pass

#Repräsentiert ein Textobjekt mit source(URL) und content(der eigentliche Text)
class Text:
    def __init__(self, source: str, content: str):
        self.source = source
        self.content = content

#Extraktor für Wikipedia-Artikel
class WikipediaExtractor(Extractor):
    def __init__(self, url: str, depth: int = 1):
        self.url = url
        self.depth = depth

    def extract(self) -> List[Text]:
        return self._extract_recursive(self.url, self.depth)

    def _extract_recursive(self, url: str, depth: int) -> List[Text]:
        if depth < 0:
            return []

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrahiert nur den Hauptinhalt des Artikels
        content_div = soup.find('div', id='mw-content-text')
        if content_div is not None:
            # Extrahiert alle Absätze und fügt Sie sie zu einem einzigen String zusammen
            content = ' '.join(p.text for p in content_div.find_all('p'))
        else:
            content = ''

        # Erstellt ein Textobjekt mit der URL als Quelle und dem zusammengesetzten String als Inhalt
        texts = [Text(url, content)]

        if depth > 0:
            for link in soup.find_all('a', href=True):
                if link['href'].startswith('/wiki/'):
                    texts.extend(self._extract_recursive('https://en.wikipedia.org' + link['href'], depth - 1))

        return texts

# Erstellt eine Instanz der WikipediaExtractor-Klasse
extractor = WikipediaExtractor('https://de.wikipedia.org/wiki/Python_(Programmiersprache)', 1)

# Ruft die extract-Methode auf, um die Texte zu extrahieren
texts = extractor.extract()

# Öffnet eine Datei zum Schreiben
with open('extracted_texts.txt', 'w', encoding='utf-8') as f:
    # Durchläuft die Liste der extrahierten Texte und schreiben Sie den Inhalt in die Datei
    for text in texts:
        f.write(f'Source: {text.source}\nContent: {text.content}\n\n')
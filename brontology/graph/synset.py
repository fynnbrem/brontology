from typing import List, Tuple
from random import choice
from math import sqrt

Vector = Tuple[float]

class Symbol:
    def __init__(self, embeddings: List[Vector]):
        self.embeddings = embeddings
        self.center = self.calculate_center()
        self.repr = self.get_representative_word()

    def calculate_center(self) -> Vector:
        # Berechnung des Zentrums der Vektoren
        return tuple(sum(x) / len(x) for x in zip(*self.embeddings))

    def get_representative_word(self) -> str:
        # Auswahl eines repräsentativen Wortes (in diesem Fall zufällig)
        return str(choice(self.embeddings))

    def distance(self, other_symbol: "Symbol") -> float:
        # Berechnung der euklidischen Distanz zu einem anderen Symbol
        return sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(self.center, other_symbol.center)))

# Beispielverwendung für calculate_center
vector1 = (1.0, 2.0, 4.0)
vector2 = (4.0, 5.0, 6.0)
symbol = Symbol([vector1, vector2])
center = symbol.calculate_center()
print(f"Center of vectors: {center}")


# Beispielverwendung für get_representative_word
representative_word = symbol.get_representative_word()
print(f"Representative word: {representative_word}")


# Beispielverwendung euklidische Distanz
symbol1 = Symbol([vector1, vector2])
symbol2 = Symbol([(7.0, 8.0, 9.0), (10.0, 11.0, 12.0)])

distance_between_symbols = symbol1.distance(symbol2)
print(f"Distance between symbols: {distance_between_symbols}")
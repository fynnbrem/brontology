"""Global configuration values for this project."""

import spacy
import stanza
from spacy import Language
from stanza import Pipeline

from brontology.language_processing.stanza_to_spacy import merge_stanza_to_spacy
from brontology.utils.typing import Doc


class _Model:
    """Lazy loader for the default language models."""

    type_ = "en_core_web_trf"

    def __init__(self):
        self._spacy_model: Language | None = None
        self._stanza_model: Pipeline | None = None

    def load(self):
        """Explicitly loads the models."""
        # Access the properties to let them load.
        _ = self.spacy_model, self.stanza_model

    @property
    def spacy_model(self) -> Language:
        """The instance of the model. The model will be created here if it does not exist yet."""
        if self._spacy_model is None:
            self._spacy_model = spacy.load(self.type_)
        return self._spacy_model

    @property
    def stanza_model(self) -> Pipeline:
        """The instance of the model. The model will be created here if it does not exist yet."""
        if self._stanza_model is None:
            self._stanza_model = stanza.Pipeline("en", processors="tokenize,coref")
        return self._stanza_model

    def full_parse(self, text: str) -> Doc:
        """Parses the text using both spaCy and stanza.
        :returns:
            The merged spaCy Doc."""
        spacy_doc: Doc = self.spacy_model(text)
        stanza_doc: stanza.Document = self.stanza_model(text)
        merge_stanza_to_spacy(stanza_doc, spacy_doc)
        return spacy_doc


Model = _Model()

if __name__ == "__main__":
    _sents = [
        "The cats were startled by the dog as it growled at them.",
        "John Bauer works at Stanford."
        " He has been there 4 years."
        " Also he likes to sit at the coffe machine, which breaks quite often.",
        "Killer Whales tend to hunt other arctic dolphins."
        " These vivid arctic dolphins often also get hunted by sharks.",
        "The dog chases the cat. They loving playing together.",
        "Ducks and birds are different, but they both are birds.",
        "Alice practiced with her new violin yesterday for the first time."
        " She fell in love with the instrument immediately, it seems like she has finally found the one.",
        "Alice and Bob said they like cheese, but he prefers sushi.",
    ]

    _all_sents = " ".join(_sents)
    _doc = Model.full_parse(_all_sents)

    print("Matched Tokens:")
    for _token in _doc:
        print()
        print([_token.text])
        print([t[1].text for t in _token._.stanza_tokens])

    print()
    print("Corefs:")
    for _coref in _doc._.coref_chains:
        print()
        print("Representative:")
        print(_coref.representative)
        print("Non-Representative:")
        print(*_coref.non_representatives, sep="\n")

import spacy
from spacy import Language


class _Model:
    """Lazy loader for the spacy language model."""

    type_ = "en_core_web_trf"

    def __init__(self):
        self._inst: Language | None = None

    def load(self):
        """Explicitly loads the model."""
        self._inst = spacy.load(self.type_)

    @property
    def inst(self) -> Language:
        """The instance of the model. The model will be created here if it does not exist yet."""
        if self._inst is None:
            self.load()
        return self._inst


Model = _Model()

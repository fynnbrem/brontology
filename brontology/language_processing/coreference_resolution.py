"""The data classes for coreference resolution.
The resolution itself is done implicitly via `stanza` in `stanza_to_spacy.py`."""

from dataclasses import dataclass
from itertools import chain
from typing import Generator, Iterable

from spacy import tokens as spacy
from spacy.tokens import Span
from stanza.models.common import doc as stanza

from brontology.utils.typing import Doc, Token


@dataclass
class CorefChain:
    """A coref chain consisting of its representative and non-representative members."""

    doc: "Doc"
    representative_: tuple[int, int]
    non_representatives_: list[tuple[int, int]]

    def __post_init__(self):
        # Register this coref chain to all contained tokens.
        for token in self.representative:
            token: Token
            token._.coref = CorefAnnotation(True, self)

        for span in self.non_representatives:
            for token in span:
                token: Token
                token._.coref = CorefAnnotation(False, self)

        self.doc._.coref_chains.append(self)

    @property
    def representative(self) -> Span:
        """The representative span for the coref chain."""
        return self.doc[slice(*self.representative_)]

    @property
    def non_representatives(self) -> Generator[Span, None, None]:
        """The non-representative spans of the coref chain."""
        return (self.doc[slice(*r)] for r in self.non_representatives_)

    @property
    def members(self) -> Generator[Span, None, None]:
        """All members (representative and non-representative) of the coref chain."""
        return (m for m in chain([self.representative], self.non_representatives))


@dataclass
class CorefAnnotation:
    """An annotation linking a token to a `CorefChain`.
    This includes the information whether this token is part of the representative span for the entire chain.
    """

    is_representative: bool
    chain: CorefChain


def merge_corefs(stanza_doc: stanza.Document, spacy_doc: Doc):
    """Merges the coreference information from the `stanza_doc` into the `spacy_doc`.
    The data is saved in `Doc._.coref_chains` and `Token._.coref`."""
    # Set up the custom attribute.
    spacy_doc._.coref_chains = list()

    for coref_chain in stanza_doc.coref:
        coref_chain: stanza.CorefChain

        representative: tuple[int, int] | None = None
        non_representatives: list[tuple[int, int]] = list()

        # Find the spacy tokens that match the range defined in the coref mentions.
        for mention_index, mention in enumerate(coref_chain.mentions):
            mention: stanza.CorefMention

            is_representative = mention_index == coref_chain.representative_index
            index_range = (mention.start_word, mention.end_word)

            collected_tokens = _match_tokens_in_stanza_range(
                list(spacy_doc), mention.sentence, index_range
            )

            span = (collected_tokens[0].i, collected_tokens[-1].i + 1)
            if is_representative:
                representative = span
            else:
                non_representatives.append(span)

        if representative is None:
            raise ValueError(
                "Cannot create a `CorefChain` without a representative value."
            )
        # Create the coref chain. It registers itself on the doc and token automatically.
        CorefChain(
            spacy_doc,
            representative_=representative,
            non_representatives_=non_representatives,
        )


def _match_tokens_in_stanza_range(
    tokens: Iterable[spacy.Token], stanza_sentence: int, stanza_range: tuple[int, int]
):
    """Finds all tokens from the `tokens`
    which have a `.stanza_token` of which the index is within the `stanza_range`."""
    collected_tokens = list()
    for spacy_token in tokens:
        spacy_token: Token
        for stanza_index, _ in spacy_token._.stanza_tokens:
            if stanza_index[0] != stanza_sentence:
                continue
            if stanza_range[0] <= stanza_index[1] < stanza_range[1]:
                collected_tokens.append(spacy_token)
                break  # Each token must only be added once.
    return collected_tokens

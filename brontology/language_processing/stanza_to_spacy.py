from typing import Iterator

import stanza.models.common.doc as stanza

from brontology.language_processing.coreference_resolution import merge_corefs
from brontology.utils.typing import Doc, Token


def is_in_char_range(spacy_token: Token, stanza_token: stanza.Token) -> bool:
    """Checks if the `stanza_token` is within the character span of the `spacy_token`.
    If the `spacy_token` is the last token of the doc, this will always be true."""
    try:
        return stanza_token.start_char < spacy_token.nbor().idx
    except IndexError:
        return True


def merge_stanza_to_spacy(stanza_doc: stanza.Document, spacy_doc: Doc) -> None:
    """Merges a stanza `Document` into a spacy `Doc`
    by linking all attributes of the stanza `Document` to custom attributes in the spacy `Doc`.
    This includes document-level information as well as token-level information.

    The spacy `Doc` is modified in-place.

    :raises ValueError:
        When trying to match documents with different source texts.
    """
    if stanza_doc.text != spacy_doc.text:
        raise ValueError("Cannot merge documents with different source texts.")

    spacy_doc._.stanza_doc = stanza_doc
    for token in spacy_doc:
        token: Token
        token._.stanza_tokens = list()

    stanza_tokens_generator: Iterator[tuple[tuple[int, int], stanza.Token]] = (
        ((sent_index, token_index), token)
        for sent_index, sent in enumerate(stanza_doc.sentences)
        for token_index, token in enumerate(sent.tokens)
    )
    stanza_index, stanza_token = next(stanza_tokens_generator)
    try:
        for spacy_token in spacy_doc:
            spacy_token: Token
            while is_in_char_range(spacy_token, stanza_token):
                spacy_token._.stanza_tokens.append((stanza_index, stanza_token))
                stanza_index, stanza_token = next(stanza_tokens_generator)
    except StopIteration:
        ...

    merge_corefs(stanza_doc, spacy_doc)

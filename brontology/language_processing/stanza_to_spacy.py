import spacy.tokens as spacy
import stanza as stanza_core
import stanza.models.common.doc as stanza
from stanza.protobuf import CorefChain

from brontology.config import Model


class Token(spacy.Token):
    class CustomAttrs:
        stanza_tokens: list[stanza.Token] | None
    _: CustomAttrs

class Doc(spacy.Doc):
    class CustomAttrs:
        coref_chains: list[CorefChain] | None
    _: CustomAttrs

spacy.Token.set_extension("stanza_tokens", default=None)
spacy.Doc.set_extension("coref_chains", default=None)



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

    spacy_doc._.coref_chains = stanza_doc.coref
    for token in spacy_doc:
        token._.stanza_tokens = list()

    stanza_tokens_generator = stanza_doc.iter_tokens()
    stanza_token = next(stanza_tokens_generator)
    try:
        for spacy_token in spacy_doc:
            spacy_token: Token
            while is_in_char_range(spacy_token, stanza_token):
                spacy_token._.stanza_tokens.append(stanza_token)
                stanza_token = next(stanza_tokens_generator)
    except StopIteration:
        ...


if __name__ == "__main__":
    _sents = [
        "The cats were startled by the dog as it growled at them.",
        "John Bauer works at Stanford.  He has been there 4 years.",
        "Killer Whales tend to hunt other dolphins. These dolphins often also get hunted by sharks."
    ]

    _all_sents = " ".join(_sents)

    _stanza_nlp = stanza_core.Pipeline("en", processors="tokenize,coref")
    _stanza_doc: stanza.Document = _stanza_nlp(_all_sents)

    _spacy_doc: Doc = Model.inst(_all_sents)

    merge_stanza_to_spacy(_stanza_doc, _spacy_doc)
    for token in _spacy_doc:
        print()
        print([token.text])
        print([t.text for t in token._.stanza_tokens])

from typing import Union, Optional, Callable

from spacy.parts_of_speech import VERB
from spacy.tokens import Span, Token

from brontology.relation_extraction.model import TokenRelation
from brontology.relation_extraction.relation_types.direct_object import (
    extract_direct_object_relation,
)
from brontology.relation_extraction.relation_types.passive_voice import (
    extract_passive_voice_relation,
)
from brontology.utils.color import A

PROCESSORS: list[Callable[[Token], TokenRelation | None]] = list()


def add_processor(processor: Callable[[Token], TokenRelation | None]):
    """Adds `processor` to `PROCESSORS`.
    The processor should take a main verb and return a `TokenRelation`
     if the phrase of the verb matches the type of the processor, or `None` if not."""
    PROCESSORS.append(processor)


def get_main_verbs(span: Span) -> list[Token]:
    """Returns all the main verbs of the `span`."""
    tokens = list()
    for token in span:
        if token.pos == VERB:
            tokens.append(token)
    return tokens


def extract_relation(verb: Token) -> TokenRelation:
    """Extracts the relation formed by the `verb` using the defined `PROCESSORS`."""
    for processor in PROCESSORS:
        relation: Optional[TokenRelation] = processor(verb)
        if relation is not None:
            return relation
    raise ValueError("Could not extract relation.")


add_processor(extract_passive_voice_relation)
add_processor(extract_direct_object_relation)

if __name__ == "__main__":
    from tests.samples.text import SAMPLE_1 as SAMPLE
    import en_core_web_trf
    from brontology.utils.spacy import highlight_token_in_span

    nlp = en_core_web_trf.load()
    doc = nlp(SAMPLE)
    t_verbs = get_main_verbs(doc)

    t_relations: list[TokenRelation] = list()
    for t_verb in t_verbs:
        try:
            t_relations.append(extract_relation(t_verb))
        except ValueError:
            ...
    for t_relation in t_relations:
        text = (
            "Found relation:\n"
            f"{t_relation}\n"
            "From sentence:\n"
            f"{highlight_token_in_span(
                t_relation.predicate.sent, [t_relation.tail, t_relation.predicate, t_relation.head], style=A.blue
            )}\n"
        )
        print(text)

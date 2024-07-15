from typing import Union, Optional

from spacy.symbols import auxpass, agent, nsubjpass, pobj
from spacy.tokens import Token

from brontology.relation_extraction.model import TokenRelation


def extract_passive_voice_relation(verb: Token) -> Optional[TokenRelation]:
    """Extracts a passive voice relation starting on the verb.
    Returns `None` if the verb is no passive voice."""
    if not any(child.dep == auxpass for child in verb.children):
        # Filter: The verb is no passive if it lacks an auxiliary passive verb.
        return None

    # ↓ Find the tail. It might be tailless if it has no agent.
    verb_agent: Optional[Token] = None
    for child in verb.children:
        if child.dep == agent:
            verb_agent = child
            break

    tail: Optional[Token] = None
    if verb_agent is not None:
        for child in verb_agent.children:
            if child.dep == pobj:
                tail = child
                break

    # ↓ Find the head. It might be headless if it has no nominal subject.
    head: Optional[Token] = None
    for child in verb.children:
        if child.dep == nsubjpass:
            head = child
            break

    return TokenRelation(tail, verb, head)

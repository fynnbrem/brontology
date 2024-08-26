from spacy.symbols import (
    nsubjpass,
    csubjpass,
    nsubj,
    csubj,
    agent,
    pobj,
    obj,
    iobj,
    dobj,
)
from spacy.tokens import Token

from brontology.utils.language_utils import get_child


def get_subj(verb: Token, is_passive: bool) -> Token | None:
    """Returns the subject of the `verb`."""
    if is_passive:
        return get_child(verb, [nsubjpass, csubjpass])
    else:
        return get_child(verb, [nsubj, csubj])


def get_obj(verb: Token, is_passive: bool) -> Token | None:
    """Returns the object of the `verb`.

    For passive voice, this is the agent's object.
    """
    if is_passive:
        agent_token = get_child(verb, agent)
        if agent_token is not None:
            return get_child(agent_token, pobj)
        else:
            return None
    else:
        return get_child(verb, [obj, iobj, dobj, pobj])

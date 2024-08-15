from spacy.symbols import (
    conj,
    nsubjpass,
    csubjpass,
    agent,
    pobj,
    nsubj,
    csubj,
    obj,
    iobj,
    dobj,
)
from spacy.tokens import Token

from brontology.utils import partition
from brontology.utils.language_utils import has_child, get_child, is_passive, get_verbs
from brontology.utils.language_utils.conjunct import (
    get_conjunct_members,
    Conjunct,
)
from brontology.utils.typing import DocSpan


def get_clause_verbs(span: DocSpan) -> list[list[Token]]:
    """Gets all clauses in the `span` identified by their verb.
    Verbs without a conjunct are automatically considered a clause.

    Conjuncted verbs that do not each form their own clause are grouped,
    while conjuncted verbs that do form their own clause get separated.

    :returns:
        All groups of verbs, with the first of each group being the leading verb of a conjunct.
    """
    matched_verbs: set[int] = set()
    clause_verbs: list[list[Token]] = list()

    def add_verb_group(g: list[Token]):
        """Adds the group `g` to the matched verbs."""
        clause_verbs.append(g)
        for t in g:
            matched_verbs.add(t.i)

    def add_single_verb(v: Token):
        """Adds the single verb `v` as one-token-group to the matched verbs."""
        clause_verbs.append([v])
        matched_verbs.add(v.i)

    for verb in get_verbs(span):
        if verb.i in matched_verbs:
            continue
        if has_child(verb, conj):
            # Analyze a conjunct on its clause-content.
            # Two cases can occur:
            # - The conjunct consists of clauses.
            #   => The verbs get put into separate groups.
            # - The conjunct does not consist of clauses.
            #   => The verbs get grouped.
            conjunct = get_conjunct_members(verb)
            clauses, verb_group = partition(conjunct[1:], is_clause)
            add_verb_group([verb] + verb_group)
            for clause_verb in clauses:
                add_single_verb(clause_verb)
        else:
            add_single_verb(verb)

    return clause_verbs


def has_subj(verb: Token) -> bool:
    """`True` if the `verb` has a subject, either passive voice or active voice."""
    if is_passive(verb):
        return has_child(verb, [nsubjpass, csubjpass])
    else:
        return has_child(verb, [nsubj, csubj])


def has_active_subj(verb: Token) -> bool:
    return has_child(verb, [nsubj, csubj])


def has_active_obj(verb: Token) -> bool:
    return has_child(verb, [obj, iobj, dobj, pobj])


def has_obj(verb: Token) -> bool:
    """`True` if the `verb` has an object.
    For passive voice, this means that the actor has a pobj."""
    if is_passive(verb):
        agent_token = get_child(verb, agent)
        if agent_token is not None:
            return has_child(agent_token, pobj)
        else:
            return False


def is_single_active_clause(verbs: Conjunct):
    # If there are multiple objects, it must be at least 2 separate clauses.
    return [has_active_obj(v) for v in verbs].count(True) <= 1


def is_clause_conjunct(verbs: Conjunct):
    passives_count = [is_passive(v) for v in verbs].count(True)
    if passives_count == len(verbs):
        all_passive = True
    elif passives_count == 0:
        all_passive = False
    else:
        # The conjunct has mixed voice so it must be different clauses.
        return True


def is_clause(verb: Token) -> bool:
    """Check if the verb forms an entire clause by itself.
    This is only true if it directly links to a subject and object."""
    if is_passive(verb):
        # Passive Verb
        # The object is defined via the actor.
        has_subj = has_child(verb, [nsubjpass, csubjpass])
        agent_token = get_child(verb, agent)
        if agent_token is not None:
            has_obj = has_child(agent_token, pobj)
        else:
            has_obj = False
    else:
        # Active Verb
        has_subj = has_child(verb, [nsubj, csubj])
        has_obj = has_child(verb, [obj, iobj, dobj, pobj])
    return has_subj and has_obj

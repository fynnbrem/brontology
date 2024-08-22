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

from brontology.relation_extraction.model import TokenRelation
from brontology.utils import partition
from brontology.utils.language_utils import (
    has_child,
    get_child,
    get_verbs,
)
from brontology.utils.language_utils.conjunct import (
    get_conjunct_members,
    Conjunct,
    get_verb_conjuncts,
)
from brontology.utils.language_utils.voice import check_passive
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


def get_relations_from_span(span: DocSpan) -> list[TokenRelation]:
    relations: list[TokenRelation] = list()
    for conjunct in get_verb_conjuncts(span):
        relations.extend(get_relations(conjunct))
    return relations


def get_relations(conjunct: Conjunct) -> list[TokenRelation]:
    relations = list()
    is_passive = check_passive(conjunct.head)
    for verb in conjunct:
        subj_token = get_subj(verb, is_passive)
        if subj_token is None:
            get_subj(conjunct.head, is_passive)

        obj_token = get_obj(verb, is_passive)
        if obj_token is None:
            get_obj(conjunct.tail, is_passive)

        if is_passive:
            relation = TokenRelation(obj_token, verb, subj_token)
        else:
            relation = TokenRelation(subj_token, verb, obj_token)
        relations.append(relation)
    return relations

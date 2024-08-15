from itertools import product

from brontology.config import Model
from brontology.language_processing.clause_extraction import get_clause_verbs
from brontology.relation_extraction.model import TokenRelation
from brontology.relation_extraction.relation_types.direct_object import (
    extract_direct_object_relation,
)
from brontology.utils.language_utils.conjunct import get_conjunct_members

doc = Model.inst("The wolf and bear chase and hunt the deer and rabbit.")

clauses = get_clause_verbs(doc)
print(clauses)
for verb_group in clauses:
    base_relation = extract_direct_object_relation(verb_group[0])
    tails = get_conjunct_members(base_relation.tail)
    heads = get_conjunct_members(base_relation.head)
    raw_relations = product(tails, verb_group, heads)
    token_relations = [TokenRelation(t, p, h) for t, p, h in raw_relations]
    print(token_relations)

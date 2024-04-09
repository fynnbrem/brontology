# noinspection PyUnresolvedReferences
from typing import Union, Optional

from brontology.graph.root import Graph
from brontology.relation_extraction.model import TokenRelation
from tests.samples.doc.sentence import MinimalClause

g = Graph()

doc = MinimalClause.a.doc
a_b = TokenRelation(*doc[0:3])
b_c = TokenRelation(*doc[4:7])
c_d = TokenRelation(*doc[8:11])
d_a = TokenRelation(*doc[12:15])

print(a_b, b_c, c_d, d_a, sep=" | ")


g.add_relation(a_b)
g.add_relation(b_c)
g.add_relation(c_d)
g.add_relation(d_a)

print(g.nodes)
print([n.incoming for n in g.nodes])

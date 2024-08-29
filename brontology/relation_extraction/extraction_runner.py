from brontology.extractor.text_model import Text, Excerpt
from brontology.relation_extraction.model import TokenRelation
from brontology.relation_extraction.relation_extractor import get_relations_from_span


def extract_relations_from_text(text: Text) -> list[TokenRelation]:
    """Extracts all relations from a `Text`.
    Only processable relations will be returned."""
    relations = get_relations_from_span(text.doc)
    for relation in relations:
        sent = relation.predicate.sent
        relation.source = Excerpt(source=text.source, slice=(sent.start, sent.end))
    return relations

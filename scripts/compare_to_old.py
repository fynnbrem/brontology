from brontology.extractor.text_extractor import WikipediaExtractor
from brontology.relation_extraction.delegator import extract_relations_from_text
from brontology.relation_extraction.model import TokenRelation
from brontology.relation_extraction.relation_extractor import get_relations_from_span
from brontology.utils.indev.prettify import get_tqdm
from tests.samples.misc import FAKE_LINKS

if __name__ == "__main__":
    old_relations: list[TokenRelation] = list()
    new_relations: list[TokenRelation] = list()
    for web_link in get_tqdm(FAKE_LINKS, title="Extracting from Text"):
        text = WikipediaExtractor(web_link).extract()
        extracted = extract_relations_from_text(text)
        old_relations.extend(extracted)
        extracted = get_relations_from_span(text.doc)
        new_relations.extend(extracted)

    for r in old_relations:
        if r not in new_relations:
            print(r)

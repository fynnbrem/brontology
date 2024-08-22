from typing import Iterable

import spacy.displacy

from brontology.config import Model
from brontology.utils import is_true_iterable
from brontology.utils.indev import get_temp
from brontology.utils.typing import DocSpan

_HTML_BASE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<style>
    body{{font-family: "Segoe UI",sans-serif}}
</style>
<body>
{}
</body>
</html>"""

_ELEMENT_BASE = """
<h3>{}</h3>
<div style="overflow-x: auto">{}</div>
<hr />
"""


def render_in_web(
    docs: Iterable[str | DocSpan] | str | DocSpan, titles: list[str] | None = None
):
    if not is_true_iterable(docs):
        docs = [docs]

    true_docs: list[DocSpan] = list()
    for index, doc in enumerate(docs):
        if isinstance(doc, str):
            doc = Model.inst(doc)
        true_docs.append(doc)
    del docs
    if titles is None:
        true_titles = [str(d) for d in true_docs]
    else:
        true_titles = titles

    def render_(doc_: DocSpan):
        """Creates the SVG for the Doc `doc_`."""
        return spacy.displacy.render(doc_, options={"compact": True}, jupyter=False)

    svgs = [render_(d) for d in true_docs]
    divs = [_ELEMENT_BASE.format(t, s) for t, s in zip(true_titles, svgs, strict=True)]

    html = _HTML_BASE.format("\n".join(divs))
    with open(get_temp() / "render.html", "w") as stream:
        stream.write(html)

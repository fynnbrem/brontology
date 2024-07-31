"""All tests for `Excerpt`."""

from brontology.extractor.text_model import Text, Excerpt, Source
from tests.samples.misc import FAKE_LINK


def test_main():
    """The excerpt has both the proper span and plaintext inferred."""
    text = Text(plain="The cat hunts the mouse vigorously.", source=Source(FAKE_LINK))
    excerpt = Excerpt(slice=slice(1, 5), source=text.source)
    assert excerpt.span == text.doc[1:5]
    assert excerpt.plain == "cat hunts the mouse"

"""All tests for `Excerpt`."""

from brontology.extractor.text_model import Text, Excerpt


def test_main():
    """The excerpt has both the proper span and plaintext inferred."""
    text = Text(plain="The cat hunts the mouse vigorously.")
    excerpt = Excerpt(origin=text, slice=slice(1, 5))
    assert excerpt.span == text.doc[1:5]
    assert excerpt.plain == "cat hunts the mouse"

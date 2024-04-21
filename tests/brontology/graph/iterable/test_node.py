# noinspection PyUnresolvedReferences
from typing import Union, Optional

from brontology.graph.iterable.graph import IterableGraph
from brontology.graph.iterable.node import IterableNode, IterableLink, M


class TestNode(IterableNode["TestLink", list, int]):
    """A node for testing with integer as member type."""

    def __init__(self):
        super().__init__()
        self.content = list()

    def add_member(self, member: int):
        """Appends the member to the content."""
        self.content.append(member)


class TestLink(IterableLink[TestNode, list, int]):
    """A link for testing with integer as member type."""

    def __init__(self, tail: int, head: int):
        super().__init__(tail, head)
        self.content = list()

    def add_member(self, member: int):
        """Appends the member to the content."""
        self.content.append(member)


class TestGraph(IterableGraph[TestNode, TestLink, int]):
    """A Graph that handles integer nodes."""

    def __init__(self):
        super().__init__(TestNode, TestLink)


def test_full_duplicate():
    g = TestGraph()
    link_1 = g.add_link_by_member(1, 2, 3)
    link_2 = g.add_link_by_member(1, 2, 3)
    assert link_1 == link_2, "Expected: Both link objects must be the same as they are duplicates."
    assert (len(link_1.head.incoming) == 1 and len(link_1.tail.outgoing) == 1), \
        "Expected: The nodes must have only one link."


if __name__ == '__main__':
    test_full_duplicate()

from brontology.graph.iterable.graph import IterableGraph
from brontology.graph.iterable.node import IterableNode, IterableLink


class FakeNode(IterableNode["TestLink", list, int]):
    """A node for testing with integer as member type."""

    def __init__(self):
        super().__init__()
        self.content = list()

    def add_member(self, member: int):
        """Appends the member to the content."""
        self.content.append(member)


class FakeLink(IterableLink[FakeNode, list, int]):
    """A link for testing with integer as member type."""

    def __init__(self, tail: int, head: int):
        super().__init__(tail, head)
        self.content = list()

    def add_member(self, member: int):
        """Appends the member to the content."""
        self.content.append(member)


class FakeGraph(IterableGraph[FakeNode, FakeLink, int]):
    """A Graph that handles integer nodes."""

    def __init__(self):
        super().__init__(FakeNode, FakeLink)


def test_no_exist():
    """When neither nodes exist, create a new link and nodes with the defined content."""
    g = FakeGraph()
    link = g.add_link_by_member(1, 2, 3)
    assert link.tail.content == [1]
    assert link.content == [2]
    assert link.head.content == [3]


def test_link_exist():
    """When the link exists but both adjacent nodes do not match, create a new link."""
    g = FakeGraph()
    link_1 = g.add_link_by_member(1, 2, 3)
    link_2 = g.add_link_by_member(4, 2, 6)
    assert link_1 is not link_2


def test_full_duplicate():
    """When the full relation already exists, do not create a new one."""
    g = FakeGraph()
    link_1 = g.add_link_by_member(1, 2, 3)
    link_2 = g.add_link_by_member(1, 2, 3)
    assert (
        link_1 == link_2
    ), "Expected: Both link objects must be the same as they are duplicates."
    assert (
        len(link_1.head.incoming) == 1 and len(link_1.tail.outgoing) == 1
    ), "Expected: The nodes must have only one link."


def test_no_link():
    """When both nodes already exist but the link does not, create just the link."""
    g = FakeGraph()
    node_1 = g.create_node([1])
    node_2 = g.create_node([3])
    link = g.add_link_by_member(1, 2, 3)
    assert node_1 is link.tail, "The node is not properly linked."
    assert node_2 is link.head, "The node is not properly linked."


def test_mirrored_link():
    """When both nodes exist with a link in the other direction, create a new link."""
    g = FakeGraph()
    link_orig = g.add_link_by_member(1, 2, 3)
    link_mirror = g.add_link_by_member(3, 2, 1)
    assert link_orig is not link_mirror, "The links must be different."


def test_no_head():
    """When the head does not exist, create it and the link to it."""
    g = FakeGraph()
    link_1 = g.add_link_by_member(1, 2, 3)
    link_2 = g.add_link_by_member(1, 2, 4)

    assert link_1 is not link_2, "The links must be different."
    assert link_2.head.content == [4]


def test_no_tail():
    """When the tail does not exist, create it and the link to it."""
    g = FakeGraph()
    link_1 = g.add_link_by_member(1, 2, 3)
    link_2 = g.add_link_by_member(4, 2, 3)

    assert link_1 is not link_2, "The links must be different."
    assert link_2.tail.content == [4]


if __name__ == "__main__":
    test_no_exist()
    test_link_exist()
    test_full_duplicate()
    test_no_link()
    test_mirrored_link()
    test_mirrored_link()
    test_no_head()
    test_no_tail()

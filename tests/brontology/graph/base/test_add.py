from brontology.graph.base.node import Node, Link


def test_add_link() -> None:
    """Creates a link and tests that the link is properly registered on both nodes."""
    node_1: Node = Node()
    node_2: Node = Node()
    link: Link = Link(node_1, node_2)

    assert link in node_1.outgoing
    assert link in node_2.incoming

    assert link not in node_1.incoming
    assert link not in node_2.outgoing


def test_add_incoming() -> None:
    """Adds an incoming link to a node, expecting it no be registered on that node."""
    node: Node = Node()
    link: Link = Link(Node(), Node())

    node.add_incoming(link)
    assert link in node.incoming


def test_add_outgoing() -> None:
    """Adds an outgoing link to a node, expecting it no be registered on that node."""
    node: Node = Node()
    link: Link = Link(Node(), Node())
    node.add_outgoing(link)
    assert link in node.outgoing


def test_switch_link_head() -> None:
    """Creates a link and later links it to a different node, expecting its head to switch."""
    node_1: Node = Node()
    node_2: Node = Node()
    link: Link = Link(Node(), Node())

    assert link.head is not node_1
    node_1.add_incoming(link)
    assert link.head is node_1
    node_2.add_incoming(link)
    assert link.head is node_2


def test_switch_link_tail() -> None:
    """Creates a link and later links it to a different node, expecting its tail to switch."""
    node_1: Node = Node()
    node_2: Node = Node()
    link: Link = Link(Node(), Node())

    assert link.tail is not node_1
    node_1.add_outgoing(link)
    assert link.tail is node_1
    node_2.add_outgoing(link)
    assert link.tail is node_2


if __name__ == "__main__":
    test_add_link()
    test_add_incoming()
    test_add_outgoing()
    test_switch_link_head()
    test_switch_link_tail()

from itertools import chain
# noinspection PyUnresolvedReferences
from typing import Union, Optional

from brontology.graph.base.node import Node, Link


def test_remove_link() -> None:
    """Removes an existing link and expects it to disappear from any connected nodes."""
    node_1: Node = Node()
    node_2: Node = Node()
    link: Link = Link(node_1, node_2)

    link.remove()
    assert link not in chain(node_1.incoming, node_1.outgoing)
    assert link not in chain(node_2.incoming, node_2.outgoing)


def test_remove_incoming() -> None:
    """Removes an incoming link from a specific node."""
    node: Node = Node()
    link: Link = Link(Node(), node)

    node.remove_incoming(link)
    assert link not in node.incoming
    try:
        link.head
    except AttributeError:
        ...
    else:
        raise AssertionError()


def test_remove_outgoing() -> None:
    """Removes an outgoing link from a specific node."""
    node: Node = Node()
    link: Link = Link(node, Node())

    node.remove_outgoing(link)
    assert link not in node.outgoing
    try:
        link.tail
    except AttributeError:
        ...
    else:
        raise AssertionError()


def test_remove_nonexistent() -> None:
    """Tries to remove a link from a node that is node connected to that node."""
    node: Node = Node()
    link: Link = Link(Node(), Node())
    try:
        node.remove_incoming(link)
    except ValueError:
        ...
    else:
        raise AssertionError()
    try:
        node.remove_outgoing(link)
    except ValueError:
        ...
    else:
        raise AssertionError()


if __name__ == '__main__':
    test_remove_link()
    test_remove_incoming()
    test_remove_outgoing()
    test_remove_nonexistent()

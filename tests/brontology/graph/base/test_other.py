from typing import Union, Optional

from brontology.graph.base.node import Node, Link


def test_incoming_nodes() -> None:
    node: Node = Node()
    neighbours: list[Node] = [Node() for _ in range(3)]

    for neighbour in neighbours:
        Link(neighbour, node)

    assert all(neighbour in node.tail_nodes for neighbour in neighbours)


def test_outgoing_nodes() -> None:
    node: Node = Node()
    neighbours: list[Node] = [Node() for _ in range(3)]

    for neighbour in neighbours:
        Link(node, neighbour)

    assert all(neighbour in node.head_nodes for neighbour in neighbours)


if __name__ == "__main__":
    test_incoming_nodes()
    test_outgoing_nodes()

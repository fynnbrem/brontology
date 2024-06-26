# noinspection PyUnresolvedReferences
from typing import Union, Optional, TypeVar, Generic, Self

L = TypeVar("L", bound="Link")


class Node(Generic[L]):
    """A graph node. Defined by its incoming and outgoing links."""

    def __init__(self) -> None:
        self._incoming: list[L] = list()
        self._outgoing: list[L] = list()

    @property
    def incoming(self) -> tuple[L, ...]:
        """The links pointing to this node.
        To modify, use `add_incoming()` or `remove_incoming()`."""
        return tuple(self._incoming)

    @property
    def outgoing(self) -> tuple[L, ...]:
        """The links pointing away from this node.
        To modify, use `add_outgoing()` or `remove_outgoing()`."""
        return tuple(self._outgoing)

    @property
    def incoming_nodes(self) -> tuple[Self, ...]:
        """The nodes that have links pointing to this node."""
        return tuple(link.tail for link in self.incoming)

    @property
    def outgoing_nodes(self) -> tuple[Self, ...]:
        """The nodes that this node's links point to."""
        return tuple(link.head for link in self.outgoing)

    def add_incoming(self, link: L) -> None:
        """Adds a link to this node's incoming links. Also sets the `head` of the link to this node."""
        self._incoming.append(link)
        link.head = self

    def add_outgoing(self, link: L) -> None:
        """Adds a link to this node's outgoing links. Also sets the `tail` of the link to this node."""
        self._outgoing.append(link)
        link.tail = self

    def remove_incoming(self, link: L) -> None:
        """Removes a link from this node's incoming links. Also deletes the `head` of the link.
        :raises ValueError:
            When the `link` is not connected to this node."""
        self._incoming.remove(link)
        del link.head

    def remove_outgoing(self, link: L) -> None:
        """Removes a link from this node's outgoing links. Also deletes the `tail` of the link.
        :raises ValueError:
            When the `link` is not connected to this node."""
        self._outgoing.remove(link)
        del link.tail


N = TypeVar("N", bound=Node)


class Link(Generic[N]):
    """A link between two nodes.
    :param head:
        The node this link points to. This link will be registered on that node.
    :param tail:
        The node this link comes from. This link will be registered on that node."""
    head: N
    """The node this link points to."""
    tail: N
    """The node this link comes from."""

    def __init__(self, tail: N, head: N) -> None:
        tail.add_outgoing(self)
        head.add_incoming(self)

    def remove(self) -> None:
        """Removes this link by removing it from both connected nodes."""
        self.head.remove_incoming(self)
        self.tail.remove_outgoing(self)

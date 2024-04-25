# noinspection PyUnresolvedReferences
from typing import Union, Optional, TypeVar, Generic, Self, Iterable

L = TypeVar("L", bound="Link")
C = TypeVar("C")

NO_CONTENT = object()


class Node(Generic[L, C]):
    """A graph node. Defined by its incoming and outgoing links."""

    content: C

    def __init__(self, content: C = NO_CONTENT) -> None:
        if content is not NO_CONTENT:
            self.content = content
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
    def tail_nodes(self) -> tuple[Self, ...]:
        """The nodes that have links pointing to this node."""
        return tuple(link.tail for link in self.incoming)

    @property
    def head_nodes(self) -> tuple[Self, ...]:
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


class Link(Generic[N, C]):
    """A link between two nodes.
    :param head:
        The node this link points to. This link will be registered on that node.
    :param tail:
        The node this link comes from. This link will be registered on that node."""
    head: N
    """The node this link points to."""
    tail: N
    """The node this link comes from."""

    content: C

    def __init__(self, tail: N, head: N, content: C = NO_CONTENT) -> None:
        if content is not NO_CONTENT:
            self.content = content
        tail.add_outgoing(self)
        head.add_incoming(self)

    def remove(self) -> None:
        """Removes this link by removing it from both connected nodes."""
        self.head.remove_incoming(self)
        self.tail.remove_outgoing(self)

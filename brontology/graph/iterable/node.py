# noinspection PyUnresolvedReferences
from typing import Union, Optional, TypeVar, Iterable, Generic

from brontology.graph.base.node import Node, Link

L = TypeVar("L", bound="Link")
C = TypeVar("C", bound=Iterable)
M = TypeVar("M")


class IterableNode(Generic[L, C, M], Node[L, C]):
    """A graph node. Defined by its incoming and outgoing links and its content.
    The content is an iterable `C` of which the members have the type `I`."""

    content: C

    def add_member(self, member: M):
        """Adds a member to the content. Abstract method, Must be implemented for the specific data type."""
        raise NotImplementedError


class IterableLink(Generic[L, C, M], Link[L, C]):
    """A graph link. Defined by its head and tail nodes and its content.
    The content is an iterable `C` of which the members have the type `I`."""

    content: C

    def add_member(self, member: M):
        """Adds a member to the content. Abstract method, must be implemented for the specific data type."""
        raise NotImplementedError

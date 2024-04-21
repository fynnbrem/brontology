# noinspection PyUnresolvedReferences
from typing import Union, Optional, TypeVar, Iterable, Generic, Type

from brontology.graph.base.node import NO_CONTENT
from brontology.graph.iterable.node import IterableNode, IterableLink, C

L = TypeVar("L", bound=IterableLink)
N = TypeVar("N", bound=IterableNode)
M = TypeVar("M")


class IterableGraph(Generic[N, L, M]):
    """Generic:
    N = node_type
    L = link_type
    M = type of members of node_type and link_type

    Constructor:
    node_type/link_type: The actual types used to instantiate the objects. Must be the same as specified in the generic.
    """

    def __init__(self, node_type: Type[N], link_type: Type[L]):
        self.node_type = node_type
        self.link_type = link_type

        self.nodes: list[C] = list()
        self.links: list[L] = list()

    def add_link_by_member(self, tail: M, link: M, head: M) -> L:
        """Adds a link to graph defined by the head, link and tail members.
        If there already exists an equal link, do not create a new one.

        Otherwise, connect the nodes that contain the head and tail members with a new link.
        The nodes will also be created if they do not exist yet, with the single member as their content.

        In any case, returns the link object.
        """
        # region: Find an existing link by starting from the tail.
        # First find the node matching the tail, then try to find a matching outgoing link.
        tail_node = self.get_node_by_member(tail)
        relation_link: Optional[L] = None
        if tail_node is not None:
            for outgoing_relation in tail_node.outgoing:
                if (
                        (link in outgoing_relation.content) and
                        (head in outgoing_relation.head.content)
                ):
                    relation_link = outgoing_relation
                    break
        # endregion
        if relation_link is not None:
            return relation_link  # The relation already exists, no need for action

        # region: Find a tail node.
        # In contrast to the head,
        # do not try to find a matching incoming link as it would have already been found above.
        head_node = self.get_node_by_member(tail)
        # endregion

        # region: Create missing nodes.
        if tail_node is None:
            tail_node = self.create_node([tail])

        if head_node is None:
            head_node = self.create_node([head])
        # endregion

        # region: Create the new link.
        relation_link = self.link_type(tail_node, head_node)
        relation_link.add_member(link)
        # endregion
        return relation_link

    def create_node(self, members: Iterable[M]):
        """Creates a new node with the members in this graph.
        Returns the newly created node.

        This does not check for duplicates."""
        node = self.node_type()
        self.nodes.append(node)
        for member in members:
            node.add_member(member)
        return node

    def get_node_by_member(self, member: M) -> Optional[N]:
        """Gets the node which contains the `member`.
        Returns `None` if there is no node with that member."""
        for node in self.nodes:
            if member in node.content:
                return node
        return None

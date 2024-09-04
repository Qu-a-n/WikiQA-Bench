from typing import Union


class Node:  # v
    def __init__(
        self,
        task,
        answer=None,
    ):
        self.task = task
        self.answer = answer
        self.group = []
        self.children = []

    def add_child(self, group: "Group"):
        self.children.append(group)

    def join_group(self, group: "Group"):
        self.group.append(group)


class Group:  # {v}
    def __init__(
        self,
        parent: Node,
        nodes: list,
        predecessors: list,
    ):
        self.parent = parent
        self.nodes = nodes
        self.predecessors = predecessors


class Graph:  # V, E

    def __init__(self, nodes: list = [], groups: list = []):
        self.nodes = nodes
        self.groups = groups

    def add_node(self, node: Union[Node, list]):
        if isinstance(node, Node):
            self.nodes.append(node)
        elif isinstance(node, list):
            self.nodes.extend(node)

    def add_group(self, group: Union[Group, list]):
        if isinstance(group, Group):
            self.groups.append(group)
        elif isinstance(group, list):
            self.groups.extend(group)

    def remove_node(self, node: Union[Node, list]):
        if isinstance(node, Node):
            self.nodes.remove(node)
        elif isinstance(node, list):
            for n in node:
                if isinstance(n, Node):
                    self.nodes.remove(n)

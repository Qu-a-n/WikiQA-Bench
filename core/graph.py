import json
from enum import Enum
from typing import Union
from core.visualize import Plotter
from core.models import gen_embedding, cosine_similarity


class Mode(Enum):
    frozen = "frozen"  # action被拒绝或者存在error，style="filled"
    finished = "finished"  # 直接得到解决，或者至少有一个子任务组得到解决，style="solid"
    waiting = "waiting"  # 存在子任务组，且所有子任务组均没有得到解决，style="dashed"
    pending = "pending"  # 不存在子任务组，可以直接执行


class Relation(Enum):
    upstream = "<-"  # 依赖关系
    downstream = "->"  # 被依赖关系
    duplicated = "="  # 重复关系
    unrelevant = "|"  # 没有关系


def checkMode(input_str, enum: Enum):
    for e in enum:
        if input_str == e.value:
            return e.value
    return None


class Node:  # v
    def __init__(
        self,
        state,
        mode: Mode = Mode.pending,
        style=None,
    ):
        self._state = state
        self.mode = mode
        self.parent = []
        self.children = []
        self.upstream = []
        self.downstream = []
        # self.action = dict()
        # self.thought = []
        self.style = style
        # self.memory = ""
        self.embedding = gen_embedding([state])[0]

    @property
    def state(self):
        return self._state  # 当获取state属性时，返回内部_state的值

    @state.setter
    def state(self, value):
        self._state = value  # 设置_state属性的值
        self.change_embedding()  # 每次_state改变时，修改embedding

    def change_embedding(self):
        self.embedding = gen_embedding([self.state])[0]

    def update(self, state=None, mode: Mode = None, style=None):
        self.state = state if state else self.state
        self.mode = mode if mode else self.mode
        self.style = style if style else self.style

    def add_children(self, nodes: list):
        if isinstance(nodes, list):
            self.children.append(nodes)
        else:
            raise TypeError

    def add_downstream(self, nodes, transformation=None):
        if isinstance(nodes, Node):
            node = nodes
            self.downstream.append(node)
            # if transformation:
            #     self.action[node.state] = transformation
        elif isinstance(nodes, list):
            for node in nodes:
                self.downstream.append(node)
                # if transformation:
                #     self.action[node.state] = transformation
        else:
            raise TypeError


class Graph:  # V, E

    def __init__(self, question, groundtruth=None, dataname=None, id=0):
        self.question = question
        self.groundtruth = groundtruth
        self.dataname = dataname if dataname else "example"  # 用于保存图片的文件夹名
        self.id = id  # 在dataset里的idx编号
        self.nodes = []
        self.timestamp = 0  # 用于保存图片的文件名
        self.root = None

    def add_node(self, node: Union[Node, list]):
        if isinstance(node, Node):
            self.nodes.append(node)
        elif isinstance(node, list):
            self.nodes.extend(node)

    def remove_node(self, node: Union[Node, list]):
        if isinstance(node, Node):
            self.nodes.remove(node)
        elif isinstance(node, list):
            for n in node:
                if isinstance(n, Node):
                    self.nodes.remove(n)

    # def find(self, value, key: str = "state"):
    #     for node in self.nodes:
    #         if key == "state":
    #             if sorted(node.state.split(" ")) == sorted(value.split(" ")):
    #                 return node
    #         if getattr(node, key) == value:
    #             return node
    #     return None

    def find(self, value, key: str = "state"):  # 贪心向量匹配
        for node in self.nodes:
            candidate = getattr(node, key)
            if cosine_similarity(candidate, value) > 0.99:
                return node

    def plot(self, propagation=None):
        plotter = Plotter("img/{}/experiment{}".format(self.dataname, self.id))
        for node in self.nodes:
            if node.style == None:
                if node.mode == Mode.finished:
                    node.style = "solid"  # 已完成的节点画实线
                elif node.mode == Mode.frozen:
                    node.style = "filled"  # 被拒绝的节点画灰
                else:
                    node.style = "dashed" or node.mode == Mode.pending  # 未完成的画虚线
            plotter.add_node(node.state, style=node.style)
            for children in node.children:
                for c in children:
                    plotter.add_edge(node.state, c.state, style="solid")
                plotter.add_cluster([c.state for c in children])
            for d in node.downstream:
                plotter.add_edge(node.state, d.state, style="dashed")
        if propagation:  # 回传边
            plotter.add_edge(
                propagation[0].state, propagation[1].state, style="tapered"
            )
        plotter.plot_graph(self.timestamp)
        self.timestamp += 1

    def to_json(self):
        root = self.nodes[0]
        # 先把root写进json
        graph_data = [
            {
                "task_id": root.state,
                "task_description": "",
                "children": [],
                "upstream": [],
                "downstream": []
            }
        ]
        return json.dumps(graph_data, indent=2)

from abc import ABC


class Decompose(ABC):
    def __init__(self):
        pass

    def decompose(self):
        pass


class Action(ABC):
    def __init__(self):
        pass

    def merge(self):
        pass

    def conclude(self):
        pass


class Complete(ABC):
    def __init__(self):
        pass

    def judge(self):
        pass


class Controller(ABC):
    def __init__(self, expander, aggregator=None, adjustor=None):
        self.graph = None
        self.expander = expander
        self.aggregator = aggregator
        self.adjustor = adjustor
        pass

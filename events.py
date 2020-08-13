from abc import ABC, abstractmethod
from typing import List


class Event(ABC):
    pass


class AddLink(Event):
    def __init__(self, node1: str, node2: str, signal: str, comment: str = ""):
        self.node1 = node1
        self.node2 = node2
        self.signal = signal
        self.comment = comment


class SelectSignal(Event):
    def __init__(self, signal_name: str):
        self.signal_name = signal_name


class SelectLink(Event):
    def __init__(self, sel_list: List[int]):
        self.sel_list = sel_list


class RemLink(Event):
    pass




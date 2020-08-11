# from __future__ import annotations

from pip.index import Link


class Link():
    def __init__(self, node1: str, node2: str, signal: str = "", comment: str = ""):
        self.node1 = node1
        self.node2 = node2
        self.signal = signal
        self.comment = comment

    def __str__(self):
        return f"n1: {self.node1}  n2: {self.node2}  signal: {self.signal}"

    def __eq__(self, other: Link):
        if ((other.node1 == self.node1 and other.node2 == self.node2) or (
                other.node2 == self.node1 and other.node1 == self.node2)):
            return True
        else:
            return False


class DLink(Link):
    pass


if __name__ == "__main__":
    print(Link("2", "1") == Link("2", "1"))
    print(isinstance(DLink("2", "1"), Link))

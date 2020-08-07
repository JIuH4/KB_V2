import enum
from abc import ABC, abstractmethod
from typing import List
from Link import Link


class Port(enum.Enum):
    m1_50 = 0
    m51_100 = 1
    m101_150 = 2
    m151_200 = 3
    m1_100 = 4
    m101_200 = 5
    barewire = 6


class Module(ABC):
    def __init__(self, port: Port = Port.barewire):
        self.nodes = []
        self.add_nodes()
        self.port: Port = port

    @abstractmethod
    def add_nodes(self):
        pass

    def __eq__(self, other):

        if self.port == other.port and self.__class__.__name__ == other.__class__.__name__:
            return True
        else:
            return False

    def check_node(self, node):
        if node in self.nodes:
            return True
        else:
            return False


class Pxi2568(Module):
    def add_nodes(self):
        kl_c = []
        for i in range(0, 10):
            kl_c.append(f"C {i + 1}")
        self.nodes.extend(kl_c)

    def check_node(self, node):
        if self.port == Port.barewire:
            if node in self.nodes:
                return True
            else:
                return False
        else:
            return False


class Pxi2569(Module):
    def add_nodes(self):
        kl_ch = []
        for i in range(0, 100):
            kl_ch.append(f"CH {i + 1}")
        self.nodes.extend(kl_ch)

    def check_node(self, node):
        if self.port == Port.barewire:
            if node in self.nodes:
                return True
            else:
                return False
        else:
            return False


class Pxi6509(Module):
    def add_nodes(self):
        p6509 = []
        for i in range(7, -1, -1):
            p6509.append(f"P 2.{i}")
            p6509.append(f"P 5.{i}")
        for i in range(7, -1, -1):
            p6509.append(f"P 1.{i}")
            p6509.append(f"P 4.{i}")
        for i in range(7, -1, -1):
            p6509.append(f"P 0.{i}")
            p6509.append(f"P 3.{i}")
        p6509.append("+5")
        p6509.append("GN1")
        for i in range(7, -1, -1):
            p6509.append(f"P 8.{i}")
            p6509.append(f"P 11.{i}")
        for i in range(7, -1, -1):
            p6509.append(f"P 7.{i}")
            p6509.append(f"P 10.{i}")
        for i in range(7, -1, -1):
            p6509.append(f"P 6.{i}")
            p6509.append(f"P 9.{i}")
        p6509.append("+5")
        p6509.append("GN2")
        self.nodes.extend(p6509)

    def check_node(self, node):
        return False


class Kbl(ABC):
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.add_nodes()
        self.modules: List[Module] = []
        self.links: List[Link] = []

    @abstractmethod
    def add_nodes(self):
        pass

    def add_module(self, module: Module):
        for mod in self.modules:
            if mod.port == module.port:
                return False
        self.modules.append(module)
        return True

    def remove_module(self, module: Module):
        for i, o in enumerate(self.modules):
            if o == module:
                del self.modules[i]
                break

    def link_in_base(self, link_to_check: Link):
        for link in self.links:
            if link == link_to_check:
                return True
        return False

    def check_node(self, node):
        if node in self.nodes:
            return True
        for mod in self.modules:
            if mod.check_node(node):
                return True
        return False

    def add_link(self, link: Link):
        if not self.link_in_base(link):
            if self.check_node(link.node1) and self.check_node(link.node2):
                self.links.append(link)
                return "link add success"
            else:
                return f"n1 in kb {self.check_node(link.node1)}   n2 in kb {self.check_node(link.node2)}"

        return "link alredy exist"

    def rem_link(self, link: Link):
        for i, o in enumerate(self.links):
            if o == link:
                del self.links[i]
                break


class Kbk(Kbl):
    def add_nodes(self):
        tmp = []
        for i in range(0, 200):
            tmp.append(f"M {i + 1}")
        for i in range(0, 16):
            tmp.append(f"K {i + 1}")
        for i in range(0, 50):
            tmp.append(f"BA1 {i + 1}")
        for i in range(0, 50):
            tmp.append(f"BA2 {i + 1}")
        for i in range(0, 50):
            tmp.append(f"BA3 {i + 1}")
        for i in range(0, 50):
            tmp.append(f"BA4 {i + 1}")
        for i in range(0, 25):
            tmp.append(f"MB1 {i + 1}")
        for i in range(0, 25):
            tmp.append(f"MB2 {i + 1}")
        for i in range(0, 25):
            tmp.append(f"MB3 {i + 1}")
        for i in range(0, 25):
            tmp.append(f"MB4 {i + 1}")
        self.nodes.extend(tmp)


if __name__ == "__main__":
    b = Pxi2568(Port.barewire)
    b2 = Pxi2569(Port.m1_50)
    k = Kbk("ds")
    k.add_module(b)
    k.add_module(b2)
    k.add_module(Pxi2568(Port.m51_100))
    k.add_module(Pxi2569(Port.m51_100))
    k.add_module(Pxi6509(Port.m51_100))
    # k.remove_module(Pxi2568(Port.m51_100))

    k.add_link(Link("M 51", "M 2", "s2"))
    k.add_link(Link("M 51", "M 2", "s2"))
    k.add_link(Link("M 51", "M 2", "s2"))
    k.add_link(Link("M 51", "K 2", "s2"))
    k.add_link(Link("M 56", "M 2", "s2"))

    k.add_link(Link("M 21", "M 2", "s2"))
    k.add_link(Link("M 51", "K 1", "s2"))
    k.add_link(Link("M 1", "M 62", "s3"))
    k.rem_link(Link("M 56", "M 2", "s2"))
    k.rem_link(Link("M 21", "M 2", "s2222"))
    for link in k.links:
        print(link)
    # print(k.modules[0].nodes)
    print(k.check_node("C 1"))

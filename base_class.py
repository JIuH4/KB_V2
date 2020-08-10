from kb_class import *
from Link import Link
from events import *


class State:
    def __init__(self, selected_signal: int = 0, all_signals=None,
                 current_links=None,
                 selected_links=None, all_nodes=None):
        if all_nodes is None:
            all_nodes = []
        if all_signals is None:
            all_signals = ["ALL"]
        if current_links is None:
            current_links = []
        if selected_links is None:
            selected_links = []
        self.all_signals: List[str] = all_signals
        self.all_nodes = all_nodes
        self.selected_signal: int = selected_signal
        self.current_links: List[Link] = current_links
        self.selected_links: List[int] = selected_links


class Observer:

    def update2(self, state: State) -> None:
        pass


class Subject(ABC):

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class Base:
    def __init__(self):
        self.kblck: Kbl = Kbk("default")

    def add_kblck(self, kbl: Kbl):
        self.kblck = kbl


class Fasade(Subject):
    def __init__(self, base: Base):
        self.base: Base = base
        self.state: State = State(all_signals=self.get_list_of_signals())
        self._observers: List[Observer] = []

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def notify(self):
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update2(self.state)

    def dispatch_event(self, event: Event):
        if isinstance(event, AddLink):
            self.add_link(event.node1, event.node2, event.signal, event.comment)
        elif isinstance(event, RemLink):
            self.rem_selected()
        elif isinstance(event, SelectSignal):
            self.select_signal(event.signal_name)
        elif isinstance(event, SelectLink):
            self.select_links(event.sel_list)
        else:
            print("wtf")

    def fill_nodes(self):
        tmp = []
        tmp.extend(self.base.kblck.nodes)
        for module in self.base.kblck.modules:
            tmp.extend(module.nodes)
        return tmp

    def state_reset(self):
        tmp_sel_signal = self.state.all_signals[self.state.selected_signal]
        tmp_sel_links = []
        for link in self.state.selected_links:
            tmp_sel_links.append(self.state.current_links[link])

        self.state = State(all_signals=self.get_list_of_signals(), current_links=self.get_links_by_signal("ALL"),
                           all_nodes=self.fill_nodes())
        self.select_signal(tmp_sel_signal)
        for link in tmp_sel_links:
            if link in self.state.current_links:
                self.state.selected_links.append(self.state.current_links.index(link))

    def get_list_of_signals(self):
        list_of_signals = []
        for link in self.base.kblck.links:
            if link.signal not in list_of_signals:
                list_of_signals.append(link.signal)
        list_of_signals.sort()
        list_of_signals.insert(0, "ALL")
        return list_of_signals

    def select_signal(self, name_of_signal):

        if name_of_signal == "ALL":
            self.state.selected_signal = 0
            # self.state.current_links.clear()
            self.state.current_links = self.get_links_by_signal(name_of_signal)
            self.state.selected_links.clear()
            self.notify()
            return "Selected ALL"
        for i, signal in enumerate(self.state.all_signals):
            if signal == name_of_signal:
                self.state.selected_signal = i
                # self.state.current_links.clear()
                self.state.current_links = self.get_links_by_signal(name_of_signal)
                self.state.selected_links.clear()
                self.notify()
                return f"Selected {name_of_signal} index {i}"

    def get_links_by_signal(self, name_of_signal):
        if name_of_signal == "ALL":
            return self.base.kblck.links
        matches = [x for x in self.base.kblck.links if x.signal == name_of_signal]
        return matches

    def select_links(self, links: List[int]):
        self.state.selected_links.clear()
        for link in links:
            if link < len(self.state.current_links):
                self.state.selected_links.append(link)
        self.notify()

    def rem_selected(self):
        tmp_links_to_rem = []
        for link_i in self.state.selected_links:
            tmp_links_to_rem.append(self.state.current_links[link_i])
        for link in tmp_links_to_rem:
            print(link)
            self.base.kblck.rem_link(link)
        self.state.selected_links.clear()
        self.state_reset()
        self.notify()

    def add_link(self, node1: str, node2: str, signal: str, comment: str = ""):
        self.base.kblck.add_link(Link(node1, node2, signal, comment))
        self.state_reset()
        self.notify()


class VSS(Observer):
    def update2(self, state: State):
        print(state.all_signals)


if __name__ == "__main__":
    b = Pxi2568(Port.barewire)
    b2 = Pxi2569(Port.m1_50)
    k = Kbk("ds")
    k.add_module(b)
    k.add_module(b2)
    k.add_module(Pxi2568(Port.m51_100))
    k.add_module(Pxi2569(Port.m51_100))
    k.add_module(Pxi6509(Port.m51_100))

    k.add_link(Link("M 51", "M 2", "s2"))
    k.add_link(Link("M 51", "M 2", "s2"))
    k.add_link(Link("M 51", "M 2", "s2"))
    k.add_link(Link("M 51", "K 2", "s2"))
    k.add_link(Link("M 56", "M 2", "s2"))

    k.add_link(Link("M 21", "M 2", "s2"))
    k.add_link(Link("M 51", "K 1", "s2"))
    k.add_link(Link("M 1", "M 62", "s3"))
    k.add_link(Link("M 1", "M 63", "s3"))
    k.add_link(Link("M 1", "M 65", "s3"))
    f = Fasade(Base())
    v = VSS()
    f.attach(v)
    f.base.kblck = k
    f.state_reset()
    print(f.select_signal("s2"))
    f.select_links([6, 1])
    f.base.kblck.rem_link(f.state.current_links[2])
    print(f.state.selected_links)
    f.state_reset()
    print(f.state.current_links)
    print(f.state.selected_signal)
    print(f.state.selected_links)
    f.dispatch_event(AddLink("M 10", "M 65", "s5"))
    f.dispatch_event(Event())
    print(f.state.all_signals)

import copy

import PySide2
import yaml
from Link import Link

from ui_elements.table import Table_widget
from temp import Scheme

from events import RemLink, SelectLink, AddLink, SelectSignal
from base_class import Observer, State, Pxi2568, Pxi2569, Port, Kbk, Pxi6509, Fasade, Base
import time
import sys
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPainter, QColor, QStandardItemModel
from PySide2.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidgetItem,
                               QWidget, QCompleter, QListWidget, QGridLayout,
                               QSizePolicy, QTableView, QHeaderView, QListView)


class Widget(QWidget, Observer):

    def __init__(self):

        QWidget.__init__(self)

        self.items_in_table = 0
        self.fasade = Fasade(Base())
        self.fasade.attach(self)
        self.currentState: State = self.fasade.state
        # Left
        self.listwidget = QListWidget()
        self.listview = QListView()
        self.listmodel = QStandardItemModel()
        self.listview.setModel(self.listmodel)
        self.table = Table_widget()

        # Right

        self.signal = QLineEdit()

        # node1
        self.node1 = QLineEdit()

        # node2
        self.node2 = QLineEdit()

        self.set_completers()

        # buttons
        self.add = QPushButton("Добавить")
        self.add.setEnabled(False)  # Disabling 'Add' button
        self.sheme = QPushButton("Схема")
        self.clear = QPushButton("Удалить")
        self.quit = QPushButton("Выход")

        self.l1 = QLabel("Сигнал")
        self.l1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.l2 = QLabel("Кл1")
        self.l2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.l3 = QLabel("Кл2")
        self.l3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.window = None

        self.grid = QGridLayout()
        self.grid.addWidget(self.l1, 0, 0)
        self.grid.addWidget(self.signal, 1, 0, 1, 2)
        self.grid.addWidget(self.l2, 2, 0)
        self.grid.addWidget(self.node1, 3, 0, )
        self.grid.addWidget(self.l3, 2, 1)
        self.grid.addWidget(self.node2, 3, 1)
        self.grid.addWidget(self.add, 5, 0, 1, 2)
        self.grid.addWidget(self.clear, 7, 0, 1, 1)
        self.grid.addWidget(self.sheme, 7, 1, 1, 1)
        self.grid.addWidget(self.quit, 9, 0, 1, 2)
        self.grid.setRowStretch(6, 1)
        self.grid.setRowStretch(8, 10)
        self.grid.setRowStretch(4, 1)

        # QWidget Layout
        self.layout = QHBoxLayout()
        self.tableview = QTableView()
        self.tablemodel = QStandardItemModel()
        self.tableview.setModel(self.tablemodel)
        self.tablemodel.setHorizontalHeaderLabels(["n1", "n2", "n3"])
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tableview.horizontalHeader().setStretchLastSection(True)
        self.tableview.horizontalHeader().setDefaultSectionSize(45)
        # self.table_view.setSizePolicy(size)
        self.layout.addWidget(self.listwidget, 30)
        self.layout.addWidget(self.table, 40)
        self.layout.addLayout(self.grid, 30)
        self.layout.setContentsMargins(1, 1, 1, 1)

        self.setLayout(self.layout)

        # Signals and Slots
        self.add.clicked.connect(self.add_element)
        self.sheme.clicked.connect(self.scheme)
        self.quit.clicked.connect(self.quit_application)
        self.clear.clicked.connect(self.delete)
        self.node1.textChanged[str].connect(self.check_disable)
        self.node2.textChanged[str].connect(self.check_disable)
        self.table.itemSelectionChanged.connect(self.on_click)
        self.listwidget.currentItemChanged.connect(self.signal_select)
        self.tempinit()
        self.window = Scheme()
        self.window.resize(1600, 900)
        self.window.move(900, 0)

    def tempinit(self):
        # b = Pxi2568(Port.barewire)
        # b2 = Pxi2569(Port.m1_50)
        # k = Kbk("ds")
        # k.add_module(b)
        # k.add_module(b2)
        # k.add_module(Pxi2568(Port.m51_100))
        # k.add_module(Pxi2569(Port.m1_50))
        # k.add_module(Pxi6509(Port.m101_150))
        # # k.remove_module(Pxi2568(Port.m51_100))
        #
        # k.add_link(Link("M 51", "M 2", "s2"))
        # k.add_link(Link("M 51", "M 2", "s2"))
        # k.add_link(Link("M 51", "M 2", "s2"))
        # k.add_link(Link("M 51", "K 2", "s2"))
        # k.add_link(Link("M 56", "M 2", "s2"))
        #
        # k.add_link(Link("M 21", "M 2", "s2"))
        # k.add_link(Link("M 51", "K 1", "s2"))
        # k.add_link(Link("M 1", "M 62", "s3"))
        # k.add_link(Link("M 1", "M 63", "s3"))
        # k.add_link(Link("M 1", "M 65", "s3"))
        # self.fasade.base.kblck = k
        # self.fasade.state_reset()
        # print(self.fasade.select_signal("s3"))
        # # self.fasade.select_links([6, 1])
        # self.fasade.base.kblck.rem_link(self.fasade.state.current_links[2])
        # print(self.fasade.state.selected_links)
        # self.fasade.state_reset()
        # print(self.fasade.state.current_links)
        # print(self.fasade.state.selected_signal)
        # print(self.fasade.state.selected_links)
        # self.fasade.dispatch_event(events.AddLink("M 10", "M 65", "s5"))
        # self.fasade.dispatch_event(events.Event())
        # print(self.fasade.state.all_signals)
        #
        # self.fasade.base.kblck = k
        # self.fasade.state_reset()
        #
        # # self.fasade.select_links([6, 1])
        #
        # print(self.fasade.state.selected_links)
        # self.fasade.state_reset()
        # print(self.fasade.state.current_links)
        # print(self.fasade.state.selected_signal)
        # print(self.fasade.state.selected_links)
        # self.fasade.dispatch_event(events.AddLink("M 10", "M 65", "s5"))
        # self.fasade.dispatch_event(events.Event())
        # print(self.fasade.state.all_signals)
        # print(yaml.dump(self.fasade.base.kblck))
        with open("tmp.yaml", 'r') as file:
            self.fasade.base.kblck = yaml.load(file, Loader=yaml.Loader)
        for i in self.fasade.base.kblck.modules:
            print(i)

        # print(self.fasade.base.kblck)
        self.fasade.state_reset()
        self.fasade.notify()
        # QMainWindow using QWidget as central widget

    def update2(self, state: State):
        self.fill_table(state)
        self.fill_list(state)
        self.currentState = copy.deepcopy(state)
        self.set_completers()
        if self.window != None:
            self.window.view.add_links(self.currentState.current_links)
            self.window.view.refresh()

            tmp = []
            for link in self.currentState.selected_links:
                tmp.append(self.currentState.current_links[link])
            self.window.view.highlight_links(tmp)
            self.window.view.refresh()

    def set_completers(self):
        completer = QCompleter(self.currentState.all_nodes, self.node1)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.node1.setCompleter(completer)
        completer2 = QCompleter(self.currentState.all_nodes, self.node2)
        completer2.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.node2.setCompleter(completer2)

    @Slot()
    def scheme(self):
        # print("sasd")
        self.window = Scheme()
        self.window.resize(1600, 900)
        self.window.move(900, 0)

        self.window.show()
        self.showMinimized()
        if self.window != None:
            print(self.fasade.base.kblck.__class__.__name__)
            self.window.view.add_module(Kbk("sd"))
            for i in self.fasade.base.kblck.modules:
                self.window.view.add_module(i)

            # self.window.view.refresh()
            # print(self.window.view.modules)
            # self.window.view.add_links(self.currentState.current_links)

            self.window.view.refresh()

    @Slot()
    def delete(self):
        print(self.currentState.selected_links)
        self.fasade.dispatch_event(RemLink())

    @Slot()
    def refresh(self):
        pass

    @Slot()
    def signal_select(self):
        if len(self.listwidget.selectedItems()) != 0:
            if self.listwidget.currentItem().text() != "ALL":
                self.signal.setText(self.listwidget.currentItem().text())
            self.fasade.dispatch_event(SelectSignal(self.listwidget.currentItem().text()))

    def list_index_by_text(self, text):
        for i in range(self.listwidget.count()):
            if self.listwidget.item(i).text() == text:
                return i
        return None

    def fill_list(self, state: State):
        if self.currentState.all_signals != state.all_signals:
            self.listwidget.clear()
            self.listwidget.addItems(state.all_signals)
            self.listwidget.blockSignals(True)
            self.listwidget.setCurrentRow(state.selected_signal)
            self.listwidget.blockSignals(False)

    @Slot()
    def add_element(self):
        print("sd")
        self.fasade.dispatch_event(AddLink(self.node1.text(), self.node2.text(), self.signal.text()))

    @Slot()
    def check_disable(self, s):
        if not self.node1.text() or not self.node2.text():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)

    @Slot()
    def on_click(self):
        sel = []
        selected = self.table.selectionModel()
        for row in selected.selectedRows():
            sel.append(row.row())

        self.fasade.dispatch_event(SelectLink(sel))

        # if self.window != None:
        #     self.window.view.highlight_links(b.selected_links)
        #     self.window.view.refresh()

    @Slot()
    def quit_application(self):
        QApplication.quit()

    def fill_table(self, state: State):
        if self.currentState.current_links != state.current_links:
            # if False:
            self.table.blockSignals(True)
            self.items_in_table = 0
            self.table.setRowCount(0)
            self.table.clear()
            self.table.setHorizontalHeaderLabels(["Кл1", "Кл2", "Сигнал"])
            for link in state.current_links:

                node1item = QTableWidgetItem(link.node1)
                node2item = QTableWidgetItem(link.node2)
                signalitem = QTableWidgetItem(link.signal)
                self.table.insertRow(self.items_in_table)
                self.table.setItem(self.items_in_table, 0, node1item)
                self.table.item(self.items_in_table, 0).setBackgroundColor(
                    QColor("light green"))
                self.table.setItem(self.items_in_table, 1, node2item)
                self.table.item(self.items_in_table, 1).setBackgroundColor(
                    QColor("light green"))
                self.table.setItem(self.items_in_table, 2, signalitem)
                self.table.item(self.items_in_table, 2).setBackgroundColor(QColor("yellow"))
                if self.items_in_table in state.selected_links:
                    self.table.selectRow(self.items_in_table)

                self.items_in_table += 1
            self.table.blockSignals(False)

    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items_in_table = 0


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("KBK")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        # self.file_save = self.file_menu.addAction('save')
        # self.file_load = self.file_menu.addAction('load')

        # Exit QAction
        exit_action = QAction("Exit", self)
        load_action = QAction("Load", self)
        save_action = QAction("Save", self)

        exit_action.setShortcut("Ctrl+Q")
        # exit_action.triggered.connect(self.exit_app)
        # load_action.triggered.connect(self.Load_app)
        # save_action.triggered.connect(self.Save_table)

        self.file_menu.addAction(load_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(exit_action)
        self.setCentralWidget(widget)

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent):
        if self.centralWidget().window != None:
            self.centralWidget().window.close()
        super().closeEvent(event)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    # @Slot()
    # def Load_app(self, checked):
    #     self.centralWidget().listwidget.clear()
    #     fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
    #     # b = Base(KBK)
    #     b.load_json(fname)
    #     # self.centralWidget().listwidget.clear()
    #     self.centralWidget().refresh()
    #     self.centralWidget().signal_select()
    #
    #     # self.centralWidget().refresh()
    #
    # def Edge_check(self, edge):
    #     if edge[:2] != "CH" and edge[0] != "P" and edge[:2] != "GN" and edge[:2] != "+5":
    #         return True
    #     else:
    #         return False

    @Slot()
    def Save_table(self):
        pass
        # tmp = []
        # for link in b.links:
        #     if self.Edge_check(link.node1) and self.Edge_check(link.node2):
        #         tmp.append([link.node1, link.node2])
        # G = nx.Graph()
        # G.add_edges_from(tmp)
        #
        # n = nx.to_numpy_matrix(G, dtype="intc")
        # numpy.set_printoptions(threshold=sys.maxsize)
        #
        # df = pd.DataFrame(data=n, index=G.nodes, columns=G.nodes)
        # df2 = pd.DataFrame(data=tmp, index=range(
        #     1, len(tmp) + 1), columns=["Node1", "Node2"])
        # # print(df2)
        # # print(n)
        # # df.style.apply(highlight_greaterthan_1,axis=1)
        #
        # df.to_excel('MS.xlsx')
        # df2.to_excel('EL.xlsx')
        # # plt.show()
        # # self.centralWidget().refresh()

    @Slot()
    def Save_app(self, checked):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    window = MainWindow(widget)
    window.resize(900, 400)
    window.move(0, 0)
    window.show()

    # Execute application
    sys.exit(app.exec_())

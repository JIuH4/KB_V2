import math
import sys
import enum
from abc import ABC, abstractmethod

from kb_class import Module, Pxi2569, Kbk
from kb_nodes import KBK
from typing import List
from ui_elements.graph_items.modules import P2569
from ui_elements.graph_items.krossblocks import Kbk as Kbk_gi
from ui_elements.graph_items.module_or_kb_base import module_or_kb_base
from ui_elements.graph_items.link import LinkState, Link_scheme
from events import RemLink, SelectLink, AddLink, SelectSignal

from ui_elements.graph_items.node import Node, NodeState
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QPoint, Qt, QSize, QRect
from PySide2.QtGui import QPainter, QFont, QColor, QPen
from PySide2.QtWidgets import (QApplication, QHBoxLayout,
                               QGraphicsScene, QWidget, QGraphicsView, QGraphicsItem, QGraphicsSceneMouseEvent)
from PySide2.QtSvg import *

from Link import Link, DLink


class Observer_for_widgets:
    def event_from_widget(self, Event_from_widget):
        pass



class Subject(ABC):

    @abstractmethod
    def attach(self, observer: Observer_for_widgets) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer_for_widgets) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class Scheme(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.layt = QHBoxLayout()
        self.view = GraphWidget(parent)
        self.layt.addWidget(self.view)
        self.setWindowTitle("Схема")
        self.setLayout(self.layt)
        # print(self.parent())
        # print("ss")

    def wheelEvent(self, event):
        numDegrees = event.delta() / 8
        numSteps = numDegrees / 15

        if event.orientation() == Qt.Horizontal:
            pass
        else:
            modifiers = QtGui.QGuiApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if numSteps > 0:
                    self.view.scale(1.05, 1.05)
                if numSteps < 0:
                    self.view.scale(0.95, 0.95)
        event.accept()

    def clc(self):
        self.view.terminals[2].state = NodeState.highlight
        print(self.view.terminals[2].num)
        print(self.view.terminals[2].name)
        self.view.highlight_links([Link("C 1", "M 100")])
        self.view.refresh()


class GraphWidget(QGraphicsView, Observer_for_widgets):
    def __init__(self,parent):
        QGraphicsView.__init__(self)

        self.timerId = 0
        self.parent=parent
        self.modules_gi: List[module_or_kb_base] = []
        self.links: List[Link_scheme] = []

        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(-785, -400, 1570, 800)
        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setBackgroundBrush(QColor("lightgray"))
        # self.parent.event_from_scheme()


    def event_from_widget(self):
        self.parent.event_from_scheme()

    def add_module(self, module):
        if isinstance(module, Kbk):
            tmp = Kbk_gi(self)
            tmp.setPos(0, 0)
            self.modules_gi.append(tmp)
            self.scene.addItem(tmp)
            # print(tmp.parentObject())

        if isinstance(module, Pxi2569):
            tmp = P2569(self)
            tmp.setPos(-130, 340)
            self.modules_gi.append(tmp)
            self.scene.addItem(tmp)

    def refresh(self):
        self.scene.update()

    def clear_links(self):
        for link in self.links:
            self.scene.removeItem(link)
        self.links.clear()

    def add_links(self, list_of_links: List[Link]):
        for module in self.modules_gi:
            for nod in module.terminals:
                nod.state = NodeState.normal
        self.clear_links()
        for link in list_of_links:
            try:
                self.print_link(link.node1, link.node2)
            except:
                pass

    def highlight_links(self, list_of_links: List[Link]):
        for module in self.modules_gi:
            for nod in module.terminals:
                nod.state = NodeState.normal
        for printed_link in self.links:
            printed_link.state = LinkState.normal

            self.get_node_by_tag(printed_link.tag1).state = NodeState.used
            self.get_node_by_tag(printed_link.tag2).state = NodeState.used
        for link in list_of_links:
            for printed_link in self.links:

                if Link(link.node1, link.node2) == Link(printed_link.tag1, printed_link.tag2):
                    printed_link.state = LinkState.highlight
                    self.get_node_by_tag(link.node1).state = NodeState.highlight
                    self.get_node_by_tag(link.node2).state = NodeState.highlight
        self.refresh()

    def get_node_by_tag(self, tag):
        for module in self.modules_gi:
            for node in module.terminals:
                if node.tag == tag:
                    return node
        return None

    def print_link(self, tag1, tag2):
        # print(f"{tag1}   {tag2}")
        tag1_pos = self.get_node_by_tag(tag1).pos()
        tag2_pos = self.get_node_by_tag(tag2).pos()
        # print(f"{tag1_pos}   {tag2_pos}")
        self.links.append(Link_scheme(tag1_pos.x(), tag1_pos.y(), tag2_pos.x(), tag2_pos.y(), tag1, tag2))
        self.scene.addItem(self.links[-1])
        self.get_node_by_tag(tag1).state = NodeState.used
        self.get_node_by_tag(tag2).state = NodeState.used
        # self.scene.addLine(tag1_pos.x(),tag1_pos.y(),tag2_pos.x(),tag2_pos.y())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Scheme()
    # widget.view.scale(0.8,0.8)
    widget.show()

    sys.exit(app.exec_())

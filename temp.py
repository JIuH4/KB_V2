import math
import sys
import enum
from kb_nodes import KBK
from typing import List
from ui_elements.graph_items.kb_base import Kb_base
from ui_elements.graph_items.node import Node, NodeState
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QPoint, Qt, QSize, QRect
from PySide2.QtGui import QPainter, QFont, QColor, QPen
from PySide2.QtWidgets import (QApplication, QHBoxLayout,
                               QGraphicsScene, QWidget, QGraphicsView, QGraphicsItem, QGraphicsSceneMouseEvent)
from PySide2.QtSvg import *

from Link import Link, DLink


class LinkState(enum.Enum):
    normal = 0
    used = 1
    highlight = 2


class Scheme(QWidget):
    def __init__(self):
        super().__init__()
        self.layt = QHBoxLayout()
        self.view = GraphWidget()
        self.layt.addWidget(self.view)
        self.setWindowTitle("Схема")
        self.setLayout(self.layt)

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


class Edge(QtWidgets.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QtWidgets.QGraphicsItem.UserType + 3

    def __init__(self, n1_x, n1_y, n2_x, n2_y, tag1, tag2):
        QtWidgets.QGraphicsItem.__init__(self)
        self.tag1 = tag1
        self.tag2 = tag2
        self.n1_x = n1_x
        self.n1_y = n1_y
        self.n2_x = n2_x
        self.n2_y = n2_y
        self.state = LinkState.normal
        self.color = QtCore.Qt.red
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        print(event.pos())

    def type(self):
        return Edge.Type

    def boundingRect(self):
        return QtCore.QRectF(self.n1_x, self.n1_y, self.n2_x, self.n2_y).normalized()

    def paint(self, painter, option, widget):
        if self.state == LinkState.normal:
            self.color = QColor('red')
        elif self.state == LinkState.used:
            self.color = QColor('red')
        elif self.state == LinkState.highlight:
            self.color = QColor('blue')

        line = QtCore.QLineF(QPoint(self.n1_x, self.n1_y), QPoint(self.n2_x, self.n2_y))

        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(self.color, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)


class Kbk(Kb_base):
    Type = QtWidgets.QGraphicsItem.UserType + 4

    def __init__(self, name: str, base_y=-100, base_x=-100, size_x=1450, size_y=500, ):
        Kb_base.__init__(self)
        self.size_x = size_x
        self.size_y = size_y
        self.base_x = base_x
        self.base_y = base_y
        self.name = name
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setCacheMode(self.DeviceCoordinateCache)
        for m in self.terminals:
            print(m.pos())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        print("1")

    def upd(self, event: QGraphicsSceneMouseEvent):
        print(event.scenePos())

    def type(self):
        return Kbk.Type

    def boundingRect(self):
        return QtCore.QRectF((self.size_x // 2) * -1, (self.size_y // 2) * -1, self.size_x, self.size_y)

    def paint(self, painter, option, widget):
        self.terminal_print_face_down(painter, -596, 210, 50, "M", start_number=0, shift=25)
        self.terminal_print_face_down(painter, 22, 210, 50, "M", start_number=25, shift=25)
        self.terminal_print_face_down(painter, -596, 110, 50, "M", start_number=100, shift=27)
        self.terminal_print_face_down(painter, 22, 110, 54, "M", start_number=125, shift=25)
        self.terminal_print_one_line(painter, -596, -2, 25, "MB2")
        self.terminal_print_one_line(painter, -596, 22, 25, "MB1")
        self.terminal_print_one_line(painter, 22, -2, 25, "MB4", tag_direction=1)
        self.terminal_print_one_line(painter, 22, 22, 25, "MB3", tag_direction=1)
        self.terminal_print_face_up(painter, -596, -112, 50, "BA2")
        self.terminal_print_face_up(painter, -596, -212, 50, "BA1")
        self.terminal_print_face_up(painter, 22, -112, 50, "BA4")
        self.terminal_print_face_up(painter, 22, -212, 50, "BA3")
        self.terminal_print_face_up(painter, 638, -112, 8, "K")
        self.terminal_print_face_up(painter, -709, -112, 8, "K", start_number=8)
        # self.print_greed(painter)
        painter.drawRect((self.size_x // 2) * -1, (self.size_y // 2) * -1, self.size_x, self.size_y)
        for m in self.terminals:
            print(m.name)


class GraphWidget(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)

        self.timerId = 0
        self.terminals: List[Node] = []
        self.links: List[Edge] = []

        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(-785, -400, 1570, 800)
        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setBackgroundBrush(QColor("lightgray"))

        self.scene.addItem(Kbk("ss"))

    def refresh(self):
        self.scene.update()

    def clear_links(self):
        for link in self.links:
            self.scene.removeItem(link)
        self.links.clear()

    def add_links(self, list_of_links: List[Link]):
        for nod in self.terminals:
            nod.state = NodeState.normal
        self.clear_links()
        for link in list_of_links:
            self.print_link(link.node1, link.node2)

    def highlight_links(self, list_of_links: List[Link]):
        for nod in self.terminals:
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
        for node in self.terminals:
            if node.tag == tag:
                return node

    def print_link(self, tag1, tag2):
        # print(f"{tag1}   {tag2}")
        for node in self.terminals:
            if node.tag == tag1:
                tag1_pos = node.pos()
            if node.tag == tag2:
                tag2_pos = node.pos()
        # print(f"{tag1_pos}   {tag2_pos}")
        self.links.append(Edge(tag1_pos.x(), tag1_pos.y(), tag2_pos.x(), tag2_pos.y(), tag1, tag2))
        self.scene.addItem(self.links[-1])
        self.get_node_by_tag(tag1).state = NodeState.used
        self.get_node_by_tag(tag2).state = NodeState.used
        # self.scene.addLine(tag1_pos.x(),tag1_pos.y(),tag2_pos.x(),tag2_pos.y())

    def print_greed(self):
        self.scene.addLine(0, -400, 0, 400, pen=QPen(QColor("black")))
        self.scene.addLine(-800, 0, 800, 0, pen=QPen(QColor("black")))
        for x in range(-800, 800, 10):
            self.scene.addLine(x, -400, x, 400, pen=QPen(QColor("green")))
        for y in range(-400, 400, 10):
            self.scene.addLine(-800, y, 800, y, pen=QPen(QColor("green")))

    def terminal_print_face_up(self, basex, basey, count, name, size=22, gap=2, start_number=0, shift=0):
        self.scene.addText(name, font=QFont('Verdana', 12)).setPos(basex - size // 2 - gap, basey - size - gap - 10)

        for number_in_row in range(0, count // 2):
            tmp = Node(self, start_number + number_in_row + 1, name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey)
            self.scene.addItem(tmp)
            self.terminals.append(tmp)
        for number_in_row in range(count // 2, count):
            tmp = Node(self, start_number + shift + number_in_row + 1, name, size=size)
            tmp.setPos(basex + (size + gap) * (number_in_row - count // 2), basey + size + gap)
            self.scene.addItem(tmp)
            self.terminals.append(tmp)

    def terminal_print_face_down(self, basex, basey, count, name, size=22, gap=2, start_number=0, shift=0):
        self.scene.addText(name, font=QFont('Verdana', 12)).setPos(basex - size // 2 - gap, basey - size - gap - 10)

        for number_in_row in range(0, count // 2):
            tmp = Node(self, start_number + number_in_row + 1, name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey + size + gap)
            self.scene.addItem(tmp)
            self.terminals.append(tmp)
        for number_in_row in range(count // 2, count):
            tmp = Node(self, start_number + shift + number_in_row + 1, name, size=size)
            tmp.setPos(basex + (size + gap) * (number_in_row - count // 2), basey)
            self.scene.addItem(tmp)
            self.terminals.append(tmp)

    def terminal_print_6509(self, basex, basey, count, name, size=22, gap=2):
        self.scene.addText(name, font=QFont('Verdana', 12)).setPos(basex - size // 2 - gap, basey - size - gap - 10)
        tmpel = []
        for element in KBK[-1]:
            if element[:2] != "+5" and element[:2] != "GN":
                tmpel.append(element[2:])
            else:
                tmpel.append(element)

        for number_in_row in range(0, count // 2):
            tmp = Node(self, tmpel[number_in_row], name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey + size + gap)
            self.scene.addItem(tmp)
            self.terminals.append(tmp)
        for number_in_row in range(count // 2, count):
            tmp = Node(self, tmpel[number_in_row], name, size=size)
            tmp.setPos(basex + (size + gap) * (number_in_row - count // 2), basey)
            self.scene.addItem(tmp)
            self.terminals.append(tmp)

    def terminal_print_one_line(self, basex, basey, count, name, size=22, gap=2, start_number=0, tag_direction=0):
        if tag_direction == 0:
            self.scene.addText(name, font=QFont('Verdana', 12)).setPos(basex - size * 2 - gap * 4,
                                                                       basey - size // 2 - 5)
        else:
            self.scene.addText(name, font=QFont('Verdana', 12)).setPos(basex + (size + gap) * count - 10,
                                                                       basey - size // 2 - 5)

        for number_in_row in range(0, count):
            tmp = Node(self, start_number + number_in_row + 1, name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey)
            self.scene.addItem(tmp)
            self.terminals.append(tmp)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Scheme()
    # widget.view.scale(0.8,0.8)
    widget.show()

    sys.exit(app.exec_())

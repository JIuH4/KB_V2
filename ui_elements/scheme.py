import math
import sys
import enum
from kb_nodes import KBK
from typing import List
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QPoint, Qt, QSize, QRect
from PySide2.QtGui import QPainter, QFont, QColor, QPen
from PySide2.QtWidgets import (QApplication, QHBoxLayout,
                               QGraphicsScene, QWidget, QGraphicsView, QGraphicsItem)
from PySide2.QtSvg import *

from Link import Link, DLink


class NodeState(enum.Enum):
    normal = 0
    used = 1
    highlight = 2


class LinkState(enum.Enum):
    normal = 0
    used = 1
    highlight = 2


class Scheme(QWidget):
    def __init__(self):
        super().__init__()

        self.layt = QHBoxLayout()
        # btn = QPushButton("Sdasd")
        # btn.clicked.connect(self.clc)
        # self.layt.addWidget(btn)
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
                    # self.view.fitInView(0.95,0.95,Qt.KeepAspectRatio)
                if numSteps < 0:
                    self.view.scale(0.95, 0.95)
            # newHeight = self.geometry().height() - event.delta()
            # width = self.geometry().width() - event.delta()
            # self.resize(width, newHeight)
        event.accept()

    def clc(self):
        # self.view.links[-1].state=LinkState.highlight
        self.view.terminals[2].state = NodeState.highlight

        print(self.view.terminals[2].num)
        print(self.view.terminals[2].name)
        # self.view.scene.removeItem(self.view.links[-1])
        # self.view.clear_links()
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


class Node(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, graphWidget, num, name: str, size=22):
        QGraphicsItem.__init__(self)
        self.state = NodeState.normal
        self.size = size
        self.name = name
        if isinstance(num, str):
            self.numstr = num
            self.num = 9999
        elif isinstance(num, int):
            self.numstr = str(num)
            self.num = num

        # self.num = num
        if self.numstr[:2] == "GN" or self.numstr == "+5":
            self.tag = self.numstr
        else:
            self.tag = name + " " + self.numstr
        self.color = QColor('light green')

        # self.setFlag(QGraphicsItem.ItemIsMovable)
        # self.setFlag(QGraphicsItem.ItemIsSelectable)
        # self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)

    def type(self):
        return Node.Type

    def boundingRect(self):

        return QtCore.QRectF((self.size // 2) * -1, (self.size // 2) * -1, self.size, self.size)

    def paint(self, painter, option, widget):
        if self.state == NodeState.normal:
            self.color = QColor('light green')
        elif self.state == NodeState.used:
            self.color = QColor('yellow')
        elif self.state == NodeState.highlight:
            self.color = QColor('cyan')
        painter.setPen(QColor("black"))
        painter.setBrush(self.color)
        painter.drawRect((self.size // 2) * -1, (self.size // 2) * -1, self.size, self.size)

        painter.setPen(QColor("black"))
        painter.setFont(QFont('Verdana', 7))

        if self.num == 9999:
            if len(self.numstr) >= 4:
                textpoint = QPoint(-12, 3)
            elif len(self.numstr) >= 3:
                textpoint = QPoint(-8, 3)
            else:
                textpoint = QPoint(-4, 3)
            if self.numstr == "GND":
                textpoint = QPoint(-12, 3)
            if self.numstr == "+5":
                textpoint = QPoint(-8, 3)
        else:

            if self.num >= 100:
                textpoint = QPoint(-11, 3)
            elif self.num >= 10:
                textpoint = QPoint(-7, 3)
            else:
                textpoint = QPoint(-3, 3)
        # if self.numstr=="GND":
        # print(f"{textpoint.x()} {textpoint.y()}")
        painter.drawText(textpoint, self.numstr)


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

        self.terminal_print_face_down(-618, 200, 50, "M", start_number=0, shift=25)
        self.terminal_print_face_down(40, 200, 50, "M", start_number=25, shift=25)
        self.terminal_print_face_down(-618, 100, 50, "M", start_number=100, shift=27)
        self.terminal_print_face_down(40, 100, 54, "M", start_number=125, shift=25)
        self.terminal_print_one_line(-618, -12, 25, "MB2")
        self.terminal_print_one_line(-618, 12, 25, "MB1")
        self.terminal_print_one_line(40, -12, 25, "MB4", tag_direction=1)
        self.terminal_print_one_line(40, 12, 25, "MB3", tag_direction=1)
        self.terminal_print_face_up(-618, -124, 50, "BA2")
        self.terminal_print_face_up(-618, -224, 50, "BA1")
        self.terminal_print_face_up(40, -124, 50, "BA4")
        self.terminal_print_face_up(40, -224, 50, "BA3")
        self.terminal_print_face_up(680, -124, 8, "K")
        self.terminal_print_face_up(-758, -124, 8, "K", start_number=8)
        self.terminal_print_face_down(-590, 300, 100, "CH")
        self.terminal_print_face_down(-670, -320, 10, "C")
        self.terminal_print_6509(-500, -320, 100, "P")
        generator = QSvgGenerator()
        generator.setFileName("test.svg")
        generator.setSize(QSize(1000, 1000))
        # generator.setViewBox(QRect(0, 0, 100, 100))
        painter = QPainter()
        painter.begin(generator)
        self.render(painter)
        painter.end()

        # self.print_link("C 1", "M 100")

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

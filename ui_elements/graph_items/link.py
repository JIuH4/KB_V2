import enum
import math

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import QPoint
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsSceneMouseEvent


class LinkState(enum.Enum):
    normal = 0
    used = 1
    highlight = 2

class Link_scheme(QtWidgets.QGraphicsItem):
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
        return Link_scheme.Type

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
import enum

from PySide2 import QtCore
from PySide2.QtCore import QPoint
from PySide2.QtGui import QColor, QFont
from PySide2.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsItem

class NodeState(enum.Enum):
    normal = 0
    used = 1
    highlight = 2


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

        if self.numstr[:2] == "GN" or self.numstr == "+5":
            self.tag = self.numstr
        else:
            self.tag = name + " " + self.numstr
        self.color = QColor('light green')

        # self.setFlag(QGraphicsItem.ItemIsMovable)
        # self.setFlag(QGraphicsItem.ItemIsSelectable)
        # self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.parentItem().upd(event)

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
        painter.drawText(textpoint, self.numstr)
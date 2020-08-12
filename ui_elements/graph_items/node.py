import enum

from PySide2 import QtCore
from PySide2.QtCore import QPoint
from PySide2.QtGui import QColor, QFont, QFontDatabase
from PySide2.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsItem


class NodeState(enum.Enum):
    normal = 0
    used = 1
    highlight = 2


class Node(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, graphWidget, name: str, group_name: str, size=22):
        QGraphicsItem.__init__(self)
        self.state = NodeState.normal
        self.size = size

        self.fixedFont = QFont("Monospace")
        self.fixedFont.setStyleHint(QFont.TypeWriter)
        self.group_name = group_name
        self.name = name
        self.tag = group_name + " " + self.name
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
        painter.setFont(self.fixedFont)

        if len(self.name) >= 3:
            textpoint = QPoint(-11, 3)
        elif len(self.name) >= 2:
            textpoint = QPoint(-7, 3)
        else:
            textpoint = QPoint(-4, 3)
        painter.drawText(textpoint, self.name)

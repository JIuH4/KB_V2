from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsItem

from ui_elements.graph_items.module_or_kb_base import module_or_kb_base

class P2569(module_or_kb_base):
    Type = QtWidgets.QGraphicsItem.UserType + 5

    def __init__(self, parent, base_y=-100, base_x=-100, size_x=1208, size_y=90, ):
        module_or_kb_base.__init__(self,parent)
        self.size_x = size_x
        self.size_y = size_y
        self.base_x = base_x
        self.base_y = base_y
        # self.name = name
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setCacheMode(self.DeviceCoordinateCache)
        for m in self.terminals:
            print(m.pos())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        print("1")

    def upd(self, event: QGraphicsSceneMouseEvent):
        print(event.scenePos())

    def type(self):
        return P2569.Type

    def boundingRect(self):
        return QtCore.QRectF((self.size_x // 2) * -1, (self.size_y // 2) * -1, self.size_x, self.size_y)

    def paint(self, painter, option, widget):
        self.terminal_print_face_up(painter, ((self.size_x // 2) * -1) + 16, ((self.size_y // 2) * -1) + 41, 100, "CH")

        # self.print_greed(painter)
        painter.drawRect((self.size_x // 2) * -1, (self.size_y // 2) * -1, self.size_x, self.size_y)

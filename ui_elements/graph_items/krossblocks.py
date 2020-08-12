from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsItem

from ui_elements.graph_items.module_or_kb_base import module_or_kb_base


class Kbk(module_or_kb_base):
    Type = QtWidgets.QGraphicsItem.UserType + 4

    def __init__(self, name: str, base_y=-100, base_x=-100, size_x=1450, size_y=500, ):
        module_or_kb_base.__init__(self)
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
        # for m in self.terminals:
        #     print(m.name)
import typing
import weakref

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsItem

from ui_elements.graph_items.module_or_kb_base import module_or_kb_base, Base_for_module


class Kb_KBK(Base_for_module):
    Type = QtWidgets.QGraphicsItem.UserType + 1

    def __init__(self, graphWidget, width=1450, height=500):
        super(Kb_KBK, self).__init__()
        self.size_x = width
        self.size_y = height
        self.graph = weakref.ref(graphWidget)
        self.edgeList = []
        # self.newPos = QtCore.QPointF()
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)
        self.terminal_print_face_down(-596, 210, 50, "M", start_number=0, shift=25)
        self.terminal_print_face_down(22, 210, 50, "M", start_number=25, shift=25)
        self.terminal_print_face_down(-596, 110, 50, "M", start_number=100, shift=27)
        self.terminal_print_face_down(22, 110, 54, "M", start_number=125, shift=25)
        self.terminal_print_one_line(-596, -2, 25, "MB2")
        self.terminal_print_one_line(-596, 22, 25, "MB1")
        self.terminal_print_one_line(22, -2, 25, "MB4", tag_direction=1)
        self.terminal_print_one_line(22, 22, 25, "MB3", tag_direction=1)
        self.terminal_print_face_up(-596, -112, 50, "BA2")
        self.terminal_print_face_up(-596, -212, 50, "BA1")
        self.terminal_print_face_up(22, -112, 50, "BA4")
        self.terminal_print_face_up(22, -212, 50, "BA3")
        self.terminal_print_face_up(638, -112, 8, "K")
        self.terminal_print_face_up(-709, -112, 8, "K", start_number=8)
        for nd in self.terminals:
            nd.setParentItem(self)

        for tx in self.texts:
            tx.setParentItem(self)
        # print(self.terminals[1].scenePos())

    def type(self):
        return self.__class__.Type

    def addEdge(self, edge):
        self.edgeList.append(weakref.ref(edge))
        edge.adjust()

    def edges(self):
        return self.edgeList

    def boundingRect(self):

        return QtCore.QRectF(-1 * (self.size_x // 2), -1 * (self.size_y // 2),
                             self.size_x, self.size_y)

    # def shape(self):
    #     path = QtGui.QPainterPath()
    #     path.addEllipse(-10, -10, 20, 20)
    #     return path

    def paint(self, painter, option, widget):

        painter.setBrush(QtCore.Qt.lightGray)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawRect(-1 * (self.size_x // 2), -1 * (self.size_y // 2),
                         self.size_x, self.size_y)

        # super().paint( painter, option, widget)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            for edge in self.edgeList:
                edge().adjust()
            self.graph().itemMoved()
            # if len(self.terminals)>0:
            # print(self.terminals[1].scenePos())

        return QtWidgets.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        QtWidgets.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtWidgets.QGraphicsItem.mouseReleaseEvent(self, event)
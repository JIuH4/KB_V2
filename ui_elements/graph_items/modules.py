import weakref

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsItem

from ui_elements.graph_items.module_or_kb_base import module_or_kb_base, Base_for_module


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


class Pxi_2569(Base_for_module):
    Type = QtWidgets.QGraphicsItem.UserType + 1

    def __init__(self, graphWidget, width=1208, height=90):
        super(Pxi_2569, self).__init__()
        self.size_x = width
        self.size_y = height
        self.graph = weakref.ref(graphWidget)
        self.edgeList = []
        # self.newPos = QtCore.QPointF()
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)

        self.terminal_print_face_up(((self.size_x // 2) * -1) + 16, ((self.size_y // 2) * -1) + 41, 100, "CH")

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
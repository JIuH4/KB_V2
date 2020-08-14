import sys
import weakref
import math
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QPoint
from ui_elements.graph_items.module_or_kb_base import module_or_kb_base


class Edge(QtWidgets.QGraphicsItem):
    Type = QtWidgets.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        QtWidgets.QGraphicsItem.__init__(self)

        self.arrowSize = 10.0
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self.source().addEdge(self)
        self.dest().addEdge(self)
        self.adjust()

    def type(self):
        return Edge.Type

    def sourceNode(self):
        return self.source()

    def setSourceNode(self, node):
        self.source = weakref.ref(node)
        self.adjust()

    def destNode(self):
        return self.dest()

    def setDestNode(self, node):
        self.dest = weakref.ref(node)
        self.adjust()

    def adjust(self):
        if not self.source() or not self.dest():
            return

        line = QtCore.QLineF(self.mapFromItem(self.source(), 0, 0), self.mapFromItem(self.dest(), 0, 0))
        length = line.length()

        if length == 0.0:
            return

        self.prepareGeometryChange()
        self.sourcePoint = line.p1()
        self.destPoint = line.p2()

    def boundingRect(self):
        if not self.source() or not self.dest():
            return QtCore.QRectF()

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized()

    def paint(self, painter, option, widget):
        if not self.source() or not self.dest():
            return

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        painter.setBrush(QtCore.Qt.black)


class Node_new(module_or_kb_base):
    Type = QtWidgets.QGraphicsItem.UserType + 1

    def __init__(self, graphWidget, width=500, height=200):
        QtWidgets.QGraphicsItem.__init__(self)
        self.size_x = width
        self.terminals = []
        self.size_y = height
        self.graph = weakref.ref(graphWidget)
        self.edgeList = []
        self.newPos = QtCore.QPointF()
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)

    def type(self):
        return Node_new.Type

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

        # painter.setBrush(QtCore.Qt.darkGray)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawRect(-1 * (self.size_x // 2), -1 * (self.size_y // 2),
                         self.size_x, self.size_y)

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawRect(-1 * (self.size_x // 4), -1 * (self.size_y // 4),
                         self.size_x // 2, self.size_y // 2)
        self.terminal_print_face_up(painter,0,0,10,"ds")

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            for edge in self.edgeList:
                edge().adjust()
            self.graph().itemMoved()

        return QtWidgets.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        QtWidgets.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtWidgets.QGraphicsItem.mouseReleaseEvent(self, event)


class GraphWidget(QtWidgets.QGraphicsView):
    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)

        self.timerId = 0
        height = 900
        width = 1300

        scene = QtWidgets.QGraphicsScene(self)
        scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        scene.setSceneRect(-1 * (width // 2), -1 * (height // 2), width, height)
        self.setScene(scene)
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)

        node1 = Node_new(self)
        node2 = Node_new(self)

        self.centerNode = Node_new(self)

        scene.addItem(node1)
        scene.addItem(node2)

        scene.addItem(self.centerNode)

        scene.addItem(Edge(node1, node2))

        scene.addItem(Edge(node2, self.centerNode))

        node1.setPos(-width // 3, -height // 3)
        node2.setPos(250, -250)

        self.centerNode.setPos(0, 0)

        for item in scene.items():
            if isinstance(item, Edge):
                item.adjust()

        # self.scale(0.8, 0.8)
        # self.setMinimumSize(400, 400)
        # self.setWindowTitle(self.tr("Elastic Nodes"))

    def itemMoved(self):
        pass  # important

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # QtCore.qsrand(QtCore.QTime(0, 0, 0).secsTo(QtCore.QTime.currentTime()))

    widget = GraphWidget()
    widget.move(QPoint(0, 0))
    widget.show()

    sys.exit(app.exec_())

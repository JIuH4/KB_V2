import enum
import math
import weakref

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import QPoint
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsSceneMouseEvent

from ui_elements.graph_items.node import NodeState


class LinkState(enum.Enum):
    normal = 0
    used = 1
    highlight = 2


class Edge(QtWidgets.QGraphicsItem):
    Type = QtWidgets.QGraphicsItem.UserType + 2

    def __init__(self, source_module, source_term_name, dest_module, dest_term_name, ):
        QtWidgets.QGraphicsItem.__init__(self)

        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.state = LinkState.normal
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.source_term_name = source_term_name
        self.dest_term_name = dest_term_name
        self.source = weakref.ref(source_module.get_terminal(source_term_name))
        self.source_module = weakref.ref(source_module)
        self.dest_module = weakref.ref(dest_module)
        self.dest = weakref.ref(dest_module.get_terminal(dest_term_name))
        source_module.addEdge(self)
        dest_module.addEdge(self)
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

        line = QtCore.QLineF(self.mapFromItem(self.source(), 0, 0),
                             self.mapFromItem(self.dest(), 0, 0))
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

        if self.state == LinkState.normal:
            self.color = QColor('red')
            self.source().state = NodeState.used
            self.dest().state = NodeState.used
        elif self.state == LinkState.used:
            self.color = QColor('red')
            self.source().state = NodeState.used
            self.dest().state = NodeState.used
        elif self.state == LinkState.highlight:
            self.color = QColor('blue')
            self.source().state = NodeState.highlight
            self.dest().state = NodeState.highlight
        self.dest().update()
        self.source().update()

        # self.dest().adjust()
        # self.source().adjust()
        # self.dest_module().update()

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(self.color, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        painter.setBrush(QtCore.Qt.black)


class Edge1(QtWidgets.QGraphicsItem):
    Type = QtWidgets.QGraphicsItem.UserType + 2

    def __init__(self, source_module, source_term_name, dest_module, dest_term_name, ):
        QtWidgets.QGraphicsItem.__init__(self)

        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.state = LinkState.normal
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.source_term_name = source_term_name
        self.dest_term_name = dest_term_name
        self.source = weakref.ref(source_module)
        self.dest = weakref.ref(dest_module)
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

        line = QtCore.QLineF(self.mapFromItem(self.source().terminals_dict.get(self.source_term_name, None), 0, 0),
                             self.mapFromItem(self.dest().terminals_dict.get(self.dest_term_name, None), 0, 0))
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

        if self.state == LinkState.normal:
            self.color = QColor('red')
            self.source().terminals_dict.get(self.source_term_name, None).state = NodeState.used
            self.dest().terminals_dict.get(self.dest_term_name, None).state = NodeState.used
        elif self.state == LinkState.used:
            self.color = QColor('red')
            self.source().terminals_dict.get(self.source_term_name, None).state = NodeState.used
            self.dest().terminals_dict.get(self.dest_term_name, None).state = NodeState.used
        elif self.state == LinkState.highlight:
            self.color = QColor('blue')
            self.source().terminals_dict.get(self.source_term_name, None).state = NodeState.highlight
            self.dest().terminals_dict.get(self.dest_term_name, None).state = NodeState.highlight

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(self.color, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        painter.setBrush(QtCore.Qt.black)

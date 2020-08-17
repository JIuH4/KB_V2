import sys
import weakref
import math
from typing import List

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QPoint
from PySide2.QtWidgets import QGraphicsItem

from ui_elements.graph_items.krossblocks import Kb_KBK
from ui_elements.graph_items.link import Edge, LinkState
from ui_elements.graph_items.module_or_kb_base import module_or_kb_base, Base_for_module
from ui_elements.graph_items.modules import Pxi_2569


class GraphWidget(QtWidgets.QGraphicsView):
    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)

        self.timerId = 0
        height = 900
        width = 1600

        scene = QtWidgets.QGraphicsScene(self)
        scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        scene.setSceneRect(-1 * (width // 2), -1 * (height // 2), width, height)

        self.setScene(scene)
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)

        self.modules: List[Base_for_module] = []
        self.links: List[Edge] = []

        self.test_init()

        for item in scene.items():
            if isinstance(item, Edge):
                item.adjust()

        # self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Scheme")

    def test_init(self):

        self.add_module(Kb_KBK(self))
        self.add_module(Pxi_2569(self))

        self.add_edge("K 1", "CH 22")
        self.add_edge("K 2", "BA1 2")
        self.modules[1].setPos(0, -350)
        self.higlight_link("K 1", "CH 22")
        self.higlight_link("K 2", "BA1 2")


    def add_module(self, module):
        if isinstance(module, Kb_KBK):
            tmp = Kb_KBK(self)
            tmp.setPos(0, 0)
            self.modules.append(tmp)
            self.scene().addItem(tmp)

        if isinstance(module, Pxi_2569):
            tmp = Pxi_2569(self)
            tmp.setPos(-130, 340)
            self.modules.append(tmp)
            self.scene().addItem(tmp)

    def get_module_by_term(self, terminal: str) -> Base_for_module:
        for module in self.modules:
            tmp = module.get_terminal(terminal)
            if tmp is not None:
                return module
        return None

    def add_edge(self, node1: str, node2: str):
        if self.get_module_by_term(node1) != None and self.get_module_by_term(node2) != None:
            tmp = Edge(self.get_module_by_term(node1), node1, self.get_module_by_term(node2), node2)
            self.scene().addItem(tmp)
            self.links.append(tmp)

    def higlight_link(self, node1: str, node2: str):
        for link in self.links:
            if link.source_term_name==node1 and link.dest_term_name==node2:
                link.state=LinkState.highlight

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

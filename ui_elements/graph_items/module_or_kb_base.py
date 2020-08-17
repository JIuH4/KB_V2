from PySide2 import QtWidgets
from PySide2.QtGui import QFont, QPen, QColor
from PySide2.QtWidgets import QGraphicsItem, QGraphicsSimpleTextItem

from ui_elements.graph_items.node import Node


class module_or_kb_base(QGraphicsItem):
    Type = QtWidgets.QGraphicsItem.UserType + 4

    def __init__(self):
        QGraphicsItem.__init__(self)
        self.terminals = []
        self.texts = []

        self.font = QFont()
        self.font.setPixelSize(16)

    def terminal_print_face_up2(self, basex, basey, count, name, size=22, gap=2, start_number=0, shift=0):
        caption = QGraphicsSimpleTextItem()
        caption.setText(name)
        caption.setFont(self.font)
        caption.setPos(basex - size // 2 - gap, basey - size - gap * 4)
        self.texts.append(caption)
        for number_in_row in range(0, count // 2):
            tmp = Node(self, str(start_number + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey)
            self.terminals.append(tmp)

        for number_in_row in range(count // 2, count):
            tmp = Node(self, str(start_number + shift + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * (number_in_row - count // 2), basey + size + gap)
            self.terminals.append(tmp)

    def terminal_print_face_up(self, painter, basex, basey, count, name, size=22, gap=2, start_number=0, shift=0):
        painter.setFont(self.font)
        # QText
        painter.drawText(basex - size // 2 - gap, basey - size - gap, name)

        for number_in_row in range(0, count // 2):
            tmp = Node(self, str(start_number + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey)
            self.terminals.append(tmp)
            tmp.setParentItem(self)

        for number_in_row in range(count // 2, count):
            tmp = Node(self, str(start_number + shift + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * (number_in_row - count // 2), basey + size + gap)
            self.terminals.append(tmp)
            tmp.setParentItem(self)

    def terminal_print_face_down(self, painter, basex, basey, count, name, size=22, gap=2, start_number=0, shift=0):
        painter.setFont(self.font)
        painter.drawText(basex - size // 2 - gap, basey - size - gap, name)

        for number_in_row in range(0, count // 2):
            tmp = Node(self, str(start_number + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey + size + gap)
            tmp.setParentItem(self)
            self.terminals.append(tmp)
        for number_in_row in range(count // 2, count):
            tmp = Node(self, str(start_number + shift + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * (number_in_row - count // 2), basey)
            tmp.setParentItem(self)
            self.terminals.append(tmp)

    def terminal_print_one_line(self, painter, basex, basey, count, name, size=22, gap=2, start_number=0,
                                tag_direction=0):
        painter.setFont(self.font)
        if tag_direction == 0:
            painter.drawText(basex - size * 2 - gap * 4, basey - size // 2 + 10, name)
        else:
            painter.drawText(basex + (size + gap) * count - 5, basey - size // 2 + 10, name)

        for number_in_row in range(0, count):
            tmp = Node(self, str(start_number + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey)
            tmp.setParentItem(self)
            self.terminals.append(tmp)

    def print_greed(self, painter):
        painter.drawLine(0, -400, 0, 400, )
        painter.drawLine(-800, 0, 800, 0, )
        for x in range(-800, 800, 10):
            painter.drawLine(x, -400, x, 400, )
        for y in range(-400, 400, 10):
            painter.drawLine(-800, y, 800, y, )


class Base_for_module(QGraphicsItem):

    def __init__(self):
        QGraphicsItem.__init__(self)
        self.terminals = []
        self.terminals_dict = {}
        self.texts = []

        self.font = QFont()
        self.font.setPixelSize(16)

    def get_terminal(self, terminal: str):
        return self.terminals_dict.get(terminal, None)

    def terminal_print_face_up(self, basex, basey, count, name, size=22, gap=2, start_number=0, shift=0):
        caption = QGraphicsSimpleTextItem()
        caption.setText(name)
        caption.setFont(self.font)
        caption.setPos(basex - size // 2 - gap, basey - size - gap * 4)
        self.texts.append(caption)
        for number_in_row in range(0, count // 2):
            tmp = Node(self, str(start_number + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey)
            self.terminals.append(tmp)
            self.terminals_dict[name + " " + str(start_number + number_in_row + 1)] = tmp

        for number_in_row in range(count // 2, count):
            tmp = Node(self, str(start_number + shift + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * (number_in_row - count // 2), basey + size + gap)
            self.terminals.append(tmp)
            self.terminals_dict[name + " " + str(start_number + shift + number_in_row + 1)] = tmp

    def terminal_print_face_down(self, basex, basey, count, name, size=22, gap=2, start_number=0, shift=0):
        caption = QGraphicsSimpleTextItem()
        caption.setText(name)
        caption.setFont(self.font)
        caption.setPos(basex - size // 2 - gap, basey - size - gap * 4)
        self.texts.append(caption)

        for number_in_row in range(0, count // 2):
            tmp = Node(self, str(start_number + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey + size + gap)
            tmp.setParentItem(self)
            self.terminals_dict[name + " " + str(start_number + number_in_row + 1)] = tmp
        for number_in_row in range(count // 2, count):
            tmp = Node(self, str(start_number + shift + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * (number_in_row - count // 2), basey)
            tmp.setParentItem(self)
            self.terminals_dict[name + " " + str(start_number + shift + number_in_row + 1)] = tmp

    def terminal_print_one_line(self, basex, basey, count, name, size=22, gap=2, start_number=0,
                                tag_direction=0):

        if tag_direction == 0:
            caption = QGraphicsSimpleTextItem()
            caption.setText(name)
            caption.setFont(self.font)
            caption.setPos(basex - size * 2 - gap * 4, basey - size // 2 + 10)
            self.texts.append(caption)
            # painter.drawText(basex - size * 2 - gap * 4, basey - size // 2 + 10, name)
        else:
            caption = QGraphicsSimpleTextItem()
            caption.setText(name)
            caption.setFont(self.font)
            caption.setPos(basex + (size + gap) * count - 5, basey - size // 2 + 10)
            self.texts.append(caption)
            # painter.drawText(basex + (size + gap) * count - 5, basey - size // 2 + 10, name)

        for number_in_row in range(0, count):
            tmp = Node(self, str(start_number + number_in_row + 1), name, size=size)
            tmp.setPos(basex + (size + gap) * number_in_row, basey)
            tmp.setParentItem(self)
            self.terminals.append(tmp)
            self.terminals_dict[name + " " + str(start_number + number_in_row + 1)] = tmp

    # def paint(self, painter, option, widget):
    #     for nd in self.terminals:
    #         nd.setParentItem(self)
    #
    #     for tx in self.texts:
    #         tx.setParentItem(self)

    def print_greed(self, painter):
        painter.drawLine(0, -400, 0, 400, )
        painter.drawLine(-800, 0, 800, 0, )
        for x in range(-800, 800, 10):
            painter.drawLine(x, -400, x, 400, )
        for y in range(-400, 400, 10):
            painter.drawLine(-800, y, 800, y, )

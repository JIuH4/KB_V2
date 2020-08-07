from PySide2.QtWidgets import (QHeaderView,
                               QTableWidget,
                               QAbstractItemView, )


class Table_widget(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self)
        self.items = 0

        self.setColumnCount(3)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeaderLabels(["n1", "n2", "n3"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setDefaultSectionSize(45)


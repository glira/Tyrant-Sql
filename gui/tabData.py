# *-* coding: utf-8 *-*

from PySide6 import QtWidgets, QtCore


class tabData(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(tabData, self).__init__()
        self.Wdg = parent
        self.Layout = QtWidgets.QHBoxLayout()
        self.Split = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.DBExplorer = TreeView()
        self.Split.insertWidget(0, self.DBExplorer)
        self.Layout.addWidget(self.Split)
        self.setLayout(self.Layout)

        #signals
        self.DBExplorer.itemClicked.connect(self.getTables)

    def getTables(self, DB=None):
        self.SqlMap = self.Wdg.SQLMap
        TBName = DB.text(0)
        if DB.parent() is None:
            if DB.childCount() == 0:
                self.SqlMap.getTables(TBName, DB)
            else:
                try:
                    if not self.DBExplorer.isItemExpanded(DB):
                        self.DBExplorer.expandItem(DB)
                    else:
                        self.DBExplorer.collapseItem(DB)
                except:
                    pass
        else:
            self.SqlMap.getTableContent(DB)

    def addTable(self, DB, Text):
        self.DBExplorer.addTable(DB, Text)

    def addDB(self, Text):
        self.DBExplorer.addDB(Text)

    def Clear(self):
        self.DBExplorer.clear()


class TreeView(QtWidgets.QTreeWidget):

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.headerItem().setText(0, 'Databases')

    def addDB(self, Text):
        ID = self.topLevelItemCount()
        NewDB = QtWidgets.QTreeWidgetItem()
        NewDB.setText(0, Text)
        self.insertTopLevelItem(ID, NewDB)

    def addTable(self, DB, Text):
        NewTB = QtWidgets.QTreeWidgetItem(DB)
        NewTB.setText(0, Text)
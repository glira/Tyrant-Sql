# *-* coding: utf-8 *-*

from PySide import QtGui
from PySide import QtCore


class tabData(QtGui.QWidget):

    def __init__(self, parent=None):
        super(tabData, self).__init__()
        self.Wdg = parent
        self.Layout = QtGui.QHBoxLayout()
        self.Split = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.DBExplorer = TreeView()
        self.EdtTest = QtGui.QTextEdit()
        self.EdtTest.setPlainText('Tables will be here soon')
        self.Split.insertWidget(0, self.DBExplorer)
        self.Split.insertWidget(1, self.EdtTest)
        self.Split.setStretchFactor(0, 8)
        self.Split.setStretchFactor(1, 20)
        self.Layout.addWidget(self.Split)
        self.setLayout(self.Layout)

        #signals
        self.DBExplorer.itemClicked.connect(self.getTables)

    def getTables(self, DB=None):
        self.SqlMap = self.Wdg.SQLMap
        TBName = DB.text(0)
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

    def addTable(self, DB, Text):
        self.DBExplorer.addTable(DB, Text)

    def addDB(self, Text):
        self.DBExplorer.addDB(Text)

    def Clear(self):
        self.DBExplorer.clear()


class TreeView(QtGui.QTreeWidget):

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.headerItem().setText(0, 'Databases')

    def addDB(self, Text):
        ID = self.topLevelItemCount()
        NewDB = QtGui.QTreeWidgetItem()
        NewDB.setText(0, Text)
        self.insertTopLevelItem(ID, NewDB)

    def addTable(self, DB, Text):
        NewTB = QtGui.QTreeWidgetItem(DB)
        NewTB.setText(0, Text)






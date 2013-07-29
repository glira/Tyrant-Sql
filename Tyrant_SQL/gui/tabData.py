# *-* coding: utf-8 *-*

from PySide import QtGui
from PySide import QtCore


class tabData(QtGui.QWidget):

    def __init__(self):
        super(tabData, self).__init__()
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

    def addDB(self, Text):
        self.DBExplorer.addDB(Text)

    def addTable(self, DB, Text):
        self.DBExplorer.addTable(DB, Text)


class TreeView(QtGui.QTreeWidget):

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.headerItem().setText(0, 'Databases')

    def addDB(self, Text):
        ID = self.topLevelItemCount()
        NewDB = QtGui.QTreeWidgetItem()
        NewDB.setText(0, Text)
        self.insertTopLevelItem(ID, NewDB)
        print('Added table ' + str(Text))

    def addTable(self, DB, Text):
        CurrentDB = self.topLevelItem(DB)
        NewTB = QtGui.QTreeWidgetItem(CurrentDB)
        NewTB.setText(0, Text)






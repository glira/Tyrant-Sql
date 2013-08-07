# *-* coding: utf-8 *-*

from PySide import QtGui


class Raw_Data(QtGui.QPlainTextEdit):

    def __init__(self, parent=None):
        super(Raw_Data, self).__init__()
        self.Wdg = parent
        self.setReadOnly(True)
        self.setLineWrapMode(self.NoWrap)
        self.textChanged.connect(self.TextChanged)

    def TextChanged(self):
        self.Wdg.RawView.setPlainText(self.toPlainText())
        Cursor = QtGui.QTextCursor()
        self.Wdg.RawView.moveCursor(Cursor.End)
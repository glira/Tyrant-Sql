# *-* coding: utf-8 *-*

from PySide6 import QtWidgets, QtGui


class Raw_Data(QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        super(Raw_Data, self).__init__()
        self.Wdg = parent
        self.setReadOnly(True)
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.textChanged.connect(self.TextChanged)

    def TextChanged(self):
        self.Wdg.RawView.setPlainText(self.toPlainText())
        cursor = self.Wdg.RawView.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        self.Wdg.RawView.setTextCursor(cursor)
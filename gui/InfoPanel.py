# *-* coding: utf-8 *-*

from PySide import QtGui


class InfoPanel(QtGui.QPlainTextEdit):

    def __init__(self):
        super(InfoPanel, self).__init__()
        self.setReadOnly(True)

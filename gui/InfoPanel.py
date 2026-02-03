# *-* coding: utf-8 *-*

from PySide6 import QtWidgets


class InfoPanel(QtWidgets.QPlainTextEdit):

    def __init__(self):
        super(InfoPanel, self).__init__()
        self.setReadOnly(True)

# *-* coding: utf-8 *-*

from PySide import QtGui
from PySide import QtCore

class Raw_Data(QtGui.QPlainTextEdit):

    def __init__(self, parent=None):
        super(Raw_Data, self).__init__()
        self.setReadOnly(True)

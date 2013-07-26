# -*- coding: utf-8 -*-
import sys

from PySide.QtGui import QApplication, QMainWindow
from gui.Ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Tyrant = MainWindow()
    Tyrant.setWindowTitle('Tyrant SQL')
    Tyrant.show()
    app.exec_()

# -*- coding: utf-8 -*-

import webbrowser

from PySide6 import QtCore, QtWidgets, QtGui


from core.TestPython import TestPython
from gui.Preferences import Ui_Preferences
from gui.InfoPanel import InfoPanel
from gui.Raw_Data import Raw_Data
from core.SqlMap import SqlMap
from gui.tabData import tabData


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(618, 654)
        self.Frame = QtWidgets.QFrame()
        self.Layout = QtWidgets.QHBoxLayout()
        self.gbxInfo = QtWidgets.QGroupBox()
        self.gbxInfo.setTitle('Information')
        self.Info = InfoPanel()
        self.InfoLayout = QtWidgets.QHBoxLayout()
        self.InfoLayout.addWidget(self.Info)
        self.gbxInfo.setLayout(self.InfoLayout)
        self.Wdg = QtWidgets.QVBoxLayout()
        self.Frame.setLayout(self.Layout)
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 621, 611))
        self.tabAnalyze = QtWidgets.QWidget()
        self.lblTarget = QtWidgets.QLabel(self.tabAnalyze)
        self.lblTarget.setGeometry(QtCore.QRect(10, 20, 64, 21))
        self.edtTarget = QtWidgets.QLineEdit(self.tabAnalyze)
        self.edtTarget.setGeometry(QtCore.QRect(90, 10, 441, 33))
        self.btnAnalyze = QtWidgets.QPushButton(self.tabAnalyze)
        self.btnAnalyze.setGeometry(QtCore.QRect(540, 10, 71, 31))
        self.lblMethod = QtWidgets.QLabel(self.tabAnalyze)
        self.lblMethod.setGeometry(QtCore.QRect(10, 60, 64, 21))
        self.cbxMethod = QtWidgets.QComboBox(self.tabAnalyze)
        self.cbxMethod.setGeometry(QtCore.QRect(90, 60, 76, 29))
        self.cbxMethod.addItem("")
        self.cbxMethod.addItem("")
        self.lblPostData = QtWidgets.QLabel(self.tabAnalyze)
        self.lblPostData.setGeometry(QtCore.QRect(10, 100, 71, 21))
        self.lblPostData.setVisible(False)
        self.edtPostData = QtWidgets.QLineEdit(self.tabAnalyze)
        self.edtPostData.setGeometry(QtCore.QRect(90, 100, 441, 33))
        self.edtPostData.setVisible(False)
        self.tabWidget.addTab(self.tabAnalyze, "")
        self.tabRawData = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tabRawData, "")
        self.tabData = tabData(self)
        self.tabWidget.addTab(self.tabData, 'Data')
        self.RawData = Raw_Data(self)
        self.RawView = QtWidgets.QPlainTextEdit()
        self.RawView.setReadOnly(True)
        self.RDLayout = QtWidgets.QHBoxLayout(self.tabRawData)
        self.RDLayout.addWidget(self.RawData)
        self.RDLayout.addWidget(self.RawView)
        MainWindow.setCentralWidget(self.Frame)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 27))
        self.menubar.setObjectName("menubar")
        self.menuTyrant = QtWidgets.QMenu(self.menubar)
        self.menuTyrant.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSql_Map_Hlelp = QtGui.QAction(MainWindow)
        self.actionOnline_Help = QtGui.QAction(MainWindow)
        self.actionLicense = QtGui.QAction(MainWindow)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setText('Preferences')
        self.menuTyrant.addSeparator()
        self.menuTyrant.addAction(self.actionPreferences)
        self.menuTyrant.addSeparator()
        self.menuTyrant.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionSql_Map_Hlelp)
        self.menuHelp.addAction(self.actionOnline_Help)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionLicense)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuTyrant.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.Wdg.addWidget(self.tabWidget)
        self.Wdg.addWidget(self.gbxInfo)
        self.Wdg.setStretchFactor(self.tabWidget, 10)
        self.Wdg.setStretchFactor(self.gbxInfo, 5)
        self.Layout.addLayout(self.Wdg)
        self.RawData.hide()
        Test = TestPython()
        Working = Test.TestVersion()
        Test2 = TestPython(1)
        Working = Test2.TestVersion()
        if not Working:
            Msg = QtWidgets.QMessageBox()
            Msg.information(self, 'Python',
                    'Tyrant failed to find Python 3.10 or higher \n Goto'
                    + ' preferences!!')

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        #to hide or show post data
        self.cbxMethod.currentIndexChanged.connect(self.ShowHidePostData)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionPreferences.triggered.connect(self.OpenPreferences)
        self.SQLMap = SqlMap(self)
        self.btnAnalyze.clicked.connect(self.Analyze)
        self.actionSql_Map_Hlelp.triggered.connect(self.SqlMapHelp)
        self.actionAbout.triggered.connect(self.About)
        self.actionLicense.triggered.connect(self.License)
        self.actionOnline_Help.triggered.connect(self.TyrantHelp)
        self.actionExit.triggered.connect(MainWindow.close)

    def SqlMapHelp(self):
        Web = webbrowser.get()
        Web.open('http://www.sqlmap.org/')

    def TyrantHelp(self):
        Web = webbrowser.get()
        Web.open('https://github.com/glira/Tyrant-Sql')

    def License(self):
        Web = webbrowser.get()
        Web.open('http://www.gnu.org/licenses/gpl-3.0.txt')

    def About(self):
        Web = webbrowser.get()
        Web.open('https://github.com/glira/Tyrant-Sql')

    def Analyze(self):
        self.SQLMap.IdentifyDB()

    def ShowHidePostData(self, ID):
        if ID == 0:
            self.edtPostData.setVisible(False)
            self.lblPostData.setVisible(False)
            self.edtPostData.setText('')
        else:
            self.edtPostData.setVisible(True)
            self.lblPostData.setVisible(True)

    def OpenPreferences(self):
        self.Pre = Ui_Preferences()
        self.Dialog = QtWidgets.QDialog()
        self.Pre.setupUi(self.Dialog, self)
        self.Dialog.exec()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        self.lblTarget.setText("Target:")
        self.btnAnalyze.setText("Analyze")
        self.lblMethod.setText("Method:")
        self.cbxMethod.setItemText(0, "GET")
        self.cbxMethod.setItemText(1, "POST")
        self.lblPostData.setText("Post Data:")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAnalyze), "Target")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRawData), "Raw Data")
        self.menuTyrant.setTitle("Tyrant")
        self.menuHelp.setTitle("Help")
        self.actionSql_Map_Hlelp.setText("Sql Map  Help")
        self.actionOnline_Help.setText("Online Help")
        self.actionLicense.setText("License")
        self.actionAbout.setText("About")
        self.actionExit.setText("Exit")
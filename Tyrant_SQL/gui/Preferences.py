# *-* coding: utf-8 *-*
from PySide import QtCore, QtGui
from core.Settings import TyrantSettings


class Ui_Preferences(object):
    def setupUi(self, Form, Wdg=None):
        self.Form = Form
        Form.resize(450, 550)
        Form.setMaximumSize(450, 550)
        Form.setMinimumSize(450, 550)
        Form.setObjectName('Form')
        self.Layout = QtGui.QVBoxLayout()
        self.HLay = QtGui.QHBoxLayout()
        self.btnSave = QtGui.QPushButton()
        self.btnSave.setText('Save')
        self.btnCancel = QtGui.QPushButton()
        self.btnCancel.setText('Cancel')
        self.HLay.addWidget(self.btnCancel)
        self.HLay.addWidget(self.btnSave)
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 20, 371, 381))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabPython = QtGui.QWidget()
        self.lblPython = QtGui.QLabel(self.tabPython)
        self.lblPython.setGeometry(QtCore.QRect(10, 10, 64, 21))
        self.edtPython = QtGui.QLineEdit(self.tabPython)
        self.edtPython.setGeometry(QtCore.QRect(70, 0, 231, 33))
        self.lblPythonSupp = QtGui.QLabel(self.tabPython)
        self.lblPythonSupp.setGeometry(QtCore.QRect(50, 40, 251, 21))
        self.tabWidget.addTab(self.tabPython, "")
        self.tab_2 = QtGui.QWidget()
        self.gbxProxy = QtGui.QGroupBox(self.tab_2)
        self.gbxProxy.setGeometry(QtCore.QRect(0, 0, 331, 381))
        self.edtIpProxy = QtGui.QLineEdit(self.gbxProxy)
        self.edtIpProxy.setGeometry(QtCore.QRect(50, 90, 231, 33))
        self.edtPortProxy = QtGui.QLineEdit(self.gbxProxy)
        self.edtPortProxy.setGeometry(QtCore.QRect(50, 130, 101, 33))
        self.cbxTorType = QtGui.QComboBox(self.gbxProxy)
        self.cbxTorType.setGeometry(QtCore.QRect(160, 130, 100, 33))
        self.cbxTorType.addItems(['HTTP', 'SOCKS4', 'SOCKS5'])
        self.lblPort = QtGui.QLabel(self.gbxProxy)
        self.lblPort.setGeometry(QtCore.QRect(10, 140, 64, 21))
        self.lblIP = QtGui.QLabel(self.gbxProxy)
        self.lblIP.setGeometry(QtCore.QRect(10, 100, 81, 21))
        self.rbtnProxy = QtGui.QRadioButton(self.gbxProxy)
        self.rbtnProxy.setGeometry(QtCore.QRect(10, 30, 200, 26))
        self.rbtnProxy.setText("Don't use proxy")
        self.rbtnHTTP = QtGui.QRadioButton(self.gbxProxy)
        self.rbtnHTTP.setGeometry(QtCore.QRect(10, 60, 109, 26))
        self.rbtnHTTP.setChecked(True)
        self.rbtnHTTP.setObjectName("radioButton")
        self.rbtnSocks = QtGui.QRadioButton(self.gbxProxy)
        self.rbtnSocks.setGeometry(QtCore.QRect(150, 60, 109, 26))
        self.rbtnSocks.setObjectName("radioButton_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.Layout.addWidget(self.tabWidget)
        Form.setLayout(self.Layout)
        self.Layout.addLayout(self.HLay)
        self.Settings = TyrantSettings(self)
        self.btnSave.clicked.connect(self.Save)
        self.btnCancel.clicked.connect(Form.reject)
        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.Settings.Populate_Prefs()
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.rbtnProxy.toggled.connect(self.ProxyInfo)
        self.rbtnHTTP.toggled.connect(self.ProxyInfo)
        self.rbtnSocks.toggled.connect(self.ProxyInfo)

    def Save(self):
        self.Settings.Save_Prefs()
        self.Form.reject()

    def ProxyInfo(self):
        if self.rbtnProxy.isChecked():
            self.lblIP.hide()
            self.lblPort.hide()
            self.edtIpProxy.hide()
            self.edtPortProxy.hide()
            self.cbxTorType.hide()
        else:
            self.lblIP.show()
            self.lblPort.show()
            self.edtIpProxy.show()
            self.edtPortProxy.show()
            self.cbxTorType.hide()
            self.edtIpProxy.setEnabled(True)
        if self.rbtnSocks.isChecked():
            self.edtIpProxy.setText('127.0.0.1')
            self.edtIpProxy.setEnabled(False)
            self.cbxTorType.show()

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Preferences",
             None, QtGui.QApplication.UnicodeUTF8))
        self.lblPython.setText(QtGui.QApplication.translate("Form", "Python:",
            None, QtGui.QApplication.UnicodeUTF8))
        self.lblPythonSupp.setText(QtGui.QApplication.translate
            ("Form", "Tyrant support Python >=2.5 and <2.8", None,
            QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPython),
            QtGui.QApplication.translate("Form", "Python", None,
            QtGui.QApplication.UnicodeUTF8))
        self.gbxProxy.setTitle(QtGui.QApplication.translate
            ("Form", "Web Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPort.setText(QtGui.QApplication.translate
            ("Form", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblIP.setText(QtGui.QApplication.translate
            ("Form", "IP:", None, QtGui.QApplication.UnicodeUTF8))
        self.rbtnHTTP.setText(QtGui.QApplication.translate
            ("Form", "HTTP Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.rbtnSocks.setText(QtGui.QApplication.translate
            ("Form", "Tor Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
            QtGui.QApplication.translate("Form", "Proxy",
            None, QtGui.QApplication.UnicodeUTF8))
# *-* coding: utf-8 *-*

from PySide6 import QtCore


class TyrantSettings(object):

    def __init__(self, Preferences=None):
        self.Settings = QtCore.QSettings('Tyrant.cfg',
                                                    QtCore.QSettings.IniFormat)
        self.Pref = Preferences

    def Populate_Prefs(self):
        print('Populating preferences')
        self.Pref.edtPython.setText(str(self.Settings.value
                                                ('Python/PythonPath', '')))
        self.Pref.edtSqlMap.setText(str(self.Settings.value
                                                ('SQLMap/SqlMapPath', 'SQL_Map/sqlmap.py')))
        self.Pref.edtIpProxy.setText(str(self.Settings.value
                                                ('SQLMap/IPProxy', '')))
        self.Pref.edtPortProxy.setText(str(self.Settings.value
                                                ('SQLMap/PortProxy', '')))
        self.Pref.rbtnProxy.setChecked(self.useBool(self.Settings.value
                                                ('SQLMap/UseProxy', 'True')))
        self.Pref.rbtnHTTP.setChecked(self.useBool(self.Settings.value
                                                ('SQLMap/UseHTTP')))
        self.Pref.rbtnSocks.setChecked(self.useBool(self.Settings.value
                                                ('SQLMap/UseTor')))
        self.Pref.cbxTorType.setCurrentIndex(int(self.Settings.value
                                                ('SQLMap/TorTypeIndex', 0)))
        self.ProxyHideShow()

    def ProxyHideShow(self):
        if self.Pref.rbtnProxy.isChecked():
            self.Pref.lblIP.hide()
            self.Pref.lblPort.hide()
            self.Pref.edtIpProxy.hide()
            self.Pref.edtPortProxy.hide()
            self.Pref.cbxTorType.hide()
        else:
            self.Pref.lblIP.show()
            self.Pref.lblPort.show()
            self.Pref.edtIpProxy.show()
            self.Pref.edtPortProxy.show()
            self.Pref.cbxTorType.hide()
            self.Pref.edtIpProxy.setEnabled(True)
        if self.Pref.rbtnSocks.isChecked():
            self.Pref.cbxTorType.show()
            self.Pref.edtIpProxy.setText('127.0.0.1')
            self.Pref.edtIpProxy.setEnabled(False)

    def useBool(self, Text):
        if Text == 'True':
            return True
        else:
            return False

    def Save_Prefs(self):
        print('Saving preferences')
        self.Settings.setValue('Python/PythonPath', self.Pref.edtPython.text())
        self.Settings.setValue('SQLMap/SqlMapPath', self.Pref.edtSqlMap.text())
        self.Settings.setValue('SQLMap/IPProxy', self.Pref.edtIpProxy.text())
        self.Settings.setValue('SQLMap/PortProxy',
                                                self.Pref.edtPortProxy.text())
        self.Settings.setValue('SQLMap/UseProxy',
                                        str(self.Pref.rbtnProxy.isChecked()))
        self.Settings.setValue('SQLMap/UseHTTP',
                                        str(self.Pref.rbtnHTTP.isChecked()))
        self.Settings.setValue('SQLMap/UseTor',
                                        str(self.Pref.rbtnSocks.isChecked()))
        self.Settings.setValue('SQLMap/TorTypeIndex',
                                    str(self.Pref.cbxTorType.currentIndex()))
        self.Settings.setValue('SQLMap/TorType',
                                        str(self.Pref.cbxTorType.currentText()))
        self.Settings.sync()
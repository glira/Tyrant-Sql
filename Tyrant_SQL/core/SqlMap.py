# *-* coding: utf-8 *-*

from PySide import QtGui
from PySide import QtCore

from core.Resources import Resources



class SqlMap(object):

    def __init__(self, parent=None):
        print('Created SQLMap manipulator')
        self.SQLFile = QtCore.QFile('SQL_Map/sqlmap.py')
        self.Wdg = parent
        self.SqlMapExist()
        self.Resources = Resources()
        self.Python = self.Resources.getPref('Python')
        self.Proc = QtCore.QProcess()
        self.Target = ''


    def SqlMapExist(self):
        if not self.SQLFile.exists():
            Info = QtGui.QMessageBox()
            Info.information(self.Wdg, 'SQLMap ERROR',
                'Tyrant SQL cannot find sqlmap.py file')

    def IdentifyDB(self):
        self.Target = self.Wdg.edtTarget.text()
        argIdentify = ['SQL_Map/sqlmap.py', '-u', str(self.Target), '--dbs',
            '--answers=skip test=N, include all tests=N' +
            ', keep testing the=Y']
        print argIdentify
        self.Proc.readyReadStandardOutput.connect(self.Output)
        self.Proc.start(self.Python, argIdentify,
                                    mode=QtCore.QIODevice.ReadWrite)



    def Output(self):
        Out = (str(self.Proc.readAllStandardOutput()))
        self.Wdg.RawData.appendPlainText(Out)

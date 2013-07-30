# *-* coding: utf-8 *-*

from PySide import QtGui
from PySide import QtCore
from threading import Thread

from core.Resources import Resources
from core.RawAnalyzer import RawAnalyzer


class SqlMap(object):

    def __init__(self, parent=None):
        print('Created SQLMap manipulator')
        self.SQLFile = QtCore.QFile('SQL_Map/sqlmap.py')
        self.Wdg = parent
        self.RawAnalyzer = RawAnalyzer(self.Wdg)
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
            ', keep testing the=Y', '--batch']
        self.getDBInfo()
        self.Run(argIdentify)
        self.Proc.finished.connect(self.getDBInfo)

    def Run(self, Arg):
        self.Th = Thread(self._Run(Arg))
        self.Th.start()

    #run the sqlmap
    def _Run(self, Arg):

        self.Proc.readyReadStandardOutput.connect(self.Output)
        self.Proc.start(self.Python, Arg,
                                    mode=QtCore.QIODevice.ReadWrite)

    #read the output and find the DBMS version and the databases
    def getDBInfo(self, a=None):
        if (a is not None) & (a != 0):
            Info = QtGui.QMessageBox()
            Info.information(self.Wdg, 'DB Analyzer', 'The databases was not \n'
             + 'analyzed. Please, restart the analyze.')
        elif a == 0:
            self.RawAnalyzer.getDBInfo()

    def Output(self):
        Out = (str(self.Proc.readAllStandardOutput()))
        if len(Out) > 1:
            self.Wdg.RawData.appendPlainText(Out)

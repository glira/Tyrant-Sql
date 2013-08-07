# -*- coding: utf-8 -*-

from PySide.QtCore import QProcess
from PySide import QtCore
from core.Resources import Resources


class TestPython(object):

    def __init__(self, ID=None):
        self.Test = QProcess()
        self.ID = ID
        #a and b to test if i get a output or command error
        self.a = True
        self.Settings = QtCore.QSettings('Tyrant.cfg',
                                                    QtCore.QSettings.IniFormat)

    def TestVersion(self):
        print('Test python version')
        self.Test.readyReadStandardError.connect(self.getOutput)
        self.Test.readyReadStandardOutput.connect(self.getOutput)
        if self.ID is not None:
            self.Test.error.connect(self.Error)
        #if i have a custom pythonpath, i'll use it here
        Res = Resources()
        Python = Res.getPref('Python')
        #test if is a pythonpath, if not open a default
        if len(Python) < 5:
            Python = 'python'
        self.Test.start(Python, ['-V'])
        self.Test.waitForFinished()
        self.Test.terminate()
        if (self.a is False) & (self.ID is None):
            #test a diferent command to run python 2.7
            a = self.TestVersion2()
            print a
            return a
        elif self.a:
            #say to program that python is working
            print('Python version found')
            self.Settings.setValue('Python/PythonPath', str(Python))
            self.Settings.sync()
            return True
        elif ((self.ID is not None) & (self.a is False)):
            return False

    def Error(self):
        self.a = False

    def TestVersion2(self):
        print('Testing python version 2')
        self.Test.readyReadStandardError.connect(self.getOutput)
        Python = 'python2.7'
        self.Test.start(Python, ['-V'])
        self.Test.waitForStarted()
        self.Test.waitForFinished()
        self.Test.terminate()
        if (self.a is False):
            #say thar python is not working
            return False
        else:
            self.Settings.setValue('Python/PythonPath', str(Python))
            self.Settings.sync()
            return True

    def getOutput(self):
        print('efsdfsfg')
        Out = str(self.Test.readAllStandardError())
        print(Out)
        if Out > 'Python 2.8':
            self.a = False
            return
        self.a = True
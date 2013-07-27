# -*- coding: utf-8 -*-

from PySide.QtCore import QProcess

class TestPython(object):

    def __init__(self):
        self.Test = QProcess()
        #a and b to test if i get a output or command error
        self.a = True

    def TestVersion(self):
        print('Test python version')
        self.Test.readyReadStandardError.connect(self.getOutput)
        self.Test.start('python', ['-V'])
        self.Test.waitForStarted()
        self.Test.waitForFinished()
        self.Test.terminate()
        if (self.a is False):
            #test a diferent command to run python 2.7
            a = self.TestVersion2()
            print a
            return a
        else:
            #say to program that python is working
            print('Print version found')
            return True


    def TestVersion2(self):
        print('Testing python version 2')
        self.Test.readyReadStandardError.connect(self.getOutput)
        self.Test.start('python2.7', ['-V'])
        self.Test.waitForStarted()
        self.Test.waitForFinished()
        self.Test.terminate()
        if (self.a is False):
            #say thar python is not working
            return False
        else:
            return True


    def getOutput(self):
        Out = str(self.Test.readAllStandardError())
        print(Out)
        if Out > 'Python 2.8':
            self.a = False
            return
        self.a = True

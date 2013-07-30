# *-* coding: utf-8 *-*

from PySide import QtCore
from PySide import QtGui


class RawAnalyzer(object):

    def __init__(self, parent=None):
        self.Wdg = parent
        self.DBMS = ''
        self.QtdDBs = 0
        self.DBNames = []
        self.Info = self.Wdg.Info

    def getDBInfo(self):
        print('[INFO]Getting DB info')
        self.Info.appendPlainText('Getting Database information...')
        self.DBMS = self.getDBMS()
        if self.DBMS is False:
            self.Info.appendPlainText('''[ERROR]Failed to find Database
                information!!!\n
                [ERROR]Please, check if this site is vulnerable and see the raw
                data for more information.''')
            return
        else:
            self.Info.appendPlainText('''[INFO] %s DBMS was found'''
            % (self.DBMS))
        self.QtdDBs = self.getDatabases()
        if self.QtdDBs == 0:
            self.Info.appendPlainText('''[Warning] Failed to count databases\n
                [Warning]See the raw data to check if was found some database
                this analyze is not goig to work.\n
                [Warning]Please, restart''')
            return
        else:
            self.Info.appendPlainText('''[INFO] %d databases were found'''
                % (self.QtdDBs))
        self.DBNames = self.getDBNames()
        for i in range(self.QtdDBs):
            Out = '[INFO]\t Table '
            Out += str(i) + ': '
            Out += self.DBNames[i]
            self.Info.appendPlainText(Out)

    def getDBNames(self):
        DBNames = []
        Edt = self.Wdg.RawData
        Cursor = QtGui.QTextCursor()
        for DB in range(self.QtdDBs):
            Edt.find('[*]')
            Edt.moveCursor(Cursor.StartOfLine)
            Edt.moveCursor(Cursor.EndOfLine, Cursor.KeepAnchor)
            Text = Edt.textCursor().selectedText()
            Text = Text.split()
            Text = Text[-1]
            DBNames.append(str(Text))
        return DBNames

    def getDatabases(self):
        QtdDBs = 0
        Edt = self.Wdg.RawData
        Cursor = QtGui.QTextCursor()
        Edt.find('available databases')
        Edt.moveCursor(Cursor.StartOfLine)
        Edt.moveCursor(Cursor.EndOfLine, Cursor.KeepAnchor)
        Text = Edt.textCursor().selectedText()
        Text = Text.split()
        Text = Text[-1]
        QtdDBs = Text[1]
        QtdDBs = int(QtdDBs)
        return (QtdDBs)


    def getDBMS(self):
        Edt = self.Wdg.RawData
        Cursor = QtGui.QTextCursor()
        Edt.moveCursor(Cursor.Start)
        Edt.find('[INFO] the back-end DBMS is')
        Edt.moveCursor(Cursor.StartOfLine)
        Edt.moveCursor(Cursor.EndOfLine, Cursor.KeepAnchor)
        Text = Edt.textCursor().selectedText()
        Text = Text.split()
        #if cant find dbms, return false to after check this error
        if len(Text) > 0:
            return(Text[-1])
        else:
            return False

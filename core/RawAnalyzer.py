# -*- coding: utf-8 -*-

from PySide6 import QtGui, QtWidgets
import csv
import re


class RawAnalyzer(object):

    def __init__(self, parent=None):
        self.Wdg = parent
        self.DBMS = ''
        self.QtdDBs = 0
        self.DBNames = []
        self.QtdTBs = 0
        self.Tables = []
        self.Info = self.Wdg.Info
        self.TabData = self.Wdg.tabData
        self.CurrentDB = None
        self.TBName = ''

    def getTBContent(self, TBName):
        self.TBName = TBName
        self.getTBEntries()

    def getTBEntries(self):
        Edt = self.Wdg.RawData
        Edt.find('dumped to CSV file')
        cursor = Edt.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
        Edt.setTextCursor(cursor)
        Text = Edt.textCursor().selectedText()
        Text = Text.split('SQL_Map')
        Text = Text[-1]
        Text = Text[:-1]
        SQL = 'SQL_Map'
        Text = SQL + Text
        print(Text)
        self.DrawTable(Text)

    def DrawTable(self, File):
        try:
            Wdg = self.Wdg.tabData.Split.widget(1)
            if Wdg:
                Wdg.hide()
                Wdg.deleteLater()
        except Exception as e:
            print(f'Error removing old widget: {e}')
        Table = QtWidgets.QTableWidget()
        self.Wdg.tabData.Split.insertWidget(1, Table)
        self.Wdg.tabData.Split.setStretchFactor(0, 8)
        self.Wdg.tabData.Split.setStretchFactor(1, 20)
        Header = []
        try:
            with open(File, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                r = -1
                c = 0
                for row in reader:
                    Table.insertRow(Table.rowCount())
                    for column in row:
                        if Table.rowCount() == 1:
                            Table.insertColumn(Table.columnCount())
                            Header = row
                        else:
                            Item = QtWidgets.QTableWidgetItem(str(column))
                            Table.setItem(r, c, Item)
                        c += 1
                    r += 1
                    c = 0
            if Header:
                Table.setHorizontalHeaderLabels(Header)
            Header = []
            for i in range(Table.rowCount()):
                Header.append(' ')
            Table.setVerticalHeaderLabels(Header)
            self.Info.appendPlainText('[INFO]Table completely loaded.')
        except Exception as e:
            self.Info.appendPlainText(f'[ERROR]Failed to load table: {e}')

    def getDBInfo(self):
        self.Info.appendPlainText('[INFO]Getting Database information...')
        self.DBMS = self.getDBMS()
        if self.DBMS == False:
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
            Out = '[INFO]\t Database '
            Out += str(i) + ': '
            Out += self.DBNames[i]
            self.Info.appendPlainText(Out)
        for D in self.DBNames:
            self.TabData.addDB(D)
        self.Info.appendPlainText('[INFO]Databases scanning complete!')
        self.Wdg.tabWidget.setCurrentIndex(2)

    def getDBNames(self):
        DBNames = []
        Edt = self.Wdg.RawData
        # Reset cursor to start
        cursor = Edt.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
        Edt.setTextCursor(cursor)
        
        # Find the "available databases" section first
        found = Edt.find('available databases')
        if not found:
            return DBNames
        
        # Now find all database names after this point
        # Format: [*] database_name
        found_count = 0
        while found_count < self.QtdDBs:
            # Find next [*] marker
            found = Edt.find('[*]')
            if not found:
                break
            
            cursor = Edt.textCursor()
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
            Edt.setTextCursor(cursor)
            Text = Edt.textCursor().selectedText()
            
            # Extract database name - it's the word after [*]
            parts = Text.split()
            if len(parts) >= 2:
                # Skip [*] and get the database name
                db_name = parts[1] if parts[0] == '[*]' else parts[-1]
                DBNames.append(str(db_name))
                found_count += 1
            else:
                # Move cursor forward to avoid infinite loop
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.Down)
                Edt.setTextCursor(cursor)
        
        return DBNames

    def getDatabases(self):
        QtdDBs = 0
        Edt = self.Wdg.RawData
        # Find "available databases" pattern
        found = Edt.find('available databases')
        if not found:
            return 0
        
        cursor = Edt.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
        Edt.setTextCursor(cursor)
        Text = Edt.textCursor().selectedText()
        
        # Parse format: "available databases [2]:" or "available databases [2]"
        import re
        match = re.search(r'\[(\d+)\]', Text)
        if match:
            QtdDBs = int(match.group(1))
        else:
            # Fallback: try to extract number from text
            Text = Text.split()
            for part in Text:
                if part.isdigit():
                    QtdDBs = int(part)
                    break
        
        return QtdDBs

    def getDBMS(self):
        Edt = self.Wdg.RawData
        cursor = Edt.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
        Edt.setTextCursor(cursor)
        
        # Try to find DBMS info - can be in different formats
        found = Edt.find('[INFO] the back-end DBMS is')
        if not found:
            # Try alternative format: "back-end DBMS: MySQL"
            cursor = Edt.textCursor()
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
            Edt.setTextCursor(cursor)
            found = Edt.find('back-end DBMS')
        
        if found:
            cursor = Edt.textCursor()
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
            Edt.setTextCursor(cursor)
            Text = Edt.textCursor().selectedText()
            Text = Text.split()
            # Extract DBMS name (usually the last word, but could be after "is" or ":")
            if len(Text) > 0:
                # Look for DBMS name after "is" or ":"
                dbms_index = -1
                for i, word in enumerate(Text):
                    if word.lower() in ['is', ':'] and i + 1 < len(Text):
                        dbms_index = i + 1
                        break
                if dbms_index > 0:
                    return Text[dbms_index]
                else:
                    return Text[-1]
        
        return False

    def AnalyzeTables(self, DB, CurrentDB):
        self.CurrentDB = CurrentDB
        self.QtdTBs = self.getQtdTable(DB)
        if self.QtdTBs == False:
            self.Info.appendPlainText('''[ERROR]Failed to find database tables.
                [ERROR]See the raw data for more information.
                [ERROR]Please restart the analyze.''')
            return False
        else:
            self.Info.appendPlainText('[INFO]%s tables was found on database %s'
                 % (self.QtdTBs, DB))
        self.Tables = self.getTables()
        if self.Tables == False:
            self.Info.appendPlainText('[ERROR]No tables found. See the raw' +
                'data for more information.')
            return False
        self.addTables()

    def addTables(self):
        for TB in self.Tables:
            self.TabData.addTable(self.CurrentDB, TB)

    def getTables(self):
        Tables = []
        Edt = self.Wdg.RawData
        a = Edt.find('+-')
        if not a:
            return False
        for i in range(self.QtdTBs):
            Text = ''
            while len(Text) < 1:
                cursor = Edt.textCursor()
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.Down)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                Edt.setTextCursor(cursor)
                Text = Edt.textCursor().selectedText()
            Text = Text.split()
            Text = Text[1]
            Tables.append(str(Text))
        if len(Tables) == 0:
            return False
        else:
            return Tables

    def getQtdTable(self, DB):
        Edt = self.Wdg.RawData
        a = Edt.find('Database: ' + DB)
        if not a:
            return False
        a = Edt.find('[')
        if not a:
            return False
        cursor = Edt.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
        Edt.setTextCursor(cursor)
        Text = Edt.textCursor().selectedText()
        Text = Text.split()
        Text = Text[0]
        Text = Text[1:]
        if len(Text) == 0:
            return False
        else:
            return(int(Text))
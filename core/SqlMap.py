# *-* coding: utf-8 *-*

import os
from PySide6 import QtWidgets, QtCore

from core.Resources import Resources
from core.RawAnalyzer import RawAnalyzer
from core.TestPython import TestPython



class SqlMap(object):

    def __init__(self, parent=None):
        print('Created SQLMap manipulator')
        self.Wdg = parent
        self.RawAnalyzer = RawAnalyzer(self.Wdg)
        self.Res = Resources()
        self.Python = self.Res.getPref('Python')
        self.SqlMapPath = self._normalizeSqlMapPath(self.Res.getPref('SqlMapPath'))
        self.SQLFile = QtCore.QFile(self.SqlMapPath)
        self.SqlMapExist()
        self.Proc = QtCore.QProcess()
        self.Target = ''
        self.CurrentDB = None
        self.isRunning = False
        self.TBName = ''
    
    def _normalizeSqlMapPath(self, path):
        """Normalize SQLMap path - if it's a directory, append sqlmap.py"""
        if not path or path == 'None':
            return 'SQL_Map/sqlmap.py'
        
        # Remove trailing slashes
        path = path.rstrip('/')
        
        # Check if path exists
        if os.path.exists(path):
            if os.path.isdir(path):
                # It's a directory, append sqlmap.py
                sqlmap_file = os.path.join(path, 'sqlmap.py')
                return sqlmap_file if os.path.exists(sqlmap_file) else sqlmap_file
            elif os.path.isfile(path):
                # It's already a file
                return path
        
        # If path doesn't end with .py, try adding it
        if not path.endswith('.py'):
            potential_file = path + '.py'
            if os.path.exists(potential_file):
                return potential_file
        
        # Return as-is (might be relative path that will be resolved later)
        return path

    def SqlMapExist(self):
        if not self.SQLFile.exists():
            msg = f'Tyrant SQL cannot find sqlmap.py file at:\n{self.SqlMapPath}\n\n'
            msg += 'Please configure the correct path in Preferences -> Python tab -> SQLMap field\n\n'
            msg += 'You can specify:\n'
            msg += '- Full path to sqlmap.py file (e.g., /home/user/.sec/sqlmap/sqlmap.py)\n'
            msg += '- Or directory containing sqlmap.py (e.g., /home/user/.sec/sqlmap)'
            info = QtWidgets.QMessageBox()
            info.warning(self.Wdg, 'SQLMap ERROR', msg)

    def IdentifyDB(self):
        Resource = Resources()
        Test = TestPython(1)
        Working = Test.TestVersion()
        if not Working:
            Msg = QtWidgets.QMessageBox()
            Msg.information(self.Wdg, 'Python',
                    'Tyrant failed to find Python 3.10 or higher \n Goto'
                    + ' preferences!!')
            return
        self.Python = Resource.getPref('Python')
        # Update SQLMap path in case it was changed in preferences
        self.SqlMapPath = self._normalizeSqlMapPath(Resource.getPref('SqlMapPath'))
        self.SQLFile = QtCore.QFile(self.SqlMapPath)
        if self.isRunning:
            self.Wdg.Info.appendPlainText('[WARINING]There is a process' +
                ' running. Please, wait.')
            return
        else:
            self.isRunning = True
        self.Target = self.Wdg.edtTarget.text()
        self.Wdg.Info.setPlainText('')
        self.Wdg.RawData.setPlainText('')
        self.Wdg.tabData.Clear()
        self.Wdg.Info.appendPlainText('[INFO]Starting the analyze.')
        # Ensure we use the current SqlMapPath
        sqlmap_path = self.SqlMapPath
        argIdentify = [sqlmap_path, '-u', str(self.Target), '--dbs',
            '--answers=skip test=N, include all tests=N' +
            ', keep testing the=Y', '--batch']
        if self.Wdg.cbxMethod.currentIndex():
            Data = self.Wdg.edtPostData.text()
            if len(Data) == 0:
                self.Wdg.Info.appendPlainText('[WARNING]Post data look be' +
                    ' empty')
                return
            else:
                argIdentify.append('--data=' + Data)
        #check if is using proxy
        argIdentify = self.Proxy(argIdentify)
        self.Run(argIdentify)
        self.Proc.finished.connect(self.getDBInfo)

    def Proxy(self, Arg):
        self.Resources = Resources()
        if self.Resources.getPref('UseHTTP'):
            IP = self.Resources.getPref('IP')
            Port = self.Resources.getPref('PortProxy')
            HOST = IP + ':' + Port
            Arg.append('--proxy=' + HOST)
        elif self.Resources.getPref('UseTor'):
            Port = self.Resources.getPref('PortProxy')
            Type = self.Resources.getPref('TorType')
            Arg.append('--tor')
            Arg.append('--tor-port=' + Port)
            Arg.append('--tor-type=' + Type)
            Arg.append('--check-tor')
        return Arg

    def Run(self, Arg):
        # Disconnect any previous connections
        try:
            self.Proc.readyReadStandardOutput.disconnect()
            self.Proc.readyReadStandardError.disconnect()
            self.Proc.errorOccurred.disconnect()
        except:
            pass
        
        # Connect to both stdout and stderr, and error signals
        self.Proc.readyReadStandardOutput.connect(self.Output)
        self.Proc.readyReadStandardError.connect(self.ErrorOutput)
        self.Proc.errorOccurred.connect(self.ProcessError)
        
        # Start the process
        self.Proc.start(self.Python, Arg)
        
        # Check if process started successfully
        if not self.Proc.waitForStarted(5000):  # Wait up to 5 seconds
            error_msg = f'[ERROR] Failed to start process: {self.Python}'
            if self.Proc.error() != QtCore.QProcess.ProcessError.UnknownError:
                error_msg += f'\nError: {self.Proc.errorString()}'
            self.Wdg.RawData.appendPlainText(error_msg)
            self.isRunning = False
    
    def ProcessError(self, error_code):
        """Handle process errors"""
        error_msg = f'\n[PROCESS ERROR] {self.Proc.errorString()}\n'
        self.Wdg.RawData.appendPlainText(error_msg)

    #read the output and find the DBMS version and the databases
    def getDBInfo(self, ExitCode=None, ExitStatus=None):
        self.isRunning = False
        try:
            self.Proc.finished.disconnect()
        except:
            pass
        
        # Read any remaining output after process finished
        data = self.Proc.readAllStandardOutput()
        if data:
            output = bytes(data).decode('utf-8', errors='ignore')
            if output:
                self.Wdg.RawData.appendPlainText(output)
        
        data = self.Proc.readAllStandardError()
        if data:
            output = bytes(data).decode('utf-8', errors='ignore')
            if output:
                self.Wdg.RawData.appendPlainText(output)
        
        Exit = ExitCode if ExitCode is not None else (ExitStatus if ExitStatus is not None else 0)
        if (Exit != 0):
            # Get error details
            error_string = self.Proc.errorString()
            if error_string:
                self.Wdg.RawData.appendPlainText(f'\n[PROCESS ERROR] {error_string}\n')
            
            Info = QtWidgets.QMessageBox()
            self.Wdg.Info.appendPlainText('[ERROR]Failed to start scanning.' +
                'See the raw data for more information')
            Info.information(self.Wdg, 'DB Analyzer', 'The databases was not \n'
             + 'analyzed. Please, restart the analyze.')
        else:
            self.RawAnalyzer.getDBInfo()

    def Output(self):
        data = self.Proc.readAllStandardOutput()
        output = bytes(data).decode('utf-8', errors='ignore')
        if output:
            self.Wdg.RawData.appendPlainText(output)
    
    def ErrorOutput(self):
        data = self.Proc.readAllStandardError()
        output = bytes(data).decode('utf-8', errors='ignore')
        if output:
            self.Wdg.RawData.appendPlainText(output)

    def getTables(self, DB, CurrentDB):
        if self.isRunning:
            self.Wdg.Info.appendPlainText('[WARNING]There is a process ' +
                'running. Please, wait.')
            return
        else:
            self.isRunning = True
        self.CurrentDB = CurrentDB
        self.Wdg.Info.appendPlainText('[INFO]Getting %s tables.Please, wait'
             % DB)
        self.DB = DB
        sqlmap_path = self.SqlMapPath
        argTables = [sqlmap_path, '-u', str(self.Target), '-D', DB,
            '--tables', '--answers=do you want to use common table existence=N']
        if self.Wdg.cbxMethod.currentIndex():
            Data = self.Wdg.edtPostData.text()
            if len(Data) == 0:
                self.Wdg.Info.appendPlainText('[WARNING]Post data look be' +
                    ' empty')
                return
            else:
                argTables.append('--data=' + Data)
        #check if is using proxy
        argTables = self.Proxy(argTables)
        self.Run(argTables)
        self.Proc.finished.connect(self.AnalyzeTables)

    def AnalyzeTables(self, ExitCode=None, ExitStatus=None):
        self.isRunning = False
        try:
            self.Proc.finished.disconnect()
        except:
            pass
        
        # Read any remaining output
        data = self.Proc.readAllStandardOutput()
        if data:
            output = bytes(data).decode('utf-8', errors='ignore')
            if output:
                self.Wdg.RawData.appendPlainText(output)
        
        data = self.Proc.readAllStandardError()
        if data:
            output = bytes(data).decode('utf-8', errors='ignore')
            if output:
                self.Wdg.RawData.appendPlainText(output)
        
        Exit = ExitCode if ExitCode is not None else (ExitStatus if ExitStatus is not None else 0)
        if Exit != 0:
            self.Wdg.Info.appendPlainText('[ERROR] The scanning stopped' +
                'incorretly. Restart the analyze')
        else:
            self.RawAnalyzer.AnalyzeTables(self.DB, self.CurrentDB)

    def getTableContent(self, TB):
        self.TBName = str(TB.text(0))
        DB = str(TB.parent().text(0))
        if self.isRunning:
            self.Wdg.Info.appendPlainText('[WARNING]There is a process ' +
                'running.Please, wait.')
            return
        else:
            self.isRunning = True
        self.Wdg.Info.appendPlainText('[INFO]Getting table content, wait')
        sqlmap_path = self.SqlMapPath
        argTBContent = [sqlmap_path, '-u', str(self.Target), '-D', DB,
            '-T', self.TBName, '--dump',
            '--answers=hashes to a temporary file=N' +
            ',dictionary-based attack=N']
        if self.Wdg.cbxMethod.currentIndex():
            Data = self.Wdg.edtPostData.text()
            if len(Data) == 0:
                self.Wdg.Info.appendPlainText('[WARNING]Post data look be' +
                    ' empty')
                return
            else:
                argTBContent.append('--data=' + Data)
        #check if is using proxy
        argTBContent = self.Proxy(argTBContent)
        self.Run(argTBContent)
        self.Proc.finished.connect(self.AnalyzeTableContent)

    def AnalyzeTableContent(self, ExitCode=None, ExitStatus=None):
        self.isRunning = False
        try:
            self.Proc.finished.disconnect()
        except:
            pass
        
        # Read any remaining output
        data = self.Proc.readAllStandardOutput()
        if data:
            output = bytes(data).decode('utf-8', errors='ignore')
            if output:
                self.Wdg.RawData.appendPlainText(output)
        
        data = self.Proc.readAllStandardError()
        if data:
            output = bytes(data).decode('utf-8', errors='ignore')
            if output:
                self.Wdg.RawData.appendPlainText(output)
        
        Exit = ExitCode if ExitCode is not None else (ExitStatus if ExitStatus is not None else 0)
        if Exit != 0:
            self.Wdg.Info.appendPlainText('[ERROR] The scanning stopped' +
                'incorretly. Restart the analyze')
        else:
            self.RawAnalyzer.getTBContent(self.TBName)

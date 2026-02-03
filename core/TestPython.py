# -*- coding: utf-8 -*-

from PySide6.QtCore import QProcess, QObject
from PySide6 import QtCore
from core.Resources import Resources


class TestPython(QObject):

    def __init__(self, ID=None):
        super().__init__()
        self.Test = QProcess()
        self.ID = ID
        #a and b to test if i get a output or command error
        self.a = False
        self.python_found = False
        self.Settings = QtCore.QSettings('Tyrant.cfg',
                                                    QtCore.QSettings.IniFormat)
        self.current_process = None

    def TestVersion(self):
        print('Test python version')
        # Reset flags
        self.a = False
        self.python_found = False
        
        # Try python3.10 first, then python3, then python
        python_commands = ['python3.10', 'python3', 'python']
        
        # If we have a custom path, try it first
        Res = Resources()
        custom_python = Res.getPref('Python')
        if custom_python and len(custom_python) >= 3 and custom_python != 'python2.7':
            python_commands.insert(0, custom_python)
        
        for Python in python_commands:
            print(f'Trying Python: {Python}')
            # Reset flags for this attempt
            self.a = False
            self.python_found = False
            
            # Create new process for each try
            test_process = QProcess()
            self.current_process = test_process
            test_process.readyReadStandardError.connect(self.getOutput)
            test_process.readyReadStandardOutput.connect(self.getOutput)
            
            test_process.start(Python, ['-V'])
            if not test_process.waitForFinished(3000):  # Wait max 3 seconds
                test_process.terminate()
                test_process.waitForFinished(1000)
                test_process.deleteLater()
                self.current_process = None
                continue
            
            exit_code = test_process.exitCode()
            
            # Read any remaining output after process finished
            data = test_process.readAllStandardError()
            if data:
                output = bytes(data).decode('utf-8', errors='ignore')
                self._checkPythonOutput(output)
            
            data = test_process.readAllStandardOutput()
            if data:
                output = bytes(data).decode('utf-8', errors='ignore')
                self._checkPythonOutput(output)
            
            test_process.deleteLater()
            self.current_process = None
            
            if exit_code == 0 and self.python_found:
                # Python 3.x found and working
                print(f'Python version found: {Python}')
                self.Settings.setValue('Python/PythonPath', str(Python))
                self.Settings.sync()
                return True
        
        # If we're checking for validation (ID is not None), return False
        if self.ID is not None:
            return False
        
        # If we're just checking availability, return whether we found Python 3
        return self.python_found


    def getOutput(self):
        # Get the sender (the QProcess that emitted the signal) or use current_process
        sender = self.sender()
        process = sender if sender else self.current_process
        
        if process is None:
            return
            
        data = process.readAllStandardError()
        output = bytes(data).decode('utf-8', errors='ignore')
        if not output:
            data = process.readAllStandardOutput()
            output = bytes(data).decode('utf-8', errors='ignore')
        
        if output:
            self._checkPythonOutput(output)
    
    def _checkPythonOutput(self, output):
        """Check if output indicates Python 3.x"""
        print(f'Python output: {output.strip()}')
        # Check if Python version is 3.x or higher
        if 'Python 3.' in output:
            # Extract version number
            import re
            version_match = re.search(r'Python 3\.(\d+)', output)
            if version_match:
                minor_version = int(version_match.group(1))
                # Accept Python 3.0 or higher (changed from 3.10 requirement)
                if minor_version >= 0:
                    self.a = True
                    self.python_found = True
            else:
                # If it says "Python 3" without version, assume it's OK
                if 'Python 3' in output:
                    self.a = True
                    self.python_found = True
        elif 'Python 2.' in output:
            # Python 2 is not supported
            self.a = False
            self.python_found = False
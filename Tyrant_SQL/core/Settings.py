# *-* coding: utf-8 *-*

from PySide import QtCore


class TyrantSettings(object):

    def __init__(self, Preferences=None):
        self.Settings = QtCore.QSettings('Tyrant.cfg',
                                                    QtCore.QSettings.IniFormat)
        self.Pref = Preferences

    def Populate_Prefs(self):
        print('Populating preferences')
        self.Pref.edtPython.setText(str(self.Settings.value
                                                        ('Python/PythonPath')))

    def Save_Prefs(self):
        print('Saving preferences')
        self.Settings.setValue('Python/PythonPath', self.Pref.edtPython.text())
        self.Settings.sync()


# *-* coding: utf-8 *-*


from PySide import QtCore


class Resources(object):

    def __init__(self):
        self.Dict = {}
        self.Settings = QtCore.QSettings('Tyrant.cfg',
                                                    QtCore.QSettings.IniFormat)
        self.Populate_Dict()

    def Populate_Dict(self):
        self.Dict['Python'] = str(self.Settings.value('Python/PythonPath'))

    def getPref(self, Name):
        try:
            return(self.Dict[str(Name)])
        except:
            print('Configuration not found')
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
        self.Dict['IP'] = str(self.Settings.value('SQLMap/IPProxy'))
        self.Dict['PortProxy'] = str(self.Settings.value('SQLMap/PortProxy'))
        self.Dict['UseHTTP'] = self.getBool(self.Settings.value
                                                            ('SQLMAP/UseHTTP'))
        self.Dict['UseTor'] = self.getBool(self.Settings.value
                                                            ('SQLMap/UseTor'))
        self.Dict['UseProxy'] = self.getBool(self.Settings.value
                                                            ('SQLMap/UseProxy'))
        self.Dict['TorType'] = str(self.Settings.value
                                                    ('SQLMap/TorType', 'HTTP'))
        self.Dict['TorTypeIndex'] = int(self.Settings.value
                                                    ('SQLMap/TorTypeIndex', 0))

    def getBool(self, Text):
        if Text == 'True':
            return True
        else:
            return False

    def getPref(self, Name):
        try:
            return(self.Dict[str(Name)])
        except:
            print('Configuration not found')
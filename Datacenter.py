class Datacenter:

    def __init__(self, name, datacenterCharacteristics):
        self.name = name
        self.datacenterCharacteristics = datacenterCharacteristics

        self.hostList = None

    def setHostList(self, hostList):
        self.hostList = hostList

    def getHostList(self):
        return self.hostList
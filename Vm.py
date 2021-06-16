class Vm:

    def __init__(self, id, ram, mips, bw, type ):
        self.id = id
        self.ram = ram
        self.mips = mips
        self.bw = bw
        self.type = type

        self.allocatedHostId = None
        # allocatedInstanceType = "a1.4xlarge"
        # currentPrice = 0.0

    def getId(self):
        return self.id

    def getMips(self):
        return self.mips

    def getRam(self):
        return self.ram

    def getType(self):
        return self.type

    def getAllocatedHostId(self):
        return self.allocatedHostId

    def setAllocatedHostId(self, id):
        self.allocatedHostId = id
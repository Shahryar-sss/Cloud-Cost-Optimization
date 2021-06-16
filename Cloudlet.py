class Cloudlet:

    def __init__(self, id, highestRamUsage, averageRamUsage, length):
        self.id = id
        self.highestRamUsage = highestRamUsage
        self.averageRamUsage = averageRamUsage
        self.length = length

        self.allocatedVmId = None
        self.costAcquired = 0.0
        self.prevAllocatedVmType = None

    def getId(self):
        return self.id

    def getAllocatedVmId(self):
        return self.allocatedVmId

    def getHighestRamUsage(self):
        return self.highestRamUsage

    def getAverageRamUsage(self):
        return self.averageRamUsage

    def getcostAcquired(self):
        return self.costAcquired

    def getPrevAllocatedVmType(self):
        return self.prevAllocatedVmType

    def getLength(self):
        return self.length

    def setLength(self, length):
        self.length = length

    def setAllocatedVmId(self, allocatedVmId):
        self.allocatedVmId = allocatedVmId

    def setcostAcquired(self,costAcquired):
        self.costAcquired=costAcquired

    def setPrevAllocatedVmType(self, prevAllocatedVmType):
        self.prevAllocatedVmType = prevAllocatedVmType

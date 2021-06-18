class Cloudlet:

    def __init__(self, id, highestRamUsage, averageRamUsage, length):
        self.id = id
        self.highestRamUsage = highestRamUsage
        self.averageRamUsage = averageRamUsage
        self.length = length

        self.allocatedVmId = None
        self.prevAllocatedVmType = None
        self.runtimeDistributionOnVm = []
        self.runningOnDemand = False
        self.migrationEvent = None

    def getId(self):
        return self.id

    def getAllocatedVmId(self):
        return self.allocatedVmId

    def getHighestRamUsage(self):
        return self.highestRamUsage

    def getAverageRamUsage(self):
        return self.averageRamUsage

    def getRuntimeDistributionOnVm(self):
        return self.runtimeDistributionOnVm

    def getRunningOnDemand(self):
        return self.runningOnDemand

    def getPrevAllocatedVmType(self):
        return self.prevAllocatedVmType

    def getLength(self):
        return self.length

    def getMigrationEvent(self):
        return self.migrationEvent

    def setLength(self, length):
        self.length = length

    def setAllocatedVmId(self, allocatedVmId):
        self.allocatedVmId = allocatedVmId

    def setRunningOnDemand(self, runningOnDemand):
        self.runningOnDemand = runningOnDemand

    def setRuntimeDistributionOnVm(self, vmType, runtimeOnVm, ondemand = False):
        self.runtimeDistributionOnVm.append((vmType, runtimeOnVm, ondemand))

    def setPrevAllocatedVmType(self, prevAllocatedVmType):
        self.prevAllocatedVmType = prevAllocatedVmType

    def setMigrationEvent(self, migrationEvent):
        self.migrationEvent = migrationEvent
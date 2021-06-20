class Cloudlet:

    def __init__(self, id, highestRamUsage, averageRamUsage, length, ramDistribution):
        self.id = id
        self.highestRamUsage = highestRamUsage
        self.averageRamUsage = averageRamUsage
        self.length = length
        self.ramDistribution = ramDistribution

        self.allocatedVmId = None
        self.prevAllocatedVmType = None
        self.runtimeDistributionOnVm = []
        self.runningOnDemand = False
        self.migrationEvent = None
        self.bucket = 0

        if 0 <= highestRamUsage <= 8:
            self.bucket = 1
        elif 9 <= highestRamUsage <= 32:
            self.bucket = 2
        elif 33 <= highestRamUsage <= 64:
            self.bucket = 3
        else:
            self.bucket = 4

        self.overUtilizedState = False
        self.ramMigrationWindow = ()

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

    def getBucket(self):
        return self.bucket

    def getLength(self):
        return self.length

    def getMigrationEvent(self):
        return self.migrationEvent

    def setLength(self, length):
        self.length = length

    def setAllocatedVmId(self, allocatedVmId):
        self.allocatedVmId = allocatedVmId

    def getRamMigrationWindow(self):
        return self.ramMigrationWindow

    def getOverUtilizedState(self):
        return self.overUtilizedState

    def setRunningOnDemand(self, runningOnDemand):
        self.runningOnDemand = runningOnDemand

    def getRamDistribution(self):
        return self.ramDistribution

    def setRuntimeDistributionOnVm(self, vmType, runtimeOnVm, migrationEvent, ondemand = False):
        self.runtimeDistributionOnVm.append((vmType, runtimeOnVm, ondemand, migrationEvent))

    def setPrevAllocatedVmType(self, prevAllocatedVmType):
        self.prevAllocatedVmType = prevAllocatedVmType

    def setBucket(self, bucket):
        self.bucket = bucket

    def setMigrationEvent(self, migrationEvent):
        self.migrationEvent = migrationEvent

    def setOverUtilizedState(self, overUtilizedState):
        self.overUtilizedState = overUtilizedState

    def setRamMigrationWindow(self, startTime):
        self.ramMigrationWindow = (startTime, 1)

    def incrementRamMigrationWindowFrequency(self):
        self.ramMigrationWindow = (self.ramMigrationWindow[0], self.ramMigrationWindow[1] + 1)
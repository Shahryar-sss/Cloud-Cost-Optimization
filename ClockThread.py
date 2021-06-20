import threading

from PrintLogs import printMessage

class ClockThread:

    currentTime = 0

    def __init__(self, vmList, cloudletList, configurationData, cloudletAllocationPolicy):
        self.vmList = vmList
        self.cloudletList = cloudletList
        self.configurationData = configurationData
        self.cloudletAllocationPolicy = cloudletAllocationPolicy

    def init(self):
        while len(self.vmList) > 0 or len([cloudlet for cloudlet in self.cloudletList if cloudlet.getLength() > 0]) > 0:
            threadList = []
            for cloudlet in self.cloudletList:
                threadList.append(threading.Thread(target=self.clockTick, args=[cloudlet]))

            for thread in threadList:
                thread.start()

            for thread in threadList:
                thread.join()

            ClockThread.currentTime += 1

    def clockTick(self, cloudlet):

        if cloudlet.getLength() == 0:
            cloudlet.setAllocatedVmId(None)
            cloudlet.setPrevAllocatedVmType(None)
            return

        currentVm = None
        for vm in self.vmList:
            if vm.getId() == cloudlet.getAllocatedVmId():
                currentVm = vm

        if currentVm is None:
            return

        currentRam = float(self.getCurrentRam(cloudlet.getRamDistribution()))

        if self.cloudletAllocationPolicy == "LowestSpotScoreFirst":

            if currentRam > 0.9 * currentVm.getRam():
                state = cloudlet.getOverUtilizedState()

                if not state:
                    cloudlet.setOverUtilizedState(True)
                    cloudlet.setRamMigrationWindow(ClockThread.currentTime)

                if state:
                    window = cloudlet.getRamMigrationWindow()

                    if ClockThread.currentTime - window[0] < 10*60:
                        cloudlet.incrementRamMigrationWindowFrequency()
                    else:
                        if window[1] >= 0.1 * 10*60:

                            message = "[" + str(
                                ClockThread.currentTime) + "] Ram utilisation threshold reached. Migrating cloudlet #" + str(
                                cloudlet.getId()) + " Ram of current allocated VM is " + str(
                                currentVm.getRam()) + " Current ram of cloudlet " + str(currentRam)
                            printMessage("CloudletAllocationAndMigration", message)

                            cloudlet.setMigrationEvent("RAM")
                            cloudlet.setPrevAllocatedVmType(currentVm.getType())
                            cloudlet.setRuntimeDistributionOnVm(currentVm.getType(), ClockThread.currentTime, "RAM")
                            cloudlet.setBucket(cloudlet.getBucket() + 1 if cloudlet.getBucket() < 4 else 4)
                            cloudlet.setOverUtilizedState(False)
                            cloudlet.setAllocatedVmId(None)
                            return

                        else:
                            cloudlet.setRamMigrationWindow(ClockThread.currentTime)

            suitableInstanceTypes = []
            for instanceType in self.configurationData.keys():
                if cloudlet.getHighestRamUsage() < self.configurationData[instanceType][1] and cloudlet.getBucket() == int(self.configurationData[instanceType][6]):
                    suitableInstanceTypes.append(instanceType)

            minSpotScore = float('inf')
            instanceTypeWithMinSpotScore = None
            for instanceType in suitableInstanceTypes:
                if float(self.configurationData[instanceType][5][int(ClockThread.currentTime / 60)]) < minSpotScore:
                    minSpotScore = float(self.configurationData[instanceType][5][int(ClockThread.currentTime / 60)])
                    instanceTypeWithMinSpotScore = instanceType

            if cloudlet.getRunningOnDemand():

                if float(self.configurationData[instanceTypeWithMinSpotScore][4][int(ClockThread.currentTime/60)]) < self.configurationData[currentVm.getType()][3]:
                    message = "[" + str(ClockThread.currentTime) + "] Migrating Cloudlet #" + str(cloudlet.getId()) + "from on demand vm #" + str(currentVm.getType()) + " to spot instance of type " + instanceTypeWithMinSpotScore
                    printMessage("CloudletAllocationAndMigration", message)

                    cloudlet.setMigrationEvent("SPOT_SCORE")
                    cloudlet.setPrevAllocatedVmType(currentVm.getType())
                    cloudlet.setRuntimeDistributionOnVm(currentVm.getType(), ClockThread.currentTime, "SPOT_SCORE", True)
                    cloudlet.setAllocatedVmId(None)
                    return

            else:
                if float(self.configurationData[currentVm.getType()][4][int(ClockThread.currentTime/60)]) > float(self.configurationData[currentVm.getType()][3]):
                    message = "[" + str(ClockThread.currentTime) + "] Vm #" + str(currentVm.getId()) + " spot price has exceeded on-demand price. Migrating Cloudlet #" + str(cloudlet.getId())
                    printMessage("CloudletAllocationAndMigration", message)

                    cloudlet.setMigrationEvent("SPOT_SCORE")
                    cloudlet.setPrevAllocatedVmType(currentVm.getType())
                    cloudlet.setRuntimeDistributionOnVm(currentVm.getType(), ClockThread.currentTime, "SPOT_SCORE")
                    cloudlet.setAllocatedVmId(None)
                    return

                if float(self.configurationData[currentVm.getType()][4][int(ClockThread.currentTime/60)]) > float(self.configurationData[instanceTypeWithMinSpotScore][4][int(ClockThread.currentTime/60)]):
                    message = "[" + str(ClockThread.currentTime) + "] Vm type " + instanceTypeWithMinSpotScore + " has lower price than Vm #" + str(currentVm.getId()) + " of type " + currentVm.getType() + ". Migrating Cloudlet #" + str(cloudlet.getId())
                    printMessage("CloudletAllocationAndMigration", message)

                    cloudlet.setMigrationEvent("SPOT_SCORE")
                    cloudlet.setPrevAllocatedVmType(currentVm.getType())
                    cloudlet.setRuntimeDistributionOnVm(currentVm.getType(), ClockThread.currentTime, "SPOT_SCORE")
                    cloudlet.setAllocatedVmId(None)
                    return

        cloudletUpdatedLength = cloudlet.getLength()-currentVm.getMips()
        cloudletUpdatedLength = cloudletUpdatedLength if cloudletUpdatedLength > 0 else 0
        if cloudletUpdatedLength == 0:
            cloudlet.setRuntimeDistributionOnVm(currentVm.getType(), ClockThread.currentTime, "COMPLETED", cloudlet.getRunningOnDemand())

            message = "[" + str(ClockThread.currentTime) + "] Cloudlet #" + str(cloudlet.getId()) + " has finished execution."
            printMessage("FinishedExecution", message)

        cloudlet.setLength(cloudletUpdatedLength)


    def getCurrentRam(self, ramDistribution):
        return ramDistribution[int(ClockThread.currentTime/60)%len(ramDistribution)]
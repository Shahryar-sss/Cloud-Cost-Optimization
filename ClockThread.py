import threading
import numpy as np

class ClockThread:

    currentTime = 0

    def __init__(self, vmList, cloudletList, configurationData, cloudletAllocationPolicy):
        self.vmList = vmList
        self.cloudletList = cloudletList
        self.configurationData = configurationData
        self.cloudletAllocationPolicy = cloudletAllocationPolicy

    def init(self):
        while len(self.vmList) > 0:
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

        currentRam = self.getCurrentRam(cloudlet.getHighestRamUsage())

        if 0.1 * currentVm.getRam() > currentRam or currentRam > 0.9 * currentVm.getRam():
            print("Ram utilisation threshold reached. Migrating cloudlet #{}".format(cloudlet.getId()))
            cloudlet.setAllocatedVmId(None)
            cloudlet.setPrevAllocatedVmType(currentVm.getType())
            cloudlet.setRuntimeDistributionOnVm(currentVm.getType(), ClockThread.currentTime)
            return

        if self.cloudletAllocationPolicy == "LowestSpotScoreFirst":
            if cloudlet.getRunningOnDemand():
                suitableInstanceTypes=[]
                for instanceType in self.configurationData.keys():
                    if cloudlet.getHighestRamUsage() < self.configurationData[instanceType][1]:
                        suitableInstanceTypes.append(instanceType)

                minSpotScore = float('inf')
                instanceTypeWithMinSpotScore = None
                for instanceType in suitableInstanceTypes:
                    if float(self.configurationData[instanceType][5][int(ClockThread.currentTime/60)]) < minSpotScore:
                        minSpotScore = float(self.configurationData[instanceType][5][int(ClockThread.currentTime/60)])
                        instanceTypeWithMinSpotScore = instanceType

                if float(self.configurationData[instanceTypeWithMinSpotScore][4][int(ClockThread.currentTime/60)]) < self.configurationData[currentVm.getType()][3]:
                    print("Migrating Cloudlet #{} from on-demand vm #{} ".format(cloudlet.getId(),currentVm.getType()))
                    cloudlet.setAllocatedVmId(None)
                    cloudlet.setPrevAllocatedVmType(currentVm.getType())
                    cloudlet.setRuntimeDistributionOnVm(currentVm.getType(), ClockThread.currentTime, True)
                    return
            else:
                if float(self.configurationData[currentVm.getType()][4][int(ClockThread.currentTime/60)]) > self.configurationData[currentVm.getType()][3]:
                    print("Vm #{} spot price has exceeded on-demand price. Migrating Cloudlet #{}".format(currentVm.getId(), cloudlet.getId()))
                    cloudlet.setAllocatedVmId(None)
                    cloudlet.setPrevAllocatedVmType(currentVm.getType())
                    cloudlet.setRuntimeDistributionOnVm(currentVm.getType(), ClockThread.currentTime)
                    return

        cloudletUpdatedLength = cloudlet.getLength()-currentVm.getMips()
        cloudletUpdatedLength = cloudletUpdatedLength if cloudletUpdatedLength > 0 else 0
        if cloudletUpdatedLength == 0:
            cloudlet.setRuntimeDistributionOnVm(currentVm.getType(), ClockThread.currentTime)
            print("Cloudlet #{} has finished execution".format(cloudlet.getId()))
        cloudlet.setLength(cloudletUpdatedLength)

    def getCurrentRam(self, averageRamUsage):
        val = np.random.normal(loc=averageRamUsage,size=1)
        while val[0] <= 0:
            val = np.random.normal(loc=averageRamUsage,size=1)
        return val[0]

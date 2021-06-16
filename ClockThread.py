import threading
import numpy as np

class ClockThread:

    currentTime = 0

    def __init__(self, vmList, cloudletList, configurationData):
        self.vmList = vmList
        self.cloudletList = cloudletList
        self.configurationData = configurationData

    def init(self):
        threadList = []
        for cloudlet in self.cloudletList:
            threadList.append(threading.Thread(target=self.clockTick, args=[cloudlet]))

        for thread in threadList:
            thread.start()

        for thread in threadList:
            thread.join()

        ClockThread.currentTime += 1

        if len(self.vmList) > 0:
            threading.Timer(0.0001, self.init).start()

    def clockTick(self, cloudlet):
        if cloudlet.getLength() == 0:
            cloudlet.setAllocatedVmId(None)
            print("Cloudlet #{} has finished execution".format(cloudlet.getId()))
            return

        currentVm = None
        for vm in self.vmList:
            if vm.getId() == cloudlet.getAllocatedVmId():
                currentVm = vm

        currentRam = self.getCurrentRam(cloudlet.getHighestRamUsage())
        print("Current ram usage of cloudlet #{} is {} and remaining instructions is {}".format(cloudlet.getId(), currentRam, cloudlet.getLength()))

        if 0.1 * currentVm.getRam() > currentRam or currentRam > 0.9 * currentVm.getRam():
            print("Ram utilisation threshold reached. Migrating cloudlet #{}".format(cloudlet.getId()))
            cloudlet.setAllocatedVmId(None)
            cloudlet.setPrevAllocatedVmType(vm.getType())
            return

        cloudletUpdatedLength = cloudlet.getLength()-currentVm.getMips()
        cloudletUpdatedLength = cloudletUpdatedLength if cloudletUpdatedLength > 0 else 0
        cloudlet.setLength(cloudletUpdatedLength)
        if ClockThread.currentTime % 60 == 0:
            cloudlet.setcostAcquired(cloudlet.getcostAcquired()+float(self.configurationData[currentVm.getType()][4][int(ClockThread.currentTime/60)]))

    def getCurrentRam(self, averageRamUsage):
        val = np.random.normal(loc=averageRamUsage,size=1)
        while val[0] <= 0:
            val = np.random.normal(loc=averageRamUsage,size=1)
        return val[0]

import threading
import random

import Vm
import VmAllocationPolicy
import VmThread
import ClockThread
from PrintLogs import printMessage


class DatacenterBroker:

    def __init__(self, name, id, datacenter, vmAllocationPolicy, cloudletAllocationPolicy, instanceConfigurationData):
        self.id = id
        self.name = name
        self.datacenter = datacenter
        self.vmAllocationPolicy = vmAllocationPolicy
        self.cloudletAllocationPolicy = cloudletAllocationPolicy

        self.hostList = datacenter.getHostList()
        self.vmList = []
        self.cloudletList = None
        self.instanceConfigurationData = instanceConfigurationData

    def getId(self):
        return self.id

    def submitCloudletList(self, cloudletList):
        self.cloudletList = cloudletList

        threadList = []
        for cloudlet in self.cloudletList:
            threadList.append(threading.Thread(target=self.createVmAndAssignCloudlet, args=[cloudlet]))

        for thread in threadList:
            thread.start()

        for thread in threadList:
            thread.join()

        self.vmThread = VmThread.VmThread(self.hostList, self.vmList, self.cloudletList, self)
        self.clockThread = ClockThread.ClockThread(self.vmList, self.cloudletList, self.instanceConfigurationData, self.cloudletAllocationPolicy)

        t1 = threading.Thread(target=self.vmThread.init)
        t2 = threading.Thread(target=self.clockThread.init)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    def createVmAndAssignCloudlet(self, cloudlet):
        if self.cloudletAllocationPolicy == "FirstComeFirstServe":
            for instanceType in self.instanceConfigurationData.keys():
                if cloudlet.getHighestRamUsage() < self.instanceConfigurationData[instanceType][1]:

                    vmId = random.randint(1, 9999)
                    vmIdList = [vm.getId() for vm in self.vmList]
                    while vmId in vmIdList:
                        vmId = random.randint(1, 9999)

                    vm = Vm.Vm(id=vmId, ram=self.instanceConfigurationData[instanceType][1],
                               mips=self.instanceConfigurationData[instanceType][0],
                               bw=self.instanceConfigurationData[instanceType][2],
                               type=instanceType)

                    message = "[" + str(ClockThread.ClockThread.currentTime) + "] Created VM #" + str(vm.getId()) + " of type " + str(vm.getType())
                    printMessage("VmAllocation", message)

                    vmAllocationPolicy = VmAllocationPolicy.VmAllocationPolicy(self.vmAllocationPolicy, self.hostList, vm, self.vmList)
                    vmAllocationPolicy.allocateHostToVm()

                    cloudlet.setAllocatedVmId(vm.getId())

                    message = "[" + str(ClockThread.ClockThread.currentTime) + "] Cloudlet #" + str(cloudlet.getId()) + " assigned to VM #" + str(vm.getId())
                    printMessage("CloudletAllocationAndMigration", message)

                    return

        elif self.cloudletAllocationPolicy == "LowestSpotScoreFirst":

            suitableInstanceTypes = []
            for instanceType in self.instanceConfigurationData.keys():
                if cloudlet.getHighestRamUsage() < self.instanceConfigurationData[instanceType][1] and cloudlet.getBucket() == int(self.instanceConfigurationData[instanceType][6]):

                    if cloudlet.getPrevAllocatedVmType() is not None:
                        if not cloudlet.runningOnDemand and instanceType == cloudlet.getPrevAllocatedVmType():
                            continue

                    suitableInstanceTypes.append(instanceType)

            migrationTime = 0
            if len(cloudlet.getRuntimeDistributionOnVm()) > 0:
               migrationTime = cloudlet.getRuntimeDistributionOnVm()[len(cloudlet.getRuntimeDistributionOnVm())-1][1]

            minSpotScore = float("inf")
            instanceTypeWithMinSpotScore = None
            for instanceType in suitableInstanceTypes:
                if float(self.instanceConfigurationData[instanceType][5][int(migrationTime/60)]) < minSpotScore:
                    minSpotScore=float(self.instanceConfigurationData[instanceType][5][int(migrationTime/60)])
                    instanceTypeWithMinSpotScore = instanceType

            if cloudlet.getPrevAllocatedVmType() is not None and float(self.instanceConfigurationData[instanceTypeWithMinSpotScore][4][int(migrationTime/60)]) > self.instanceConfigurationData[cloudlet.getPrevAllocatedVmType()][3]:
                if cloudlet.getBucket() == int(self.instanceConfigurationData[cloudlet.getPrevAllocatedVmType()][6]):
                    cloudlet.setRunningOnDemand(True)
                    instanceTypeWithMinSpotScore = cloudlet.getPrevAllocatedVmType()
                else:
                    if float(self.instanceConfigurationData[instanceTypeWithMinSpotScore][4][int(migrationTime/60)]) > float(self.instanceConfigurationData[instanceTypeWithMinSpotScore][3]):
                        cloudlet.setRunningOnDemand(True)
                        instanceTypeWithMinSpotScore = instanceTypeWithMinSpotScore
            else:
                cloudlet.setRunningOnDemand(False)

            vmId = random.randint(1, 9999)
            vmIdList = [vm.getId() for vm in self.vmList]
            while vmId in vmIdList:
                vmId = random.randint(1, 9999)

            vm = Vm.Vm(id=vmId, ram=self.instanceConfigurationData[instanceTypeWithMinSpotScore][1],
                       mips=self.instanceConfigurationData[instanceTypeWithMinSpotScore][0],
                       bw=self.instanceConfigurationData[instanceTypeWithMinSpotScore][2],
                       type=instanceTypeWithMinSpotScore)

            message = "[" + str(ClockThread.ClockThread.currentTime) + "] Created VM #" + str(vm.getId()) + " of type " + str(vm.getType())
            printMessage("VmAllocation", message)

            vmAllocationPolicy = VmAllocationPolicy.VmAllocationPolicy(self.vmAllocationPolicy, self.hostList, vm, self.vmList)
            vmAllocationPolicy.allocateHostToVm()

            cloudlet.setAllocatedVmId(vm.getId())

            message = "[" + str(ClockThread.ClockThread.currentTime) + "] Cloudlet #" + str(cloudlet.getId()) + " assigned to VM #" + str(vm.getId())
            printMessage("CloudletAllocationAndMigration", message)
            return

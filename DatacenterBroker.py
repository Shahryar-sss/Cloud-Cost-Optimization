import threading
import random

import Vm
import VmAllocationPolicy
import VmThread
import ClockThread
from InstanceConfiguration import instanceConfigurationData


class DatacenterBroker:

    def __init__(self, name, id, datacenter, vmAllocationPolicy, cloudletAllocationPolicy):
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

                    if cloudlet.getPrevAllocatedVmType() is not None and instanceType == cloudlet.getPrevAllocatedVmType():
                        continue

                    vmId = random.randint(1, 99999999)
                    vmIdList = [vm.getId() for vm in self.vmList]
                    while vmId in vmIdList:
                        vmId = random.randint(1, 99999999)

                    vm = Vm.Vm(id=vmId, ram=instanceConfigurationData[instanceType][1],
                               mips=instanceConfigurationData[instanceType][0],
                               bw=instanceConfigurationData[instanceType][2],
                               type=instanceType)

                    print("Created VM #{} of type {}".format(vm.getId(), vm.getType()))

                    vmAllocationPolicy = VmAllocationPolicy.VmAllocationPolicy(self.vmAllocationPolicy, self.hostList, vm, self.vmList)
                    vmAllocationPolicy.allocateHostToVm()

                    cloudlet.setAllocatedVmId(vm.getId())
                    print("Cloudlet #{} assigned to VM #{}".format(cloudlet.getId(), vm.getId()))
                    return
        elif self.cloudletAllocationPolicy == "LowestSpotScoreFirst":
            suitableInstanceTypes = []
            for instanceType in self.instanceConfigurationData.keys():
                if cloudlet.getHighestRamUsage() < self.instanceConfigurationData[instanceType][1]:

                    if cloudlet.getPrevAllocatedVmType() is not None and instanceType == cloudlet.getPrevAllocatedVmType() and cloudlet.getRunningOnDemand() == False:
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
                cloudlet.setRunningOnDemand(True)
                instanceTypeWithMinSpotScore = cloudlet.getPrevAllocatedVmType()
            else:
                cloudlet.setRunningOnDemand(False)

            vmId = random.randint(1, 99999999)
            vmIdList = [vm.getId() for vm in self.vmList]
            while vmId in vmIdList:
                vmId = random.randint(1, 99999999)

            vm = Vm.Vm(id=vmId, ram=instanceConfigurationData[instanceTypeWithMinSpotScore][1],
                       mips=instanceConfigurationData[instanceTypeWithMinSpotScore][0],
                       bw=instanceConfigurationData[instanceTypeWithMinSpotScore][2],
                       type=instanceTypeWithMinSpotScore)

            vmAllocationPolicy = VmAllocationPolicy.VmAllocationPolicy(self.vmAllocationPolicy, self.hostList, vm, self.vmList)
            vmAllocationPolicy.allocateHostToVm()

            cloudlet.setAllocatedVmId(vm.getId())

            print("Cloudlet #{} assigned to VM #{}".format(cloudlet.getId(), vm.getId()))
            return

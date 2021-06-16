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
        self.clockThread = ClockThread.ClockThread(self.vmList, self.cloudletList, self.instanceConfigurationData)

        t1 = threading.Thread(target=self.vmThread.init)
        t2 = threading.Thread(target=self.clockThread.init)

        t1.start()
        t2.start()

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
import threading

import DatacenterBroker

class VmThread:

    def __init__(self, hostList, vmList, cloudletList, brokerReference):
        self.hostList = hostList
        self.vmList = vmList
        self.cloudletList = cloudletList
        self.brokerReference = brokerReference

    def init(self):
        thread = threading.Thread(target=self.manageVms)
        thread.start()
        thread.join()

    def manageVms(self):
        while len(self.vmList) > 0:

            assignedCloudlets = [cloudlet.getAllocatedVmId() for cloudlet in self.cloudletList if cloudlet.getAllocatedVmId() is not None]
            for vm in self.vmList:
                if vm.getId() in assignedCloudlets:
                    continue

                self.vmList.remove(vm)
                print("VM #{} removed from host #{}".format(vm.getId(), vm.getAllocatedHostId()))
                for host in self.hostList:
                    if host.getId() == vm.getAllocatedHostId():
                        host.setAvailableRam(host.getAvailableRam() + vm.getRam())
                        print("Available ram in host #{} is {}GB".format(host.getId(), host.getAvailableRam()))


            unassignedCloudlets = [cloudlet for cloudlet in self.cloudletList if cloudlet.getAllocatedVmId() is None]
            for cloudlet in unassignedCloudlets:
                if cloudlet.getLength() == 0:
                    continue

                print("Migrating cloudlet #{} to new VM".format(cloudlet.getId()))
                DatacenterBroker.DatacenterBroker.createVmAndAssignCloudlet(self.brokerReference, cloudlet)
        return

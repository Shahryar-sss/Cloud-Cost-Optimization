import threading

import DatacenterBroker
from PrintLogs import printMessage
import ClockThread

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
                message = "[" + str(ClockThread.ClockThread.currentTime) + "] VM #" + str(vm.getId()) + " removed from host #" + str(vm.getAllocatedHostId())
                printMessage("VmAllocation", message)

                for host in self.hostList:
                    if host.getId() == vm.getAllocatedHostId():
                        host.setAvailableRam(host.getAvailableRam() + vm.getRam())
                        message = "[" + str(ClockThread.ClockThread.currentTime) + "] Available ram in host #" + str(host.getId()) + " is " + str(host.getAvailableRam()) + "GB"
                        printMessage("VmAllocation", message)

            unassignedCloudlets = [cloudlet for cloudlet in self.cloudletList if cloudlet.getAllocatedVmId() is None]
            for cloudlet in unassignedCloudlets:
                if cloudlet.getLength() == 0:
                    continue

                DatacenterBroker.DatacenterBroker.createVmAndAssignCloudlet(self.brokerReference, cloudlet)
        return

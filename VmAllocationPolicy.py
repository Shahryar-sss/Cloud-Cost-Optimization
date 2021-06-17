from PrintLogs import printMessage
import ClockThread

class VmAllocationPolicy:

    def __init__(self, vmAllocationPolicyName, hostList, vm, vmList):
        self.vmAllocationPolicyName = vmAllocationPolicyName
        self.hostList = hostList
        self.vm = vm
        self.vmList = vmList

    def allocateHostToVm(self):
        if self.vmAllocationPolicyName == "FirstComeFirstServe":
            self.allocateFirstComeFirstServe()

    def allocateFirstComeFirstServe(self):

        for host in self.hostList:
            if self.vm.getRam() < host.getAvailableRam():
                self.vm.setAllocatedHostId(host.getId())
                self.vmList.append(self.vm)
                host.setAvailableRam(host.getAvailableRam() - self.vm.getRam())

                message = "[" + str(ClockThread.ClockThread.currentTime) + "] VM #" + str(self.vm.getId()) + " assigned to host #" + str(host.getId())
                printMessage("VmAllocation", message)

                message = "[" + str(ClockThread.ClockThread.currentTime) + "] Available ram in host #" + str(host.getId()) + " is " + str(host.getAvailableRam())
                printMessage("VmAllocation", message)
                return

        message = "[" + str(ClockThread.ClockThread.currentTime) + "] Could not allocate #" + str(self.vm.getId()) + ". No host with sufficient ram is available"
        printMessage("VmAllocation", message)


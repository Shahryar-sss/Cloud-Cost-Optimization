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
                print("VM #{} mapped to host #{}".format(self.vm.getId(), host.getId()))
                print("Available ram in host #{} is {}".format(host.getId(), host.getAvailableRam()))
                return

        print("Could not allocate {}. No host with sufficient ram is available".format(self.vm.getId()))

import DatacenterCharacteristics
import Datacenter
import DatacenterBroker
import Host
import Cloudlet
from PrintLogs import printMessage
from InstanceConfiguration import instanceConfigurationData

class Main:

    def test(self):

        datacenter = self.createDatacenter("Datacenter_0")

        hostlist = []
        hostlist.append(Host.Host(id=0, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=1, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=2, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=3, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))

        datacenter.setHostList(hostlist)

        broker1 = DatacenterBroker.DatacenterBroker("Broker1", 0, datacenter ,"FirstComeFirstServe", "FirstComeFirstServe", instanceConfigurationData)
        broker2 = DatacenterBroker.DatacenterBroker("Broker2", 1, datacenter ,"FirstComeFirstServe", "LowestSpotScoreFirst", instanceConfigurationData)

        cloudletList = []

        demandFile = open("./Dataset/DemandData.csv",'r')
        demands = demandFile.readlines()[1:]
        demandParams = [demand.split(",") for demand in demands]

        cloudletList.append(Cloudlet.Cloudlet(id=1, highestRamUsage=1.604003906, averageRamUsage=1.604003906, length=9939638879))
        # cloudletList.append(Cloudlet.Cloudlet(id=2, highestRamUsage=2.62109375, averageRamUsage=2.62109375, length=3177483209))

        broker2.submitCloudletList(cloudletList)

        for cloudlet in cloudletList:
            printMessage("FinishedExecution", "\nCloudlet ID #" + str(cloudlet.getId()))
            printMessage("FinishedExecution", "VM TYPE\t\tEnd Time\t\tInstance Type\t\tMigration Event")
            for item in cloudlet.getRuntimeDistributionOnVm():
                printMessage("FinishedExecution", str(item[0]) + "\t\t" + str(item[1]) + (" " * (4 - len(str(item[1])))) + "\t\t" + ("Spot" if not item[2] else "On Demand") + "\t\t\t\t" + item[3])

    def createDatacenter(self, name):
        datacenterCharacteristics = DatacenterCharacteristics.DatacenterCharacteristics("x86", "Linux", "Xen", "Asia/Kolkata")
        datacenter = Datacenter.Datacenter(name, datacenterCharacteristics)
        return datacenter


t = Main()
t.test()

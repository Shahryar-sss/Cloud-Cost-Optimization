import DatacenterCharacteristics
import Datacenter
import DatacenterBroker
import Host
import Cloudlet
from PrintLogs import printMessage
from InstanceConfiguration import instanceConfigurationData
import ClockThread

class Main:

    def test(self):

        datacenter = self.createDatacenter("Datacenter_0")

        hostlist = []
        hostlist.append(Host.Host(id=0, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=1, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=2, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=3, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))

        datacenter.setHostList(hostlist)

        broker1 = DatacenterBroker.DatacenterBroker("Broker1", 0, datacenter, "FirstComeFirstServe", "FirstComeFirstServe", instanceConfigurationData)
        broker2 = DatacenterBroker.DatacenterBroker("Broker2", 1, datacenter, "FirstComeFirstServe", "LowestSpotScoreFirst", instanceConfigurationData)

        cloudletList = []

        demandFile = open("./Dataset/DemandDataMerged.csv",'r')
        demands = demandFile.readlines()[1:]
        demandParams = [demand.split(",") for demand in demands]

        for item in demandParams:
            cloudletList.append(Cloudlet.Cloudlet(id=demandParams.index(item), highestRamUsage=float(item[2]), averageRamUsage=float(item[3]), length=float(item[1])))

        broker2.submitCloudletList(cloudletList)

        for cloudlet in cloudletList:
            printMessage("OutputTables", "Cloudlet ID #" + str(cloudlet.getId()))
            printMessage("OutputTables", "VM TYPE\t\t\t\tEnd Time\tInstance Type\t\tMigration Event\t\tCost")
            tempRuntime=cloudlet.getRuntimeDistributionOnVm()
            for i in range(len(tempRuntime)):

                timeSpentOnVM = tempRuntime[i][1]-tempRuntime[i-1][1] if i > 0 else tempRuntime[i][1]
                startTime = tempRuntime[i-1][1] if i>0 else tempRuntime[i][1]

                costOnVM = 0
                for j in range(1, int(timeSpentOnVM/3600)+1):
                    costOnVM += float(instanceConfigurationData[tempRuntime[i][0]][4][int(startTime/60) + j*60])

                costOnVM += timeSpentOnVM % 3600 * float(instanceConfigurationData[tempRuntime[i][0]][4][int(timeSpentOnVM/60+startTime/60)]) / 3600

                printMessage("OutputTables", str(tempRuntime[i][0]) + (" " * (12 - len(str(tempRuntime[i][0])))) + "\t\t\t" + str(tempRuntime[i][1]) + (" " * (4 - len(str(tempRuntime[i][1])))) + "\t\t" + ("Spot" if not tempRuntime[i][2] else "On Demand") + "\t\t\t\t" + tempRuntime[i][3] + (" " * (9 - len(tempRuntime[i][3]))) + "\t\t" + str(costOnVM))
            printMessage("OutputTables", "\n")

    def createDatacenter(self, name):
        datacenterCharacteristics = DatacenterCharacteristics.DatacenterCharacteristics("x86", "Linux", "Xen", "Asia/Kolkata")
        datacenter = Datacenter.Datacenter(name, datacenterCharacteristics)
        return datacenter

t = Main()
t.test()

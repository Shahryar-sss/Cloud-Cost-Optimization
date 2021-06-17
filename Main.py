import DatacenterCharacteristics
import Datacenter
import DatacenterBroker
import Host
import Cloudlet

class Main:

    def test(self):

        datacenter = self.createDatacenter("Datacenter_0")

        hostlist = []
        hostlist.append(Host.Host(id=0, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=1, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=2, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=3, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))

        datacenter.setHostList(hostlist)

        broker1 = DatacenterBroker.DatacenterBroker("Broker1", 0, datacenter ,"FirstComeFirstServe", "FirstComeFirstServe")
        broker2 = DatacenterBroker.DatacenterBroker("Broker2", 1, datacenter ,"FirstComeFirstServe", "LowestSpotScoreFirst")

        cloudletList = []

        demandFile = open("./Dataset/DemandData.csv",'r')
        demand = demandFile.readlines()[1]
        demandParams = demand.split(",")

        cloudletList.append(Cloudlet.Cloudlet(id=1, highestRamUsage=1.604003906, averageRamUsage=0.009488242, length=7939638879))

        broker2.submitCloudletList(cloudletList)
        # broker2.submitCloudletList(cloudletList2)

        for cloudlet in cloudletList:
            print("Cloudlet ID #{}".format(cloudlet.getId()))
            print("VM ID\t\tEnd Time\t\tInstance Type")
            for item in cloudlet.getRuntimeDistributionOnVm():
                print("{}\t\t{}\t\t{}".format(item[0], item[1], "Spot" if item[2] == False else "On Demand"))

    def createDatacenter(self, name):
        datacenterCharacteristics = DatacenterCharacteristics.DatacenterCharacteristics("x86", "Linux", "Xen", "Asia/Kolkata")
        datacenter = Datacenter.Datacenter(name, datacenterCharacteristics)
        return datacenter


t = Main()
t.test()

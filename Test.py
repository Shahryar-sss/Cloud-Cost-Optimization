import DatacenterCharacteristics
import Datacenter
import DatacenterBroker
import Host
import Cloudlet

class Test:

    def test(self):

        datacenter = self.createDatacenter("Datacenter_0")

        hostlist = []
        hostlist.append(Host.Host(id=0, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))
        hostlist.append(Host.Host(id=1, availableRam=1024, bw=10.0, storage=1048576, mips=1000000))

        datacenter.setHostList(hostlist)

        broker = DatacenterBroker.DatacenterBroker("Broker", 0, datacenter ,"FirstComeFirstServe", "LowestSpotScoreFirst")

        cloudletList = []
        cloudletList.append(Cloudlet.Cloudlet(id=1, highestRamUsage=12.09375, averageRamUsage=0.007679621, length=4785113058))
        cloudletList.append(Cloudlet.Cloudlet(id=2, highestRamUsage=89.484375, averageRamUsage=0.008999961, length=3420260768))

        broker.submitCloudletList(cloudletList)

        for cloudlet in cloudletList:
            print("Cloudlet ID #{}".format(cloudlet.getId()))
            print("VM ID\t\tEnd Time\t\tInstance Type")
            for item in cloudlet.getRuntimeDistributionOnVm():
                print("{}\t\t{}\t\t{}".format(item[0], item[1], "Spot" if item[2] == False else "On Demand"))


    def createDatacenter(self, name):
        datacenterCharacteristics = DatacenterCharacteristics.DatacenterCharacteristics("x86", "Linux", "Xen", "Asia/Kolkata")
        datacenter = Datacenter.Datacenter(name, datacenterCharacteristics)
        return datacenter


t = Test()
t.test()

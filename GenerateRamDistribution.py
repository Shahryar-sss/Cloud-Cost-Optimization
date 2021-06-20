import numpy as np
import csv

def generateRamDistribution():
    file = './Dataset/DemandDataCompressed.csv'
    file1 = './Dataset/DemandDataWithRamDistribution.csv'
    with open(file, 'r') as read_obj, open(file1, 'w',newline='') as write_obj:
        csv_reader = csv.reader(read_obj)
        next(csv_reader)
        csv_write = csv.writer(write_obj)
        for row in csv_reader:

            avgRam = row[2]
            RamDistribution = ""
            i = 0
            while i < 1000:

                ram = np.random.normal(loc=float(avgRam), scale=0.1 * float(avgRam))

                if ram > 0:
                    if i < 999:
                        RamDistribution += str(ram) + "_"
                    else:
                        RamDistribution += str(ram)
                    i += 1

            row.append(RamDistribution)
            csv_write.writerow(row)

generateRamDistribution()

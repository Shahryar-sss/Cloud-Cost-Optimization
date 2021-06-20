import csv
import os
import pandas as pd

from PrintLogs import printMessage
instanceConfigurationData = {}

def instanceType():

    file = "./Dataset/instance_details.csv"
    spotdir = "./Dataset/spot_price_with_score"


    with open(file, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            tempList = [float(row[1].split(" ")[0])*1000000,float(row[2].split(" ")[0]),float(row[3].split(" ")[0]),float(row[4].split(" ")[0]),row[5]]
            instanceConfigurationData[row[0]] = tempList

    for files in os.walk((os.path.normpath(spotdir)), topdown=False):
        for name in files[2]:
            instanceName=name.split('_')[0]
            if instanceName in instanceConfigurationData:
                bucket=instanceConfigurationData[instanceName][4]
                instanceConfigurationData[instanceName]=instanceConfigurationData[instanceName][:-1]
                spotfilename = os.path.join(spotdir, name)
                temp=pd.read_csv(spotfilename,usecols=[1,2],names=['spotPrice','spotScore'])
                temp=temp.iloc[43201:,:]
                spotPriceList=temp['spotPrice'].values.tolist()
                spotScoreList=temp['spotScore'].values.tolist()
                instanceConfigurationData[instanceName].append(spotPriceList)
                instanceConfigurationData[instanceName].append(spotScoreList)
                instanceConfigurationData[instanceName].append(bucket)

printMessage("Misc", "Gathering instance configuration data from dataset")
instanceType()


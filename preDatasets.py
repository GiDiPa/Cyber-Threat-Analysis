import glob
import re
import os
import test
import gatherData

'''
#######################################################################################
##########################GDP CYBERINTELLIGENCE ASSIGNMENT#############################
############################started on 7th April 2020##################################
#######################################################################################

this file need to start creating all the datasets from data gathered from web.
The alexa file contains all benign sites, malign sites are gathered on multiple txt file. top1mExtract.py

maliciousfromcurl.py and dgaGen(script DGAGenerator) produce sets with union function(see code) to remove duplicates.
As suggested in the paper you gave, ds1 is with file requested from url, ds2 is with dga files!


Created also a function that execute regex to be sure on having only urls or ips(if we don't have urls on txt or csv files).
Useful in first commit, but not too much now(just kept).
#urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', page)
#ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', page)


In last part I create datasets as requested in pdf file, with the same numbers. I convert sets in lists(sets don't have index) and everytime
I add a textline in a file I delete the element from list, avoiding the risk of duplicates in different files!
''' 
    

#bit redundant but works as requested
def createDatasets(malignDS1,malignDS2,benign):
    benignList = list(benign)
    malignDS1List = list(malignDS1)
    malignDS2List = list(malignDS2)
    #create ds1 Training
    ds1Tr = open("DS1/preDs1Training.txt","w")
    for i in range(97506):
        ds1Tr.write(benignList[0].rstrip("\n") + " , 0\n")
        #ds1Tr.writelines("\n")
        benignList.pop(0)
    for i in range(77506):
        ds1Tr.writelines(malignDS1List[0])
        ds1Tr.writelines(" , 1")
        ds1Tr.writelines("\n")
        malignDS1List.pop(0)
    ds1Tr.close()
    #create ds2 Training
    ds2Tr = open("DS2/preDs2Training.txt","w")
    for i in range(49000):
        ds2Tr.write(benignList[0].rstrip("\n") + " , 0\n")
        #ds1Tr.writelines("\n")
        benignList.pop(0)
    for i in range(19005):
        ds2Tr.writelines(malignDS2List[0])
        ds2Tr.writelines(" , 1")
        ds2Tr.writelines("\n")
        malignDS2List.pop(0)
    ds2Tr.close()
    #create ds1 Test
    ds1Te = open("DS1/preDs1Test.txt","w")
    for i in range(15000):
        ds1Te.write(benignList[0].rstrip("\n") + " , 0\n")
        benignList.pop(0)
    for i in range(110012):
        ds1Te.writelines(malignDS1List[0])
        ds1Te.writelines(" , 1")
        ds1Te.writelines("\n")
        malignDS1List.pop(0)
    ds1Te.close()
    #create ds2 Test
    ds2Te = open("DS2/preDs2Test.txt","w")
    for i in range(20000):
        ds2Te.write(benignList[0].rstrip("\n") + " , 0\n")
        benignList.pop(0)
    for i in range(5000):
        ds2Te.writelines(malignDS2List[0])
        ds2Te.writelines(" , 1")
        ds2Te.writelines("\n")
        malignDS2List.pop(0)
    ds2Te.close()


def main():
    mergedMaliciousFromDGA = gatherData.dgaGen()
    benign = gatherData.BenignInSet()
    mergedMaliciosFromCurl = gatherData.getMaliciousSetDS1()
    createDatasets(mergedMaliciosFromCurl,mergedMaliciousFromDGA,benign)
    print ("Done")




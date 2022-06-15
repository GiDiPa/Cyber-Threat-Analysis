import modulesCompleteDS
from modulesCompleteDS import extractFDQN
from modulesCompleteDS import ipFromDomain
from modulesCompleteDS import entropyInDomainName
from modulesCompleteDS import extractTld
from modulesCompleteDS import extractCountry
from modulesCompleteDS import extractCity
from modulesCompleteDS import extractASOrganization
from modulesCompleteDS import extractASN
from modulesCompleteDS import numSubDomains
from modulesCompleteDS import isOnline
from modulesCompleteDS import whoisAge
import csv

#run this as python script without any function inside. 
#this is going to simply show how i get the data to fill fields
#inside the csv file. I just take the url from preDS.txt files and 
#recall every function in completeModules.py for the corrispective
#field.

finalDS2 = open('DS2/finalds2.csv' , 'a')
with finalDS2:
    writer = csv.writer(finalDS2)
    firstRow = ["Domain","Entropy","Online","IP","WhoisAge","Country","City","TLD","ASN","Organisation","#SubDomains","Class"]
    writer.writerow(firstRow)
    preDS2Test = open("DS2/preDs2Test.txt","r")
    for line in preDS2Test:
        fields = line.split(" , ")
        newRow = [extractFDQN(fields[0]),entropyInDomainName(fields[0]),isOnline(fields[0]),ipFromDomain(fields[0]),whoisAge(fields[0]),
            extractCountry(fields[0]),extractCity(fields[0]),extractTld(fields[0]),extractASN(fields[0]),
            extractASOrganization(fields[0]), numSubDomains(fields[0]),fields[1].strip("\n")]
        writer.writerow(newRow)
    preDS2Test.close()
    preDS2Training = open("DS2/preDs2Training.txt","r")
    for line in preDS2Training:
        fields = line.split(" , ")
        newRow = [extractFDQN(fields[0]),entropyInDomainName(fields[0]),isOnline(fields[0]),ipFromDomain(fields[0]),whoisAge(fields[0]),
            extractCountry(fields[0]),extractCity(fields[0]),extractTld(fields[0]),extractASN(fields[0]),
            extractASOrganization(fields[0]), numSubDomains(fields[0]),fields[1].strip("\n")]
        writer.writerow(newRow)
    preDS2Training.close()
finalDS2.close()

finalDS1 = open('DS1/finalds1.csv' , 'a')
with finalDS1:
    writer = csv.writer(finalDS1)
    firstRow = ["Domain","Entropy","Online","IP","WhoisAge","Country","City","TLD","ASN","Organisation","#SubDomains","Class"]
    writer.writerow(firstRow)
    preDS1Test = open("DS1/preDs1Test.txt","r")
    for line in preDS1Test:
        fields = line.split(" , ")
        newRow = [extractFDQN(fields[0]),entropyInDomainName(fields[0]),isOnline(fields[0]),ipFromDomain(fields[0]),whoisAge(fields[0]),
            extractCountry(fields[0]),extractCity(fields[0]),extractTld(fields[0]),extractASN(fields[0]),
            extractASOrganization(fields[0]), numSubDomains(fields[0]), fields[1].strip("\n")]
        writer.writerow(newRow)
    preDS1Test.close()
    preDS1Training = open("DS1/preDs1Training.txt","r")
    for line in preDS1Training:
        fields = line.split(" , ")
        newRow = [extractFDQN(fields[0]),entropyInDomainName(fields[0]),isOnline(fields[0]),ipFromDomain(fields[0]),whoisAge(fields[0]),
            extractCountry(fields[0]),extractCity(fields[0]),extractTld(fields[0]),extractASN(fields[0]),
            extractASOrganization(fields[0]), numSubDomains(fields[0]), fields[1].strip("\n")]
        writer.writerow(newRow)
    preDS1Training.close()
finalDS1.close()
'''

modules for gather data from txt or csv file and with dgagenerator package.
curlJsonFile takes url from a json array and put values in set.
curlXgetfiles takes txt file and extract url calling the module extractUrlOrIPs.
Then the getMaliciousSetDS1() function that merge sets into one (avoiding duplicates) and returning on preDatasets.py 

below the import for the curl functions
'''
import requests
import json
import urllib
import extractURLorIPS

''' 
adding the imports to call the modules needed to make dgagen() works.
'''
from datetime import date
from datetime import timedelta
from dgaGenerator.Necurs import Necurs
from dgaGenerator.Cryptolocker import Cryptolocker
from dgaGenerator.Ranbyus import Ranbyus
from dgaGenerator.ZeusBot import ZeusBot
from dgaGenerator.Torpig import Torpig
from dgaGenerator.Symmi import Symmi
# Compute domains for the current day/period:

def dgaGen():
    mergeDGA = set()
    # Compute domains for a given date:
    #x=Symmi.domainsFor(date(2020, 3, 31))
    start_date = date(2020, 4, 1)
    end_date = date(2020, 4, 17)
    delta = timedelta(days=1)
    dgaList = [Necurs,Cryptolocker,Ranbyus,ZeusBot,Torpig,Symmi]
    while start_date <= end_date:
        for i in dgaList:
            mergeDGA = mergeDGA.union(set(i.domainsFor(start_date)))
        start_date += delta
    return mergeDGA

#see the first comment
def curlJsonFile():
    setFromJson = set()
    response = requests.get('http://data.phishtank.com/data/b8809811972429c33d9525fae289ff3c6b77ab2284a53ed70213d6d3bcb5a41f/online-valid.json').json()
    for elem in response:
        setFromJson.add(elem["url"])
    return setFromJson

#see the first comment
def curlXGetFiles(url):
    file = str(urllib.request.urlopen(url).read().decode())
    return extractURLorIPS.extractURLsOrIPs(file)

#see the comment
def getMaliciousSetDS1():
    mergeUrlFiles = set()
    urls = ['https://openphish.com/feed.txt','https://urlhaus.abuse.ch/downloads/text/']
    mergeUrlFiles = mergeUrlFiles.union(curlJsonFile())
    for url in urls:
        mergeUrlFiles = mergeUrlFiles.union(curlXGetFiles(url))
    return mergeUrlFiles

'''
function that extract urls from top-1m.csv file and put into a set.
The reason why I'm putting in a set is to put everytime random lines to 
write on output files.
'''
def BenignInSet():
    toText = set()
    with open('benign/top-1m.csv', "r") as infile:
        for row in infile:
            toText.add(row.split(",")[1])
    return toText







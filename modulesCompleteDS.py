from urllib.parse import urlparse
import tldextract
import urllib.request
import socket
from tld import get_tld
import geoip2.database
import EntroPy.EntroPy
from collections import Counter
import requests
from requests import ConnectionError
from fake_useragent import UserAgent
import torproxy
import re
from search_engine_scraper import bing_search,yahoo_search
from SES import search_engines_cli


# this function extract the domain from URL. I added just an option
#to have always an URL with http:// format to compute as best as
#the library can (some url are just domain like google.com and I parse anyway
def extractFDQN(url):
    if not (url.startswith('//') or url.startswith('http://') or url.startswith('https://')):
        url = '//' + url
    urlTest = urlparse(url)
    return '{uri.netloc}'.format(uri=urlTest)
        
#check if domain is online or not. I recall extractFDQN() function and
#i do a request to see if I get 200 code(if I have a redirect I consider it
#and after response 301 check again if the redirect is online.
def isOnline(url):
    url = "http://" + extractFDQN(url)
    try:
        request = requests.get(url, allow_redirects = True, timeout = 1)
        return "Y"
    except Exception as e:
        return "N"
    
#this just extract the IP from domains, if available.
#There is a regex that check if the domain is an ip with port,
#and I remove the port and save the IP.
def ipFromDomain(url):
    url = extractFDQN(url)
    try:
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,5}$", url):
            ext = tldextract.extract(url)
            url = ext.domain
            s = socket.gethostbyname(url)
            return socket.gethostbyname(url)
        s = socket.gethostbyname(url)
        return socket.gethostbyname(url)
    except Exception as e:
        return "NULL"

#simple code that extract TLD. if url isn't with http:// format, 
#the library needs that
def extractTld(url):
    if not (url.startswith('//') or url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    try:
        return get_tld(url)
    except Exception as e:
        return "NULL"

#for the next 4 functions I used the Geolite2 Databases to fill my dataset. There are
#3 db to use: 1 for ASN and Organisation, 1 for City, 1 for Countries
#the functions are all similar. I extract ip from the domain and check 
#if the ip is in database
def extractASN(url):
    response = ipFromDomain(url)
    if (response == "NULL"):
        return "NULL"
    else:
        try:
            with geoip2.database.Reader('dbs/geoip2/GeoLite2-ASN.mmdb') as reader:
                response = reader.asn(response)
                if (response.autonomous_system_number is None):
                    return "NULL"
                return response.autonomous_system_number
        except Exception as e:
            return "NULL"

def extractASOrganization(url):
    response = ipFromDomain(url)
    if (response == "NULL"):
        return "NULL"
    else:
        try:
            with geoip2.database.Reader('dbs/geoip2/GeoLite2-ASN.mmdb') as reader:
                response = reader.asn(response)
                if (response.autonomous_system_organization is None):
                    return "NULL"
                return response.autonomous_system_organization
        except Exception as e:
            return "NULL"
    

def extractCountry(url):
    response = ipFromDomain(url)
    if (response == "NULL"):
        return "NULL"
    else:
        try:
            reader = geoip2.database.Reader('dbs/geoip2/GeoLite2-Country.mmdb')
            response = reader.country(response)
            if (response.country.iso_code is None):
                return "NULL"
            return response.country.iso_code
        except Exception as e:
            return "NULL"
    

def extractCity(url):
    response = ipFromDomain(url)
    if (response == "NULL"):
        return "NULL"
    else:
        try:
            reader = geoip2.database.Reader('dbs/geoip2/GeoLite2-City.mmdb')
            response = reader.city(response)
            if (response.city.name is None):
                return "NULL"
            return response.city.name
        except Exception as e:
            return "NULL"

#with this function I check the number of subdomains for each url
#in my predataset. the first thing I do is to check if 
#url extracted has an ip and if is not an IP as Url. Then 
#when I enter if condition I call the function from 
#Search engine scraper that works to find the number of subdomain.
#The rest is explained in that py file.
def numSubDomains(url):
    try:
        ip = ipFromDomain(url)
        ext = tldextract.extract(url)
        compareIpUrl = ext.domain
        if ip != "NULL" and ip != compareIpUrl:
            return search_engines_cli.numSubDom(ip,ext)
    except Exception as e:
        return "NULL"

#using the entroPy package to extract the entropy
#from domain name. if is an ip is NULL, otherwise 
#I compute the probability of the letters in 
#domain name. That function create a dictionary to pass 
#at function that calculate shannon entropy.
def entropyInDomainName(url):
    ext = tldextract.extract(url)
    url = ext.domain
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",url):
        return "NULL"
    prob = EntroPy.EntroPy._probabilities(url)
    return EntroPy.EntroPy.shannon_entropy(prob)

#this function is needed when we search on whois API
#the days since a site has been renewed or created.
#See that file to have more details.
#It is a must having a tor proxy because whois api
#return error with reached limit with same public IP
def whoisAge(url):
    ip = ipFromDomain(url)
    if (ip == "NULL"):
        return "NULL"
    else:
        return torproxy.torWhois(ip)








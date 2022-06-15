'''
function for regex on txt file and extract url or Ip(ips just in case I do not find any url)
'''

import re

def extractURLsOrIPs(fileContent):
    if (re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+~]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fileContent) is not None):
        urls = set(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+~]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fileContent))
        return urls
    else:
        ips = set(re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', fileContent))
        return ips
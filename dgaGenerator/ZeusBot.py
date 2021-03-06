#!/usr/bin/env python3
import datetime
import sys
import hashlib

from dgaGenerator.DGAMalware import DGAMalware
"""A few constants for that DGA.

TLDs used and length of the MD5 hash.

"""
tlds = [".ru", ".biz", ".info", ".org", ".net", ".com"]
HASHLEN = 16

"""Domain Generation Algorithm for ZeusBot.

Source:
  http://vrt-blog.snort.org/2014/03/decoding-domain-generation-algorithms.html
  Dave
  March 6, 2014

"""
class ZeusBot(DGAMalware):

  """
  The lifetime of ZeusBot's DGA domains if 7 by default
  but they also change on the first of the month.
  """
  @classmethod
  def domainsLifetime(self):
    return 7 * 24 * 3600
  
  @classmethod
  def domainsFor(self, date):
    domains = []
    dateData = self.genDate(date)
    nb_ok = 0
    nb_total = 0
    for i in range(1000):
      # Reverse order of bytes when generating URLs.
      # This will match the order in how it URLs are incremented in the malware itself.
      hibyte = (i >> 8) & 0xff
      lobyte = i & 0xff

      pbData = [dateData[0], dateData[1], dateData[2], lobyte, hibyte, 0x00, 0x00]
      hashValue = self.getMD5Hash(pbData)
      
      domain = ""
      URL = self.genURL(hashValue)
      for k in range(len(URL)):
        domain += "%c" % URL[k]
      
      TLD = self.genTLD(i)
      # Random value (Before flipping it around for the hash).
      for k in range(len(TLD)):
        domain += "%c" % TLD[k]
      domains.append(domain)
    return domains


  @classmethod
  def couldUseDomain(self, domain):
    useTLD = False
    for tld in tlds:
      if domain.endswith(tld):
        useTLD = True
        break
    if not useTLD:
      return False
    return not any(char.isdigit() for char in domain)


  @classmethod
  def genDate(self, date):
    # Add 30h to last byte of year.
    year = ((date.year) & 0xff) + 0x30
    day = (date.day // 7) * 7
    dateData = [year % 256, date.month, day]
    return dateData


  # Generate TLD based on random seed based on low-byte of random seed.
  @classmethod
  def genTLD(self, rand):
    lobyte = rand & 0xff
    if (rand % 6) == 0:
      TLD = tlds[0]
    elif (rand % 5) == 0:
      TLD = tlds[1]
    elif (lobyte & 3) == 00:
      TLD = tlds[2]
    elif (rand % 3) == 0:
      TLD = tlds[3]
    elif (lobyte & 1) == 0:
      TLD = tlds[4]
    else:
      TLD = tlds[5]
    return TLD


  # Generate URL based on MD5 hash.
  @classmethod
  def genURL(self, hashValue):
    # Grab each byte of hash.
    URL = ""
    for j in range(HASHLEN):
      cl = hashValue[j]
      dl = cl
      dl = (dl & 0x1F) + 0x61
      cl = (cl >> 3) + 0x61
      if cl != dl:
        if dl <= 0x7A:
          URL += chr(dl)
        if cl <= 0x7A:
          URL += chr(cl)
    return URL


  # Compute the MD5 checksum for generated bytes
  @classmethod
  def getMD5Hash(self, pbData):
    inputStr = ""
    for value in pbData:
      inputStr += chr(value)
    
    digest = hashlib.md5(inputStr.encode('latin-1')).digest()

    outputStr = []
    for i in range(HASHLEN):
      outputStr.append(digest[i])
    return outputStr[0: HASHLEN]

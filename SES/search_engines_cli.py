# -*- encoding: utf-8 -*-
import argparse
import csv
from stem import Signal
from stem.control import Controller
import re
import tldextract
from modulesCompleteDS import extractFDQN
from collections import Counter
try:
    from search_engines.engines import search_engines_dict
    from search_engines.multiple_search_engines import MultipleSearchEngines, AllSearchEngines
    from search_engines import config
except ImportError as e:
    msg = '"{}"\nPlease install `search_engines` to resolve this error.'
    raise ImportError(msg.format(str(e)))

# with help of a tor proxy I just use bing dorks to see with an ip
#as query ip:"172.34.55.97" (example) how many numbers of subdomain has.
#I bring with me ip and ext value from completeModules.py with numSubDomain()
#function.
def numSubDom(ip,ext):
    with Controller.from_port(address='192.168.56.3', port=9051) as controller:
        controller.authenticate(password='lsirc')
        controller.signal(Signal.NEWNYM)
        controller.close()

    proxy="http://192.168.56.3:8118"
    timeout=config.TIMEOUT + (10 * bool(proxy))
    engines=['bing']  # ['all','google','bing']
    #IP="193.136.58.218"
    if not engines:
        print('Please choose a search engine: ' + ', '.join(search_engines_dict))
    else:
        if 'all' in engines:
            engine = AllSearchEngines(proxy, timeout)
        elif len(engines) > 1:
            engine = MultipleSearchEngines(engines, proxy, timeout)
        else:
            engine = search_engines_dict[engines[0]](proxy, timeout)
        filter = None  #[url, title, text, host]', default=None
        if filter:
            engine.set_search_operator(filter)
        query="ip:\"" + ip + "\""
        pages=10
        listlink = list(engine.search(query, 10))
        domain = "{}".format(ext.registered_domain)
        useful = [] #html, csv, json
        #i collect the list of results and then in for loop I see how many
        #links has the same subdomain name as the url given in input.
        #finally i just return the number of subdomain. 
        #I use the torproxy for this operation because after many request with
        #same ip returns error(yahoo and google) or 0(bing case).
        for i in listlink:
            tempUrl = extractFDQN(i['link'])
            if (tldextract.extract(tempUrl).registered_domain == domain):
                useful.append(tempUrl)
        return len(Counter(useful).keys())




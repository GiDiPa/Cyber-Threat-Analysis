import requests
from stem import Signal
from stem.control import Controller
from datetime import datetime
from datetime import date
from fake_useragent import UserAgent

def torWhois(ip):
    if ip == "NULL":
        return "NULL"
    else:
        with Controller.from_port(address='192.168.56.3', port=9051) as controller:
            controller.authenticate(password='lsirc')
            controller.signal(Signal.NEWNYM)
            controller.close()
        ua = UserAgent()
        proxies = {"http": "http://192.168.56.3:8118"}
        headers = {'User-Agent': ua.random}
        IP = ip
        """
        "https://rdap.lacnic.net/rdap/ip/"+IP
        # Latin America and Caribbean
        "http://rdap.afrinic.net/rdap/ip/"+IP
        # Africa
        "http://rdap.apnic.net/ip/"+IP
        # Asia/Pacific only
        "http://rdap.arin.net/registry/ip/"+IP # North America only
        "http://rdap.db.ripe.net/ip/"+IP
        # Europe, Middle East and
        "http://rdap.registro.br/ip/"+IP
        # Brazil
        """
        #in this case this function is called by whoisAge in completeModules.py
        #using torproxy.py I check how many years ago(expressed in days) the url
        # was renewed or created. I access the json file and then I search on 
        # field events that contain the needed information.
        # I take always the first position because in all cases, if exist, 
        # the first place is for renewals, if don't, is a created value.
        # Then I do calculate to return the value expressed in days.  
        #the URL List variable is needed to verify the ip in different databases
        #because not everyone contains information I need.
        now = datetime.now().date()
        URL = ["http://rdap.db.ripe.net/ip/" + IP,"http://rdap.registro.br/ip/" + IP,"http://rdap.arin.net/registry/ip/" + IP,"http://rdap.apnic.net/ip/"+IP, "https://rdap.lacnic.net/rdap/ip/" + IP]
        try:
            for url in URL:
                r = requests.get(url, proxies=proxies, headers=headers)
                if r.status_code != 404:
                    r = r.json()
                    if r['events'][0]:
                        age = datetime.strptime(r['events'][0]['eventDate'][0:10], "%Y-%m-%d").date()
                        days = now - age
                        return days.days
        except Exception as e:
            return "NULL"    



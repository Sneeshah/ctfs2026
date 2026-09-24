# 2FA simple bypass

**Category:** Web Exploitation — Authentication
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-simple-bypass`

This lab's two-factor authentication can be bypassed. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, access Carlos's account page.

- Your credentials: wiener:peter
- Victim's credentials carlos:montoya

---

## Reconnaissance

- What does the application do? 
    - The website is a blog about several, seemingly to tech related topics. Users can read and leave comments under blog articles.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - There is an account page with a login, the comments below articles can be consideres input too.
- What happens with normal input?
    - Correct user logins log the user in normally after using the email client to retrieve the second client

---

## Analysis


#### Vulnerability

- What exactly is vulnerable and why?
    
The 2FA implementation is vulnerable due to not checking the second factor (code sent to email) properly before logging in.

---

## Solution 

### Step 1 - Recon / Looking at responses

This lab attaches an email client to retrieve the second factor. 
On every login there is a code generated that is sent to the email server.
The url before logging in (the login screen) is: `https://0adc00fe043db3858043540800650079.web-security-academy.net/login`
The url after inserting the correct username and password is: `https://0adc00fe043db3858043540800650079.web-security-academy.net/login2`
When logged in the url is `https://0adc00fe043db3858043540800650079.web-security-academy.net/my-account?id=wiener`


---

### Step 2 - Enumeration / Step 3 - Exploit

The code seems to be verified after logging in (url changes login to login2) so after inputting the loginname `wiener` with the password `peter` it is possible to simple remove `login2` and replace it with `my-account?id=wiener` and log in. 
Now the same should work for the given target account (`carlos:montoya`), this time with the url query ending with `my-account?id=carlos`. 
This solves the lab.

---
## Real World Impact

This is pretty bad, this 2FA does practically nothing but gives a false sense of security. 2FA is used specifically so an attacker can't get system access without a second factor but in this case he doesn't need it. Getting a username/password combination is often not a problem for the attacker, there are lots of leaks and he can still use bruteforce. 
This method of securing 2FA is not protecting against that.

---
## Learnings
- Always validate all factors before logging in.

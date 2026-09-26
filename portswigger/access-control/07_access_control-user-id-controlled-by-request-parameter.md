# User ID controlled by request parameter 

**Category:** Web Exploitation — Access control
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter`

This lab has a horizontal privilege escalation vulnerability on the user account page.
To solve the lab, obtain the API key for the user carlos and submit it as the solution.
You can log in to your own account using the following credentials: wiener:peter 

---

## Reconnaissance

- What does the application do? 
    - The website is a shop with an account functionality. Users can look at the details of items on the homepage.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - User input is allowed for the login page and potentially the url
- What happens with normal input?
    - Unable to say for now, normal input for the login functionality should just login the user

---

## Analysis


#### Vulnerability

This is a classic Insecure Direct Object Reference (IDOR) vulnerability. The server is not verifing if a user is authorized to access that specific user record.

---

## Solution 

### Step 1 - Recon / Looking at responses

Not much to see here. Log in as `wiener` with `peter` as a password and notice the url: `https://0aba00900378c89f82d61f2a00510056.web-security-academy.net/my-account?id=wiener`
In the account it shows the API key, so presumably for other users it is the same and every user has their own key.

---

### Step 2 - Enumeration / Step 3 - Exploit

Changing the url to: `https://0aba00900378c89f82d61f2a00510056.web-security-academy.net/my-account?id=carlos` takes us to carlos account. His API-Key is `RPLAoM7XOKFALvQNxwIVypdOmiUplaLx`.
Submitting that to the solution solves the lab. 

---
## Real World Impact

One of the easiest ways to do privilege escalation (in this case horizontal) is devastating for any system. The server needs to check if a user actually owns the object he tries to access. If an attacker finds a site like this he is free to get information about any account in the system. And chances are that admin accounts are also not secured properly in such an environment and an attacker can escalate vertically as well.

---
## Learnings

- IDOR needs two things: a direct/guessable object like a username and no server-side check of ownership on that request


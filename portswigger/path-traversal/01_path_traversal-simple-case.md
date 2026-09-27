# File path traversal, simple case
**Category:** Web Exploitation — Path traversal
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/file-path-traversal/lab-simple`

This lab contains a path traversal vulnerability in the display of product images.
To solve the lab, retrieve the contents of the /etc/passwd file. 

---

## Reconnaissance

- What does the application do? 
    - The website is a shop. 
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - No input anywhere
- What happens with normal input?
    - No input anywhere

---

## Analysis


#### Vulnerability

Classic path traversal vulnerability, no defenses in this lab yet.

---

## Solution 

### Step 1 - Recon / Looking at responses

Requests and responses look normal but when the users clicks on a shop page the url changes to `https://0af30025038ef888824bf11b005400bc.web-security-academy.net/product?productId=4` 
At that page the pictures have to be loaded from somewhere. And the response tells us where from: 
```
                       <img src="/resources/images/rating5.png">
                        <div id="price">$39.07</div>
                        <img src="/image?filename=33.jpg">
```


---
### Step 2 - Enumeration / Exploitation

Sending the mentioned request to repeater and changing it to `GET image?filename=../../../etc/passwd` prints the contents of `passwd` in the response. This solves the lab.

---
## Real World Impact

This vulnerability lets any user access any readable file, like passwd or config files. An attacker using this could get database access, find leaked credentials or escalate his privileges.

---
## Learnings

- any paramter that reads a file could be susceptible to path traversal
- can't do it straight in the browser since it normalizes `../` need to do it in burp directly

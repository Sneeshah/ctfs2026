# File path traversal, traversal sequences blocked with absolute path bypass
**Category:** Web Exploitation — Path traversal
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass`

This lab contains a path traversal vulnerability in the display of product images.
The application blocks traversal sequences but treats the supplied filename as being relative to a default working directory.
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

Classic path traversal vulnerability, this time the application strips `../` sequences from the request.

---

## Solution 

### Step 1 - Recon / Looking at responses

The server filters `../` from the request and returns `No such file` as per the labs name an absolute path should work.
---
### Step 2 - Enumeration / Exploitation

Changing the request for an image to `GET /image?filename=/etc/passwd HTTP/2` is successfull and the response includes the contents of the passwd file

---
## Real World Impact

This vulnerability lets any user access any readable file, like passwd or config files. An attacker using this could get database access, find leaked credentials or escalate his privileges.

---
## Learnings

- sometimes applications use a simple 'dumb' filter to just filter `../` sequences. The simple workaround is an absolute path which is even easier than the original solution

# File path traversal, traversal sequences stripped non-recursively
**Category:** Web Exploitation — Path traversal
**Difficulty:** Practicioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/file-path-traversal/lab-sequences-stripped-non-recursively`

This lab contains a path traversal vulnerability in the display of product images.
The application strips path traversal sequences from the user-supplied filename before using it.
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

Classic path traversal vulnerability, this time the application strips `../` sequences from the request but the full path input does not work since the server apparently adds the input to a fixed base directory.

---

## Solution 

### Step 1 - Recon / Looking at responses

The server seems to strip `../` again from the request. This time not taking the input as a path from the home directory but instead from a fixed base directory like `/var/www/images/` feeding `/etc/passwd/` into that creates `/var/www/images//etc/passwd` which obviously cant work.
If the server really strips `../` then the crafted payload needs to be able to survive that strip. Maybe with something like `....//`

---
### Step 2 - Enumeration / Exploitation

yep, that was the correct thought changing the request to `GET /image?filename=....//....//....//etc/passwd HTTP/2` solves the lab and prints the passwd file

---
## Real World Impact

This vulnerability lets any user access any readable file, like passwd or config files. An attacker using this could get database access, find leaked credentials or escalate his privileges.

---
## Learnings

- nexsting beats stripping non-recursively.
- nesting forbidden patterns inside themselves is an easy way to circumvent (`....//`, `..././`. `....\/` can all work)
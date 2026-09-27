# File path traversal, validation of file extension with null byte bypass
**Category:** Web Exploitation — Path traversal
**Difficulty:** Practicioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/file-path-traversal/lab-validate-file-extension-null-byte-bypass`

This lab contains a path traversal vulnerability in the display of product images.
The application validates that the supplied filename ends with the expected file extension.
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

Exactly the opposite of last lab. The security check only checks the ending of the input for the correct file extension, while the actual file read works for the whole input until it hits a null byte.

---

## Solution 

### Step 1 - Recon / Looking at responses

This time the application has a normal path inside its usual response again. But the lab name strongly hints at the solution. 

---
### Step 2 - Enumeration / Exploitation

Using nullbytes to circumvent the file extension check means changing the header from `GET /product?productId=3 HTTP/2` to `GET /image?filename=73.jpg HTTP/2` and then finally to `GET /image?filename=../../../etc/passwd%00.png HTTP/2`

`%00` basically cuts the paramter in two pieces. The extension check reads `../../../etc/passwd\0.png` and accepts it. 
The underlying function that calls the file usually stops reading at the first null byte (old convention from C) which means the passwd file is read and send in the response

---
## Real World Impact

This vulnerability lets any user access any readable file, like passwd or config files. An attacker using this could get database access, find leaked credentials or escalate his privileges.

---
## Learnings

- this is a really old vulnerability and does not work on newer versions (PHP killed null-byte poisoning in 5.3.4 in 2010, rejecting any path containing \0, java also rejects it )
- an easy fix to all these path traversals is not passing user-supplied input into filesystem-APIs and if that can not be avoided to validate input before processing - use whitelisting (deny default) and canonicalize (resolve path to its true form) the input before verifying the path still ends in an allowed directory. 
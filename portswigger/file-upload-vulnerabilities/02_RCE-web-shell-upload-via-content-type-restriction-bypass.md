# Web shell upload via Content-Type restriction bypass
**Category:** Web Exploitation — file upload vulnerability
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass`


---

## Reconnaissance

- What does the application do? 
    - The website is a blog with account functionality. Users can leave comments on blogs and use pictures as an avatar
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - When commenting or logging in, pictures can be uploaded as an avatar


---

## Analysis


#### Vulnerability

The extensions of the upload are checked by the server now but the method used is flawed. Checking the `Content-Type`-header does not validate the fieltype reliably since it is a client-controlled value which an attacker can easily change.

---

## Solution 

### Step 1 - Recon / Looking at responses

Upload function seems like last lab. Uploading a `test.png` works the same.

---
### Step 2 - Enumeration / Exploitation

The upload uses the header `Content Disposition`, which uses the header `Content-Type` specifying the type of file uploaded. Uploading a `shell.php` is refused because the `Content-Type`-header is set to `application/octet-stream` when `shell.php` is uploaded. This can be changed to image/jpeg in burp repeater with the same php-file which returns a successfull response. Reloading the website shows the request: `GET /files/avatars/shell.php` which has the secret in the response (same request is made for normal uploads as well to get the picture shown on the website).

---
## Real World Impact

Webserver executes any uploaded code -> Remote Code execution. An attacker abusing this could read all the files on the server including passwd. 

---
## Learnings

- `Content-Type`-header is client-controlled -> should not be trusted for validations
- THE CLIENT SHOULD NEVER BE TRUSTED, VALIDATION NEEDS TO BE SERVER SIDE
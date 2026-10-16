# Web shell upload via extension blacklist bypass
**Category:** Web Exploitation — file upload vulnerability
**Difficulty:** Practitioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass`

This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed due to a fundamental flaw in the configuration of this blacklist.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.
You can log in to your own account using the following credentials: wiener:peter 

---

## Reconnaissance

- What does the application do? 
    - The website is a blog with account functionality. Users can leave comments on blogs and use pictures as an avatar
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - When commenting or logging in, pictures can be uploaded as an avatar


---

## Analysis


#### Vulnerability

This time the uploadfilter uses a blocklist, but this is a problem cause a blocklist is limited to extensions it knows. By changing the fiels associated with php through uploading a config file it can be circumvented entirely.

---

## Solution 

### Step 1 - Recon / Looking at responses

Upload of a legit PNG as a profile picture works as in the other labs. The Post-request that uploads the picture also gets the same response specifying the filepath where it is uploaded to.
php-files are not allowed and will be rejected.
Changing the filename `shell1.php` to `shell1.php.png` is a trick I used once, maybe it works here too. 
And yeah it uploads at least. But visiting `https://0a10007e03c6478f810c111b009c00ec.web-security-academy.net/files/avatars/shell1.php.png` shows an error saying the file is faulty. So this trick does not work here.

---
### Step 2 - Enumeration / Exploitation

In the academy they described uploading configuration files, so let's try that.
Uploading a `.htaccess`-file with the following content:
```
AddType application/x-httpd-php .hello
```
works as expected and uploads. 
Now changing the filename of our web shell to `shell1.hello` is uploadable and works. After uploading accessing `/files/avatars/shell1.hello` shows the secret to solve the lab.

---
## Real World Impact

Webserver executes any uploaded code -> Remote Code execution. An attacker abusing this could read all the files on the server including passwd. 

---
## Learnings

- extension blocklists are not reliable, whitelists are better.
- always worth to check if uploading config files like `.htaccess` or `web.config` 
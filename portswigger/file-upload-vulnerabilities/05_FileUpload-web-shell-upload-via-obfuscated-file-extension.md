# Web shell upload via obfuscated file extension
**Category:** Web Exploitation — file upload vulnerability
**Difficulty:** Practitioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-obfuscated-file-extension`

This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed using a classic obfuscation technique.
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

This time the file upload is filtered. Only PNG and JPG are accepted, but the filter simply looks at the last extension e.g. what comes after the last dot. By adding nullbytes before the extension this can be circumvented since the validation happens in a high-level language but the server processes the file in some low-level function creating a discrepancy in what is treated as a filename.
The validator basically sees: `shell1.php%00.png` and checks that `.png` is the last extension. The server saving the file stops reading at `%00` thus saving `shell1.php`

---

## Solution 

### Step 1 - Recon / Looking at responses

On uploading the standard `.php`-shell, the message returned indicates only JPG and PNG files are valid.
This time the lab is all about obfuscating the file extension. Let's first try changing the file extension to `.php.png` and see if it works.
Seems to work, let's access `files/avatars/shell1.php.png` to see if it worked. Sadly an error, let's try `png.php` -> Denied.
Since the first returned message tells us we definetly need a PNG or JPG file we know the last extension is read now and it needs to be either of those. That also means uploading a file named `shell1.php.` with a trailing dot won't work (no png/jpg found). 
Let's try adding null byte characters like the lab described.

---
### Step 2 - Enumeration / Exploitation

Adding nullbytes worked. First input was `shell1.asp%00.png` which was uploaded as `shell1.asp`, trying the same with php instead of asp worked and uploaded it. Under `/files/avatars/shell1.php` the secret was revealed.

---
## Real World Impact

Webserver executes any uploaded code -> Remote Code execution. An attacker abusing this could read all the files on the server including passwd. 

---
## Learnings

- tricking the extension filter depends onthe underlying server, Apache, Windows, Linux all behave different
- Null-byte bypass = validator and server see different filenames is similiar to [Path Traversal Lab 6](../path-traversal/06_path_traversal-validation-of-file-extension-with-null-byte-bypass.md)
# Source code disclosure via backup files
**Category:** Web Exploitation — Information disclosure
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-via-backup-files`

This lab leaks its source code via backup files in a hidden directory. To solve the lab, identify and submit the database password, which is hard-coded in the leaked source code. 

---

## Reconnaissance

- What does the application do? 
    - The website is a shop. No account functionality
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - No user input except maybe the url
- What happens with normal input?
    - No normal user input

---

## Analysis


#### Vulnerability

Credentials should never be hardcoded like that. The file in `/backup` is `.bak` so it is not executed (the server does not know how to) and thus easily readable. A backup file like this should not be left to view for normal users.

---

## Solution 

### Step 1 - Recon / Looking at responses

No `/sitemap.xml`. But there is a `/robots.txt` and it includes the backup directory: `/backup/`. `/backup` includes a file called `ProductTemplate.java.bak` which contains the password used to solve this lab: `bj3fwlpds9fxs1zplqts6ife6a15v4gh`

---


## Real World Impact

After getting a password like this an attacker can freely read, write, copy or even delete the database. The database key should NEVER be accessible on client-side. Any leak of it can be detrimental. Hardcoding secrets is bad practice, they are often forgotten in backup or config files and turn a leak into full access.

---
## Learnings

- hidden directories might include files that have value information (like in this case a database password)

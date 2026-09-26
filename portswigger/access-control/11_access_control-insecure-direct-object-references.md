# Insecure direct object references

**Category:** Web Exploitation — Access control
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/access-control/lab-insecure-direct-object-references`

This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs.
Solve the lab by finding the password for the user carlos, and logging into their account. 

---

## Reconnaissance

- What does the application do? 
    - The website is a shop with an account functionality. Users can look at the details of items on the homepage.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - User input is allowed for the login page and potentially the url, the website now has a live chat which allows users even without account to chat (with a bot)
- What happens with normal input?
    - Unable to say for now, normal input for the login functionality should just login the user. Normal chat input is just pasted into the chat

---

## Analysis


#### Vulnerability

Insecure direct object refernces (IDOR) on a filesystem object. Transcript stored in static files that are named sequentially makes condition 1 for IDORs (knwowing the reference in this case filename) trivial. There also is no ownership check for these files, so anyone can access them.

---

## Solution 

### Step 1 - Recon / Looking at responses

This time no login. Instead user chatlogs are stored on the servers filesystem and retrieved by static urls. The chat system works but putting in for example `<b>hello</b> prints the text in bold hinting at an XSS vulnerability there.
There is also a button to view the transcript of the chat which in this case downloads a `.txt` file.
In my case that file is named `2.txt`. This suggests the files are named with an increasing counter. 

---

### Step 2 - Enumeration / Step 3 - Exploit

Using burp repeater I can take a look at `1.txt` by simnply chainging the GET-request from `GET /download-transcript/2.txt HTTP/2` to `GET /download-transcript/1.txt HTTP/2` and indeed there is a user asking the bot for their password: `4voxlqbb2bk0rq7eta41`
Using this password to login as carlos solves the lab.

---
## Real World Impact

This bug lets attackers enumerate the files and bulkd download any transcript stored on the server. This can be a huge amount of useless information but there might be sensitive information like in this case a password as well. The fix to this is to do an ownership check before letting a user download a transcript. That way users can only download their own chat with the bot.

---
## Learnings

- even files can leak information, always try out all the functions a website is offering
- sequential integers are super easy references for IDORs, no guessing needed
# Blind OS command injection with output redirection
**Category:** Web Exploitation — OS Command Injection
**Difficulty:** Practicioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection`

This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response. However, you can use output redirection to capture the output from the command. There is a writable folder at:
/var/www/images/

The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.

To solve the lab, execute the whoami command and retrieve the output. 

---

## Reconnaissance

- What does the application do? 
    - The website is a shop. There is a feedback form too
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - Only the feedback form accepts input
- What happens with normal input?
    - When fedback is submitted an email with feedback is sent.

---

## Analysis


#### Vulnerability

This is textbook os command injection - the app takes input from a user and feeds it straight into a shell command (similiar to sql injections). The only challenge here is that this injection ios blind but with redirecting the output to a known file this is not really a problem


---

## Solution 

### Step 1 - Recon / Looking at responses

Same feedback system as last lab. `& ping -c 10 127.0.0.1 &` delays the response again.

---
### Step 2 - Enumeration / Exploitation

As instructed whoami with redirecting output to `/var/www/images/` which like this `|| whoami > /var/www/images/output.txt ||` or `||+whoami+>+/var/www/images/output.txt+||` in encoded form.
Turning the filter for images off in burp proxy shows requests for images too, changing the request to `GET /image?filename=output.txt HTTP/2` prints the username and finishes the lab
Using `&` at the end of our payload does not work since it break the logic in the shell and presumably throws an error there. That is why `||` or `#` work better here

---
## Real World Impact


Dangerous vulnerability, the attacker can run any command here. That means reading, stealing or deleting any file including credentials, API keys etc. Even creating a backdoor for easier access is possible. Basically a full server compromise right here.

---
## Learnings

- blind can turn into non-blind if there is a read and writeable directory
- can use `#` (comment) instead of `||` after the payload too, might be cleaner 
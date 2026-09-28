# Blind OS command injection with time delays
**Category:** Web Exploitation — OS Command Injection
**Difficulty:** Practicioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays`

This lab contains a blind OS command injection vulnerability in the feedback function.
The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response.
To solve the lab, exploit the blind OS command injection vulnerability to cause a 10 second delay. 

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

This is textbook os command injection - the app takes input from a user and feeds it straight into a shell command (similiar to sql injections). The only challenge here is that this injection does not instantly return output in the response, making it a blind injection.


---

## Solution 

### Step 1 - Recon / Looking at responses

Since the lab is talking about a blind injection lets use the trick we learned: `& ping -c 10 127.0.0.1 &` to see if the server actually executes our command. The trailing `&` is needed so the arguments after it do not glue onto the ping command and break it.
The POST-request sends the inputted data like this `csrf=6v2b9htV2eDSg2NOGaBMtu4WCikd6ins&name=hello&email=hello%40hello.de&subject=sd&message=Hello`
Trying one paramater at a time and replacing its value with `hello%26%20%70%69%6e%67%20%2d%63%20%31%30%20%31%32%37%2e%30%2e%30%2e%31%20%26&`. `%26%20%70%69%6e%67%20%2d%63%20%31%30%20%31%32%37%2e%30%2e%30%2e%31%20%26&` is just the URL-encoded ping command.

---
### Step 2 - Enumeration / Exploitation

The injection only worked on the email paramter. We know that since the response did only come 10 seconds after the request. That also solves the lab.

---
## Real World Impact


Dangerous vulnerability, the attacker can run any command here. That means reading, stealing or deleting any file including credentials, API keys etc. Even creating a backdoor for easier access is possible. Basically a full server compromise right here.

---
## Learnings

- time can be an oracle for OS command injection. 
- wrapping payloads into `&....&` isolates the command from the parameters
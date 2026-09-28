# OS command injection, simple case
**Category:** Web Exploitation — OS Command Injection
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/os-command-injection/lab-simple`

This lab contains an OS command injection vulnerability in the product stock checker.
The application executes a shell command containing user-supplied product and store IDs, and returns the raw output from the command in its response.
To solve the lab, execute the whoami command to determine the name of the current user. 

---

## Reconnaissance

- What does the application do? 
    - The website is a shop. Every item also has the functionality to check its stock in different locations.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - No input anywhere on the website
- What happens with normal input?
    - No input anywhere on the website

---

## Analysis


#### Vulnerability

This is textbook os command injection - the app takes input from a user and feeds it straight into a shell command (similiar to sql injections). The intended command probably looked like reportstock.sh <productID> <storeID>

---

## Solution 

### Step 1 - Recon / Looking at responses

When checking the stock a POST-request is send to the server with the specific `productid` and `storeID`.
Now there are only 3 stores - so what happens if `storeId` is set to smth else than 1, 2 or 3. 
The answer is the website does not work properly but returns a two-digit number - no matter the input. Same happens when tampering with `productID`.
It also happens when one or both paramters are strings which makes no sense at all.
When appending a `"` to a paramter a syntax error is returned so it seems like this input is fed straight into some kind of shell command.
Using `&` to run `echo "hello"` does not work since `&` is the form field seperator here.
`productId=55&storeId=45 | echo "hello"` returns `hello` so we can inject commands. 

---
### Step 2 - Enumeration / Exploitation

`productId=55&storeId=45 | whoami` returns the current user `peter-72KaOs` and the lab is solved.
Alternatively to use `&` it can be encoded like this:
productId=55&storeId=45%26%20%77%68%6f%61%6d%69

---
## Real World Impact

Dangerous vulnerability, the attacker can run any command here. That means reading, stealing or deleting any file including credentials, API keys etc. Even creating a backdoor for easier access is possible. Basically a full server compromise right here.

---
## Learnings

- works like sqli just a different backend (shell vs database)
- `;` = run sequentially, `&&` run if first command succeeds, `||` run if first fails, `&` background first command and run second command, `|` pipe, `0xa` seperates with newline
- metacharacters that are special url characters need to be encoded to work
- if even nonesensical input returns output it is a tell that the input is used as an argument for something
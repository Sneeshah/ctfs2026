# SQL injection UNION attack, determining the number of columns returned by the query

**Category:** Web Exploitation — SQL Injection  
**Difficulty:** Practitioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns`



This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. You will then use this technique in subsequent labs to construct the full attack.

To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values. 


---

## Reconnaissance

- What does the application do? 
    - A website that shows items, their prices and details. Users can search by categories and their is an account functionality
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - there is no input field but the user can input text into the url
- What happens with normal input?
    - inputting a normal word instead of the given categories prints the word on the page and shows no results

---

## Analysis

#### Technology Stack
```
Database:   Can't be sure of the underlying database
Input:      URL
Behavior:   union based sql injection
```

#### Vulnerability

- What exactly is vulnerable and why?
    

As per the lab instructions the category filter is vulnerable. 
It probably looks like this:
```sql
SELECT * FROM products WHERE category = '[input]'
```
To use an actual UNION attack we need to first find out how many columns are returned by this query. 

---

## Solution

### Step 1 - Craft payload

The title suggest to use a method to find the number of returned coolumns

First way to do it:
```sql
category=' ORDER BY 1--
```
every subsequent input the number is increased until an error is thrown.
This works if WAFs (Web Application Firewalls) block the Keyword union. ORDER BY is a legitimate input when users sort a product by price or similiar. UNION SELECT is almost never legitimate and might be blocked. ORDER BY is also a bit simpler.
Second way to do it:
```sql
category=' UNION SELECT Null
```
on every subsequent input the number of nulls is increased until the moment the number of nulls matches the returned columns. Then the database will return an additional row of null values.
I decided to use the NULL method. It confirms the column number and when successfull I can just replace NULL with actual data in the next setp.

### Step 2 - Extract / Exploit


The payload

```sql
category=' UNION SELECT Null, Null, Null
```
Works because the first query retrives 3 columns. Thus the lab is solved.
---

## Real World Impact

This showscases an easy way for an attacker to get info on the column count of a database. This might not seem like much but every bit of info is valuable for an attacker and should not be given away lightly. In this case it is vital to know for a later UNION attack

---

## Learnings

-first step of a union attack, could be pretty tedious in bigger systems and needs automation via the `Intruder` tool inside burp suite.

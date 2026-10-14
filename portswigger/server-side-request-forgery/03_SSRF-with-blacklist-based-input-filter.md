# SSRF with blacklist-based input filter
**Category:** Web Exploitation — SSRF
**Difficulty:** Practicioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter`

This lab has a stock check feature which fetches data from an internal system.
To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.
The developer has deployed two weak anti-SSRF defenses that you will need to bypass. 

---

## Reconnaissance

- What does the application do? 
    - The website is a shop. There is a stock-check feature
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - No direct user input, only in the request itself
- What happens with normal input?
    - The stock of an item at a certain location is given back

---

## Analysis


#### Vulnerability

The app takes an url from user input (stockApi) and fetches it server-side. This time there is an input filter which has to be circumvented.

---

## Solution 

### Step 1 - Recon / Looking at responses

Again the url is encoded so we also have to send encoded urls.
Using `http://localhost/admin` doesn't work and is blocked for security reasons. So a filter is in place.
Using `127.0.0.1` or `2130706433`, `017700000001` or even `127.1` is also blocked.
Cutting `admin` out and works for example `stockApi=http://127.1/?productId=3&storeId=1`

---
### Step 2 - Enumeration / Exploitation

Singel encoding the `a` in admin did not work to get around the filter.Still getting the `security reasons block`-message.
Double encoding for the `a` in admin does the trick however:
`stockApi=http://127.1/%25%36%31dmin?productId=3&storeId=1`
`stockApi=http://127.1/%25%36%31dmin/delete?username=carlos` deletes carlos

---
## Real World Impact

Abusing this vulnerability an attacker can reach internal services (admin panels, databases) and in the process steal credentials or API-Keys. 
He could also map the internal server using the server as a proxy.

---
## Learnings

- always try no encode - encoded once and encoded twice 
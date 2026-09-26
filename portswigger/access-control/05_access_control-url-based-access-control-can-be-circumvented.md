# URL-based access control can be circumvented

**Category:** Web Exploitation — Access control
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-circumvented`

This website has an unauthenticated admin panel at /admin, but a front-end system has been configured to block external access to that path. However, the back-end application is built on a framework that supports the X-Original-URL header.
To solve the lab, access the admin panel and delete the user carlos.  

---

## Reconnaissance

- What does the application do? 
    - The website is a shop with an account functionality. Users can look at the details of items on the homepage.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - User input is allowed for the login page and potentially the url
- What happens with normal input?
    - Unable to say for now, normal input for the login functionality should just login the user

---

## Analysis


#### Vulnerability

There is a mismatch between front-end and back-end here. The back-end supports `X-Original-URL` headers which allows the attacker to bypass the front-end block.
In other words: front-end and back-end make the same decision (is this action permitted) based on two different bases. Front-end looks at paths while back-end looks at headers. 

---

## Solution 

### Step 1 - Recon / Looking at responses

No login this time, no access to the admin panel on first glance, but the lab talks about the `X-Original-URL` header.
Adding this header like this `X-Original-URL: /admin` to a couple of requests showed something interesting when used with just `/` the response already shows the admin panel. Deleting an object here still runs into restricted access but that is because the new url path is: `https://0a29005c04a64028801554ba00ba0046.web-security-academy.net/admin/delete?username=carlos`
so adding only `/admin` is not enough.
---

### Step 2 - Enumeration / Step 3 - Exploit

The final step now is to add `/admin/delete` and change the request to `GET /?username=carlos HTTP/2`
And the lab is solved.

It is not possible to just use `X-Original-URL: /admin/delete/?username=carlos` because the `X-Original-URL`-header overwrites the path that is used to find the resource. So the `username`part would never be read as a parameter. That is why it has to go into the request as a parameter.

---
## Real World Impact

This vulnerability makes attackers able to reach any path that was meant to be blocked. In this case it was about the admin panel but api endpoints or really anything are at risk here.

---
## Learnings

- if front-end blocks a path, test back-end with URL-rewrite headers (X-Original-URL or X-Rewrite-URL)
- the header carries only the path, parameters belong to the request line
- access control enforced at an earlier layer is bypassable when a later layer re-derives the decision from input the earlier layer never inspected
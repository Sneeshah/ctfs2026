# Method-based access control can be circumvented

**Category:** Web Exploitation — Access control
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/access-control/lab-method-based-access-control-can-be-circumvented`

This lab implements access controls based partly on the HTTP method of requests. You can familiarize yourself with the admin panel by logging in using the credentials administrator:admin.

To solve the lab, log in using the credentials wiener:peter and exploit the flawed access controls to promote yourself to become an administrator. 

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

This lab implements a working access control, but simply does only work on the expected case. The case of getting a GET-request when there should be a POST-request is not running into the control.

---

## Solution 

### Step 1 - Recon / Looking at responses

First loggin in as an admin and upgrading carlos account. Taking a look around at what an admin can do. As `wiener` I have no such permissions.
Looking at the requests the role to change user accounts is a simple POST-request that transmits `username` and `action` (which is either upgrade or downgrade).
Simple editing the session cookie to the session of 'wiener' and setting `username` to `wiener` and `action` to `upgrade` does run into an unauthorized-error - meaning the access-control works. The lab talks about controls being based on http request methods so the next step is changing that.


---

### Step 2 - Enumeration / Step 3 - Exploit

Changing the request method to GET and moving the paramters `username` and `action` to the url (GET-requests do not have a body?) actually upgrades wieners rights to admin so lab solved.
Changing request in burp repeater is only one rightclick and choosing `Change request method`.

---
## Real World Impact

This attack has similiar consequences as the last ones. In this case an attacker needs a way to understand how an admin actually changes users rights and permissions though. But after getting their hands on that it is another recipe for disaster. The problem here is that the access control only works for POST-requests. It would be even better if it worked for POST-requests and simply denied anything else so there are no tricks with manipulated requests possible (deny by default).

---
## Learnings

- sometimes simple solutions work best. I did not think something as easy as changing a POST-request to a GET-request ever circumvents anything

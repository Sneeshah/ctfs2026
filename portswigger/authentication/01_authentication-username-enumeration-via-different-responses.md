# Username enumeration via different responses

**Category:** Web Exploitation — Authentication
**Difficulty:** Apprentice
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses`

This lab is vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

- Candidate usernames
- Candidate passwords

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.  

---

## Reconnaissance

- What does the application do? 
    - The website is a blog about several, seemingly to tech related topics. Users can read and leave comments under blog articles.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - There is an account page with a login, the comments below articles can be consideres input too.
- What happens with normal input?
    - I assume normal login actually logs you in

---

## Analysis

#### Technology Stack

 - Set-Cookie: session=...; Secure; HttpOnly; SameSite=None
 - Cookie has no dot in it -> no JWT (header.payload.signature - structure)
 - no Server/X-Powered-By, generic cookie name -> not really identifiable.

#### Vulnerability

- What exactly is vulnerable and why?
    
As per the lab instructions the username is vulnerable to enumeration and the password to brutefoce attacks.
As shown in step 1 and 2 this is true and bruteforce attacks find the correct login really quickly.

---

## Solution 

### Step 1 - Looking at responses

There is no url redirect on failed tries.
The only thing coming back on unsuccessful logins is a printed: `Invalid username`. This also shows in the http response in burp repeater. There is no difference in the response status code no matter what username is input. I guess the response changes if the inputted username is correct.

---

### Step 2 - Enumeration / Step 3 - Exploit

In this case I do not really see the point of guessing/enumerating a password when there is no real hint at it. So let's just use Burp Intruder and bruteforce it. Input the list of possible usernames proved. After the attack ran, just look ast the length of the repsponses, the correct one should differ in length.

```
username=adm&password=a
```
returns a http request that does not say `Invalid Username` but `Incorrect password`
So now we just do the same for passwords with the correct username provided.


```
username=adm&password=biteme
```
This returns a http 302 which stands for `found`
So we can login

---

## Other Notes:

- <b>Authentication</b> is the process of verifying the identity of a user or client. Websites are potentially exposed to anyone who is connected to the internet. This makes robust authentication mechanisms integral to effective web security. <b>Authorization</b> involves verifying whether a user is allowed to do something. 

Three types of authentication:
- Something you know, such as a password or the answer to a security question. These are sometimes called "knowledge factors".
- Something you have, This is a physical object such as a mobile phone or security token. These are sometimes called "possession factors".
- Something you are or do. For example, your biometrics or patterns of behavior. These are sometimes called "inherence factors". 

Most authentication vulnerabilities are either weak mechanisms or logic flaws in the coding = `broken authentication`

Brutforcing usernames is easy if the username-pattern is easy. Like `firstname.lastname@somecompany.com` or the defaults `admin` or `administrator`. These should always be changed on configuration to something less obvious.
Usernames should not be disclosed publicly in the form or user profiles or http responses.

Always use high-entropy passwords and for organizations: do not ask for regular changes or users will choose the simplest passwords available.

Servers should send the same response no matter if username or password are incorrect.

---
## Real World Impact

If a website was that poorly secured with no measures taken against bruteforced logins, they might not have a login at all. This was super easy and does not take much technical know-how. The logged in attacker could destroy the whole site after an login or, maybe even worse, change content according to their agenda and maybe bait people onto another website - which the attacker controls. Lots of possibilites - lots of danger.


---
## Learnings

- Burp Intruder can do brute force - but commandline tools are quicker (at least compared to the community edition)
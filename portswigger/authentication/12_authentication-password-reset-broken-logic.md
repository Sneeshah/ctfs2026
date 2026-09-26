# Password reset poisoning via middleware

**Category:** Web Exploitation — Authentication
**Difficulty:** Practicioner
**Progress:** Solved

---

## Description

**Lab URL:** `https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-poisoning-via-middleware`
 
This lab is vulnerable to password reset poisoning. The user carlos will carelessly click on any links in emails that he receives. To solve the lab, log in to Carlos's account. You can log in to your own account using the following credentials: wiener:peter. Any emails sent to this account can be read via the email client on the exploit server. 

---

## Reconnaissance

- What does the application do? 
    - The website is a blog about several, seemingly to tech related topics. Users can read and leave comments under blog articles.
- Where is user input accepted? (forms, URL parameters, headers, cookies)
    - There is an account page with a login, the comments below articles can be consideres input too.
- What happens with normal input?
    - Correct user logins log the user in normally, if setting the logged in checkbox it keeps the user logged in for next time

---

## Analysis


#### Vulnerability

The password reset method is vulnerable. Allowing the client side usage of `X-Forwarded-Host` creates the possibilities of password reset poisoning.

---

## Solution 

### Step 1 - Recon / Looking at responses

The same idea of tokens as in the last lab. This time the token is actually used for the reset though. But the lab instructions give the hint to use password reset poisoning and there is an exploit page in the lab as well. Password reset looks and works like it should. 
The first post request that triggers the password reset is the interesting one here. 
Just changing host to `exploit-0a1c00500337a63681864267011000f0.exploit-server.net` (notice: not the full url) does not work, since we want the website to still "create" the password reset.
`X-Forwarded-Host: exploit-0a1c00500337a63681864267011000f0.exploit-Server.net:` works and returns a 200 response.
Usually the server combines 'https://', 'host' and the 'token. By using `X-Forwarded-Host` it is possible to set the host part to our own host.
Usual reset link:
```
https://0ac000f5034fa66d81bb43f800d6007a.web-security-academy.net/forgot-password?temp-forgot-password-token=gwakey77zlf2ml7ju6mq2dn8aolwuu9r
```
Link after using `X-Forwarded-Host`:
```
https://Exploit-0a1c00500337a63681864267011000f0.exploit-Server.net/forgot-password?temp-forgot-password-token=7h115pdspfsp6c2sqcd36mfcw2k3yjh2
```

`X-Forwarded-Host` tells the server where the user came from and which host is used in the reset-link

In the access log the correct poisoned url is also shown for the password reset so it works.

---

### Step 2 - Enumeration / Step 3 - Exploit

Now the same thing but changing 'wiener' to 'carlos' (our target)
And his token is `jum1ej6d7heddbwl51mcpjmbiyljj46x`

Now we can simply take a correct password reset url: `https://0ac000f5034fa66d81bb43f800d6007a.web-security-academy.net/forgot-password?temp-forgot-password-token=w6xmreym0hovtfquvdl3ml4f9esx3oio` and change the token to the one just grabbed: 
`https://0ac000f5034fa66d81bb43f800d6007a.web-security-academy.net/forgot-password?temp-forgot-password-token=jum1ej6d7heddbwl51mcpjmbiyljj46x`
Set the new password for carlos (who is identified by the token) and login to his account.

---
## Real World Impact

By abusing this attackers can again get the passwords of any user that falls for reset and clicks on the link. This means they can potentially also log them out of their account and change everything (including emails and names). This is also not limited to one single account.

---
## Learnings

- host headers (like `Host` or `X-Forwarded-*`) are attackable.
- if cracking the secret is not possible, sometimes it is possible to get the server to tell you the secret.
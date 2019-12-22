---
layout: menu
title: "Pythagoreic Pancakes [ppc 413]"
description: "X-MAS CTF 2019 [Professional Programming & Coding] Pythagoreic Pancakes (413 pts)"
header-img: "chals/ctf/2019_XMASCTF/xmas_ctf_2019.png"
tags: [xmas, x-mas, xmas ctf, x-mas ctf, 2019, ctf, challenge, writeup, write-up, solution, programming, coding, professional programming and coding, ppc, pythagoreic pancakes, primitive pythagorean triples, pythagorean triples, triples, euclidean algorithm, coprimes, gcd]
---

# <span style="color:red">Pythagoreic Pancakes (413 pts)</span>

---

## PART 1 : CHALLENGE DESCRIPTION

```
We got a weird transmission through space time from some guy that claims he's related to Santa Claus. He says that he has a really difficult problem that he needs to solve and he needs your help. Maybe it's worth investigating.

Remote server: nc challs.xmas.htsp.ro 14004
Author: Gabies
```

---

## PART 2 : SHA-256 PARTIAL MATCHING

Connecting to the given server using __`netcat`__ gives:

```
$ nc challs.xmas.htsp.ro 14004

  Provide a hex string X such that sha256(X)[-6:] = 3b7f23

```

The server asks for a hex-encoded string where the last 6 characters when hashed using SHA-256 matches the given (e.g. __`3b7f23`__) which changes everytime a new connection is formed.

I solved it using the following block of code:

```py
from pwn import *
import hashlib

pwnable = remote("challs.xmas.htsp.ro", 14004)

request = pwnable.recvline()
log.info(request)
criterion = request[-7:-1]
log.info("FINDING PARTIAL HASH COLLISION WITH \"%s\"" % (criterion))

characters = '0123456789abcdef'
length = 16

string = characters[0] * length
char_indices =  [0 for x in string]

while char_indices.count(len(characters)-1) != len(char_indices):

    hexString = "".join([characters[x] for x in char_indices])

    sha256 = hashlib.sha256()
    sha256.update(bytes(hexString.decode("hex")))
    sha256_hex = str(sha256.hexdigest())

    if sha256_hex[-6:] == criterion:
        log.success("PARTIAL MATCH FOUND: %s" % (hexString.decode("hex")))
        log.success("SHA256 HASH: %s" % (sha256_hex))
        log.info("SENDING HEX STRING: %s" % (hexString))
        pwnable.sendline(hexString)
        break

    char_indices[-1] += 1
    for x in range(len(string)-1, 0, -1):

        if char_indices[x] == len(characters): 
            char_indices[x] = 0
            char_indices[x-1] += 1

```

This works by generating an initial string of <strong>`0`</strong>s with length 16 and from what I've noticed, the required match could be generated <strong style="color:orange">within a tolerance of 5 hex characters</strong>

The hex string is decoded into ASCII then hashed using SHA-256 then if last 6 characters of the hash matches the given, the hex string is submitted to the server.

After a successful submission, the server responds with:

```
Good, you can continue!

Hey there, Santa's distant relative here, Pythagora has a question for you!
Sit and listen, it might be an old story.
Note: the pythagorean triples are sorted increasingly by c (the hypotenuse), then by b (the long leg) then by a (the short leg).
Also you have 5 seconds / test.
```

The server gives you a challenge of finding <strong style="color:orange">primitive pythagorean triples</strong> sorted by the length of each side starting from the right with the longest side (hypotenuse)

---

## PART 3 : GETTING THE FLAG

I found a variant of [Euclid's Formula for generating pythagorean triples](https://en.wikipedia.org/wiki/Pythagorean_triple#A_variant) wherein if __`m`__ and __`n`__ are <strong style="color:orange">odd numbers</strong> and are <strong style="color:orange">coprime</strong> (their greatest common divisor is 1) and __`m > n`__, then following the formula below results in a primitive pythagorean triple:

<img alt="Euclid's Formula" src="./screenshots/euclids_formula.png" style="display:block;margin-left:auto;margin-right:auto">

Now, the next step is to find an algorithm that returns the greatest common divisor (GCD) of two numbers. 

I found [this](https://www.di-mgt.com.au/euclidean.html):

```py
def getGCD(sml_num, lrg_num): # Euclidian Algorithm

    while sml_num > 0:
        
        r = lrg_num % sml_num
        lrg_num = sml_num
        sml_num = r

    return lrg_num

```

Now that I have everything I need to generate primitive pythagorean triples, all that is left is to solve the challenges:

```py
from pwn import *
import hashlib

pwnable = remote("challs.xmas.htsp.ro", 14004)
print("====================================================================")
log.info("GENERATING PRIMITIVE PYTHAGOREAN TRIPLES")

def getGCD(sml_num, lrg_num): # Euclidian Algorithm

    while sml_num > 0:
        
        r = lrg_num % sml_num
        lrg_num = sml_num
        sml_num = r

    return lrg_num

triples = list()
for x in range(2, 5001):

    for y in range(1, x):

        if x % 2 == 1 and y % 2 == 1:
            if getGCD(y, x) == 1:
                # Euclid's formula for determining Pythagorean Triples
                a = x*y
                b = (x**2 - y**2)/2
                c = (x**2 + y**2)/2

                triple = sorted([a, b ,c])

                triples.append([x, y, triple])

triples = sorted(triples, key=lambda x: (x[2][2], x[2][1]))

log.success("%d PRIMITIVE PYTHAGOREAN TRIPLES GENERATED" % (len(triples)))
print("====================================================================")

request = pwnable.recvline()
log.info(request)
criterion = request[-7:-1]
log.info("FINDING PARTIAL HASH COLLISION WITH \"%s\"" % (criterion))

characters = '0123456789abcdef'
length = 16

string = characters[0] * length
char_indices =  [0 for x in string]

while char_indices.count(len(characters)-1) != len(char_indices):

    hexString = "".join([characters[x] for x in char_indices])

    sha256 = hashlib.sha256()
    sha256.update(bytes(hexString.decode("hex")))
    sha256_hex = str(sha256.hexdigest())

    if sha256_hex[-6:] == criterion:
        log.success("PARTIAL MATCH FOUND: %s" % (hexString.decode("hex")))
        log.success("SHA256 HASH: %s" % (sha256_hex))
        log.info("SENDING HEX STRING: %s" % (hexString))
        pwnable.sendline(hexString)
        break

    char_indices[-1] += 1
    for x in range(len(string)-1, 0, -1):

        if char_indices[x] == len(characters): 
            char_indices[x] = 0
            char_indices[x-1] += 1 

pwnable.recvline()
log.success(pwnable.recvline())
for i in range(0, 5): pwnable.recvline()
print("===================================================================")

for i in range(0, 10):
    log.info(pwnable.recvline())
    challenge = pwnable.recvline()
    log.info(challenge)

    nth_prim_triple = int(challenge.split(" ")[3].split("-")[0])
    triple = triples[nth_prim_triple - 1][2]

    log.info("%d-TH PRIMITIVE PYTHAGOREAN TRIPLE: %d, %d, %d" % (nth_prim_triple, triple[0], triple[1], triple[2]))

    pwnable.sendline("%d,%d,%d" % (triple[0], triple[1], triple[2]))
    log.success(pwnable.recvline())
    print("===================================================================")

log.info(pwnable.recvline())
log.success(pwnable.recvline())
print("===================================================================")
```

The code above precomputes all possible primitive pythagorean triples from coprimes found from the first 5000 positive integers then sorts them by length of the hypotenuse then length of the longest leg. All precomputed values are saved in memory and are retrieved by index when the challenge comes.

Running the code:

```console
[+] Opening connection to challs.xmas.htsp.ro on port 14004: Done
====================================================================
[*] GENERATING PRIMITIVE PYTHAGOREAN TRIPLES
[+] 2533381 PRIMITIVE PYTHAGOREAN TRIPLES GENERATED
====================================================================
[*] Provide a hex string X such that sha256(X)[-6:] = 536a79
[*] FINDING PARTIAL HASH COLLISION WITH "536a79"
[+] PARTIAL MATCH FOUND: \x00\x00\x00\x00\x005\x80\x96
[+] SHA256 HASH: 3aa22a42ecb2d489b7473fdaba23200a5d8eaf36012d35213972e6eecc536a79
[*] SENDING HEX STRING: 0000000000358096
[+] Good, you can continue!
===================================================================
[*] Here's the challange #1:
[*] Give me the 8455-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 8455-TH PRIMITIVE PYTHAGOREAN TRIPLE: 5980, 52731, 53069
[+] Well done, here, have another.
===================================================================
[*] Here's the challange #2:
[*] Give me the 1477-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 1477-TH PRIMITIVE PYTHAGOREAN TRIPLE: 3040, 8769, 9281
[+] Well done, here, have another.
===================================================================
[*] Here's the challange #3:
[*] Give me the 10155-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 10155-TH PRIMITIVE PYTHAGOREAN TRIPLE: 14555, 62172, 63853
[+] Well done, here, have another.
===================================================================
[*] Here's the challange #4:
[*] Give me the 5379-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 5379-TH PRIMITIVE PYTHAGOREAN TRIPLE: 10023, 32264, 33785
[+] Well done, here, have another.
===================================================================
[*] Here's the challange #5:
[*] Give me the 7662-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 7662-TH PRIMITIVE PYTHAGOREAN TRIPLE: 25320, 40921, 48121
[+] Well done, here, have another.
===================================================================
[*] Here's the challange #6:
[*] Give me the 15703-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 15703-TH PRIMITIVE PYTHAGOREAN TRIPLE: 48032, 86175, 98657
[+] Well done, here, have another.
===================================================================
[*] Here's the challange #7:
[*] Give me the 45559-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 45559-TH PRIMITIVE PYTHAGOREAN TRIPLE: 184149, 219220, 286301
[+] Well done, here, have another.
===================================================================
[*] Here's the challange #8:
[*] Give me the 137044-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 137044-TH PRIMITIVE PYTHAGOREAN TRIPLE: 400044, 762517, 861085
[+] Well done, here, have another.
===================================================================
[*] Here's the challange #9:
[*] Give me the 397207-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 397207-TH PRIMITIVE PYTHAGOREAN TRIPLE: 936411, 2313460, 2495789
[+] Well done, here, have another.
===================================================================
[*] Here's the challange #10:
[*] Give me the 1182921-th primitive pythagorean triple in the following format: a,b,c with a < b < c.
[*] 1182921-TH PRIMITIVE PYTHAGOREAN TRIPLE: 535567, 7413144, 7432465
[+] Well done, here, have another.
===================================================================
[*] Good one mate, Pythagora would be proud!
[+] Here's your flag: X-MAS{Th3_Tr33_0f_pr1m1t1v3_Pyth4g0r34n_tr1ple5}
===================================================================
[*] Closed connection to challs.xmas.htsp.ro port 14004
```

---

<div style="width:100%;overflow-x:auto"><h2>FLAG : <strong>X-MAS{Th3_Tr33_0f_pr1m1t1v3_Pyth4g0r34n_tr1ple5}</strong></h2></div>

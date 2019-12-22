---
layout: menu
title: "Santa's crackme [rev 25]"
description: "X-MAS CTF 2019 [Reverse Engineering] Santa's crackme (25 pts)"
header-img: "chals/ctf/2019_XMASCTF/xmas_ctf_2019.png"
tags: [xmas, x-mas, xmas ctf, x-mas ctf, 2019, ctf, challenge, writeup, write-up, solution, reversing, reverse engineering, santas crackme, ltrace, strcmp]
---

# <span style="color:red">Pythagoreic Pancakes (413 pts)</span>

---

## PART 1 : CHALLENGE DESCRIPTION

```
I bet you can't crack this!

Files: download
Author: littlewho
```

--- 

## PART 2 : GIVEN FILES

[>] [main](./files/main)

---

## PART 3 : GETTING THE FLAG

```console
$ file main

  main: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=5a1d1f7ac1d7a5998eec19ad57aa061fc81f1e4d, not stripped

```

The given executable is a 64-bit ELF file and running it on __`ltrace`__ shows:

```console
$ python -c 'print "A"*50' | ltrace ./main

  printf("Enter your license key: ")                            = 24
  __isoc99_scanf(0x402029, 0x7ffdeca5b8b0, 0, 0)                = 1
  strcmp("B", "[")                                              = -25
  strcmp("B", ".")                                              = 20
  strcmp("B", "N")                                              = -12
  strcmp("B", "B")                                              = 0
  strcmp("B", "P")                                              = -14
  strcmp("B", "x")                                              = -54
  strcmp("B", "6")                                              = 12
  strcmp("B", "7")                                              = 11
  strcmp("B", "m")                                              = -43
  strcmp("B", "4")                                              = 14	
  strcmp("B", "7")                                              = 11
  strcmp("B", "\\")                                             = -26
  strcmp("B", "2")                                              = 16
  strcmp("B", "6")                                              = 12
  strcmp("B", "\\")                                             = -26
  strcmp("B", "a")                                              = -31
  strcmp("B", "7")                                              = 11
  strcmp("B", "g")                                              = -37
  strcmp("B", "\\")                                             = -26
  strcmp("B", "7")                                              = 11
  strcmp("B", "4")                                              = 14
  strcmp("B", "\\")                                             = -26
  strcmp("B", "o")                                              = -45
  strcmp("B", "2")                                              = 16
  strcmp("B", "`")                                              = -30
  strcmp("B", "0")                                              = 18
  strcmp("B", "m")                                              = -43
  strcmp("B", "6")                                              = 12
  strcmp("B", "0")                                              = 18
  strcmp("B", "\\")                                             = -26
  strcmp("B", "`")                                              = -30
  strcmp("B", "k")                                              = -41
  strcmp("B", "0")                                              = 18
  strcmp("B", "`")                                              = -30
  strcmp("B", "h")                                              = -38
  strcmp("B", "2")                                              = 16
  strcmp("B", "m")                                              = -43
  strcmp("B", "5")                                              = 13
  strcmp("B", "~")                                              = -60
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  strcmp("B", "")                                               = 66
  puts("License key is incorrect"License key is incorrect
  )                              = 25
  +++ exited (status 0) +++

```
 
The program shifted the input characters (__`A`__ -> __`B`__) and are passed to a __`strcmp()`__ function individually with a corresponding character relative to the license key.

The integer values on the right are the difference between the decimal values of the shifted input character and the character it was compared to.

The license key seems to only have 39 characters and pooling all the characters compared to the inputthen passing it to __`ltrace`__ in order to know by how much each character shifts gives:

```console
$ echo -e '[.NBPx67m47\\26\\a7g\\74\\o2`0m60\\`k0`h2m5~' | ltrace ./main

  printf("Enter your license key: ")                            = 24
  __isoc99_scanf(0x402029, 0x7ffc868dca50, 0, 0)                = 1
  strcmp("X", "[")                                              = -3
  strcmp("-", ".")                                              = -1
  strcmp("M", "N")                                              = -1
  strcmp("A", "B")                                              = -1
  strcmp("S", "P")                                              = 3
  strcmp("{", "x")                                              = 3
  strcmp("5", "6")                                              = -1
  strcmp("4", "7")                                              = -3
  strcmp("n", "m")                                              = 1
  strcmp("7", "4")                                              = 3
  strcmp("4", "7")                                              = -3
  strcmp("_", "\\")                                             = 3
  strcmp("1", "2")                                              = -1
  strcmp("5", "6")                                              = -1
  strcmp("_", "\\")                                             = 3
  strcmp("b", "a")                                              = 1
  strcmp("4", "7")                                              = -3
  strcmp("d", "g")                                              = -3
  strcmp("_", "\\")                                             = 3
  strcmp("4", "7")                                              = -3
  strcmp("7", "4")                                              = 3
  strcmp("_", "\\")                                             = 3
  strcmp("l", "o")                                              = -3
  strcmp("1", "2")                                              = -1
  strcmp("c", "`")                                              = 3
  strcmp("3", "0")                                              = 3
  strcmp("n", "m")                                              = 1
  strcmp("5", "6")                                              = -1
  strcmp("3", "0")                                              = 3
  strcmp("_", "\\")                                             = 3
  strcmp("c", "`")                                              = 3
  strcmp("h", "k")                                              = -3
  strcmp("3", "0")                                              = 3
  strcmp("c", "`")                                              = 3
  strcmp("k", "h")                                              = 3
  strcmp("1", "2")                                              = -1
  strcmp("n", "m")                                              = 1
  strcmp("6", "5")                                              = 1
  strcmp("}", "~")                                              = -1
  puts("License key is incorrect"Enter your license key: License key is incorrect
  )                              = 25
  +++ exited (status 0) +++

```

The characters seems to have been shifted to show the flag. Pooling all the differences on the right:

```py
>>> string = "[.NBPx67m47\\26\\a7g\\74\\o2`0m60\\`k0`h2m5~"
>>> diff = [-3, -1, -1, -1, 3, 3, -1, -3, 1, 3, -3, 3, -1, -1, 3, 1, -3, -3, 3, -3, 3, 3, -3, -1, 3, 3, 1, -1, 3, 3, 3, -3, 3, 3, 3, -1, 1, 1, -1]
>>> "".join([chr(ord(string[x]) + diff[x]) for x in range(0, len(string))])
'X-MAS{54n74_15_b4d_47_l1c3n53_ch3ck1n6}'
```

```console
$ echo "X-MAS{54n74_15_b4d_47_l1c3n53_ch3ck1n6}" | ./main

  Enter your license key: License key is correct

```

---

<div style="width:100%;overflow-x:auto"><h2>FLAG : <strong>X-MAS{54n74_15_b4d_47_l1c3n53_ch3ck1n6}</strong></h2></div>

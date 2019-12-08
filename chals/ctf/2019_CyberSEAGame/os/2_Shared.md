---
layout: menu
description: "Cyber SEA Game 2019 [OS] Shared (110 pts)"
header-img: "chals/ctf/2019_CyberSEAGame/cyber_sea_game_2019.png"
tags: [cyber sea game, cyber sea games, cyberseagame, cyberseagames, 2019, ctf, challenge, writeup, write-up, solution, os, linux, shared object, so, so file, shared objects, dynamically linked binary, dynamic link, ld_library_path]
---

# <span style="color:red">Shared (110 pts)</span>

---

## PART 1 : CHALLENGE DESCRIPTION

```
You are asked to investigate a case where the execution of an exe file on Linux fails. Download the attached document and find a flag.

flag format: Flag{single-byte alphanumeric characters/symbols}
```

---

## PART 2 : GIVEN FILES

[>] [Shared_04dca129c011213979aded2e7bef71d3.zip](./files/Shared_04dca129c011213979aded2e7bef71d3.zip)
- libflag.so
- main.exe

---

## PART 3 : GETTING THE FLAG

```console
$ file main.exe

  main.exe: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.18, BuildID[sha1]=572e5a45a57b8e8de469cfe301e7d653fb4a6565, not stripped

```

The binary included in the zip archive is an ELF file and running the binary in a Linux terminal outputs:

```console
$ chmod +x ./main.exe

$ ./main.exe

  ./main.exe: error while loading shared libraries: libflag.so: cannot open shared object file: No such file or directory

$ ldd ./main.exe

  	linux-vdso.so.1 (0x00007ffc60b4c000)
  	libflag.so => not found
  	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ff7683e1000)
      	/lib64/ld-linux-x86-64.so.2 (0x00007ff7685be000)

```

Running __`./main.exe`__ regularly and through __`ldd`__ returns that __`libflag.so`__ could not be found.

Export the current working directory or where the __`libflag.so`__ file is saved to the environment variable, __`LD_LIBRARY_PATH`__, to force load the shared object file to the binary.

```console
$ export LD_LIBRARY_PATH=$(pwd)

$ ./main.exe

  flag{specify_the_library}

```

---

## FLAG : __flag{specify_the_library}__ 

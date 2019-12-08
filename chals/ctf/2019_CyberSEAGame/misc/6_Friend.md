---
layout: menu
title: "Friend [msc 100]"
description: "Cyber SEA Game 2019 [Misc] Friend (100 pts)"
header-img: "chals/ctf/2019_CyberSEAGame/cyber_sea_game_2019.png"
tags: [cyber sea game, cyber sea games, cyberseagame, cyberseagames, 2019, ctf, challenge, writeup, write-up, solution, misc, miscellaneous, friend, md5, sha1, hash, hash collision]
---

# <span style="color:red">Friend (100 pts)</span>

---

## PART 1 : CHALLENGE DESCRIPTION

```
Among File001 to File999, find files with the same features with File.
Identify the files and also provide evidence for the commonality.

flag format: flag{File<4 digits>_lowercase alphanumeric}
```

---

## PART 2 : GIVEN FILES

[>] [Friend_0ad3d2abf5ededb11275ce89417f314e.zip](./files/Friend_0ad3d2abf5ededb11275ce89417f314e.zip)
- File
- Files/File0001 - Files/File0999
- memo.txt

---

## PART 3 : EXAMINING THE FILES

The goal is to find a file with similar "features" with the file, __`File`__.

First we inspect the contents of __`memo.txt`__:

```console
$ cat memo.txt

  File    	b9fef2a8fc93b05e7701e97196fda6c4fbeea25ff8e64fdfee7015eca8fa617d
  File0001	5097d0556fde49fda625b2cba261e1bee99c66c073a3398844de3360c5f835c3
  File0002	fd2c2fba409f10b32f4827f745efae50d1e5254f6f024ad964952eac3b2a332b
  File0003	369db1c424b954d97c1203905f53d11ce0f2b6942d4b0bf059fdceebfa96d73b
  File0004	15536fd2969cebf4577cc116da195f905c8f88e5768683d623795b5c09ff5f8b
  File0005	858ac7f973834a3e426efa3f00d48a3fc38ec0ff4e44249ed610f3c6e56e537c
  ...
  File0995	fa1306d21761346491e6c21b21e655518078e01906ca704360783c2b0aa072e3
  File0996	daa5f5024a2e8953272b49273b17a843ee96c0f940ecba2eed76401f8d794fa9
  File0997	c0e178abd3ea6bcdc074c0ad3490cb5d363de62d00fc22d331eb3d80835cec31
  File0998	f41720d08c00bd15de6dbc13907ab36bc40d6b15080f7b1592c4e312a4f46db1
  File0999	e85f5d89e52aef154930d337a1b655c44d81c896ddfeebcae09cd02a83a07586

```

It contains __SHA1__ hashes of all the files included in the zip file. Now to see what "features" __`File__ has...

```console
$ cat File

  Ƙ!�������e�o�*p

$ cat File | xxd -p

  d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb
  7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd72
  80373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd0239
  6306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a88393
  96f965ab6ff72a70

```

The similar file should contain a similar hexdump to __`File`__

---

## PART 4 : GETTING THE FLAG

Finding a "similar" file:

```console
$ cat Files/* | xxd -p | grep --color d131 | wc -l

  7

$ cat Files/* | xxd -p | grep --color d131dd | wc -l

  2

$ cat Files/* | xxd -p | grep --color d131dd

  d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb
  916e0fd3d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004

$ while IFS= read -r line; do
>   file=$(echo $line | cut -d" " -f1)
>   match=$(cat "Files/${file}" | xxd -p | tr -d '\n' | egrep --color d131dd02)
>   if [ ! -z $match ]; then
>     echo $file
>   fi
> done < memo.txt

  File0623

$ cat Files/File0623 | xxd -p

  d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb
  7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf2
  80373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd0239
  6306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a88393
  96f9652b6ff72a70

$ cat memo.txt | egrep -e "File( |0623)"

  File    	b9fef2a8fc93b05e7701e97196fda6c4fbeea25ff8e64fdfee7015eca8fa617d
  File0623	8d12236e5c4ed9f4e790db4d868fd5c399df267e18ff65c1107c328228cffc98

```

__`File0623`__ is the closest match to __`File`__ with a few subtle differences.

They both have different SHA1 hashes as well... but what if they were hashed differently.

```console
$ cat File | md5sum

  79054025255fb1a26e4bc422aef54eb4  -

$ cat Files/File0623 | md5sum

  79054025255fb1a26e4bc422aef54eb4  -

```

The contents of __`File`__ and __`File0623`__ has a hash collision over __MD5__. The hash might be the required evidence for the challenge.

---

## FLAG : __flag{File0623_79054025255fb1a26e4bc422aef54eb4}__

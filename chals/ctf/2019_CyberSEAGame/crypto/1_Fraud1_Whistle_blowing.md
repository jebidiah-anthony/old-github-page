---
layout: menu
title: "Fraud(1) [cry 50]"
description: "Cyber SEA Game 2019 [Cryptography] Fraud(1) Whistle blowing (50 pts)"
header-img: "chals/ctf/2019_CyberSEAGame/cyber_sea_game_2019.png"
tags: [cyber sea game, cyber sea games, cyberseagame, cyberseagames, 2019, ctf, challenge, writeup, write-up, solution, cryptography, crypto, full-width encoding, fullwidth encoding, unicode, codepoint]
---

# <span style="color:red">Fraud(1) Whistle Blowing (50 pts)</span>

---

## PART 1 : CHALLENGE DESCRIPTION

```
Mr. Horii is in charge of investigation of a case of embezzlement that occurred in the company.
While he has not been able to find any clue, he received an email from an unknown sender.

/EF/BC/B6/EF/BC/A7/EF/BD/87/EF/BD/9A/EF/BC/B8/EF/BC/90/EF/BC/B6/EF/BD/94/EF/BC/B9/EF/BD/8A/EF/BC/AE/EF/BC/96/EF/BD/85/EF/BD/8D/EF/BD/97/EF/BD/9A/EF/BD/83/EF/BD/8C/EF/BC/98/EF/BD/98/EF/BC/AE/EF/BC/B6/EF/BC/99/EF/BC/A7/EF/BD/84/EF/BC/B7/EF/BC/91/EF/BD/90/EF/BC/BA/EF/BC/B1/EF/BC/9D/EF/BC/9D

The email appears to contain important information about the incident, but the essential parts are replaced by meaningless strings. Mr. Horii has no idea about what to do.
Find information hidden in this email for Mr. Horii.

flag format: flag{[A-Za-z0-9 symbols]}
```

---

## PART 2 : GETTING THE FLAG

Unicode characters with codepoints from __`U+FF00`__ to __`U+FF60`__ are Full-width characters and their literal __UTF-8__ equivalents are __`\xEF\xBC\x80`__ to __`\xEF\xBC\xBF`__ and __`\xEF\xBD\x80`__ to __`\xEF\xBD\xA0`__

```console
$ c="/EF/BC/B6/EF/BC/A7/EF/BD/87/EF/BD/9A/EF/BC/B8/EF/BC/90/EF/BC/B6/EF/BD/94/EF/BC/B9/EF/BD/8A/EF/BC/AE/EF/BC/96/EF/BD/85/EF/BD/8D/EF/BD/97/EF/BD/9A/EF/BD/83/EF/BD/8C/EF/BC/98/EF/BD/98/EF/BC/AE/EF/BC/B6/EF/BC/99/EF/BC/A7/EF/BD/84/EF/BC/B7/EF/BC/91/EF/BD/90/EF/BC/BA/EF/BC/B1/EF/BC/9D/EF/BC/9D"

$ c=$(echo $c | sed -e "s/\//\\\x/g")

$ echo -e $c

  ＶＧｇｚＸ０ＶｔＹｊＮ６ｅｍｗｚｃｌ８ｘＮＶ９ＧｄＷ１ｐＺＱ＝＝
```

Convert the full-width encoding to ASCII

```console
$ echo -e $c | uni2ascii -B -q

  VGgzX0VtYjN6emwzcl8xNV9GdW1paQ==

$ echo "VGgzX0VtYjN6emwzcl8xNV9GdW1pZQ==" | base64 -d

  Th3_Emb3zzl3r_15_Fumie  
```

---

## FLAG : __flag{Th3_Emb3zzl3r_15_Fumie}__

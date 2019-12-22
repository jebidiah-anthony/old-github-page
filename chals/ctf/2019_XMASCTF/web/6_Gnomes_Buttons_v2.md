---
layout: menu
title: "Gnome's Buttons v2 [web 152]"
description: "X-MAS CTF 2019 [Web] Gnome's Buttons v2 (152 pts)"
header-img: "chals/ctf/2019_XMASCTF/xmas_ctf_2019.png"
tags: [xmas, x-mas, xmas ctf, x-mas ctf, 2019, ctf, challenge, writeup, write-up, solution, web, web exploitation, gnomes buttons, gnomes buttons v2, fuzzing, GET parameter, HTTP GET, GET]
---

# <span style="color:red">Gnome's Buttons v2 (152 pts)</span>

---

## PART 1 : CHALLENGE DESCRIPTION

```
WARNING: GUESSING
HOROVIEO CHUM! ME donut like cukies anymor! Git me some gud TAITAL!
kisses from @trupples

Remote server: http://challs.xmas.htsp.ro:11007
Author: bobi
```

---

## PART 2 : GETTING THE FLAG

The given link leads you to __`http://challs.xmas.htsp.ro:11007/?a=b`__:

![Landing Page](./screenshots/5_Gnome's_Buttons_v2.png)

The site seems to accept GET parameters such as __`?a=b`__ but what the challenge is asking for is a <strong>gud TAITAL</strong> (title). Now, adding a __`title`__ parameter with a value __`flag`__:

### `http://challs.xmas.htsp.ro:11007/?title=flag`

![Almost Flag](./screenshots/5_Gnome's_Buttons_v2_almost.png)

The challenge description warned that guessing may be required. Now, setting the __`title`__ to __`fl4g`__:

### `http://challs.xmas.htsp.ro:11007/?title=fl4g`

![Flag](./screenshots/5_Gnome's_Buttons_v2_flag.png)

---

<div style="width:100%;overflow-x:auto"><h2>FLAG : <strong>X-MAS{Gu3sS1ng_f0r_beGg1nN&rs}</strong></h2></div>

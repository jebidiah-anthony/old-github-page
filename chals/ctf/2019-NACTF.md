---
layout: menu
title: "NACTF 2019"
description: "NACTF 2019 Cryptography challenge write-ups"
tags: [ctf, capture the flag, challenges, challenge write ups, write-ups, writeups, write-up, writeup, nactf, solutions, 2019]
challenges: [[Dr. J's Group Test Randomizer:<br/>Board Problem &num;0, crypto/3_Group_Test_Randomizer_0.html, Crypto (100), Middle Square], [Reversible Sneaky Algorithm &num;0, crypto/4_Reversible_Sneaky_Algorithm_0.html, Crypto (125), RSA], [Super Duper AES, crypto/5_Super_Duper_AES.html, Crypto (250), Subtitution-Permutation], [Reversible Sneaky Algorithm &num;1, crypto/6_Reversible_Sneaky_Algorithm_1.html, Crypto (275), RSA], [Dr. J's Group Test Randomizer:<br/>Board Problem &num;1, crypto/7_Group_Test_Randomizer_1.html, Crypto (300), Middle Square], [Reversible Sneaky Algorithm &num;2, crypto/8_Reversible_Sneaky_Algorithm_2.html, Crypto (350), RSA]]
---

## <span style="color:red">$ [NACTF 2019](https://www.nactf.com/)</span>

---

### DURATION
<div style="margin-left:10px">[<span>Wed, 18 Sep 2019, 06:00 PHT</span> - <span>Mon, 23 Sep 2019, 06:00 PHT</span>]</div>

---

### CHALLENGES

<div style="overflow-x:auto">
 <table>
   <tr>
     <td><strong style="text-decoration:underline">NAME</strong></td>
     <td><strong style="text-decoration:underline">CATEGORY/PTS</strong></td>
     <td><strong style="text-decoration:underline">TAGS</strong></td>
   </tr>
   {% for chal in page.challenges %}
   <tr>
     <td><a href="./2019_NACTF/{{ chal[1] }}">{{ chal[0] }}</a></td>
     <td>{{ chal[2] }}</td>
     <td>{{ chal[3] }}</td>
   </tr>
   {% endfor %}
 </table>
</div>

---
layout: menu
title: "TG:Hack 2019"
description: "TG:Hack 2019 Web exploit challenge write-ups"
header-img: "chals/ctf/2019_CyberSEAGame/cyber_sea_game_2019.png"
tags: [ctf, capture-the-flag, challenges, challenge-write-ups, write-ups, writeups, write-up, writeup, tghack, "tg:hack", solutions, 2019]
challenges: [[Fortune Cookie, web/1_Fortune_cookie.html, Web (50), HTTP Cookies], [Imagicur, web/2_Imagicur.html, Web (150), Arbitrary File Upload], [Wandshop, web/3_Wandshop.html, Web (100), Form Input Value], [itsmagic, web/4_itsmagic.html, Web (100), Directory Fuzzing], [Wizardschat, web/5_Wizardschat.html, Web (300), Server-side Template Injection]]
---

## <span style="color:red">$ [TG:Hack 2019](https://tghack.no/)</span>

---

### DURATION
<div style="margin-left:10px">[<span>Thu, 18 Apr 2019, 00:00 PHT</span> - <span>Sun, 21 Apr 2019, 00:00 PHT</span>]</div>

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
     <td><a href="./2019_TGHack/{{ chal[1] }}">{{ chal[0] }}</a></td>
     <td>{{ chal[2] }}</td>
     <td>{{ chal[3] }}</td>
   </tr>
   {% endfor %}
 </table>
</div>

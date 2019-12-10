---
layout: menu
title: "TJCTF 2019"
description: "TJCTF 2019 Web exploit challenge write-up"
tags: [ctf, capture the flag, challenges, challenge write ups, write-ups, writeups, write-up, writeup, tjctf, solutions, 2019]
challenges: [[Moar Horse 2, web/2_moar_horse_2.html, Web (70), "Scripting, Recursive Search"]]
---

## <span style="color:red">$ [TJCTF 2019](https://tjctf.org/)</span>

---

### DURATION
<div style="margin-left:10px">[<span>Sat, 06 Apr 2019, 07:00 PHT</span> - <span>Wed, 10 Apr 2019, 07:00 PHT</span>]</div>

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
     <td><a href="./2019_TJCTF/{{ chal[1] }}">{{ chal[0] }}</a></td>
     <td>{{ chal[2] }}</td>
     <td>{{ chal[3] }}</td>
   </tr>
   {% endfor %}
 </table>
</div>

---
layout: menu
title: "X-MAS CTF 2019"
description: "A few challenge solutions/write-ups for X-MAS CTF 2019"
header-img: "chals/ctf/2019_XMASCTF/xmas_ctf_2019.png"
tags: [ctf, capture-the-flag, challenges, challenge-write-ups, write-ups, writeups, write-up, writeup, xmas, x-mas, xmas ctf, x-mas ctf, solutions, 2019]
challenges: [
        [Back to 2007, for/5_Back_to_2007.html, Forensics (499), "Rotated Bits, UDP Stream"],
	[Orakel, ppc/1_Orakel.html, PPC (152), Word Search],
        [Pythagoreic Pancakes, ppc/2_Pythagoreic_Pancakes.html, PPC (413), Primitive Pythagorean Triples],
        [Santa's crackme, rev/1_Santa's_crackme.html, Reversing (25), "strcmp"],
	[Rigged Election, web/3_Rigged_Election.html, Web (50), Scripting],
	[Gnome's Buttons v2, web/6_Gnomes_Buttons_v2.html, Web (152), GET Parameter]
]
---

## <span style="color:red">$ X-MAS CTF 2019</span>

---

### DURATION
<div style="margin-left:10px">[<span>Sat, 14 Dec 2019, 03:00 PHT</span> - <span>Sat, 21 Dec 2019, 03:00 PHT</span>]</div>

---

### CHALLENGES WRITE-UPS

<div style="overflow-x:auto">
 <table>
   <tr>
     <td><strong style="text-decoration:underline">NAME</strong></td>
     <td><strong style="text-decoration:underline">CATEGORY/PTS</strong></td>
     <td><strong style="text-decoration:underline">TAGS</strong></td>
   </tr>
   {% for chal in page.challenges %}
   <tr>
     <td><a href="./2019_XMASCTF/{{ chal[1] }}">{{ chal[0] }}</a></td>
     <td>{{ chal[2] }}</td>
     <td>{{ chal[3] }}</td>
   </tr>
   {% endfor %}
 </table>
</div>


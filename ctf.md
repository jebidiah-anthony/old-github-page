---
layout: menu
title: "CTF WRITE-UPS"
description: "Solution to CTF Challenges I've encountered."
tags: [ctf, capture-the-flag, challenges, challenge-write-ups, write-ups, writeups, write-up, writeup, nactf, cyberseagame, cyberseagames, cyber-sea-game, cyber-sea-games, tghack, "tg:hack", tjctf, hackthebox, htb, solutions, 2019]
---

# <span style="color:red">$ ctf write-ups</span>

---

<div style="overflow-x:auto">
 <table>
   {% for ctf in site.ctf_menu %}
   <tr>
     <td><a href="{{ site.url }}/chals/ctf/{{ ctf[1] }}-{{ ctf[0] }}.html">{{ ctf[2] }} {{ ctf[1] }}</a></td>
     <td>{{ ctf[3] }} - {{ ctf[4] }}</td>
   </tr>
   {% endfor %}
   <tr>
     <td><a href="./chals/htb/challenges.html">HTB Retired Challenges</a></td>
     <td>(
       {% for cat in site.htb_chls %}
       <span style="padding:0 5px">
         <a href="./chals/htb/challenges.html#{{ cat[0] }}">{{ cat[1] }}</a>
       </span>
       {% endfor %}
     )</td>
   </tr>
 </table>
</div>

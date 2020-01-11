---
layout: menu
title: "HTB CHALLENGES"
description: "Retired HackTheBox challenge write-ups"
header-img: htb.png
tags: [ctf, capture the flag, challenges, challenge write ups, write-ups, writeups, write-up, writeup, htb, hackthebox, solutions]
challenges_for: [
  [Keep Tryin', Keep_Tryin.html, 50 pts, Medium, orange, "Apr 25, 2018", "Oct 27, 2019"],  
  [Marshal in the Middle, "Marshal_in_the_Middle.html", 40 pts, Medium, orange, "Sep 01, 2017", "Jan 10, 2020"],
  [Deadly Arthropod, "", 40 pts, Medium, orange, "Oct 26, 2017", "Active"],
  [Reminiscent, "", 40 pts, Medium, orange, "Oct 26, 2017", "Active"], 
  [Blue Shadow, "", 60 pts, Medium, orange, "May 28, 2018", "Active"], 
  [MarketDump, "", 30 pts, Medium, orange, "May 16, 2019", "Active"], 
  [Took the Byte, "", 20 pts, Easy, green, "Jun 30, 2019", "Active"]
]
challenges_mob: [
  [Cryptohorrific, "", 40 pts, Medium, orange, "Jun 20, 2018", "Active"]
]
challenges_pwn: [
  [Ropme, "", 80 pts, Hard, red, "Jul 08, 2017", "Active"],  
  [Little Tommy, "", 40 pts, Medium, orange, "Sep 26, 2017", "Active"],  
  [Old Bridge, "", 80 pts, Hard, red, "Apr 25, 2018", "Active"],  
  [ropmev2, "", 40 pts, Hard, red, "Jul 10, 2019", "Active"]
]
challenges_web: [
  [HDC, HDC.html, 30 pts, Easy, green, "Jul 10, 2017", "Jul 31, 2019"],
  [I know Mag1k, "", 50 pts, Medium, orange, "Jul 12, 2017", "Active"],
  [Grammar, "", 70 pts, Hard, red, "Jul 22, 2017", "Active"],  
  [Lernaean, "", 20 pts, Easy, green, "Jul 26, 2017", "Active"],  
  [Cartographer, "", 30 pts, Easy, green, "Aug 31, 2017", "Active"],  
  [Emdee five for life, "", 20 pts, Easy, green, "May 21, 2019", "Active"],  
  [Fuzzy, "", 20 pts, Easy, green, "Jul 05, 2019", "Active"],  
  [FreeLancer, "", 30 pts, Medium, orange, "Jul 31, 2019", "Active"]
]
---

## <span id="for" style="color:red">$ htb retired challenges</span>

---

<div style="overflow-x:auto">
 <table>
   <tr>
     <td><strong style="text-decoration:underline">CHALLENGE NAME</strong></td>
     <td><strong style="text-decoration:underline">CATEGORY</strong></td>
     <td><strong style="text-decoration:underline">POINTS</strong></td>
     <td><strong style="text-decoration:underline">DIFFICULTY</strong></td>
     <td><strong style="text-decoration:underline">RELEASED</strong></td>
     <td><strong style="text-decoration:underline">RETIRED</strong></td>
   </tr>
   {% for chal in page.challenges_for %}
   <tr>
     <td>
       {% if chal[6] == "Active" %}
         {{ chal[0] }}
       {% else %}
         <a href="./for/{{ chal[1] }}">{{ chal[0] }}</a>
       {% endif %}
     </td>
     <td><span>Forensics</span></td>
     <td><span style="color:{{ chal[4] }}">{{ chal[2] }}</span></td>
     <td><span style="color:{{ chal[4] }}">{{ chal[3] }}</span></td>
     <td>{{ chal[5] }}</td>
     <td>{{ chal[6] }}</td>
   </tr>
   {% endfor %}
   <tr><td colspan="6" id="mob"></td></tr>
   <tr><td colspan="6" style="border-top:1px dashed #eaeaea"></td></tr>
   {% for chal in page.challenges_mob %}
   <tr>
     <td>
       {% if chal[6] == "Active" %}
         {{ chal[0] }}
       {% else %}
         <a href="./mob/{{ chal[1] }}">{{ chal[0] }}</a>
       {% endif %}
     </td>
     <td><span>Mobile</span></td>
     <td><span style="color:{{ chal[4] }}">{{ chal[2] }}</span></td>
     <td><span style="color:{{ chal[4] }}">{{ chal[3] }}</span></td>
     <td>{{ chal[5] }}</td>
     <td>{{ chal[6] }}</td>
   </tr>
   {% endfor %}
   <tr><td colspan="6" id="pwn"></td></tr>
   <tr><td colspan="6" style="border-top:1px dashed #eaeaea"></td></tr>
   {% for chal in page.challenges_pwn %}
   <tr>
     <td>
       {% if chal[6] == "Active" %}
         {{ chal[0] }}
       {% else %}
         <a href="./pwn/{{ chal[1] }}">{{ chal[0] }}</a>
       {% endif %}
     </td>
     <td><span>Pwn</span></td>
     <td><span style="color:{{ chal[4] }}">{{ chal[2] }}</span></td>
     <td><span style="color:{{ chal[4] }}">{{ chal[3] }}</span></td>
     <td>{{ chal[5] }}</td>
     <td>{{ chal[6] }}</td>
   </tr>
   {% endfor %}
   <tr><td colspan="6" id="web"></td></tr>
   <tr><td colspan="6" style="border-top:1px dashed #eaeaea"></td></tr>
   {% for chal in page.challenges_web %}
   <tr>
     <td>
       {% if chal[6] == "Active" %}
         {{ chal[0] }}
       {% else %}
         <a href="./web/{{ chal[1] }}">{{ chal[0] }}</a>
       {% endif %}
     </td>
     <td><span>Web</span></td>
     <td><span style="color:{{ chal[4] }}">{{ chal[2] }}</span></td>
     <td><span style="color:{{ chal[4] }}">{{ chal[3] }}</span></td>
     <td>{{ chal[5] }}</td>
     <td>{{ chal[6] }}</td>
   </tr>
   {% endfor %}
 </table>
</div>

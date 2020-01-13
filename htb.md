---
title: "HTB WRITE-UPS"
layout: menu
description: "Retired HackTheBox Machine Write-ups"
header-img: "chals/htb/htb.png"
tags: [HackTheBox, htb, boot2root, solutions, solution, writeup, write-up, machines, machine, linux, windows, openbsd, stratosphere, poison, canape, sunday, devoops, tartarsauce, jerry, hawk, active, waldo, mischief, teacher, irked, lightweight, chaos, help, flujab, friendzone, ctf, luke, kryptos, swagshop, writeup, ellingson, safe, jebidiah-anthony, jebidiah, pentest, pentesting, penetration testing]
boxes: [
    [Bitlab, "POST-MERGE METHOD", "./boxes/38_Bitlab.html", orange, Linux, 10.10.10.110, 30 pts, "Jan 12, 2020"],
    [Craft, "", "", orange, Linux, 10.10.10.114, 30 pts, "Jan 05, 2020"],
    [Networked, "", "", green, Linux, 10.10.10.146, 20 pts, "Nov 16, 2019"],
    [Jarvis, "", "", orange, Linux, 10.10.10.143, 30 pts, "Nov 09, 2019"],
    [Haystack, "", "", green, Linux, 10.10.10.115, 20 pts, "Nov 02, 2019"],
    [Safe, "NO PRIVESC YET", "./boxes/33_Safe.html", green, Linux, 10.10.10.147, 20 pts, "Oct 26, 2019"],
    [Ellingson, "", "./boxes/32_Ellingson.html", red, Linux, 10.10.10.139, 40 pts, "Oct 19, 2019"],
    [WriteUp, "", "./boxes/31_WriteUp.html", green, Linux, 10.10.10.138, 20 pts,  "Oct 12, 2019"],
    [SwagShop, "", "./boxes/30_swagshop.html", green, Linux, 10.10.10.140, 20 pts, "Sep 28, 2019"],
    [Kryptos, "", "./boxes/29_kryptos.html", white, Linux, 10.10.10.129, 50 pts, "Sep 21, 2019"],
    [Luke, "", "./boxes/28_Luke.html", orange, FreeBSD, 10.10.10.137, 30 pts,  "Sep 14, 2019"],
    [OneTwoSeven, "", "", red, Linux, 10.10.10.133, 40 pts,  "Sep 01, 2019"],
    [CTF, "", "./boxes/26_CTF.html", white, Linux, 10.10.10.122, 50 pts, "Jul 20, 2019"],
    [FriendZone, "", "./boxes/25_Friendzone.html", green, Linux, 10.10.10.123, 20 pts,  "Jul 13, 2019"],
    [Flujab, "", "./boxes/24_Flujab.html", red, Linux, 10.10.10.124, 40 pts,  "Jun 15, 2019"],
    [Help, "", "./boxes/23_Help.html", green, Linux, 10.10.10.121, 20 pts,  "Jun 08, 2019"],
    [Chaos, "", "./boxes/22_Chaos.html", orange, Linux, 10.10.10.120, 30 pts,  "May 25, 2019"],
    [Lightweight, "", "./boxes/21_Lightweight.html", orange, Linux, 10.10.10.119, 30 pts,  "May 11, 2019"],
    [Irked, "", "./boxes/20_Irked.html", green, Linux, 10.10.10.117, 20 pts,  "Apr 27, 2019"],
    [Teacher, "", "./boxes/19_Teacher.html", green, Linux, 10.10.10.153, 20 pts,  "Apr 20, 2019"],
    [Frolic, "", "", green, Linux, 10.10.10.111, 20 pts,  "Mar 24, 2019"],
    [Dab, "", "", red, Linux, 10.10.10.86, 40 pts,  "Feb 02, 2019"],
    [Reddish, "", "", white, Linux, 10.10.10.94, 50 pts,  "Jan 26, 2019"],
    [Mischief, "", "./boxes/15_Mischief.html", white, Linux, 10.10.10.92, 50 pts,  "Jan 06, 2019"],
    [Waldo, "NO PRIVESC YET", "./boxes/14_Waldo.html", orange, Linux, 10.10.10.87, 30 pts,  "Dec 16, 2018"],
    [Active, "", "https://hackedthebox.wordpress.com/htb-active/", green, Windows, 10.10.10.100, 20 pts,  "Dec 09, 2018"],
    [Hawk, "", "https://hackedthebox.wordpress.com/htb-hawk/", orange, Linux, 10.10.10.102, 30 pts,  "Dec 02, 2018"],
    [Jerry, "", "https://hackedthebox.wordpress.com/htb-jerry/", green, Windows, 10.10.10.95, 20 pts,  "Nov 18, 2018"],
    [TartarSauce, "", "https://hackedthebox.wordpress.com/htb-tartarsauce/", orange, Linux, 10.10.10.88, 30 pts,  "Oct 21, 2018"],
    [DevOops, "", "https://hackedthebox.wordpress.com/htb-dev0ops/", orange, Linux, 10.10.10.91, 30 pts,  "Oct 14, 2018"],
    [Sunday, "", "https://hackedthebox.wordpress.com/htb-sunday/", green, Solaris, 10.10.10.76, 20 pts,  "Sep 30, 2018"],
    [Olympus, "", "", orange, Linux, 10.10.10.83, 30 pts,  "Sep 23, 2018"],
    [Canape, "", "https://hackedthebox.wordpress.com/htb-canape/", orange, Linux, 10.10.10.70, 30 pts,  "Sep 16, 2018"],
    [Poison, "", "https://hackedthebox.wordpress.com/htb-poison/", orange, FreeBSD, 10.10.10.84, 30 pts,  "Sep 09, 2018"],
    [Stratosphere, "", "https://hackedthebox.wordpress.com/htb-stratosphere/", orange, Linux, 10.10.10.64, 30 pts, "Sep 02, 2018"],
    [Celestial, "", "", orange, Linux, 10.10.10.85, 30 pts,  "Aug 26, 2018"],
    [Valentine, "", "", green, Linux, 10.10.10.79, 20 pts,  "Jul 29, 2018"],
    [Aragog, "", "", orange, Linux, 10.10.10.78, 30 pts, "Jul 22, 2018"]
]
---

## <span style="color:red">$ htb write-ups</span>

---

<div style="overflow-x:auto">
  <table>
    <tr>
      <td><strong style="text-decoration:underline">BOX NAME</strong></td>
      <td><strong style="text-decoration:underline">OS</strong></td>
      <td><strong style="text-decoration:underline">MACHINE IP</strong></td>
      <td><strong style="text-decoration:underline">RETIRED</strong></td>
    </tr>
    {% for box in page.boxes %}{% if box[2] != "" %}
    <tr>
      <td><a href="{{ box[2] }}">{{ box[0] }}</a> {% if box[1] != "" %}({{box[1]}}){% endif %}</td>
      <td><span style="color:{{ box[3] }}">{{ box[4] }}</span></td>
      <td><span style="color:{{ box[3] }}">{{ box[5] }}</span></td>
      <td>{{ box[7] }}</td>
    </tr>
    {% endif %}{% endfor %}
    {% for box in page.boxes %}{% if box[2] == "" %}
    <tr>
      <td>{{ box[0] }} {% if box[1] != "" %}({{box[1]}}){% endif %}</td>
      <td><span style="color:{{ box[3] }}">{{ box[4] }}</span></td>
      <td><span style="color:{{ box[3] }}">{{ box[5] }}</span></td>
      <td>{{ box[7] }}</td>
    </tr>
    {% endif %}{% endfor %}
  </table>
</div>

---

### LEGEND : <strong style="color:green">EASY (20 pts)</strong> | <strong style="color:orange">MEDIUM (30 pts)</strong> | <strong style="color:red">HARD (40 pts)</strong> | <strong style="color:white">INSANE (50 pts)</strong>


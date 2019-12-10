---
layout: menu
title: "Cyber SEA Game 2019"
description: "A few Cyber SEA Game 2019 challenge write-ups"
header-img: "chals/ctf/2019_CyberSEAGame/cyber_sea_game_2019.png"
tags: [ctf, capture-the-flag, challenges, challenge-write-ups, write-ups, writeups, write-up, writeup, cyberseagame, cyberseagames, cyber-sea-game, cyber-sea-games, solutions, 2019]
challenges: [
  [Fraud(1) Whistle blowing, crypto/1_Fraud1_Whistle_blowing.html, Crypto (50), Fullwidth Unicode Encoding], 
  [Shared, os/2_Shared.html, OS (110), Shared Objects]
]
recommendations: [[Binary Ultra, https://altelus1.github.io/writeups/cyberseagames2019/binary_ultra, Binary (50), 'Write-up by my teammate, <a href="https://altelus1.github.io/about.html" target="_blank">Altelus</a>'], [Present, https://altelus1.github.io/writeups/cyberseagames2019/present, Binary (100), 'Write-up by my teammate, <a href="https://altelus1.github.io/about.html" target="_blank">Altelus</a>']]
---

## <span style="color:red">$ Cyber SEA Game 2019</span>

---

### DURATION
<div style="margin-left:10px">[<span>Thu, 21 Nov 2019, 11:30 PHT</span> - <span>Thu, 21 Nov 2019, 18:30 PHT</span>]</div>

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
     <td><a href="./2019_CyberSEAGame/{{ chal[1] }}">{{ chal[0] }}</a></td>
     <td>{{ chal[2] }}</td>
     <td>{{ chal[3] }}</td>
   </tr>
   {% endfor %}
 </table>
</div>

---

### RECOMMENDATIONS

<div style="overflow-x:auto">
 <table>
   <tr>
     <td><strong style="text-decoration:underline">NAME</strong></td>
     <td><strong style="text-decoration:underline">CATEGORY/PTS</strong></td>
     <td><strong style="text-decoration:underline">TAGS</strong></td>
   </tr>
   {% for chal in page.recommendations %}
   <tr>
     <td><a href="{{ chal[1] }}" target="_blank">{{ chal[0] }}</a></td>
     <td>{{ chal[2] }}</td>
     <td>{{ chal[3] }}</td>
   </tr>
   {% endfor %}
 </table>
</div>

- Write-ups from <a href="https://khroot.com/2019/12/06/cyber-sea-game-2019-write-up/" target="_blank">Team Cambodia</a>
- Write-ups from <a href="https://github.com/end1an/Cyber-SEA-GAME-2019" target="_blank">Team Thailand</a>

  [The_Sword, crypto/2_The_Sword.html, Crypto (50), Embedded Text], 
  [ShellScript, crypto/3_ShellScript.html, Crypto (200), Obfuscated Code], 
  [PDF-JPGS, forensics/4_PDF-JPGS.html, Forensics (120), File Headers], 
  [Notes, forensics/5_Notes.html, Forensics (120), MS Office Macro], 
  [Friend, misc/6_Friend.html, Misc (100), Hash Collision], 
  [Trim_Auth, misc/8_Trim_Auth.html, Misc (150), SQL Truncation], 
  [Intact, network/1_Intact.html, Network (80), FTP], 

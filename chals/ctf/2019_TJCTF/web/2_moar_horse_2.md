---
layout: default
---

# Moar Horse 2 (70 pts)

## CHALLENGE INFO

- __WRITTEN BY__ : okulkarni
- __DESCRIPTION__ :
  ```
  Moar Horse is back and better than ever before! Check out this site and see if you can find the flag. It shouldn't be that hard, right?
  ```
- __CHALLENGE LINK__: https://moar_horse_2.tjctf.org
- __LANDING PAGE__: https://moar_horse_2.tjctf.org/4b043a01-a4b7-4141-8a99-fc94fe7e3778.html
  
  ![Landing Page](./screenshots/moar_horse_2_home.png)

  - __PAGE SOURCE__:
    ```html
    <html>

    <head>
        <link href="/style.css" rel="stylesheet">
    </head>

    <body>
        <div class="jumbotron text-center">
            <div class="container">
                <h1>Welcome to Flag Finding!</h1>
            </div>
        </div>
        <div class="container">
            <div class="row">
                <div class="col-xs-6"> <a href="/9d3b0782-9323-49f8-a5f3-57abd07b82bc.html" class="btn btn-sm animated-button gibson-one">Backward</a> </div>
                <div class="col-xs-6"> <a href="/e634644e-b802-496a-8bb5-0e0aac40779f.html" class="btn btn-sm animated-button gibson-two">Forward</a>
                </div>
            </div>
        </div>
    </body>

    </html>
    ```
- __ASSUMED OBJECTIVE__ : Move FORWARD or BACKWARD to find the flag

---

## NOTES:

- Going `FORWARD` then `BACKWARD` doesn't take you back.
- Run a script that recursively goes through all possible paths

## SOLUTION:

- __*moar_horse_2.py*__
  ```py
  def check_link(target, curr, links):

      print(curr)

      req = r.get(target+curr)

      if "{" in req.text: 
          print(req.text)
          exit()

      if(req.text[319:361]) not in links:
          links.append(req.text[319:361])
          check_link(target, req.text[319:361], links) #BACKWARD

      if(req.text[473:515]) not in links:
          links.append(req.text[473:515])
          check_link(target, req.text[473:515], links) #FORWARD

  target = "https://moar_horse_2.tjctf.org"
  curr = "/4b043a01-a4b7-4141-8a99-fc94fe7e3778.html" # DEFAULT STARTING POINT
  links = ["/4b043a01-a4b7-4141-8a99-fc94fe7e3778.html"]

  check_link(target, curr, links)

  ```
- Running __*moar_horse_2.py*__
  ```console
  python3 moar_horse_2.py

  # /4b043a01-a4b7-4141-8a99-fc94fe7e3778.html
  # /9d3b0782-9323-49f8-a5f3-57abd07b82bc.html
  # /a07cb0d7-df0a-4b5e-9ba3-12fc002fb71a.html
  # /77504246-70cd-4501-bea2-7ca7426f55e9.html
  # /42bc2fcc-d3f6-4de3-9b67-15a865d62cb8.html
  # ...
  # /9e9d65cd-3790-4549-b8eb-50dd5e41e820.html
  # /a6a78b27-0cae-452b-830a-771bf8bd032a.html
  # /638cb4e6-568f-4dbc-b185-d545aff438d6.html
  # /3cf94f73-568f-4dbc-b185-d545aff438d6.html <---has the flag
  ```
  ```html
  <html>

  <head>
      <link href="/style.css" rel="stylesheet">
  </head>

  <body>
      <div class="jumbotron text-center">
          <div class="container">
              <h1>Welcome to Flag Finding!</h1>
          </div>
      </div>
      <div class="container">
          <div class="row">
              <div class="col-xs-6"> <a href="/4b043a01-a4b7-4141-8a99-fc94fe7e3778.html" class="btn btn-sm animated-button gibson-one">Backward</a> </div>
              <div class="col-xs-6"> <a href="/4b043a01-a4b7-4141-8a99-fc94fe7e3778.html" class="btn btn-sm animated-button gibson-two">Forward</a>
              </div>
          </div>
      </div>
  </body>
  <!-- tjctf{s0rry_n0_h0rs3s_anym0ar} -->
  </html>
  ```

---

## FLAG : __tjctf{s0rry_n0_h0rs3s_anym0ar}__

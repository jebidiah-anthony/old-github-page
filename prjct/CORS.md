---
layout: menu
title: "CORS"
description: "This is a brief introduction to Cross Origin Resource Sharing along with common misconfigurations that might lead to exploitation. This was an entry to mubix’s OSCP giveaway challenge 3. I did not win but I still really learned a lot which is still a great takeaway."
tags: [CORS, cross origin resource sharing, cross-origin resource sharing, misconfigurations, misconfig, headers, pre-flight, preflight]
---

# <span style="color:red">Cross Origin Resource Sharing (CORS)</span>

---

## What is CORS?

Web pages, say like http://example.com/page, can always request resources from another web page as long as it comes from the same origin (this includes protocol, domain, and port). This __same origin policy__ helps prevent malicious behavior since data circulates only from within the domain.

But what if the resources you need are only available elsewhere? This is where CORS come into play. It allows you to access resources or to navigate to another server. This is helpful especially when loading images, scripts, stylesheets, etc. CORS requests are done by using standard HTTP methods such as __`GET`__, __`PATCH`__, __`POST`__,  __`PUT`__, and __`DELETE`__ and are implemented using HTTP headers.

__HTTP Request Headers__:
- __`Origin`__
- __`Access-Control-Request-Method`__
- __`Access-Control-Request-Headers`__

__HTTP Response Headers__:
- __`Access-Control-Allow-Origin`__
- __`Access-Control-Allow-Credentials`__
- __`Access-Control-Expose-Headers`__
- __`Access-Control-Max-Age`__
- __`Access-Control-Allow-Methods`__
- __`Access-Control-Allow-Headers`__

__`Access-Control-Allow-Origin`__ allows servers to specify how their resources are shared externally. Many times, this header will be set to __`*`__ pertaining to any external domain. It could be a list of domains or it could even be set to __`null`__. 

Most servers only allow __`GET`__ requests as to avoid any intention of maliciously editing or deleting assets. However, such requests are not automatically dropped by the server. It first undergoes a __preflight test__ in order to determine what methods are allowed.

---

__Pre-flight Test__

1. It first sends an __`OPTIONS`__ request:
   ```http
   OPTIONS /resource HTTP/1.1
   Origin: example.com
   Access-Control-Request-Method: DELETE
   ```

2. The server responds:
   ```http
   HTTP/1.1 200 OK
   Access-Control-Allow-Origin: *
   Access-Control-Allow-Method: DELETE, GET
   ```

After the pre-flight test, the original request is then handled.

3. Deleting a resource:
   ```http
   DELETE /resource HTTP/1.1
   ORIGIN: example.com
   Access-Control-Request-Method: DELETE
   ```

4. The server responds:
   ```http
   HTTP/1.1 200 OK
   Access-Control-Allow-Origin: *
   ```

Since the __`DELETE`__ method was allowed after checking during the pre-flight test, the resource was successfully deleted. Other headers automatically added by the browser are omitted from the example above.

---

## Common Misconfigurations

- __`Access-Control-Allow-Credentials`__ is set to __`true`__:

   > Credentials are often stored in cookies and cookies are used to maintain our sessions or what the browser uses to indicate that we are currently logged in. Its value is mostly unique to our own and this header enables credential transmission which is bad new especially for websites susceptible to [Cross-Site Scripting (XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)).

   > This would only be exploitable if __`Access-Control-Allow-Origin`__ is not set to a wildcard (__`*`__) even if the a wildcard was used to cover a website's subdomains (e.g. __`*.example.com`__).

   > Exposing your website to everyone and used along with this header the console would return __`Cannot use wildcard in Access-Control-Allow-Origin when credentials flag is true.`__ This could be a work around but this is still bad practice.

- __`Access-Control-Allow-Origin: null`__

  > Hostile documents could be crafted and sent with a __`Origin: null`__ header and it would be accepted since serialization of the __`Origin`__ of files are defined to be null.
  
  > This should not be used.

- Don't give unneeded methods in __`Access-Control-Allow-Method`__

  > __`DELETE`__, __`PATCH`__, __`POST`__, and __`PUT`__ could be used to alter or remove a site's assets/resources and even trigger further unwanted actions.

- Giving access to everyone -- __`Access-Control-Allow-Origin: *`__

  > Perhaps adding specific websites to a white list might be advisable if resources contain somewhat sensitive content.

  > Or perhaps limiting accessible subdomains and endpoints would prove to be more secure but this would require different configurations.

---

## REFERENCES

```
- https://www.codecademy.com/articles/what-is-cors
- https://portswigger.net/research/exploiting-cors-misconfigurations-for-bitcoins-and-bounties
- https://www.geekboy.ninja/blog/exploiting-misconfigured-cors-cross-origin-resource-sharing/
- https://stackoverflow.com/questions/12001269/what-are-the-security-risks-of-setting-access-control-allow-origin
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
- https://mobilejazz.com/blog/which-security-risks-do-cors-imply/
```

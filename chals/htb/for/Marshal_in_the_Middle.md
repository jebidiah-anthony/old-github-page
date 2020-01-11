---
layout: menu
description: "HTB Marshal in the Middle' [FORENSICS] (40 pts)"
header-img: "chals/htb/htb.png"
tags: [hackthebox, htb, challenge, forensics, network, network forensics, write up, solution, marshal in the middle]
---

# <span style="color:red">Marshal in the Middle [FORENSICS] (40 pts)</span>

---

## PART 1 : CHALLENGE DESCRIPTION

```
The security team was alerted to suspicous network activity from a production web server.
Can you determine if any data was stolen and what it was?
```

---

## PART 2 : GIVEN FILES

[>] [MarshalInTheMiddle.zip](./files/MarshalInTheMiddle.zip)

```console
$ sha256sum MarshalInTheMiddle.zip

  cdf53bab266ab4b8a28b943516bc064e9f966dae0a33503648694e15cb50ae2b  MarshalInTheMiddle.zip

$ unzip MarshalInTheMiddle.zip

  Archive:  MarshalInTheMiddle.zip
     creating: bro/
  [MarshalInTheMiddle.zip] bro/conn.log password: hackthebox
    inflating: bro/conn.log            
    inflating: bro/http.log            
    inflating: bro/packet_filter.log   
    inflating: bro/files.log           
    inflating: bro/ssl.log             
    inflating: bro/weird.log           
    inflating: bro/dns.log             
    inflating: bundle.pem              
    inflating: chalcap.pcapng          
    inflating: secrets.log 

```

---

## PART 3 : GETTING THE FLAG

Since this is a network forensics challenge, I first checked what protocols comprises the given __`.pcapng`__ file:

```console
$ tshark -r chalcap.pcapng 2>/dev/null | sed -e 's/^[ ]*\w*\s*//g' | sed -E 's/\s{2,}/ /g' | cut -d' ' -f5 | sort | uniq -c | sort -bnr

  9013 TCP
  1992 TLSv1.2
   934 HTTP2
   854 DNS
   668 HTTP
   158 TLSv1
    11 ARP
     7 DHCPv6
     2 HTTP2/XML
     1 SSH
     1 MP4
 
```



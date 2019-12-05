---
layout: default
description: "HTB Keep Trying' [FORENSICS] (50 pts)"
header-img: "chals/htb/htb.png"
tags: "hackthebox, htb, challenge, forensics, network, network-forensics, write-up, solution, dns, dns-txt, txt, txt-record, dns-exfil, dns-exfiltration, base64, rc4, keep-tryin, keep-trying"
---

# Keep Tryin' [FORENSICS] (50 pts)

---

## PART 1 : CHALLENGE DESCRIPTION

```
This packet capture seems to show some suspicious traffic
```

---

## PART 2 : GIVEN FILES

[>] [keeptrying.zip](./files/keeptrying.zip)
- keeptryin.pcap

---

## PART 3 : GETTING THE FLAG

```console
$ unzip keeptrying.zip

  Archive:  keeptrying.zip
  [keeptrying.zip] keeptryin.pcap password: hackthebox 
    inflating: keeptryin.pcap 

```

The zip file contains a <span style="color:orange">.pcap</span> file and opening the file using __`tshark`__ shows:

```console
$ tshark -r keeptryin.pcap

      1   0.000000 192.168.135.128 → 172.16.60.1  DNS 98 Standard query 0x601d TXT init.c2VjcmV0LnR4dHwx.totallylegit.com
      2   0.001224  172.16.60.1 → 192.168.135.128 DNS 113 Standard query response 0x601d TXT init.c2VjcmV0LnR4dHwx.totallylegit.com TXT
      3   0.003428 192.168.135.128 → 172.16.60.1  DNS 272 Standard query 0xa700 TXT 0.0ejXWsr6TH-P_1xkEstaVwi7WDy8AcxufnGotWXH3ckb2Lh5A-qFljIWOAOLUS0.T1W8P4CpiCZbCM7_QKcv-r0JG29RpsyYY5YkZRxo7YDIYUJpHlGgxu5PWV1G_DA.KNrmnrktfbeDgzcpPJBjPTeMYx3Qs1Q6bAuFhROWXemJ80gPTYIz0xl8usJQN3m.w.totallylegit.com
      4   0.004150  172.16.60.1 → 192.168.135.128 DNS 286 Standard query response 0xa700 TXT 0.0ejXWsr6TH-P_1xkEstaVwi7WDy8AcxufnGotWXH3ckb2Lh5A-qFljIWOAOLUS0.T1W8P4CpiCZbCM7_QKcv-r0JG29RpsyYY5YkZRxo7YDIYUJpHlGgxu5PWV1G_DA.KNrmnrktfbeDgzcpPJBjPTeMYx3Qs1Q6bAuFhROWXemJ80gPTYIz0xl8usJQN3m.w.totallylegit.com TXT
      5   2.986212 192.168.135.128 → 172.16.60.1  TCP 66 49828 → 80 [SYN, ECN, CWR] Seq=0 Win=8192 Len=0 MSS=1460 WS=256 SACK_PERM=1
      6   2.986598  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49828 [SYN, ACK] Seq=0 Ack=1 Win=64240 Len=0 MSS=1460
      7   2.986672 192.168.135.128 → 172.16.60.1  TCP 54 49828 → 80 [ACK] Seq=1 Ack=1 Win=64240 Len=0
      8   2.986850 192.168.135.128 → 172.16.60.1  TCP 288 POST /flag HTTP/1.1  [TCP segment of a reassembled PDU]
      9   2.987027  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49828 [ACK] Seq=1 Ack=235 Win=64240 Len=0
     10   2.987055 192.168.135.128 → 172.16.60.1  HTTP 63 POST /flag HTTP/1.1  (application/x-www-form-urlencoded)
     11   2.987195  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49828 [ACK] Seq=1 Ack=244 Win=64240 Len=0
     12   5.629379  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49828 [FIN, PSH, ACK] Seq=1 Ack=244 Win=64240 Len=0
     13   5.629476 192.168.135.128 → 172.16.60.1  TCP 54 49828 → 80 [ACK] Seq=244 Ack=2 Win=64240 Len=0
     14   5.629672 192.168.135.128 → 172.16.60.1  TCP 54 49828 → 80 [FIN, ACK] Seq=244 Ack=2 Win=64240 Len=0
     15   5.629838  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49828 [ACK] Seq=2 Ack=245 Win=64239 Len=0
     16   9.921970 192.168.135.128 → 172.16.60.1  TCP 66 49829 → 80 [SYN, ECN, CWR] Seq=0 Win=8192 Len=0 MSS=1460 WS=256 SACK_PERM=1
     17   9.922358  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49829 [SYN, ACK] Seq=0 Ack=1 Win=64240 Len=0 MSS=1460
     18   9.922437 192.168.135.128 → 172.16.60.1  TCP 54 49829 → 80 [ACK] Seq=1 Ack=1 Win=64240 Len=0
     19   9.922626 192.168.135.128 → 172.16.60.1  TCP 290 POST /lootz HTTP/1.1  [TCP segment of a reassembled PDU]
     20   9.922821  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49829 [ACK] Seq=1 Ack=237 Win=64240 Len=0
     21   9.922844 192.168.135.128 → 172.16.60.1  HTTP 82 POST /lootz HTTP/1.1  (application/x-www-form-urlencoded)
     22   9.923008  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49829 [ACK] Seq=1 Ack=265 Win=64240 Len=0
     23  13.117202  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49829 [FIN, PSH, ACK] Seq=1 Ack=265 Win=64240 Len=0
     24  13.117330 192.168.135.128 → 172.16.60.1  TCP 54 49829 → 80 [ACK] Seq=265 Ack=2 Win=64240 Len=0
     25  13.117516 192.168.135.128 → 172.16.60.1  TCP 54 49829 → 80 [FIN, ACK] Seq=265 Ack=2 Win=64240 Len=0
     26  13.117678  172.16.60.1 → 192.168.135.128 TCP 60 80 → 49829 [ACK] Seq=2 Ack=266 Win=64239 Len=0

```

It is a relatively short packet capture and two things you will notice immediately are <strong style="color:orange">DNS TXT</strong> records and <strong style="color:orange">HTTP POST</strong> requests. One of which is a __POST__ request to __`/flag`__.

Showing only HTTP requests and extracting POST data:

```console
$ tshark -Y "http.request.method==POST" -r keeptryin.pcap

     10   2.987055 192.168.135.128 → 172.16.60.1  HTTP 63 POST /flag HTTP/1.1  (application/x-www-form-urlencoded)
     21   9.922844 192.168.135.128 → 172.16.60.1  HTTP 82 POST /lootz HTTP/1.1  (application/x-www-form-urlencoded)

$ tshark -Y "http.request.method==POST" -T fields -e http.file_data -r keeptryin.pcap

  TryHarder
  S2VlcCB0cnlpbmcsIGJ1ZmZ5Cg==

$ echo S2VlcCB0cnlpbmcsIGJ1ZmZ5Cg== | base64 -d

  Keep trying, buffy

```

It doesn't show much but it might be useful for later.

Now, filtering the pcap for <strong style="color:orange">DNS TXT</strong> records and returning query names:

```console
$ tshark -Y "dns" -r keeptryin.pcap | grep response

      2   0.001224  172.16.60.1 → 192.168.135.128 DNS 113 Standard query response 0x601d TXT init.c2VjcmV0LnR4dHwx.totallylegit.com TXT
      4   0.004150  172.16.60.1 → 192.168.135.128 DNS 286 Standard query response 0xa700 TXT 0.0ejXWsr6TH-P_1xkEstaVwi7WDy8AcxufnGotWXH3ckb2Lh5A-qFljIWOAOLUS0.T1W8P4CpiCZbCM7_QKcv-r0JG29RpsyYY5YkZRxo7YDIYUJpHlGgxu5PWV1G_DA.KNrmnrktfbeDgzcpPJBjPTeMYx3Qs1Q6bAuFhROWXemJ80gPTYIz0xl8usJQN3m.w.totallylegit.com TXT

$ tshark -Y "dns.txt" -T fields -e dns.qry.name -n -r keeptryin.pcap

  init.c2VjcmV0LnR4dHwx.totallylegit.com
  0.0ejXWsr6TH-P_1xkEstaVwi7WDy8AcxufnGotWXH3ckb2Lh5A-qFljIWOAOLUS0.T1W8P4CpiCZbCM7_QKcv-r0JG29RpsyYY5YkZRxo7YDIYUJpHlGgxu5PWV1G_DA.KNrmnrktfbeDgzcpPJBjPTeMYx3Qs1Q6bAuFhROWXemJ80gPTYIz0xl8usJQN3m.w.totallylegit.com

```

Omitting __`init.`__, the initial number for succeeding queries (e.g. __`0.`__), and __`.totallylegit.com`__:

```console
$ data=$(tshark -Y "dns.txt" -T fields -e dns.qry.name -n -r keeptryin.pcap)

$ echo $data | tr ' ' '\n' | sed -E "s/^(init.|\w\.)(.*).totallylegit.com/\2/g" | tr -d '.'

  c2VjcmV0LnR4dHwx
  0ejXWsr6TH-P_1xkEstaVwi7WDy8AcxufnGotWXH3ckb2Lh5A-qFljIWOAOLUS0T1W8P4CpiCZbCM7_QKcv-r0JG29RpsyYY5YkZRxo7YDIYUJpHlGgxu5PWV1G_DAKNrmnrktfbeDgzcpPJBjPTeMYx3Qs1Q6bAuFhROWXemJ80gPTYIz0xl8usJQN3mw

```

The "__`.`__" character was also dropped since it is a special character interpreted differently for Domain Names.

The output would seem to be a <span style="color:orange">base64 encoded string</span> but instead of "__`+`__" and "__`/`__", the string returned contains "__`_`__" and "__`-`__".

Maybe those were substituted during exfiltration and trying to guess the proper substitution:

```console
$ data=$(echo $data | tr ' ' '\n' | sed -E "s/^(init.|\w\.)(.*).totallylegit.com/\2/g" | tr -d '.')

$ echo $data | tr '-' '+' | tr '_' '/' | tr ' ' '\n'

  c2VjcmV0LnR4dHwx
  0ejXWsr6TH+P/1xkEstaVwi7WDy8AcxufnGotWXH3ckb2Lh5A+qFljIWOAOLUS0T1W8P4CpiCZbCM7/QKcv+r0JG29RpsyYY5YkZRxo7YDIYUJpHlGgxu5PWV1G/DAKNrmnrktfbeDgzcpPJBjPTeMYx3Qs1Q6bAuFhROWXemJ80gPTYIz0xl8usJQN3mw

$ echo c2VjcmV0LnR4dHwx | base64 -d | xxd 

  00000000: 7365 6372 6574 2e74 7874 7c31            secret.txt|1

$ secret="0ejXWsr6TH+P/1xkEstaVwi7WDy8AcxufnGotWXH3ckb2Lh5A+qFljIWOAOLUS0T1W8P4CpiCZbCM7/QKcv+r0JG29RpsyYY5YkZRxo7YDIYUJpHlGgxu5PWV1G/DAKNrmnrktfbeDgzcpPJBjPTeMYx3Qs1Q6bAuFhROWXemJ80gPTYIz0xl8usJQN3mw"

$ echo ${secret}== | base64 -d | xxd

  00000000: d1e8 d75a cafa 4c7f 8fff 5c64 12cb 5a57  ...Z..L...\d..ZW
  00000010: 08bb 583c bc01 cc6e 7e71 a8b5 65c7 ddc9  ..X<...n~q..e...
  00000020: 1bd8 b879 03ea 8596 3216 3803 8b51 2d13  ...y....2.8..Q-.
  00000030: d56f 0fe0 2a62 0996 c233 bfd0 29cb feaf  .o..*b...3..)...
  00000040: 4246 dbd4 69b3 2618 e589 1947 1a3b 6032  BF..i.&....G.;`2
  00000050: 1850 9a47 9468 31bb 93d6 5751 bf0c 028d  .P.G.h1...WQ....
  00000060: ae69 eb92 d7db 7838 3372 93c9 0633 d378  .i....x83r...3.x
  00000070: c631 dd0b 3543 a6c0 b858 5139 65de 989f  .1..5C...XQ9e...
  00000080: 3480 f4d8 233d 3197 cbac 2503 779b       4...#=1...%.w.

$ echo ${secret}== | base64 -d > secret_file

$ file secret_file

  secret_file: data

```

A file called __`secret.txt`__ was extracted during DNS exfiltration but the following data doesn't seem to be a proper txt file.

Maybe it was encrypted by flipping or XORing the file bytes.

![RC4 Decrypt](./screenshots/keep_tryin_rc4.png)

As it turns out, the file was <span style="color:orange">encrypted using RC4</span> (a stream cipher closely related to simple XORs) where the key (__`TryHarder`__) used was taken from the HTTP POST request to __`/flag`__.	

Now saving the generated zip file as __`secret.zip`__:

```console
$ unzip secret.zip

  Archive:  secret.zip
    inflating: secret.txt  

$ cat secret.txt

  HTB{$n3aky_DN$_Tr1ck$}

```

---

## FLAG : __HTB{$n3aky_DN$_Tr1ck$}__

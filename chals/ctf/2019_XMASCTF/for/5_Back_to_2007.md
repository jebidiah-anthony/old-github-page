---
layout: menu
title: "Back to 2007 [for 499]"
description: "X-MAS CTF 2019 [Forensics] Back to 2007 (499 pts)"
header-img: "chals/ctf/2019_XMASCTF/xmas_ctf_2019.png"
tags: [xmas, x-mas, xmas ctf, x-mas ctf, 2019, ctf, challenge, writeup, write-up, solution, forensics, network forensics, networking, networks, udp, udp-stream]
---

# <span style="color:green">Back to 2007 (499 pts)</span>

---

## PART 1 : CHALLENGE DESCRIPTION

```
I captured some messages sent on this game server, and I really want to see what they say :(

Files: sd_doomsday.pcap
Author: Milkdrop
Note: Each character in the flag message is doubled: XX--MMAASS{{....}}. Please submit only one character from every pair.
```

---

## PART 2 : GIVEN FILES

[>] [fun on sd_doomsday.pcapng](./files/fun on sd_doomsday.pcapng)

---

## PART 3 : CHECKING THE TRAFFIC

It was noted that the flag's characters were repeating however running __`strings`__ returns nothing:

```console
$ strings fun\ on\ sd_doomsday.pcapng | grep -ae "XX--" | wc -l

  0

```

No matches were found so the flag must be either scattered or altered inside the traffic if not embedded in a file.

Now viewing the network traffic using __`tshark`__:

```console
$ tshark -r 'fun on sd_doomsday.pcapng'

      1   0.000000 162.254.196.68 → 192.168.1.100 UDP 350 27019 → 63592 Len=308
      2   0.258607 192.168.1.100 → 162.254.196.68 UDP 78 63592 → 27019 Len=36
      3   0.512194 37.61.223.15 → 192.168.1.100 TCP 54 6568 → 50884 [ACK] Seq=1 Ack=1 Win=254 Len=0
      4   0.512238 192.168.1.100 → 37.61.223.15 TCP 54 [TCP ACKed unseen segment] 50884 → 6568 [ACK] Se
  q=1 Ack=2 Win=511 Len=0
      5   4.122025 192.168.1.100 → 137.74.91.216 UDP 67 49826 → 27015 Len=25
      6   4.133071 192.168.1.100 → 5.200.27.206 UDP 67 49826 → 27105 Len=25
      7   4.133173 192.168.1.100 → 212.83.129.138 UDP 67 49826 → 27015 Len=25
      8   4.504978 5.200.27.206 → 192.168.1.100 UDP 161 27105 → 49826 Len=119
      9   6.382254 192.168.1.100 → 162.254.196.68 UDP 126 63592 → 27019 Len=84
     10   6.712720 192.168.1.100 → 137.74.91.216 UDP 67 49827 → 27015 Len=25
  ...omitted...
  24211 101.965019 192.168.1.100 → 216.58.215.48 TCP 54 [TCP Retransmission] 50997 → 443 [FIN, ACK] Seq=8631 Ack=4414 Win=131072 Len=0
  24212 102.296533 216.58.215.48 → 192.168.1.100 TCP 54 443 → 50997 [FIN, ACK] Seq=4414 Ack=8632 Win=81152 Len=0
  24213 102.296570 192.168.1.100 → 216.58.215.48 TCP 54 50997 → 443 [ACK] Seq=8632 Ack=4415 Win=131072 Len=0
  24214 103.628170 162.254.196.68 → 192.168.1.100 UDP 286 27019 → 63592 Len=244
  24215 103.628266 162.254.196.68 → 192.168.1.100 UDP 286 27019 → 63592 Len=244
  24216 103.724487 192.168.1.100 → 64.74.17.221 TCP 138 50922 → 12975 [PSH, ACK] Seq=85 Ack=1 Win=512 Len=84
  24217 103.885185 192.168.1.100 → 162.254.196.68 UDP 78 63592 → 27019 Len=36
  24218 103.887489 64.74.17.221 → 192.168.1.100 TCP 54 12975 → 50922 [ACK] Seq=1 Ack=169 Win=1025 Len=0
  24219 106.495478 162.254.196.68 → 192.168.1.100 UDP 286 27019 → 63592 Len=244
  24220 106.707533 192.168.1.100 → 162.254.196.68 UDP 174 63592 → 27019 Len=132

$ tshark -2 -R "udp" -r 'fun on sd_doomsday.pcapng' | wc -l

  3405

$ tshark -2 -R "udp" -T fields -e udp.stream -r 'fun on sd_doomsday.pcapng' | sort | uniq -c

      133 0
  ...omitted...
     3174 53
  ...omitted...

```

There seems to be a lot of data passed over UDP and it seems worth further exploring. This idea is supported by the fact that most of the UDP packets belong to the same stream (<strong style="color:green">stream 53</strong>)

---

## PART 4 : GETTING THE FLAG

From my observations the average length of each packet data is around 100-250 and further filtering the packets by its length reduces traffic data significantly:

```console
$ tshark -2 -R "udp.stream eq 53 and data.len > 100 and data.len < 250" -r 'fun on sd_doomsday.pcapng' | wc -l 

  225

```

Since according to the challenge the flag's characters were repeating, the next step I did was to search for packet data with consecutive repeating bytes:

```console
$ packet_data=$(tshark -2 -R "udp.stream eq 53 and data.len > 100 and data.len < 250" -T fields -e data -r 'fun on sd_doomsday.pcapng')

$ echo $packet_data | tr ' ' '\n' | egrep --color -E "([1-9a-f].)\1([1-9a-f].)\2([1-9a-f].)\3"

  ...omitted...
  6f0b00003f060000713ce2b0013fefedcfc81a3117960722121414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414142424242414141414f495e444552435540445f51514141424242424141414141414141424028044440b906d01006070a205408e7642a0e63132430000000000004370a20540b84111c0
  42060000710b0000a1f1ef003fefedcf88df4500bd80002aa3af21b430baaf20363680a634b6b53080a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a020212121a1a0a0a0a0af2427aa22a9a12228aaafa0a0a020212121a1a0a0a0a0a0a0a020000000a06139d10280bb200540d3e2e2440b800218050004a1e8440b803012c385c450e0f3137295e23d00f8
  7a0d0000dc06000071987db1013fefedcf881231179607228285d5d2d2d414143435b5b71713434777723237f7f575764643d3d63633f3f5e5e61613737686864647f7f545470703e3e61613737686864647f7f5f5f5f5f5d5d72702b044440bf0ae010020f3a205c0c46029a0e4b62d4300000000000043f3a205c062c00dc0
  df0600007c0d0000218fc4013fefedcf48d74580ac80002aa3af21b430baaf20363680a634b6b530002cac9696a6a6a0a0a9a9bdbd98183aba9393b9b9afafb3331a9ab6b69999af2f37b79898b33334343abaaf2f3a3a181837b79898b33334343abaafafafafafafbe3e000000a0e17ad102c0bb200440d362e8450b80028806000421ee450b80f017c385c456e035a3fa92c83d00020000be000080

```

Four packet data contains repeating bytes that is long enough to form a flag.

### The strings were: 

1. <div style="color:yellooverflow-x:auto;padding-top:10px">6f 0b 00 00 3f 06 00 00 71 3c e2 b0 01 3<strong style="color:green">f ef e</strong>d cf c8 1a 31 17 96 07 2<strong style="color:green">2 12 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 24 24 24 24 14 14 14 1</strong>4 f4 95 e4 44 55 24 35 54 04 45 f<strong style="color:green">5 15 14 14 14 24 24 24 24 14 14 14 14 14 14 14 1</strong>4 24 02 80 44 44 0b 90 6d 01 00 60 70 a2 05 40 8e 76 42 a0 e6 31 32 43 00 00 00 00 00 00 43 70 a2 05 40 b8 41 11 c0</div>

2. <div style="overflow-x:auto;padding-top:10px">42 06 00 00 71 0b 00 00 a1 f1 ef 00 3f ef ed cf 88 df 45 00 bd 80 00 2a a3 af 21 b4 30 ba af 20 <strong style="color:green">36 36</strong> 80 a6 34 b6 b5 30 80 <strong style="color:green">a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0 a0</strong> a0 20 <strong style="color:green">21 21</strong> 21 a1 <strong style="color:green">a0 a0 a0 a0</strong> af 24 27 aa 22 a9 a1 22 28 aa af <strong style="color:green">a0 a0</strong> a0 20 <strong style="color:green">21 21</strong> 21 a1 <strong style="color:green">a0 a0 a0 a0 a0 a0</strong> a0 20 00 00 00 a0 61 39 d1 02 80 bb 20 05 40 d3 <strong style="color:green">e2 e2</strong> 44 0b 80 02 18 05 00 04 a1 e8 44 0b 80 30 12 c3 85 c4 50 e0 f3 13 72 95 e2 3d 00 f8</div>

3. <div style="overflow-x:auto;padding-top:10px">7a 0d 00 00 dc 06 00 00 71 98 7d b1 01 3<strong style="color:green">f ef e</strong>d cf 88 12 31 17 96 07 2<strong style="color:green">2 82 85 d5 d2 d2 d4 14 14 34 35 b5 b7 17 13 43 47 77 72 32 37 f7 f5 75 76 46 43 d3 d6 36 33 f3 f5 e5 e6 16 13 73 76 86 86 46 47 f7 f5 45 47 07 03 e3 e6 16 13 73 76 86 86 46 47 f7 f5 f5 f5 f5 f5 d5 d</strong>7 27 02 b0 44 44 0b f0 ae 01 00 20 f3 a2 05 c0 c4 60 29 a0 e4 b6 2d 43 00 00 00 00 00 00 43 f3 a2 05 c0 62 c0 0d c0</div>

4. <div style="overflow-x:auto;padding-top:10px">df 06 00 00 7c 0d 00 00 21 8f c4 01 3f ef ed cf 48 d7 45 80 ac 80 00 2a a3 af 21 b4 30 ba af 20 <strong style="color:green">36 36</strong> 80 a6 34 b6 b5 30 00 2c ac <strong style="color:green">96 96 a6 a6 a0 a0 a9 a9 bd bd</strong> 98 18 3a ba <strong style="color:green">93 93 b9 b9 af af</strong> b3 33 1a 9a <strong style="color:green">b6 b6 99 99</strong> af 2f 37 b7 <strong style="color:green">98 98</strong> b3 33 <strong style="color:green">34 34</strong> 3a ba af 2f <strong style="color:green">3a 3a 18 18</strong> 37 b7 <strong style="color:green">98 98</strong> b3 33 <strong style="color:green">34 34</strong> 3a ba <strong style="color:green">af af af af af af</strong> be 3e 00 00 00 a0 e1 7a d1 02 c0 bb 20 04 40 d3 62 e8 45 0b 80 02 88 06 00 04 21 ee 45 0b 80 f0 17 c3 85 c4 56 e0 35 a3 fa 92 c8 3d 00 02 00 00 be 00 00 80</div>

The first and second strings may have numerous repeating bytes but their variation of is almost non-existent so I just dropped it.

The third string seems to be a prime candidate for a flag since trying to convert the highlighted hex data into ASCII returns:

```console
$ string="2 82 85 d5 d2 d2 d4 14 14 34 35 b5 b7 17 13 43 47 77 72 32 37 f7 f5 75 76 46 43 d3 d6 36 33 f3 f5 e5 e6 16 13 73 76 86 86 46 47 f7 f5 45 47 07 03 e3 e6 16 13 73 76 86 86 46 47 f7 f5 f5 f5 f5 f5 d5 d"

$ echo $string | tr -d " " | xxd -p -r

  ((]]--AACC[[qq44ww##WWdd==cc??^^aa77hhddTTpp>>aa77hhdd____]]

```

It seems close to the actual flag but trying to figure how to bring it back to its original format was too much for me so maybe this is nothing more than a rabbit hole.

The fourth string, however, has repeating bytes but are spread out throughout the data and wondering what do with it made me try rotating the bits for each byte counter-clockwise.

```py
>>> bits = bin(ord("X"))[2:].zfill(8)
>>> bits
'01011000'
>>> shifted = bits[-1] + bits[:-1]
>>> shifted
'00101100'
>>> hex(int(shifted, 2))[2:]
'2c'
```

Doing this rotation for the string "<strong style="color:orange">X-MAS{</strong>":

```py
>>> def rotateBits(char):
...     bits = bin(ord(char))[2:].zfill(8)
...     shifted = bits[-1] + bits[:-1]
...     return hex(int(shifted, 2))[2:]
... 
>>> [rotateBits(char) for char in "X-MAS{"]
['2c', '96', 'a6', 'a0', 'a9', 'bd']
```

And true enough for the fourth string, the rotated hex value were found:

- <div style="overflow-x:auto;padding-top:10px">df 06 00 00 7c 0d 00 00 21 8f c4 01 3f ef ed cf 48 d7 45 80 ac 80 00 2a a3 af 21 b4 30 ba af 20 36 36 80 a6 34 b6 b5 30 00 <strong style="color:red">2c</strong> ac <strong style="color:red">96</strong> 96 <strong style="color:red">a6</strong> a6 <strong style="color:red">a0</strong> a0 <strong style="color:red">a9</strong> a9 <strong style="color:red">bd</strong> bd 98 18 3a ba 93 93 b9 b9 af af b3 33 1a 9a b6 b6 99 99 af 2f 37 b7 98 98 b3 33 34 34 3a ba af 2f 3a 3a 18 18 37 b7 98 98 b3 33 34 34 3a ba af af af af af af be 3e 00 00 00 a0 e1 7a d1 02 c0 bb 20 04 40 d3 62 e8 45 0b 80 02 88 06 00 04 21 ee 45 0b 80 f0 17 c3 85 c4 56 e0 35 a3 fa 92 c8 3d 00 02 00 00 be 00 00 80</div>

Now reversing the rotation by going clockwise for the whole packet data starting from the <strong style="color:red">2c</strong> byte:

```py
>>> def rotateBits(byte):
...     bits = bin(int(byte, 16))[2:].zfill(8)
...     shifted = bits[1:] + bits[0]
...     return hex(int(shifted, 2))[2:]
... 
>>> [rotateBits(byte) for byte in packet_data]
['58', '59', '2d', '2d', '4d', '4d', '41', '41', '53', '53', '7b', '7b', '31', '30', '74', '75', '27', '27', '73', '73', '5f', '5f', '67', '66', '34', '35', '6d', '6d', '33', '33', '5f', '5e', '6e', '6f', '31', '31', '67', '66', '68', '68', '74', '75', '5f', '5e', '74', '74', '30', '30', '6e', '6f', '31', '31', '67', '66', '68', '68', '74', '75', '5f', '5f', '5f', '5f', '5f', '5f', '7d', '7c', '0', '0', '0', '41', 'c3', 'f4', 'a3', '4', '81', '77', '40', '8', '80', 'a7', 'c4', 'd1']
>>> [int(rotateBits(byte),16) for byte in packet_data]
[88, 89, 45, 45, 77, 77, 65, 65, 83, 83, 123, 123, 49, 48, 116, 117, 39, 39, 115, 115, 95, 95, 103, 102, 52, 53, 109, 109, 51, 51, 95, 94, 110, 111, 49, 49, 103, 102, 104, 104, 116, 117, 95, 94, 116, 116, 48, 48, 110, 111, 49, 49, 103, 102, 104, 104, 116, 117, 95, 95, 95, 95, 95, 95, 125, 124, 0, 0, 0, 65, 195, 244, 163, 4, 129, 119, 64, 8, 128, 167, 196, 209]
>>> packet_data = "2c ac 96 96 a6 a6 a0 a0 a9 a9 bd bd 98 18 3a ba 93 93 b9 b9 af af b3 33 1a 9a b6 b6 99 99 af 2f 37 b7 98 98 b3 33 34 34 3a ba af 2f 3a 3a 18 18 37 b7 98 98 b3 33 34 34 3a ba af af af af af af be 3e 00 00 00 a0 e1 7a d1 02 c0 bb 20 04 40 d3 62 e8"
>>> packet_data = packet_data.split(" ")
>>> flag = [rotateBits(byte) for byte in packet_data]
>>> flag
['58', '59', '2d', '2d', '4d', '4d', '41', '41', '53', '53', '7b', '7b', '31', '30', '74', '75', '27', '27', '73', '73', '5f', '5f', '67', '66', '34', '35', '6d', '6d', '33', '33', '5f', '5e', '6e', '6f', '31', '31', '67', '66', '68', '68', '74', '75', '5f', '5e', '74', '74', '30', '30', '6e', '6f', '31', '31', '67', '66', '68', '68', '74', '75', '5f', '5f', '5f', '5f', '5f', '5f', '7d', '7c', '0', '0', '0', '41', 'c3', 'f4', 'a3', '4', '81', '77', '40', '8', '80', 'a7', 'c4', 'd1']
>>> flag = [int(x, 16) for x in flag]
>>> flag
[88, 89, 45, 45, 77, 77, 65, 65, 83, 83, 123, 123, 49, 48, 116, 117, 39, 39, 115, 115, 95, 95, 103, 102, 52, 53, 109, 109, 51, 51, 95, 94, 110, 111, 49, 49, 103, 102, 104, 104, 116, 117, 95, 94, 116, 116, 48, 48, 110, 111, 49, 49, 103, 102, 104, 104, 116, 117, 95, 95, 95, 95, 95, 95, 125, 124, 0, 0, 0, 65, 195, 244, 163, 4, 129, 119, 64, 8, 128, 167, 196, 209]
>>> flag = [chr(x) for x in flag]
>>> flag
['X', 'Y', '-', '-', 'M', 'M', 'A', 'A', 'S', 'S', '{', '{', '1', '0', 't', 'u', "'", "'", 's', 's', '_', '_', 'g', 'f', '4', '5', 'm', 'm', '3', '3', '_', '^', 'n', 'o', '1', '1', 'g', 'f', 'h', 'h', 't', 'u', '_', '^', 't', 't', '0', '0', 'n', 'o', '1', '1', 'g', 'f', 'h', 'h', 't', 'u', '_', '_', '_', '_', '_', '_', '}', '|', '\x00', '\x00', '\x00', 'A', 'Ã', 'ô', '£', '\x04', '\x81', 'w', '@', '\x08', '\x80', '§', 'Ä', 'Ñ']
>>> flag = "".join(flag)[::2]
>>> flag
"X-MAS{1t's_g4m3_n1ght_t0n1ght___}\x00\x00Ã£\x81@\x80Ä"
```

---

## FLAG : <div style="width:100%;overflow-x:auto"><h2>FLAG : <strong>X-MAS{1t's_g4m3_n1ght_t0n1ght___}</strong></h2></div>























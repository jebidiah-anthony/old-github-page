---
layout: menu
description: "HTB Marshal in the Middle' [FORENSICS] (40 pts)"
header-img: "chals/htb/htb.png"
tags: [hackthebox, htb, challenge, forensics, network, network forensics, write up, solution, marshal in the middle, ssl strip, ssl\/tls, pastebin, bro, bro logs, dns, nss key log file, sslkeylogfile, ssl key log file, tshark]
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

The zip file contains a series of bro logs, a packet capture, a PEM certificate, and a NSS Key Log file.

With the given files (especially with the __`bundle.pem`__ and __`secrets.log`__), the suspicious activity most likely lies within __HTTPS__ or __HTTP over SSL/TLS__ traffic.

---

## PART 3 : INITIAL ANALYSIS

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

There, indeed, is a lot of TLS and HTTP packets in the capture file.

Next is to eliminate who the actor for the suspicious activity might be.

```console
$ cat bro/dns.log | awk -F'\t' '{ printf "%s\t%s\n", $3, $5 }' | sort | uniq -c | egrep -e "\w\.\w*\."

  419 10.10.100.43	10.10.20.1
    8 10.10.20.13	10.10.20.1 

$ cat bro/dns.log | awk -F'\t' '$3 == "10.10.20.13" { printf "%s\t%s\n", $14, $10 }' | sort | uniq -c | sort -bnr

    3 A		pastebin.com
    3 AAAA	pastebin.com
    1 PTR	14.20.10.10.in-addr.arpa
    1 A		mysql-m1.prod.htb

```

__`10.10.20.1`__ seems to be the DNS server and what is weird is that __`10.10.20.13`__ has the same host identifier as the earlier mentioned server. Moreover, it made a request for __`pastebin.com`__ which is a common dumping grounds for exfiltrated data.

It may be wise to limit the search to __`10.10.20.13`__'s activity.

---

## PART 4 : GETTING THE FLAG

Since we were given an <strong style="color:orange">NSS Key Log File</strong> (__`secrets.log`__), the traffic must be encrypted and in order to view actual packet data, the __`-o 'tls.keylog_file:./secrets.log'`__ option should be used with __`tshark`__ or add the keylog file to the <strong style="color:orange">(Pre)-Master-Secret log filename</strong> in __`wireshark`__ under __`Edit`__ -> __`Preferences`__ -> __`Protocols`__ -> __`TLS`__.

<strong style="color:orange">NSS Key Log File</strong>

> Can be used by external programs to decrypt TLS connections. It follows the format: __`LABEL <space> ClientRandom <space> SECRET`__.
> <hr style="border-bottom:1px dotted #666"/>
> __`LABEL`__ : It describes the following secret.<br/>
> __`ClientRandom`__ : 32 random bytes encoded as 64 hexadecimal characters.<br/>
> __`SECRET`__ : Depending on the label (__`CLIENT_RANDOM`__ in this case wherein there are 48 bytes encoded 96 hexadecimal characters.)

Now to search for __`10.10.20.13`__'s activity limited to http since the challenge description points to problem with a web server:

```console
$ tshark -2 -R "ip.src==10.10.20.13 and http" -o 'tls.keylog_file:./secrets.log' -r chalcap.pcapng

  1 170.203546  10.10.20.13 → 104.20.208.21 HTTP 1804 POST /api/api_post.php HTTP/1.1  (application/x-www-form-urlencoded)
  2 186.485524  10.10.20.13 → 104.20.209.21 HTTP 1278 POST /api/api_post.php HTTP/1.1  (application/x-www-form-urlencoded)
  3 237.038819  10.10.20.13 → 104.20.208.21 HTTP 6855 POST /api/api_post.php HTTP/1.1  (application/x-www-form-urlencoded) 

```

There was a huge packet (with a size of __`6855`__) and viewing the data it contains:

```console
$ tshark -2 -R "ip.src==10.10.20.13 and http and frame.len==6855" -T fields -e http.file_data -o 'tls.keylog_file:./secrets.log' -r chalcap.pcapng

  api_user_key=ed67c1aec48d47270dd002d0baa29814&api_dev_key=bb8aa307a7d4b6073976149b65977bae&api_paste_private=2&api_option=paste&api_paste_code=IssuingNetwork,CardNumber\nAmerican Express,345806846723249\nAmerican Express,345390632937883\nAmerican Express,348537668979836\nAmerican Express,377053228050054\nAmerican Express,376583316960401\nAmerican Express,370728090418771\nAmerican Express,343089157698829\nAmerican Express,376783960099486\nAmerican Express,370925614011310\nAmerican Express,345655064666899\nAmerican Express,349526416252983\nAmerican Express,374137601650417\nAmerican Express,379459312870752\nAmerican Express,342002781858009\nAmerican Express,371548417517132\nAmerican Express,374215542017076\nAmerican Express,378061197392448\nAmerican Express,373623819098896\nAmerican Express,378714893017707\nAmerican Express,372204783826157\nAmerican Express,374543879869094\nAmerican Express,347256757140959\nAmerican Express,344113218649966\nAmerican Express,370438099582029\nAmerican Express,379074114959362\nAmerican Express,376214359658856\nAmerican Express,374392766168545\nAmerican Express,378120275674968\nAmerican Express,377653788608231\nAmerican Express,372228747692280\nAmerican Express,379712206774419\nAmerican Express,371170584736336\nAmerican Express,341821906223364\nAmerican Express,346031816502270\nAmerican Express,342388871615015\nAmerican Express,342297596567577\nAmerican Express,371116813447823\nAmerican Express,347275681898029\nAmerican Express,340159467728765\nAmerican Express,341291086603530\nAmerican Express,370154070448409\nAmerican Express,370945625943350\nAmerican Express,346669026997960\nAmerican Express,345555131951417\nAmerican Express,370679406346331\nAmerican Express,374039336944042\nAmerican Express,376358640457337\nAmerican Express,340489816646982\nAmerican Express,376988515894717\nAmerican Express,343938540360150\nAmerican Express,378753104699614\nAmerican Express,371067527561203\nAmerican Express,372071568257688\nAmerican Express,371298336467262\nAmerican Express,377742701779979\nAmerican Express,370606011245970\nAmerican Express,373298847804357\nAmerican Express,379386423260799\nAmerican Express,375746261865385\nAmerican Express,349236877420497\nAmerican Express,377277758621600\nAmerican Express,340515950981783\nAmerican Express,370380522063476\nAmerican Express,347840973813653\nAmerican Express,343732320743671\nAmerican Express,344856839404977\nAmerican Express,378553260917242\nAmerican Express,375171892130283\nAmerican Express,347077947108072\nAmerican Express,374065404228380\nAmerican Express,349572089871063\nAmerican Express,340873970916598\nAmerican Express,376501051822032\nAmerican Express,378635675028929\nAmerican Express,372262705444244\nAmerican Express,377327829524687\nAmerican Express,347637516705986\nHTB{Th15_15_4_F3nD3r_Rh0d35_M0m3NT!!}\nAmerican Express,343588840524078\nAmerican Express,375354542667439\nAmerican Express,342786650506356\nAmerican Express,376519541622051\nAmerican Express,372925141702629\nAmerican Express,379064920049805\nAmerican Express,372062866981368\nAmerican Express,340119293062854\nAmerican Express,377622183441043\nAmerican Express,345596477927538\nAmerican Express,346120357010486\nAmerican Express,348743175358502\nAmerican Express,348265083838326\nAmerican Express,374165182475318\nAmerican Express,343413470215022\nAmerican Express,377835450116425\nAmerican Express,343319576934756\nAmerican Express,349097271174704\nAmerican Express,343047062516676\nAmerican Express,347837794215977\nAmerican Express,377905537353414\nAmerican Express,343336645380480\nAmerican Express,349722904687745\nAmerican Express,379439377204840\nAmerican Express,371098010402175\nAmerican Express,341711119881514\nAmerican Express,379155339156478\nAmerican Express,346499893173952\nAmerican Express,379822410604029\nAmerican Express,378401969278765\nAmerican Express,376187523024900\nAmerican Express,371560862816232\nAmerican Express,374688712671981\nAmerican Express,346567385784039\nAmerican Express,349677499992027\nAmerican Express,378863874883072\nAmerican Express,370538962014776\nAmerican Express,378695319664554\nAmerican Express,377700801047184\nAmerican Express,341490109937152\nAmerican Express,375116305929698\nAmerican Express,376293550656281\nAmerican Express,376184934284512\nAmerican Express,370692215483682\nAmerican Express,341484791940103\nAmerican Express,341379048961417\nAmerican Express,374162791962349\nAmerican Express,370307175675108\nAmerican Express,349013931675378\nAmerican Express,347949547383489\nAmerican Express,342996616020703\nAmerican Express,349356556270045\nAmerican Express,346684782309441\nAmerican Express,379871086475610\nAmerican Express,345199109118715\nAmerican Express,340216820858984\nAmerican Express,349888469898835\nAmerican Express,346365151301637\nAmerican Express,378265272063804\nAmerican Express,349959481746698\nAmerican Express,348263119237951\nAmerican Express,373484474433864\nAmerican Express,377663560742140\nAmerican Express,370212530971871\nAmerican Express,376863650124206\nAmerican Express,373727306606895\nAmerican Express,344917353013352\nAmerican Express,341618870946529\nAmerican Express,349386219430900\nAmerican Express,378491822173402\nAmerican Express,377749742143933\nAmerican Express,343787312359902\nAmerican Express,342834615655924\nAmerican Express,373220167257297\nAmerican Express,342409875100604\nAmerican Express,374623961952105\nAmerican Express,342343248508898\nAmerican Express,370014624976364\nAmerican Express,370634519297087\nAmerican Express,378686083206003\nAmerican Express,345301479069094\nAmerican Express,341653062519404\nAmerican Express,344466041049600\nAmerican Express,340831124516177\nAmerican Express,371352670040878\nAmerican Express,376506773521960\nAmerican Express,373412041523057\nAmerican Express,371761796232138\nAmerican Express,372758692991600\nAmerican Express,375081018662582\nAmerican Express,379755239006424\nAmerican Express,379846246153760\nAmerican Express,371606808641125\nAmerican Express,348577292127113\nAmerican Express,374145045728368\nAmerican Express,347077718247133\nAmerican Express,340453378523583\nAmerican Express,344546944525481\nAmerican Express,377030750473656\nAmerican Express,371832335323686\nAmerican Express,348749016952684\nAmerican Express,373007620504443\nAmerican Express,376917237325536\nAmerican Express,345005318377549\nAmerican Express,346253765527997\nAmerican Express,349673285691824\nAmerican Express,379556545602579\nAmerican Express,344722223105333\nAmerican Express,349796314273585\nAmerican Express,344803589396672\nAmerican Express,372038817288624\nAmerican Express,343935624567445\nAmerican Express,342699774398016\nAmerican Express,377323872814232\nAmerican Express,377540985647023\nAmerican Express,347894643938739\nAmerican Express,379439395658019\nAmerican Express,376650833504747\nAmerican Express,343979751964728\nAmerican Express,377648365324335\nAmerican Express,377309456167584\nAmerican Express,347081651786503\nAmerican Express,347727257462630\nAmerican Express,344419972274507\nAmerican Express,370147246447792\nAmerican Express,375039789680878\nAmerican Express,346840335828432\nAmerican Express,346557187869278\nAmerican Express,340511052332744\nAmerican Express,378147342634378\nAmerican Express,347894225651353\nAmerican Express,377048863390823\nAmerican Express,378984721869708\nAmerican Express,376893345466290\nAmerican Express,340993435902015\nAmerican Express,345021743290579\nAmerican Express,372216617148053\nAmerican Express,345721594543956\nAmerican Express,370701456996490\nAmerican Express,378075075335832\nAmerican Express,347193033978698\nAmerican Express,378449242282864\nAmerican Express,347225645203899\nAmerican Express,374757600945979\nAmerican Express,342834096127575\nAmerican Express,347662201357208\nAmerican Express,343574247594591\nAmerican Express,370566322534167\nAmerican Express,372334356047228\nAmerican Express,344289113810802\nAmerican Express,348157167680627\nAmerican Express,378139627479017\nAmerican Express,341433918625899\nAmerican Express,375054585319852\nAmerican Express,375232023349653\nAmerican Express,371277165625117\nAmerican Express,375201533060415\nAmerican Express,370486975047062\nAmerican Express,345341443311941\nAmerican Express,370079377557471\nAmerican Express,348277553108999\nAmerican Express,348942096401546\nAmerican Express,340139468957183\nAmerican Express,375501135914772\nAmerican Express,348469770686390\nAmerican Express,372121835443015\nAmerican Express,342572197088771\nAmerican Express,349239713481020\nAmerican Express,379395776757541\nAmerican Express,377424909245976\nAmerican Express,346716240079230\nAmerican Express,342897267037956\nAmerican Express,372256457425906\nAmerican Express,347780418120357\nAmerican Express,345626501272781\nAmerican Express,348313982208785\nAmerican Express,377268832627986\nAmerican Express,348464633254247\nAmerican Express,345862988784051\nAmerican Express,372478188557829\nAmerican Express,346931472667467\nAmerican Express,376210287092911\nAmerican Express,349669214408298\nAmerican Express,349589127207480\nAmerican Express,373465045108259\nAmerican Express,345993581429677\nAmerican Express,379055189988279\nAmerican Express,342079255260219\nAmerican Express,372148370619824\nAmerican Express,341669065343451\nAmerican Express,343887050822002\nAmerican Express,375806364224144\nAmerican Express,341482592864373\nAmerican Express,343996994073075\nAmerican Express,348241530301408\nAmerican Express,340508494078869\nAmerican Express,341222588779064\nAmerican Express,341732458268378\nAmerican Express,342215785733206\nAmerican Express,375206484753587\nAmerican Express,348757630021869\nAmerican Express,375207977915915\nAmerican Express,378757965166902\nAmerican Express,371416072169864\nAmerican Express,371472284470210\nAmerican Express,344313444200085\nAmerican Express,371633951327088\nAmerican Express,373356508545394\nAmerican Express,346745901450190\nAmerican Express,375181398034764\nAmerican Express,348193944767049\nAmerican Express,379595687856023\nAmerican Express,347620188567868\nAmerican Express,371310095007468\nAmerican Express,378682000836261\nAmerican Express,374595741589813\nAmerican Express,370884641976377\nAmerican Express,371607107266291\nAmerican Express,377652257867146\nAmerican Express,376637079066374\nAmerican Express,345584266046595\nAmerican Express,340067183054384\nAmerican Express,341277850000334\nAmerican Express,341015814446098\nAmerican Express,342533390773452\nAmerican Express,376192394344189\nAmerican Express,343383111886624\nAmerican Express,374675072100834\nAmerican Express,348256685835653\nAmerican Express,372575544986608\nAmerican Express,376401373745583\nAmerican Express,342379126565899\nAmerican Express,346049017594391\nAmerican Express,373038486671992\nAmerican Express,343457158735405\nAmerican Express,340704529133239\nAmerican Express,377579823735301\nAmerican Express,374967588156800\nAmerican Express,372686112667320\nAmerican Express,341984840780285\nAmerican Express,373958109083988\nAmerican Express,371282587212338\nAmerican Express,371274146115201\nAmerican Express,375883096203118\nAmerican Express,347301054097666\nAmerican Express,343300721511053\nAmerican Express,340255289396029\nAmerican Express,375990362325374\nAmerican Express,343370733453560\nAmerican Express,342287408842862\nAmerican Express,348804061474645\nAmerican Express,371637510509326\nAmerican Express,378703796776774\nAmerican Express,349472306877482\nAmerican Express,344780438642987\nAmerican Express,378027734086116\nAmerican Express,346466146518556\nAmerican Express,343220729798991\nAmerican Express,378229907226962\nAmerican Express,374667417516923\nAmerican Express,343467230099563\nAmerican Express,349511258864699\nAmerican Express,349511141464095\nAmerican Express,370006599144259\nAmerican Express,377617826115186\nAmerican Express,379169502147297\nAmerican Express,373496044312105\nAmerican Express,377027560130781\nAmerican Express,374894851366082\nAmerican Express,349229238497916\nAmerican Express,372634070441056\nAmerican Express,375582667693786\nAmerican Express,375027644539694\nAmerican Express,346571317871203\nAmerican Express,373404070015592\nAmerican Express,342932357360933\nAmerican Express,378788416228850\nAmerican Express,346523832315760\nAmerican Express,346555775031558\nAmerican Express,377689619342913\nAmerican Express,372545677253019\nAmerican Express,378959598323203\nAmerican Express,348334757958008\nAmerican Express,348928076558314\nAmerican Express,343815776077452\nAmerican Express,371651434313657\nAmerican Express,373385669824926\nAmerican Express,377587129014446\nAmerican Express,349961591775088\nAmerican Express,377262527714142\nAmerican Express,374353905627247\nAmerican Express,344127718183706\nAmerican Express,370394640760004\nAmerican Express,342501026140156\nAmerican Express,371990240035645\nAmerican Express,344045629467283\nAmerican Express,372417880208372\nAmerican Express,376848472499589\nAmerican Express,348836111506778\nAmerican Express,341253206773262\nAmerican Express,379813062281463\nAmerican Express,340389988094393\nAmerican Express,348861999184142\nAmerican Express,378272683395502\nAmerican Express,378913030244634\nAmerican Express,371745098486450\nAmerican Express,347365349266279\nAmerican Express,341650305850257\nAmerican Express,345512937435434\nAmerican Express,345034766920956\nAmerican Express,376462350476477\nAmerican Express,370601311448960\nAmerican Express,378323147198691\nAmerican Express,372269640352689\nAmerican Express,349501478749697\nAmerican Express,346605935208784\nAmerican Express,347016994528519\nAmerican Express,370662025937227\nAmerican Express,377697725813677\nAmerican Express,349751884430099\nAmerican Express,373559452294766\nAmerican Express,347293629507818\nAmerican Express,346944733058632\nAmerican Express,346540195773088\nAmerican Express,377646253436773\nAmerican Express,378137477976348\nAmerican Express,371979298957057\nAmerican Express,347244087119885\nAmerican Express,370828135962682\nAmerican Express,344635944815370\nAmerican Express,371256715300140\nAmerican Express,379100809243737\nAmerican Express,340470483320994\nAmerican Express,376426496187447\nAmerican Express,374314125645476\nAmerican Express,348029280065251\nAmerican Express,375398240964424\nAmerican Express,379666458903185\nAmerican Express,345219721518272\nAmerican Express,349262935875001\nAmerican Express,372319583768886

$ echo -e $(tshark -2 -R "ip.src==10.10.20.13 and http and frame.len==6855" -T fields -e http.file_data -o 'tls.keylog_file:./secrets.log' -r chalcap.pcapng) | head

  api_user_key=ed67c1aec48d47270dd002d0baa29814&api_dev_key=bb8aa307a7d4b6073976149b65977bae&api_paste_private=2&api_option=paste&api_paste_code=IssuingNetwork,CardNumber
  American Express,345806846723249
  American Express,345390632937883
  American Express,348537668979836
  American Express,377053228050054
  American Express,376583316960401
  American Express,370728090418771
  American Express,343089157698829
  American Express,376783960099486
  American Express,370925614011310

$ echo -e $(tshark -2 -R "ip.src==10.10.20.13 and http and frame.len==6855" -T fields -e http.file_data -o 'tls.keylog_file:./secrets.log' -r chalcap.pcapng) | grep {

  HTB{Th15_15_4_F3nD3r_Rh0d35_M0m3NT!!}

```

There are a lot of __`American Express`__ numbers dumped to pastebin which is apparently the suspicious behaviour the challenge description pertains to. :)

---

<div style="width:100%;overflow-x:auto"><h2>FLAG : <strong>HTB{Th15_15_4_F3nD3r_Rh0d35_M0m3NT!!}</strong></h2></div>

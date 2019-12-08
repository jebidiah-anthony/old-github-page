---
title: PROJECTS
layout: menu
description: "Various manuals and proof of concepts I've created out of personal interest most of which in a Windows context."
tags: [projects, pass-the-ticket, double-hop, psremoting, evtx, custom logs, ecmangen, subscription, windows event forwarder, windows event collector, wec, wef, elastalerter, elastalert, elasticsearch, rules, cross origin resource sharing, cors, mubix]
---

## <span style="color:red">$ projects</span>

---

## >>[CORS for Dummies](./prjct/CORS.html)<<
> This is a brief introduction to __Cross Origin Resource Sharing__ along with common misconfigurations that might lead to exploitation. This was an entry to mubix's OSCP giveaway challenge 3. I did not win but I still really learned a lot which is still a great takeaway.

## >>[elastalerter.py](./prjct/elastalerter.html)<<
> An elastalert rule tester built using python. Tests could be set-up uniquely and could be run by batch. Specified logs are indexed using [__Elasticsearch 7.4.0__](https://www.elastic.co/downloads/past-releases/elasticsearch-7-4-0) and are used with a custom elastalert [alerter](https://github.com/jebidiah-anthony/elastalerter/blob/master/elastalerter/alerter.py). This program covers testing for single matches and log aggregation with field mapping capabilities. ([source code](https://github.com/jebidiah-anthony/elastalerter/blob/master/elastalerter.py))

## >>[Setting up a Windows Event Collector](./prjct/Windows-Event-Collector.html)<<
> This lays out how to create a sbuscription (both source and collector initiated) that collects selected forwarded __`.evtx`__  event logs from a workstation to a domain controller.

## >>[Creating Custom __*.evtx*__ Logfiles](./prjct/Custom-evtx-Logfiles.html)<<
> This shows the process of how to create custom __`.evtx`__ log files using __`ecmangen.exe`__ and other utilities present in the [__Windows Development Kit__](https://go.microsoft.com/fwlink/p/?LinkId=838916). The log file(s) created could be used as a destination log for forwarded events.

## >>[Pass-the-Ticket: PSRemoting Double-hop Bypass](./prjct/PTT-PSRemoting.html)<<
> The double-hop problem occurs when, for example, a local PowerShell instance connected via PSRemoting to a remote server which is connected to the target server and an attempt to execute commands on the target server was made and was rejected. The end goal of this proof-of-concept is to execute a pass-the-ticket attack on an active directory while being remotely connected to a domain computer with administrator privileges.


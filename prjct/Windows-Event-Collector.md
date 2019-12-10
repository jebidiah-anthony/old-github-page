---
layout: menu
title: Windows Event Collector
description: "This lays out how to create a sbuscription (both source and collector initiated) that collects selected forwarded .evtx event logs from a workstation to a domain controller."
tags: [windows, event manager, event viewer, event logs, windows logs, logs, windows event forwarder, windows event collector, subscription, evtx]
---

# <span style="color:red">Setting up a Windows Event Collector</span>

---

## __ENVIRONMENT:__

#### MACHINES:

<div style="overflow-x:auto">
  <table>
    <tr>
      <th>HOSTNAME</th>
      <th>MACHINE IP</th>
      <th>OS</th>
      <th>REMARKS</th>
    </tr>
    <tr>
      <td>MSEDGEWIN10</td>
      <td>192.168.150.128</td>
      <td>Windows 10 Enterprise Evaluation</td>
      <td>Source Machine</td>
    </tr>
    <tr>
      <td>WIN-BO2CT95INDP</td>
      <td>192.168.150.133</td>
      <td>Windows Server 2016</td>
      <td>Collector Machine</td>
    </tr>
  </table>
</div>

- The <span style="color:orange">FQDN</span> for WIN-BO2CT95INDP is <span style="color:orange">__win-bo2ct95indp.bossmanben.local__</span>

---

## __ASSUMPTIONS:__

#### 1.  The Source Machine (MSEDGEWIN10) is part of a Domain Controller (WIN-BO2CT95INDP).

#### 2. This guide uses __*Security Logs*__ as an example.

#### 3. The steps below will create a subscription that collects __*Security logs*__ from the __Source Machine__ (MSEDGEWIN10).

---

## __PROCEDURE:__

### __i. Start the WinRM service__

1. Open __PowerShell__ on the Source Machine (MSEDGEWIN10):
   ```powershell
   winrm quickconfig
   ```
   - Add the Collector Machine to the Source Machine's trustedhosts:
     ```powershell
     Set-Item wsman:localhost/client/trustedhosts 192.168.150.133
     ```
   - Restart the service for changes to take effect:
     ```powershell
     Restart-Service WinRM
     ```

2. Check if the service is running:
   ```powershell
   winrm get winrm/config
   ```
   ```
   ...omitted...
           AllowRemoteAccess = true
       Winrs
           AllowRemoteShellAccess = true
   ...omitted...
   ```

   - `AllowRemoteAccess = true` signifies that the service is running.

   <span></span>

3. Test if the Collector Machine (BOSSMANBEN) is reachable using WinRM:
   ```powershell
   Test-WSMan WIN-BO2CT95INDP
   ```
   ```
   wsmid           : http://schemas.dmtf.org/wbem/wsman/identity/1/wsmanidentity.xsd
   ProtocolVersion : http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd
   ProductVendor   : Microsoft Corporation
   ProductVersion  : OS: 0.0.0 SP: 0.0 Stack: 3.0
   ```
   - WinRM is __enabled by default__ on Windows Server 2012 and up.
   - This is just a measure to check if the Collector Machine is indeed reachable.

<hr class="section-divider"/>

### __ii. Add the Collector Machine to the Event Log Readers groups__
<span style="height:10px"></span>
#### __In the Source Machine (MSEDGEWIN10):__

  1. Open the __Local Users and Groups__:
      
     - Press `Win` + `R` then enter `lusrmgr.msc`

     <span></span>

  2. Navigate to `Local Users and Groups (Local)` __>__ `Groups`:
      
     1. Right-click `Event Log Readers` and select `Properties`
     2. Select `Add...`

     <span></span>

  3. Select `Object Types...` then check the box, `Computers`

  4. `Enter the object names to select` -- "__*WIN-BO2CT95INDP*__"

     - Select `Check Names` for good measure.

  5. Select `OK` when done.

<hr class="section-divider"/>

### __iii. Create Subscriptions using Event Viewer__
<span style="height:10px"></span>
#### __In the Collector Machine (WIN-BO2CT95INDP):__

1. Open the __Event Viewer__:

   - Press `Win` + `R` then enter gpedit `eventvwr.msc`

2. On the left panel, right-click on `Subscriptions` then select `Create Subscription...`

   1. `Subscription Name` -- Remote Security Logs
   2. `Description` -- Security Logs from the Domain Computer, MSEDGEWIN10
   3. `Destination log` -- Forwarded Events
        
      - Custom logs could be created but `Forwarded Events` is selected by default.
      - Click [here](./Custom-evtx-Logfiles.html) to create custom logs.

   4. Select `Subscription type and source computers`:

      <span style="color:#b5e853">If you choose `Collector initiated`, then select `Select Computers...`</span>

      1. Select `Add Domain Computers...`
      2. `Enter the object name to select` -- "__*MSEDGEWIN10*__"
      3. Select `Check Names` for good measure.
      4. Select `OK`
      5. Select `Test` for good measure.
      6. Select `OK`

      <span style="color:#b5e853">For `Source initiated`, select `Select Computer Groups...` then do the following extra steps on the Source Machine</span>
            
      1. Press `Win` + `R` then enter `gpedit.msc`
               
         1. Navigate to `Computer Management` __>__ `Administrative Templates` __>__ `Windows Components` __>__ `Event Forwarding`
         2. Right-click on `Configure target Subscription Manager` then select `Edit`
         3. Choose `Enabled`
         4. Under `Options`, beside `SubscriptionManagers`, press `Show...`
         5. Enter `Server= http://win-bo2ct95indp.bossmanben.local:5985 /wsman/SubscriptionManager/WEC, Refresh=30`
         6. Press `OK`
         7. Press `OK`

      2. Open __PowerShell__ or __cmd__ the run `gpupdate /force`

      <span style="color:#b5e853">For `Source initiated`, do the following on the Collector Machine (WIN-BO2CT95INDP)</span>

      1. Open __PowerShell__ or __cmd__ then run `wecutil quick-config`         

   5. Select `Select Events...`:

      1. `Logged` -- "__*Any time*__"
      2. `Event level` -- __*Critical*__, __*Error*__, __*Information*__, __*Warning*__
      3. Choose `By log` -- __*Windows*__ -> __*Security*__
      4. Filter __Event IDs__ -- 4624, 4657, 4688, 4698, 4720, 4722, 4724, 4732, 4738, 4769
      5. Select `OK`
   
   6. Select `Advanced...`:
         
      1. `User Account` -- Choose `Machine Account`
      2. `Event Delivery Optimization` -- Choose `Minimize Latency`
      3. Select `OK`

      <div style="overflow-x:auto">
        <table>
          <tr>
            <th>OPTION</th>
            <th>DESCRIPTION</th>
            <th>INTERVAL</th>
          </tr>
          <tr>
            <td>Normal</td>
            <td>Does not conserve bandwidth</td>
            <td>15 minutes via pull delivery</td>
          </tr>
          <tr>
            <td>Minimize Bandwidth</td>
            <td>Bandwidth for delivery is controlled</td>
            <td>6 hours via push delivery</td>
          </tr>
          <tr>
            <td>Minimize Latency</td>
            <td>Delivery with minimal delay</td>
            <td>30 seconds via push delivery</td>
          </tr>
        </table>
      </div>

   7. Select `OK`

3. Right-click on the newly created subscription then select `Runtime Status`:

   ```
   [MSEDGEWIN10.bossmanben.local] - Error - Last retry time: 7/17/2019 8:27:52 PM. 
   Code (0x138C): <f:ProviderFault provider="Event Forwarding Plugin" path="C:\Windows\system32\wevtfwd.dll" 
   ```

#### <span style="text-decoration:none">__In the Source Machine (WIN-BO2CT95INDP)__</span>

1. Run `wevtutil`:
   ```powershell
   wevtutil get-log Security
   ```
   ```
   name: Security
   enabled: true
   type: Admin
   owningPublisher:
   isolation: Custom
   channelAccess: O:BAG:SYD:(A;;0xf0005;;;SY)(A;;0x5;;;BA)(A;;0x1;;;S-1-5-32-573)
   logging:
     logFileName: %SystemRoot%\System32\Winevt\Logs\Security.evtx
     retention: false
     autoBackup: false
     maxSize: 20971520
   publishing:
     fileMax: 1
   ```

2. Add the __Network Service Account__ (S-1-5-20) to the `channelAccess` field:
   ```powershell
   wevtutil set-log Security /ca:"O:BAG:SYD:(A;;0xf0005;;;SY)(A;;0x5;;;BA)(A;;0x1;;;S-1-5-32-573)(A;;0x1;;;S-1-5-20)"
   ```
   - WinRM runs under the __*Network Service Account*__ which had no access to the __Security Logs__

#### <span style="text-decoration:none">__Going back to the Collector Machine (WIN-BO2CT95INDP)__</span>

  1. Go to the __Event Viewer__:

     - Press `Win` + `R` then enter gpedit `eventvwr.msc`

  2. On the left panel, go to `Subscriptions` then select the recently created subscription

  3. On the right panel, under the __*subscription name*__, select `Retry`

  4. Right-click on the recently created subscription then select `Runtime Status`:
     ```
     [MSEDGEWIN10.bossmanben.local] - Active - : No additional status.
     ```
     - An Event with __ID 100 (Name="SubscribeSuccess")__ will appear on __*Microsoft-Windows-Event-ForwardPlugin/Operational*__ in the Source Machine (MSEDGEWIN10)

<hr class="section-divider"/>

### __iv. Wait for logs to be sent to the Forwarded Events logs__

__NOTE(S)__:
- TImestamps are preserved
- Log contents are preserved

---

## __REFERENCES:__

```
- https://www.vkernel.ro/blog/how-to-configure-windows-event-log-forwarding?fbclid=IwAR1bQ9VpgL--PWaqvEWcJBduR3xJ2UnBBhZmO7UGef-NXcKN9PCINZ3gmQ0
- https://www.itprotoday.com/strategy/q-what-are-some-simple-tips-testing-and-troubleshooting-windows-event-forwarding-and?fbclid=IwAR3ceGoJU-jgkD2U_rVo2FmQee5M0spvE85lZRVw0FHv4YFTphLaX-5JJe8
- https://rockyprogress.wordpress.com/2011/12/04/security-event-log-collection-from-a-domain-controller/?fbclid=IwAR01Puy9Wvr4eCQeV828raqfLesYJwVTw_8EAmDgvJIKYBVWoaT3giv24PA
- https://blogs.technet.microsoft.com/supportingwindows/2016/07/18/setting-up-a-source-initiated-subscription-on-an-event-collector-computer/?fbclid=IwAR2JagIePrComWaIcZknK_92Igakb4_jvnrmJJnGpZlFGnms_2PM7z6trJc
```

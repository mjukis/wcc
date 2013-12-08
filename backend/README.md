WCC backend service 
===================

Capabilities, both __required__ and desired
-----
*   __Server, capable of running on a Raspberry Pi__
    *   __Should be default store for peer-to-peer messages__
    *   __Hosts an IRC style chat system__
    *   __Hosts a twitter style chat system__
    *   __Hosts a email style comm system__
    *   __Stores Radio logs__
    *   __Stores Postal logs__
    *   BBS style message board
    *   Graceful reloading of updated components without lost connections
*  User database
   *  Identifies unique users with encrypted passwords
   *  Each client able to add users while connected to server
      *  When user is added, user data is created on the server
   *  Each user able to login from any client while connected to server
      *  After first login, user credentials are downloaded to client
      *  Subsequent logins can be handled by client when offline
*  Client able to connect via ad-hoc WiFi, WiFi DHCP access point or wired DHCP router

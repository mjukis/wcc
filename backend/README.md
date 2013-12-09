WCC backend service 
===================

Server backend
-----
*  Capable of running under Ubuntu (static location)
*  Capable of running on a Raspberry Pi (event locations)
*  Maintains user database
   *  Handles requests to add and delete users
   *  Distributes password hashes of users who have been authorized on individual client
*  Hosts main database (default store) for data being passed between clients
*  Hosts BBS style message board
*  Hosts WCC Library
*  Graceful reloading of updated components without lost connections

Client backend
-----
*  Recieves user input from frontend applications and stores it in database
*  Provides data to frontend in response to frontend requests
*  Handles requests for data from Internet sources
*  Synchronizes local database with server to propagate messages
*  Detects incoming messages and informs frontend about events
*  Authenticates users with encrypted passwords
*  Able to connect via ad-hoc WiFi mesh, WiFi DHCP access point or wired DHCP router
   *  User selects mode in settings

Future ideas
-----

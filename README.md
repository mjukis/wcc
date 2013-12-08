WCC  
===  
  
Wasteland Communication Corp software  
  
Capabilities, both __required__ and desired 
-----
*   __Server, capable of running on a Raspberry Pi__
    *   https://github.com/mjukis/wcc/tree/master/backend
*   __Multiple clients, capable of running on a Raspberry Pi__
    *   __GUI emulates mostly functioning terminal__
    *   __Uses RabbitMQ to gather user input and deliver it to server/other clients__
    *   __Capable of working offline and storing messages until connected__
    *   __Capable of Peer-to-Peer messaging when server is offline__
        *   Capable of mesh networking via other clients
    *   __Has multiple "apps"__
        *   __Verify username and password__
        *   __Postal Log w viewer/editor__
        *   __Radio Log w viewer/editor__
            *   Real-time Internet functions when available
        *   Radiotelegram Input Form
        *   __Single room group chat (Like an IRC channel)__
        *   __Instant Messaging with recipient (Like Twitter)__
        *   __Long form messaging with recipient (Like email)__
            *   Ability to send and recieve emails via system
        *   BBS style message board   
        *   Forced program updating

Client design
-----
*   Basics
    *   Machine with 15" or smaller TFT screen, running 1024x768 resolution minimum
    *   Upon powerup, boots automatically with no visual cues into WCC software
    *   No local shell access
*   Networking
    *   Will autoconfigure networking and enter VPN via Ethernet port DHCP
    *   Will allow user to configure WLAN SSID/pwd via WCC software, and will enter VPN via WLAN DHCP
    *   Will mesh with other nodes and enter VPN via mesh
    *   These modes selectable via settings


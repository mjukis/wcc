WCC  
===  
  
Wasteland Communication Corp software  

System requirements
-----
*   Python 2.7.6+
    *   Libraries:
        *   curses
        *   tornado (pip install tornado)
        *   psutil (apt-get install python-psutil)
        *   couchdb (pip install couchdb)
*   CouchDB (apt-get install couchdb)
*   xwindows
*   cool-retro-term and QT5 (sudo apt-get install build-essential qmlscene qt5-qmake qt5-default qtdeclarative5-dev qtdeclarative5-controls-plugin qtdeclarative5-qtquick2-plugin libqt5qml-graphicaleffects qtdeclarative5-dialogs-plugin qtdeclarative5-localstorage-plugin qtdeclarative5-window-plugin)
  
Capabilities, both __required__ and desired 
-----
*   1024x768 display
*   Emulates look of old terminal
    *   Simulates display issues (loss of tracking, blur etc)
*   Asynchronous
    *   Ability to take user input
    *   Ability to display updates (clock, incoming messages etc) simultaneously
*   Screensaver
*   Multiple "apps"
    *   Login Screen (with ability to log out and in again)
    *   Postal Log w viewer/editor
    *   Radio Log w viewer/editor
        *   Real-time Internet functions when available (QRZ.com lookup, distance and bearing to station)
    *   Radiotelegram Input Form
    *   Single room group chat (Like an IRC channel)
    *   Instant Messaging with recipient (Like Twitter)
    *   Long form messaging with recipient (Like email)
    *   BBS style message board
    *   PDF viewer

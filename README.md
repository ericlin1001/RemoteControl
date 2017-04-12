# RemoteControl
A remote control software, https://github.com/ericlin1001/RemoteControl

# How does it work?
* 1.Share screen, by send real-time screenshot to client.
* 2.Remote control the server computer, by sending the same mouse or keyboard command to the server computer, i.e. a mouse click in client will be sent to the server side, and the server side will perform the exactly action.
* 3.Well, it's currently just a semi-finished product. Since only some mouse action and some keys command are supported. To extend it to fully functions as remote desktop, it's not hard, just needs some work.

# What does it support now?
* Real-time screen capturing in LAN.
* Mouse and keyboard synchronizing
* Highlighting mouse click position

# TODO::
1. Server side:
* [ ]Allow mutiple client to connect.
* [ ]Decently deal with failure.
* [ ]Implement login, better image compression (predictive encoding), etc.

2. Client side:
* [ ]Make it portable to other platforms, e.g. Windows, Android, etc..

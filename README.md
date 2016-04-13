#RemoteControl

#What's it?
---
A simple program like remote desktop.

#How does it work?
---
* 1.Share screen, by send real-time screenshot to client.
* 2.Remote control the server computer, by sending the same mouse or keyboard command to the server computer, i.e. a mouse click in client will be sent to the server side, and the server side will perform the exactly action.
* 3.Well, it's currently just a semi-finished product. Since only some mouse action and some keys command are supported. To extend it to fully functions as remote desktop, it's not hard, just needs some work.

#TODO::
---
Server side:
* To allow more than 1 client to connect.
* If a client fails, correctly deal with this.
* Need to implement functions: login, better image compression(Like predictive encoding)

---
Client side:
* Make it portal to any platform....

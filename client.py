#!/usr/bin/python3
import  threading
import clientServer
from PyQt5 import  * 
from PyQt5.QtGui import  * 
from PyQt5.QtCore import  * 
from PyQt5.QtWidgets import  * 


class MyScrollArea(QScrollArea):
#class MyLabel(QLabel):
    def setC(self, c):
        self.c = c;
    def keyPressEvent(self, e):
        key = e.key();
        if key>= 65 and key<= 90:
            key = key+ 32;
        key = chr(key);
        self.c.send('keyDown,' + key);
        print('keyDown', key);

    def keyReleaseEvent(self, e):
        key = e.key();
        if key>= 65 and key<= 90:
            key = key+ 32;
        key = chr(key);
        self.c.send('keyUp,' + key);
        print('keyUp', key);

    def mouseMoveEvent(self, e):
        x = e.x();
        y = e.y();
        w, h = 1920, 1080
        if x<0 or y<0 or x>w or y>h:return;
        self.c.send('mouseMove,' + str(x) + ',' + str(y));
        print('mousemove' , e.x(), e.y());

    def mouseReleaseEvent(self, e):
        x = e.x();
        y = e.y();
        w, h = 1920, 1080
        if x<0 or y<0 or x>w or y>h:return;
        self.c.send('mouseUp,' + str(x) + ',' + str(y));
        print('mouseUp' , e.x(), e.y());

    def mousePressEvent(self, e):
        x = e.x();
        y = e.y();
        w, h = 1920, 1080
        if x<0 or y<0 or x>w or y>h:return;
        self.c.send('mouseDown,' + str(x) + ',' + str(y));
        print('mouseDown' , x, y);
    
class ShowImage(QObject):
    sender = pyqtSignal(bytes);
    def __init__(self, c):
        super(ShowImage, self).__init__();
        w, h = 1920, 1080
        label = QLabel();
        #label = MyLabel();
        label.setScaledContents(True);
        #sa = QScrollArea();
        sa = MyScrollArea();
        sa.setMouseTracking(True);
        sa.setC(c);
        #label.setC(c);
        sa.setWidget(label);
        sa.setWindowTitle('Eric remove Desktop');
        sa.resize(w, h);
        sa.show();
        self.label = label
        self.sa = sa;

    def connect(self):
        self.sender.connect(self.showData);
        
    def showImageEmit(self, data):
        self.sender.emit(data);

    def showData(self, data):
        b = QByteArray();
        b.append(data);
        img = QPixmap()
        img.loadFromData(b, 'JPEG')
        self.label.setPixmap(img);
        self.label.adjustSize();

class updateScreenThread(threading.Thread):
    isEnd = False;
    def stop(self):
        self.isEnd = True;
    def setP(self, c, s):
        self.c = c;
        self.s = s;

    def run(self):
        c = self.c;
        while not self.isEnd:
            mess = c.recv()
            args = mess.split(',');
            if args[0] != 'screen':
                print("Error: recv>", args);
            type = args[1]
            size = int(args[2])
            data = c.recvRaw(size);
            self.s.showImageEmit(data);

def init():
    app = QApplication([]);
    c = clientServer.Client();
    s = ShowImage(c);
    s.connect();
    us =  updateScreenThread();
    us.setP(c, s);
    us.start();
    app.exec_();
    us.stop();
    us.join();

init();

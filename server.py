#!/usr/bin/python3
import pyautogui, socket,  threading
from PyQt5.QtGui import  * 
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QBuffer, QByteArray, QIODevice
import clientServer

class GrabScreen():
    def getMouseXY(self):
        p = QCursor.pos();
        return p.x(), p.y();

    def __init__(self):
        self.app  =  QApplication([])
        self.screen = self.app.primaryScreen();
        self.sid = QApplication.desktop().winId();

    def getScreenAsData(self, quality = 20):
        ss = self.screen.grabWindow(self.sid);
        #b = ss.toImage().mirrored(True, True);
        #ss.convertFromImage(b);
        painter = QPainter();
        painter.begin(ss);
        painter.setBrush(QColor( 255,0,  0))
        size = 8;
        half_size = size / 2;
        cx, cy = self.getMouseXY();
        painter.drawEllipse(cx - half_size, cy - half_size, size,size);
        painter.end();
        #
        bytesArray = QByteArray();
        buff = QBuffer(bytesArray);
        ss.save(buff, 'JPEG', quality = quality)
        data = bytesArray.data();
        return data;


class SendScreenThread(threading.Thread):
    isEnd = False;
    def __init__(self, c):
        super(SendScreenThread, self).__init__();
        self.c = c;

    def stop(self):
        self.isEnd = True
    def run(self):
        s = GrabScreen();
        while (not self.c.isFail) and (not self.isEnd):
            data = s.getScreenAsData();
            self.c.send('screen,jpg,'  + str(len(data)));
            self.c.sendRaw(data);


def execute(order):
    args = order.split(',');
    mess = args[0];
    if mess.startswith('key'):
        key = args[1]
        if mess.endswith('Down'):
            pyautogui.keyDown(key);
        else:
            pyautogui.keyUp(key);
    elif mess.startswith('mouse'):
        x = int(args[1])
        y = int(args[2])
        if mess.endswith('Down'):
            pyautogui.mouseDown(x, y);
        elif mess.endswith('Up'):
            pyautogui.mouseUp(x, y);
        else:
            pyautogui.moveTo(x, y);
    else:
        print("Error:mess=", args);

def init():
    pyautogui.FAILSAFE = False;
    pyautogui.PAUSE = 0;
    pyautogui.MINIMUM_SLEEP = 0;
    pyautogui.MINIMUM_DURATION = 0;
    server = clientServer.Server();
    while 1:
        server.accept();
        sendScreenThread= SendScreenThread(server);
        sendScreenThread.start();#sending screen.
        while not server.isFail:
            order = server.recv()
            execute(order);
            print('order>', order);
        print('Client disconnected!');
        sendScreenThread.stop();
        sendScreenThread.join();
        
init();
#test();

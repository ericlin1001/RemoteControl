#!/usr/bin/python3
import  socket, time

class Tic():
    last = 0;
    def tic(self, s = 'Tic:'):
        current =time.time();
        sub = current - self.last;
        self.last = current;
        print(s, sub);
        return sub;

def getPort(isIncrement = False):
    f = open('a.txt');
    id = int(f.read());
    f.close();
    if isIncrement:
        id = id + 1;
        f = open('a.txt', 'w');
        f.write(str(id))
        f.close();
    return id;

class Server():
    client = None;
    isFail = False;
    def sendRaw(self, mess):
        if self.isFail:return;
        try:
            self.client.send(mess);
        except:
            self.isFail = True;

    def send(self, mess = '', end = '\n'):
        if self.isFail:return;
        try:
            self.client.send((mess + end).encode());
        except:
            self.isFail = True;

    def old_recv(self, delim = '\n'):
        data = ''
        c = self.client;
        r = c.recv(1);
        if r is None:
            return '';
        r = r.decode()
        while 1:
            data = data + r;
            r = c.recv(1);
            if r is None:
                break;
            r = r.decode()
            if r == delim or r  == '\0':
                break;

    def fail(self):
        self.isFail = True;
        print('Error:fail');

    def recv(self, delim = '\n'):
        if self.isFail:return '';
        data = '';
        try:
            c = self.client;
            r = c.recv(1);
            if r is None:
                self.fail();
                return '';
            r = r.decode()
            while 1:
                data = data + r;
                r = c.recv(1);
                if r is None:
                    self.fail();
                    return ''
                    break;
                r = r.decode()
                if r == delim or r  == '\0':
                    break;
        except:
            self.fail();
        return data
    def recvRaw(self, size):
        data = b"";
        if self.isFail:return b'';
        try:
            while len(data)<size:
                t = self.client.recv(size - len(data));
                data = data + t;
        except:
            self.isFail = True;
        return data;

    def __init__(self):
        self.s = socket.socket();
        #host = '172.18.219.99'
        host = ''
        self.port = port = getPort(True);
        self.s.bind((host, port))
        print('listening port', port);
        self.s.listen(4);

    def accept(self):
        print('waiting...');
        self.client, addr = self.s.accept();
        print('recv from ', self.client);
        self.isFail = False;
        return self.client;


class Client():
    def sendRaw(self, mess):
        self.client.send(mess);

    def send(self, mess = '', end = '\n'):
        self.client.send((mess + end).encode());

    def recv(self, delim = '\n'):
        c = self.client;
        r = c.recv(1);
        if r is None:
            return '';
        r = r.decode()
        data = '';
        while 1:
            data = data + r;
            r = c.recv(1);
            if r is None:
                break;
            r = r.decode()
            if r == delim or r  == '\0':
                break;
        return data
    def recvRaw(self, size):
        data = b"";
        while len(data)<size:
            t = self.client.recv(size - len(data));
            data = data + t;
        return data;

    def __init__(self, host = '172.18.219.99'):
        self.s = socket.socket();
        #host = '172.18.219.99'
        self.port = port = getPort();
        print('connect to host, port',host,  port);
        self.s.connect((host, port))
        self.client = self.s;


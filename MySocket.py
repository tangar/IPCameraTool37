import datetime
import socket
import threading

class RxSocket:
    def __init__(self,  host = '', port = 9998, callback = None):
        self.Host = host
        self.Port = port
        self.Rxsocket = None
        self.isReady = False
        self.t = None
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()
        self.timeout = 100
        self.Callback = callback
        
    def Open(self, host = '', port = 9998):
        try:
            self.Host = host
            self.Port = port        
            self.Rxsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.Rxsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.Rxsocket.bind((self.Host, self.Port))
            self.isReady = True
        except:
            self.isReady = False

    def recvfrom(self, len = 4096):
        if(self.isReady):
            return self.Rxsocket.recvfrom(4096)
        
    def _reader(self):
        event = threading.Event()
        while True:
            event.wait(0.01)
            try:
                if (self.isReady):
                    data, address = self.recvfrom(4096)

                    if(self.Callback):
                        self.Callback(data, address)
            
            except Exception:
                current_dateTime = datetime.datetime.now()
                print(f"Failed, exception was thrown")

class TxSocket:
    def __init__(self, name = '', port = 9999):
        self.Name = name
        self.Port = port
        self.isReady = False
        self.TxSocket = None

    def Open(self, host = '', port = 9998):
        try:
            self.Host = host
            self.Port = port        
            self.TxSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Адрес и порт получателя
            self.addressTx = (self.Host, self.Port)
            self.isReady = True
        except:
            self.isReady = False

    def Send(self, data):
        if(self.isReady):
            try:
                self.TxSocket.sendto(data, self.addressTx)
            except:
                self.isReady = False
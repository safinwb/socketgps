from operator import index
import sys
import socket
import serial
from time import sleep
from threading import Thread


# Enter Server Information - Note we are the server
UDP_IP     = "0.0.0.0"
UDP_PORT   = 8080
bufferSize  = 1024

# udpThread Class initiates thread for UDP, this proccess connections 
# and sends data.
class udpThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        #variables
        self.clients = []
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.settimeout(0.1)
        self.sock.bind((UDP_IP, UDP_PORT))    #Server Binding
        self.start()
        print("UDP Thread started")
        
    def run(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                if not search(self.clients, addr):
                    self.clients.append(addr)
                    clientIP  = "New Connection from: {}".format(addr)
                    print(clientIP)
            except:
                pass

            sleep(0.1)
    
    def txData(self, msg, address):
        try:
            self.sock.sendto(str(msg + '\0').encode('utf-8'), (address))
        
        except:
            print(msg)
            print(address)
            print("Something went wrong with Network")

    def txClients(self, data):
            if len(self.clients):
                #print(self.clients)
                for x in self.clients:
                    self.txData(data, x)



class relayThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.ser = serial.Serial('/dev/ttyUSB0', baudrate = 115200)
        print(self.ser.name)
        self.cnxns = udpThread()
        self.start()
        print("Serial Thread started")
        
    def run(self):
        while True:
            try:
                x = self.ser.readline()
            except:
                self.cnxns.txClients("Serial Device ERROR")

            #Sepreate Try/Except to filter some shit out dw
            try:
                self.cnxns.txClients(str(x.decode('utf-8')))
            except:
                pass


def main():
    gpsRcv = relayThread()
    print("Program is running")
    while True:
        sleep(1)

def search(list, item):
    for i in range(len(list)):
        if list[i] == item:
            return True
    return False

if __name__=="__main__":
    print(""" _______  _______  _______  ___   _  _______  _______  _______ 
|       ||       ||       ||   | | ||       ||       ||       |
|  _____||   _   ||       ||   |_| ||    ___||    _  ||  _____|
| |_____ |  | |  ||       ||      _||   | __ |   |_| || |_____ 
|_____  ||  |_|  ||      _||     |_ |   ||  ||    ___||_____  |
 _____| ||       ||     |_ |    _  ||   |_| ||   |     _____| |
|_______||_______||_______||___| |_||_______||___|    |_______|

--------------- One way to get ya'll some GPS -----------------
""")
    main()

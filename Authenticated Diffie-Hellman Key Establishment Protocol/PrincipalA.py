import socket
import data_and_utils as utils
from random import randrange as rr
import hashlib
import hmac
from os import system                           # required for setting the name of terminal window

name = "Principal A"
system("title "+name)

class keys:
    def __init__(self):
        # existing (old) shared secret key with principal B (used for authentication)
        self.sec_keyB = "d1ab6f59ae0b6860f3c426f7c060ce524ed020ee29eb5b87d377f8a06646047a"

    def init_keys(self):
        """initialize Diffie-Hellman private & public keys"""
        self.priv_key = rr(1,utils.n+1)
        self.pub_key = utils.pt_multiply(self.priv_key, utils.G)
        self.pub_key = "".join(map(utils.intToPaddedHex, self.pub_key))

    def MACB(self, msg):
        """generating MAC of msg using secret key shared with B"""
        mac_key = bytes(self.sec_keyB, "utf-8")
        msg = bytes(msg, "utf-8")
        mac = hmac.new(mac_key, msg, hashlib.sha256).hexdigest()
        return mac
    
    def authenticateB(self, msg, rec_mac):
        """authenticates the message received from B"""
        mac = self.MACB(msg)
        return mac == rec_mac

    def newKeyB(self, msg):
        """calculate new key (x-coordinate of resultant point)"""
        recv = [utils.toInt(msg[:64]), utils.toInt(msg[64:])]
        new_key = utils.pt_multiply(self.priv_key, recv)
        self.sec_keyB = utils.intToPaddedHex(new_key[0])
        return self.sec_keyB

    def resetKeys(self):
        """reset Diffie-Hellman private & public keys"""
        self.priv_key = rr(1,utils.n+1)
        self.pub_key = utils.pt_multiply(self.priv_key, utils.G)
        self.pub_key = "".join(map(utils.intToPaddedHex, self.pub_key))

#initializing keys
K = keys()
K.init_keys()                                                       # initialize EC Diffie-Hellman Keys

# socket creation
s = socket.socket()
s.bind(("localhost",49175))
s.listen(5)

print("Waiting for connection")

while True:
    try:
        #connecting with other principal
        c, addr = s.accept()
        pr_name = c.recv(1024).decode()
        print("\nConnected with", addr, "(", pr_name, ")")

        print("\nEstablishing new shared secret key.")

        msg = str(K.pub_key)                                        # message is the public key of A
        mac = K.MACB(msg)                                           # generate MAC
        AtoB = bytes(msg+mac,"utf-8")                               # concatenate message with MAC, then convert to byte stream 
        c.send(AtoB)                                                # send message
        
        BtoA = c.recv(1024).decode()                                #receive message from B

        if len(BtoA) != 2*utils.hlen + 64:                          # validate message length
            raise Exception("ERROR: Corrupted Message Received")

        # authenticate message received from B
        rec_mac = BtoA[-64:]
        rec_msg = BtoA[:-64]
        if not K.authenticateB(rec_msg, rec_mac):
            raise Exception("Cannot authenticate received message")
        print("\nMessage from B to A Authenticated Successfully!")

        # continue only if authentication is successful

        # calculating new key
        T = utils.Timer()
        new_keyB = K.newKeyB(rec_msg)                               # x-coordinate of generated point
        time_ = T.lap()
        
        print("\nGENERTATED KEY (In hexadecimal notation):")        # print generated key
        print(new_keyB)

        print("\nTime requred to compute key:", time_, "ms")

        c.close()

        print("\nConnection closed with", addr, "(", pr_name, ")")

    except Exception as E:
        print()
        print(E)

        # close connection if still connected
        try: c.close()
        except: pass

        print("Connection Terminated.")

    finally: 
        print("\n" + "--"*33 + "\n" + "--"*33)
        print("\nWaiting for new connection")

        # uncomment following line to generate new Diffie-Hellman private-public key for each connection
        #K.init_keys() 

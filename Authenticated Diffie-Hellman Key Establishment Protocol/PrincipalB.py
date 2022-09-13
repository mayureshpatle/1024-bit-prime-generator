import socket
import data_and_utils as utils
from random import randrange as rr
import hashlib
import hmac
from os import system                           # required for setting the name of terminal window

name = "Principal B"
system("title "+name)

class keys:
    def __init__(self):
        # existing (old) shared secret key with principal A (used for authentication)
        self.sec_keyA = "d1ab6f59ae0b6860f3c426f7c060ce524ed020ee29eb5b87d377f8a06646047a"

    def init_keys(self):
        """initialize Diffie-Hellman private & public keys"""
        self.priv_key = rr(1,utils.n+1)
        self.pub_key = utils.pt_multiply(self.priv_key, utils.G)
        self.pub_key = "".join(map(utils.intToPaddedHex, self.pub_key))

    def MACA(self, msg):
        """generating MAC of msg using secret key shared with A"""
        mac_key = bytes(self.sec_keyA, "utf-8")
        msg = bytes(msg, "utf-8")
        mac = hmac.new(mac_key, msg, hashlib.sha256).hexdigest()
        return mac
    
    def authenticateA(self, msg, rec_mac):
        """authenticates the message received from A"""
        mac = self.MACA(msg)
        return mac == rec_mac

    def newKeyA(self, msg):
        """calculates new key (x-coordinate of resultant point)"""
        recv = [utils.toInt(msg[:64]), utils.toInt(msg[64:])]
        new_key = utils.pt_multiply(self.priv_key, recv)
        self.sec_keyA = utils.intToPaddedHex(new_key[0])
        return self.sec_keyA

    def resetKeys(self):
        """reset Diffie-Hellman private & public keys"""
        self.priv_key = rr(1,utils.n+1)
        self.pub_key = utils.pt_multiply(self.priv_key, utils.G)
        self.pub_key = "".join(map(utils.intToPaddedHex, self.pub_key))


try:
    #initialize keys
    K = keys()
    K.init_keys()                                               # initialize EC Diffie-Hellman Keys

    #socket creation
    c = socket.socket()

    #connect to principal A
    print("Establishing Connection.")
    c.connect(("localhost", 49175))
    c.send(bytes(name, "utf-8"))
    print("\nConnection Established Successfully.")

    AtoB = c.recv(1024).decode()                                # reveive message from A

    if len(AtoB) != 2*utils.hlen + 64:                          # validate message length
        raise Exception("ERROR: Corrupted Message Received")

    # authenticate message received from A
    rec_mac = AtoB[-64:]
    rec_msg = AtoB[:-64]
    if not K.authenticateA(rec_msg, rec_mac):
        raise Exception("Cannot authenticate received message")
    print("\nMessage from A to B Authenticated Successfully!")

    # continue only if authentication is successful
    msg = str(K.pub_key)                                        # message is the public key of B
    mac = K.MACA(msg)                                           # generate MAC
    BtoA = bytes(msg+mac,"utf-8")                               # concatenate message with MAC, then convert to byte stream 
    c.send(BtoA)                                                # send message


    # calculating new key
    T = utils.Timer()
    new_keyA = K.newKeyA(rec_msg)                               # x-coordinate of generated point
    time_ = T.lap()
    
    print("\nGENERTATED KEY (In hexadecimal notation):")        # print generated key
    print(new_keyA)

    print("\nTime requred to compute key:", time_, "ms")
    
    
except Exception as E:
    print()
    print(E)

    #close connection if still connected
    try: c.close()
    except: pass

    print("\nConnection Terminated.")

finally:
    print("\nPress Enter to Exit this Process/Close this Window")

input()
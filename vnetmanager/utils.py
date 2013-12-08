from datetime import datetime
import socket
import struct
import random

def now():
    return datetime.utcnow()

def ipToInteger(ipAddr):
    return struct.unpack("!I", socket.inet_aton(ipAddr))[0]

def integerToIp(intIpAddr):
    return socket.inet_ntoa(struct.pack("!I", intIpAddr))


def generateMAC():
    macInteger = random.getrandbits(48)
    macInteger  = macInteger | (1<<42)
    macInteger = macInteger & int('111111101111111111111111111111111111111111111111',2)
    macString = str(hex(macInteger))
    blocks = [macString[x:x+2] for x in xrange(0, len(macString), 2)]
    macFormatted = ':'.join(blocks)
    macFormatted = macFormatted.rstrip("-L").lstrip("0x-")
    return macFormatted.rstrip('-:').lstrip(':-')

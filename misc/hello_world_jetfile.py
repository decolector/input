#!/usr/bin/python

from socket import *
from JetFileII import Font
from JetFileII import Animate
from JetFileII import Format
from JetFileII import Date
from JetFileII import Message
displayMsg = Message.DisplayControlWithoutChecksum

import re

#currently static values for my display
groupAddr = 1
unitAddr = 1
widthPixels = 120
heightPixels = 7

text = '{red}{7x6}{randomin}{randomout}Hello{nl}World{nl}JetFile{nl}'
print text
msg = displayMsg.Create(1,text=text);
print msg

s = socket(AF_INET, SOCK_STREAM)
addr = ("192.168.1.105", 9520)

s.connect(addr)
s.send(msg)
s.close()
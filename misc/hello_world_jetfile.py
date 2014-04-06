#!/usr/bin/python

from socket import *

from JetFileII import Message, Animate
displayMsg = Message.DisplayControlWithoutChecksum

import re

#currently static values for my display
groupAddr = 1
unitAddr = 1
widthPixels = 120
heightPixels = 7


pausa = Animate.Pause.Seconds(0)
print pausa

text = '{red}{7x6}{moveleftin}{moveleftout}{slowest}{pause}Hola Mundo cruel que me haces trabajar tanto y ganar tan pocp, pero todo sea por el arte :,('
print text
msg = displayMsg.Create(1,text=text);
print msg

s = socket(AF_INET, SOCK_STREAM)
addr = ("192.168.1.105", 9520)

s.connect(addr)
s.send(msg)
s.close()
#!/usr/bin/python

import os
import sys
import time
from datetime import datetime
import re
from threading import Thread, Timer
import socket
import logging
logging.basicConfig()
import requests as req
from apscheduler.scheduler import Scheduler
import xml.etree.ElementTree as ET
import requests

from JetFileII import Font
from JetFileII import Animate
from JetFileII import Format
from JetFileII import Date
from JetFileII import Message


class LedDisplay(Thread):
    def __init__(self, addr, port):
        super(LedDisplay, self).__init__()
        Thread.__init__(self)
        self.displayMsg = Message.DisplayControlWithoutChecksum
        self.addr = addr
        self.port = port
        #configure display
        #currently static values for my display
        self.groupAddr = 1
        self.unitAddr = 1
        self.widthPixels = 120
        self.heightPixels = 7
        self.msg = None

    def createMessage(self, text):
        self.msg = self.displayMsg.Create(1, text=text)

    def run(self):

        #create connection with display
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
            s.connect((self.addr, self.port))

            #send message and close connection
            print "Sending message to screen"
            s.send(self.msg)
            s.close()
            print "Message sent to screen, now waiting for next db hit"

        except socket.timeout:
            print ' Timed out, error sending message to sign, trying later.'


message = LedDisplay('192.168.1.101', 9520)
text = '{red}{7x6}{slowest}{moveleftin}{moveleftout}{left}{left}{pause}' + 'cuerpo' + ' > (' + 'author' + ')                        '
message.createMessage(text) 
message.start()








# import requests

# host = "https://api.mongohq.com/databases/vital/collections/messages/documents"
# key = '6pnomhzb6yre2nifkc4u'
# limit = 10
# heads = {'content-type': 'application/json'}


# params = {'_apikey': key, 'sort': '{"date":-1}', 'limit': 100}
# res = requests.get(host, headers=heads, params=params)

# msgs = []
# actualBatch = 0

# if res.status_code != 200:
#     print "Error in response: " + res.text
# else:
#     totalMessages = res.headers['X-Mongohq-Count']

#     for row in res.json():
#         msgs.append(row)

#     for i in range(len(msgs), int(totalMessages), 100):
#         res = requests.get(host, headers=heads, params={'_apikey': key,
#                                                         'sort': '{"date":-1}',
#                                                         'limit': 100,
#                                                         'skip': i})
        
#         for row in res.json():
#             msgs.append(row)

#     print len(msgs)
#                 
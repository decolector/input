# -*- coding: utf-8 -*-
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
        #self.msg = self.displayMsg.Create(1, text=text)
        self.msg = Message.WriteText(text, disk_partition='D', file_label='A')

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


def filterChars(words):
    """
    This function replaces non ASCII chars with __
    to avoid sending special characters to the sign
    """

    ns = "".join((c if ord(c) < 128 else '_' for c in words))
    return ns


def insertExtAscii(words):
    """
    Returns a string with a {extascii} tag inserted before every extended ascii char
    """
    ns = ""
    for char in words:
        if ord(char) < 128:
            ns += '{extascii}' + char
        else:
            ns += char
    return ns



def getMessages(host, key, limit):
    print "query database"

    heads = {'content-type': 'application/json'}
    params = {'_apikey': key, 'sort': '{"date":-1}', 'limit': limit}
    res = requests.get(host, headers=heads, params=params)

    msgs = []

    if res.status_code != 200:
        print "Error in response: " + res.text
    else:
        totalMessages = res.headers['X-Mongohq-Count']


        for row in res.json():
            msgs.append(row)

#        for i in range(len(msgs), int(totalMessages), 100):
#            res = requests.get(host, headers=heads, params={'_apikey': key,
#                                                            'sort': '{"date":-1}',
#                                                            'limit': limit,
#                                                            'skip': i})
#            
#            for row in res.json():
#                msgs.append(row)

    return msgs

def writeToScreen(host, key, limit, batch, time_message, display_addr, display_port):

    docs = getMessages(host, key, limit)

    for i in range(0, len(docs), batch):
        text = ''
        print 'Batch: %s to %s' %(i, i+batch-1)

        for o in range(i, i+batch-1):
            doc = docs[o]
            if 'author' in doc and 'body' in doc:
                author = filterChars(doc['author'].encode('utf-8', 'ignore'))
                body = filterChars(doc['body'].encode('utf-8', 'ignore'))

                print "message: %s >  %s" % (body, author)
                line = '{red}{7x6}{slowest}{moveleftin}{moveleftout}{left}{left}{pause} %s > (%s)                        ' % (body,author)
                text += line

        message = LedDisplay(display_addr, display_port)
        message.createMessage(text) 
        message.start()

        time.sleep(batch*time_message)


def main():
    """
    Read configuration
    """

    config_file = "config.xml"

    xml = ET.parse(config_file)
    HOST = xml.find('host').text
    DB_NAME = xml.find('db_name').text
    ENDPOINT = xml.find('endpoint').text
    DISPLAY_ADDR = xml.find("display_addr").text
    DISPLAY_PORT = int(xml.find('display_port').text)
    SECONDS = int(xml.find('seconds').text)
    LIMIT = int(xml.find('limit').text)
    KEY = xml.find('key').text
    BATCH_TIME = int(xml.find('batch_time').text)

    print "Starting permitidorayar ..."

    #HOST = HOST_NAME + DB_NAME + ENDPOINT
    print HOST, DB_NAME, DISPLAY_ADDR, DISPLAY_PORT

    while True: 
        time_message = 15
        writeToScreen(HOST, KEY, LIMIT, 10, time_message, DISPLAY_ADDR, DISPLAY_PORT)

    # # Start the scheduler
    # sched = Scheduler()

    # # Schedule job_function to be called every two hours
    # sched.add_interval_job(readData, seconds=SECONDS, args=[HOST, DISPLAY_ADDR, DISPLAY_PORT, LIMIT, KEY], start_date=datetime.now())
    # sched.start()

    #try:
    #    while True:
    #        time.sleep(0.1)
    #except KeyboardInterrupt:
    #    print "terminating"
    #    sched.shutdown()


if __name__ == "__main__":
    main()

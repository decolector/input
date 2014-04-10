#!/usr/bin/python

import os
import sys
import time
from datetime import datetime
import re
from threading import Thread, Timer
from socket import *
import logging
logging.basicConfig()
import couchdbkit
from apscheduler.scheduler import Scheduler
import xml.etree.ElementTree as ET

from JetFileII import Font
from JetFileII import Animate
from JetFileII import Format
from JetFileII import Date
from JetFileII import Message




class LedDisplay():
	"""Class to manage a led sign"""

	def __init__(self, db_host, db_name, display_addr, display_port, endpoint):

		#super(LedDisplay, self).__init__()
		#Thread.__init__(self)
		self.displayMsg = Message.DisplayControlWithoutChecksum
		self.addr = display_addr
		self.port = display_port
		#configure display
		#currently static values for my display
		self.groupAddr = 1
		self.unitAddr = 1
		self.widthPixels = 120
		self.heightPixels = 7
		self.msg = None
		self.dbserver = couchdbkit.Server(db_host)
		self.db = self.dbserver.get_or_create_db(db_name)
		self.endpoint = endpoint

	def sendMessage(self, text):
	 	self.msg = self.displayMsg.Create(1,text=text)
		#create connection with display
		s = socket(AF_INET, SOCK_STREAM)

 		s.connect((self.addr,self.port))
		#send message and close connection
		print "Sending messsage to display"
		s.send(self.msg)
		s.close()



	def query(self):
			
		text = ''
		print 'Hitting database...'
		for doc in self.db.all_docs( limit=5, descending=False, include_docs=True):
			author = doc['doc']['author']
			body = doc['doc']['body']
			print 'message: ', body, ' by ', author
			linea = '{red}{7x6}{slowest}{moveleftin}{moveleftout}{left}{left}{pause}' + body + ' > (' + str(author) + ')                         '
			text += linea

		
		print "Message built"
		self.sendMessage(text)



def main():

	config_file = "config.xml"
	xml = ET.parse(config_file)
	HOST_NAME = xml.find('host_name').text
	DB_NAME = xml.find('db_name').text
	DISPLAY_ADDR = xml.find("display_addr").text
	DISPLAY_PORT = int(xml.find('display_port').text)
	ENDPOINT = xml.find("endpoint").text
	SECONDS = int(xml.find("seconds").text)
	USERNAME = xml.find("username").text
	PASSWORD = xml.find("password").text

	HOST = 'http://'+ USERNAME+ ':'+ PASSWORD + '@'+ HOST_NAME

	print "starting ..."
	
	#print HOST, DB_NAME, DISPLAY_ADDR, DISPLAY_PORT
	#readData(HOST, DB_NAME, DISPLAY_ADDR, DISPLAY_PORT)
	display = LedDisplay(HOST, DB_NAME, DISPLAY_ADDR, DISPLAY_PORT, ENDPOINT)
	# Start the scheduler
	sched = Scheduler()

	sched.add_interval_job(display.query, seconds=SECONDS )
	sched.start()

	try: 
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		print "terminating"
		sched.shutdown()


if __name__ == "__main__":
	main()

	#configure http client
	#base_url = "https://decolector.iriscouch.com/messages/"
	#url =  base_url + '_all_docs'
	#text = '{red}{7x6}{randomin}{randomout}Hello{nl}World{nl}JetFile{nl}'



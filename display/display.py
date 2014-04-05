#!/usr/bin/python

import os
import time
from datetime import datetime
import re
from threading import Thread, Timer
from socket import *
import requests as req
from apscheduler.scheduler import Scheduler

from JetFileII import Font
from JetFileII import Animate
from JetFileII import Format
from JetFileII import Date
from JetFileII import Message



class LedDisplay(Thread):
	"""Class to manage a led sign"""

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
	 	self.msg = self.displayMsg.Create(1,text=text)



	def run(self):
		#create connection with display
		s = socket(AF_INET, SOCK_STREAM)

 		s.connect((self.addr,self.port))
		#send message and close connection
		s.send(self.msg)
		s.close()


def readData(host, db_name, display_addr, display_port):
		#Timer(10, readData(host, db_name, display_addr, display_port))
		#get the data
		ops = {'limit':'5', 'include_docs':'true', 'descending':'true'}
		heads = {'content-type':'application/json'}
		url = host + db_name + "/_all_docs"
		res = req.get(url, headers=heads, params=ops)
		print res
		
		#create message
		text = ''
		tmp = res.json()
		rows = tmp['rows']
		for row in rows:
			body = row['doc']['body']
			auth = row['doc']['author']
			linea = '{red}{7x6}{randomin}{randomout}' + str(auth) + " dice: " + body + '{nl}'
			text += linea

		print "Message text : ", text

		message = LedDisplay(display_addr, display_port)
		message.createMessage(text)
		message.start()


def main():
	HOST = "https://decolector.iriscouch.com/"
	DB_NAME = "messages"
	DISPLAY_ADDR = "192.168.1.105"
	DISPLAY_PORT = 9520
	print "starting ..."
	readData(HOST, DB_NAME, DISPLAY_ADDR, DISPLAY_PORT)

	# Start the scheduler
	sched = Scheduler()


	# Schedule job_function to be called every two hours
	sched.add_interval_job(readData, minutes=1, args = [HOST, DB_NAME, DISPLAY_ADDR, DISPLAY_PORT])
	sched.start()

	try: 
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		print "terminating"
		sched.shutdown()


if __name__ == "__main__":
	main()

'''
class MessageReader(Thread):
	"""MessageReader reads messages from the web"""
	def __init__(self, host, db_name):
		super(MessageReader, self).__init__()
		Thread.__init__(self)
		self.host = host
		self.db_name = db_name

	def run(self):
		#get the data
		ops = {'limit':'5', 'include_docs':'true', 'descending':'false'}
		heads = {'content-type':'application/json'}
		url = self.host + self.db_name + "/_all_docs"
		res = req.get(url, headers=heads, params=ops)
		print res
		
		#create message
		text = ''
		tmp = res.json()
		rows = tmp['rows']
		for row in rows:
			msg = row['doc']['body']
			auth = row['doc']['author']
			linea = '{red}{7x6}{randomin}{randomout}' + str(auth) + " dice: " + msg + '{nl}'
			text += linea

		print text


		print msg

'''
	#configure http client
	#base_url = "https://decolector.iriscouch.com/messages/"
	#url =  base_url + '_all_docs'
	#text = '{red}{7x6}{randomin}{randomout}Hello{nl}World{nl}JetFile{nl}'



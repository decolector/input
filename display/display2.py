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
	 	self.msg = self.displayMsg.Create(1,text=text)

	def run(self):

		#create connection with display
		#s = socket(AF_INET, SOCK_STREAM)

 		#s.connect((self.addr,self.port))
		#send message and close connection
		#print "Sending messsage"
		#s.send(self.msg)
		#s.close()
		print "Message sent, now waiting for next db hit"



def filterChars(words):
	"""
	This function replaces non ASCII chars with __ 
	to avoid sending special characters to the sign
	"""

	ns = "".join((c if ord(c) < 128 else '_' for c in words))
	return ns


def readData(host, display_addr, display_port, limit, key):
		# #Timer(10, readData(host, db_name, display_addr, display_port))
		# #get the data
		# ops = {'limit':limit, 'sort':{'date': -1}}
		# heads = {'content-type':'application/json'}
		# url = host
		# res = req.get(url, params=ops)

		#print "Response from server: " + res.text
		
		#create message
		text = ''
		#build the request

		params = {'_apikey': key, 'sort': '{"date":-1}', 'limit': limit}
		res = requests.get(host, params = params)
	
		tmp = res.json()
		#print res.text
		
		if res.status_code != 200:
			print "Error in response:" + res.text



		else:
			print "succesfully aquired data from db"
			rows = tmp

			for row in rows:
				body = filterChars(row['body'].encode("utf-8"))
				author = filterChars(row['author'].encode("utf-8"))
				print "mensaje: " + body + " by: " + author
				linea = '{red}{7x6}{slowest}{moveleftin}{moveleftout}{left}{left}{pause}' + body + ' > (' + str(author) + ')                        ' 
				text += linea

			print "Message built"
			message = LedDisplay(display_addr, display_port)
			message.createMessage(text)	
			message.start()

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

	print "starting ..."

	#HOST = HOST_NAME + DB_NAME + ENDPOINT
	print HOST, DB_NAME, DISPLAY_ADDR, DISPLAY_PORT

	# Start the scheduler
	sched = Scheduler()

	# Schedule job_function to be called every two hours
	sched.add_interval_job(readData, seconds=SECONDS, args = [HOST, DISPLAY_ADDR, DISPLAY_PORT, LIMIT, KEY], start_date = datetime.now())
	sched.start()

	try: 
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		print "terminating"
		sched.shutdown()


if __name__ == "__main__":
	main()

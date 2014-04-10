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
		print "Sending messsage"
		s.send(self.msg)
		s.close()
		print "Message sent, now waiting for next db hit"


def readData(host, display_addr, display_port, limit):
		# #Timer(10, readData(host, db_name, display_addr, display_port))
		# #get the data
		# ops = {'limit':limit, 'sort':{'date': -1}}
		# heads = {'content-type':'application/json'}
		# url = host
		# res = req.get(url, params=ops)

		#print "Response from server: " + res.text
		
		#create message
		text = ''
		#linea = '{red}{7x6}{slow}{moveleftin}{moveleftout}Esto es una prueba de animacion{nl}'
		params = {'_apikey': '6pnomhzb6yre2nifkc4u', 'sort': '{"date":-1}', 'limit': limit}
		res = requests.get('https://api.mongohq.com/databases/vital/collections/messages/documents', params)
	
		tmp = res.json()
		#print res.text
		
		if res.status_code != 200:
			print "Error in response, trying later ..."

		else:
			print "succesfully aquired data from db"
			rows = tmp

			for row in rows:
				body = row['body'].encode("utf-8")
				author = row['author'].encode("utf-8")
				print "mensaje: " + body + " by: " + author
				#linea = '{red}{7x6}{slow}{moveleftin}{moverightout}' + body + '  (' + str(auth) + ') '
				linea = '{red}{7x6}{slowest}{moveleftin}{moveleftout}{left}{left}{pause}' + body + ' > (' + str(author) + ')                        '
				
				text += linea

			#print "Message text : ", text
			print "Message built"
			message = LedDisplay(display_addr, display_port)
			message.createMessage(text)	
			message.start()



def main():

	config_file = "config.xml"
	xml = ET.parse(config_file)
	HOST_NAME = xml.find('host_name').text
	DB_NAME = xml.find('db_name').text
	ENDPOINT = xml.find('endpoint').text
	DISPLAY_ADDR = xml.find("display_addr").text
	DISPLAY_PORT = int(xml.find('display_port').text)
	SECONDS = int(xml.find('seconds').text)
	LIMIT = int(xml.find('limit').text)

	print "starting ..."

	HOST = HOST_NAME + DB_NAME + ENDPOINT
	print HOST, DB_NAME, DISPLAY_ADDR, DISPLAY_PORT

	# Start the scheduler
	sched = Scheduler()

	# Schedule job_function to be called every two hours
	sched.add_interval_job(readData, seconds=SECONDS, args = [HOST, DISPLAY_ADDR, DISPLAY_PORT, LIMIT])
	sched.start()

	try: 
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		print "terminating"
		sched.shutdown()


if __name__ == "__main__":
	main()



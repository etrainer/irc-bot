#!/usr/bin/env python

import sys
import socket
import string
import argparse
import time

class ircbot():

	def __init__(self, host, port, channel, name, log):
		self.HOST = host
		self.PORT = port
		self.CHANNEL = channel
		self.NICK = name
		self.IDENT = name
		self.REALNAME = name
		self.LOG = log

		try:
			#Try to connect
			self.irc = socket.socket()
			self.irc.connect((self.HOST, self.PORT))
			print("Connected to %s\n" % self.HOST)

			self.irc.send(("NICK %s\r\n" % self.NICK).encode())
			self.irc.send(("USER %s %s bla :%s\r\n" % (self.IDENT, self.HOST, self.REALNAME)).encode())
			self.irc.send(("JOIN %s\r\n" % self.CHANNEL).encode())
			print("Joined %s as %s\n" % (self.CHANNEL, self.NICK))
		
		except Exception as e:
			#Something went wrong
			#print the error message
			print(e)
			sys.exit(1)
	def run(self):
		"""
			This is the main application loop
		"""
		
		print("Logging ...\n")
		#create a variable to dump log information into
		readbuffer = ""

		#in an infinite loop read everything
		#strip out what we don't want
		#respond to any PINGs sent by the IRC server so it doesn't drop us!
		#write to the screen or the log file
		while True:
			readbuffer = readbuffer + decode(self.irc.recv(1024))
			#we don't need everything the server sends
			temp = readbuffer.split("\n")
			readbuffer = temp.pop()
			#step through each of the lines in the list
			for line in temp:
				#strip off trailing whitespace and split string into a list
				linex = line.rstrip()
				linex = linex.split()
				#when the IRC Server sends a ping, need to respond
				if (linex[0] == "PING"):
					self.irc.send(bytes("PONG %s\r\n" % linex[1]))
				else:
					now = time.strftime("(%Y-%m-%d %H:%M:%S)")
					#print to the screen or the log file
					if self.LOG == 'stdout':
						print(now + encode(line))
					else:
						with open(self.LOG, "a") as log:
							log.write(now + encode(line))

#we may see different character encodings
#do our best to handle the different types
def decode(bytes):
	try:
		text = bytes.decode('utf-8')
	except UnicodeDecodeError:
		try:
			text = bytes.decode('iso-8859-1')
		except UnicodeDecodeError:
			text = bytes.decode('cp1252')
	return text

def encode(bytes):
	try:
		text = bytes.encode('utf-8')
	except UnicodeEncodeError:
		try:
			text = bytes.encode('iso-8859-1')
		except UnicodeEncodeError:
			text = bytes.encode('cp1252')
	return text

def parseargs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--server',default='irc.freenode.net', help='DNS address of the IRC server. default=irc.freenode.net')
	parser.add_argument('-p', '--port', type=int, default=6667, help='port number of IRC server. default=6667')
	parser.add_argument('-c', '--channel', default='#linux', help='IRC channel to join. default=#linux')
	parser.add_argument('-n', '--name', default='Mandalorian', help='how the bot will be identified in the channel. default=Mandalorian')
	parser.add_argument('-o', '--output', default='stdout', help='file to write log to. default=stdout')
	return parser.parse_args()

if __name__ == '__main__':

	#get the options from the parser
	opt = parseargs()

	#create our bot and start running it
	bot = ircbot(opt.server, opt.port, opt.channel, opt.name, opt.output)
	bot.run()


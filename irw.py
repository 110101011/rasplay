#!/usr/bin/python

import socket
import threading
import logging, sys

now_key = "KEY_1"

SOCKPATH = "/var/run/lirc/lircd"
sock = None

initialized = False

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def init():
	global sock
	global initialized	
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	sock.connect(SOCKPATH)
	initialized = True
	logging.debug("Starting irw socket")

def next_key():
	global now_key
	while initialized == True:
		while True:
			data = sock.recv(128)
			data.strip()
			if data:
				break
		words = data.split()
		key = str(words[2])
		key = key.split("b'")[1]
		key = key.split("'")[0]
		now_key = key

class NextKey(threading.Thread):

        def __init__(self, function_next_key):
                threading.Thread.__init__(self)
                self.runnable = function_next_key
                self.deamon = True

        def run(self):
                self.runnable()


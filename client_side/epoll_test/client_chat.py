#!/usr/local/bin/python

import socket
import time
import threading
import signal

# global variables define here
#
INPUT_CONTENT = ""
IS_RUNNING = 0

# class define here
#
class MyinputThread(threading.Thread):
	''' a new thread to handle user input '''
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global INPUT_CONTENT
		global IS_RUNNING
		IS_RUNNING = 1
		while IS_RUNNING:		
			print "\n"
			INPUT_CONTENT = raw_input("(192.168.56.102):")
	def stop(self):
		global IS_RUNNING
		IS_RUNNING = 0

# global function define here
#
def signal_handle(signum, frame):
	global IS_RUNNING
	IS_RUNNING = 0
	myInputThread.stop()

# main function
#
if __name__ == "__main__":
	IS_RUNNING = 1
	signal.signal(signal.SIGINT, signal_handle)

	connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	connFd.connect(("192.168.56.101", 2003))
	connFd.settimeout(0.1)

	myInputThread = MyinputThread()
	myInputThread.start()

	while IS_RUNNING:
		client_content = INPUT_CONTENT
		if len(client_content) > 0 and connFd.send(client_content) != len(client_content):
		    print "connection lost"
		    break
		INPUT_CONTENT = ""
		try:
		    readData = connFd.recv(1024)
		except socket.timeout,e:
		    err = e.args[0]
		    if err == 'time out':
	                print "time out"
			readData = "time out"
		else:
		    print "\n" + "(192.168.56.101): " + readData
	connFd.close()

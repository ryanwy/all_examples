#!/usr/local/bin/python

import time
import threading
import signal

IsRunning = 0

class MyTestThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global IsRunning
		IsRunning = 1
		num = 0
		while IsRunning:
			print num
			num += 1
			time.sleep(1)
	def stop(self):
		global IsRunning
		IsRunning = 0
		print "we are about to stop"

def signal_handle(signum, frame):
	print "detect a interrupt signal" + str(signum)
	global thread
	thread.stop()

if __name__ == "__main__":
	thread = MyTestThread()
	thread.start()

	signal.signal(signal.SIGINT, signal_handle)
	print "test begin"
	while IsRunning:
		pass


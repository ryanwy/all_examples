#!/usr/local/bin/python

import threading
import time

class myTestThread(threading.Thread):
	''' Using class for thread test '''
	
	def __init__(self, threadId, threadName):
		threading.Thread.__init__(self)
		self.threadID = threadId
		self.threadName = threadName
	def run(self):
		print "We are runing now" + self.threadName
		if self.threadID == 1:
			test_thread(self.threadID, self.threadName)
		elif self.threadID == 2:
			test_thread2(self.threadID, self.threadName)
		print "running over"
	def stop(self):
	    pass	
def test_thread(countNum, threadName):
	while True:
		print threadName + " : " + str(countNum)
		countNum += 1
		time.sleep(1)

def test_thread2(countNum, threadName):
	print threadName + " : " + str(countNum)
	while True:
	    name = raw_input("please enter")


if __name__ == "__main__":
	thread1 = myTestThread(2, "t2")
	thread2 = myTestThread(1, "t1")
	thread1.start()
	thread2.start()
	#time.sleep(10)
	#thread1.stop()
	#thread2.stop()
	print "main exit"

#!/usr/bin/python

import sys
import thread
import time
import traceback

def test_thread(strname, num):
	print "thread" + strname
	while True:
		print strname + " : " + str(num)
		num = num + 1
	#time.sleep(1)

if __name__ == "__main__":
	print "now we start"
	try:
		thread.start_new_thread(test_thread, ('t1', 1));
		thread.start_new_thread(test_thread, ('t2', 2));
		#time.sleep(10)
	except Exception, e:
		print e
	else:
		name = raw_input("pls enter")
		thread.exit_thread()

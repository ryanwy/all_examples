#!/usr/bin/python

import socket
import time
 
if __name__ == "__main__":
	connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	connFd.connect(("192.168.56.101", 2003))
	for i in range(1, 11):
		data = "The Number is %d" % i
		if connFd.send(data) != len(data):
			break
		readData = connFd.recv(1024)
		print "test"
		if len(readData) > 0 :
		    print "data from server:" + readData
		else:
		    continue
		time.sleep(1)
	connFd.close()

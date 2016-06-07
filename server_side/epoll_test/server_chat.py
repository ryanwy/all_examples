#!/usr/local/bin/python

import socket
import select
import errno
import os
import sys
import time
import threading
import traceback
import signal
try:
    import fcntl
except ImportError:
    fcntl = None

# global varables define here
#
IS_RUNNING = 0
SERVER_INPUT = ""
CONNECTION_FD = None

# class define here
#
class ServerInput(threading.Thread):
	''' thread to handle write event '''
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global SERVER_INPUT
		global CONNECTION_FD
		global IS_RUNNING
		IS_RUNNING = 1
		while IS_RUNNING:
			SERVER_INPUT = raw_input("(192.168.56.101): ")
			content = SERVER_INPUT
			if len(content) > 0 :
				send_len = 0
				while True:
					try:
						global connections
						send_len += CONNECTION_FD.send(content)
					except Exception, e:
						print "error happen"
						traceback.print_exc()
						print e
					else:
						if(send_len == len(content)):
							break
						content = ""
						SERVER_INPUT = ""
	def stop(self):
		global IS_RUNNING
		IS_RUNNING = 0

# globla function here
def signal_handle(signum, frame):
	print "detect a signal" + str(signum)
	global IS_RUNNING
	IS_RUNNING = 0 
	server_input_thread.stop()


# main function
#
if __name__ == "__main__":
	server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
	server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_fd.bind(("0.0.0.0", 2003))
	server_fd.listen(10)
	epoll_fd = select.epoll()
	epoll_fd.register(server_fd.fileno(), select.EPOLLIN|select.EPOLLOUT)
	connections = {}
	addresses = {}
	datalist = {}
	client_addr = ""
	server_content = ""

	signal.signal(signal.SIGINT, signal_handle)
	# a new thread to handle output event
	#
	server_input_thread = ServerInput() 
	try:
		server_input_thread.start()
	except Exception, e:
		print e
	else:
		IS_RUNNING = 1

	# just use EPOLLIN to listen read event
	#
	while IS_RUNNING:
		epoll_list = epoll_fd.poll()
		for fd, events in epoll_list:
			if fd == server_fd.fileno():
				conn, addr = server_fd.accept()
				conn.setblocking(0)
				epoll_fd.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)
				connections[conn.fileno()] = conn
				addresses[conn.fileno()] = addr
				client_addr = addr
				flags = fcntl.fcntl(conn.fileno(), fcntl.F_GETFL)
				flags = flags | os.O_NONBLOCK
				fcntl.fcntl(conn.fileno(), fcntl.F_SETFL, flags)
				print "	Welcome our new guest: " + str(client_addr)
				CONNECTION_FD = conn
			elif select.EPOLLIN & events:
				datas = ''
				while True:
					try:
						data = connections[fd].recv(10)
						if not data and not datas:
							epoll_fd.unregister(fd)
							connections[fd].close()
							break
						else:
							datas += data
					except socket.error, msg:
						if msg.errno == errno.EAGAIN:
							print "error"
							datalist[fd] = datas
							break
						else:	
							print "connecting error"
							epoll_fd.unregister(fd)
							connections[fd].close()
							CONNECTION_FD = None
							break
					print "\n" + str(client_addr) + " : " + datas
			elif select.EPOLLHUP & events:
				print "unknown connect"
				epoll_fd.unregister(fd)
				connections[fd].close()
			else:
				continue
	else:
		for fd in connections:
			epoll_fd.unregister(fd)
			connections[fd].close() # close all connection
		CONNECTION_FD = None

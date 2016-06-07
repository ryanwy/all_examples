#!/usr/bin/python

import socket, select, errno

if __name__ == "__main__":
	server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
	server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_fd.bind(("0.0.0.0", 2003))
	server_fd.listen(10)
	epoll_fd = select.epoll()
	epoll_fd.register(server_fd.fileno(), select.EPOLLIN)
	connections = {}
	addresses = {}
	datalist = {}
	while True:
		epoll_list = epoll_fd.poll()
		for fd, events in epoll_list:
			print "event comes.."
			if fd == server_fd.fileno():
				print "new connect"
				conn, addr = server_fd.accept()
				conn.setblocking(0)
				epoll_fd.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)
				connections[conn.fileno()] = conn
				addresses[conn.fileno()] = addr
				print addr
			elif select.EPOLLIN & events:
				print "ready reading"
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
							print "data rev:" + datas
					except socket.error, msg:
						if msg.errno == errno.EAGAIN:
							print"data not ready now?" + datas
							datalist[fd] = datas
							epoll_fd.modify(fd, select.EPOLLET | select.EPOLLOUT)
							break
						else:	
							print "something wrong happened"
							epoll_fd.unregister(fd)
							connections[fd].close()
							break
			elif select.EPOLLHUP & events:
				print "unknown connect"
				epoll_fd.unregister(fd)
				connections[fd].close()
			elif select.EPOLLOUT & events:
				sendLen = 0     
				while True:
					print "sending.." + datalist[fd][sendLen:]
					sendLen += connections[fd].send(datalist[fd][sendLen:])
					if sendLen == len(datalist[fd]):
						break
				epoll_fd.modify(fd, select.EPOLLIN | select.EPOLLET)
			else:
				continue

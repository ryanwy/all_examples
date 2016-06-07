#!/usr/local/bin/python

"""
This is a test for twisted server
"""
import sys
from twisted.internet import reactor
from twisted.internet import stdio, protocol
from twisted.protocols import basic
from twisted.application import service, internet

class CmdPromptServer(basic.LineReceiver):
    delimiter = b'\n'
    def connectionMade(self):
        self.transport.write(">>>")
    
    def lineReceived(self, line):
        if 'quit' == line.strip('\n') or 'exit' == line.strip('\n'):
            myservice.stopService()
        try:
            if self.protocol_instance:
                self.protocol_instance.sendLine("Server: " + line + '\n')
            else:
                print "protocol instance null, skip"
            if self.output:
                try:
                    pass
                    #self.output.write(">>> \n")
                except Exception, e:
                    print e
            else:
                print "transport null"
                raise AttributeError
        except Exception, e:
            print "error occur"
            print e

    def connectionLost(self, reason):
        print "connection lost"

class ServerChatProtocol(basic.LineReceiver):

    def connectionMade(self):
        self.transport.write('connection made')
        self.factory.cmd.output = self.transport
        self.factory.cmd.protocol_instance = self
    
    def lineReceived(self, line):
        print line
        #self.sendLine('Server >>> ' + data)
        #self.transport.write('Server >>> ' + data)
    
    def connectionLost(self, reason):
        print "connection lost"

cmdprompt = CmdPromptServer()   
factory = protocol.ServerFactory()
factory.protocol = ServerChatProtocol
factory.cmd = cmdprompt
cmdprompt.factory = factory
cmdprompt.output = None
cmdprompt.protocol_instance = None
stdio.StandardIO(cmdprompt)
#reactor.listenTCP(8000,factory)
#reactor.run()
#if __name__ == "__main__":
application = service.Application("server")
myservice = internet.TCPServer(8000, factory)
myservice.setServiceParent(application)
'''
try: 
    pass
    #main()
except KeyboardInterrupt:
    print "Interrupt occur"
    sys.exit(0)
'''

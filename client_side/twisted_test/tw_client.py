#!/usr/local/bin/python

"""
This is just a test for twisted client
"""
import sys
from twisted.internet import reactor, protocol
from twisted.internet import stdio
from twisted.protocols import basic
from twisted.application import service, internet

HOST_IP_ADDR = "192.168.56.101" # host ip address to connect


class CmdPromptClient(basic.LineReceiver):
    """ Command prompt to handle standard input and output """
   
    delimiter = b'\n'
    def connectionMade(self):
        self.transport.write(">>>")
            
    def lineReceived(self, line):
        if 'quit'== line.strip('\n') or 'exit' == line.strip('\n'):
            #self.connectionLost(self)
            #sys.exit()
            myclient.stopService()
            
        try:
            self.factory.protocol_instance.sendLine("Client: " + line + '\n')
            #self.factory.protocol_instance.transport.write("\r\n" + " >>> ")
        except Exception, e:
            print "error occur"
            print e
            self.factory.protocol_instance.transport.loseConnection()
    def connectionLost(self, reason):
        print "connection lost"

class ClientChatProtocol(basic.LineReceiver):
    """ Use to send and receive message """

    def connectionMade(self):
        #self.factory.cmd.output = self.transport
        self.transport.write("connection made(cilent)")

    def lineReceived(self, line):
        print line
        #self.factory.cmd.sendLine(data)
    def connectionLost(self, reason):
        print "wow, connection lost"

class ClientChatFactory(protocol.ClientFactory):
    """ Chat protocol factory """
    
    protocol = ClientChatProtocol
    
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()
    
    def buildProtocol(self, addr):
        client_protocol = protocol.ClientFactory.buildProtocol(self, addr)
        self.protocol_instance = client_protocol
        return client_protocol

# this connects the protocol to a server running on port 8000
cmdprompt = CmdPromptClient()
stdio.StandardIO(cmdprompt)
f = ClientChatFactory()
cmdprompt.factory = f
#reactor.connectTCP(HOST_IP_ADDR, 8000, f)
#reactor.run()
application = service.Application("client")
myclient = internet.TCPClient(HOST_IP_ADDR, 8000, f)
myclient.setServiceParent(application)
"""
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Interruption occur"
        sys.exit(0)
"""

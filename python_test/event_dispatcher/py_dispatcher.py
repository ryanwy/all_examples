#!/usr/local/bin/python

from pydispatch import dispatcher

SIGNAL_IN_USE = 'signal-in-use'

# this is receiver to handle event
def handle_event(data):
    print 'event received:' + data


if __name__ == '__main__':
    # only specify sender is first
    dispatcher.connect(handle_event, signal = SIGNAL_IN_USE, sender = 'first')
    # send event use special sender    
    dispatcher.send(SIGNAL_IN_USE, 'first', 'hello first')
    dispatcher.send(SIGNAL_IN_USE, 'second', 'hello second') # cannot receive
    #m = dispatcher.getAllReceivers()
    #print m.next()


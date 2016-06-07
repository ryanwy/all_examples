#!/usr/local/bin/python

import os
try:
    import test_pb2
except Exception, e:
    print "import err"
    print e
    test_pb2 = None

def main():
    info = test_pb2.news()
    info.header = "Bigboom"
    info.news_id = 10001
    info.body = "Today is very special day"
    info.link = "www.bignews.com"

    info_serial = info.SerializeToString()
    print info_serial

    try: 
        if not os.path.isfile("pb_serial.txt"):
            f = open("pb_serial.txt", 'wb')
            f.write(info_serial)
            f.close()
        else:
            print "file exist"
            #f = open("pb_serial.txt", 'ab')
            #f.write(info_serial)
    except Exception, e:
        print e

    try:
        fr = open("pb_serial.txt")
        content = fr.read()
    except Exception, e:
        print e
    else:
        info.ParseFromString(content)
        fr.close()
        print info.header
        print info.news_id
        print info.body
        print info.link

if __name__ == '__main__':
    main()

import sys

def printadd():
    print "hello, add"

def printdivide():
    print "hello, divide"

def printmulti():
    print "hello, multi"

def printminus():
    print "hello, minus"

def execute():
    try:
        if len(sys.argv[1:]) == 0 or len(sys.argv[1:]) > 1:
            raise ValueError
            sys.exit(1)
        choice = int(sys.argv[1])
        if choice == 1:
            printadd()
        elif choice == 2:
            printdivide()
        elif choice == 3:
            printmulti()
        elif choice == 4:
            printminus()
        else:
            print "re-enter it"
    except ValueError:
        print "valueerror, re-enter it"
        sys.exit(1)

if __name__ == "__main__":
    execute()

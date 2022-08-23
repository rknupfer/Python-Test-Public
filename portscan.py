import socket
import subprocess
import sys
from datetime import datetime

#Blank your screen
subprocess.call('clear', shell=True)

#Ask for input
remoteServer = raw input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

#Print a nice banner with information on which host we are about to scan
print " " * 60
print "Please wait, scanning remote host", remoteServerIP
print " " * 60

#Check the date and time the scan was started
t1 = datetime.now()

#Using the range function to specify ports
#Also we will do error handling

try:
    for port in range (1,5000):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print "port {}:     Open".format(port)
        sock.close()

except KeyboardInterrupt:
    print "You pressed Ctrl+C"
    sys.exit()

except socket.gaierror:
    print "Couldn't connect to server"
    sys.exit()

#Checking time again
t2 = datetime.now

#Calculate the difference in time to know how long the scan took
total = t2 - t1

#fPrinting the information on the screen
print 'Scanning completed in" ', total






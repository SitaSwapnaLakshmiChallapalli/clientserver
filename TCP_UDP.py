#!/usr/bin/env python3

import socket
import threading
import sys


def scanneran(ip,port,protocol,mylst):
    if protocol=='tcp':
        scanner=socket.socket(socket.AF_INET,socket.SOCK_STREAM)                        #TCP connections
    else:
        scanner=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)                         #UDP connections

    scanner.settimeout(1)               #timeout to 1 second
    try:
        output=scanner.connect_ex((ip,port))            #Connecting to sepcified IP address and port number
        port_status='OPEN'                              #port status is 'OPEN'
        if output!=0:                                   #if output not equal to zero then port status is 'Closed'
            port_status='CLOSED'
        try:
            service=socket.getservbyport(port,protocol) #Retrieving the service name
        except:
            service='svc name unavailable'                      # If service name can/could not be determined then append to my_list
        mylst.append([port,port_status,service])

    except socket.gaierror:                                     
        if mylst[0]==0:
            print("Error: Host {} does not exist".format(ip))
        mylst[0]=1
        sys.exit()

    except KeyboardInterrupt:                                   #if user interrupts the program 
        print("Program interrupted by user.")
        sys.exit()


#arguments:( <hostname> <protocol> <portlow> <porthigh> )
if len(sys.argv)!=5:
    print("usage: ./Portscanner.py <hostname> <protocol> <portlow> <porthigh>")
    sys.exit()


#to check if the protocol can either be 'tcp' or 'udp'
if sys.argv[2] not in ['tcp','udp']:
    print("Invalid protocol:"+sys.argv[2]+".","Specify \"tcp\" or \"udp\"")
    print("usage: ./Portscanner.py <hostname> <protocol> <portlow> <porthigh>")
    sys.exit()

#entering the port numbers if port numbers are not entered print usage
try:
    sys.argv[3]=int(sys.argv[3])
    sys.argv[4]=int(sys.argv[4])

except:
    print("usage: ./Portscanner.py <hostname> <protocol> <portlow> <porthigh>")
    sys.exit()

#To check the port range
if sys.argv[3]<0 or sys.argv[4]>65535 or sys.argv[3]>sys.argv[4]:
    print("usage: ./Portscanner.py <hostname> <protocol> <portlow> <porthigh>")
    sys.exit()


mylst=[0]
port_low=sys.argv[3]
port_high=sys.argv[4]

print "scanning host = ",sys.argv[1]+" , ","protocol =",sys.argv[2]+",","ports:",str(sys.argv[3])+"->"+str(sys.argv[4])

# to print the service names that are open
for port in range(port_low,port_high+1):
    scanneran(sys.argv[1],port,sys.argv[2],mylst)

l=sorted(mylst[1:], key=lambda x: x[0])
for port in l:
    if port[1] == 'OPEN':
        print( "Port {0}:      port_status:{2}      Protocol:{3}    Service:{1}".format(port[0], port[2], port[1], sys.argv[2]))

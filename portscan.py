#!/usr/bin/python

# Copyright 2014 Simon Barth

import os
import sys
import socket
import string
import multiprocessing
from multiprocessing import Lock

def PORTscanner(IP, PORT, proc, lock):
    
    openPorts = []
    socket.setdefaulttimeout(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((IP, PORT))
    if result == 0:
        print "\033[1;32m[+] Port "+str(PORT)+": \t\t Open"
        openPorts.append(PORT)
    sock.close()
    
    filename = "/tmp/port"+str(IP)+":"+str(proc)
    fileHandle = open ( filename, 'w' )
    fileHandle.write (str(openPorts)) 
    fileHandle.close() 
    
def main():
    
    remoteServer = sys.argv[1]
    IP  = socket.gethostbyname(remoteServer)
    l = Lock()  
    proclist = []
    minimals = {}
    maximals = {}
    # Edit the following list to change to ports which will be scanned
    PORTs = [20, 21, 22, 23, 25, 53, 80, 110, 433, 587, 3389, 5222, 5223, 25565, 51413]
       
    print "\033[1;34m[*] Starting portscan on "+str(IP)+"... please wait"
    for n in range(14):
        PORT = PORTs[n]             
        process = multiprocessing.Process(target=PORTscanner, args=[IP, PORT, n, l])
        process.start()
        proclist.append(process)

if __name__ == "__main__":
    try:
        main()       
    except KeyboardInterrupt:
        print "\033[1;31m\n[-] You pressed Ctrl+C\n\x1b[0m\r"
        for process in proclist:
            process.terminate()
        sys.exit()
    print "\n\x1b[0m\r"

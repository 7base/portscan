#!/usr/bin/python

import os
import sys
import socket
import string
import multiprocessing
import subprocess
from multiprocessing import Lock

def IPscanner(IPmin, IPmax, proc, lock):
    
    onlineIPs = []
    offlineIPs = []
    for IP in range(IPmin, IPmax): 
        socket.setdefaulttimeout(1)
        IPcon = "87.156.144."+str(IP)
        try:
            socket.gethostbyaddr(IPcon)
            lock.acquire()
            print "\033[1;32m[+] "+str(IPcon)+" \tis available"
            lock.release()
            onlineIPs.append(IPcon)
        except:
            offlineIPs.append(IPcon)
    
    filename = "/tmp/ip"+str(proc)
    fileHandle = open ( filename, 'w' )
    if len(onlineIPs) > 0:
        fileHandle.write (str(onlineIPs)+"\n"+str(offlineIPs))
    else:
        fileHandle.write ( "\n"+str(offlineIPs) )   
    fileHandle.close() 
    
def main():
    
    l = Lock()  
    proclist = []
    minimals = {}
    maximals = {}
    IPtotal = 256
    
    IPpro = IPtotal/64
    minimal = 0
    maximal = IPpro
    print "\033[1;34m[*] Calculating process distribution\n"
    for n in range(64):
        minimals[n] = minimal
        maximals[n] = maximal
        minimal = minimal+IPpro
        maximal = maximal+IPpro
    
    print "[*] Starting scan... please wait"
    for n in range(64):
        IPmin = minimals[n]        
        IPmax = maximals[n]       
        process = multiprocessing.Process(target=IPscanner, args=[IPmin, IPmax, n, l])
        process.start()
        proclist.append(process)

if __name__ == "__main__":
    try:
        main()       
    except KeyboardInterrupt:
        print "\033[1;31m\n[-] You pressed Ctrl+C\n\x1b[0m\r"
        for process in proclist: # then kill them all off
            process.terminate()
        sys.exit()
    print "\n\x1b[0m\r"

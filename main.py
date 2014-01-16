#!/usr/bin/python

# Copyright 2014 Simon Barth

import os
import sys
import socket
import string
import subprocess
import datetime

def help():
    print "\033[1;33m\nPython Portscanner V0.3-beta\n\nSyntax: main.py x.x.x\n\nThis version scans following ports: 20, 21, 22, 23, 25, 53, 80, 110, 433, 587, 3389, 5222, 5223, 25565, 51413"
    sys.exit("\n[*] Script finished. Exiting\n\x1b[0m\r")

def main():
    if len(sys.argv) < 2:
        help()
    else:
        targetIP = sys.argv[1]
    offlineIPs = []
    onlineIPs = []
    offlineto = []
    onlineto = []
    
    subprocess.call('python ipscanner.py '+str(targetIP), shell=True) #Calls the ipscanner.py script and waits for it to finish
    
    print "\033[1;34m[*] IP-Scan Finished. Evaluating logfiles... please wait"
    for n in range(64):
        readerfile = "/tmp/ip"+str(n)
        fileHandle = open (readerfile)
        onlineto.append(fileHandle.readline())
        offlineto.append(fileHandle.readline())
        fileHandle.close()
    print "\n\n\033[1;33mOnline IPs: \033[1;32m"
    for ip in onlineto:
        ip = ip.split()
        for ip in ip:
            ip = string.replace(ip, "\n", "")
            ip = string.replace(ip, ",", "")
            ip = string.replace(ip, "[", "")
            ip = string.replace(ip, "]", "")        
            ip = string.replace(ip, "'", "")       
            if len(ip) > 5:
                onlineIPs.append(ip)
                print "\r"+str(ip)+"\r"   
    for ip in offlineto:
        ip = string.replace(ip, "\n", "")
        ip = string.replace(ip, "['", "")
        ip = string.replace(ip, "']", "")       
        if len(ip) > 5:
            offlineIPs.append(ip)
    '''
    For debugging. Ignore this
    print onlineIPs
    print offlineIPs
    '''
    for IP in onlineIPs:
        subprocess.call('python portscan.py '+str(IP), shell=True)
    
    print "\033[1;34m[*] Portscan Finished. Evaluating logfiles... please wait"
    now = datetime.datetime.now()
    report = "PORTreport-"+str(now)+".txt" #Saves report in a file with timestamp in the name
    file = open(report, 'w')
    print "\033[1;34m[*] Writing logfile to: "+str(report) 
    for IP in onlineIPs:
        portlist = []
        portlistraw = []
        portlistfinal = []
        for n in range(14):
            readerfile = "/tmp/port"+str(IP)+":"+str(n)
            fileHandle = open(readerfile)
            portlistraw.append(fileHandle.readline())
            fileHandle.close()
        for port in portlistraw:
            port = string.replace(port, "\n", "")
            port = string.replace(port, "[", "")
            port = string.replace(port, "]", "")        
            port = string.replace(port, "'", "")        
            if len(port) >= 2:
                portlist.append(port)
        portlistfinal = [x for x in portlist if x != []]   
        file.write ("Report for IP: "+str(IP)+"\nOpen Ports:\t"+str(portlistfinal)+"\n\n")
        
    file.close()
        
    ### ENDLINE MODULE ###
    print "\033[1;34m[*] Cleaning tmp-files..."
    for n in range(64):
        filename = "/tmp/ip"+str(n)
        os.remove(filename)
    for ip in onlineIPs:
        for n in range(14):
            filename = "/tmp/port"+ip+":"+str(n)
            os.remove(filename)
    sys.exit("[*] Script finished. Exiting\n\x1b[0m\r")

if __name__ == "__main__":
    main()  

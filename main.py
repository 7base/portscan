#!/usr/bin/python

import os
import sys
import socket
import string
import subprocess

def main():
    
    offlineIPs = []
    onlineIPs = []
    offlineto = []
    onlineto = []
    
    subprocess.call('python ipscanner.py', shell=True)
    
    print "\033[1;34m[*] IP-Test Finished. Evaluating logfiles... please wait"
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
    print "\n\n\033[1;33mOffline IPs: \033[1;31m\nOffline Ips are hidden"     
    for ip in offlineto:
        ip = string.replace(ip, "\n", "")
        ip = string.replace(ip, "['", "")
        ip = string.replace(ip, "']", "")       
        if len(ip) > 5:
            offlineIPs.append(ip)
    '''
    print onlineIPs
    print offlineIPs
    '''
    for IP in onlineIPs:
        subprocess.call('python portscan.py '+str(IP), shell=True)
    
    print "\033[1;34m[*] Portscan Finished. Evaluating logfiles... please wait"
    report = "/home/simon/PORTreport-87.156.144.*"
    file = open(report, 'w')
    print "\033[1;34m[*] Writing logfile to: "+str(file) 
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

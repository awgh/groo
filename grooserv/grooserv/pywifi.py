#!/usr/bin/env python

import sys, string
from subprocess import Popen,PIPE

def pywifi_scan():
    try:
        p1 = Popen(['/sbin/iwlist', 'ath0', 'scan'], stdout=PIPE, stderr=PIPE)
        IWLIST = 1
    except OSError,ose:
        print ose
        print 'Loading Test Data Instead...'
        p1 = Popen(['cat', 'iwlist.txt'], stdout=PIPE)
        IWLIST = 0
    
    pEnd = Popen(['grep','-A3', '-B1', 'ESSID'], stdin=p1.stdout, stdout=PIPE)
    output = pEnd.communicate()[0]
    
    ssid_list = []
    lines = string.split(output,'\n')
    iwnet = {}
    for line in lines:
        s = string.strip(line)
        sv = s.split(":")
        lsv = len(sv)
        if lsv == 1:
            ssid_list.append(iwnet)
            iwnet = {}
        elif lsv == 2:
            if sv[0] == 'Mode':
                iwnet['mode'] = sv[1]
            elif string.find(sv[1], 'Channel') > 0:
                sx = sv[1].split(' ')
                ssx = sx[-1]
                iwnet['channel'] = ssx[:-1]
            elif sv[0] == 'ESSID':
                iwnet['essid'] = sv[1][1:len(sv[1])-1]
        else:
            sw = s.split(" ")
            iwnet['bssid'] = sw[len(sw)-1]         
    
    return ssid_list

def pywifi_parseClient( essid, dumpfile ):

    f = open(dumpfile, "r")
    essid_table = {} # essid to bssed
    result = ""
    essid_mac = ""

    nextLineIsDict = 1;
    whichDict = 1;

    lines = f.readlines()[1:]
    for line in lines:
        if nextLineIsDict == 1:
            if whichDict == 1:
                headers1 = string.split(line, ",")
            elif whichDict == 2:
                headers2 = string.split(line, ",")
            nextLineIsDict = 0
        
        elif string.strip(line) == "":
            try:
                essid_mac = essid_table[essid]
                nextLineIsDict = 1
                whichDict = 2
            except KeyError:
                return
        
        else:
            if whichDict == 1:
                linedata = string.split(line, ",")
                d = {}
                for i in range(len(linedata)):
                    d[ string.strip(headers1[i]) ] = string.strip(linedata[i])
                essid_table[string.strip(d['ESSID'])] = string.strip(d['BSSID'])
                
            elif whichDict == 2:
                linedata = string.split(line, ",")
                d = {}
                for i in range(len(linedata)):
                    if i < len(headers2):
                        d[ string.strip(headers2[i]) ] = string.strip(linedata[i])
                if string.strip(d['BSSID']) == essid_mac:
                    result = string.strip(d['Station MAC'])            
    return result

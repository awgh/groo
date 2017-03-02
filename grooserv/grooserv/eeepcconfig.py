
import pymenu        

def regen_crackmenu( menuapp ):
    mitems = menuapp.rescan( [menuapp.fakeauthcrack, 'mainmenu'] )
    crackmenu = pymenu.Menu( 'GET CRACKING', mitems )
    menuapp.addMenu('crackmenu', crackmenu)

def regen_deauthmenu( menuapp ):
    mitems = menuapp.rescan( [menuapp.deauth] )
    deauthmenu = pymenu.Menu( 'BOOT SPLAT', mitems )
    menuapp.addMenu('deauthmenu', deauthmenu)

groo_root = "~/groo/"

monitor_if = "ath1"

aircrack = "/usr/bin/aircrack-ng"
airodump = "/usr/sbin/airodump-ng"
aireplay = "/usr/sbin/aireplay-ng"

iwlist = groo_root + "scripts/wiscan.pl "+monitor_if
helpfile = 'README.web'

dumpDirectory = groo_root + "dumps"
  
def loadMenus(app):

    # Hardcoding a couple system vars
    app.env['MAC'] =  '06:22:43:08:bd:40'
#    app.env['MAC'] = '06:1B:2F:FF:FF:FF'
    app.env['IF0'] = 'ath1'
    
    mainmenu = pymenu.Menu( 'WHAT BITCH WHAT?',\
               [\
                ('Full Scan',   ['SHELL:'+iwlist]),\
                ('Crack',  [regen_crackmenu, 'crackmenu']),\
                ('Deauth Flood',  [regen_deauthmenu, 'deauthmenu']),\
                ('View Keys', [app.listKeys]),\
                ('View Progress', ['resumemenu']),\
                ('Cancel Crack', ['SHELL:killall screen;sleep 1;screen -wipe']),\
                ('Help', ['SHELL:cat '+helpfile])\
               ] )
    app.addMenu('mainmenu', mainmenu)
    app.startMenu('mainmenu')
    
    resumemenu = pymenu.Menu( 'RESUME', [\
                 ('DUMP',['ATTACH:dump']),\
                 ('AUTH',['ATTACH:auth']),\
                 ('CRACK',['ATTACH:crack'])] )
    app.addMenu('resumemenu', resumemenu)

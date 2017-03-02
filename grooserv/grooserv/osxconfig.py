
import pymenu        

def regen_crackmenu( menuapp ):
    mitems = menuapp.rescan( [menuapp.fakeauthcrack, 'mainmenu'] )
    crackmenu = pymenu.Menu( 'GET CRACKING', mitems )
    menuapp.addMenu('crackmenu', crackmenu)

def regen_deauthmenu( menuapp ):
    mitems = menuapp.rescan( [menuapp.deauth] )
    deauthmenu = pymenu.Menu( 'BOOT SPLAT', mitems )
    menuapp.addMenu('deauthmenu', deauthmenu)

groo_root = "/Users/burtz/groo/"
airtools_root = "/opt/local/bin/"

iwlist = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s"
helpfile = 'README.web'
  
def loadMenus(app):

    mainmenu = pymenu.Menu( 'WHAT BITCH WHAT?',\
               [\
                ('Full Scan',   ['SHELL:'+iwlist]),\
                ('Crack',  [regen_crackmenu, 'crackmenu']),\
                ('Deauth Flood',  [regen_deauthmenu, 'deauthmenu']),\
                ('View Keys', [app.listKeys]),\
                ('View Progress', ['resumemenu']),\
                ('Cancel Crack', ['SHELL:killall SCREEN;screen -wipe']),\
                ('Help', ['SHELL:cat '+helpfile])\
               ] )
    app.addMenu('mainmenu', mainmenu)
    app.startMenu('mainmenu')
    
    resumemenu = pymenu.Menu( 'RESUME', [\
                 ('DUMP',['ATTACH:dump']),\
                 ('AUTH',['ATTACH:auth']),\
                 ('CRACK',['ATTACH:crack'])] )
    app.addMenu('resumemenu', resumemenu)

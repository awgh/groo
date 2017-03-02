
test = False # is grooserv in test mode?
#test = True

if test:
    import osxconfig
    from osxconfig import loadMenus
    from osxconfig import groo_root,aircrack,airodump,aireplay
#else:
#    import itxconfig
#    from itxconfig import loadMenus
#    from itxconfig import dumpDirectory
#    from itxconfig import groo_root,aircrack,airodump,aireplay
else:
    import eeepcconfig
    from eeepcconfig import loadMenus
    from eeepcconfig import dumpDirectory
    from eeepcconfig import groo_root,aircrack,airodump,aireplay

    

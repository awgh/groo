
#test = False # is grooserv in test mode?
test = True

if test:
    import osxconfig
    from osxconfig import loadMenus
    from osxconfig import groo_root,airtools_root
else:
    import itxconfig
    from itxconfig import loadMenus
    from itxconfig import dumpDirectory
    from itxconfig import groo_root,airtools_root        

    

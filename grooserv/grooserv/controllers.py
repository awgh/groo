import turbogears as tg
from turbogears import controllers, expose, flash
from turbogears import identity, redirect, widgets

from grooserv import model

import cherrypy
from cherrypy import request, response

import pymenu
from pymenu import Menu, MenuApp, formatExceptionInfo
import string
import grooconfig

# from grooserv import json
# import logging
# log = logging.getLogger("grooserv.controllers")

class Menus:
    def __init__(self, menuapp):
        self.app = menuapp

    def strongly_expire(func):
        """Decorator that sends headers that instruct browsers and proxies not to cache.
        """
        def newfunc(*args, **kwargs):
            cherrypy.response.headers['Expires'] = 'Sun, 19 Nov 1978 05:00:00 GMT'
            cherrypy.response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
            cherrypy.response.headers['Pragma'] = 'no-cache'
            return func(*args, **kwargs)
        return newfunc

    @expose(template=".templates.menu")
    @strongly_expire
    @identity.require(identity.in_group("admin"))
    def default(self, menu=None, action=None):
        
        # is this a valid menu name?
        m = None
        try:
            m = self.app.menus[menu]
        except:
            m = self.app.currentMenu()   
        if m == None:
            m = self.app.currentMenu()
        
        if action != None:
            try:
                if action == 'm':
                    self.app.processTransition(m, 'm', self.app.webModeHandler)
                else:
                    idx = int(action)
                    self.app.processTransition(m, str(idx), self.app.webModeHandler)
            except:
                print formatExceptionInfo()
                    
        # After transition, set up new page
        cmenu = self.app.currentMenu()
        menuname = cmenu.title
        tupleList = [("","")]
        wlist = []
        mitems = cmenu.menuitems        
        
        for i in range(0, len(mitems)):
            tupleList.append(('/menus/'+self.app.currentmenu+'?action='+str(i+1), mitems[i][0]))
        
        jump = widgets.JumpMenu("Options", options=tupleList)
        wlist.append( jump.js )
        wlist.append( jump )
        
        hc = self.app.hardcopyReady
        sr = self.app.shellResult
        
        if hc != None:
            self.app.hardcopyReady = None
            try:
                f = open( self.app.hardcopies[hc], 'r' )
                txt = f.read()
                f.close()
                wlist.append( widgets.TextArea(default=txt, rows=24, cols=80, attrs={'READONLY':'true'}) )
            except:
                wlist.append( widgets.TextArea(default='No screen available.', rows=24, cols=80, attrs={'READONLY':'true'}) )

        if sr != None:
            self.app.shellResult = None
            wlist.append( widgets.TextArea(default=sr, rows=24, cols=80, attrs={'READONLY':'true'}) )
        
        return dict(title=cmenu.title, wlist=wlist)

class Root(controllers.RootController):

    def __init__(self):
        self.app = MenuApp()
        grooconfig.loadMenus(self.app)        
        self.menus = Menus(self.app)


    @expose(template=".templates.menu")
    @identity.require(identity.in_group("admin"))
    def index(self, *args, **kw):
       redirect(tg.url('/menus'))

    @expose(template="grooserv.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous and identity.was_login_attempted() \
                and not identity.get_identity_errors():
            redirect(tg.url(forward_url or previous_url or '/', kw))

        forward_url = None
        previous_url = request.path

        if identity.was_login_attempted():
            msg = _("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg = _("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg = _("Please log in.")
            forward_url = request.headers.get("Referer", "/")

        response.status = 403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
            original_parameters=request.params, forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        redirect("/")

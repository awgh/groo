
_____________________________
#                           #
# GROO v0.2 (eeepc) README  #
#                           #
# 1/29/09   awgh@awgh.org   #
-----------------------------

IMPORTANT:
There are several hard-coded values in the file grooserv/grooserv/eeepcconfig.py, including
the MAC address and the full paths to aircrack-ng programs.  

You may need to change some of the values in this file.  At a minimum, set groo_root to be the
correct directory for where groo is installed.  It defaults to "~/groo".

I hope to push these into the .cfg file whenever I get my act together...


DEPENDENCIES
-------------------------------------------------------
(Starting from a default Ubuntu Netbook Remix install):

Drivers:
  madwifi-ng driver patched for reinjection (if patch is needed?)

From apt-get:
  madwifi-tools
  sqlite
  aircrack-ng
  screen
  python

From pip or easy_install:
  turbogears
  kid
  turbokid
  sqlobject
-------------------------------------------------------

To initialize the wireless card to Monitor mode, check out the example script:
./scripts/init_ath

To fire up the web service (as root):
./start-groo.sh

The server will start up on port 8080 by default.
A single user has already been created, named 'admin'.  
The default password is 'maxterm'.

Keep an eye out for path errors, you'll probably have to tweak the scripts to get them to work on your box.

Any questions? Comments? Fixes?

email me at awgh@awgh.org



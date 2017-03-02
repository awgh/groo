Just a quick note until I get a chance to write a FAQ.

The TurboGears code lives in grooserv/grooserv mostly.

There are a couple helper Bash scripts in scripts/.

Be sure to look at the file grooserv/grooserv/grooconfig.py for a place to change the config.

You will need to have at least the following packages installed:
Python
aircrack-ng
SQLite3
TurboGears, SQLObject, related dependencies.

To fire up the web service (as root):
cd grooserv
python start-grooserv.py

The server will start up on port 8080 by default.
A single user has already been created, named 'admin'.  
The default password is 'maxterm'.

Keep an eye out for path errors, you'll probably have to tweak the scripts to get them to work on your box.

Any questions? Comments? Fixes?

email me at awgh@awgh.org



#!/bin/bash
sudo -v
cd grooserv
sudo chmod 777 /var/run/screen
sudo python start-grooserv.py

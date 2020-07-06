#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:30:13 2020

@author: Pedro Augusto Salamoni
"""

import Config.prelibs
import time
import pexpect
from Config.dbmanager import LocalDatabase

class Setup:
    """Default configuration for Octopus Project Raspberries."""

    def __init__(self):
        self.process = pexpect
        self._db = LocalDatabase()
        
        
    def send(self, command, pause=0):
        self.process.run(f"{command}\n")
        time.sleep(pause)
        
    def create_directory(self):
        self.send('sudo mkdir /usr/bin/octopus/')
        self.send('sudo cp Config/ini.py /usr/bin/octopus/')
        self.send('sudo cp Config/bluetoothctl.py /usr/bin/octopus/')
        self.send('sudo cp config.json /usr/bin/octopus/')
        self.send('sudo cp fdb.json /usr/bin/octopus/')  
        self.send('sudo cp octopus.db /usr/bin/octopus/')
        
    def create_service(self):
        
        service_txt = "[Unit]\n Description=Octopus Service\n After=multi-user.target\n Conflicts=getty@tty1.service\n\n [Service]\n Type=simple\n ExecStart=/usr/bin/python3 /usr/bin/octopus/ini.py\n StandardInput=tty-force\n\n [Install]\n WantedBy=multi-user.target"
        
        f = open('/lib/systemd/system/octopus.service', 'w')
        f.write(service_txt)
        f.close()
        
        self.send('sudo systemctl daemon-reload')
        self.send('sudo systemctl enable octopus.service')
        self.send('sudo systemctl start octopus.service')
        
    def delete_service(self):
        self.send('sudo systemctl end octopus.service')
        self.send('sudo systemctl disable octopus.service')
        self.send('rm -f /lib/systemd/system/octopus.service')
        self.send('sudo systemctl daemon-reload')
        
    def delete_directory(self):
        self.send('rm -rf /usr/bin/octopus/')
    
    def install(self):
        
        self.create_directory()
        self.create_service()
        
        self._db.create_database()
        self._db.register_places()
        self._db.register_sensors()
        
    def uninstall(self):
        
        self.delete_service()
        self.delete_directory()
        
        try:
            self.delete_database()
        except:
            pass
        
        try:
            self.delete_service()
        except:
            pass
        
        try:
            self.delete_directory()
        except:
            pass
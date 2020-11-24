#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 13:50:07 2020

@author: setup
"""

def preInstall():
    #Preparing libraries needed to run script
    import pexpect
    pexpect.run("sudo pip3 install mysql-connector-python\n")

preInstall()
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import bluetoothctl
import time

class ConnectionBT():
    
    def __init__(self):
        
        #Attributes
        self._btctl = bluetoothctl.Bluetoothctl()
        self._btctl.sp_init('00:18:E4:40:00:06')
        self._sp = None
        
    def remove_sensors(self):
        try:
            self._btctl.remove('00:18:E4:40:00:06')
        except:
            pass
        
    def connect_sensors(self):
        
        self._btctl.start_scan()
        self._btctl.pair('00:18:E4:40:00:06','0000')
        
        try:
            self._sp = serial.Serial(port='/dev/rfcomm0', baudrate=9600, bytesize=8, timeout=10, stopbits=serial.STOPBITS_ONE)
            sp_txt = self._sp.readline().decode("utf-8")
        except:
            print("Offline")
            return False
        else:
            print(".")
            return True
        
    def get_data(self):
        
        bt_output=['']
        
        while len(bt_output)<2:
            try:
                sp_txt = self._sp.readline().decode("utf-8")
            except:
                print("Connection Lost")
                break
            bt_output = sp_txt.replace('\r\n','').split(':')
            print(bt_output)
            print(sp_txt)
            #TIMEOUT
        
        return sp_txt
    
    def send_confirmation(self):
        
        msg = self._btctl.parse_device_info('OK TESTE')
        #self._sp.write(msg)
        

if __name__ == '__main__':
    
    cbt = ConnectionBT()

    while True:
        cbt.remove_sensors()
        
        if cbt.connect_sensors():
            data = cbt.get_data()
            cbt.send_confirmation()
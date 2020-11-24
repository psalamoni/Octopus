# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import bluetoothctl
import time
import dbmanager as dbm

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
        
        try:
            self._btctl.start_scan()
            self._btctl.pair('00:18:E4:40:00:06','0000')
            self._sp = serial.Serial(port='/dev/rfcomm0', baudrate=9600, bytesize=8, timeout=10, stopbits=serial.STOPBITS_ONE)
            self._sp.readline().decode("utf-8")
        except:
            return False
        else:
            return True
        
    def get_data(self):
        
        bt_output=['']
        i=0
        
        while (len(bt_output) < 5) or ('' in bt_output) or (None in bt_output) or (i<50):
            try:
                sp_txt = self._sp.readline().decode("utf-8")
                bt_output = sp_txt.replace('\r\n','').split(':')
                print(f"data: {bt_output}")
            except:
                print("Connection Lost")
                return False
            i+=1
        
        if i>=50:
            return True
        else:
            return bt_output
    
    def send_confirmation(self):
        
        msg = self._btctl.parse_device_info('J')
        self._sp.write(msg)
        

if __name__ == '__main__':
    
    cbt = ConnectionBT()

    while True:
        cbt.remove_sensors()
        
        if cbt.connect_sensors():
            data = cbt.get_data()
            
            if data == False:
                continue
            elif data == True:
                print(f"Sending this:{data}")
                cbt.send_confirmation()
                cbt.remove_sensors()
            else:
                if dbm.LocalDatabase.insert_data(data[0],data[1],data[2],data[3],data[4]):
                    cbt.send_confirmation()
                    cbt.remove_sensors()
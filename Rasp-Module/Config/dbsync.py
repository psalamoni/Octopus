#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 11:02:29 2020

@author: setup
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 11:30:13 2020

@author: Pedro Salamoni
"""

import dbmanager as dbm

class DBsync():
    
    def __init__(self):
        
        self._ldb = dbm.LocalDatabase()
        self._fdb = dbm.ForeignDatabase()
        
    def syncDB(self):
        
        data = self._ldb.get_data()
        
        if data:
            
            for sdata in data:
                if self._fdb.insert_data(sdata[1],sdata[2],sdata[3],sdata[4],sdata[5]):
                    self._ldb.del_data(sdata[0])
                else:
                    print('Couldn\'t insert data in Foreign Database, please check internet connection and/or Database Setup')
                    return
                
        print('You\'re safe. Your data is up-to-date in Foreign Database!')

if __name__ == '__main__':
    
    dbs = DBsync()
    
    dbs.syncDB()
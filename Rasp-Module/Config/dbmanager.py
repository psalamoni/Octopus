#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:29:13 2020

@author: Pedro Salamoni
"""

import mysql.connector
import sqlite3
import json

class LocalDatabase:
    """Local Database Connection."""

    def __init__(self):
        self._cursor = None
        self._conn = None
        self._fdb = ForeignDatabase()
        
    def connect_database(self):
        """Connect database"""
        self._conn = sqlite3.connect('/usr/bin/octopus/octopus.db')
        self._cursor = self._conn.cursor()
        
        return self._cursor
        
    def close_database(self):
        
        if self._conn == None:
            return
        
        self._conn.commit()
        self._conn.close()
        self._conn = None
        self._cursor = None

    def create_database(self):
        
        if self._conn == None:
            self.connect_database()
        
        """Create Place db"""
        self._cursor.execute('''
                         CREATE TABLE place (
                             id_place INTEGER PRIMARY KEY,
                             abbreviation VARCHAR(3) NOT NULL,
                             description TEXT NULL
                             )''')
                         
        """Create Sensor db"""
        self._cursor.execute('''
                         CREATE TABLE sensor (
                             id_sensor INTEGER PRIMARY KEY,
                             id_place INTEGER,
                             id_uid_type INT(10),
                             abbreviation VARCHAR(3) NOT NULL,
                             sensor_type VARCHAR(50) NOT NULL,
                             description TEXT NULL,
                             FOREIGN KEY(id_place) REFERENCES place(id_place)
                             )''')
        
        """Create Data db"""
        self._cursor.execute('''CREATE TABLE data (
            id_data INTEGER PRIMARY KEY AUTOINCREMENT,
            id_sensor INTEGER,
            value REAL NULL,
            dtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            description TEXT NULL,
            valid INTEGER,
            FOREIGN KEY(id_sensor) REFERENCES sensor(id_sensor)
            )''')
        
        self.close_database()
        
    def find_id_sensor(self, place_id, id_uid_type, abbreviation):
        if self._conn == None:
            self.connect_database()
            
        self._cursor.execute(
            f'SELECT id_sensor FROM sensor WHERE id_place={place_id} AND id_uid_type={id_uid_type} AND abbreviation="{abbreviation}"'
            )
        
        result = self._cursor.fetchone()
        
        self.close_database()
        
        try:
            return int(result[0])
        except:
            return False
    
    def insert_data(self, abbreviation, id_place, id_uid_type, time, value):
        
        if self._conn == None:
            self.connect_database()
        
        id_sensor = self.find_id_sensor(id_place, id_uid_type, abbreviation)
            
        if id_sensor:
            self._cursor.execute(
                f'INSERT INTO data (id_sensor, value, dtime, description, valid) VALUES ({id_sensor}, {value}, {time}, "", 0)'
                )
            return True
        else:
            return False
        
    def import_parameters(self):
        
        c = json.load(open('/usr/bin/octopus/config.json','r'))
        for key, value in c.items():
            setattr(self, key, value)
        self.place_id = int(self.place_id)
        
    def register_places(self):
        
        self.import_parameters()
        
        if self._conn == None:
            self.connect_database()
        
        self._cursor.execute(
            f'INSERT INTO place (id_place, abbreviation, description) VALUES ({self.place_id}, "{self.place_abbreviation}", "{self.place_description}")'
            )
        self._fdb.register_places(self.place_id, self.place_abbreviation, self.place_description)
    
    def register_sensors(self):
        
        self.import_parameters()
        
        if self._conn == None:
            self.connect_database()
            
        for sensor in self.sensors:
            id_uid_type, abbreviation, sensor_type, description = sensor
            id_sensor = self._fdb.register_sensors(self.place_id, id_uid_type, abbreviation, sensor_type, description)
            self._cursor.execute(
                f'INSERT INTO sensor (id_sensor, id_place, id_uid_type, abbreviation, sensor_type, description) VALUES ({id_sensor}, {self.place_id}, {id_uid_type}, "{abbreviation}", "{sensor_type}", "{description}")'
                )
            
        self.close_database()
        
class ForeignDatabase:
    """Foreign Database Connection"""
    
    def __init__(self):
        self._cursor = None
        self._conn = None
        
    def connect_database(self):
        """Connect database"""
        
        c = json.load(open('/usr/bin/octopus/fdb.json','r'))
        for key, value in c.items():
            setattr(self, key, value)
        
        self._conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.pswd
            )
        self._cursor = self._conn.cursor()
        
        return self._cursor
        
    def close_database(self):
        
        if self._conn == None:
            return
        
        self._conn.commit()
        self._conn.close()
        self._conn = None
        self._cursor = None
        
    def find_id_sensor(self, place_id, id_uid_type, abbreviation):
        if self._conn == None:
            self.connect_database()
            
        self._cursor.execute(
            f'SELECT id_sensor FROM {self.bd_name}.sensor WHERE id_place={place_id} AND id_uid_type={id_uid_type} AND abbreviation="{abbreviation}"'
            )
        
        result = self._cursor.fetchone()
        
        self.close_database()
        
        return int(result[0])
    
    def register_places(self, place_id, place_abbreviation, place_description):
        
        if self._conn == None:
            self.connect_database()

        self._cursor.execute(
            f'INSERT INTO {self.bd_name}.place (id_place, abbreviation, description) VALUES ({place_id}, "{place_abbreviation}", "{place_description}")'
            )
            
        self.close_database()
        
        return
    
    def register_sensors(self, place_id, id_uid_type, abbreviation, sensor_type, description):
        
        if self._conn == None:
            self.connect_database()

        self._cursor.execute(
            f'INSERT INTO {self.bd_name}.sensor (id_place, id_uid_type, abbreviation, sensor_type, description) VALUES ("{place_id}", "{id_uid_type}", "{abbreviation}", "{sensor_type}", "{description}")'
            )
            
        self.close_database()
        
        return self.find_id_sensor(place_id,id_uid_type,abbreviation)
#!/usr/bin/env python

import copy
#import dateutil.parser
#import cbpro

#from datetime import datetime
import orjson as json
import sys
import ciso8601
import os
import pathlib
import gzip 
import io
from subprocess import Popen, PIPE
#last_day=None
#last_seq=None
from enum import Enum 

class EventsToDiskSaver():
    def __init__(self, destination_path , product_id):
        self.destination_path = destination_path
        self.product_id = product_id
        self.sequence = None
        self.last_day = None
        self.file_path = None
        self.out_file = None
        self.out_buffer = None
        self.save_orderbook = None
        self.last_ddate = None
        self.Modes =  Enum('Modes', 'FAST SAFE')
        self.mode = self.Modes.FAST
        
    
    def get_path(self, ddate, prefix="events_"):
        dir_path = self.destination_path + "/" + str(ddate.year) + "/" + str(ddate.month) + "/" + str(ddate.day)
        dir_path = pathlib.Path(dir_path)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e: 
                print(e)
                print("Error creating destination path")
        
        filecount = 0
        file_path = str(dir_path) + "/" + prefix + self.product_id + "_" + str(filecount) + ".json.gz"
        file_path = pathlib.Path(file_path)
        while( file_path.exists() ):
            filecount += 1
            file_path = str(dir_path) + "/" + prefix + self.product_id + "_" + str(filecount) + ".json.gz"
            file_path = pathlib.Path(file_path)
            
        return file_path
    
    def close(self):
        if self.out_file is not None:
            #self.out_buffer.flush()
            if self.mode == self.Modes.FAST:
                self.out_buffer.stdin.close()
                self.out_buffer.wait()
            self.out_file.close()
            self.out_file = None
        
        
    def store(self, msg, line):
        save_orderbook = False
        if 'product_id' in msg:

            #now = dateutil.parser.parse(datetime.now().isoformat()+'Z')
            #msg['time'] = dateutil.parser.parse(msg['time'])
            ddate = ciso8601.parse_datetime(msg['time'])
            self.last_ddate = ddate
            sequence = msg['sequence']
            if self.sequence is None:
                self.sequence = sequence-1
                self.file_path = None
            
            if sequence <= self.sequence:
                print("out of order sequence", sequence, "last_seq", self.sequence)
                self.file_path = None
            
            if sequence != self.sequence +1:
                print("Missing data", sequence, "last_seq", self.sequence)
                self.file_path = None
            
            self.sequence = sequence

            if self.last_day is None or ddate.day != self.last_day :
                self.file_path = None
                #Mirar si existe la ruta
                
            self.last_day = ddate.day
            
            if self.file_path is None:
                self.save_orderbook = self.get_path( ddate, prefix="orderbook_")
                save_orderbook = True
                
            
            if self.file_path is None or self.out_file is None:
                if self.out_file is not None:
                    #self.out_buffer.flush()
                    if self.mode == self.Modes.FAST:
                        self.out_buffer.stdin.close()
                        self.out_buffer.wait()
                    self.out_file.close()
                    self.out_file = None
                    
                self.file_path = self.get_path(ddate)
                print("Opening", str(self.file_path))
                #self.out_file = gzip.open( str(self.file_path), "wb")
                #self.out_buffer = io.BufferedWriter(self.out_file, buffer_size=100000000)
                if self.mode == self.Modes.FAST:
                    self.out_file = open( str(self.file_path), "wb")
                    p = Popen('gzip', stdin=PIPE, stdout=self.out_file)
                    self.out_buffer=p
                if self.mode == self.Modes.SAFE:
                    self.out_file = gzip.open( str(self.file_path), "wb")

            
            
            if self.mode == self.Modes.FAST:
                self.out_buffer.stdin.write( str.encode(line))
            elif self.mode == self.Modes.SAFE:
                self.out_file.write( str.encode(line))

        return save_orderbook


if __name__ == "__main__":

    where_to_save=sys.argv[1]
    produt_id= sys.argv[2]

    eventSaver = EventsToDiskSaver(where_to_save, produt_id)
    eventSaver.mode = eventSaver.Modes.FAST
    count=1
    salir=10
    for line in sys.stdin:
        #print(line)
        try:
            msg = json.loads(line)
            #print(msg)
        except:
            print("Error processing", line)
            continue
        if msg['type'] == 'heartbeat':
            #print("Skipping heartbeat")
            continue
        
        eventSaver.store(msg, line)
        
        ##if 'product_id' in msg:

            ###now = dateutil.parser.parse(datetime.now().isoformat()+'Z')
            ###msg['time'] = dateutil.parser.parse(msg['time'])
            ##ddate = ciso8601.parse_datetime(msg['time'])
            ##seq = msg['sequence']
            ##if last_seq is None:
                ##last_seq = seq-1
            
            ##if seq <= last_seq:
                ##print("out of order sequence", seq, "last_seq", last_seq)
            
            ##if seq != last_seq +1:
                ##print("Missing data", seq, "last_seq", last_seq)
            
            ##last_seq = seq
            ###if msg['time'].minute == 40 and msg['time'].second == 0:
                ###print(msg['time'])
            ##if last_day is None or ddate.day != last_day :
                ##path=
                ###Mirar si existe la ruta
                
                
        count = (count + 1)%100000
        if count == 0:
            print("Checkpoint", msg['product_id'], msg['time'])
            #salir-=1
            #if salir <= 0:
                #break

    eventSaver.close()


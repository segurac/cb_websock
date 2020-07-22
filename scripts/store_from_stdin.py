#/usr/bin/env python

import sys
from bson.binary import Binary
from sortedcontainers import SortedDict
import copy
import dateutil.parser
from pymongo import MongoClient
import cbpro
import pymongo
from datetime import datetime
import ujson as json

mongo_client = MongoClient('mongodb://172.17.0.2:27017/')

# specify the database and collection
db = mongo_client.coinbaseDB
#product = 'BTC-USD'
product = sys.argv[1]
collection = db[product + '_events']
collection.create_index([("sequence", pymongo.ASCENDING)], unique=True)
collection.create_index([("sequence", pymongo.DESCENDING)], unique=True)
collection.create_index([("time", pymongo.ASCENDING)])
collection.create_index([("time", pymongo.DESCENDING)])

count=1
for line in sys.stdin:
    #print(line)
    try:
        msg = json.loads(line)
    except:
        print("Error processing", line)
        continue
    if 'product_id' in msg:

        #now = dateutil.parser.parse(datetime.now().isoformat()+'Z')
        msg['time'] = dateutil.parser.parse(msg['time'])
        try:
            collection.insert_one(msg)
            count = (count + 1)%10000
            if count == 0:
                print("Checkpoint", product)
            
        except Exception as e: 
            print(e)
            print("Error inserting event")


    


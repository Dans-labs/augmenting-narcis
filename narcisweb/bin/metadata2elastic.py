#!/usr/local/bin/python
from __future__ import print_function, absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from pymongo import MongoClient
from os import walk
import simplejson
import json
import logging
from elasticsearch import Elasticsearch
logging.basicConfig(filename='logs/importmetadata.log',format='%(asctime)s %(levelname)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)

path = "/exchange"
metadatapath = path
print("Importing metadata from %s" % metadatapath)
logging.info("Importing metadata from %s" % metadatapath)

es = Elasticsearch(
['elasticsnarcis'],
http_auth=('elastic', 'changeme'),
port=9200
)

client = MongoClient('mongodb://mongonarcis:27017')
datasetdb = client.get_database('narcis')
col = datasetdb.data
newindex = 'narcis'
newcol = 'metadata'

f = []
for (dirpath, dirnames, filenames) in walk("%s" % metadatapath):
    f.extend(filenames)

for filename in f:
    filepath = "%s/%s" % (path, filename)
    file = open(filepath, 'r')
    print(filepath)
    for lastline in file:
        metadata = json.loads(lastline)
        url = "https://www.narcis.nl/dataset/RecordID/%s" % metadata['id']
        info = {}
        info[url] = metadata

        try:
            es.create(index=newindex, doc_type=newcol, body=info[url], id=info[url]['id'])
        except:
            try:
                es.delete(index=newindex, doc_type=newcol, id=info[url]['id'])
                es.create(index=newindex, doc_type=newcol, body=info[url], id=info[url]['id'])
            except:
                logging.error("Error in inserting %s into 'dataset' database" % (path + "/" + filename))

print("Metadata imported")
logging.info("Metadata imported")


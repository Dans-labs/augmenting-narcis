#!/usr/local/bin/python
from __future__ import print_function, absolute_import

# make sure you only have the DOIBoost 2017 files in the data/original folder

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from pymongo import MongoClient
from os import walk
import simplejson
import json
import logging
import ast
logging.basicConfig(filename='importdoiboost.log',format='%(asctime)s %(levelname)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)

path = "/exchange/DOIboost2017"
metadatapath = path

print("Importing metadata from %s" % metadatapath)
logging.info("Importing metadata from %s" % metadatapath)

client = MongoClient('mongodb://mongonarcis:27017')
datasetdb = client.get_database('narcis')
col = datasetdb["doiboost2017"]

f = []
for (dirpath, dirnames, filenames) in walk("%s" % metadatapath):
    if filenames == '.DS_Store':
        os.remove(filenames)
    f.extend(filenames)

print("Files to be uploaded: ", len(f), ".")
i = 0
for filename in f:
    i += 1
    filepath = "%s/%s" % (path, filename)
    file = open(filepath, 'r')

    for lastline in file:
        metadata = json.loads(lastline)
        try:
            # create a dict from the metadata string
            col.insert_one(ast.literal_eval(metadata))
        except:
            logging.error("Error in inserting %s into 'dataset' database" % (path + "/" + filename))
    print(i, "files out of ", len(f), "uploaded.")
print((len(f) - i), "not uploaded.")


print("Metadata imported")
logging.info("Metadata imported")

#!/usr/local/bin/python
from __future__ import print_function, absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from os import walk
from easy.settings import *
from easy.core.database import *

import logging
logging.basicConfig(filename='logs/importmetadata.log',format='%(asctime)s %(levelname)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)

path = "%s/../../tests" % HERE
metadatapath = "%s/metadata" % path
print("Importing metadata from %s" % metadatapath)
logging.info("Importing metadata from %s" % metadatapath)

client = MongoClient()
datasetdb = client.get_database('dataset')
col = datasetdb.data

f = []
for (dirpath, dirnames, filenames) in walk("%s" % metadatapath):
    f.extend(filenames)

for filename in f:
    filepath = "%s/metadata/%s" % (path, filename)
    metadata = metadata2mongo(filepath, logging)
    if metadata:
        try:
            col.insert_one(metadata)
        except:
            logging.error("Error in inserting %s into 'dataset' database" % (path + "/" + filename))

print("Metadata imported")
logging.info("Metadata imported")


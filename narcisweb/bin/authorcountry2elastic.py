#!/usr/local/bin/python
from __future__ import print_function, absolute_import

# make sure you only have the DOIBoost 2017 files in the data/original folder

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from elasticsearch import helpers, Elasticsearch
from os import walk
import simplejson
import json
import logging
import ast

es = Elasticsearch(
    ['elasticsnarcis'],
    http_auth=('elastic', 'changeme'),
    port=9200
    )

path = "/exchange/Authors"
metadatapath = path

print("Importing metadata from %s" % metadatapath)

f = []
for (dirpath, dirnames, filenames) in walk("%s" % metadatapath):
    f.extend(filenames)

print("Files to be uploaded:", len(f))

i = 0
for filename in f:

    i += 1
    filepath = "%s/%s" % (path, filename)
    file = open(filepath, 'r')

    print(filepath)

    for lastline in file:
        metadata = json.loads(lastline)
        try:
            helpers.bulk(es, metadata, index='authorcountry', doc_type='metadata')
        except:
            print("Error.")

    print(i, "files out of ", len(f), "uploaded.")

print("Metadata imported")

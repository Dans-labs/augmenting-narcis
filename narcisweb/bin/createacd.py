import csv
import json
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from collections import defaultdict
import os

# get the mongo client
client = MongoClient('mongo')

# get the database
metadatadb = client.get_database('narcis')

# get the metadata collection
metacollection = metadatadb.doiboost2017

# get the elasticsearch connection
es_host = "elasticsnarcis"
es_local = Elasticsearch([es_host])
es = es_local

# set the elasticsearch index
searchindex = 'grid'

def list_to_csv(data, filename):
    """
    Add the dict to an existing json

    @param  array    The data
    @param  string   The folder name
    @param  string   The file name
    """

    # append the data to the file
    with open(filename, 'a') as fp:

        writer = csv.writer(fp)
        writer.writerow(data)

def create_author_country_data(metacollection, filename):
    """
    Create the dataset with author, affiliation and date combinations

    @param  dict    The metadata of a paper
    @return array   The list of GRID ids
    """

    # get the complete collection as an iterable
    subset = metacollection.find({})

    # make sure that the file exists
    file = open(filename, "w+")
    file.close()

    # add the country and date to the enrty of the author
    list_to_csv(['name', 'country', 'date'], filename)

    # loop over the metadata entries
    for metadata in subset:

        try:
            # get the date of the paper
            date = metadata['issued']

            # get the author information
            authors = metadata['authors']

            # loop over the authors in the list
            for author in authors:

                # get the full name
                name = author['fullname']

                # get the affiliation(s) of the author
                affiliations = author['affiliations']

                # only continue if there is information about the affiliation
                if affiliations:

                    # loop over the affiliation information
                    for affiliation in affiliations:

                        # get the identifiers
                        identifiers = affiliation['identifiers']

                        # the author needs to have an GRID id
                        if len(identifiers) < 2:
                            continue

                        # get the value of the second item, which is always the GRID id
                        gridID = identifiers[1]['value']

                        # retrieve the counrty of the authors affiliation in the GRID data
                        res = es.search(index=searchindex,
                                        body={"query": {"match": {'ID': "%s" % gridID }}})
                        country = res['hits']['hits'][0]['_source']['Country']

                        # add the country and date to the enrty of the author
                        list_to_csv([name, country, date], filename)
        except:
            continue

# run the functions
create_author_country_data(metacollection, "ACD.csv")

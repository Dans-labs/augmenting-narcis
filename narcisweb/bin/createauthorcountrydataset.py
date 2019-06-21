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

# set the elasticsearch index and doctype
searchindex = 'grid'

def dict_to_json(data, foldername, filename):
    """
    Add the dict to an existing json

    @param  dict     The data
    @param  string   The folder name
    @param  string   The file name
    """

    # append the data to the file
    with open(foldername + "/" + filename + ".json", 'a') as fp:

        # create json code of the dict
        json_data = json.dumps(data)

        # write the json to the file and add a new line
        fp.write(json_data + "\n")

def create_author_country_data(metacollection, foldername, filename):
    """
    Create the dataset with author, affiliation and date combinations

    @param  dict    The metadata of a paper
    @return array   The list of GRID ids
    """

    if not os.path.exists(foldername):
        os.makedirs(foldername)

    # get the complete collection as an iterable
    subset = metacollection.find()

    # index of the partial file
    file_index = 1

    # number of lines in the current file
    file_lines = 0

    # the maximum number of lines in the file
    max_file_size = 10000

    # make sure that the file exists
    file = open(foldername + "/" + filename+"-"+str(file_index) + ".json", "w+")
    file.close()

    # loop over the metadata entries
    for metadata in subset:

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
                    dict_to_json({'name': name, 'country': country, 'date': date},
                                 foldername, filename+"-"+str(file_index))

                    # the file can't contain too many lines or it will become too big
                    if file_lines >= 10000:

                        # add one to the file index
                        file_index += 1

                        # reset the number of lines
                        file_lines = 0

                        # make sure that the file exists
                        file = open(foldername + "/" + filename+"-"+str(file_index) + ".json", "w+")
                        file.close()

                    # add one to the max number of lines in the current file
                    file_lines += 1

# run the functions
create_author_country_data(metacollection, "Authors", "part")

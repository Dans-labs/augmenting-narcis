#!/usr/bin/python
# -*- coding: utf-8 -*-
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

URL = 'https://dataverse.nl/oai?set=dataversenl' #tilburg_oai'
URL = 'http://zandbak11.dans.knaw.nl/dataexplore/oai'
URL = "http://oai.narcis.nl/oai"
registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)
client = Client(URL, registry)
for header, metadata, _ in client.listRecords(metadataPrefix='oai_dc'):
    if URL:
        if metadata is None:
            continue

        metadata_fields = metadata.getMap().iteritems()
        for p, vv in metadata_fields:
            for v in vv:
                print "%s %s" % (p, v)
		s = v

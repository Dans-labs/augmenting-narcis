from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
import json

URL = 'http://oai.narcis.nl/oai' #?verb=GetRecord&metadataPrefix=oai_dc&identifier='
registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)
client = Client(URL, registry)

for header, record, other in client.listRecords(metadataPrefix='oai_dc'):
    if not record:
        continue
    datarecord = record.getMap()
    datarecord['id'] = header.identifier()
    datarecord['datestamp'] = str(header.datestamp())
    print(json.dumps(datarecord))

